# Agentic Indie Library

Centralized **global** skills and commands for Claude Code, OpenAI Codex, and Cursor.

## Directory Structure

```
library/
├── .agent/              # Library management (sessions, tasks)
├── agents/              # DISTRIBUTABLE SKILLS & COMMANDS
│   ├── .claude/
│   │   ├── skills/      # 42 skills
│   │   └── commands/
│   ├── .codex/
│   │   ├── skills/      # 42 skills
│   │   └── commands/
│   └── .cursor/
│       ├── skills/      # 47 skills
│       └── commands/    # 30 commands
├── docs/                # Library documentation
│   ├── PLATFORM-ADAPTATIONS.md
│   ├── SKILL-MANAGEMENT.md
│   └── SYMLINK-CONFIG.md
└── scripts/             # Scaffolding, sync scripts
```

## Current Status

| Category | Claude | Codex | Cursor | Status |
|----------|--------|-------|--------|--------|
| **Skills** | 43 | 43 | 48 | Base parity + Cursor extras |
| **Commands** | 1 | 0 | 30 | Cursor-focused |

## How It Works

This repo is symlinked from each agent's home directory:

```bash
~/.claude/skills   -> library/agents/.claude/skills
~/.claude/commands -> library/agents/.claude/commands
~/.codex/skills    -> library/agents/.codex/skills
~/.cursor/skills   -> library/agents/.cursor/skills
~/.cursor/commands -> library/agents/.cursor/commands
```

Edit skills/commands in `agents/`, changes are immediately available to all agents.

See `docs/SYMLINK-CONFIG.md` for full configuration details.

## Installation

```bash
# Clone repository
git clone <repo-url> ~/www/agenticindiedev/library

# Create symlinks (adjust path as needed)
ln -s /path/to/library/agents/.claude/skills ~/.claude/skills
ln -s /path/to/library/agents/.claude/commands ~/.claude/commands
ln -s /path/to/library/agents/.codex/skills ~/.codex/skills
ln -s /path/to/library/agents/.cursor/skills ~/.cursor/skills
ln -s /path/to/library/agents/.cursor/commands ~/.cursor/commands
```

## Adding Skills & Commands

### Adding a Skill

1. Create directory in `agents/.claude/skills/skill-name/`
2. Add `SKILL.md` with YAML frontmatter
3. Sync to other platforms (see `docs/PLATFORM-ADAPTATIONS.md`)
4. Update this README

```bash
mkdir -p agents/.claude/skills/my-skill
touch agents/.claude/skills/my-skill/SKILL.md
```

### Adding a Command

1. Create `.md` file in `agents/.cursor/commands/`
2. Follow naming: `{verb}-{noun}.md`
3. Update this README

## Documentation

- `docs/PLATFORM-ADAPTATIONS.md` - Claude vs Codex vs Cursor differences
- `docs/SKILL-MANAGEMENT.md` - Syncing skills across platforms
- `docs/SYMLINK-CONFIG.md` - Current symlink configuration

## Commands

| Command | Description | Cursor |
|---------|-------------|--------|
| analyze-codebase | Codebase analysis | [Link](agents/.cursor/commands/analyze-codebase.md) |
| api-test | API test generation | [Link](agents/.cursor/commands/api-test.md) |
| bug | Bug capture workflow | [Link](agents/.cursor/commands/bug.md) |
| clean | Cleanup workflow | [Link](agents/.cursor/commands/clean.md) |
| code-review | Code review | [Link](agents/.cursor/commands/code-review.md) |
| db-setup | MongoDB/Redis setup | [Link](agents/.cursor/commands/db-setup.md) |
| de-slop | Clean AI code artifacts | [Link](agents/.cursor/commands/de-slop.md) |
| deploy | Deployment workflows | [Link](agents/.cursor/commands/deploy.md) |
| docs-generate | Documentation generation | [Link](agents/.cursor/commands/docs-generate.md) |
| docs-update | Documentation updates | [Link](agents/.cursor/commands/docs-update.md) |
| end | End session | [Link](agents/.cursor/commands/end.md) |
| env-setup | Environment variables | [Link](agents/.cursor/commands/env-setup.md) |
| inbox | Process inbox items | [Link](agents/.cursor/commands/inbox.md) |
| launch | Launch workflow | [Link](agents/.cursor/commands/launch.md) |
| migrate | Database migrations | [Link](agents/.cursor/commands/migrate.md) |
| monitoring-setup | Sentry/Analytics setup | [Link](agents/.cursor/commands/monitoring-setup.md) |
| mvp-plan | MVP planning | [Link](agents/.cursor/commands/mvp-plan.md) |
| new-cmd | Create new commands | [Link](agents/.cursor/commands/new-cmd.md) |
| new-session | Create session files | [Link](agents/.cursor/commands/new-session.md) |
| optimize-prompt | Prompt optimization | [Link](agents/.cursor/commands/optimize-prompt.md) |
| performance | Performance analysis | [Link](agents/.cursor/commands/performance.md) |
| quick-fix | Quick fixes | [Link](agents/.cursor/commands/quick-fix.md) |
| refactor-code | Code refactoring | [Link](agents/.cursor/commands/refactor-code.md) |
| review-pr | PR review | [Link](agents/.cursor/commands/review-pr.md) |
| scaffold | Project scaffolding | [Link](agents/.cursor/commands/scaffold.md) |
| security-audit | Security audit | [Link](agents/.cursor/commands/security-audit.md) |
| start | Start session | [Link](agents/.cursor/commands/start.md) |
| task | Task management | [Link](agents/.cursor/commands/task.md) |
| test | Test tracking | [Link](agents/.cursor/commands/test.md) |
| validate | Validation workflow | [Link](agents/.cursor/commands/validate.md) |

## Skills

| Skill | Description | Claude | Codex | Cursor |
|-------|-------------|--------|-------|--------|
| accessibility | WCAG 2.1 AA compliance | Yes | Yes | Yes |
| agent-folder-init | Initialize .agent/ folder | Yes | Yes | Yes |
| analytics-expert | Content analytics | Yes | Yes | Yes |
| api-design-expert | RESTful API design | Yes | Yes | Yes |
| artifacts-builder | Project artifacts | Yes | Yes | Yes |
| aws-infrastructure | AWS EC2/VPC/ALB setup | - | - | Yes |
| changelog-generator | Git changelogs | Yes | Yes | Yes |
| clerk-implementer | Clerk auth | Yes | Yes | - |
| component-library | Component standards | Yes | Yes | Yes |
| content-creator | Newsletters & tweets with your voice | Yes | Yes | Yes |
| content-script-developer | Browser extensions | Yes | Yes | Yes |
| copywriter | Brand copywriting | Yes | Yes | Yes |
| design-consistency-auditor | Design system | Yes | Yes | Yes |
| docker-expert | Docker/compose | - | - | Yes |
| docs | Documentation | Yes | Yes | Yes |
| docusaurus-writer | Docusaurus sites | Yes | Yes | Yes |
| error-handling-expert | Error patterns | Yes | Yes | Yes |
| expo-architect | Expo/React Native | Yes | Yes | Yes |
| fullstack-workspace-init | Monorepo setup | Yes | Yes | Yes |
| gh-address-comments | GitHub comments | Yes | Yes | Yes |
| gh-fix-ci | Fix CI/CD | Yes | Yes | Yes |
| internal-comms | Internal comms | Yes | Yes | Yes |
| landing-page-vercel | Vercel landing pages | Yes | Yes | Yes |
| leads-researcher | Lead research | Yes | Yes | - |
| mcp-builder | MCP servers | Yes | Yes | Yes |
| micro-landing-builder | Micro landing pages | Yes | Yes | Yes |
| mongodb-migration-expert | MongoDB migrations | Yes | Yes | Yes |
| monitoring-setup | Sentry/Analytics | - | - | Yes |
| nestjs-queue-architect | BullMQ queues | Yes | Yes | Yes |
| nestjs-testing-expert | NestJS testing | Yes | Yes | Yes |
| package-architect | npm packages | Yes | Yes | Yes |
| performance-expert | Performance | Yes | Yes | Yes |
| planning-assistant | Content planning | Yes | Yes | Yes |
| plasmo-extension-architect | Plasmo extensions | Yes | Yes | Yes |
| project-scaffold | Project scaffolding | Yes | Yes | Yes |
| prompt-engineer | Prompt engineering | Yes | Yes | Yes |
| qa-reviewer | QA review | Yes | Yes | Yes |
| react-native-components | RN components | Yes | Yes | Yes |
| roadmap-analyzer | Product roadmap | Yes | Yes | Yes |
| rules-capture | Coding rules | Yes | Yes | Yes |
| search-domain-validator | Domain validation | Yes | Yes | - |
| security-expert | App security | Yes | Yes | Yes |
| serializer-specialist | Data serialization | Yes | Yes | Yes |
| session-documenter | Session docs | Yes | Yes | Yes |
| skill-creator | Skill creation | Yes | Yes | Yes |
| strategy-expert | Content strategy | Yes | Yes | Yes |
| stripe-implementer | Stripe payments | Yes | Yes | Yes |
| testing-expert | Testing strategies | Yes | Yes | Yes |
| webapp-testing | Web app testing | Yes | Yes | Yes |
| workflow-automation | Workflow automation | Yes | Yes | Yes |

## How Skills Adapt to Projects

Skills are **adaptive** - they scan project documentation to understand:

- Project architecture and structure
- Brand voice and tone
- Existing patterns and conventions
- Terminology and style

If a project has its own skill, the generic skill will collaborate with or defer to it.
