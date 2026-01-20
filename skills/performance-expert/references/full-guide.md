# Performance Expert - Full Guide

## Core Performance Principles

### 1. Frontend Performance (React/Next.js)

**Bundle Optimization:**

- Code splitting by route
- Dynamic imports for heavy components
- Tree shaking enabled
- Remove unused dependencies
- Optimize large dependencies

**React Optimization:**

- Memoization (`useMemo`, `useCallback`)
- Component splitting to prevent re-renders
- Virtualization for long lists
- Lazy loading for routes/components
- React.memo for expensive components

**Next.js Optimization:**

- Server Components where appropriate
- Static generation (SSG) for static content
- ISR (Incremental Static Regeneration)
- Image optimization (`next/image`)
- Font optimization
- Script optimization

**Asset Optimization:**

- Images optimized (WebP, compression)
- Fonts subset and preloaded
- CSS minified and purged
- JavaScript minified
- Gzip/Brotli compression

### 2. Backend Performance (NestJS)

**API Response Times:**

- Target: < 200ms (p95)
- Database queries optimized
- Caching implemented
- Background jobs for heavy operations
- Connection pooling configured

**Query Optimization:**

- Indexes on frequently queried fields
- Compound indexes for multi-field queries
- Projections to limit fields
- Pagination implemented
- Aggregation pipelines optimized

**Caching Strategy:**

- Redis caching for frequently accessed data
- Cache invalidation strategy
- Cache TTL configured
- Cache warming for critical data

**Background Processing:**

- Heavy operations in queues (BullMQ)
- Async processing for non-critical tasks
- WebSocket for real-time updates
- No blocking operations in request handlers

### 3. Database Performance (MongoDB)

**Index Strategy:**

- Indexes on frequently queried fields
- Compound indexes for multi-field queries
- Indexes on foreign keys
- No unnecessary indexes
- Index usage monitored

**Query Optimization:**

- Early filtering (`$match` early in aggregation)
- Projection before expensive operations
- Limit and skip for pagination
- Sort with indexes
- Avoid full collection scans

**Aggregation Pipeline:**

- `$match` early in pipeline
- `$project` before expensive operations
- Index usage in aggregations
- Pipeline stages optimized
- Use `$lookup` efficiently

**Connection Management:**

- Connection pooling configured
- Connection limits set
- Idle connections closed
- Connection monitoring

### 4. Infrastructure Performance (AWS)

**CDN Configuration:**

- CloudFront caching configured
- Cache headers set correctly
- Static assets on CDN
- Edge locations optimized
- Cache invalidation strategy

**Lambda Optimization:**

- Cold start optimization
- Memory allocation optimized
- Connection pooling
- Provisioned concurrency (if needed)
- Function size minimized

**Database Performance:**

- MongoDB Atlas performance tier appropriate
- Read replicas configured (if needed)
- Connection pooling optimized
- Monitoring enabled
- Query performance tracked

## Performance Metrics

### Frontend Metrics (Core Web Vitals)

- **LCP (Largest Contentful Paint)**: < 2.5s
- **FID (First Input Delay)**: < 100ms
- **CLS (Cumulative Layout Shift)**: < 0.1
- **FCP (First Contentful Paint)**: < 1.8s
- **TTI (Time to Interactive)**: < 3.8s
- **TBT (Total Blocking Time)**: < 200ms

### Backend Metrics

- **API Response Time (p50)**: < 100ms
- **API Response Time (p95)**: < 200ms
- **API Response Time (p99)**: < 500ms
- **Database Query Time**: < 50ms (p95)
- **Error Rate**: < 0.1%
- **Throughput**: Monitor requests/second

### Database Metrics

- **Query Execution Time**: < 50ms (p95)
- **Index Hit Ratio**: > 95%
- **Connection Pool Usage**: < 80%
- **Slow Query Count**: < 1% of queries

## Common Performance Issues

### 1. N+1 Queries

**Problem:** Multiple database queries in loops

**Solution:**

```typescript
// BAD: N+1 queries
async findAll() {
  const users = await this.userModel.find({});
  for (const user of users) {
    user.posts = await this.postModel.find({ userId: user._id });
  }
  return users;
}

// GOOD: Aggregation pipeline
async findAll() {
  return this.userModel.aggregate([
    {
      $lookup: {
        from: 'posts',
        localField: '_id',
        foreignField: 'userId',
        as: 'posts'
      }
    }
  ]);
}
```

### 2. Large Bundle Size

**Problem:** JavaScript bundle too large

**Solution:**

- Code splitting by route
- Dynamic imports for heavy components
- Remove unused dependencies
- Optimize large libraries
- Tree shaking enabled

### 3. Missing Indexes

**Problem:** Slow database queries

**Solution:**

```typescript
// Create indexes
await db.collection('users').createIndex({ email: 1 });
await db.collection('posts').createIndex(
  { organization: 1, createdAt: -1 }
);
```

### 4. Unnecessary Re-renders

**Problem:** React components re-rendering too often

**Solution:**

```typescript
// Memoized
const processed = useMemo(
  () => data.map(item => process(item)),
  [data]
);

const handleClick = useCallback(() => {
  // handler
}, [dependencies]);
```

### 5. Blocking Operations

**Problem:** Heavy operations blocking request handlers

**Solution:**

- Move to background jobs
- Use queues (BullMQ)
- Async processing
- WebSocket for real-time updates

## Performance Optimization Patterns

### React Memoization

```typescript
// Memoize expensive computations
const expensiveValue = useMemo(() => {
  return heavyComputation(data);
}, [data]);

// Memoize callbacks
const handleClick = useCallback(() => {
  doSomething(id);
}, [id]);

// Memoize components
const ExpensiveComponent = React.memo(({ data }) => {
  return <div>{/* render */}</div>;
});
```

### Next.js Optimization

```typescript
// Static generation
export async function getStaticProps() {
  return {
    props: { data },
    revalidate: 3600 // ISR
  };
}

// Dynamic imports
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <Loading />,
  ssr: false
});

// Image optimization
import Image from 'next/image';
<Image src="/image.jpg" width={500} height={300} alt="..." />
```

### Database Query Optimization

```typescript
// Projection
const users = await this.userModel.find(
  { organization },
  { email: 1, name: 1 } // Only needed fields
);

// Pagination
const posts = await this.postModel.find({})
  .limit(20)
  .skip(page * 20)
  .sort({ createdAt: -1 });

// Indexed query
const users = await this.userModel.find({
  organization: orgId,  // Indexed field
  isDeleted: false
});
```

### Caching Strategy

```typescript
// Redis caching
async findAll(organizationId: string) {
  const cacheKey = `users:${organizationId}`;
  const cached = await this.redis.get(cacheKey);

  if (cached) {
    return JSON.parse(cached);
  }

  const users = await this.userModel.find({ organization: organizationId });
  await this.redis.setex(cacheKey, 3600, JSON.stringify(users));

  return users;
}
```

## Performance Testing

**Load Testing:**

```bash
# Using k6
k6 run load-test.js

# Test scenarios:
# - Normal load
# - Peak load
# - Stress test
# - Spike test
```

**Profiling:**

```bash
# Node.js profiling
node --prof app.js
node --prof-process isolate-*.log
```

**Bundle Analysis:**

```bash
# Analyze bundle
npm run build
npm run analyze

# Or with webpack-bundle-analyzer
ANALYZE=true npm run build
```

## Performance Checklist

### Frontend

- [ ] Bundle size optimized (< 200KB initial)
- [ ] Code splitting implemented
- [ ] Images optimized and lazy loaded
- [ ] Fonts optimized
- [ ] CSS purged
- [ ] JavaScript minified
- [ ] Gzip/Brotli compression enabled
- [ ] Caching headers configured
- [ ] React components memoized
- [ ] Virtualization for long lists

### Backend

- [ ] Database queries optimized
- [ ] Indexes created and used
- [ ] Caching implemented
- [ ] Background jobs for heavy operations
- [ ] Connection pooling configured
- [ ] Response compression enabled
- [ ] Rate limiting configured
- [ ] Monitoring enabled

### Database

- [ ] Indexes on frequently queried fields
- [ ] Compound indexes for multi-field queries
- [ ] Query projections used
- [ ] Pagination implemented
- [ ] Aggregation pipelines optimized
- [ ] Connection pooling configured
- [ ] Read replicas configured (if needed)

### Infrastructure

- [ ] CDN configured
- [ ] Caching strategy implemented
- [ ] Auto-scaling configured
- [ ] Monitoring and alerting set up
- [ ] Cost optimization reviewed

## Best Practices

1. **Measure First:** Profile before optimizing
2. **Set Targets:** Define performance budgets
3. **Monitor Continuously:** Track metrics over time
4. **Optimize Incrementally:** Make small, measurable changes
5. **Test Regularly:** Load test before deployment
6. **Cache Strategically:** Cache what makes sense
7. **Index Thoughtfully:** Indexes improve reads but slow writes
8. **Monitor Costs:** Balance performance and cost
