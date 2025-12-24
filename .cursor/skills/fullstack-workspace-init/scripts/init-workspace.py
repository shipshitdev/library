#!/usr/bin/env python3
"""
Scaffold a full-stack monorepo workspace.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from textwrap import dedent


def create_root_package_json(name: str) -> str:
    return json.dumps({
        "name": name.lower().replace(" ", "-"),
        "version": "0.0.1",
        "private": True,
        "workspaces": [
            "api",
            "frontend",
            "mobile",
            "packages"
        ],
        "scripts": {
            "dev:api": "cd api && bun run start:dev",
            "dev:frontend": "cd frontend && bun run dev",
            "dev:mobile": "cd mobile && bun run start"
        }
    }, indent=2)


def create_npmrc() -> str:
    return "engine-strict=true\n"


def create_gitignore() -> str:
    return dedent("""\
        # Dependencies
        node_modules/
        .pnp
        .pnp.js

        # Build
        dist/
        build/
        .next/
        out/

        # Environment
        .env
        .env.local
        .env.*.local

        # Logs
        logs/
        *.log
        npm-debug.log*

        # OS
        .DS_Store
        Thumbs.db

        # IDE
        .idea/
        .vscode/
        *.swp
        *.swo

        # Test
        coverage/

        # Misc
        .vercel
        .turbo
    """)


def create_readme(name: str) -> str:
    return dedent(f"""\
        # {name}

        Full-stack monorepo workspace.

        ## Structure

        - `api/` - NestJS backend
        - `frontend/` - NextJS apps
        - `mobile/` - React Native + Expo
        - `packages/` - Shared packages

        ## Getting Started

        ```bash
        bun install
        ```

        ## Development

        ```bash
        # Backend
        cd api && bun run start:dev

        # Frontend
        cd frontend && bun run dev

        # Mobile
        cd mobile && bun run start
        ```

        ## Documentation

        See `.agent/README.md` for AI documentation.
    """)


def create_agents_md(name: str) -> str:
    return dedent(f"""\
        # {name}

        AI agent entry point. Documentation in `.agent/`.

        ## Projects

        - `api/` - NestJS backend → `api/.agent/`
        - `frontend/` - NextJS apps → `frontend/.agent/`
        - `mobile/` - React Native → `mobile/.agent/`
        - `packages/` - Shared → `packages/.agent/`

        ## Quick Start

        Read `.agent/SYSTEM/ai/SESSION-QUICK-START.md` first.
    """)


def create_claude_md(name: str) -> str:
    return dedent(f"""\
        # {name}

        Claude entry point. Rules in `.agent/SYSTEM/RULES.md`.

        ## Commands

        ```bash
        bun run dev:api      # Start backend
        bun run dev:frontend # Start frontend
        bun run dev:mobile   # Start mobile
        ```

        ## Critical Rules

        See `.agent/SYSTEM/critical/CRITICAL-NEVER-DO.md`
    """)


def create_codex_md(name: str) -> str:
    return dedent(f"""\
        # {name}

        Codex entry point. Documentation in `.agent/`.
    """)


# API Templates
def create_api_package_json(org: str) -> str:
    return json.dumps({
        "name": f"@{org}/api",
        "version": "0.0.1",
        "private": True,
        "scripts": {
            "build": "nest build",
            "start": "nest start",
            "start:dev": "nest start --watch",
            "start:debug": "nest start --debug --watch",
            "start:prod": "node dist/main",
            "lint": "eslint \"{src,apps,libs,test}/**/*.ts\"",
            "test": "jest"
        },
        "dependencies": {
            "@nestjs/common": "^11.0.0",
            "@nestjs/core": "^11.0.0",
            "@nestjs/mongoose": "^11.0.0",
            "@nestjs/platform-express": "^11.0.0",
            "@nestjs/swagger": "^8.0.0",
            "mongoose": "^8.0.0",
            "reflect-metadata": "^0.2.0",
            "rxjs": "^7.8.0",
            "class-validator": "^0.14.0",
            "class-transformer": "^0.5.0"
        },
        "devDependencies": {
            "@nestjs/cli": "^11.0.0",
            "@nestjs/schematics": "^11.0.0",
            "@types/express": "^5.0.0",
            "@types/node": "^22.0.0",
            "typescript": "^5.7.0"
        }
    }, indent=2)


def create_nest_cli_json() -> str:
    return json.dumps({
        "$schema": "https://json.schemastore.org/nest-cli",
        "collection": "@nestjs/schematics",
        "sourceRoot": "apps/api/src",
        "monorepo": True,
        "root": "apps/api",
        "compilerOptions": {
            "webpack": False,
            "tsConfigPath": "tsconfig.json"
        },
        "projects": {
            "api": {
                "type": "application",
                "root": "apps/api",
                "entryFile": "main",
                "sourceRoot": "apps/api/src"
            }
        }
    }, indent=2)


def create_api_tsconfig() -> str:
    return json.dumps({
        "compilerOptions": {
            "module": "commonjs",
            "declaration": True,
            "removeComments": True,
            "emitDecoratorMetadata": True,
            "experimentalDecorators": True,
            "allowSyntheticDefaultImports": True,
            "target": "ES2021",
            "sourceMap": True,
            "outDir": "./dist",
            "baseUrl": "./",
            "incremental": True,
            "skipLibCheck": True,
            "strictNullChecks": True,
            "noImplicitAny": True,
            "strictBindCallApply": True,
            "forceConsistentCasingInFileNames": True,
            "noFallthroughCasesInSwitch": True,
            "paths": {
                "@collections/*": ["apps/api/src/collections/*"],
                "@services/*": ["apps/api/src/services/*"],
                "@guards/*": ["apps/api/src/guards/*"],
                "@helpers/*": ["apps/api/src/helpers/*"]
            }
        }
    }, indent=2)


def create_api_main_ts() -> str:
    return dedent("""\
        import { NestFactory } from "@nestjs/core";
        import { ValidationPipe } from "@nestjs/common";
        import { SwaggerModule, DocumentBuilder } from "@nestjs/swagger";
        import { AppModule } from "./app.module";

        async function bootstrap() {
          const app = await NestFactory.create(AppModule);

          // Validation
          app.useGlobalPipes(
            new ValidationPipe({
              whitelist: true,
              transform: true,
            })
          );

          // CORS
          app.enableCors();

          // Swagger
          const config = new DocumentBuilder()
            .setTitle("API")
            .setDescription("API Documentation")
            .setVersion("1.0")
            .addBearerAuth()
            .build();
          const document = SwaggerModule.createDocument(app, config);
          SwaggerModule.setup("api/docs", app, document);

          const port = process.env.PORT || 3001;
          await app.listen(port);
          console.log(`API running on http://localhost:${port}`);
        }
        bootstrap();
    """)


def create_api_app_module_ts() -> str:
    return dedent("""\
        import { Module } from "@nestjs/common";
        import { ConfigModule } from "@nestjs/config";
        import { MongooseModule } from "@nestjs/mongoose";

        @Module({
          imports: [
            ConfigModule.forRoot({
              isGlobal: true,
            }),
            MongooseModule.forRoot(process.env.MONGODB_URI || "mongodb://localhost/api"),
          ],
          controllers: [],
          providers: [],
        })
        export class AppModule {}
    """)


def create_api_dockerfile() -> str:
    return dedent("""\
        FROM oven/bun:1 AS base
        WORKDIR /app

        # Install dependencies
        FROM base AS deps
        COPY package.json bun.lockb ./
        RUN bun install --frozen-lockfile

        # Build
        FROM base AS builder
        COPY --from=deps /app/node_modules ./node_modules
        COPY . .
        RUN bun run build

        # Production
        FROM base AS runner
        ENV NODE_ENV=production
        COPY --from=builder /app/dist ./dist
        COPY --from=builder /app/node_modules ./node_modules
        EXPOSE 3001
        CMD ["bun", "run", "start:prod"]
    """)


# Frontend Templates
def create_frontend_package_json(org: str) -> str:
    return json.dumps({
        "name": f"@{org}/frontend",
        "version": "0.0.1",
        "private": True,
        "scripts": {
            "dev": "next dev --turbo",
            "build": "next build",
            "start": "next start",
            "lint": "next lint"
        },
        "dependencies": {
            "next": "^15.0.0",
            "react": "^19.0.0",
            "react-dom": "^19.0.0",
            "axios": "^1.7.0",
            "zustand": "^5.0.0",
            "react-hook-form": "^7.50.0",
            "zod": "^3.23.0",
            "@hookform/resolvers": "^3.9.0"
        },
        "devDependencies": {
            "@types/node": "^22.0.0",
            "@types/react": "^19.0.0",
            "@types/react-dom": "^19.0.0",
            "typescript": "^5.7.0",
            "tailwindcss": "^4.0.0",
            "@tailwindcss/postcss": "^4.0.0",
            "daisyui": "^5.0.0"
        }
    }, indent=2)


def create_frontend_next_config() -> str:
    return dedent("""\
        import type { NextConfig } from "next";

        const nextConfig: NextConfig = {
          reactStrictMode: true,
        };

        export default nextConfig;
    """)


def create_frontend_tailwind_config() -> str:
    return dedent("""\
        import type { Config } from "tailwindcss";
        import daisyui from "daisyui";

        const config: Config = {
          content: [
            "./apps/**/*.{js,ts,jsx,tsx,mdx}",
            "./packages/**/*.{js,ts,jsx,tsx,mdx}",
          ],
          theme: {
            extend: {},
          },
          plugins: [daisyui],
          daisyui: {
            themes: ["light", "dark"],
          },
        };

        export default config;
    """)


def create_frontend_tsconfig() -> str:
    return json.dumps({
        "compilerOptions": {
            "target": "ES2017",
            "lib": ["dom", "dom.iterable", "esnext"],
            "allowJs": True,
            "skipLibCheck": True,
            "strict": True,
            "noEmit": True,
            "esModuleInterop": True,
            "module": "esnext",
            "moduleResolution": "bundler",
            "resolveJsonModule": True,
            "isolatedModules": True,
            "jsx": "preserve",
            "incremental": True,
            "plugins": [{"name": "next"}],
            "paths": {
                "@components/*": ["packages/components/*"],
                "@services/*": ["packages/services/*"],
                "@hooks/*": ["packages/hooks/*"],
                "@interfaces/*": ["packages/interfaces/*"],
                "@props/*": ["packages/props/*"],
                "@/*": ["./*"]
            }
        },
        "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
        "exclude": ["node_modules"]
    }, indent=2)


def create_frontend_layout_tsx() -> str:
    return dedent("""\
        import type { Metadata } from "next";
        import "./globals.css";

        export const metadata: Metadata = {
          title: "Dashboard",
          description: "Application dashboard",
        };

        export default function RootLayout({
          children,
        }: Readonly<{
          children: React.ReactNode;
        }>) {
          return (
            <html lang="en" data-theme="dark">
              <body>{children}</body>
            </html>
          );
        }
    """)


def create_frontend_page_tsx() -> str:
    return dedent("""\
        export default function Home() {
          return (
            <main className="min-h-screen p-8">
              <h1 className="text-4xl font-bold">Dashboard</h1>
              <p className="mt-4 text-gray-500">Welcome to your dashboard.</p>
            </main>
          );
        }
    """)


def create_frontend_globals_css() -> str:
    return dedent("""\
        @import "tailwindcss";
    """)


# Mobile Templates
def create_mobile_package_json(org: str) -> str:
    return json.dumps({
        "name": f"@{org}/mobile",
        "version": "0.0.1",
        "private": True,
        "main": "expo-router/entry",
        "scripts": {
            "start": "expo start",
            "android": "expo start --android",
            "ios": "expo start --ios",
            "web": "expo start --web"
        },
        "dependencies": {
            "expo": "~52.0.0",
            "expo-router": "~4.0.0",
            "expo-status-bar": "~2.0.0",
            "react": "^19.0.0",
            "react-native": "^0.76.0",
            "react-native-safe-area-context": "^5.0.0",
            "react-native-screens": "~4.4.0"
        },
        "devDependencies": {
            "@types/react": "^19.0.0",
            "typescript": "^5.7.0"
        }
    }, indent=2)


def create_mobile_app_json(name: str) -> str:
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
                "bundleIdentifier": f"com.{slug}.app"
            },
            "android": {
                "package": f"com.{slug}.app"
            },
            "experiments": {
                "typedRoutes": True
            }
        }
    }, indent=2)


def create_mobile_tsconfig() -> str:
    return json.dumps({
        "extends": "expo/tsconfig.base",
        "compilerOptions": {
            "strict": True,
            "paths": {
                "@/*": ["./*"]
            }
        },
        "include": ["**/*.ts", "**/*.tsx", ".expo/types/**/*.ts", "expo-env.d.ts"]
    }, indent=2)


def create_mobile_layout_tsx() -> str:
    return dedent("""\
        import { Stack } from "expo-router";
        import { StatusBar } from "expo-status-bar";

        export default function RootLayout() {
          return (
            <>
              <Stack>
                <Stack.Screen name="index" options={{ title: "Home" }} />
              </Stack>
              <StatusBar style="auto" />
            </>
          );
        }
    """)


def create_mobile_index_tsx() -> str:
    return dedent("""\
        import { View, Text, StyleSheet } from "react-native";

        export default function Home() {
          return (
            <View style={styles.container}>
              <Text style={styles.title}>Welcome</Text>
              <Text style={styles.subtitle}>Your mobile app is ready.</Text>
            </View>
          );
        }

        const styles = StyleSheet.create({
          container: {
            flex: 1,
            alignItems: "center",
            justifyContent: "center",
            padding: 20,
          },
          title: {
            fontSize: 32,
            fontWeight: "bold",
          },
          subtitle: {
            fontSize: 16,
            color: "#666",
            marginTop: 8,
          },
        });
    """)


# Packages Templates
def create_packages_package_json(org: str) -> str:
    return json.dumps({
        "name": f"@{org}/packages",
        "version": "0.0.1",
        "private": True,
        "workspaces": [
            "packages/*"
        ]
    }, indent=2)


def create_packages_tsconfig() -> str:
    return json.dumps({
        "compilerOptions": {
            "target": "ES2020",
            "module": "ESNext",
            "moduleResolution": "bundler",
            "declaration": True,
            "strict": True,
            "skipLibCheck": True,
            "esModuleInterop": True
        }
    }, indent=2)


def scaffold_workspace(
    root: Path,
    name: str,
    org: str,
    allow_outside: bool,
) -> None:
    """Create the full workspace structure."""

    cwd = Path.cwd()
    if not allow_outside and not root.is_relative_to(cwd):
        print(f"Error: Target path {root} is outside current directory.")
        print("Use --allow-outside to confirm this is intentional.")
        sys.exit(1)

    if root.exists():
        print(f"Error: {root} already exists.")
        sys.exit(1)

    print(f"Creating workspace at {root}...")

    # Create directories
    dirs = [
        root,
        root / ".agent",
        root / "api" / "apps" / "api" / "src" / "collections",
        root / "api" / "apps" / "api" / "src" / "auth",
        root / "api" / "apps" / "api" / "src" / "config",
        root / "api" / "apps" / "api" / "src" / "guards",
        root / "api" / "apps" / "api" / "src" / "helpers",
        root / "api" / ".agent",
        root / "frontend" / "apps" / "dashboard" / "app",
        root / "frontend" / "packages" / "components",
        root / "frontend" / "packages" / "services",
        root / "frontend" / "packages" / "hooks",
        root / "frontend" / "packages" / "interfaces",
        root / "frontend" / ".agent",
        root / "mobile" / "app",
        root / "mobile" / ".agent",
        root / "packages" / "packages" / "common" / "serializers",
        root / "packages" / "packages" / "common" / "interfaces",
        root / "packages" / "packages" / "common" / "enums",
        root / "packages" / "packages" / "helpers",
        root / "packages" / "packages" / "constants",
        root / "packages" / ".agent",
    ]

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # Root files
    files = {
        root / "package.json": create_root_package_json(name),
        root / ".npmrc": create_npmrc(),
        root / ".gitignore": create_gitignore(),
        root / "README.md": create_readme(name),
        root / "AGENTS.md": create_agents_md(name),
        root / "CLAUDE.md": create_claude_md(name),
        root / "CODEX.md": create_codex_md(name),

        # API
        root / "api" / "package.json": create_api_package_json(org),
        root / "api" / "nest-cli.json": create_nest_cli_json(),
        root / "api" / "tsconfig.json": create_api_tsconfig(),
        root / "api" / "Dockerfile": create_api_dockerfile(),
        root / "api" / "apps" / "api" / "src" / "main.ts": create_api_main_ts(),
        root / "api" / "apps" / "api" / "src" / "app.module.ts": create_api_app_module_ts(),
        root / "api" / "AGENTS.md": create_agents_md(f"{name} API"),
        root / "api" / "CLAUDE.md": create_claude_md(f"{name} API"),
        root / "api" / "CODEX.md": create_codex_md(f"{name} API"),

        # Frontend
        root / "frontend" / "package.json": create_frontend_package_json(org),
        root / "frontend" / "next.config.ts": create_frontend_next_config(),
        root / "frontend" / "tailwind.config.ts": create_frontend_tailwind_config(),
        root / "frontend" / "tsconfig.json": create_frontend_tsconfig(),
        root / "frontend" / "apps" / "dashboard" / "app" / "layout.tsx": create_frontend_layout_tsx(),
        root / "frontend" / "apps" / "dashboard" / "app" / "page.tsx": create_frontend_page_tsx(),
        root / "frontend" / "apps" / "dashboard" / "app" / "globals.css": create_frontend_globals_css(),
        root / "frontend" / "AGENTS.md": create_agents_md(f"{name} Frontend"),
        root / "frontend" / "CLAUDE.md": create_claude_md(f"{name} Frontend"),
        root / "frontend" / "CODEX.md": create_codex_md(f"{name} Frontend"),

        # Mobile
        root / "mobile" / "package.json": create_mobile_package_json(org),
        root / "mobile" / "app.json": create_mobile_app_json(name),
        root / "mobile" / "tsconfig.json": create_mobile_tsconfig(),
        root / "mobile" / "app" / "_layout.tsx": create_mobile_layout_tsx(),
        root / "mobile" / "app" / "index.tsx": create_mobile_index_tsx(),
        root / "mobile" / "AGENTS.md": create_agents_md(f"{name} Mobile"),
        root / "mobile" / "CLAUDE.md": create_claude_md(f"{name} Mobile"),
        root / "mobile" / "CODEX.md": create_codex_md(f"{name} Mobile"),

        # Packages
        root / "packages" / "package.json": create_packages_package_json(org),
        root / "packages" / "tsconfig.json": create_packages_tsconfig(),
        root / "packages" / "AGENTS.md": create_agents_md(f"{name} Packages"),
        root / "packages" / "CLAUDE.md": create_claude_md(f"{name} Packages"),
        root / "packages" / "CODEX.md": create_codex_md(f"{name} Packages"),
    }

    for filepath, content in files.items():
        filepath.write_text(content)
        print(f"Created: {filepath}")

    # Run agent-folder-init for .agent folders
    agent_init_script = Path.home() / ".cursor" / "skills" / "agent-folder-init" / "scripts" / "scaffold.py"
    if agent_init_script.exists():
        for project in [root, root / "api", root / "frontend", root / "mobile", root / "packages"]:
            project_name = project.name if project != root else name
            try:
                subprocess.run([
                    "python3", str(agent_init_script),
                    "--root", str(project),
                    "--name", project_name,
                    "--allow-outside"
                ], check=True, capture_output=True)
                print(f"Initialized .agent/ for {project}")
            except subprocess.CalledProcessError:
                print(f"Warning: Could not initialize .agent/ for {project}")

    print(f"\n✅ Workspace created at: {root}")
    print(f"\nNext steps:")
    print(f"1. cd {root}")
    print(f"2. bun install")
    print(f"3. Start developing!")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold a full-stack monorepo workspace."
    )
    parser.add_argument(
        "--root",
        type=Path,
        required=True,
        help="Directory to create the workspace in",
    )
    parser.add_argument(
        "--name",
        type=str,
        required=True,
        help="Project name",
    )
    parser.add_argument(
        "--org",
        type=str,
        default="myorg",
        help="Organization name for package scoping (default: myorg)",
    )
    parser.add_argument(
        "--allow-outside",
        action="store_true",
        help="Allow creating files outside current directory",
    )

    args = parser.parse_args()

    scaffold_workspace(
        root=args.root.resolve(),
        name=args.name,
        org=args.org,
        allow_outside=args.allow_outside,
    )


if __name__ == "__main__":
    main()
