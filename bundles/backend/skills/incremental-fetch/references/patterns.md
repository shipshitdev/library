# Incremental Fetch Patterns

Code patterns and schemas for implementing resilient incremental data fetching.

## Database Schema

### Ingestion State Table

```sql
CREATE TABLE IF NOT EXISTS ingestion_state (
    asset_id VARCHAR NOT NULL,      -- entity being fetched (user, account, symbol)
    data_type VARCHAR NOT NULL,     -- watermark type (see below)
    last_id VARCHAR,                -- watermark value (string for large ints)
    last_timestamp TIMESTAMP,       -- optional: timestamp-based watermark
    updated_at TIMESTAMP DEFAULT now(),
    PRIMARY KEY (asset_id, data_type)
);
```

### Why Separate Rows for Each Watermark Type

The `data_type` column stores different watermark types as separate rows, not columns:

```
asset_id    | data_type       | last_id
------------|-----------------|--------
@elonmusk   | tweets          | 1234567  (newest fetched)
@elonmusk   | tweets_oldest   | 1000000  (oldest fetched)
BTCUSD      | prices_1h       | 9876543
BTCUSD      | prices_1h_oldest| 8000000
```

This design allows:

- N watermark types per entity without schema changes
- Different data types (tweets, prices_1h, prices_1d) tracked independently
- Bidirectional fetching (newest + oldest) per data type

### Watermark Functions

```python
def get_ingestion_state(conn, asset_id: str, data_type: str) -> dict | None:
    result = conn.execute("""
        SELECT last_id, last_timestamp, updated_at
        FROM ingestion_state
        WHERE asset_id = ? AND data_type = ?
    """, [asset_id, data_type]).fetchone()

    if not result:
        return None
    return {"last_id": result[0], "last_timestamp": result[1]}


def update_ingestion_state(conn, asset_id: str, data_type: str,
                           last_id: str = None, last_timestamp = None):
    conn.execute("""
        INSERT INTO ingestion_state (asset_id, data_type, last_id, last_timestamp, updated_at)
        VALUES (?, ?, ?, ?, now())
        ON CONFLICT (asset_id, data_type) DO UPDATE SET
            last_id = COALESCE(EXCLUDED.last_id, ingestion_state.last_id),
            last_timestamp = COALESCE(EXCLUDED.last_timestamp, ingestion_state.last_timestamp),
            updated_at = now()
    """, [asset_id, data_type, last_id, last_timestamp])
```

## Fetch Loop Pattern

```python
def fetch_for_asset(asset_id: str, backfill: bool = False, max_pages: int = 50):
    conn = get_connection()

    # Get watermarks (separate rows in DB)
    state = get_ingestion_state(conn, asset_id, "tweets")
    oldest_state = get_ingestion_state(conn, asset_id, "tweets_oldest")

    newest_id = state.get("last_id") if state else None
    oldest_id = oldest_state.get("last_id") if oldest_state else None

    # Determine fetch mode
    if backfill and oldest_id:
        since_id = None
        until_id = oldest_id  # Fetch older than this
    elif newest_id:
        since_id = newest_id  # Fetch newer than this
        until_id = None
    else:
        since_id = None  # Full fetch
        until_id = None

    # Track watermarks for THIS run
    run_newest_id = None
    run_oldest_id = None
    pagination_token = None

    for page in range(max_pages):
        # Fetch one page
        items, next_token = fetch_page(
            asset_id,
            since_id=since_id,
            until_id=until_id,
            pagination_token=pagination_token
        )

        if not items:
            break

        # Track watermarks (compare as INT for numeric IDs)
        for item in items:
            item_id = item["id"]
            if run_newest_id is None or int(item_id) > int(run_newest_id):
                run_newest_id = item_id
            if run_oldest_id is None or int(item_id) < int(run_oldest_id):
                run_oldest_id = item_id

        # SAVE DATA IMMEDIATELY after each page (resilience)
        insert_items(conn, asset_id, items)
        print(f"Page {page + 1}: {len(items)} items saved")

        if not next_token:
            break
        pagination_token = next_token

    # UPDATE WATERMARKS ONCE at end (correctness)
    if run_newest_id:
        if newest_id is None or int(run_newest_id) > int(newest_id):
            update_ingestion_state(conn, asset_id, "tweets", last_id=run_newest_id)

    if run_oldest_id:
        update_ingestion_state(conn, asset_id, "tweets_oldest", last_id=run_oldest_id)

    conn.close()
```

## Retry Pattern

```python
import time
import random

def fetch_with_retry(url: str, params: dict, max_attempts: int = 3):
    for attempt in range(max_attempts):
        try:
            response = client.get(url, params=params, timeout=30.0)

            if response.status_code == 429:  # Rate limit
                reset_ts = response.headers.get("x-rate-limit-reset", "0")
                wait = max(0, int(reset_ts) - int(time.time()) + 5)

                if wait > 120:  # Don't wait more than 2 minutes
                    return None, "rate_limit_skip"

                print(f"Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue

            if response.status_code != 200:
                return None, f"http_{response.status_code}"

            return response.json(), None

        except TimeoutError:
            # Exponential backoff with jitter
            wait = (2 ** attempt) * 5 + random.uniform(0, 3)
            print(f"Timeout, waiting {wait:.0f}s (attempt {attempt + 1}/{max_attempts})")
            time.sleep(wait)

    return None, "max_retries_exceeded"
```

## Gotchas

### 1. Compare IDs as integers

Tweet IDs and similar identifiers are numeric but may be stored as strings. Always compare as int:

```python
# WRONG: string comparison ("9" > "10" is True)
if item_id > run_newest_id:

# RIGHT: numeric comparison
if int(item_id) > int(run_newest_id):
```

### 2. Data saves vs watermark updates are DIFFERENT

This is the #1 mistake. The timing is different for a reason:

- **Data**: Save per-page for resilience (crash recovery)
- **Watermarks**: Save at end for correctness (don't claim progress until complete)

### 3. Handle backfill-without-data error

If user requests `--backfill` but no data exists yet, error loudly:

```python
if backfill and not oldest_id:
    oldest_in_db = conn.execute("SELECT MIN(id) FROM items WHERE asset_id = ?", [asset_id]).fetchone()[0]
    if not oldest_in_db:
        raise Error("Cannot backfill - no data exists. Run without --backfill first.")
```

### 4. Rate limit skip tracking

When you hit rate limits and skip an asset, record it for next run:

```python
FETCH_STATE_FILE = Path("data/fetch_state.json")

def write_fetch_state(skipped_assets: list, reason: str):
    state = {
        "last_run": datetime.now().isoformat(),
        "skipped_assets": skipped_assets,
        "skip_reason": reason
    }
    FETCH_STATE_FILE.write_text(json.dumps(state, indent=2))
```

Then prioritize skipped assets on next run.

### 5. Use ON CONFLICT for upserts

When inserting data, handle duplicates gracefully:

```python
conn.execute("""
    INSERT INTO items (id, asset_id, data, fetched_at)
    VALUES (?, ?, ?, now())
    ON CONFLICT (id) DO UPDATE SET
        data = EXCLUDED.data,
        fetched_at = now()
""", [item_id, asset_id, data])
```

This allows re-running without duplicate key errors and updates stale data.
