---
name: project-init-orchestrator
description: Orchestrates complete project initialization — scaffolding, agent folders, linting, test coverage, and component setup (NestJS, Next.js, Expo, Plasmo). Use when starting a new project or adding infrastructure to an existing one.
metadata:
  version: "1.0.0"
  tags: project-init, scaffolding, orchestration, setup, monorepo
---

# Project Init Orchestrator

## Overview

This skill orchestrates project initialization by choosing the smallest safe
setup route. For new Shipshit.dev product repos, prefer `npx @shipshitdev/v0`
as the primary scaffolder. Use the lower-level init skills for existing repos,
repairs, or project types not covered by v0.

## Contract

Inputs:

- Target project path and project name
- Project type: new Shipshit.dev product, existing repo, docs-only, library, or custom
- Desired app surfaces, routes, agent platform support, and GitHub setup

Outputs:

- Selected initialization route
- List of delegated skills or v0 command used
- Files/directories created or modified
- Verification status and remaining manual setup

Creates/Modifies:

- New product repos through `npx @shipshitdev/v0`
- Existing repo `.agents/`, `.claude/`, `.codex/`, lint, test, and scaffold files when delegated

External Side Effects:

- May install dependencies when using v0 or delegated setup skills
- May create a GitHub repo or issue only when the v0 command is run with GitHub flags

Confirmation Required:

- Before creating a GitHub repo or issue
- Before running setup outside the current workspace
- Before overwriting existing agent/config files

Delegates To:

- `fullstack-workspace-init` for v0-backed Shipshit.dev product scaffolding
- `agent-folder-init` for existing repos that only need AI project context
- `linter-formatter-init`, `testing-cicd-init`, and `husky-test-coverage` for repo repair
- `scaffold` for small module/component additions inside an existing codebase

## When to Use This Skill

This skill activates automatically when users:

- Start a new project from scratch
- Want full project setup with one command
- Need AI-first development infrastructure + code quality tools
- Say "initialize project", "set up new project", "bootstrap project"
- Want consistent setup across multiple projects

## Skills Orchestrated

| Order | Skill | Purpose | Required |
|-------|-------|---------|----------|
| 1 | `fullstack-workspace-init` / `npx @shipshitdev/v0` | New Shipshit.dev product repo | Conditional |
| 2 | `agent-folder-init` | AI documentation & standards for existing repos | Conditional |
| 3 | `linter-formatter-init` | ESLint/Biome + formatter + pre-commit repair | Conditional |
| 4 | `testing-cicd-init` / `husky-test-coverage` | Test and CI gates | Optional |
| 5 | `scaffold` | Incremental module/component additions | Optional |

## Route Selection

Use this order:

1. New Shipshit.dev product repo: run `npx @shipshitdev/v0`.
2. New non-product repo: scaffold only the requested repo structure, then add agent docs and gates.
3. Existing repo missing AI context: run `agent-folder-init`.
4. Existing repo with weak quality gates: run linter/test/CI skills only.
5. Existing repo needing one feature/module: run `scaffold` after finding 3+ examples.

For v0-backed setup, use interactive mode unless the user provides all inputs:

```bash
npx @shipshitdev/v0 <project-directory>
```

For non-interactive Shipshit.dev product setup:

```bash
npx @shipshitdev/v0 <project-directory> \
  --scope "<product scope>" \
  --agent codex \
  --apps web,app,desktop,mobile,extension,cli \
  --routes overview,new-task,search,inbox,activities \
  --no-github
```

## Orchestration Flow

```
┌─────────────────────────────────────────────────────────────┐
│              PROJECT INIT ORCHESTRATOR                       │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 1: GATHER CONTEXT                                    │
│  • Project name and path                                    │
│  • Tech stack (Next.js, NestJS, Expo, Plasmo)              │
│  • Package manager preference (bun, pnpm, npm)             │
│  • Test coverage threshold (default: 80%)                  │
│  • Additional scaffolding needs                            │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 2: AGENT FOLDER INIT                                 │
│  • Create .agents/ directory structure                       │
│  • Set up SESSIONS/, TASKS/, SYSTEM/ folders               │
│  • Generate coding standards and rules                      │
│  • Copy agent configs (.claude/, .codex/, .cursor/)        │
│  ──────────────────────────────────────────────────────────│
│  Invocation:                                                │
│  python3 scripts/scaffold.py                               │
│          (from agent-folder-init skill)                    │
│          --root /path/to/project                           │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 3: LINTER FORMATTER INIT                             │
│  • Detect project tech stack                                │
│  • Install ESLint + Prettier (or Biome)                    │
│  • Configure framework-specific rules                       │
│  • Set up lint-staged for pre-commit                       │
│  • Create .vscode/settings.json                            │
│  ──────────────────────────────────────────────────────────│
│  Invocation:                                                │
│  Use linter-formatter-init skill guidance                   │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 4: HUSKY TEST COVERAGE (if tests exist)             │
│  • Detect test runner (Jest, Vitest, Mocha)                │
│  • Configure coverage thresholds                            │
│  • Add pre-commit hook for test coverage                   │
│  ──────────────────────────────────────────────────────────│
│  Invocation:                                                │
│  Use husky-test-coverage skill guidance                     │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 5: COMPONENT SCAFFOLD (optional)                     │
│  • Scaffold additional components if requested:            │
│    - Backend (NestJS + MongoDB + Swagger + Dockerfile)     │
│    - Frontend (Next.js + Tailwind + App Router)            │
│    - Mobile (Expo + Expo Router + React Native)            │
│    - Extension (Plasmo + React + Tailwind)                 │
│  • Supports monorepo (workspaces) or separate repos       │
│  ──────────────────────────────────────────────────────────│
│  Invocation:                                                │
│  python3 scripts/scaffold.py                               │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 6: VERIFICATION                                      │
│  • Verify all configurations created                        │
│  • Run lint check (should pass)                            │
│  • Confirm git hooks installed                             │
│  • Generate setup summary                                   │
└─────────────────────────────────────────────────────────────┘
```

## Usage

### Quick Start (Recommended)

When user says "initialize my project" or "set up new project":

```
1. Ask for project context:
   - Project path (default: current directory)
   - New Shipshit.dev product or existing repo repair?
   - Product scope if using v0
   - App surfaces and routes if non-default
   - Agent to hand off to: codex or claude
   - Test coverage threshold (default: 80%)
   - Need additional scaffolding? (backend, frontend, mobile, extension)

2. Execute phases in order:
   v0 route OR existing-repo phases → verification
```

### Manual Orchestration

If you need to run phases individually:

**Phase 2: Agent Folder Init**

```bash
python3 scripts/scaffold.py --root /path/to/project  # from agent-folder-init skill
```

**Phase 3: Linter Formatter**
Follow the `linter-formatter-init` skill to:

- Install dependencies based on detected stack
- Configure ESLint rules
- Set up Prettier
- Configure lint-staged

**Phase 4: Test Coverage**
Follow the `husky-test-coverage` skill to:

- Detect test runner
- Configure coverage thresholds
- Add pre-commit hook

**Phase 5: Component Scaffold (optional)**

```bash
python3 scripts/scaffold.py
```

Supports scaffolding:

- **Backend (NestJS)**: MongoDB, Swagger, soft deletes (`isDeleted`), multi-tenancy (filter by `organization`), Dockerfile
- **Frontend (Next.js)**: Tailwind CSS, TypeScript strict, App Router, path aliases (`@components/`, `@services/`, `@hooks/`)
- **Mobile (Expo)**: Expo Router, TypeScript, platform-specific configs
- **Extension (Plasmo)**: React + TypeScript, Tailwind, manifest config, popup component

Structure options:

- **Monorepo**: All components in one repo with workspace config
- **Separate repos**: Each component in its own directory
- **Existing projects**: Add components incrementally

## Configuration Presets

### Minimal (AI docs + linting)

```
Phases: 2, 3
Output:
├── .agents/
├── .eslintrc.js
├── .prettierrc
├── .husky/pre-commit (lint-staged)
└── .vscode/settings.json
```

### Standard (+ test coverage)

```
Phases: 2, 3, 4
Output:
├── .agents/
├── .eslintrc.js
├── .prettierrc
├── .husky/pre-commit (lint-staged + tests)
├── jest.config.js (coverage thresholds)
└── .vscode/settings.json
```

### Full Stack (+ scaffolding)

```
Phases: 2, 3, 4, 5
Output:
├── .agents/
├── apps/
│   ├── web/          (Next.js)
│   ├── api/          (NestJS)
│   ├── mobile/       (Expo)
│   └── extension/    (Plasmo)
├── packages/
│   └── shared/
├── .eslintrc.js
├── .prettierrc
├── .husky/pre-commit
└── .vscode/settings.json
```

## Generated Structure

After full orchestration, your project will have:

```
project-root/
├── .agents/                          # AI-first documentation
│   ├── SESSIONS/                    # Daily session logs
│   ├── TASKS/                       # Task tracking
│   │   └── INBOX.md
│   ├── SYSTEM/                      # Architecture docs
│   │   ├── ARCHITECTURE.md
│   │   └── RULES.md
│   └── README.md
│
├── .claude/                         # Claude Code configs
│   ├── commands/
│   ├── rules/
│   └── skills/
│
├── .husky/                          # Git hooks
│   └── pre-commit                   # Runs lint-staged + tests
│
├── .vscode/                         # Editor settings
│   └── settings.json                # Format on save
│
├── .eslintrc.js                     # ESLint configuration
├── .prettierrc                      # Prettier configuration
├── .lintstagedrc                    # Lint-staged configuration
│
└── [app directories if scaffolded]
```

## Best Practices

### Sequencing

- Always run agent-folder-init FIRST (establishes standards)
- Run linter-formatter-init BEFORE husky-test-coverage (both use Husky)
- Run component scaffolding LAST (depends on base setup)

### Customization

- Each phase can be skipped if already configured
- Phases are idempotent (safe to re-run)
- Configuration can be customized after orchestration

### Verification Checklist

After orchestration, verify:

- [ ] `.agents/` folder exists with proper structure
- [ ] `npm run lint` or `bun lint` works
- [ ] `npm run format` or `bun format` works
- [ ] Git commit triggers pre-commit hooks
- [ ] Tests run on commit (if Phase 4 enabled)

## Example Interaction

**User:** "Set up my new project at ~/projects/my-saas"

**Orchestrator Response:**

```
I'll initialize your project with full AI-first infrastructure.

Let me gather some context:
1. Tech stack: [Next.js / NestJS / Node.js / Other]
2. Package manager: [bun / pnpm / npm]
3. Test coverage threshold: [80% default]
4. Need scaffolding? [backend / frontend / mobile / extension]

[After user responds]

Starting orchestration...

✓ Phase 2: Agent Folder Init
  - Created .agents/ with 13 files
  - Copied agent configs (.claude/, .codex/, .cursor/)

✓ Phase 3: Linter Formatter Init
  - Detected: Next.js + TypeScript
  - Installed: eslint, prettier, lint-staged
  - Created: .eslintrc.js, .prettierrc, .lintstagedrc

✓ Phase 4: Husky Test Coverage
  - Detected: Jest
  - Set threshold: 80%
  - Added pre-commit hook

✓ Phase 6: Verification
  - All configs created ✓
  - Lint check passed ✓
  - Git hooks installed ✓

Project initialized successfully!
```

## Troubleshooting

### Phase fails to complete

- Check if dependencies are installed (`node`, `python3`)
- Verify write permissions to project directory
- Check if conflicting configs exist

### Linting errors after setup

- Run `npm run lint:fix` to auto-fix
- Check `.eslintrc.js` matches your stack
- Verify TypeScript config if using TS

### Pre-commit hook not running

- Run `npx husky install` manually
- Check `.husky/pre-commit` exists and is executable
- Verify `prepare` script in package.json
