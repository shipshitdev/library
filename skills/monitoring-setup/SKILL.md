---
name: monitoring-setup
description: Sets up Sentry error tracking and Google Analytics for NestJS and Next.js applications. Activates when users need to configure error tracking, set up production monitoring, add Google Analytics, or track application errors and user behavior.
metadata:
  version: "1.0.0"
  tags: "monitoring, sentry, analytics"
---

# Monitoring Setup

## When to Use

- Need to set up error tracking (Sentry)
- Want to configure Google Analytics
- Need monitoring for production applications
- Want to track application errors and user behavior

## Sentry Setup

### NestJS Backend

1. Install: `bun add @sentry/node @sentry/profiling-node`
2. Initialize in `main.ts` before app creation
3. Configure DSN via `SENTRY_DSN` environment variable
4. Set appropriate sample rates for production

### Next.js Frontend

1. Install: `bun add @sentry/nextjs`
2. Run: `bunx @sentry/wizard@latest -i nextjs`
3. Configure client/server/edge configs
4. Set `NEXT_PUBLIC_SENTRY_DSN` for client-side

## Google Analytics Setup

### Next.js Setup

1. Add Google Analytics script to root layout
2. Use `NEXT_PUBLIC_GA_MEASUREMENT_ID` (format: G-XXXXXXXXXX)
3. Create analytics utility functions for event tracking
4. Set up page view tracking

### Common Events

- User signup/login
- Purchases/conversions
- Feature usage
- Custom business events

## Best Practices

- Use different DSNs for dev/prod
- Set appropriate sample rates
- Respect user privacy (GDPR/CCPA)
- Don't track sensitive data
- Set up alerts for critical errors

## Integration

This skill integrates with `/monitoring-setup` command for automated setup workflows.
