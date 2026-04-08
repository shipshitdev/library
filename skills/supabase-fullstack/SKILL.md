---
name: supabase-fullstack
description: Comprehensive Supabase skill for building full-stack applications. This skill should be used when users want to set up Supabase, implement authentication, design databases with Row Level Security, manage file storage, create Edge Functions, use Realtime subscriptions, or run migrations. Covers Next.js, React, and general TypeScript/JavaScript integrations.
license: Complete terms in LICENSE.txt
---

# Supabase Full-Stack

Build production-ready applications with Supabase as your backend. This skill covers the complete Supabase stack from project setup to production deployment.

## Quick Setup

### 1. Install Dependencies

```bash
# Core
bun add @supabase/supabase-js

# For Next.js SSR
bun add @supabase/ssr

# CLI (for migrations, types, edge functions)
bun add -D supabase
```

### 2. Environment Variables

```env
NEXT_PUBLIC_SUPABASE_URL=https://<project-ref>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<anon-key>
SUPABASE_SERVICE_ROLE_KEY=<service-role-key>  # Server-side only, NEVER expose
```

### 3. Client Setup

#### Browser Client (Next.js App Router)

```typescript
// lib/supabase/client.ts
import { createBrowserClient } from "@supabase/ssr";

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}
```

#### Server Client (Next.js App Router)

```typescript
// lib/supabase/server.ts
import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";

export async function createClient() {
  const cookieStore = await cookies();

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookiesToSet) {
          try {
            for (const { name, value, options } of cookiesToSet) {
              cookieStore.set(name, value, options);
            }
          } catch {
            // Called from Server Component — ignore
          }
        },
      },
    }
  );
}
```

#### Service Role Client (admin operations)

```typescript
// lib/supabase/admin.ts
import { createClient } from "@supabase/supabase-js";

export const supabaseAdmin = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!,
  { auth: { autoRefreshToken: false, persistSession: false } }
);
```

### 4. Middleware (Auth + SSR)

```typescript
// middleware.ts
import { createServerClient } from "@supabase/ssr";
import { NextResponse, type NextRequest } from "next/server";

export async function middleware(request: NextRequest) {
  let response = NextResponse.next({ request });

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll();
        },
        setAll(cookiesToSet) {
          for (const { name, value } of cookiesToSet) {
            request.cookies.set(name, value);
          }
          response = NextResponse.next({ request });
          for (const { name, value, options } of cookiesToSet) {
            response.cookies.set(name, value, options);
          }
        },
      },
    }
  );

  // Refresh session — IMPORTANT: don't remove this
  const { data: { user } } = await supabase.auth.getUser();

  // Protect routes
  if (!user && request.nextUrl.pathname.startsWith("/dashboard")) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return response;
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|api/webhooks).*)"],
};
```

## Authentication

### Email + Password

```typescript
// Sign up
const { data, error } = await supabase.auth.signUp({
  email: "user@example.com",
  password: "securepassword",
  options: {
    data: { full_name: "Jane Doe" }, // stored in auth.users.raw_user_meta_data
  },
});

// Sign in
const { data, error } = await supabase.auth.signInWithPassword({
  email: "user@example.com",
  password: "securepassword",
});

// Sign out
await supabase.auth.signOut();
```

### OAuth (Google, GitHub, etc.)

```typescript
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: "google",
  options: {
    redirectTo: `${window.location.origin}/auth/callback`,
    queryParams: { access_type: "offline", prompt: "consent" },
  },
});
```

**Auth callback route** (`app/auth/callback/route.ts`):

```typescript
import { createClient } from "@/lib/supabase/server";
import { NextResponse } from "next/server";

export async function GET(request: Request) {
  const { searchParams, origin } = new URL(request.url);
  const code = searchParams.get("code");
  const next = searchParams.get("next") ?? "/dashboard";

  if (code) {
    const supabase = await createClient();
    const { error } = await supabase.auth.exchangeCodeForSession(code);
    if (!error) return NextResponse.redirect(`${origin}${next}`);
  }

  return NextResponse.redirect(`${origin}/auth/error`);
}
```

### Magic Link

```typescript
const { error } = await supabase.auth.signInWithOtp({
  email: "user@example.com",
  options: { emailRedirectTo: `${window.location.origin}/auth/callback` },
});
```

### Auth State Listener

```typescript
useEffect(() => {
  const { data: { subscription } } = supabase.auth.onAuthStateChange(
    (event, session) => {
      if (event === "SIGNED_IN") router.refresh();
      if (event === "SIGNED_OUT") router.push("/login");
    }
  );
  return () => subscription.unsubscribe();
}, []);
```

## Database

### Schema Design Patterns

#### User Profiles (extend auth.users)

```sql
-- Create profiles table linked to auth
create table public.profiles (
  id uuid references auth.users(id) on delete cascade primary key,
  full_name text,
  avatar_url text,
  billing_plan text default 'free' check (billing_plan in ('free', 'pro', 'enterprise')),
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Auto-create profile on signup
create or replace function public.handle_new_user()
returns trigger as $$
begin
  insert into public.profiles (id, full_name, avatar_url)
  values (
    new.id,
    new.raw_user_meta_data ->> 'full_name',
    new.raw_user_meta_data ->> 'avatar_url'
  );
  return new;
end;
$$ language plpgsql security definer;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();
```

#### Multi-tenant (team/org based)

```sql
create table public.teams (
  id uuid default gen_random_uuid() primary key,
  name text not null,
  created_at timestamptz default now()
);

create table public.team_members (
  team_id uuid references public.teams(id) on delete cascade,
  user_id uuid references auth.users(id) on delete cascade,
  role text default 'member' check (role in ('owner', 'admin', 'member')),
  primary key (team_id, user_id)
);

-- Items scoped to teams
create table public.projects (
  id uuid default gen_random_uuid() primary key,
  team_id uuid references public.teams(id) on delete cascade not null,
  name text not null,
  created_at timestamptz default now()
);
```

### Row Level Security (RLS)

**Always enable RLS on every table that contains user data.**

```sql
-- Enable RLS
alter table public.profiles enable row level security;
alter table public.projects enable row level security;

-- Users can read/update their own profile
create policy "Users can view own profile"
  on public.profiles for select
  using (auth.uid() = id);

create policy "Users can update own profile"
  on public.profiles for update
  using (auth.uid() = id);

-- Team members can view team projects
create policy "Team members can view projects"
  on public.projects for select
  using (
    exists (
      select 1 from public.team_members
      where team_members.team_id = projects.team_id
      and team_members.user_id = auth.uid()
    )
  );

-- Only team admins/owners can insert projects
create policy "Team admins can create projects"
  on public.projects for insert
  with check (
    exists (
      select 1 from public.team_members
      where team_members.team_id = projects.team_id
      and team_members.user_id = auth.uid()
      and team_members.role in ('owner', 'admin')
    )
  );
```

### Querying

```typescript
// Basic select
const { data, error } = await supabase
  .from("projects")
  .select("*")
  .eq("team_id", teamId)
  .order("created_at", { ascending: false });

// Select with relations
const { data } = await supabase
  .from("projects")
  .select(`
    *,
    team:teams(name),
    tasks(id, title, status)
  `)
  .eq("id", projectId)
  .single();

// Insert
const { data, error } = await supabase
  .from("projects")
  .insert({ team_id: teamId, name: "New Project" })
  .select()
  .single();

// Upsert
const { data } = await supabase
  .from("profiles")
  .upsert({ id: userId, full_name: "Updated Name" })
  .select()
  .single();

// Delete
const { error } = await supabase
  .from("projects")
  .delete()
  .eq("id", projectId);

// RPC (call database functions)
const { data } = await supabase.rpc("get_team_stats", { team_id: teamId });
```

## Storage

```typescript
// Upload file
const { data, error } = await supabase.storage
  .from("avatars")
  .upload(`${userId}/avatar.png`, file, {
    cacheControl: "3600",
    upsert: true,
    contentType: file.type,
  });

// Get public URL
const { data: { publicUrl } } = supabase.storage
  .from("avatars")
  .getPublicUrl(`${userId}/avatar.png`);

// Get signed URL (private buckets)
const { data: { signedUrl } } = await supabase.storage
  .from("documents")
  .createSignedUrl("path/to/file.pdf", 3600); // 1 hour

// Delete
await supabase.storage.from("avatars").remove([`${userId}/avatar.png`]);
```

### Storage RLS

```sql
-- Storage policies (in SQL editor)
create policy "Users can upload own avatar"
  on storage.objects for insert
  with check (
    bucket_id = 'avatars'
    and (storage.foldername(name))[1] = auth.uid()::text
  );

create policy "Avatar images are publicly accessible"
  on storage.objects for select
  using (bucket_id = 'avatars');
```

## Realtime

```typescript
// Subscribe to changes
const channel = supabase
  .channel("project-tasks")
  .on(
    "postgres_changes",
    {
      event: "*", // INSERT, UPDATE, DELETE, or *
      schema: "public",
      table: "tasks",
      filter: `project_id=eq.${projectId}`,
    },
    (payload) => {
      console.log("Change:", payload.eventType, payload.new);
    }
  )
  .subscribe();

// Broadcast (ephemeral, no DB)
const channel = supabase.channel("room-1");
channel.on("broadcast", { event: "cursor" }, ({ payload }) => {
  updateCursor(payload);
});
channel.subscribe((status) => {
  if (status === "SUBSCRIBED") {
    channel.send({ type: "broadcast", event: "cursor", payload: { x, y } });
  }
});

// Presence (online users)
const channel = supabase.channel("room-1");
channel.on("presence", { event: "sync" }, () => {
  const state = channel.presenceState();
  setOnlineUsers(Object.values(state).flat());
});
channel.subscribe(async (status) => {
  if (status === "SUBSCRIBED") {
    await channel.track({ user_id: userId, name: userName });
  }
});

// Cleanup
supabase.removeChannel(channel);
```

## Edge Functions

```bash
# Create
bunx supabase functions new my-function

# Deploy
bunx supabase functions deploy my-function

# Local dev
bunx supabase functions serve
```

### Edge Function Template

```typescript
// supabase/functions/my-function/index.ts
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const supabase = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
    );

    // Get user from JWT
    const authHeader = req.headers.get("Authorization")!;
    const { data: { user } } = await supabase.auth.getUser(
      authHeader.replace("Bearer ", "")
    );

    if (!user) {
      return new Response(JSON.stringify({ error: "Unauthorized" }), {
        status: 401,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const body = await req.json();

    // Your logic here...

    return new Response(JSON.stringify({ success: true }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
```

### Call from Client

```typescript
const { data, error } = await supabase.functions.invoke("my-function", {
  body: { key: "value" },
});
```

## Migrations

```bash
# Init (first time)
bunx supabase init

# Link to remote project
bunx supabase link --project-ref <project-ref>

# Create migration
bunx supabase migration new create_projects_table

# Apply locally
bunx supabase db reset

# Push to remote
bunx supabase db push

# Pull remote changes
bunx supabase db pull

# Generate TypeScript types
bunx supabase gen types typescript --project-id <project-ref> > types/supabase.ts
```

### Type-Safe Client

```typescript
import { createBrowserClient } from "@supabase/ssr";
import type { Database } from "@/types/supabase";

export function createClient() {
  return createBrowserClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}
```

## Common Patterns

### Pagination

```typescript
const PAGE_SIZE = 20;

const { data, count } = await supabase
  .from("projects")
  .select("*", { count: "exact" })
  .range(page * PAGE_SIZE, (page + 1) * PAGE_SIZE - 1)
  .order("created_at", { ascending: false });
```

### Full-Text Search

```sql
-- Add search column
alter table public.projects add column fts tsvector
  generated always as (to_tsvector('english', coalesce(name, '') || ' ' || coalesce(description, ''))) stored;

create index projects_fts on public.projects using gin(fts);
```

```typescript
const { data } = await supabase
  .from("projects")
  .select("*")
  .textSearch("fts", query, { type: "websearch" });
```

### Webhook Handler (Stripe, etc.)

```typescript
// app/api/webhooks/stripe/route.ts
import { supabaseAdmin } from "@/lib/supabase/admin";
import Stripe from "stripe";

export async function POST(req: Request) {
  const body = await req.text();
  const sig = req.headers.get("stripe-signature")!;
  const event = stripe.webhooks.constructEvent(body, sig, webhookSecret);

  switch (event.type) {
    case "checkout.session.completed": {
      const session = event.data.object;
      await supabaseAdmin
        .from("profiles")
        .update({ billing_plan: "pro" })
        .eq("id", session.metadata.user_id);
      break;
    }
  }

  return new Response("ok");
}
```

## Security Checklist

- [ ] RLS enabled on ALL tables with user data
- [ ] Service role key NEVER exposed to client
- [ ] Auth callback URL configured in Supabase dashboard
- [ ] Storage policies set for all buckets
- [ ] Database functions use `security definer` carefully
- [ ] Realtime enabled only on necessary tables
- [ ] Edge Function secrets stored via `supabase secrets set`
- [ ] Types regenerated after schema changes

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No rows returned" but data exists | Check RLS policies — user may not have access |
| Auth session lost on refresh | Ensure middleware refreshes session (see Middleware section) |
| OAuth redirect fails | Check redirect URL in Supabase dashboard → Auth → URL Configuration |
| Types outdated | Run `bunx supabase gen types typescript` after schema changes |
| Edge Function 500 | Check `bunx supabase functions logs my-function` |
| Realtime not working | Enable replication for the table in Supabase dashboard |
