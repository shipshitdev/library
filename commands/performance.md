# Performance - Performance Analysis Command

**Purpose:** Analyze and optimize performance for React, Next.js, NestJS applications covering frontend, backend, database, and infrastructure.

## When to Use

- Performance issues reported
- Slow page loads
- High API response times
- Database query optimization
- Infrastructure optimization
- Before scaling

## Project Context Discovery

**Before analyzing, discover the project's setup:**

1. **Identify Project Type:**
   - Check for React/Next.js frontend
   - Check for NestJS backend
   - Identify database (MongoDB)
   - Review infrastructure (AWS)

2. **Discover Performance Tools:**
   - Check for Lighthouse CI
   - Look for performance monitoring (New Relic, Datadog)
   - Review bundle analyzers (webpack-bundle-analyzer)
   - Check for APM tools

3. **Identify Performance Metrics:**
   - Check for performance budgets
   - Review Core Web Vitals
   - Check API response time targets
   - Review database query performance

## Performance Analysis Workflow

### Phase 1: Frontend Performance (React/Next.js)

**1.1 Bundle Analysis**

```bash
# Analyze bundle size
npm run build
npm run analyze

# Or with webpack-bundle-analyzer
ANALYZE=true npm run build
```

**Check for:**

- ✅ Bundle size under thresholds
- ✅ Code splitting implemented
- ✅ Tree shaking working
- ✅ Unused dependencies removed
- ✅ Large dependencies optimized

**1.2 Core Web Vitals**

```bash
# Run Lighthouse
npx lighthouse https://[site-url] --view

# Or in CI
npm run lighthouse:ci
```

**Metrics to check:**

- **LCP (Largest Contentful Paint)**: < 2.5s
- **FID (First Input Delay)**: < 100ms
- **CLS (Cumulative Layout Shift)**: < 0.1
- **FCP (First Contentful Paint)**: < 1.8s
- **TTI (Time to Interactive)**: < 3.8s

**1.3 React Performance**

**Check for:**

- ✅ Memoization used appropriately (`useMemo`, `useCallback`)
- ✅ Components split to prevent re-renders
- ✅ Virtualization for long lists
- ✅ Lazy loading for routes/components
- ✅ Image optimization

**Common Issues:**

```typescript
// ❌ BAD: Unnecessary re-renders
function Component({ data }) {
  const processed = data.map(item => process(item));
  return <List items={processed} />;
}

// ✅ GOOD: Memoized
function Component({ data }) {
  const processed = useMemo(
    () => data.map(item => process(item)),
    [data]
  );
  return <List items={processed} />;
}
```

**1.4 Next.js Performance**

**Check for:**

- ✅ Server Components used where appropriate
- ✅ Static generation (SSG) for static content
- ✅ ISR (Incremental Static Regeneration) configured
- ✅ Image optimization (`next/image`)
- ✅ Font optimization
- ✅ Script optimization

**1.5 Asset Optimization**

**Check for:**

- ✅ Images optimized (WebP, compression)
- ✅ Fonts subset and preloaded
- ✅ CSS minified and purged
- ✅ JavaScript minified
- ✅ Gzip/Brotli compression enabled

### Phase 2: Backend Performance (NestJS)

**2.1 API Response Times**

**Check for:**

- ✅ Response times < 200ms (p95)
- ✅ Database queries optimized
- ✅ Caching implemented
- ✅ Background jobs for heavy operations
- ✅ Connection pooling configured

**2.2 Database Query Optimization**

**MongoDB-specific:**

```typescript
// ❌ BAD: N+1 queries
async findAll() {
  const users = await this.userModel.find({});
  for (const user of users) {
    user.posts = await this.postModel.find({ userId: user._id });
  }
  return users;
}

// ✅ GOOD: Aggregation pipeline
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

**2.3 Caching Strategy**

**Check for:**

- ✅ Redis caching for frequently accessed data
- ✅ Cache invalidation strategy
- ✅ Cache TTL configured
- ✅ Cache warming for critical data

**2.4 Background Jobs**

**Check for:**

- ✅ Heavy operations in queues (BullMQ)
- ✅ Async processing for non-critical tasks
- ✅ WebSocket for real-time updates
- ✅ No blocking operations in request handlers

### Phase 3: Database Performance (MongoDB)

**3.1 Index Analysis**

```bash
# Check indexes
db.collection.getIndexes()

# Analyze query performance
db.collection.explain('executionStats').find({ organization: 'org123' })
```

**Check for:**

- ✅ Indexes on frequently queried fields
- ✅ Compound indexes for multi-field queries
- ✅ Indexes on foreign keys
- ✅ No unnecessary indexes

**3.2 Query Optimization**

**Common optimizations:**

```typescript
// ❌ BAD: Fetching all fields
const users = await this.userModel.find({ organization });

// ✅ GOOD: Projection
const users = await this.userModel.find(
  { organization },
  { email: 1, name: 1 } // Only needed fields
);

// ❌ BAD: No limit
const posts = await this.postModel.find({});

// ✅ GOOD: Pagination
const posts = await this.postModel.find({})
  .limit(20)
  .skip(page * 20)
  .sort({ createdAt: -1 });
```

**3.3 Aggregation Pipeline Optimization**

**Check for:**

- ✅ Early filtering (`$match` early)
- ✅ Projection before expensive operations
- ✅ Index usage in aggregations
- ✅ Pipeline stages optimized

### Phase 4: Infrastructure Performance (AWS)

**4.1 CDN Configuration**

**Check for:**

- ✅ CloudFront caching configured
- ✅ Cache headers set correctly
- ✅ Static assets on CDN
- ✅ Edge locations optimized

**4.2 Lambda Performance**

**Check for:**

- ✅ Cold start optimization
- ✅ Memory allocation optimized
- ✅ Connection pooling
- ✅ Provisioned concurrency (if needed)

**4.3 Database Performance**

**Check for:**

- ✅ MongoDB Atlas performance tier
- ✅ Read replicas configured
- ✅ Connection pooling
- ✅ Monitoring enabled

**4.4 Auto-Scaling**

**Check for:**

- ✅ Auto-scaling configured
- ✅ Scaling policies optimized
- ✅ Resource limits set
- ✅ Cost optimization

## Performance Metrics to Track

### Frontend Metrics

- **Bundle Size**: < 200KB initial load
- **Time to First Byte (TTFB)**: < 600ms
- **First Contentful Paint (FCP)**: < 1.8s
- **Largest Contentful Paint (LCP)**: < 2.5s
- **Total Blocking Time (TBT)**: < 200ms
- **Cumulative Layout Shift (CLS)**: < 0.1

### Backend Metrics

- **API Response Time (p95)**: < 200ms
- **API Response Time (p99)**: < 500ms
- **Database Query Time**: < 50ms (p95)
- **Error Rate**: < 0.1%
- **Throughput**: Requests per second

### Database Metrics

- **Query Execution Time**: < 50ms (p95)
- **Index Hit Ratio**: > 95%
- **Connection Pool Usage**: < 80%
- **Slow Query Count**: < 1% of queries

## Performance Optimization Checklist

### Frontend

- [ ] Bundle size optimized
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

## Performance Testing

**Load Testing:**

```bash
# Using k6 or similar
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

# Analyze profile
node --prof-process isolate-*.log
```

## Common Performance Issues

### 1. N+1 Queries

**Problem:** Multiple database queries in loops

**Solution:** Use aggregation pipelines, batch queries, or eager loading

### 2. Large Bundle Size

**Problem:** JavaScript bundle too large

**Solution:** Code splitting, tree shaking, remove unused dependencies

### 3. Missing Indexes

**Problem:** Slow database queries

**Solution:** Add indexes on frequently queried fields

### 4. Unnecessary Re-renders

**Problem:** React components re-rendering too often

**Solution:** Memoization, component splitting, React.memo

### 5. Blocking Operations

**Problem:** Heavy operations blocking request handlers

**Solution:** Move to background jobs, use queues

## Output Format

When analyzing performance:

```
⚡ PERFORMANCE ANALYSIS

Project: [project-name]
Date: [date]
Focus: [frontend/api/database]

📊 FRONTEND METRICS

Bundle Size:
- Current: 450KB
- Target: < 200KB
- Status: ⚠️  Exceeds target

Core Web Vitals:
- LCP: 2.1s ✅ (Target: < 2.5s)
- FID: 85ms ✅ (Target: < 100ms)
- CLS: 0.05 ✅ (Target: < 0.1)

🔍 ISSUES FOUND

1. Large Bundle Size
   Impact: Slow initial load
   Solution: Implement code splitting
   Priority: HIGH

2. Missing Image Optimization
   Impact: Slow image loading
   Solution: Use next/image, WebP format
   Priority: MEDIUM

📊 BACKEND METRICS

API Response Times:
- p50: 120ms ✅
- p95: 280ms ⚠️  (Target: < 200ms)
- p99: 450ms ⚠️  (Target: < 500ms)

Database Queries:
- Average: 45ms ✅
- p95: 120ms ⚠️  (Target: < 50ms)
- Slow queries: 2% ⚠️

🔍 ISSUES FOUND

1. Slow Database Queries
   Impact: High p95 response time
   Solution: Add indexes, optimize queries
   Priority: HIGH

2. Missing Caching
   Impact: Repeated expensive operations
   Solution: Implement Redis caching
   Priority: MEDIUM

💡 RECOMMENDATIONS

1. Implement code splitting for routes
2. Add database indexes on frequently queried fields
3. Implement Redis caching for API responses
4. Optimize images (WebP, lazy loading)
5. Add database query monitoring

📋 OPTIMIZATION PLAN

Week 1:
- Add missing database indexes
- Implement code splitting

Week 2:
- Set up Redis caching
- Optimize images

Week 3:
- Monitor improvements
- Fine-tune optimizations
```

---

**Created:** 2025-12-24
**Purpose:** Comprehensive performance analysis and optimization
**Focus:** Frontend (React/Next.js), Backend (NestJS), Database (MongoDB), Infrastructure (AWS)
