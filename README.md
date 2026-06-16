![Ship Shit Dev Skills](./assets/banner.svg)

# Ship Shit Dev Skills

![Project Type](https://img.shields.io/badge/Project-Skills-blue)

182 AI agent skills for indie developers. Works with Claude Code and OpenAI Codex.

## Directory Structure

```
skills/
├── skills/              # All skills (182)
├── commands/            # All commands (13)
├── bundles/             # Generated marketplace bundles
├── .agents/             # Repo management, memory, meta-skills
│   ├── SYSTEM/          # Architecture docs, skill standards
│   ├── memory/          # Repo decisions and context
│   └── skills/          # Meta-skills for maintaining this repo
├── .claude/             # Claude Code config (agents, rules)
├── .codex/              # Codex CLI config
└── scripts/             # Validation, generation, migration
```

## What's Included

- **Skills**: Specialized agent capabilities for specific domains (e.g., `stripe-implementer`, `nestjs-expert`)
- **Commands**: Workflow commands for structured tasks (e.g., `check-domain`, `security-audit`, `performance`)
- **Scripts**: Validation, generation, and migration tooling
- **The Dev Loop**: a board-driven autonomous workflow that ships software with
  `gh` + Claude + Codex (see below)

## The Dev Loop — ship software with gh + Claude + Codex

The flagship workflow: a **board-driven autonomous dev loop** that turns a GitHub
issue into a reviewed PR, with you as architect/reviewer. It is the open, `gh`-driven
version of **ShipCode**'s pipeline — same stages, no app required.

- **Plan** (human): `feature-intake` → `writing-prds` / `writing-plans` write the PRD
  and implementation plan onto the issue.
- **Dispatch** (human opt-in): apply `dispatch:claude` (Claude lane),
  `dispatch:codex` (Codex lane), or `dispatch:openrouter` (OpenRouter lane) to a
  **Backlog** issue.
- **Execute** (AI): the loop claims it → **In Progress** → branch → implement →
  `qa-reviewer` + tests → PR, advancing `loop:*` phase labels as it goes.
- **Review** (human): the PR lands in **Human Review**, auto-assigned to you. Merge =
  Done; reject = back to Backlog.

Board columns are for humans (**Backlog · In Progress · Human Review · Done ·
Deferred**); the AI loop's sub-phases ride as `loop:*` labels. Status is the GitHub
Projects board `Status` field — the single source of truth.

```bash
# 1. Install the dev-loop bundle (every skill the loop needs)
/plugin marketplace add shipshitdev/skills
/plugin install shipshitdev-dev-loop@shipshitdev

# 2. Provision your repo: labels + board + workflows + secrets (idempotent)
bash scripts/setup-dev-loop.sh            # --dry-run to preview

# 3. Write your repo's routing block (tracker + labels + domain). In Claude Code:
/setup-agent-routing

# 4. Drive it
/loop                                     # Phase 1: local pull (Claude lane)
# …or apply dispatch:claude / dispatch:codex to fire Phase 2 (GitHub Actions)
```

Full reference: [`.agents/SYSTEM/AI-DEV-LOOP.md`](.agents/SYSTEM/AI-DEV-LOOP.md).

## Installation

### Quick Install (Recommended)

```bash
# Install all skills globally for Claude Code and Codex
npx skills add shipshitdev/skills -g --agent claude-code codex --skill '*' -y

# Install specific skills
npx skills add shipshitdev/skills -g --skill stripe-implementer -y

# List available skills
npx skills add shipshitdev/skills --list
```

> **Do NOT use `--all`** — it installs to every agent the CLI knows about (30+).
> Always use `--agent` to target only the agents you use.

### Project-local Install

```bash
npx skills add shipshitdev/skills --agent claude-code codex
```

### Claude Code Plugin (Alternative)

```bash
/plugin marketplace add shipshitdev/skills
/plugin install shipshitdev-startup@shipshitdev    # or any category bundle
/plugin install shipshitdev-dev-workflow@shipshitdev
```

### For Contributors

```bash
git clone https://github.com/shipshitdev/skills.git ~/shipshitdev-skills
cd ~/shipshitdev-skills
npx skills add . -g --agent claude-code codex --skill '*' -y
```

## Adding Skills & Commands

### Adding a Skill

1. Create directory in `skills/skill-name/`
2. Add `SKILL.md` with YAML frontmatter
3. Update this README

```bash
mkdir -p skills/my-skill
touch skills/my-skill/SKILL.md
```

### Adding a Command

1. Create `.md` file in `commands/`
2. Follow naming: `{verb}-{noun}.md`
3. Update this README

## Documentation

- `.agents/SYSTEM/SKILL-STANDARDS.md` - Agent Skills spec + Claude Code extensions
- `.agents/SYSTEM/SKILL-MANAGEMENT.md` - Single-source skill workflow
- `.agents/SYSTEM/ARCHITECTURE.md` - .agents folder structure
- `.agents/SYSTEM/PLATFORM-ADAPTATIONS.md` - Claude vs Codex writing guide
- `.agents/SYSTEM/AI-DEV-LOOP.md` - Board-driven autonomous dev loop (`/loop` + agent-dispatch)

## Commands

| Command | Description |
|---------|-------------|
| bug | File a GitHub bug issue |
| check-domain | Domain name generator & availability checker |
| clean | Cleanup workflow |
| co-founder | Strategic business partner workflow |
| env-setup | Environment variables |
| feature | Client requirement intake |
| inbox | Process inbox items |
| loop | Claim and work one dispatch:claude issue end-to-end |
| merge | Review and land open PRs into the trunk |
| release | Cut a trunk release with patch notes |
| optimize-prompt | Prompt optimization |
| performance | Performance analysis |
| security-audit | Security audit |

## Skills (182)

### Startup (14)

`business-model-auditor`, `cofounder-evaluator`, `constraint-eliminator`, `early-hiring-advisor`, `execution-accelerator`, `execution-validator`, `fundraise-advisor`, `idea-validator`, `market-sizer`, `mvp-architect`, `offer-architect`, `offer-validator`, `pricing-strategist`, `startup-icp-definer`

### Sales (13)

`channel-validator`, `competitive-intelligence-analyst`, `email-finder`, `funnel-architect`, `funnel-validator`, `lead-channel-optimizer`, `leads-researcher`, `outbound-optimizer`, `partnership-builder`, `retention-engine`, `support-systems-architect`, `traffic-architect`, `traffic-validator`

### Marketing & CRO (1)

`x-algorithm-optimizer`

### Branding (5)

`brand-architect`, `expert-architect`, `expert-validator`, `positioning-angles`, `search-domain-validator`

### Content (9)

`changelog-generator`, `content-creator`, `copy-validator`, `copywriter`, `docs`, `humanizer`, `internal-comms`, `nextra-writer`, `youtube-video-analyst`

### Planning (10)

`business-operator`, `cto-advisor`, `feature-intake`, `prd-quality-gate`, `roadmap-analyzer`, `rules-capture`, `strategy-expert`, `task-prd-creator`, `writing-plans`, `writing-prds`

### Frontend & React (28)

`accessibility`, `ai-loading-ux`, `clarify`, `component-library`, `critique`, `design-consistency-auditor`, `expo-architect`, `frontend-design`, `html-style`, `landing-page-vercel`, `layout`, `micro-landing-builder`, `nextjs-validator`, `polish`, `quick-view`, `quieter`, `react-component-performance`, `react-hook-form`, `react-native-components`, `react-patterns`, `react-refactor`, `react-testing-library`, `shadcn`, `shadcn-setup`, `table-filters`, `tailwind`, `tailwind-validator`, `theme-factory`

### Backend & Data (8)

`api-design-expert`, `error-handling-expert`, `graphql-architect`, `incremental-fetch`, `nestjs-expert`, `turborepo`, `typescript-expert`, `typescript-refactor`

### Infrastructure (11)

`aws-infrastructure`, `docker-expert`, `ec2-backend-deployer`, `mongodb-atlas-checker`, `mongodb-migration-expert`, `monitoring-setup`, `nestjs-queue-architect`, `performance-expert`, `production-audit`, `redis-caching`, `security-expert`

### Payments (2)

`financial-operations-expert`, `stripe-implementer`

### Security (1)

`security-audit`

### Testing (7)

`ai-regression-testing`, `husky-test-coverage`, `playwright-e2e-init`, `qa-reviewer`, `tdd`, `testing-cicd-init`, `testing-expert`

### AI Agents (17)

`advanced-evaluation`, `agent-architecture-audit`, `agent-browser`, `ai-agent-cost-optimizer`, `comment-mode`, `context-degradation`, `context-engineering`, `context-fundamentals`, `context-optimization`, `evaluation`, `mcp-builder`, `memory-systems`, `multi-agent-patterns`, `skill-comply`, `skill-creator`, `spec-first`, `tool-design`

### Dev Workflow (26)

`agent-config-audit`, `analyze-codebase`, `audit`, `code-review`, `codebase-advisor`, `commit-summary`, `de-slop`, `debug`, `deploy`, `deployment-composer`, `execution-debugging`, `full-code-review`, `llm-structured-output`, `merge-open-prs`, `prompt-engineering`, `receiving-code-review`, `refactor-code`, `release`, `scaffold`, `shape`, `skill-capture`, `skill-scout`, `structural-review`, `systematic-debugging`, `verification-before-completion`, `worktree`

### GitHub (14)

`bug`, `feature-intake`, `finishing-a-development-branch`, `gh-address-comments`, `gh-fix-ci`, `gh-inbox`, `gh-pr-publish`, `gh-project-board`, `gh-review-suggestions`, `github-actions-author`, `git-safety`, `release-cleanup`, `release-pr-gates`, `worktree`

### Session Management (7)

`agent-folder-init`, `executing-plans`, `session-documenter`, `session-end`, `session-start`, `setup-agent-routing`, `workspace-performance-audit`

### Workspace Setup (11)

`artifacts-builder`, `biome-validator`, `bun-validator`, `clerk-validator`, `content-script-developer`, `devcontainer-setup`, `fullstack-workspace-init`, `linter-formatter-init`, `open-source-checker`, `package-architect`, `project-init-orchestrator`

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
/plugin marketplace add shipshitdev/skills

# Install category bundles
/plugin install shipshitdev-startup@shipshitdev
/plugin install shipshitdev-testing@shipshitdev
/plugin install shipshitdev-frontend@shipshitdev
/plugin install shipshitdev-dev-workflow@shipshitdev
/plugin install shipshitdev-security@shipshitdev
# Autonomous dev loop (executing-plans, setup-agent-routing, feature-intake, writing-prds, …)
/plugin install shipshitdev-session@shipshitdev
/plugin install shipshitdev-planning@shipshitdev
# The whole dev loop in one bundle (feature-intake → executing-plans → qa-reviewer …)
/plugin install shipshitdev-dev-loop@shipshitdev
```
