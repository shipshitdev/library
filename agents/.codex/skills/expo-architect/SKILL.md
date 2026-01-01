---
name: expo-architect
description: Scaffold a production-ready Expo React Native app with working screens, navigation, and optional Clerk auth. Generates complete mobile app structure that runs immediately with `bun start`.
metadata:
  short-description: Scaffold production-ready Expo React Native apps with navigation, auth, and quality tooling
---

# Expo Architect

Create a **production-ready** Expo React Native app with:
- **Framework:** Expo SDK 54 + React Native 0.83 + TypeScript
- **Navigation:** Expo Router (file-based routing)
- **Auth:** Clerk authentication (optional)
- **UI:** NativeWind (Tailwind for RN) or StyleSheet
- **Quality:** Biome linting + TypeScript strict mode
- **Package Manager:** bun

## What Makes This Different

This skill generates **working mobile apps**, not empty scaffolds:
- Complete navigation structure with working screens
- Optional Clerk authentication flow
- Real UI components with proper styling
- API client integration ready
- Runs immediately with `bun start`

---

## Workflow

### Phase 1: PRD Brief Intake

**Ask the user for a brief product description**, then extract and confirm:

```
I'll help you build [App Name]. Based on your description, I understand:

**App Type:** [Tab-based / Stack-based / Drawer]

**Screens:**
- Home - [description]
- [Screen2] - [description]
- [Screen3] - [description]

**Features:**
- [Feature 1]
- [Feature 2]

**Auth Required:** Yes/No

**Backend API:** [URL or "none"]

Is this correct? Any adjustments?
```

### Phase 2: Auth Setup (If Requested)

Generate Clerk authentication for mobile:

**Files:**
- `providers/clerk-provider.tsx` - ClerkProvider wrapper
- `app/(auth)/sign-in.tsx` - Sign in screen
- `app/(auth)/sign-up.tsx` - Sign up screen
- `lib/auth.ts` - Auth utilities

**Environment:**
- `.env` with `EXPO_PUBLIC_CLERK_PUBLISHABLE_KEY`

### Phase 3: Screen Generation

For each extracted screen, generate:

**Tab-based App:**
```
app/
├── _layout.tsx              # Root layout with providers
├── (tabs)/
│   ├── _layout.tsx          # Tab navigator
│   ├── index.tsx            # Home tab
│   ├── [screen].tsx         # Other tabs
│   └── ...
├── (auth)/                  # Auth screens (if enabled)
│   ├── sign-in.tsx
│   └── sign-up.tsx
└── [entity]/
    └── [id].tsx             # Detail screens
```

**Stack-based App:**
```
app/
├── _layout.tsx              # Root layout with providers
├── index.tsx                # Home screen
├── [screen].tsx             # Other screens
└── (auth)/                  # Auth screens (if enabled)
```

### Phase 4: Component Generation

**Generated Components:**
```
components/
├── ui/
│   ├── Button.tsx
│   ├── Input.tsx
│   ├── Card.tsx
│   └── Text.tsx
├── [entity]/
│   ├── [Entity]List.tsx
│   ├── [Entity]Item.tsx
│   └── [Entity]Form.tsx
└── layout/
    ├── Header.tsx
    └── SafeContainer.tsx
```

### Phase 5: Quality Setup

**Biome Configuration:**
- `biome.json` with React Native rules
- Import organization
- 100 character line width

**TypeScript:**
- Strict mode enabled
- Path aliases configured
- Expo types included

### Phase 6: Verification

Run quality gate and report results:

```
✅ Generation complete!

Quality Report:
- bun install: ✓ succeeded
- bun run lint: ✓ 0 errors
- TypeScript: ✓ no errors

Ready to run:
  cd [project]
  bun start
```

---

## Usage

```bash
# Create app with PRD-style prompt
python3 ~/.codex/skills/expo-architect/scripts/init-expo.py \
  --root ~/www/myapp \
  --name "My App" \
  --brief "A fitness tracker where users can log workouts, track progress, and set goals."

# Or interactive mode
python3 ~/.codex/skills/expo-architect/scripts/init-expo.py \
  --root ~/www/myapp \
  --name "My App" \
  --interactive

# With specific options
python3 ~/.codex/skills/expo-architect/scripts/init-expo.py \
  --root ~/www/myapp \
  --name "My App" \
  --tabs "Home,Workouts,Profile" \
  --auth
```

---

## Generated Structure

```
myapp/
├── .agent/                  # AI documentation
├── app/
│   ├── _layout.tsx          # Root layout
│   ├── (tabs)/
│   │   ├── _layout.tsx      # Tab navigator
│   │   ├── index.tsx        # Home
│   │   ├── workouts.tsx     # Workouts
│   │   └── profile.tsx      # Profile
│   ├── (auth)/              # Auth screens
│   │   ├── sign-in.tsx
│   │   └── sign-up.tsx
│   └── workout/
│       └── [id].tsx         # Workout detail
├── components/
│   ├── ui/                  # Base UI components
│   ├── workout/             # Feature components
│   └── layout/              # Layout components
├── lib/
│   ├── api.ts               # API client
│   ├── auth.ts              # Auth utilities
│   └── storage.ts           # AsyncStorage helpers
├── providers/
│   ├── clerk-provider.tsx   # Auth provider
│   └── query-provider.tsx   # React Query provider
├── types/
│   └── index.ts             # TypeScript types
├── app.json                 # Expo config
├── app.config.ts            # Dynamic config
├── package.json
├── tsconfig.json
├── biome.json
└── .env.example
```

---

## Key Patterns

### Root Layout Pattern

```typescript
import { Stack } from "expo-router";
import { StatusBar } from "expo-status-bar";
import { ClerkProvider } from "@/providers/clerk-provider";
import { QueryProvider } from "@/providers/query-provider";

export default function RootLayout() {
  return (
    <ClerkProvider>
      <QueryProvider>
        <Stack>
          <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
          <Stack.Screen name="(auth)" options={{ headerShown: false }} />
        </Stack>
        <StatusBar style="auto" />
      </QueryProvider>
    </ClerkProvider>
  );
}
```

### Tab Navigator Pattern

```typescript
import { Tabs } from "expo-router";
import { Home, Dumbbell, User } from "lucide-react-native";

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: "#3b82f6",
        tabBarInactiveTintColor: "#9ca3af",
        tabBarStyle: { backgroundColor: "#0f172a" },
        headerStyle: { backgroundColor: "#0f172a" },
        headerTintColor: "#fff",
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: "Home",
          tabBarIcon: ({ color, size }) => <Home size={size} color={color} />,
        }}
      />
      <Tabs.Screen
        name="workouts"
        options={{
          title: "Workouts",
          tabBarIcon: ({ color, size }) => <Dumbbell size={size} color={color} />,
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: "Profile",
          tabBarIcon: ({ color, size }) => <User size={size} color={color} />,
        }}
      />
    </Tabs>
  );
}
```

### Screen Component Pattern

```typescript
import { View, Text, FlatList, StyleSheet } from "react-native";
import { useEffect, useState } from "react";
import { SafeContainer } from "@/components/layout/SafeContainer";
import { WorkoutItem } from "@/components/workout/WorkoutItem";
import { api } from "@/lib/api";
import type { Workout } from "@/types";

export default function WorkoutsScreen() {
  const [workouts, setWorkouts] = useState<Workout[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.workouts.getAll()
      .then(setWorkouts)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <SafeContainer style={styles.center}>
        <Text>Loading...</Text>
      </SafeContainer>
    );
  }

  return (
    <SafeContainer>
      <FlatList
        data={workouts}
        keyExtractor={(item) => item._id}
        renderItem={({ item }) => <WorkoutItem workout={item} />}
        contentContainerStyle={styles.list}
      />
    </SafeContainer>
  );
}

const styles = StyleSheet.create({
  center: { flex: 1, alignItems: "center", justifyContent: "center" },
  list: { padding: 16, gap: 12 },
});
```

### API Client Pattern

```typescript
const API_URL = process.env.EXPO_PUBLIC_API_URL || "http://localhost:3001";

async function getAuthToken(): Promise<string | null> {
  // Get token from Clerk
  const clerk = (global as any).Clerk;
  if (!clerk?.session) return null;
  return clerk.session.getToken();
}

async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = await getAuthToken();

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`);
  }

  return response.json();
}

export const api = {
  workouts: {
    getAll: () => request<Workout[]>("/workouts"),
    getById: (id: string) => request<Workout>(`/workouts/${id}`),
    create: (data: Partial<Workout>) =>
      request<Workout>("/workouts", {
        method: "POST",
        body: JSON.stringify(data),
      }),
    update: (id: string, data: Partial<Workout>) =>
      request<Workout>(`/workouts/${id}`, {
        method: "PATCH",
        body: JSON.stringify(data),
      }),
    delete: (id: string) =>
      request<void>(`/workouts/${id}`, { method: "DELETE" }),
  },
};
```

---

## Development Commands

After scaffolding:

```bash
cd myapp

# Install dependencies
bun install

# Start Expo development server
bun start

# Run on specific platform
bun run ios      # iOS simulator
bun run android  # Android emulator
bun run web      # Web browser

# Quality commands
bun run lint         # Check code style
bun run lint:fix     # Fix code style
bun run typecheck    # Type checking
```

---

## Environment Variables

Create `.env` based on `.env.example`:

```
# Clerk (if using auth)
EXPO_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...

# API
EXPO_PUBLIC_API_URL=http://localhost:3001
```

---

## EAS Build Configuration

For production builds, create `eas.json`:

```json
{
  "cli": { "version": ">= 5.0.0" },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "preview": {
      "distribution": "internal"
    },
    "production": {}
  },
  "submit": {
    "production": {}
  }
}
```

---

## References

- `references/templates/` - Code generation templates
- `references/patterns/` - Common mobile patterns
