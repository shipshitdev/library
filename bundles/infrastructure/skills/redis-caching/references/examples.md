# Redis Caching: Full Examples

Implementation-level TypeScript for each pattern referenced from SKILL.md.

## Redis Client Singleton

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

## Tag-Based Invalidation

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

## Sliding-Window Rate Limiting

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

## Session Storage

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
