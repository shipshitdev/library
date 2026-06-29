---
name: agent-folder-init
description: Add or repair .agents/ project context for an existing repo. Use for AI agent documentation, session tracking, task management, and coding standards; do not use as the primary new-product scaffold.
metadata:
  version: "1.0.0"
  tags: "agents, setup, documentation"
---

# Agent Folder Init

## Contract

Inputs:

- Existing project root
- Project name and primary tech stack
- Agent platforms to support: Claude Code, Codex, Cursor, or all

Outputs:

- `.agents/` documentation structure
- Root agent entry files such as `AGENTS.md`, `CLAUDE.md`, and `CODEX.md`
- Summary of files created and files skipped because they already existed

Creates/Modifies:

- `.agents/`, `.claude/`, `.codex/`, `.cursor/`, and root agent entry files
- Does not create application source code

External Side Effects:

- None beyond local file writes

Confirmation Required:

- Before overwriting existing agent docs or config files
- Before writing outside the current workspace

Delegates To:

- `project-init-orchestrator` when starting a new product repo
- `fullstack-workspace-init` / `npx @shipshitdev/v0` when a new Shipshit.dev product should be scaffolded
- `agent-config-audit` after generation to detect drift or stale config

## Purpose

This skill scaffolds a lean AI agent documentation system including:

- Session tracking (daily files in `.agents/sessions/`)
- Durable project context in `.agents/memory/` (one topic per file)
- Agent config folders (.claude, .codex, .cursor) with commands, rules, and agents

## When to Use

- Adding AI coding-assistant context to an existing project
- Setting up AI-first development workflows
- Migrating an existing project to use structured AI documentation

For new Shipshit.dev product repos, prefer `project-init-orchestrator`, which
routes to `npx @shipshitdev/v0` and includes the standard `.agents`, `.claude`,
and `.codex` setup.

## Usage

Run the scaffold script:

```bash
python3 scripts/scaffold.py --help

# Basic usage
python3 scripts/scaffold.py \
  --root /path/to/project \
  --name "My Project"

# With custom options
python3 scripts/scaffold.py \
  --root /path/to/project \
  --name "My Project" \
  --tech "nextjs,nestjs" \
  --allow-outside
```

## Generated Structure

### Documentation (.agents/)

```
.agents/
├── README.md                    # Navigation hub
├── memory/
│   └── README.md                # Source of truth for durable project facts
└── sessions/
    ├── README.md                # Session format guide
    └── TEMPLATE.md              # Session file template
```

**Rules and coding standards** go in the repo's agent entry file (`AGENTS.md`, `CLAUDE.md`, or `CODEX.md`) and the user's platform-level instruction file — not inside `.agents/`.

**Task tracking** uses GitHub Issues (`gh issue list`, `gh issue create`) — not local task files.

### Agent Configs

```
.claude/
├── commands/                    # Slash commands (project-specific)
│   ├── start.md
│   ├── end.md
│   ├── new-session.md
│   ├── commit-summary.md
│   ├── code-review.md
│   ├── bug.md
│   ├── quick-fix.md
│   ├── refactor-code.md
│   ├── inbox.md
│   ├── task.md
│   ├── validate.md
│   └── clean.md
├── agents/                      # Specialized agents (project-specific)
│   ├── senior-backend-engineer.md
│   └── senior-frontend-engineer.md
└── skills/                      # Project-specific skills

.codex/
├── commands/
└── skills/

.cursor/
└── commands/
```

**Note:** Agent configs (`agents/`, `commands/`) are copied from the installed library bundle so projects get the latest version. Rules are not copied because they are expected to be managed at the user or repo level to avoid duplication and drift.

### Root Files

- `AGENTS.md` - Points to `.agents/README.md`
- `CLAUDE.md` - Claude-specific entry point
- `CODEX.md` - Codex-specific entry point
- `.editorconfig` - Editor configuration

## Key Patterns

### memory/ Files

- One topic per file: `memory/architecture.md`, `memory/deployment.md`, `memory/entities.md`, etc.
- Every file carries a `last_verified: YYYY-MM-DD` front-matter field.
- Transient or short-lived facts add `status: temporary`.

### Session Files

- **One file per day**: `sessions/YYYY-MM-DD.md`
- Multiple sessions same day use Session 1, Session 2, etc. in the same file.

## Customization

After scaffolding, customize:

1. Root agent entry file - Add project-specific coding standards and "never do" rules
2. `.agents/memory/architecture.md` - Document your architecture decisions
3. `.agents/memory/entities.md` - Document your data entities
4. `.agents/memory/deployment.md` - Document deployment steps and gotchas
5. GitHub Issues - Create issues for tasks (`gh issue create`)
6. `.claude/rules/` - Add project-specific rule files
7. `.claude/commands/` - Add project-specific slash commands

## Integration with Other Skills

This skill integrates with:

| Skill | How It Works Together |
|-------|----------------------|
| `project-init-orchestrator` | Routes new product requests to v0 before lower-level setup |
| `fullstack-workspace-init` | Uses v0 for new Shipshit.dev product workspaces |
| `linter-formatter-init` | Sets up quality tooling in the scaffolded project |
| `husky-test-coverage` | Enforces test coverage in pre-commit hooks |
