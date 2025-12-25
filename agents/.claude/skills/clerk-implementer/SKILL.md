---
name: clerk-implementer
description: This skill should be used when users need to implement Clerk authentication, user management, or organization features in Next.js or NestJS applications. It activates when users ask about Clerk integration, authentication setup, user management, organizations, or Clerk API implementation.
---

# Clerk Implementer

## Overview

This skill enables Claude to implement comprehensive Clerk authentication integrations including user authentication, user management, organization/team features, and route protection for Next.js and NestJS applications. Claude will use this skill to set up Clerk, implement authentication flows, manage users and organizations, and secure routes with middleware and guards.

## When to Use This Skill

This skill activates automatically when users:

- Need to integrate Clerk authentication into their application
- Want to implement user sign up and sign in
- Need to set up password reset functionality
- Want to manage user profiles and sessions
- Need to implement organization/team features
- Want to protect routes with authentication
- Need to access user context in API routes or services

## Project Context Discovery

**Before implementing Clerk integration, discover the project's context:**

1. **Scan Project Documentation:**
   - Check `.agent/SYSTEM/ARCHITECTURE.md` for authentication architecture
   - Review existing authentication patterns
   - Look for environment variable usage
   - Check for existing Clerk integration

2. **Identify Framework:**
   - Determine if using Next.js (App Router or Pages Router)
   - Check if using NestJS backend
   - Review existing middleware patterns
   - Check for API route protection needs

3. **Use Project-Specific Skills:**
   - Check for `[project]-clerk-implementer` skill
   - Review project-specific authentication patterns
   - Follow project's security standards

## Setup and Configuration

### 1. Install Clerk SDK

**Next.js:**
```bash
npm install @clerk/nextjs
# or
yarn add @clerk/nextjs
```

**NestJS:**
```bash
npm install @clerk/clerk-sdk-node
# or
yarn add @clerk/clerk-sdk-node
```

### 2. Environment Variables

Create `.env.local` (Next.js) or `.env` (NestJS):

```env
# Clerk API Keys
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...
CLERK_WEBHOOK_SECRET=whsec_...

# Clerk URLs (optional, defaults to Clerk hosted)
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/
```

### 3. Clerk Dashboard Setup

1. Create account at [clerk.com](https://clerk.com)
2. Create a new application
3. Configure authentication methods (Email, OAuth, etc.)
4. Copy publishable key and secret key
5. Set up webhook endpoints (if needed)

## Next.js Implementation

### 1. App Router Setup

**Root Layout:**

```typescript
// app/layout.tsx
import { ClerkProvider } from '@clerk/nextjs';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>{children}</body>
      </html>
    </ClerkProvider>
  );
}
```

**Middleware (Route Protection):**

```typescript
// middleware.ts
import { authMiddleware } from '@clerk/nextjs';

export default authMiddleware({
  // Public routes that don't require authentication
  publicRoutes: ['/'],
  
  // Routes that are always protected
  protectedRoutes: ['/dashboard', '/profile'],
  
  // Routes to redirect to after sign in/up
  afterAuth(auth, req) {
    if (auth.userId && req.nextUrl.pathname === '/') {
      return Response.redirect(new URL('/dashboard', req.url));
    }
  },
});

export const config = {
  matcher: ['/((?!.+\\.[\\w]+$|_next).*)', '/', '/(api|trpc)(.*)'],
};
```

**Protected Route Example:**

```typescript
// app/dashboard/page.tsx
import { auth, currentUser } from '@clerk/nextjs';
import { redirect } from 'next/navigation';

export default async function DashboardPage() {
  const { userId } = auth();
  
  if (!userId) {
    redirect('/sign-in');
  }

  const user = await currentUser();

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome, {user?.firstName} {user?.lastName}</p>
      <p>Email: {user?.emailAddresses[0]?.emailAddress}</p>
    </div>
  );
}
```

### 2. Client Components (User Interface)

**Sign In Component:**

```typescript
// components/sign-in.tsx
'use client';

import { SignIn } from '@clerk/nextjs';

export default function SignInPage() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <SignIn />
    </div>
  );
}
```

**Sign Up Component:**

```typescript
// components/sign-up.tsx
'use client';

import { SignUp } from '@clerk/nextjs';

export default function SignUpPage() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <SignUp />
    </div>
  );
}
```

**User Button (Profile Menu):**

```typescript
// components/user-button.tsx
'use client';

import { UserButton } from '@clerk/nextjs';

export default function UserButtonComponent() {
  return <UserButton afterSignOutUrl="/" />;
}
```

**Use Auth Hook:**

```typescript
// components/protected-content.tsx
'use client';

import { useAuth, useUser } from '@clerk/nextjs';

export default function ProtectedContent() {
  const { isSignedIn, userId } = useAuth();
  const { user } = useUser();

  if (!isSignedIn) {
    return <div>Please sign in</div>;
  }

  return (
    <div>
      <p>User ID: {userId}</p>
      <p>Email: {user?.emailAddresses[0]?.emailAddress}</p>
    </div>
  );
}
```

### 3. API Routes (Server-side)

**Protected API Route:**

```typescript
// app/api/protected/route.ts
import { auth, currentUser } from '@clerk/nextjs';
import { NextResponse } from 'next/server';

export async function GET() {
  const { userId } = auth();
  
  if (!userId) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    );
  }

  const user = await currentUser();

  return NextResponse.json({
    message: 'Protected data',
    userId,
    userEmail: user?.emailAddresses[0]?.emailAddress,
  });
}
```

**API Route with User Data:**

```typescript
// app/api/user/route.ts
import { currentUser } from '@clerk/nextjs';
import { NextResponse } from 'next/server';

export async function GET() {
  const user = await currentUser();

  if (!user) {
    return NextResponse.json(
      { error: 'Not authenticated' },
      { status: 401 }
    );
  }

  return NextResponse.json({
    id: user.id,
    firstName: user.firstName,
    lastName: user.lastName,
    email: user.emailAddresses[0]?.emailAddress,
    imageUrl: user.imageUrl,
  });
}
```

### 4. Pages Router Setup (Legacy)

**App Component:**

```typescript
// pages/_app.tsx
import { ClerkProvider } from '@clerk/nextjs';
import type { AppProps } from 'next/app';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <ClerkProvider>
      <Component {...pageProps} />
    </ClerkProvider>
  );
}

export default MyApp;
```

**Server-side Page:**

```typescript
// pages/dashboard.tsx
import { getAuth } from '@clerk/nextjs/server';
import { GetServerSideProps } from 'next';

export default function Dashboard({ userId }: { userId: string }) {
  return <div>Dashboard for user: {userId}</div>;
}

export const getServerSideProps: GetServerSideProps = async (context) => {
  const { userId } = getAuth(context.req);

  if (!userId) {
    return {
      redirect: {
        destination: '/sign-in',
        permanent: false,
      },
    };
  }

  return {
    props: { userId },
  };
};
```

## NestJS Implementation

### 1. Module Setup

```typescript
// src/clerk/clerk.module.ts
import { Module, Global } from '@nestjs/common';
import { ClerkService } from './clerk.service';

@Global()
@Module({
  providers: [ClerkService],
  exports: [ClerkService],
})
export class ClerkModule {}
```

### 2. Clerk Service

```typescript
// src/clerk/clerk.service.ts
import { Injectable } from '@nestjs/common';
import { clerkClient } from '@clerk/clerk-sdk-node';

@Injectable()
export class ClerkService {
  private clerk = clerkClient;

  getClerk() {
    return this.clerk;
  }

  async getUser(userId: string) {
    return await this.clerk.users.getUser(userId);
  }

  async updateUser(userId: string, data: any) {
    return await this.clerk.users.updateUser(userId, data);
  }

  async deleteUser(userId: string) {
    return await this.clerk.users.deleteUser(userId);
  }
}
```

### 3. Authentication Guard

```typescript
// src/clerk/clerk.guard.ts
import {
  Injectable,
  CanActivate,
  ExecutionContext,
  UnauthorizedException,
} from '@nestjs/common';
import { clerkClient } from '@clerk/clerk-sdk-node';

@Injectable()
export class ClerkGuard implements CanActivate {
  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context.switchToHttp().getRequest();
    const token = this.extractTokenFromHeader(request);

    if (!token) {
      throw new UnauthorizedException('No token provided');
    }

    try {
      const { userId } = await clerkClient.verifyToken(token);
      request.userId = userId;
      
      // Optionally fetch full user object
      const user = await clerkClient.users.getUser(userId);
      request.user = user;
      
      return true;
    } catch (error) {
      throw new UnauthorizedException('Invalid token');
    }
  }

  private extractTokenFromHeader(request: any): string | undefined {
    const [type, token] = request.headers.authorization?.split(' ') ?? [];
    return type === 'Bearer' ? token : undefined;
  }
}
```

### 4. Custom Decorator for User

```typescript
// src/clerk/current-user.decorator.ts
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

export const CurrentUser = createParamDecorator(
  (data: unknown, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    return request.user;
  },
);

export const CurrentUserId = createParamDecorator(
  (data: unknown, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    return request.userId;
  },
);
```

### 5. Controller with Authentication

```typescript
// src/users/users.controller.ts
import { Controller, Get, UseGuards } from '@nestjs/common';
import { ClerkGuard } from '../clerk/clerk.guard';
import { CurrentUser, CurrentUserId } from '../clerk/current-user.decorator';
import { ClerkService } from '../clerk/clerk.service';

@Controller('users')
@UseGuards(ClerkGuard)
export class UsersController {
  constructor(private clerkService: ClerkService) {}

  @Get('me')
  async getCurrentUser(@CurrentUserId() userId: string) {
    return await this.clerkService.getUser(userId);
  }

  @Get('profile')
  async getProfile(@CurrentUser() user: any) {
    return {
      id: user.id,
      firstName: user.firstName,
      lastName: user.lastName,
      email: user.emailAddresses[0]?.emailAddress,
    };
  }
}
```

### 6. Webhook Handler

```typescript
// src/clerk/clerk.webhook.controller.ts
import { Controller, Post, Body, Headers, HttpCode, HttpStatus } from '@nestjs/common';
import { Webhook } from 'svix';
import { clerkClient } from '@clerk/clerk-sdk-node';

@Controller('webhooks/clerk')
export class ClerkWebhookController {
  @Post()
  @HttpCode(HttpStatus.OK)
  async handleWebhook(
    @Body() body: any,
    @Headers('svix-id') svixId: string,
    @Headers('svix-timestamp') svixTimestamp: string,
    @Headers('svix-signature') svixSignature: string,
  ) {
    const webhookSecret = process.env.CLERK_WEBHOOK_SECRET!;

    const wh = new Webhook(webhookSecret);

    let evt: any;

    try {
      evt = wh.verify(JSON.stringify(body), {
        'svix-id': svixId,
        'svix-timestamp': svixTimestamp,
        'svix-signature': svixSignature,
      });
    } catch (err) {
      throw new Error('Webhook verification failed');
    }

    const { id, ...attributes } = evt.data;
    const eventType = evt.type;

    switch (eventType) {
      case 'user.created':
        // Handle user creation
        console.log('User created:', id);
        break;

      case 'user.updated':
        // Handle user update
        console.log('User updated:', id);
        break;

      case 'user.deleted':
        // Handle user deletion
        console.log('User deleted:', id);
        break;

      default:
        console.log(`Unhandled event type: ${eventType}`);
    }

    return { received: true };
  }
}
```

## Organization/Team Features

### 1. Create Organization (Next.js)

```typescript
// app/api/organizations/route.ts
import { auth, currentUser } from '@clerk/nextjs';
import { NextResponse } from 'next/server';
import { clerkClient } from '@clerk/clerk-sdk-node';

export async function POST(request: Request) {
  const { userId } = auth();
  
  if (!userId) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    );
  }

  const { name } = await request.json();

  const organization = await clerkClient.organizations.createOrganization({
    name,
    createdBy: userId,
  });

  return NextResponse.json({ organizationId: organization.id });
}
```

### 2. Organization Membership (Next.js)

```typescript
// components/organization-switcher.tsx
'use client';

import { OrganizationSwitcher } from '@clerk/nextjs';

export default function OrganizationSwitcherComponent() {
  return (
    <OrganizationSwitcher
      afterCreateOrganizationUrl="/dashboard"
      afterSelectOrganizationUrl="/dashboard"
    />
  );
}
```

### 3. Organization Guard (NestJS)

```typescript
// src/clerk/organization.guard.ts
import {
  Injectable,
  CanActivate,
  ExecutionContext,
  ForbiddenException,
} from '@nestjs/common';
import { clerkClient } from '@clerk/clerk-sdk-node';

@Injectable()
export class OrganizationGuard implements CanActivate {
  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context.switchToHttp().getRequest();
    const userId = request.userId;
    const organizationId = request.params.organizationId || request.body.organizationId;

    if (!organizationId) {
      throw new ForbiddenException('Organization ID required');
    }

    const memberships = await clerkClient.users.getOrganizationMembershipList({
      userId,
    });

    const hasAccess = memberships.some(
      (m) => m.organization.id === organizationId
    );

    if (!hasAccess) {
      throw new ForbiddenException('Not a member of this organization');
    }

    request.organizationId = organizationId;
    return true;
  }
}
```

## Best Practices

### Security
- Always verify tokens on the server side
- Use HTTPS for all authentication flows
- Store secrets in environment variables
- Implement proper error handling
- Validate user permissions before actions

### Session Management
- Use Clerk's built-in session management
- Implement proper logout flows
- Handle token refresh automatically
- Use middleware for route protection

### User Management
- Sync user data with your database when needed
- Handle webhooks for user lifecycle events
- Implement proper user data validation
- Respect user privacy and data protection

### Organization Management
- Implement proper organization access controls
- Use organization guards for multi-tenant features
- Handle organization membership changes via webhooks
- Implement proper organization data isolation

### Error Handling
- Provide clear error messages
- Handle authentication failures gracefully
- Implement proper logging for security events
- Handle edge cases (expired tokens, revoked access)

## Common Clerk Events

- `user.created` - New user signed up
- `user.updated` - User profile updated
- `user.deleted` - User account deleted
- `session.created` - New session started
- `session.ended` - Session ended
- `organization.created` - New organization created
- `organizationMembership.created` - User joined organization
- `organizationMembership.deleted` - User left organization

## Example User Requests

**Example 1: "Add Clerk authentication to my Next.js app"**
- Install Clerk SDK
- Set up ClerkProvider in root layout
- Create sign-in and sign-up pages
- Configure middleware for route protection
- Add UserButton component

**Example 2: "Protect API routes with Clerk in NestJS"**
- Set up Clerk module and service
- Create authentication guard
- Add CurrentUser decorator
- Protect controller endpoints
- Handle authentication errors

**Example 3: "Implement organization/team features"**
- Set up organization creation
- Add organization switcher component
- Implement organization guards
- Handle organization webhooks
- Enforce organization-based data access

