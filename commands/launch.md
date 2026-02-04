# Launch - Startup Launch Workflow

**Purpose:** Orchestrate complete startup launch workflow from pre-launch checks through post-launch verification

## Usage

```bash
/launch              # Full launch workflow (interactive)
/launch --check      # Pre-launch checklist only (dry run)
/launch --verify     # Post-launch verification only
```

## When to Use

Use this command when:

- Ready to launch a new product/feature to production
- Need comprehensive pre-launch validation
- Want to ensure all systems are ready before going live
- Need post-launch verification and monitoring setup

## What This Command Does

Orchestrates a complete launch workflow:

1. **Pre-Launch Checks** - Tests, security, performance, monitoring setup
2. **Deployment** - Executes deployment workflow (integrates with `/deploy`)
3. **Post-Launch Verification** - Health checks, smoke tests, monitoring validation
4. **Launch Report** - Generates comprehensive launch documentation

---

## Workflow

### Phase 1: Pre-Launch Checks

**1.1 Code Quality & Tests**

```bash
# Run linter
npm run lint || pnpm lint

# Type checking
npm run type-check || tsc --noEmit

# Build verification
npm run build || pnpm build

# Tests (push to CI if required by project rules)
# Check .agents/SYSTEM/critical/ for test rules
```

**Checklist:**

- [ ] Linter passes with no errors
- [ ] TypeScript compiles successfully
- [ ] Build completes without errors
- [ ] Tests pass (in CI if required)

**1.2 Security Audit**

```bash
# Security audit
npm audit || pnpm audit

# Check for exposed secrets
grep -r "password\|secret\|key" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" . | grep -v "node_modules" | grep -v ".env"

# Review authentication/authorization configs
```

**Checklist:**

- [ ] No critical security vulnerabilities
- [ ] No secrets hardcoded in source
- [ ] Authentication properly configured
- [ ] Authorization rules in place

**1.3 Performance Checks**

```bash
# Check bundle sizes (if applicable)
# Next.js: Check .next/analyze output
# NestJS: Check dist/ size

# Review performance metrics
# Use /performance command if needed
```

**Checklist:**

- [ ] Bundle sizes within acceptable limits
- [ ] No obvious performance bottlenecks
- [ ] Database queries optimized
- [ ] Images/assets optimized

**1.4 Monitoring Setup Verification**

```bash
# Check if Sentry is configured
grep -r "SENTRY_DSN" .env* || true
grep -r "@sentry" package.json || true

# Check if Google Analytics is configured
grep -r "GA_MEASUREMENT_ID\|gtag" . || true
```

**Checklist:**

- [ ] Sentry DSN configured (if using Sentry)
- [ ] Google Analytics configured (if using GA)
- [ ] Error tracking active
- [ ] Analytics events tracked

**1.5 Environment Validation**

```bash
# Check required environment variables
cat .env.example 2>/dev/null || cat .env.template 2>/dev/null || true

# Verify production environment variables are set
# (This will vary by deployment platform)
```

**Checklist:**

- [ ] All required environment variables documented
- [ ] Production environment variables set
- [ ] Database connection strings valid
- [ ] API keys and secrets configured

**1.6 Documentation**

```bash
# Verify README is up to date
cat README.md

# Check API documentation exists (if applicable)
# Check for .agents/SYSTEM/ARCHITECTURE.md updates
```

**Checklist:**

- [ ] README.md up to date
- [ ] API documentation complete (if applicable)
- [ ] Architecture docs current
- [ ] Changelog updated (if applicable)

### Phase 2: Deployment

**2.1 Pre-Deployment**

If all pre-launch checks pass, proceed to deployment:

```bash
# Use /deploy command patterns
# This integrates with existing /deploy workflow
```

**Deployment Steps:**

1. Run migrations (if database changes)
2. Deploy to staging first (if staging environment exists)
3. Run smoke tests on staging
4. Deploy to production
5. Monitor deployment logs

**Integration with `/deploy` command:**

The launch command orchestrates deployment but delegates actual deployment execution to the `/deploy` command workflow. Reference `.cursor/commands/deploy.md` for deployment specifics.

### Phase 3: Post-Launch Verification

**3.1 Health Checks**

```bash
# Check API health endpoint
curl https://[production-url]/health || curl https://[production-url]/api/health

# Check frontend loads
curl -I https://[production-url]/

# Verify database connectivity (if health endpoint includes this)
```

**Checklist:**

- [ ] Health endpoint returns 200 OK
- [ ] Frontend loads successfully
- [ ] Database connections working
- [ ] All critical services running

**3.2 Smoke Tests**

Test critical user flows:

- [ ] User can sign up / sign in
- [ ] Core feature functionality works
- [ ] API endpoints respond correctly
- [ ] Payment flow works (if applicable)
- [ ] Error handling works (test error scenarios)

**3.3 Monitoring Verification**

```bash
# Check Sentry dashboard for errors
# Check Google Analytics for traffic
# Verify error tracking is working
```

**Checklist:**

- [ ] Sentry receiving events (if configured)
- [ ] Google Analytics tracking (if configured)
- [ ] Error alerts configured
- [ ] Monitoring dashboards accessible

**3.4 Performance Verification**

```bash
# Check page load times
# Monitor API response times
# Check database query performance
```

**Checklist:**

- [ ] Page load times acceptable
- [ ] API response times within SLA
- [ ] Database queries performant
- [ ] No obvious bottlenecks

### Phase 4: Launch Report

Generate comprehensive launch documentation:

```markdown
# Launch Report - [Product Name] - [Date]

## Pre-Launch Checks
- ✅ All checks passed
- [Details of any issues found and resolved]

## Deployment
- Deployed to: [environment]
- Deployment time: [timestamp]
- Deployment ID/hash: [if applicable]

## Post-Launch Verification
- ✅ Health checks passed
- ✅ Smoke tests passed
- ✅ Monitoring active

## Monitoring Setup
- Sentry: [configured/not configured]
- Google Analytics: [configured/not configured]

## Known Issues
- [List any known issues or limitations]

## Next Steps
- [Post-launch tasks]
- [Monitoring to watch]
- [Optimizations planned]
```

Save to: `.agents/SESSIONS/[today].md` or `.agents/LAUNCHES/[product-name]-[date].md`

---

## Manual Checklist for AI Agent

When user runs `/launch`:

### Pre-Launch Phase

- [ ] Check critical rules: `.agents/SYSTEM/critical/CRITICAL-NEVER-DO.md`
- [ ] Run code quality checks (lint, type-check, build)
- [ ] Run security audit
- [ ] Check performance metrics
- [ ] Verify monitoring setup (Sentry, Google Analytics)
- [ ] Validate environment variables
- [ ] Check documentation completeness
- [ ] Report any blockers found

### Deployment Phase

- [ ] Confirm user wants to proceed to deployment
- [ ] Run database migrations (if needed)
- [ ] Deploy to staging first (if staging exists)
- [ ] Run smoke tests on staging
- [ ] Get user confirmation for production deployment
- [ ] Deploy to production
- [ ] Monitor deployment logs

### Post-Launch Phase

- [ ] Run health checks
- [ ] Execute smoke tests
- [ ] Verify monitoring (Sentry, Google Analytics)
- [ ] Check performance metrics
- [ ] Generate launch report
- [ ] Document in session file

---

## Examples

### Example 1: Full Launch Workflow

**User:** `/launch`

**AI Actions:**

1. Run all pre-launch checks
2. Report results: "Pre-launch checks passed ✅"
3. Ask: "Ready to deploy? (y/n)"
4. On confirmation, execute deployment
5. Run post-launch verification
6. Generate launch report
7. Save to `.agents/SESSIONS/[today].md`

### Example 2: Pre-Launch Check Only

**User:** `/launch --check`

**AI Actions:**

1. Run all pre-launch checks
2. Report results with detailed checklist
3. Stop before deployment
4. User can fix any issues before proceeding

### Example 3: Post-Launch Verification

**User:** `/launch --verify`

**AI Actions:**

1. Skip pre-launch and deployment
2. Run post-launch verification only
3. Check health, monitoring, performance
4. Generate verification report

---

## Safety Features

**Before deployment:**

- ✅ Requires explicit user confirmation for production
- ✅ Runs all pre-launch checks first
- ✅ Validates environment setup

**During deployment:**

- ✅ Monitors deployment logs
- ✅ Ready to rollback if issues detected

**After deployment:**

- ✅ Comprehensive verification
- ✅ Monitoring validation
- ✅ Issue tracking

---

## Error Handling

**If pre-launch checks fail:**

- Stop launch process
- Report specific failures
- Provide remediation steps
- User fixes issues and re-runs

**If deployment fails:**

- Attempt rollback (if supported)
- Report deployment failure
- Generate failure report
- Suggest next steps

**If post-launch verification fails:**

- Report specific failures
- Provide debugging steps
- Check monitoring for errors
- Suggest remediation

---

## Integration with Other Commands

This command integrates with:

- **`/deploy`** - Delegates actual deployment execution
- **`/monitoring-setup`** - Verifies monitoring is configured
- **`/performance`** - Can trigger performance analysis if needed
- **`/security-audit`** - Can trigger security audit if needed

---

**Created:** 2025-01-27
**Purpose:** Orchestrate complete startup launch workflow from planning through post-launch verification
