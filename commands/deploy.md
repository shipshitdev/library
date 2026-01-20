# Deploy - Deployment Workflow Command

**Purpose:** Streamline deployment workflows for React, Next.js, NestJS applications to various environments (AWS, Vercel, etc.)

## When to Use

- Deploying to staging/production
- Setting up deployment pipelines
- Configuring CI/CD workflows
- Managing environment-specific deployments

## Project Context Discovery

**Before deploying, discover the project's setup:**

1. **Identify Project Type:**
   - Scan for `package.json` to detect framework (React, Next.js, NestJS)
   - Check for `next.config.js` (Next.js)
   - Check for `nest-cli.json` (NestJS)
   - Check for `vite.config.js` or `webpack.config.js` (React/Vite)

2. **Discover Deployment Platform:**
   - Check for AWS config files (`serverless.yml`, `cloudformation.yml`, `terraform/`)
   - Check for Vercel config (`vercel.json`)
   - Check for Docker files (`Dockerfile`, `docker-compose.yml`)
   - Review `.github/workflows/` for CI/CD
   - Check environment variables for deployment URLs

3. **Identify Build Commands:**
   - Check `package.json` scripts for build commands
   - Look for `build`, `build:prod`, `build:staging` scripts
   - Check for framework-specific build commands

4. **Check Environment Configuration:**
   - Review `.env.example` or `.env.template`
   - Check for environment-specific configs
   - Identify required environment variables

## Deployment Workflow

### Phase 1: Pre-Deployment Checks

**1.1 Code Quality Checks**

```bash
# Run linter
npm run lint
# or
pnpm lint

# Run type checking
npm run type-check
# or
tsc --noEmit

# Run tests (if not disabled locally)
# Note: Check project rules - some projects run tests only in CI
```

**1.2 Build Verification**

```bash
# Test build locally
npm run build
# or
pnpm build

# Verify build output exists
ls -la dist/  # NestJS
ls -la .next/  # Next.js
ls -la build/  # React
```

**1.3 Environment Validation**

- Verify all required environment variables are set
- Check database connection strings
- Validate API keys and secrets
- Confirm deployment target matches environment

**1.4 Security Checks**

- Run security audit: `npm audit` or `pnpm audit`
- Check for exposed secrets in code
- Verify authentication/authorization configs
- Review dependency vulnerabilities

### Phase 2: Deployment Execution

**2.1 Framework-Specific Deployment**

#### Next.js (Vercel)

```bash
# Deploy to Vercel
vercel --prod  # Production
vercel         # Preview

# Or via GitHub Actions
# Check .github/workflows/deploy.yml
```

#### NestJS (AWS/Docker)

```bash
# Build Docker image
docker build -t [project-name]:[tag] .

# Push to registry
docker push [registry]/[project-name]:[tag]

# Deploy via AWS ECS/Fargate
# Or use serverless framework
serverless deploy --stage [environment]
```

#### React (Static Hosting)

```bash
# Build static files
npm run build

# Deploy to S3/CloudFront
aws s3 sync build/ s3://[bucket-name] --delete
aws cloudfront create-invalidation --distribution-id [id] --paths "/*"
```

**2.2 Database Migrations**

```bash
# Run migrations before deployment
npm run migrate:up
# or
npx prisma migrate deploy  # Prisma
# or custom migration script
```

**2.3 Environment-Specific Config**

- Update environment variables in deployment platform
- Configure feature flags
- Set up monitoring and logging
- Configure CDN/caching rules

### Phase 3: Post-Deployment Verification

**3.1 Health Checks**

```bash
# Check deployment health
curl https://[deployment-url]/health
curl https://[deployment-url]/api/health

# Verify API endpoints
curl https://[deployment-url]/api/v1/status
```

**3.2 Smoke Tests**

- Test critical user flows
- Verify API endpoints respond
- Check database connectivity
- Validate authentication flow

**3.3 Monitoring**

- Check deployment logs
- Monitor error rates
- Verify metrics collection
- Check alert configurations

## Environment-Specific Workflows

### Staging Deployment

```bash
/deploy staging
```

**Process:**

1. Build with staging config
2. Deploy to staging environment
3. Run smoke tests
4. Notify team of deployment

### Production Deployment

```bash
/deploy production
```

**Process:**

1. **Require confirmation** - Production deployments are critical
2. Create deployment branch/tag
3. Run full test suite (in CI)
4. Build production bundle
5. Deploy with zero-downtime strategy
6. Run health checks
7. Monitor for issues
8. Rollback plan ready

## AWS-Specific Patterns

### ECS/Fargate Deployment

```bash
# Update task definition
aws ecs update-service \
  --cluster [cluster-name] \
  --service [service-name] \
  --force-new-deployment

# Monitor deployment
aws ecs describe-services \
  --cluster [cluster-name] \
  --services [service-name]
```

### Lambda Deployment

```bash
# Deploy serverless function
serverless deploy --stage [environment]

# Or AWS SAM
sam build
sam deploy --guided
```

### S3/CloudFront Static Deployment

```bash
# Build and sync
npm run build
aws s3 sync build/ s3://[bucket] --delete --cache-control "max-age=31536000"

# Invalidate CloudFront
aws cloudfront create-invalidation \
  --distribution-id [id] \
  --paths "/*"
```

## MongoDB Considerations

**Before deployment:**

1. **Database Migrations:**

   ```bash
   # Run migrations
   npm run migrate:up
   
   # Or use migration tool
   npx migrate-mongo up
   ```

2. **Connection String:**
   - Verify MongoDB connection string for environment
   - Check replica set configuration
   - Verify network access (VPC, security groups)

3. **Index Verification:**
   - Ensure indexes are created
   - Check index performance
   - Verify compound indexes

## Rollback Procedures

**If deployment fails:**

1. **Identify Issue:**
   - Check deployment logs
   - Review error messages
   - Check health endpoints

2. **Rollback Strategy:**

   **Docker/ECS:**

   ```bash
   # Revert to previous task definition
   aws ecs update-service \
     --cluster [cluster] \
     --service [service] \
     --task-definition [previous-version]
   ```

   **Vercel:**

   ```bash
   # Revert to previous deployment
   vercel rollback
   ```

   **Database:**

   ```bash
   # Rollback migrations if needed
   npm run migrate:down
   ```

3. **Post-Rollback:**
   - Verify rollback successful
   - Check application health
   - Document issue for investigation

## Safety Features

**Always include:**

1. **Confirmation for Production:**

   ```
   ⚠️  WARNING: Deploying to PRODUCTION
   
   Current version: v1.2.3
   New version: v1.2.4
   
   Changes:
   - Feature X
   - Bug fix Y
   
   Continue? (y/n)
   ```

2. **Pre-Deployment Checklist:**
   - [ ] All tests passing
   - [ ] Build successful
   - [ ] Environment variables configured
   - [ ] Database migrations ready
   - [ ] Rollback plan prepared
   - [ ] Team notified

3. **Deployment Monitoring:**
   - Watch deployment logs
   - Monitor error rates
   - Check performance metrics
   - Verify functionality

## Common Deployment Patterns

### Blue-Green Deployment

```bash
# Deploy new version alongside old
# Switch traffic when verified
# Keep old version for quick rollback
```

### Canary Deployment

```bash
# Deploy to small percentage of traffic
# Monitor metrics
# Gradually increase if healthy
# Rollback if issues detected
```

### Rolling Deployment

```bash
# Update instances one at a time
# Maintain service availability
# Monitor each instance
```

## Integration with CI/CD

**Discover CI/CD setup:**

1. **Check GitHub Actions:**

   ```bash
   ls .github/workflows/
   ```

2. **Review Pipeline:**
   - Build steps
   - Test steps
   - Deployment steps
   - Environment configuration

3. **Deploy via CI/CD:**

   ```bash
   # Trigger deployment workflow
   gh workflow run deploy.yml \
     --ref main \
     -f environment=production
   ```

## Error Handling

**Common Issues:**

1. **Build Failures:**
   - Check build logs
   - Verify dependencies
   - Check environment variables
   - Review TypeScript errors

2. **Deployment Timeouts:**
   - Check network connectivity
   - Verify deployment platform status
   - Review resource limits
   - Check deployment logs

3. **Database Connection Issues:**
   - Verify connection strings
   - Check network access
   - Review security groups
   - Test connection manually

## Best Practices

1. **Always test builds locally** before deploying
2. **Use feature flags** for gradual rollouts
3. **Monitor deployments** closely
4. **Have rollback plan** ready
5. **Document deployment process** in project docs
6. **Automate repetitive steps** via CI/CD
7. **Version deployments** for tracking
8. **Notify team** of deployments

## Output Format

When deploying, show:

```
🚀 DEPLOYMENT STARTED

Environment: [environment]
Project: [project-name]
Version: [version]
Platform: [platform]

📋 PRE-DEPLOYMENT CHECKS
✅ Linter passed
✅ Type check passed
✅ Build successful
✅ Environment variables configured
✅ Database migrations ready

🔄 DEPLOYING...
[Progress indicators]

✅ DEPLOYMENT COMPLETE

URL: https://[deployment-url]
Health: https://[deployment-url]/health

📊 MONITORING
- Error rate: 0.01%
- Response time: 120ms
- Status: Healthy

💡 NEXT STEPS
1. Run smoke tests
2. Monitor for 15 minutes
3. Verify critical flows
```

---

**Created:** 2025-12-24
**Purpose:** Streamline deployment workflows across React, Next.js, NestJS projects
**Platforms:** AWS, Vercel, Docker, Static Hosting
