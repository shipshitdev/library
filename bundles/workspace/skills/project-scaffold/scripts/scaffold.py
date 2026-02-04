#!/usr/bin/env python3
"""
Unified project scaffolder - scaffold .agent folders, backend, frontend, mobile, and extensions.
Works for both new projects and adding components to existing projects.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from textwrap import dedent


SKILL_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = SKILL_DIR / "assets" / "templates"


def ask_question(prompt: str, default: str | None = None, choices: list[str] | None = None) -> str:
    """Ask an interactive question."""
    if choices:
        prompt += f" ({'/'.join(choices)})"
    if default:
        prompt += f" [{default}]"
    prompt += ": "
    
    while True:
        answer = input(prompt).strip()
        if not answer and default:
            return default
        if not answer:
            print("Please provide an answer.")
            continue
        if choices and answer not in choices:
            print(f"Please choose one of: {', '.join(choices)}")
            continue
        return answer


def ask_yes_no(prompt: str, default: bool = False) -> bool:
    """Ask a yes/no question."""
    default_str = "Y/n" if default else "y/N"
    answer = input(f"{prompt} ({default_str}): ").strip().lower()
    if not answer:
        return default
    return answer in ("y", "yes")


def is_git_initialized(root: Path) -> bool:
    """Check if git is already initialized in the project."""
    return (root / ".git").exists()


def init_git_repository(root: Path) -> None:
    """Initialize git repository if not already initialized."""
    if is_git_initialized(root):
        print("ℹ️  Git repository already initialized. Skipping.")
        return
    
    try:
        # Check if git is available
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        
        # Initialize git
        subprocess.run(["git", "init"], cwd=root, check=True)
        print("✅ Initialized git repository")
    except subprocess.CalledProcessError:
        print("⚠️  Warning: Could not initialize git repository (git may not be installed)")
    except FileNotFoundError:
        print("⚠️  Warning: Git not found. Skipping git initialization.")


def scaffold_agent_folder(root: Path, project_name: str, tech_stack: str = "", allow_outside: bool = False) -> None:
    """Scaffold .agent folder structure."""
    agent_init_script = Path.home() / ".codex" / "skills" / "agent-folder-init" / "scripts" / "scaffold.py"
    if not agent_init_script.exists():
        agent_init_script = Path.home() / ".claude" / "skills" / "agent-folder-init" / "scripts" / "scaffold.py"
    if not agent_init_script.exists():
        agent_init_script = Path.home() / ".cursor" / "skills" / "agent-folder-init" / "scripts" / "scaffold.py"
    
    if agent_init_script.exists():
        try:
            subprocess.run([
                "python3", str(agent_init_script),
                "--root", str(root),
                "--name", project_name,
                "--tech", tech_stack,
                "--allow-outside" if allow_outside else ""
            ], check=True, capture_output=True)
            print(f"✅ Initialized .agents/ for {root}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Warning: Could not initialize .agents/ for {root}: {e}")
    else:
        print(f"⚠️  Warning: agent-folder-init script not found. Skipping .agents/ initialization.")


def create_api_structure(root: Path, name: str, org: str, is_monorepo: bool) -> None:
    """Create NestJS backend structure."""
    api_root = root / "api" if is_monorepo else root
    
    
    dirs = [
        api_root / "apps" / "api" / "src" / "collections",
        api_root / "apps" / "api" / "src" / "auth",
        api_root / "apps" / "api" / "src" / "config",
        api_root / "apps" / "api" / "src" / "guards",
        api_root / "apps" / "api" / "src" / "helpers",
    ]
    
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    
    # Package.json
    package_json = {
        "name": f"@{org}/api" if is_monorepo else name.lower().replace(" ", "-"),
        "version": "0.0.1",
        "private": True,
        "scripts": {
            "build": "nest build",
            "start": "nest start",
            "start:dev": "nest start --watch",
            "start:debug": "nest start --debug --watch",
            "start:prod": "node dist/main",
            "lint": "biome check .",
            "lint:fix": "biome check --write .",
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
            "typescript": "^5.7.0",
            "@biomejs/biome": "^1.9.0"
        }
    }
    
    (api_root / "package.json").write_text(json.dumps(package_json, indent=2))
    
    # biome.json
    biome_config = {
        "$schema": "https://biomejs.dev/schemas/1.9.0/schema.json",
        "vcs": {
            "enabled": True,
            "clientKind": "git",
            "useIgnoreFile": True
        },
        "files": {
            "ignoreUnknown": False,
            "ignore": ["node_modules", "dist", ".next", "build"]
        },
        "formatter": {
            "enabled": True,
            "indentStyle": "space",
            "indentWidth": 2,
            "lineWidth": 100
        },
        "organizeImports": {
            "enabled": True
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
    }
    (api_root / "biome.json").write_text(json.dumps(biome_config, indent=2))
    
    # nest-cli.json
    nest_cli = {
        "$schema": "https://json.schemastore.org/nest-cli",
        "collection": "@nestjs/schematics",
        "sourceRoot": "apps/api/src",
        "monorepo": is_monorepo,
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
    }
    (api_root / "nest-cli.json").write_text(json.dumps(nest_cli, indent=2))
    
    # tsconfig.json
    tsconfig = {
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
    }
    (api_root / "tsconfig.json").write_text(json.dumps(tsconfig, indent=2))
    
    # main.ts
    main_ts = dedent("""\
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
    (api_root / "apps" / "api" / "src" / "main.ts").write_text(main_ts)
    
    # app.module.ts
    app_module = dedent("""\
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
    (api_root / "apps" / "api" / "src" / "app.module.ts").write_text(app_module)
    
    # Dockerfile
    dockerfile = dedent("""\
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
    (api_root / "Dockerfile").write_text(dockerfile)
    
    # Entry files
    agents_md = dedent(f"""\
        # {name} API

        AI agent entry point. Documentation in `.agents/`.
    """)
    (api_root / "AGENTS.md").write_text(agents_md)
    (api_root / "CLAUDE.md").write_text(agents_md)
    (api_root / "CODEX.md").write_text(agents_md)
    
    print(f"✅ Created backend structure at {api_root}")


def create_frontend_structure(root: Path, name: str, org: str, is_monorepo: bool) -> None:
    """Create NextJS frontend structure."""
    frontend_root = root / "frontend" if is_monorepo else root
    
    dirs = [
        frontend_root / "apps" / "dashboard" / "app",
        frontend_root / "packages" / "components",
        frontend_root / "packages" / "services",
        frontend_root / "packages" / "hooks",
        frontend_root / "packages" / "interfaces",
    ]
    
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    
    # Package.json
    package_json = {
        "name": f"@{org}/frontend" if is_monorepo else name.lower().replace(" ", "-"),
        "version": "0.0.1",
        "private": True,
        "scripts": {
            "dev": "next dev --turbo",
            "build": "next build",
            "start": "next start",
            "lint": "biome check .",
            "lint:fix": "biome check --write ."
        },
        "dependencies": {
            "next": "^15.0.0",
            "react": "^19.0.0",
            "react-dom": "^19.0.0",
            "axios": "^1.7.0",
            "zustand": "^5.0.0",
            "react-hook-form": "^7.50.0",
            "zod": "^3.23.0",
            "@hookform/resolvers": "^3.9.0",
            "@agenticindiedev/ui": "latest"
        },
        "devDependencies": {
            "@types/node": "^22.0.0",
            "@types/react": "^19.0.0",
            "@types/react-dom": "^19.0.0",
            "typescript": "^5.7.0",
            "tailwindcss": "^4.0.0",
            "@tailwindcss/postcss": "^4.0.0",
            "@biomejs/biome": "^1.9.0",
            "sass": "^1.83.0"
        }
    }
    (frontend_root / "package.json").write_text(json.dumps(package_json, indent=2))
    
    # next.config.ts
    next_config = dedent("""\
        import type { NextConfig } from "next";
        import path from "path";

        const nextConfig: NextConfig = {
          reactStrictMode: true,
          transpilePackages: ["@agenticindiedev/ui"],
          sassOptions: {
            includePaths: [path.join(__dirname, "node_modules")],
          },
          // Empty turbopack config to acknowledge we have webpack config but want Turbopack
          turbopack: {},
          webpack: (config) => {
            // Configure sass-loader to resolve @agenticindiedev/ui package imports
            const rules = config.module.rules;
            const scssRule = rules.find(
              (rule: unknown) =>
                rule &&
                typeof rule === "object" &&
                rule !== null &&
                "test" in rule &&
                rule.test &&
                typeof rule.test === "object" &&
                "toString" in rule.test &&
                rule.test.toString().includes("scss"),
            );

            if (
              scssRule &&
              typeof scssRule === "object" &&
              scssRule !== null &&
              "oneOf" in scssRule &&
              Array.isArray(scssRule.oneOf)
            ) {
              scssRule.oneOf.forEach((oneOf: unknown) => {
                if (
                  oneOf &&
                  typeof oneOf === "object" &&
                  oneOf !== null &&
                  "use" in oneOf &&
                  Array.isArray(oneOf.use)
                ) {
                  oneOf.use.forEach((loader: unknown) => {
                    if (
                      loader &&
                      typeof loader === "object" &&
                      loader !== null &&
                      "loader" in loader &&
                      typeof loader.loader === "string" &&
                      loader.loader.includes("sass-loader")
                    ) {
                      const loaderWithOptions = loader as {
                        options?: {
                          api?: string;
                          sassOptions?: Record<string, unknown>;
                        };
                      };
                      loaderWithOptions.options = {
                        ...loaderWithOptions.options,
                        api: "modern-compiler",
                        sassOptions: {
                          ...loaderWithOptions.options?.sassOptions,
                          includePaths: [path.join(__dirname, "node_modules")],
                        },
                      };
                    }
                  });
                }
              });
            }

            return config;
          },
        };

        export default nextConfig;
    """)
    (frontend_root / "next.config.ts").write_text(next_config)
    
    # tailwind.config.ts
    tailwind_config = dedent("""\
        import type { Config } from "tailwindcss";

        const config: Config = {
          content: [
            "./apps/**/*.{js,ts,jsx,tsx,mdx}",
            "./packages/**/*.{js,ts,jsx,tsx,mdx}",
            "./node_modules/@agenticindiedev/ui/**/*.{js,ts,jsx,tsx}",
          ],
          theme: {
            extend: {},
          },
          plugins: [],
        };

        export default config;
    """)
    (frontend_root / "tailwind.config.ts").write_text(tailwind_config)
    
    # tsconfig.json
    tsconfig = {
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
    }
    (frontend_root / "tsconfig.json").write_text(json.dumps(tsconfig, indent=2))
    
    # layout.tsx
    layout_tsx = dedent("""\
        import type { Metadata } from "next";
        import "./globals.scss";

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
    (frontend_root / "apps" / "dashboard" / "app" / "layout.tsx").write_text(layout_tsx)
    
    # page.tsx
    page_tsx = dedent("""\
        export default function Home() {
          return (
            <main className="min-h-screen p-8">
              <h1 className="text-4xl font-bold">Dashboard</h1>
              <p className="mt-4 text-gray-500">Welcome to your dashboard.</p>
            </main>
          );
        }
    """)
    (frontend_root / "apps" / "dashboard" / "app" / "page.tsx").write_text(page_tsx)
    
    # biome.json
    biome_config = {
        "$schema": "https://biomejs.dev/schemas/1.9.0/schema.json",
        "vcs": {
            "enabled": True,
            "clientKind": "git",
            "useIgnoreFile": True
        },
        "files": {
            "ignoreUnknown": False,
            "ignore": ["node_modules", "dist", ".next", "build"]
        },
        "formatter": {
            "enabled": True,
            "indentStyle": "space",
            "indentWidth": 2,
            "lineWidth": 100
        },
        "organizeImports": {
            "enabled": True
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
    }
    (frontend_root / "biome.json").write_text(json.dumps(biome_config, indent=2))
    
    # postcss.config.mjs
    postcss_config = dedent("""\
        const config = {
          plugins: {
            "@tailwindcss/postcss": {},
          },
        };

        export default config;
    """)
    (frontend_root / "postcss.config.mjs").write_text(postcss_config)

    # globals.scss
    globals_scss = dedent("""\
        @use "tailwindcss";
        @use "@agenticindiedev/ui/themes/dark";

        @source "../../node_modules/@agenticindiedev/ui/dist/**/*.{js,cjs}";
    """)
    (frontend_root / "apps" / "dashboard" / "app" / "globals.scss").write_text(globals_scss)
    
    # Entry files
    agents_md = dedent(f"""\
        # {name} Frontend

        AI agent entry point. Documentation in `.agents/`.
    """)
    (frontend_root / "AGENTS.md").write_text(agents_md)
    (frontend_root / "CLAUDE.md").write_text(agents_md)
    (frontend_root / "CODEX.md").write_text(agents_md)
    
    print(f"✅ Created frontend structure at {frontend_root}")


def create_mobile_structure(root: Path, name: str, org: str, is_monorepo: bool) -> None:
    """Create Expo mobile structure."""
    mobile_root = root / "mobile" if is_monorepo else root
    
    (mobile_root / "app").mkdir(parents=True, exist_ok=True)
    
    slug = name.lower().replace(" ", "-")
    
    # package.json
    package_json = {
        "name": f"@{org}/mobile" if is_monorepo else slug,
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
    }
    (mobile_root / "package.json").write_text(json.dumps(package_json, indent=2))
    
    # app.json
    app_json = {
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
    }
    (mobile_root / "app.json").write_text(json.dumps(app_json, indent=2))
    
    # tsconfig.json
    tsconfig = {
        "extends": "expo/tsconfig.base",
        "compilerOptions": {
            "strict": True,
            "paths": {
                "@/*": ["./*"]
            }
        },
        "include": ["**/*.ts", "**/*.tsx", ".expo/types/**/*.ts", "expo-env.d.ts"]
    }
    (mobile_root / "tsconfig.json").write_text(json.dumps(tsconfig, indent=2))
    
    # _layout.tsx
    layout_tsx = dedent("""\
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
    (mobile_root / "app" / "_layout.tsx").write_text(layout_tsx)
    
    # index.tsx
    index_tsx = dedent("""\
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
    (mobile_root / "app" / "index.tsx").write_text(index_tsx)
    
    # Entry files
    agents_md = dedent(f"""\
        # {name} Mobile

        AI agent entry point. Documentation in `.agents/`.
    """)
    (mobile_root / "AGENTS.md").write_text(agents_md)
    (mobile_root / "CLAUDE.md").write_text(agents_md)
    (mobile_root / "CODEX.md").write_text(agents_md)
    
    print(f"✅ Created mobile structure at {mobile_root}")


def create_extension_structure(root: Path, name: str, org: str, is_monorepo: bool) -> None:
    """Create Plasmo browser extension structure."""
    extension_root = root / "extension" if is_monorepo else root
    
    (extension_root / "src").mkdir(parents=True, exist_ok=True)
    
    slug = name.lower().replace(" ", "-")
    
    # package.json
    package_json = {
        "name": f"@{org}/extension" if is_monorepo else f"{slug}-extension",
        "version": "0.0.1",
        "private": True,
        "scripts": {
            "dev": "plasmo dev",
            "build": "plasmo build",
            "package": "plasmo package"
        },
        "dependencies": {
            "plasmo": "0.90.5",
            "react": "^19.0.0",
            "react-dom": "^19.0.0",
            "@agenticindiedev/ui": "latest"
        },
        "devDependencies": {
            "@types/chrome": "0.1.32",
            "@types/node": "^22.0.0",
            "@types/react": "^19.0.0",
            "@types/react-dom": "^19.0.0",
            "typescript": "^5.7.0",
            "tailwindcss": "^3.4.18",
            "@tailwindcss/postcss": "^4.0.0"
        },
        "manifest": {
            "host_permissions": [],
            "permissions": [
                "storage",
                "tabs",
                "scripting",
                "activeTab"
            ]
        }
    }
    (extension_root / "package.json").write_text(json.dumps(package_json, indent=2))
    
    # tsconfig.json
    tsconfig = {
        "extends": "plasmo/templates/tsconfig.base",
        "exclude": ["node_modules"],
        "include": [".plasmo/index.d.ts", "./**/*.ts", "./**/*.tsx"],
        "compilerOptions": {
            "paths": {
                "~*": ["./src/*"]
            },
            "baseUrl": "."
        }
    }
    (extension_root / "tsconfig.json").write_text(json.dumps(tsconfig, indent=2))
    
    # tailwind.config.ts
    tailwind_config = dedent("""\
        import type { Config } from "tailwindcss";

        const config: Config = {
          content: [
            "./src/**/*.{js,ts,jsx,tsx}",
            "./node_modules/@agenticindiedev/ui/**/*.{js,ts,jsx,tsx}",
          ],
          theme: {
            extend: {},
          },
          plugins: [],
        };

        export default config;
    """)
    (extension_root / "tailwind.config.ts").write_text(tailwind_config)
    
    # postcss.config.js
    postcss_config = dedent("""\
        module.exports = {
          plugins: {
            "@tailwindcss/postcss": {},
          },
        };
    """)
    (extension_root / "postcss.config.js").write_text(postcss_config)
    
    # popup.tsx
    popup_tsx = dedent("""\
        import { useState } from "react";

        export default function Popup() {
          const [count, setCount] = useState(0);

          return (
            <div className="w-64 p-4">
              <h1 className="text-2xl font-bold mb-4">Extension</h1>
              <button
                onClick={() => setCount(count + 1)}
                className="btn btn-primary"
              >
                Count: {count}
              </button>
            </div>
          );
        }
    """)
    (extension_root / "src" / "popup.tsx").write_text(popup_tsx)
    
    # Entry files
    agents_md = dedent(f"""\
        # {name} Extension

        AI agent entry point. Documentation in `.agents/`.
    """)
    (extension_root / "AGENTS.md").write_text(agents_md)
    (extension_root / "CLAUDE.md").write_text(agents_md)
    (extension_root / "CODEX.md").write_text(agents_md)
    
    print(f"✅ Created extension structure at {extension_root}")


def create_monorepo_root(root: Path, name: str, components: dict) -> None:
    """Create monorepo root files."""
    workspaces = []
    if components.get("backend"):
        workspaces.append("api")
    if components.get("frontend"):
        workspaces.append("frontend")
    if components.get("mobile"):
        workspaces.append("mobile")
    if components.get("extension"):
        workspaces.append("extension")
    
    # package.json
    package_json = {
        "name": name.lower().replace(" ", "-"),
        "version": "0.0.1",
        "private": True,
        "workspaces": workspaces,
        "scripts": {
            "dev:api": "cd api && bun run start:dev" if components.get("backend") else None,
            "dev:frontend": "cd frontend && bun run dev" if components.get("frontend") else None,
            "dev:mobile": "cd mobile && bun run start" if components.get("mobile") else None,
            "dev:extension": "cd extension && bun run dev" if components.get("extension") else None,
        }
    }
    # Remove None values
    package_json["scripts"] = {k: v for k, v in package_json["scripts"].items() if v is not None}
    (root / "package.json").write_text(json.dumps(package_json, indent=2))
    
    # .npmrc
    (root / ".npmrc").write_text("engine-strict=true\n")
    
    # .gitignore
    gitignore = dedent("""\
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
        .plasmo
    """)
    (root / ".gitignore").write_text(gitignore)
    
    # README.md
    readme = dedent(f"""\
        # {name}

        Full-stack monorepo workspace.

        ## Structure

        {f"- `api/` - NestJS backend" if components.get("backend") else ""}
        {f"- `frontend/` - NextJS apps" if components.get("frontend") else ""}
        {f"- `mobile/` - React Native + Expo" if components.get("mobile") else ""}
        {f"- `extension/` - Plasmo browser extension" if components.get("extension") else ""}

        ## Getting Started

        ```bash
        bun install
        ```

        ## Development

        ```bash
        {"# Backend\n        cd api && bun run start:dev" if components.get("backend") else ""}
        {"# Frontend\n        cd frontend && bun run dev" if components.get("frontend") else ""}
        {"# Mobile\n        cd mobile && bun run start" if components.get("mobile") else ""}
        {"# Extension\n        cd extension && bun run dev" if components.get("extension") else ""}
        ```

        ## Documentation

        See `.agents/README.md` for AI documentation.
    """)
    (root / "README.md").write_text(readme)
    
    # Entry files
    agents_md = dedent(f"""\
        # {name}

        AI agent entry point. Documentation in `.agents/`.
    """)
    (root / "AGENTS.md").write_text(agents_md)
    (root / "CLAUDE.md").write_text(agents_md)
    (root / "CODEX.md").write_text(agents_md)


def interactive_scaffold() -> None:
    """Interactive scaffolding flow."""
    print("🚀 Unified Project Scaffolder\n")
    
    # Project name
    project_name = ask_question("Project name")
    
    # Project root
    default_root = Path.cwd()
    root_input = ask_question(f"Project root path", str(default_root))
    root = Path(root_input).expanduser().resolve()
    
    # Check if exists
    is_existing = root.exists() and any(root.iterdir())
    if is_existing:
        print(f"⚠️  Directory {root} already exists. Will add components to existing project.")
        if not ask_yes_no("Continue?", True):
            print("Cancelled.")
            return
    
    # Repository structure
    if not is_existing:
        repo_structure = ask_question("Repository structure", "monorepo", ["monorepo", "separate"])
        is_monorepo = repo_structure == "monorepo"
    else:
        # Detect if it's a monorepo
        has_workspace = (root / "package.json").exists()
        if has_workspace:
            try:
                pkg = json.loads((root / "package.json").read_text())
                is_monorepo = "workspaces" in pkg
            except:
                is_monorepo = False
        else:
            is_monorepo = False
        print(f"Detected structure: {'monorepo' if is_monorepo else 'separate repos'}")
    
    # Components to scaffold
    components = {}
    print("\nSelect components to scaffold:")
    components["agent"] = ask_yes_no("  .agent folder?", True)
    components["backend"] = ask_yes_no("  Backend (NestJS)?", False)
    components["frontend"] = ask_yes_no("  Frontend (NextJS)?", False)
    components["mobile"] = ask_yes_no("  Mobile (Expo)?", False)
    components["extension"] = ask_yes_no("  Extension (Plasmo)?", False)
    
    if not any(components.values()):
        print("No components selected. Exiting.")
        return
    
    # Organization name (for monorepo packages)
    org = "myorg"
    if is_monorepo:
        org = ask_question("Organization name for packages", "myorg")
    
    # Tech stack
    tech_stack = []
    if components["backend"]:
        tech_stack.append("nestjs")
    if components["frontend"]:
        tech_stack.append("nextjs")
    if components["mobile"]:
        tech_stack.append("expo")
    if components["extension"]:
        tech_stack.append("plasmo")
    tech_stack_str = ",".join(tech_stack)
    
    # Create root if needed
    root.mkdir(parents=True, exist_ok=True)
    
    # Scaffold components
    print(f"\n📦 Scaffolding components...\n")
    
    if components["agent"]:
        scaffold_agent_folder(root, project_name, tech_stack_str, allow_outside=True)
    
    if components["backend"]:
        create_api_structure(root, project_name, org, is_monorepo)
        if components["agent"]:
            scaffold_agent_folder(
                root / "api" if is_monorepo else root,
                f"{project_name} API",
                "nestjs",
                allow_outside=True
            )
    
    if components["frontend"]:
        create_frontend_structure(root, project_name, org, is_monorepo)
        if components["agent"]:
            scaffold_agent_folder(
                root / "frontend" if is_monorepo else root,
                f"{project_name} Frontend",
                "nextjs",
                allow_outside=True
            )
    
    if components["mobile"]:
        create_mobile_structure(root, project_name, org, is_monorepo)
        if components["agent"]:
            scaffold_agent_folder(
                root / "mobile" if is_monorepo else root,
                f"{project_name} Mobile",
                "expo",
                allow_outside=True
            )
    
    if components["extension"]:
        create_extension_structure(root, project_name, org, is_monorepo)
        if components["agent"]:
            scaffold_agent_folder(
                root / "extension" if is_monorepo else root,
                f"{project_name} Extension",
                "plasmo",
                allow_outside=True
            )
    
    # Create monorepo root files
    if is_monorepo and not is_existing:
        create_monorepo_root(root, project_name, components)
    
    # Initialize git repository if not already initialized
    init_git_repository(root)
    
    print(f"\n✅ Scaffolding complete!")
    print(f"\nNext steps:")
    print(f"1. cd {root}")
    if is_monorepo:
        print(f"2. bun install")
    else:
        for comp, enabled in components.items():
            if enabled and comp != "agent":
                print(f"2. cd {comp if comp in ['backend', 'frontend', 'mobile', 'extension'] else '.'} && bun install")
    print(f"3. Start developing!")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Unified project scaffolder - scaffold .agent folders, backend, frontend, mobile, and extensions."
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        default=True,
        help="Run in interactive mode (default)",
    )
    parser.add_argument(
        "--root",
        type=Path,
        help="Project root directory",
    )
    parser.add_argument(
        "--name",
        type=str,
        help="Project name",
    )
    parser.add_argument(
        "--monorepo",
        action="store_true",
        help="Create as monorepo",
    )
    parser.add_argument(
        "--agent",
        action="store_true",
        help="Scaffold .agent folder",
    )
    parser.add_argument(
        "--backend",
        action="store_true",
        help="Scaffold backend (NestJS)",
    )
    parser.add_argument(
        "--frontend",
        action="store_true",
        help="Scaffold frontend (NextJS)",
    )
    parser.add_argument(
        "--mobile",
        action="store_true",
        help="Scaffold mobile (Expo)",
    )
    parser.add_argument(
        "--extension",
        action="store_true",
        help="Scaffold extension (Plasmo)",
    )
    parser.add_argument(
        "--org",
        type=str,
        default="myorg",
        help="Organization name for packages (default: myorg)",
    )
    
    args = parser.parse_args()
    
    # If no flags provided, run interactive mode
    if args.interactive or not any([args.root, args.name, args.backend, args.frontend, args.mobile, args.extension]):
        interactive_scaffold()
    else:
        # Non-interactive mode (for future use)
        print("Non-interactive mode not yet implemented. Use --interactive or run without flags.")
        sys.exit(1)


if __name__ == "__main__":
    main()
