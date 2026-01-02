---
name: linter-formatter-init
description: Set up ESLint, Prettier, and pre-commit hooks for any JavaScript/TypeScript project. Use when initializing code quality tooling for a new project or adding linting to an existing one. Supports ESLint + Prettier or Biome as alternatives.
---
# Linter Formatter Init

Set up comprehensive linting and formatting for JavaScript/TypeScript projects.

## Purpose

This skill automates the setup of:
- ESLint for code linting
- Prettier for code formatting
- Husky + lint-staged for pre-commit hooks
- VS Code settings (or compatible editor) for auto-format on save
- npm scripts for manual linting and formatting

## When to Use

Use when:
- Starting a new JS/TS project
- Adding linting to an existing project without tooling
- Standardizing code quality across a team
- Setting up pre-commit hooks to enforce quality

## Quick Start

```bash
# Basic setup (ESLint + Prettier)
python3 ~/.codex/skills/linter-formatter-init/scripts/setup.py \
  --root /path/to/project

# With TypeScript support
python3 ~/.codex/skills/linter-formatter-init/scripts/setup.py \
  --root /path/to/project \
  --typescript

# Use Biome instead of ESLint + Prettier
python3 ~/.codex/skills/linter-formatter-init/scripts/setup.py \
  --root /path/to/project \
  --biome

# Skip pre-commit hooks
python3 ~/.codex/skills/linter-formatter-init/scripts/setup.py \
  --root /path/to/project \
  --no-hooks
```

## What Gets Installed

### Dependencies

**ESLint + Prettier (default):**
- eslint
- prettier
- eslint-config-prettier
- eslint-plugin-prettier
- @typescript-eslint/parser (if --typescript)
- @typescript-eslint/eslint-plugin (if --typescript)

**Biome (alternative):**
- @biomejs/biome

**Pre-commit hooks:**
- husky
- lint-staged

### Configuration Files

```
project/
├── .eslintrc.json          # ESLint config
├── .prettierrc             # Prettier config
├── .prettierignore         # Prettier ignore patterns
├── .vscode/
│   └── settings.json       # Auto-format on save
├── .husky/
│   └── pre-commit          # Pre-commit hook
└── package.json            # Updated with scripts + lint-staged
```

### npm Scripts Added

```json
{
  "scripts": {
    "lint": "eslint . --ext .js,.jsx,.ts,.tsx",
    "lint:fix": "eslint . --ext .js,.jsx,.ts,.tsx --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check ."
  }
}
```

## Configuration Options

### ESLint Rules (Default)

The default ESLint config includes:
- Recommended rules for JS/TS
- Prettier integration (no formatting conflicts)
- No console.log in production
- Prefer const over let
- No unused variables (error)
- Consistent return types (TypeScript)

### Prettier Options (Default)

```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100,
  "bracketSpacing": true
}
```

### Customization

After setup, customize:
1. `.eslintrc.json` - Add project-specific rules
2. `.prettierrc` - Adjust formatting preferences
3. `.eslintignore` / `.prettierignore` - Add ignore patterns

## Pre-commit Hooks

When enabled (default), lint-staged runs on every commit:

```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md,yml,yaml}": ["prettier --write"]
  }
}
```

This ensures:
- All committed code passes linting
- All committed code is formatted
- No broken code enters the repo

## VS Code Integration

The skill creates `.vscode/settings.json`:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

## Biome Alternative

Biome is a faster, all-in-one alternative to ESLint + Prettier:

```bash
python3 ~/.codex/skills/linter-formatter-init/scripts/setup.py \
  --root /path/to/project \
  --biome
```

Creates `biome.json` instead of ESLint/Prettier configs:

```json
{
  "$schema": "https://biomejs.dev/schemas/2.3.10/schema.json",
  "assist": {
    "actions": {
      "source": { "organizeImports": "on" }
    }
  },
  "linter": {
    "enabled": true,
    "rules": { "recommended": true }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2
  }
}
```

## Monorepo Support

For monorepos, run from the root:

```bash
python3 ~/.codex/skills/linter-formatter-init/scripts/setup.py \
  --root /path/to/monorepo \
  --typescript \
  --monorepo
```

This adds root-level config that applies to all packages.

## Troubleshooting

### ESLint conflicts with Prettier

The config includes `eslint-config-prettier` which disables all ESLint rules that conflict with Prettier. If you still see conflicts:

```bash
# Check for conflicting rules
npx eslint-config-prettier .eslintrc.json
```

### Pre-commit hooks not running

```bash
# Reinstall husky
npx husky install
chmod +x .husky/pre-commit
```

### Format on save not working

1. Install the Prettier extension in VS Code (or compatible editor)
2. Set Prettier as default formatter
3. Enable "Format on Save" in settings

## Framework-Specific Configs

The skill detects common frameworks and adjusts config:

- **Next.js**: Adds `next/core-web-vitals` to ESLint
- **React**: Adds `eslint-plugin-react` and `eslint-plugin-react-hooks`
- **NestJS**: Adds rules for decorators and DI patterns
- **Node.js**: Adds `eslint-plugin-node` rules

## Manual Setup (Alternative)

If you prefer manual setup over the script:

```bash
# Install dependencies
npm install -D eslint prettier eslint-config-prettier eslint-plugin-prettier husky lint-staged

# TypeScript support
npm install -D @typescript-eslint/parser @typescript-eslint/eslint-plugin

# Initialize ESLint
npx eslint --init

# Initialize Husky
npx husky install
npx husky add .husky/pre-commit "npx lint-staged"
```

Then copy configs from `~/.codex/skills/linter-formatter-init/assets/configs/`