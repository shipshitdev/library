#!/usr/bin/env python3
"""
Scaffold a production-ready Expo React Native app.

This script creates a complete Expo mobile app with:
- Expo Router for file-based navigation
- Optional Clerk authentication
- TypeScript with strict mode
- Biome linting
- Working screens and components

Usage:
  python3 init-expo.py --root ~/www/myapp --name "My App"
  python3 init-expo.py --root ~/www/myapp --name "Fitness" --tabs "Home,Workouts,Profile" --auth
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from textwrap import dedent
from dataclasses import dataclass


@dataclass
class ScreenConfig:
    """Configuration for a screen to be generated."""
    name: str  # e.g., "Home"
    icon: str = "Home"  # Lucide icon name

    @property
    def pascal_case(self) -> str:
        return self.name[0].upper() + self.name[1:]

    @property
    def kebab_case(self) -> str:
        return self.name.lower().replace(" ", "-")

    @property
    def file_name(self) -> str:
        if self.name.lower() == "home":
            return "index"
        return self.kebab_case


# =============================================================================
# PACKAGE.JSON AND CONFIG TEMPLATES
# =============================================================================

def create_package_json(name: str, with_auth: bool) -> str:
    slug = name.lower().replace(" ", "-")
    deps = {
        "expo": "~54.0.0",
        "expo-router": "~6.0.0",
        "expo-status-bar": "~3.0.0",
        "expo-constants": "~18.0.0",
        "expo-linking": "~7.0.0",
        "react": "19.0.0",
        "react-native": "0.83.0",
        "react-native-safe-area-context": "~5.4.0",
        "react-native-screens": "~4.10.0",
        "lucide-react-native": "~0.470.0",
        "react-native-svg": "~15.9.0",
    }

    if with_auth:
        deps["@clerk/clerk-expo"] = "~4.0.0"
        deps["expo-secure-store"] = "~15.0.0"

    return json.dumps({
        "name": slug,
        "version": "1.0.0",
        "main": "expo-router/entry",
        "scripts": {
            "start": "expo start",
            "android": "expo start --android",
            "ios": "expo start --ios",
            "web": "expo start --web",
            "lint": "biome check .",
            "lint:fix": "biome check --write .",
            "typecheck": "tsc --noEmit"
        },
        "dependencies": deps,
        "devDependencies": {
            "@types/react": "~19.0.0",
            "typescript": "~5.9.0",
            "@biomejs/biome": "~2.3.0"
        }
    }, indent=2)


def create_app_json(name: str) -> str:
    slug = name.lower().replace(" ", "-")
    return json.dumps({
        "expo": {
            "name": name,
            "slug": slug,
            "version": "1.0.0",
            "scheme": slug,
            "platforms": ["ios", "android"],
            "ios": {
                "supportsTablet": True,
                "bundleIdentifier": f"com.{slug.replace('-', '')}.app"
            },
            "android": {
                "package": f"com.{slug.replace('-', '')}.app"
            },
            "experiments": {
                "typedRoutes": True
            }
        }
    }, indent=2)


def create_tsconfig() -> str:
    return json.dumps({
        "extends": "expo/tsconfig.base",
        "compilerOptions": {
            "strict": True,
            "baseUrl": ".",
            "paths": {
                "@/*": ["./*"],
                "@/components/*": ["components/*"],
                "@/lib/*": ["lib/*"],
                "@/providers/*": ["providers/*"],
                "@/types/*": ["types/*"]
            }
        },
        "include": ["**/*.ts", "**/*.tsx", ".expo/types/**/*.ts", "expo-env.d.ts"]
    }, indent=2)


def create_biome_config() -> str:
    return json.dumps({
        "$schema": "https://biomejs.dev/schemas/2.3.0/schema.json",
        "assist": {
            "actions": {
                "source": {"organizeImports": "on"}
            }
        },
        "files": {
            "ignore": ["node_modules", ".expo", "dist"]
        },
        "formatter": {
            "enabled": True,
            "indentStyle": "space",
            "indentWidth": 2,
            "lineWidth": 100
        },
        "linter": {
            "enabled": True,
            "rules": {
                "recommended": True
            }
        },
        "javascript": {
            "formatter": {
                "quoteStyle": "double",
                "semicolons": "always",
                "trailingCommas": "es5"
            }
        }
    }, indent=2)


def create_env_example(with_auth: bool) -> str:
    content = "# API\nEXPO_PUBLIC_API_URL=http://localhost:3001\n"
    if with_auth:
        content += "\n# Clerk Authentication\nEXPO_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_xxx\n"
    return content


def create_gitignore() -> str:
    return dedent("""\
        # Dependencies
        node_modules/

        # Expo
        .expo/
        dist/
        web-build/

        # Native
        *.orig.*
        *.jks
        *.p8
        *.p12
        *.key
        *.mobileprovision

        # Environment
        .env
        .env.local
        .env.*.local

        # OS
        .DS_Store
        Thumbs.db

        # IDE
        .idea/
        .vscode/
    """)


# =============================================================================
# ROOT LAYOUT AND PROVIDERS
# =============================================================================

def create_root_layout(with_auth: bool) -> str:
    if with_auth:
        return dedent("""\
            import { Stack } from "expo-router";
            import { StatusBar } from "expo-status-bar";
            import { ClerkProvider } from "@/providers/clerk-provider";

            export default function RootLayout() {
              return (
                <ClerkProvider>
                  <Stack>
                    <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
                    <Stack.Screen name="(auth)" options={{ headerShown: false }} />
                  </Stack>
                  <StatusBar style="auto" />
                </ClerkProvider>
              );
            }
        """)
    else:
        return dedent("""\
            import { Stack } from "expo-router";
            import { StatusBar } from "expo-status-bar";

            export default function RootLayout() {
              return (
                <>
                  <Stack>
                    <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
                  </Stack>
                  <StatusBar style="auto" />
                </>
              );
            }
        """)


def create_clerk_provider() -> str:
    return dedent("""\
        import { ClerkProvider as BaseClerkProvider } from "@clerk/clerk-expo";
        import * as SecureStore from "expo-secure-store";
        import { ReactNode } from "react";

        const publishableKey = process.env.EXPO_PUBLIC_CLERK_PUBLISHABLE_KEY!;

        const tokenCache = {
          async getToken(key: string) {
            try {
              return SecureStore.getItemAsync(key);
            } catch {
              return null;
            }
          },
          async saveToken(key: string, value: string) {
            try {
              return SecureStore.setItemAsync(key, value);
            } catch {
              return;
            }
          },
        };

        interface Props {
          children: ReactNode;
        }

        export function ClerkProvider({ children }: Props) {
          return (
            <BaseClerkProvider publishableKey={publishableKey} tokenCache={tokenCache}>
              {children}
            </BaseClerkProvider>
          );
        }
    """)


# =============================================================================
# TAB NAVIGATOR
# =============================================================================

def create_tab_layout(screens: list[ScreenConfig]) -> str:
    imports = ["import { Tabs } from \"expo-router\";"]
    icon_imports = ", ".join(s.icon for s in screens)
    imports.append(f'import {{ {icon_imports} }} from "lucide-react-native";')

    tabs = []
    for screen in screens:
        tabs.append(f"""\
      <Tabs.Screen
        name="{screen.file_name}"
        options={{{{
          title: "{screen.pascal_case}",
          tabBarIcon: ({{ color, size }}) => <{screen.icon} size={{size}} color={{color}} />,
        }}}}
      />""")

    tabs_str = "\n".join(tabs)

    return dedent(f"""\
        {chr(10).join(imports)}

        export default function TabLayout() {{
          return (
            <Tabs
              screenOptions={{{{
                tabBarActiveTintColor: "#3b82f6",
                tabBarInactiveTintColor: "#9ca3af",
                tabBarStyle: {{ backgroundColor: "#0f172a" }},
                headerStyle: {{ backgroundColor: "#0f172a" }},
                headerTintColor: "#fff",
              }}}}
            >
        {tabs_str}
            </Tabs>
          );
        }}
    """)


def create_screen_component(screen: ScreenConfig) -> str:
    return dedent(f"""\
        import {{ View, Text, StyleSheet }} from "react-native";
        import {{ SafeContainer }} from "@/components/layout/SafeContainer";

        export default function {screen.pascal_case}Screen() {{
          return (
            <SafeContainer>
              <View style={{styles.container}}>
                <Text style={{styles.title}}>{screen.pascal_case}</Text>
                <Text style={{styles.subtitle}}>This is the {screen.name.lower()} screen.</Text>
              </View>
            </SafeContainer>
          );
        }}

        const styles = StyleSheet.create({{
          container: {{
            flex: 1,
            padding: 20,
          }},
          title: {{
            fontSize: 28,
            fontWeight: "bold",
            color: "#fff",
            marginBottom: 8,
          }},
          subtitle: {{
            fontSize: 16,
            color: "#9ca3af",
          }},
        }});
    """)


# =============================================================================
# AUTH SCREENS
# =============================================================================

def create_auth_layout() -> str:
    return dedent("""\
        import { Stack } from "expo-router";

        export default function AuthLayout() {
          return (
            <Stack
              screenOptions={{
                headerStyle: { backgroundColor: "#0f172a" },
                headerTintColor: "#fff",
              }}
            >
              <Stack.Screen name="sign-in" options={{ title: "Sign In" }} />
              <Stack.Screen name="sign-up" options={{ title: "Sign Up" }} />
            </Stack>
          );
        }
    """)


def create_sign_in_screen() -> str:
    return dedent("""\
        import { View, Text, TextInput, Pressable, StyleSheet } from "react-native";
        import { useState } from "react";
        import { useSignIn } from "@clerk/clerk-expo";
        import { useRouter } from "expo-router";
        import { SafeContainer } from "@/components/layout/SafeContainer";

        export default function SignInScreen() {
          const { signIn, setActive, isLoaded } = useSignIn();
          const router = useRouter();
          const [email, setEmail] = useState("");
          const [password, setPassword] = useState("");
          const [error, setError] = useState("");

          const handleSignIn = async () => {
            if (!isLoaded) return;

            try {
              const result = await signIn.create({
                identifier: email,
                password,
              });

              if (result.status === "complete") {
                await setActive({ session: result.createdSessionId });
                router.replace("/(tabs)");
              }
            } catch (err: any) {
              setError(err.errors?.[0]?.message || "Sign in failed");
            }
          };

          return (
            <SafeContainer>
              <View style={styles.container}>
                <Text style={styles.title}>Welcome Back</Text>

                {error && <Text style={styles.error}>{error}</Text>}

                <TextInput
                  style={styles.input}
                  placeholder="Email"
                  placeholderTextColor="#9ca3af"
                  value={email}
                  onChangeText={setEmail}
                  autoCapitalize="none"
                  keyboardType="email-address"
                />

                <TextInput
                  style={styles.input}
                  placeholder="Password"
                  placeholderTextColor="#9ca3af"
                  value={password}
                  onChangeText={setPassword}
                  secureTextEntry
                />

                <Pressable style={styles.button} onPress={handleSignIn}>
                  <Text style={styles.buttonText}>Sign In</Text>
                </Pressable>

                <Pressable onPress={() => router.push("/(auth)/sign-up")}>
                  <Text style={styles.link}>Don't have an account? Sign Up</Text>
                </Pressable>
              </View>
            </SafeContainer>
          );
        }

        const styles = StyleSheet.create({
          container: {
            flex: 1,
            padding: 20,
            justifyContent: "center",
          },
          title: {
            fontSize: 28,
            fontWeight: "bold",
            color: "#fff",
            marginBottom: 24,
            textAlign: "center",
          },
          input: {
            backgroundColor: "#1e293b",
            color: "#fff",
            padding: 16,
            borderRadius: 8,
            marginBottom: 12,
            fontSize: 16,
          },
          button: {
            backgroundColor: "#3b82f6",
            padding: 16,
            borderRadius: 8,
            alignItems: "center",
            marginTop: 8,
          },
          buttonText: {
            color: "#fff",
            fontSize: 16,
            fontWeight: "600",
          },
          link: {
            color: "#3b82f6",
            textAlign: "center",
            marginTop: 16,
          },
          error: {
            color: "#ef4444",
            marginBottom: 12,
            textAlign: "center",
          },
        });
    """)


def create_sign_up_screen() -> str:
    return dedent("""\
        import { View, Text, TextInput, Pressable, StyleSheet } from "react-native";
        import { useState } from "react";
        import { useSignUp } from "@clerk/clerk-expo";
        import { useRouter } from "expo-router";
        import { SafeContainer } from "@/components/layout/SafeContainer";

        export default function SignUpScreen() {
          const { signUp, setActive, isLoaded } = useSignUp();
          const router = useRouter();
          const [email, setEmail] = useState("");
          const [password, setPassword] = useState("");
          const [error, setError] = useState("");

          const handleSignUp = async () => {
            if (!isLoaded) return;

            try {
              const result = await signUp.create({
                emailAddress: email,
                password,
              });

              if (result.status === "complete") {
                await setActive({ session: result.createdSessionId });
                router.replace("/(tabs)");
              }
            } catch (err: any) {
              setError(err.errors?.[0]?.message || "Sign up failed");
            }
          };

          return (
            <SafeContainer>
              <View style={styles.container}>
                <Text style={styles.title}>Create Account</Text>

                {error && <Text style={styles.error}>{error}</Text>}

                <TextInput
                  style={styles.input}
                  placeholder="Email"
                  placeholderTextColor="#9ca3af"
                  value={email}
                  onChangeText={setEmail}
                  autoCapitalize="none"
                  keyboardType="email-address"
                />

                <TextInput
                  style={styles.input}
                  placeholder="Password"
                  placeholderTextColor="#9ca3af"
                  value={password}
                  onChangeText={setPassword}
                  secureTextEntry
                />

                <Pressable style={styles.button} onPress={handleSignUp}>
                  <Text style={styles.buttonText}>Sign Up</Text>
                </Pressable>

                <Pressable onPress={() => router.push("/(auth)/sign-in")}>
                  <Text style={styles.link}>Already have an account? Sign In</Text>
                </Pressable>
              </View>
            </SafeContainer>
          );
        }

        const styles = StyleSheet.create({
          container: {
            flex: 1,
            padding: 20,
            justifyContent: "center",
          },
          title: {
            fontSize: 28,
            fontWeight: "bold",
            color: "#fff",
            marginBottom: 24,
            textAlign: "center",
          },
          input: {
            backgroundColor: "#1e293b",
            color: "#fff",
            padding: 16,
            borderRadius: 8,
            marginBottom: 12,
            fontSize: 16,
          },
          button: {
            backgroundColor: "#3b82f6",
            padding: 16,
            borderRadius: 8,
            alignItems: "center",
            marginTop: 8,
          },
          buttonText: {
            color: "#fff",
            fontSize: 16,
            fontWeight: "600",
          },
          link: {
            color: "#3b82f6",
            textAlign: "center",
            marginTop: 16,
          },
          error: {
            color: "#ef4444",
            marginBottom: 12,
            textAlign: "center",
          },
        });
    """)


# =============================================================================
# UI COMPONENTS
# =============================================================================

def create_safe_container() -> str:
    return dedent("""\
        import { SafeAreaView, StyleSheet, ViewStyle } from "react-native";
        import { ReactNode } from "react";

        interface Props {
          children: ReactNode;
          style?: ViewStyle;
        }

        export function SafeContainer({ children, style }: Props) {
          return (
            <SafeAreaView style={[styles.container, style]}>
              {children}
            </SafeAreaView>
          );
        }

        const styles = StyleSheet.create({
          container: {
            flex: 1,
            backgroundColor: "#0f172a",
          },
        });
    """)


def create_button_component() -> str:
    return dedent("""\
        import { Pressable, Text, StyleSheet, ViewStyle } from "react-native";
        import { ReactNode } from "react";

        interface Props {
          children: ReactNode;
          onPress: () => void;
          variant?: "primary" | "secondary" | "ghost";
          style?: ViewStyle;
        }

        export function Button({ children, onPress, variant = "primary", style }: Props) {
          return (
            <Pressable
              style={[styles.button, styles[variant], style]}
              onPress={onPress}
            >
              <Text style={[styles.text, variant === "ghost" && styles.ghostText]}>
                {children}
              </Text>
            </Pressable>
          );
        }

        const styles = StyleSheet.create({
          button: {
            padding: 16,
            borderRadius: 8,
            alignItems: "center",
          },
          primary: {
            backgroundColor: "#3b82f6",
          },
          secondary: {
            backgroundColor: "#1e293b",
          },
          ghost: {
            backgroundColor: "transparent",
          },
          text: {
            color: "#fff",
            fontSize: 16,
            fontWeight: "600",
          },
          ghostText: {
            color: "#3b82f6",
          },
        });
    """)


def create_input_component() -> str:
    return dedent("""\
        import { TextInput, StyleSheet, TextInputProps } from "react-native";

        interface Props extends TextInputProps {
          // Add custom props here
        }

        export function Input(props: Props) {
          return (
            <TextInput
              style={styles.input}
              placeholderTextColor="#9ca3af"
              {...props}
            />
          );
        }

        const styles = StyleSheet.create({
          input: {
            backgroundColor: "#1e293b",
            color: "#fff",
            padding: 16,
            borderRadius: 8,
            fontSize: 16,
          },
        });
    """)


def create_card_component() -> str:
    return dedent("""\
        import { View, StyleSheet, ViewStyle } from "react-native";
        import { ReactNode } from "react";

        interface Props {
          children: ReactNode;
          style?: ViewStyle;
        }

        export function Card({ children, style }: Props) {
          return (
            <View style={[styles.card, style]}>
              {children}
            </View>
          );
        }

        const styles = StyleSheet.create({
          card: {
            backgroundColor: "#1e293b",
            borderRadius: 12,
            padding: 16,
          },
        });
    """)


# =============================================================================
# LIB FILES
# =============================================================================

def create_api_client() -> str:
    return dedent("""\
        const API_URL = process.env.EXPO_PUBLIC_API_URL || "http://localhost:3001";

        async function getAuthToken(): Promise<string | null> {
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
          get: <T>(endpoint: string) => request<T>(endpoint),
          post: <T>(endpoint: string, data: unknown) =>
            request<T>(endpoint, {
              method: "POST",
              body: JSON.stringify(data),
            }),
          patch: <T>(endpoint: string, data: unknown) =>
            request<T>(endpoint, {
              method: "PATCH",
              body: JSON.stringify(data),
            }),
          delete: <T>(endpoint: string) =>
            request<T>(endpoint, { method: "DELETE" }),
        };
    """)


def create_types_index() -> str:
    return dedent("""\
        // Add your TypeScript types here

        export interface User {
          _id: string;
          email: string;
          name?: string;
          createdAt: string;
          updatedAt: string;
        }

        // Example entity type
        export interface Entity {
          _id: string;
          title: string;
          description?: string;
          userId: string;
          createdAt: string;
          updatedAt: string;
        }
    """)


# =============================================================================
# MAIN SCAFFOLD FUNCTION
# =============================================================================

def scaffold_expo_app(
    root: Path,
    name: str,
    screens: list[ScreenConfig],
    with_auth: bool,
    allow_outside: bool,
) -> None:
    """Create the full Expo app structure."""

    cwd = Path.cwd()
    if not allow_outside and not root.is_relative_to(cwd):
        print(f"Error: Target path {root} is outside current directory.")
        print("Use --allow-outside to confirm this is intentional.")
        sys.exit(1)

    if root.exists():
        print(f"Error: {root} already exists.")
        sys.exit(1)

    print(f"Creating Expo app at {root}...")
    print(f"Screens: {', '.join(s.name for s in screens)}")
    print(f"Auth: {'Yes' if with_auth else 'No'}")

    # Create directories
    dirs = [
        root,
        root / ".agent",
        root / "app" / "(tabs)",
        root / "components" / "layout",
        root / "components" / "ui",
        root / "lib",
        root / "types",
    ]

    if with_auth:
        dirs.extend([
            root / "app" / "(auth)",
            root / "providers",
        ])

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # Base files
    files = {
        root / "package.json": create_package_json(name, with_auth),
        root / "app.json": create_app_json(name),
        root / "tsconfig.json": create_tsconfig(),
        root / "biome.json": create_biome_config(),
        root / ".env.example": create_env_example(with_auth),
        root / ".gitignore": create_gitignore(),

        # Root layout
        root / "app" / "_layout.tsx": create_root_layout(with_auth),

        # Tab navigator
        root / "app" / "(tabs)" / "_layout.tsx": create_tab_layout(screens),

        # Components
        root / "components" / "layout" / "SafeContainer.tsx": create_safe_container(),
        root / "components" / "ui" / "Button.tsx": create_button_component(),
        root / "components" / "ui" / "Input.tsx": create_input_component(),
        root / "components" / "ui" / "Card.tsx": create_card_component(),

        # Lib
        root / "lib" / "api.ts": create_api_client(),

        # Types
        root / "types" / "index.ts": create_types_index(),
    }

    # Screen files
    for screen in screens:
        files[root / "app" / "(tabs)" / f"{screen.file_name}.tsx"] = create_screen_component(screen)

    # Auth files
    if with_auth:
        files[root / "providers" / "clerk-provider.tsx"] = create_clerk_provider()
        files[root / "app" / "(auth)" / "_layout.tsx"] = create_auth_layout()
        files[root / "app" / "(auth)" / "sign-in.tsx"] = create_sign_in_screen()
        files[root / "app" / "(auth)" / "sign-up.tsx"] = create_sign_up_screen()

    # Write all files
    for filepath, content in files.items():
        filepath.write_text(content)
        print(f"Created: {filepath.relative_to(root)}")

    print(f"\n✅ Expo app created at: {root}")
    print(f"\nNext steps:")
    print(f"1. cd {root}")
    print(f"2. bun install")
    if with_auth:
        print(f"3. Copy .env.example to .env and add your Clerk key")
        print(f"4. bun start")
    else:
        print(f"3. bun start")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold a production-ready Expo React Native app."
    )
    parser.add_argument(
        "--root",
        type=Path,
        required=True,
        help="Directory to create the app in",
    )
    parser.add_argument(
        "--name",
        type=str,
        required=True,
        help="App name",
    )
    parser.add_argument(
        "--tabs",
        type=str,
        default="Home,Settings",
        help="Comma-separated list of tab names (default: 'Home,Settings')",
    )
    parser.add_argument(
        "--auth",
        action="store_true",
        help="Include Clerk authentication",
    )
    parser.add_argument(
        "--allow-outside",
        action="store_true",
        help="Allow creating files outside current directory",
    )

    args = parser.parse_args()

    # Parse screens with default icons
    icon_map = {
        "home": "Home",
        "settings": "Settings",
        "profile": "User",
        "search": "Search",
        "workouts": "Dumbbell",
        "explore": "Compass",
        "favorites": "Heart",
        "notifications": "Bell",
        "messages": "MessageCircle",
        "calendar": "Calendar",
    }

    screens = []
    for tab_name in args.tabs.split(","):
        tab_name = tab_name.strip()
        icon = icon_map.get(tab_name.lower(), "Circle")
        screens.append(ScreenConfig(name=tab_name, icon=icon))

    scaffold_expo_app(
        root=args.root.resolve(),
        name=args.name,
        screens=screens,
        with_auth=args.auth,
        allow_outside=args.allow_outside,
    )


if __name__ == "__main__":
    main()
