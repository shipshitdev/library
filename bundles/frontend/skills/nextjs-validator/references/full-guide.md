# Next.js Validator — Full Examples

## Validation Output Example

```
=== Next.js 16 Validation Report ===

Package Version: next@16.1.0 ✓

File Structure:
  ✓ Using app/ directory (App Router)
  ✗ Found pages/ directory - migrate to App Router
  ✓ Found proxy.ts
  ✗ Found middleware.ts - migrate to proxy.ts

Patterns:
  ✓ Using Server Components
  ✗ Found getServerSideProps in 2 files
  ✓ Using next/navigation

Config:
  ✓ next.config.ts (TypeScript)
  ✓ Turbopack enabled (default)

Summary: 2 issues found
  - Migrate pages/ to app/ directory
  - Replace middleware.ts with proxy.ts
```

## Migration Guide

### From middleware.ts to proxy.ts

**Before (v15):**

```typescript
// middleware.ts
import { NextResponse } from 'next/server';

export function middleware(request) {
  // Edge runtime
  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*'],
};
```

**After (v16):**

```typescript
// proxy.ts
import { createProxy } from 'next/proxy';

export const proxy = createProxy({
  // Node.js runtime
  async handle(request) {
    // Full Node.js APIs available
    return request;
  },
  matcher: ['/dashboard/:path*'],
});
```

### From getServerSideProps to Server Components

**Before:**

```typescript
// pages/dashboard.tsx
export async function getServerSideProps() {
  const data = await fetchData();
  return { props: { data } };
}

export default function Dashboard({ data }) {
  return <View data={data} />;
}
```

**After:**

```typescript
// app/dashboard/page.tsx
export default async function Dashboard() {
  const data = await fetchData();
  return <View data={data} />;
}
```

## Intercepting Routes Example

```
app/
├── feed/
│   └── page.tsx
├── photo/
│   └── [id]/
│       └── page.tsx
└── @modal/
    └── (.)photo/
        └── [id]/
            └── page.tsx
```
