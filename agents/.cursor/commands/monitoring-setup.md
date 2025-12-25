# Monitoring Setup - Sentry & Google Analytics

**Purpose:** Set up error tracking (Sentry) and analytics (Google Analytics) for NestJS and Next.js applications

## Usage

```bash
/monitoring-setup              # Set up both Sentry and Google Analytics
/monitoring-setup --sentry     # Set up Sentry only
/monitoring-setup --analytics  # Set up Google Analytics only
```

## When to Use

Use this command when:

- Setting up a new project
- Need error tracking and analytics
- Preparing for production launch
- Want to monitor application health

## What This Command Does

Sets up comprehensive monitoring:

1. **Sentry Integration** - Error tracking for NestJS and Next.js
2. **Google Analytics** - Analytics tracking (GA4) for Next.js
3. **Configuration** - Environment variables, initialization
4. **Event Tracking** - Set up common event tracking patterns

---

## Workflow

### Phase 1: Sentry Setup

**1.1 Install Dependencies**

**NestJS Backend:**

```bash
cd api
npm install @sentry/node @sentry/profiling-node
# or
pnpm add @sentry/node @sentry/profiling-node
```

**Next.js Frontend:**

```bash
cd frontend
npm install @sentry/nextjs
# or
pnpm add @sentry/nextjs
```

**1.2 Initialize Sentry (NestJS)**

**Create Sentry configuration:**

```typescript
// src/config/sentry.config.ts
import * as Sentry from '@sentry/node';
import { ProfilingIntegration } from '@sentry/profiling-node';

export function initSentry() {
  if (!process.env.SENTRY_DSN) {
    console.warn('Sentry DSN not configured, skipping Sentry initialization');
    return;
  }

  Sentry.init({
    dsn: process.env.SENTRY_DSN,
    environment: process.env.NODE_ENV || 'development',
    integrations: [
      new ProfilingIntegration(),
    ],
    tracesSampleRate: process.env.NODE_ENV === 'production' ? 0.1 : 1.0,
    profilesSampleRate: process.env.NODE_ENV === 'production' ? 0.1 : 1.0,
  });
}
```

**Initialize in main.ts:**

```typescript
// src/main.ts
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { initSentry } from './config/sentry.config';

async function bootstrap() {
  // Initialize Sentry before creating app
  initSentry();

  const app = await NestFactory.create(AppModule);
  
  // ... rest of bootstrap
}

bootstrap();
```

**1.3 Initialize Sentry (Next.js)**

**Run Sentry wizard:**

```bash
cd frontend
npx @sentry/wizard@latest -i nextjs
```

This will:
- Create `sentry.client.config.ts`
- Create `sentry.server.config.ts`
- Create `sentry.edge.config.ts`
- Update `next.config.js`
- Create `sentry.properties`

**Manual setup (if wizard doesn't work):**

**Create `sentry.client.config.ts`:**

```typescript
// sentry.client.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV || 'development',
  tracesSampleRate: 1.0,
  debug: process.env.NODE_ENV === 'development',
});
```

**Create `sentry.server.config.ts`:**

```typescript
// sentry.server.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV || 'development',
  tracesSampleRate: 1.0,
});
```

**Update `next.config.js`:**

```javascript
// next.config.js
const { withSentryConfig } = require('@sentry/nextjs');

const nextConfig = {
  // ... existing config
};

module.exports = withSentryConfig(
  nextConfig,
  {
    silent: true,
    org: process.env.SENTRY_ORG,
    project: process.env.SENTRY_PROJECT,
  },
  {
    widenClientFileUpload: true,
    transpileClientSDK: true,
    hideSourceMaps: true,
    disableLogger: true,
  }
);
```

**1.4 Environment Variables**

Add to `.env` (backend) and `.env.local` (frontend):

```env
# Sentry Configuration
SENTRY_DSN=https://[your-sentry-dsn]@[org].ingest.sentry.io/[project-id]
SENTRY_ORG=your-org
SENTRY_PROJECT=your-project

# Frontend only
NEXT_PUBLIC_SENTRY_DSN=https://[your-sentry-dsn]@[org].ingest.sentry.io/[project-id]
```

**1.5 Error Boundary (Next.js)**

**Create error boundary component:**

```typescript
// components/ErrorBoundary.tsx
'use client';

import * as Sentry from '@sentry/nextjs';
import { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: any) {
    Sentry.captureException(error, { contexts: { react: errorInfo } });
  }

  render() {
    if (this.state.hasError) {
      return <div>Something went wrong. Please refresh the page.</div>;
    }

    return this.props.children;
  }
}
```

**Wrap app with error boundary:**

```typescript
// app/layout.tsx or pages/_app.tsx
import { ErrorBoundary } from '@/components/ErrorBoundary';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <ErrorBoundary>
          {children}
        </ErrorBoundary>
      </body>
    </html>
  );
}
```

### Phase 2: Google Analytics Setup

**2.1 Install Google Analytics (GA4)**

**For Next.js App Router:**

```typescript
// app/layout.tsx
import Script from 'next/script';

export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        <Script
          src={`https://www.googletagmanager.com/gtag/js?id=${process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID}`}
          strategy="afterInteractive"
        />
        <Script id="google-analytics" strategy="afterInteractive">
          {`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', '${process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID}');
          `}
        </Script>
      </head>
      <body>{children}</body>
    </html>
  );
}
```

**For Next.js Pages Router:**

```typescript
// pages/_app.tsx
import { useEffect } from 'react';
import { useRouter } from 'next/router';
import Script from 'next/script';

export default function App({ Component, pageProps }) {
  const router = useRouter();

  useEffect(() => {
    const handleRouteChange = (url: string) => {
      if (typeof window !== 'undefined' && window.gtag) {
        window.gtag('config', process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID, {
          page_path: url,
        });
      }
    };

    router.events.on('routeChangeComplete', handleRouteChange);
    return () => {
      router.events.off('routeChangeComplete', handleRouteChange);
    };
  }, [router.events]);

  return (
    <>
      <Script
        src={`https://www.googletagmanager.com/gtag/js?id=${process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID}`}
        strategy="afterInteractive"
      />
      <Script id="google-analytics" strategy="afterInteractive">
        {`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', '${process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID}');
        `}
      </Script>
      <Component {...pageProps} />
    </>
  );
}
```

**2.2 Create Analytics Utility**

```typescript
// lib/analytics.ts
export const gtag = (...args: any[]) => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag(...args);
  }
};

// Page view tracking
export const trackPageView = (url: string) => {
  gtag('config', process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID!, {
    page_path: url,
  });
};

// Event tracking
export const trackEvent = (
  action: string,
  category: string,
  label?: string,
  value?: number
) => {
  gtag('event', action, {
    event_category: category,
    event_label: label,
    value: value,
  });
};

// Common events
export const analytics = {
  signup: () => trackEvent('signup', 'user'),
  login: () => trackEvent('login', 'user'),
  purchase: (value: number) => trackEvent('purchase', 'ecommerce', undefined, value),
  // Add more common events as needed
};
```

**2.3 Environment Variables**

Add to `.env.local` (frontend):

```env
NEXT_PUBLIC_GA_MEASUREMENT_ID=G-XXXXXXXXXX
```

**2.4 Track Custom Events**

Example usage:

```typescript
// In your components
import { analytics } from '@/lib/analytics';

// Track signup
const handleSignup = async () => {
  await signup();
  analytics.signup();
};

// Track purchase
const handlePurchase = async (amount: number) => {
  await purchase();
  analytics.purchase(amount);
};

// Custom event
import { trackEvent } from '@/lib/analytics';

trackEvent('button_click', 'engagement', 'header_cta');
```

### Phase 3: Verification

**3.1 Test Sentry**

**Test error reporting (NestJS):**

```typescript
// Test endpoint
@Get('/test-sentry')
testSentry() {
  throw new Error('Test Sentry error');
}
```

**Test error reporting (Next.js):**

```typescript
// Test page or component
const testSentry = () => {
  throw new Error('Test Sentry error');
};
```

**3.2 Test Google Analytics**

- Visit your site
- Check Google Analytics Real-Time reports
- Verify page views are tracked
- Test custom events

**3.3 Verify Configuration**

```bash
# Check environment variables
grep SENTRY .env* || true
grep GA_MEASUREMENT .env* || true

# Check Sentry DSN format
echo $SENTRY_DSN | grep -E "^https://.*@.*\.ingest\.sentry\.io/.*$"

# Check GA Measurement ID format
echo $NEXT_PUBLIC_GA_MEASUREMENT_ID | grep -E "^G-[A-Z0-9]+$"
```

---

## Manual Checklist for AI Agent

When user runs `/monitoring-setup`:

### Sentry Setup

- [ ] Install Sentry packages (backend and/or frontend)
- [ ] Create Sentry configuration files
- [ ] Initialize Sentry in main.ts (NestJS) or via wizard (Next.js)
- [ ] Add environment variables
- [ ] Create error boundary (Next.js)
- [ ] Test error reporting
- [ ] Verify errors appear in Sentry dashboard

### Google Analytics Setup

- [ ] Add Google Analytics script to layout
- [ ] Create analytics utility functions
- [ ] Add environment variables
- [ ] Set up page view tracking
- [ ] Set up common event tracking
- [ ] Test analytics tracking
- [ ] Verify events appear in GA dashboard

### Documentation

- [ ] Document setup in session file
- [ ] Note environment variables needed
- [ ] Document common tracking patterns

---

## Examples

### Example 1: Full Setup (Sentry + GA)

**User:** `/monitoring-setup`

**AI Actions:**
1. Detect project structure (NestJS, Next.js, or both)
2. Install Sentry packages
3. Set up Sentry configuration
4. Install Google Analytics
5. Set up GA tracking
6. Add environment variables
7. Test both services
8. Document setup

### Example 2: Sentry Only

**User:** `/monitoring-setup --sentry`

**AI Actions:**
1. Install Sentry packages
2. Set up Sentry configuration
3. Add environment variables
4. Test Sentry
5. Skip Google Analytics setup

### Example 3: Analytics Only

**User:** `/monitoring-setup --analytics`

**AI Actions:**
1. Set up Google Analytics
2. Add environment variables
3. Test GA tracking
4. Skip Sentry setup

---

## Environment Variables Summary

**Required for Sentry:**
- `SENTRY_DSN` - Backend and server-side frontend
- `NEXT_PUBLIC_SENTRY_DSN` - Client-side frontend
- `SENTRY_ORG` - Organization slug (optional)
- `SENTRY_PROJECT` - Project slug (optional)

**Required for Google Analytics:**
- `NEXT_PUBLIC_GA_MEASUREMENT_ID` - GA4 Measurement ID (format: G-XXXXXXXXXX)

---

## Best Practices

**Sentry:**
- Use different DSNs for development and production
- Set appropriate sample rates for production (lower = less volume)
- Configure source maps for better error tracking
- Set up alerts for critical errors

**Google Analytics:**
- Respect user privacy (GDPR, CCPA compliance)
- Use event tracking for key user actions
- Don't track sensitive user data
- Set up conversion goals

---

**Created:** 2025-01-27
**Purpose:** Set up Sentry and Google Analytics for comprehensive application monitoring

