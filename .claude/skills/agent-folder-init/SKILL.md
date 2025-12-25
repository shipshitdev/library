---
name: agent-folder-init
description: Initialize a comprehensive .agent/ folder structure for AI-first development. Use this skill when starting a new project that needs AI agent documentation, session tracking, task management, and coding standards. Generates full structure based on proven patterns from production projects.
---

# Agent Folder Init

Create a comprehensive `.agent/` folder structure for AI-first development workflows.

## Purpose

This skill scaffolds a complete AI agent documentation system including:
- Session tracking (daily files)
- Task management
- Coding standards and rules
- Architecture decision records
- Security checklists
- SOPs for common workflows
- Agent config folders (.claude, .codex, .cursor) with commands, rules, and agents

## When to Use

Use this skill when:
- Starting a new project that will use AI coding assistants
- Setting up AI-first development workflows
- Migrating an existing project to use structured AI documentation

## Usage

Run the scaffold script:

```bash
python3 ~/.claude/skills/agent-folder-init/scripts/scaffold.py --help

# Basic usage
python3 ~/.claude/skills/agent-folder-init/scripts/scaffold.py \
  --root /path/to/project \
  --name "My Project"

# With custom options
python3 ~/.claude/skills/agent-folder-init/scripts/scaffold.py \
  --root /path/to/project \
  --name "My Project" \
  --tech "nextjs,nestjs" \
  --allow-outside
```

## Generated Structure

### Documentation (.agent/)

```
.agent/
├── README.md                    # Navigation hub
├── SYSTEM/
│   ├── README.md
│   ├── RULES.md                 # Coding standards
│   ├── ARCHITECTURE.md          # What's implemented
│   ├── SUMMARY.md               # Current state
│   ├── ai/
│   │   ├── SESSION-QUICK-START.md
│   │   ├── SESSION-DOCUMENTATION-PROTOCOL.md
│   │   └── USER-PREFERENCES.md
│   ├── architecture/
│   │   ├── DECISIONS.md         # ADRs
│   │   └── PROJECT-MAP.md
│   ├── critical/
│   │   ├── CRITICAL-NEVER-DO.md
│   │   └── CROSS-PROJECT-RULES.md
│   └── quality/
│       └── SECURITY-CHECKLIST.md
├── TASKS/
│   ├── README.md
│   └── INBOX.md
├── SESSIONS/
│   ├── README.md
│   └── TEMPLATE.md
├── SOP/
│   └── README.md
├── EXAMPLES/
│   └── README.md
└── FEEDBACK/
    └── README.md
```

### Agent Configs

```
.claude/
├── commands/                    # Slash commands
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
├── rules/                       # Auto-loaded rules
│   ├── ai-agent-behavior.md
│   ├── coding-standards.md
│   ├── session-workflow.md
│   └── user-preferences.md
├── agents/                      # Specialized agents
│   ├── senior-backend-engineer.md
│   └── senior-frontend-engineer.md
└── skills/                      # Project-specific skills

.codex/
├── commands/
└── skills/

.cursor/
└── commands/
```

### Root Files

- `AGENTS.md` - Points to `.agent/README.md`
- `CLAUDE.md` - Claude-specific entry point
- `CODEX.md` - Codex-specific entry point
- `.editorconfig` - Editor configuration

## Key Patterns

### Naming Conventions
- **Top-level directories**: ALL-CAPS (`SYSTEM/`, `TASKS/`, `SESSIONS/`)
- **Files**: ALL-CAPS for critical files (`README.md`, `RULES.md`), kebab-case for others

### Session Files
- **One file per day**: `YYYY-MM-DD.md`
- Multiple sessions same day use Session 1, Session 2, etc. in the same file

## Customization

After scaffolding, customize:
1. `SYSTEM/RULES.md` - Add project-specific coding standards
2. `SYSTEM/ARCHITECTURE.md` - Document your architecture
3. `SYSTEM/critical/CRITICAL-NEVER-DO.md` - Add project-specific violations
4. `SOP/` - Add your standard operating procedures
5. `.claude/rules/` - Add project-specific rules
6. `.claude/commands/` - Add project-specific commands
