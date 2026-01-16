# Ship Shit Dev Library

![Project Type](https://img.shields.io/badge/Project-Library-blue)

100+ AI agent skills for indie developers. Works with Claude Code, OpenAI Codex, and Cursor.

## Directory Structure

```
library/
├── .agent/              # Library management (sessions, tasks)
├── agents/              # DISTRIBUTABLE SKILLS & COMMANDS
│   ├── .claude/
│   │   ├── skills/      # 116 skills
│   │   └── commands/
│   ├── .codex/
│   │   ├── skills/      # 116 skills
│   │   └── commands/
│   └── .cursor/
│       ├── skills/      # 103 skills
│       └── commands/    # 30 commands
├── docs/                # Library documentation
│   ├── PLATFORM-ADAPTATIONS.md
│   ├── SKILL-MANAGEMENT.md
│   └── SYMLINK-CONFIG.md
└── scripts/             # Scaffolding, sync scripts
```

## Current Status

| Category   | Claude | Codex | Cursor | Status                        |
|------------|--------|-------|--------|-------------------------------|
| **Skills** | 116    | 116   | 103    | Claude/Codex parity           |
| **Commands** | 1     | 0     | 30     | Cursor-focused                |

## What's Included

- **Skills**: Specialized agent capabilities for specific domains (e.g., `stripe-implementer`, `mongodb-migration-expert`)
- **Commands**: Workflow commands for structured tasks (e.g., `code-review`, `deploy`, `mvp-plan`)
- **Documentation**: Platform-specific adaptations and management guides
- **Scripts**: Tooling for syncing, validation, and generation

## How It Works

This repo is symlinked from each agent's home directory:

```bash
~/.claude/skills   -> library/agents/.claude/skills
~/.claude/commands -> library/agents/.claude/commands
~/.codex/skills    -> library/agents/.codex/skills
~/.cursor/skills   -> library/agents/.cursor/skills
~/.cursor/commands -> library/agents/.cursor/commands
```

Edit capabilities in `agents/`, changes are immediately available to all agents.

See `docs/SYMLINK-CONFIG.md` for full configuration details.

## Installation

### Claude Code

```bash
# Add the marketplace
/plugin marketplace add shipshitdev/library

# Install all skills
/plugin install shipshitdev-full@shipshitdev

# Or install specific bundles
/plugin install shipshitdev-startup@shipshitdev
/plugin install shipshitdev-testing@shipshitdev
/plugin install shipshitdev-frontend@shipshitdev
```

### Manual Installation (Symlinks)

```bash
# Clone repository
git clone https://github.com/shipshitdev/library.git ~/shipshitdev-library

# Create symlinks
ln -s ~/shipshitdev-library/agents/.claude/skills ~/.claude/skills
ln -s ~/shipshitdev-library/agents/.claude/commands ~/.claude/commands
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

| Command          | Description                                    | Cursor                                                      |
|------------------|------------------------------------------------|-------------------------------------------------------------|
| analyze-codebase | Codebase analysis                               | [analyze-codebase](agents/.cursor/commands/analyze-codebase.md) |
| api-test         | API test generation                            | [api-test](agents/.cursor/commands/api-test.md)             |
| bug              | Bug capture workflow                            | [bug](agents/.cursor/commands/bug.md)                       |
| check-domain     | Domain name generator & availability checker   | [check-domain](agents/.cursor/commands/check-domain.md)       |
| clean            | Cleanup workflow                                | [clean](agents/.cursor/commands/clean.md)                     |
| code-review      | Code review                                     | [code-review](agents/.cursor/commands/code-review.md)        |
| db-setup         | MongoDB/Redis setup                             | [db-setup](agents/.cursor/commands/db-setup.md)              |
| de-slop          | Clean AI code artifacts                         | [de-slop](agents/.cursor/commands/de-slop.md)                |
| deploy           | Deployment workflows                            | [deploy](agents/.cursor/commands/deploy.md)                   |
| docs-generate    | Documentation generation                        | [docs-generate](agents/.cursor/commands/docs-generate.md)     |
| docs-update      | Documentation updates                           | [docs-update](agents/.cursor/commands/docs-update.md)        |
| end              | End session                                     | [end](agents/.cursor/commands/end.md)                         |
| env-setup        | Environment variables                           | [env-setup](agents/.cursor/commands/env-setup.md)            |
| inbox            | Process inbox items                             | [inbox](agents/.cursor/commands/inbox.md)                     |
| launch           | Launch workflow                                 | [launch](agents/.cursor/commands/launch.md)                    |
| migrate          | Database migrations                             | [migrate](agents/.cursor/commands/migrate.md)                 |
| monitoring-setup| Sentry/Analytics setup                         | [monitoring-setup](agents/.cursor/commands/monitoring-setup.md) |
| mvp-plan         | MVP planning                                    | [mvp-plan](agents/.cursor/commands/mvp-plan.md)               |
| new-cmd          | Create new commands                             | [new-cmd](agents/.cursor/commands/new-cmd.md)                 |
| new-session      | Create session files                            | [new-session](agents/.cursor/commands/new-session.md)         |
| optimize-prompt  | Prompt optimization                             | [optimize-prompt](agents/.cursor/commands/optimize-prompt.md)  |
| performance      | Performance analysis                            | [performance](agents/.cursor/commands/performance.md)           |
| quick-fix        | Quick fixes                                     | [quick-fix](agents/.cursor/commands/quick-fix.md)              |
| refactor-code    | Code refactoring                                | [refactor-code](agents/.cursor/commands/refactor-code.md)     |
| review-pr        | PR review                                       | [review-pr](agents/.cursor/commands/review-pr.md)              |
| scaffold         | Project scaffolding                             | [scaffold](agents/.cursor/commands/scaffold.md)                |
| security-audit   | Security audit                                  | [security-audit](agents/.cursor/commands/security-audit.md)   |
| start            | Start session                                   | [start](agents/.cursor/commands/start.md)                      |
| task             | Task management                                 | [task](agents/.cursor/commands/task.md)                         |
| test             | Test tracking                                   | [test](agents/.cursor/commands/test.md)                        |
| validate         | Validation workflow                             | [validate](agents/.cursor/commands/validate.md)                 |

## Skills

| Skill                      | Description                    | Claude | Codex | Cursor |
|----------------------------|--------------------------------|--------|-------|--------|
| accessibility              | WCAG 2.1 AA compliance         | Yes    | Yes   | Yes    |
| agent-folder-init          | Initialize .agent/ folder       | Yes    | Yes   | Yes    |
| analytics-expert            | Content analytics              | Yes    | Yes   | Yes    |
| api-design-expert          | RESTful API design             | Yes    | Yes   | Yes    |
| artifacts-builder          | Project artifacts              | Yes    | Yes   | Yes    |
| aws-infrastructure         | AWS EC2/VPC/ALB setup          | -      | -     | Yes    |
| changelog-generator       | Git changelogs                 | Yes    | Yes   | Yes    |
| clerk-implementer          | Clerk auth                    | Yes    | Yes   | -      |
| component-library          | Component standards            | Yes    | Yes   | Yes    |
| content-creator            | Newsletters & tweets with your voice | Yes | Yes | Yes |
| content-script-developer  | Browser extensions             | Yes    | Yes   | Yes    |
| copywriter                 | Brand copywriting              | Yes    | Yes   | Yes    |
| design-consistency-auditor | Design system                 | Yes    | Yes   | Yes    |
| docker-expert              | Docker/compose                 | -      | -     | Yes    |
| docs                      | Documentation                  | Yes    | Yes   | Yes    |
| docusaurus-writer         | Docusaurus sites               | Yes    | Yes   | Yes    |
| error-handling-expert      | Error patterns                 | Yes    | Yes   | Yes    |
| expo-architect             | Expo/React Native              | Yes    | Yes   | Yes    |
| fullstack-workspace-init   | Monorepo setup                 | Yes    | Yes   | Yes    |
| gh-address-comments       | GitHub comments                | Yes    | Yes   | Yes    |
| gh-fix-ci                 | Fix CI/CD                      | Yes    | Yes   | Yes    |
| internal-comms            | Internal comms                 | Yes    | Yes   | Yes    |
| landing-page-vercel        | Vercel landing pages           | Yes    | Yes   | Yes    |
| leads-researcher           | Lead research                  | Yes    | Yes   | -      |
| mcp-builder                | MCP servers                    | Yes    | Yes   | Yes    |
| micro-landing-builder      | Micro landing pages            | Yes    | Yes   | Yes    |
| mongodb-migration-expert   | MongoDB migrations             | Yes    | Yes   | Yes    |
| monitoring-setup          | Sentry/Analytics               | -      | -     | Yes    |
| nestjs-queue-architect     | BullMQ queues                 | Yes    | Yes   | Yes    |
| nestjs-testing-expert      | NestJS testing                 | Yes    | Yes   | Yes    |
| package-architect          | npm packages                   | Yes    | Yes   | Yes    |
| performance-expert         | Performance                    | Yes    | Yes   | Yes    |
| planning-assistant         | Content planning               | Yes    | Yes   | Yes    |
| plasmo-extension-architect | Plasmo extensions             | Yes    | Yes   | Yes    |
| project-scaffold           | Project scaffolding            | Yes    | Yes   | Yes    |
| prompt-engineer             | Prompt engineering             | Yes    | Yes   | Yes    |
| qa-reviewer                | QA review                      | Yes    | Yes   | Yes    |
| react-native-components    | RN components                  | Yes    | Yes   | Yes    |
| roadmap-analyzer           | Product roadmap                | Yes    | Yes   | Yes    |
| rules-capture              | Coding rules                   | Yes    | Yes   | Yes    |
| search-domain-validator    | Domain validation              | Yes    | Yes   | -      |
| security-expert            | App security                   | Yes    | Yes   | Yes    |
| serializer-specialist      | Data serialization             | Yes    | Yes   | Yes    |
| session-documenter         | Session docs                  | Yes    | Yes   | Yes    |
| skill-creator              | Skill creation                | Yes    | Yes   | Yes    |
| strategy-expert            | Content strategy               | Yes    | Yes   | Yes    |
| stripe-implementer         | Stripe payments               | Yes    | Yes   | Yes    |
| task-prd-creator           | Task & PRD creation workflow   | Yes    | Yes   | Yes    |
| testing-expert             | Testing strategies             | Yes    | Yes   | Yes    |
| webapp-testing             | Web app testing                | Yes    | Yes   | Yes    |
| workflow-automation        | Workflow automation            | Yes    | Yes   | Yes    |

## Complementary Skills (External)

These external skill repositories complement this library. Install them separately when needed.

| Category | Skill | Description | Source |
|----------|-------|-------------|--------|
| **Audit Lifecycle** | fix-review | Verify fix commits address audit findings | trailofbits |
| **Code Auditing** | audit-context-building | Deep architectural context analysis | trailofbits |
| | burpsuite-project-parser | Search and extract data from Burp Suite files | trailofbits |
| | differential-review | Security-focused code change review | trailofbits |
| | semgrep-rule-creator | Custom Semgrep rule creation | trailofbits |
| | sharp-edges | Identify error-prone APIs and footgun designs | trailofbits |
| | static-analysis | CodeQL, Semgrep, SARIF toolkit | trailofbits |
| | testing-handbook-skills | Fuzzers, sanitizers, coverage tools | trailofbits |
| | variant-analysis | Find similar vulnerabilities across codebases | trailofbits |
| **Development** | ask-questions-if-underspecified | Clarify requirements before implementing | trailofbits |
| | culture-index | Interpret Culture Index survey results | trailofbits |
| **Frontend** | react-best-practices | React/Next.js performance optimization patterns | vercel-labs |
| | web-design-guidelines | Review UI for Web Interface Guidelines compliance | vercel-labs |
| **Reverse Engineering** | dwarf-expert | DWARF debugging format expertise | trailofbits |
| **Smart Contracts** | building-secure-contracts | Security toolkit for 6 blockchains | trailofbits |
| | entry-point-analyzer | Identify state-changing entry points | trailofbits |
| **Verification** | constant-time-analysis | Detect timing side-channels in crypto code | trailofbits |
| | property-based-testing | Property-based testing for multiple languages | trailofbits |
| | spec-to-code-compliance | Specification compliance checker | trailofbits |

### Installation

```bash
# vercel-labs/agent-skills (Frontend)
claude plugin marketplace add vercel-labs --source github --owner vercel-labs --repo agent-skills
claude plugin install <skill-name>@vercel-labs

# trailofbits/skills (Security)
claude plugin marketplace add trailofbits --source github --owner trailofbits --repo skills
claude plugin install <skill-name>@trailofbits
```

**Repositories:**

- https://github.com/vercel-labs/agent-skills
- https://github.com/trailofbits/skills

---

## How Skills Adapt to Projects

Skills are **adaptive** - they scan project documentation to understand:

- Project architecture and structure
- Brand voice and tone
- Existing patterns and conventions
- Terminology and style

If a project has its own skill, the generic skill will collaborate with or defer to it.

## Publishing & CI/CD

When you push to `master`, GitHub Actions automatically regenerates the `bundles/` directory to keep marketplace plugins in sync with skills.

### Claude Marketplace

Users install directly from GitHub:

```bash
# Add the marketplace
/plugin marketplace add shipshitdev/library

# Install full library
/plugin install shipshitdev-full@shipshitdev

# Or install specific bundles
/plugin install shipshitdev-startup@shipshitdev
/plugin install shipshitdev-testing@shipshitdev
/plugin install shipshitdev-frontend@shipshitdev
```
