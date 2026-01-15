# incremental-fetch

Build resilient data ingestion pipelines from APIs.

## When to Use

- Fetching paginated data from APIs
- Need to track progress and avoid duplicates
- Support both new data and historical backfills
- "ingest from API", "pull tweets", "backfill data"

## What It Does

Uses a **two-watermark pattern**:

| Watermark | Purpose |
|-----------|---------|
| `newest_id` | Fetch new data since last run |
| `oldest_id` | Backfill older data |

## Key Rules

1. Save **records** after each page (resilience)
2. Save **watermarks** once at end (correctness)
3. Never re-fetch existing data
4. Resume from interruption without data loss

## Resources

- `references/patterns.md` - Schemas and code examples
