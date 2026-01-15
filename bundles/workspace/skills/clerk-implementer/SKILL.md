---
name: clerk-implementer
description: This skill should be used when users need to implement Clerk authentication, user management, or organization features in Next.js or NestJS applications. It activates when users ask about Clerk integration, authentication setup, user management, organizations, or Clerk API implementation.
---

# Clerk Implementer

## Overview

Implement Clerk authentication integrations including user authentication, user management, organization/team features, and route protection for Next.js and NestJS applications.

## When to Use

- Integrate Clerk authentication into applications
- Implement user sign up/sign in
- Set up password reset functionality
- Manage user profiles and sessions
- Implement organization/team features
- Protect routes with authentication
- Access user context in API routes or services

## Project Context Discovery

Before implementing:
1. Check `.agent/SYSTEM/ARCHITECTURE.md` for existing auth patterns
2. Identify framework (Next.js App Router vs NestJS)
3. Look for project-specific `[project]-clerk-implementer` skill

## Critical Rules for Next.js App Router

### ALWAYS DO:
- Use `clerkMiddleware()` from `@clerk/nextjs/server` in `proxy.ts`
- Create `proxy.ts` in `src/` directory (or root if no src)
- Wrap app with `<ClerkProvider>` in `app/layout.tsx`
- Import `auth()` from `@clerk/nextjs/server` with `async/await`
- Store keys only in `.env.local`, use placeholders in code

### NEVER DO:
- Use `authMiddleware()` (deprecated)
- Reference `_app.tsx` or Pages Router patterns
- Print/write actual API keys to files or logs

## Quick Setup

### Next.js
```bash
bun add @clerk/nextjs@latest
```

### NestJS
```bash
bun add @clerk/clerk-sdk-node
```

### Environment Variables
```env
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=YOUR_PUBLISHABLE_KEY
CLERK_SECRET_KEY=YOUR_SECRET_KEY
```

## Key Patterns

### Next.js App Router - Middleware
```typescript
// proxy.ts
import { clerkMiddleware } from "@clerk/nextjs/server";
export default clerkMiddleware();
```

### Next.js - Protected Route
```typescript
import { auth } from "@clerk/nextjs/server";
const { userId } = await auth();
if (!userId) redirect('/sign-in');
```

### NestJS - Auth Guard
```typescript
@Injectable()
export class ClerkGuard implements CanActivate {
  async canActivate(context: ExecutionContext) {
    const token = this.extractTokenFromHeader(request);
    const { userId } = await clerkClient.verifyToken(token);
    request.userId = userId;
    return true;
  }
}
```

### Components
- `<ClerkProvider>` - Wrap app
- `<SignInButton>`, `<SignUpButton>` - Auth buttons
- `<UserButton>` - Profile menu
- `<SignedIn>`, `<SignedOut>` - Conditional rendering
- `<OrganizationSwitcher>` - Multi-tenant switching

## Webhook Events
- `user.created` / `user.updated` / `user.deleted`
- `session.created` / `session.ended`
- `organization.created`
- `organizationMembership.created` / `organizationMembership.deleted`

---

**For complete implementation examples, NestJS service setup, organization guards, and webhook handlers, see:** `references/full-guide.md`
