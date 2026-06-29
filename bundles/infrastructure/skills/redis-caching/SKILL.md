---
name: redis-caching
description: "Redis caching, rate limiting, session storage, pub/sub, and production integration patterns for TypeScript, Next.js, NestJS, and Prisma applications. Use when adding cache-aside or write-through caching, rate limiting, session or lock storage, pub/sub fanout, or reviewing Redis key design and TTLs."
metadata:
  version: "1.0.0"
  tags: "redis, caching, rate-limiting, sessions, prisma, nestjs, nextjs"
---

# Redis Caching

Implement Redis as a production support layer, not as a second database.

## When to Use

- Add cache-aside or write-through caching around Prisma or API reads.
- Protect expensive routes with rate limiting.
- Store short-lived sessions, verification state, locks, or counters.
- Add pub/sub or stream-backed event fanout.
- Review Redis key design, TTLs, invalidation, or connection handling.

For BullMQ job queue architecture, use `nestjs-queue-architect` instead of duplicating queue patterns here.

## First Decisions

1. Choose the runtime.
   - Long-lived Node.js or NestJS process: use `ioredis`.
   - Serverless or edge runtime: prefer the Upstash Redis SDK or REST API.
   - Background jobs: use BullMQ guidance from `nestjs-queue-architect`.
2. Define the cache contract before coding.
   - Source of truth: Prisma/database, upstream API, computed result, or session authority.
   - Freshness: hard TTL, stale-while-revalidate, explicit invalidation, or write-through.
   - Failure mode: fail open for cache reads, fail closed for auth/session/rate-limit writes.
3. Design keys and invalidation together.
   - Namespace every key: `app:env:entity:id:variant`.
   - Keep keys stable and inspectable.
   - Add TTLs to every cache, lock, session, and rate-limit key.

## Installation

```bash
bun add ioredis

# Optional serverless Redis
bun add @upstash/redis @upstash/ratelimit
```

Use one Redis client per process. Do not create a new TCP client per request.

```typescript
import Redis from "ioredis";

declare global {
  var redisClient: Redis | undefined;
}

export const redis =
  globalThis.redisClient ??
  new Redis(process.env.REDIS_URL ?? "redis://localhost:6379", {
    enableReadyCheck: true,
    lazyConnect: true,
    maxRetriesPerRequest: 3,
    retryStrategy(attempt) {
      return Math.min(attempt * 50, 2_000);
    },
  });

if (process.env.NODE_ENV !== "production") {
  globalThis.redisClient = redis;
}
```

Wire `error`, `connect`, and `reconnecting` events into the app logger or APM. Avoid logging credentials from connection URLs.

## Cache-Aside With Prisma

Use cache-aside for reads where brief staleness is acceptable.

```typescript
type CacheOptions = {
  ttlSeconds: number;
  jitterSeconds?: number;
};

const json = {
  encode(value: unknown) {
    return JSON.stringify(value);
  },
  decode<T>(value: string): T {
    return JSON.parse(value) as T;
  },
};

function withJitter(ttlSeconds: number, jitterSeconds = 30) {
  return ttlSeconds + Math.floor(Math.random() * jitterSeconds);
}

export async function getCached<T>(
  key: string,
  load: () => Promise<T>,
  options: CacheOptions,
): Promise<T> {
  const cached = await redis.get(key);
  if (cached !== null) {
    return json.decode<T>(cached);
  }

  const value = await load();
  const ttl = withJitter(options.ttlSeconds, options.jitterSeconds);
  await redis.set(key, json.encode(value), "EX", ttl);
  return value;
}
```

Example around Prisma:

```typescript
export async function getWorkspace(workspaceId: string) {
  return getCached(
    `app:prod:workspace:${workspaceId}`,
    () =>
      prisma.workspace.findUniqueOrThrow({
        where: { id: workspaceId },
        select: { id: true, name: true, plan: true, updatedAt: true },
      }),
    { ttlSeconds: 300, jitterSeconds: 60 },
  );
}
```

## Stampede Protection

Protect hot keys with a short lock. Keep the lock TTL small and release it only if this process owns the token.

```typescript
import { randomUUID } from "node:crypto";

const RELEASE_LOCK = `
if redis.call("GET", KEYS[1]) == ARGV[1] then
  return redis.call("DEL", KEYS[1])
end
return 0
`;

export async function getCachedWithLock<T>(
  key: string,
  load: () => Promise<T>,
  options: CacheOptions,
): Promise<T> {
  const cached = await redis.get(key);
  if (cached !== null) {
    return json.decode<T>(cached);
  }

  const lockKey = `lock:${key}`;
  const token = randomUUID();
  const locked = await redis.set(lockKey, token, "EX", 10, "NX");

  if (locked === "OK") {
    try {
      const value = await load();
      await redis.set(key, json.encode(value), "EX", withJitter(options.ttlSeconds));
      return value;
    } finally {
      await redis.eval(RELEASE_LOCK, 1, lockKey, token);
    }
  }

  await new Promise((resolve) => setTimeout(resolve, 75));
  const retry = await redis.get(key);
  if (retry !== null) {
    return json.decode<T>(retry);
  }

  return load();
}
```

## Invalidation

Prefer direct invalidation for known keys. Use tag sets when one mutation affects many keys.

```typescript
export async function cacheSetWithTags(
  key: string,
  value: unknown,
  tags: string[],
  ttlSeconds: number,
) {
  const pipeline = redis.pipeline();
  pipeline.set(key, json.encode(value), "EX", ttlSeconds);

  for (const tag of tags) {
    const tagKey = `cachetag:${tag}`;
    pipeline.sadd(tagKey, key);
    pipeline.expire(tagKey, ttlSeconds + 60);
  }

  await pipeline.exec();
}

export async function invalidateTag(tag: string) {
  const tagKey = `cachetag:${tag}`;
  const keys = await redis.smembers(tagKey);
  if (keys.length > 0) {
    await redis.unlink(...keys);
  }
  await redis.del(tagKey);
}
```

Use `SCAN` instead of `KEYS` for emergency pattern cleanup. Do not put pattern invalidation on hot request paths.

## Rate Limiting

Use sorted sets for sliding-window limits when exactness matters.

```typescript
import { randomUUID } from "node:crypto";

type RateLimitResult = {
  allowed: boolean;
  limit: number;
  remaining: number;
  resetAt: Date;
};

export async function slidingWindowRateLimit(
  subject: string,
  limit: number,
  windowSeconds: number,
): Promise<RateLimitResult> {
  const key = `ratelimit:${subject}`;
  const now = Date.now();
  const windowStart = now - windowSeconds * 1_000;
  const member = `${now}:${randomUUID()}`;

  const results = await redis
    .multi()
    .zremrangebyscore(key, 0, windowStart)
    .zadd(key, now, member)
    .zcard(key)
    .pexpire(key, windowSeconds * 1_000)
    .exec();

  const count = Number(results?.[2]?.[1] ?? 0);

  return {
    allowed: count <= limit,
    limit,
    remaining: Math.max(limit - count, 0),
    resetAt: new Date(now + windowSeconds * 1_000),
  };
}
```

For public traffic, set response headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `Retry-After`.

## Sessions And Verification State

- Store opaque session IDs or token hashes, not raw JWTs or long-lived secrets.
- Set TTL on every session key.
- Regenerate sessions after privilege changes.
- Delete sessions on logout, account deletion, and password reset.
- Treat Redis write failure as auth failure for login, logout, MFA, and password reset flows.

```typescript
type SessionRecord = {
  userId: string;
  workspaceId: string;
  issuedAt: string;
};

export async function createSession(sessionId: string, session: SessionRecord) {
  await redis.set(
    `session:${sessionId}`,
    json.encode(session),
    "EX",
    60 * 60 * 24 * 7,
  );
}
```

## Pub/Sub And Streams

- Use pub/sub for ephemeral fanout where missed messages are acceptable.
- Use streams when consumers need replay, backpressure, or durable delivery.
- Keep payloads small; store large objects elsewhere and publish IDs.
- Add consumer observability: lag, dead letters, retries, and handler errors.

## Production Checklist

- [ ] All cache, lock, session, and rate-limit keys have TTLs.
- [ ] Cache reads fail open where possible; auth and rate-limit writes fail closed.
- [ ] Hot keys use TTL jitter or stampede protection.
- [ ] No request path uses `KEYS`, unbounded `SMEMBERS`, or large `HGETALL`.
- [ ] Invalidation is tested alongside the write path.
- [ ] Redis metrics cover latency, hit rate, memory, evictions, blocked clients, and reconnects.
- [ ] Local tests cover cache hit, cache miss, Redis down, invalidation, and rate-limit exceeded.
