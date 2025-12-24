# Global Skills & Commands Repository

Centralized **global** skills and commands for Claude Code, OpenAI Codex, and Cursor.

## Directory Structure

```
skills/
├── .claude/
│   ├── skills/              # Claude global skills (12)
│   └── commands/            # Claude global commands
│
├── .codex/
│   ├── skills/              # Codex global skills (36)
│   └── commands/            # Codex global commands
│
└── .cursor/
    ├── skills/              # Cursor global skills (5)
    └── commands/            # Cursor global commands (18)
```

## How It Works

This repo is symlinked from each agent's home directory:

```
~/.claude/skills -> /Users/decod3rs/www/agenticindiedev/skills/.claude/skills
~/.codex/skills  -> /Users/decod3rs/www/agenticindiedev/skills/.codex/skills
~/.cursor/commands -> /Users/decod3rs/www/agenticindiedev/skills/.cursor/commands
~/.cursor/skills -> /Users/decod3rs/www/agenticindiedev/skills/.cursor/skills
```

Project repos can also symlink to specific skills here for shared functionality.

**Project Integration:**
- Projects can symlink to this repo for generic commands and skills
- Project-specific commands and skills remain in project workspace
- Skills adapt to project context by scanning project documentation

Edit skills/commands here, changes are immediately available to agents.

## Installation

This repository contains skills and commands that can be installed individually. Each item has its own installation instructions.

**Quick Start:**

1. Clone this repository
2. Choose the skills/commands you want to install
3. Follow the installation instructions in each item's directory

**Installation Methods:**

- **Symlink** (recommended): Automatically receive updates when the repository is updated
- **Copy**: Complete independence, customize without affecting source

See [INSTALL.md](INSTALL.md) for:

- Complete installation guide
- Registry of all available skills/commands
- Installation method comparison
- Troubleshooting

**Individual Installation:**

- **Commands**: Each command file (`.cursor/commands/*.md`) contains installation instructions at the top
- **Skills**: Each skill directory contains an `INSTALL.md` file with detailed instructions

## Current Skills & Commands

### Cursor (.cursor/)

**Commands (18):**

- analyze-codebase, bug, clean, code-review, docs-generate, docs-update, end, inbox, new-cmd, new-session, optimize-prompt, quick-fix, refactor-code, review-pr, start, task, test, validate

**Skills (5):**

- analytics-expert, planning-assistant, project-scaffold, strategy-expert, workflow-automation

See `.cursor/commands/README.md` and `.cursor/skills/README.md` for details.

### Claude (.claude/skills/)

- agent-folder-init
- changelog-generator
- design-consistency-auditor
- fullstack-workspace-init
- internal-comms
- micro-landing-builder
- project-scaffold
- qa-reviewer
- roadmap-analyzer
- session-documenter
- skill-creator
- webapp-testing

### Codex (.codex/skills/)

- accessibility
- agent-folder-init
- analytics-expert
- artifacts-builder
- changelog-generator
- component-library
- content-script-developer
- copywriter
- design-consistency-auditor
- docs
- docusaurus-writer
- expo-architect
- fullstack-workspace-init
- gh-address-comments
- gh-fix-ci
- internal-comms
- landing-page-vercel
- mcp-builder
- micro-landing-builder
- mongodb-migration-expert
- nestjs-queue-architect
- nestjs-testing-expert
- package-architect
- planning-assistant
- plasmo-extension-architect
- project-scaffold
- prompt-engineer
- qa-reviewer
- react-native-components
- roadmap-analyzer
- rules-capture
- serializer-specialist
- session-documenter
- strategy-expert
- webapp-testing
- workflow-automation

## Adding Skills & Commands

### Adding Commands

1. Create a new `.md` file in `.cursor/commands/`
2. Follow the naming convention: `{verb}-{noun}.md` (e.g., `analyze-codebase.md`, `review-pr.md`)
3. Use standard `.agent/` folder structure:
   - `.agent/SYSTEM/` - Architecture, rules, summary
   - `.agent/SESSIONS/` - Session documentation
   - `.agent/TASKS/` - Task files
   - `.agent/PRDS/` - Product requirement documents
   - `.agent/EXAMPLES/` - Code examples
4. Use placeholders only for project-specific paths:
   - `[project]` - Project name/path
   - `[frontend-project]` - Frontend project path
   - `[backend-project]` - Backend project path
5. Update `.cursor/commands/README.md` with the new command

See `GENERICIZATION.md` for detailed guidelines on making commands generic.

### Adding Skills

1. Create a new directory in `.cursor/skills/` (or `.claude/skills/`, `.codex/skills/`)
2. Add `SKILL.md` file with YAML frontmatter
3. Include instructions and examples
4. Update the appropriate skills `README.md` with the new skill

```bash
# Cursor skill
mkdir -p .cursor/skills/my-skill
touch .cursor/skills/my-skill/SKILL.md

# Claude skill
mkdir -p .claude/skills/my-skill
touch .claude/skills/my-skill/SKILL.md

# Codex skill
mkdir -p .codex/skills/my-skill
touch .codex/skills/my-skill/SKILL.md
```

## Skill Format

```
skill-name/
├── README.md           # Description, usage
├── SKILL.md            # Main prompt/instructions (or skill.md)
├── scripts/            # Optional automation
└── templates/          # Optional templates
```

## Documentation

- `INSTALL.md` - Complete installation guide for all skills/commands
- `.cursor/commands/README.md` - Cursor commands reference
- `.cursor/skills/README.md` - Cursor skills reference

## How Skills Adapt to Projects

Skills in this repository are designed to be **adaptive**:

1. **Discover Project Context**: Skills scan project documentation (`.agent/SYSTEM/`, `.agent/SOP/`, etc.) to understand:
   - Project architecture and structure
   - Brand voice and tone
   - Existing patterns and conventions
   - Terminology and style

2. **Use Project-Specific Skills**: If a project has its own skill (e.g., `[project]-analytics-expert`), the generic skill will collaborate with or defer to it

3. **Adapt to Project Patterns**: Skills match the project's:
   - Documentation style
   - Code patterns
   - Naming conventions
   - Workflow processes
