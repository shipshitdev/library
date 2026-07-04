![Ship Shit Dev Skills](./assets/banner.svg)

# Ship Shit Dev Skills

![Project Type](https://img.shields.io/badge/Project-Skills-blue)

163 AI agent skills for development workflows. Works with Claude Code, OpenAI Codex, and Cursor.

## Directory Structure

```
skills/
├── skills/              # All skills (163)
├── commands/            # All commands (30)
├── bundles/             # Generated marketplace bundles
├── .agents/             # Repo management, memory, meta-skills
│   ├── memory/          # Repo decisions, context, and system docs
│   ├── sessions/        # Historical session logs
│   └── skills/          # Meta-skills for maintaining this repo
├── .claude/             # Claude Code config (agents, rules)
├── .codex/              # Codex CLI config
└── scripts/             # Validation, generation, migration
```

## What's Included

- **The Dev Loop**: a board-driven autonomous workflow that ships software with
  `gh` + Claude + Codex.
- **Engineering Workflows**: code review, debugging, QA, release, GitHub triage,
  branch cleanup, production audit, and CI repair.
- **Implementation Specialists**: frontend, backend, infrastructure, security,
  testing, payments, and workspace setup skills.
- **Agent Engineering**: context engineering, memory systems, evaluation,
  multi-agent patterns, MCP building, and prompt/tool design.
- **Maintenance Tooling**: scripts that validate skills, regenerate bundles, and
  keep the marketplace catalog aligned with source.

## The Dev Loop — ship software with gh + Claude + Codex

The flagship workflow: a **board-driven autonomous dev loop** that turns a GitHub
issue into a reviewed PR, with you as architect/reviewer. It is the open, `gh`-driven
version of **ShipCode**'s pipeline — same stages, no app required.

- **Plan** (human): `feature-intake` → `prd-writer` / `writing-plans` write the PRD
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

Full reference: [`.agents/memory/system/ai-dev-loop.md`](.agents/memory/system/ai-dev-loop.md).

## Installation

### Quick Install (Recommended)

```bash
# Install all skills globally for Claude Code, Codex, and Cursor
npx skills add shipshitdev/skills -g --agent claude-code codex cursor --skill '*' -y

# Install specific skills
npx skills add shipshitdev/skills -g --skill stripe-implementer -y

# List available skills
npx skills add shipshitdev/skills --list
```

> **Do NOT use `--all`** — it installs to every agent the CLI knows about (30+).
> Always use `--agent` to target only the agents you use.

### Project-local Install

```bash
npx skills add shipshitdev/skills --agent claude-code codex cursor
```

### Claude Code Plugin (Alternative)

```bash
/plugin marketplace add shipshitdev/skills
/plugin install shipshitdev-dev-loop@shipshitdev
/plugin install shipshitdev-dev-workflow@shipshitdev
/plugin install shipshitdev-github@shipshitdev
/plugin install shipshitdev-testing@shipshitdev
/plugin install shipshitdev-security@shipshitdev
```

### For Contributors

```bash
git clone https://github.com/shipshitdev/skills.git ~/shipshitdev-skills
cd ~/shipshitdev-skills
npx skills add . -g --agent claude-code codex cursor --skill '*' -y
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

- `.agents/memory/system/skill-standards.md` - Agent Skills spec + Claude Code extensions
- `.agents/memory/system/skill-management.md` - Single-source skill workflow
- `.agents/memory/system/architecture.md` - .agents folder structure
- `.agents/memory/system/platform-adaptations.md` - Claude vs Codex writing guide
- `.agents/memory/system/ai-dev-loop.md` - Board-driven autonomous dev loop (`/loop` + agent-dispatch)

## Development Commands

| Command | Description |
|---------|-------------|
| address | Resolve PR review comments — propose fixes and replies |
| agent | Audit, configure, scaffold, and route agents and subagents |
| board | Set up, audit, or normalize a GitHub Projects v2 board |
| bug | File a GitHub bug issue |
| clean | Clean completed tasks and consolidate session files |
| codex-loop | Claim and work one dispatch:codex issue locally via codex exec |
| deploy | Deploy the app and provision infrastructure |
| design | Review and refine UI — audit, critique, polish, layout |
| deslop | Remove AI slop and tells from code |
| env | Scaffold and validate environment variables |
| feature | Capture requirements into PRD epics and GitHub issues |
| fix-ci | Diagnose and fix failing CI checks on a PR |
| inbox | Capture quick tasks into a project inbox |
| loop | Claim and work one dispatch issue end-to-end |
| merge | Review and land open PRs into the trunk |
| performance | Analyze frontend, backend, database, and infrastructure performance |
| pr | Create, update, and publish a pull request |
| prd | Create specs, PRDs, and feature plans |
| prompt | Optimize prompts for AI generation |
| qa | Run a structured verification pass before commit |
| release | Cut a trunk release with patch notes |
| review | Review changes, a PR, all open PRs, or recent commits |
| scan | Run dependency, code, config, and OWASP security scans |
| skill | Author, capture, test, and scout agent skills |
| standup | Summarize what you shipped over a time window |
| suggest | Post inline suggested changes on a PR |
| test | Run, author, and set up tests |
| tests | Run the right tests and turn red green |

## Skills (163)

### Dev Loop (10)

`interview`, `feature-intake`, `prd-writer`, `writing-plans`, `prd-quality-gate`, `prd-task-creator`, `executing-plans`, `setup-agent-routing`, `gh-project-board`, `qa-reviewer`

### Dev Workflow (42)

`agent-architecture-audit`, `agent-config-audit`, `ai-agent-cost-optimizer`, `ai-regression-testing`, `analyze-codebase`, `codebase-advisor`, `code-review`, `structural-review`, `full-code-review`, `review-dispatch`, `commit-summary`, `changelog-generator`, `standup`, `de-slop`, `refactor-dispatch`, `tech-debt`, `stack-modernization`, `debug`, `deploy`, `execution-debugging`, `deployment-composer`, `docs`, `llm-structured-output`, `merge-open-prs`, `production-audit`, `refactor-code`, `release`, `release-dispatch`, `release-cleanup`, `release-pr-gates`, `scaffold`, `shape`, `skill-capture`, `skill-comply`, `skill-scout`, `systematic-debugging`, `receiving-code-review`, `verification-before-completion`, `worktree`, `skill-dispatch`, `deploy-dispatch`, `ultracode`

### GitHub (19)

`bug`, `gh-address-comments`, `gh-fix-ci`, `gh-inbox`, `gh-pr-publish`, `gh-project-board`, `gh-review-suggestions`, `github-actions-author`, `git-safety`, `feature-intake`, `merge-open-prs`, `release`, `release-dispatch`, `release-cleanup`, `release-pr-gates`, `worktree`, `finishing-a-development-branch`, `pr-comments`, `fix-merge-conflicts`

### Testing (8)

`playwright-e2e-init`, `tdd`, `testing-expert`, `testing-cicd-init`, `qa-reviewer`, `husky-test-coverage`, `test-runner`, `test-dispatch`

### Frontend & React (31)

`frontend-design`, `component-library`, `accessibility`, `audit`, `clarify`, `critique`, `design-consistency-auditor`, `html-style`, `layout`, `polish`, `quieter`, `react-component-performance`, `react-hook-form`, `theme-factory`, `react-patterns`, `react-refactor`, `react-testing-library`, `react-native-components`, `expo-architect`, `landing-page-vercel`, `micro-landing-builder`, `ai-loading-ux`, `table-filters`, `quick-view`, `nextjs-validator`, `nextra-writer`, `shadcn`, `shadcn-setup`, `tailwind`, `tailwind-validator`, `design-dispatch`

### Backend & Data (8)

`api-design-expert`, `error-handling-expert`, `graphql-architect`, `nestjs-expert`, `incremental-fetch`, `turborepo`, `typescript-expert`, `typescript-refactor`

### Infrastructure (12)

`docker-expert`, `aws-infrastructure`, `ec2-backend-deployer`, `vercel-deploy`, `postgres-ops`, `mongodb-migration-expert`, `mongodb-atlas-checker`, `monitoring-setup`, `nestjs-queue-architect`, `performance-expert`, `redis-caching`, `security-expert`

### Security (5)

`security-audit`, `security-expert`, `git-safety`, `dependency-audit`, `open-source-checker`

### AI Agents (18)

`prompt-engineering`, `mcp-builder`, `skill-creator`, `context-fundamentals`, `context-optimization`, `context-degradation`, `context-engineering`, `memory-systems`, `multi-agent-patterns`, `tool-design`, `evaluation`, `advanced-evaluation`, `comment-mode`, `spec-first`, `agent-browser`, `agent-dispatch`, `codex-image-gen`, `ultracode`

### Workspace Setup (11)

`fullstack-workspace-init`, `project-init-orchestrator`, `linter-formatter-init`, `clerk-validator`, `content-script-developer`, `package-architect`, `artifacts-builder`, `open-source-checker`, `devcontainer-setup`, `biome-validator`, `bun-validator`

### Planning & PRDs (12)

`icp`, `roadmap-analyzer`, `roadmap-to-milestones`, `cto-advisor`, `interview`, `feature-intake`, `prd-task-creator`, `prd-writer`, `prd-quality-gate`, `rules-capture`, `writing-plans`, `prd-dispatch`

### Payments & Product Integrations (1)

`stripe-implementer`

### Session Management (7)

`agent-folder-init`, `session-end`, `session-start`, `session-documenter`, `executing-plans`, `setup-agent-routing`, `workspace-performance-audit`

## How Skills Adapt to Projects

Skills are **adaptive** - they scan project documentation to understand:

- Project architecture and structure
- Tooling, scripts, and CI conventions
- Existing patterns and conventions
- Domain terminology and implementation constraints

If a project has its own skill, the generic skill will collaborate with or defer to it.

## Publishing & CI/CD

When you push to `master`, GitHub Actions automatically regenerates the `bundles/` directory to keep marketplace plugins in sync with skills.

### Claude Marketplace

Users install directly from GitHub:

```bash
# Add the marketplace
/plugin marketplace add shipshitdev/skills

# Install category bundles
/plugin install shipshitdev-dev-loop@shipshitdev
/plugin install shipshitdev-dev-workflow@shipshitdev
/plugin install shipshitdev-github@shipshitdev
/plugin install shipshitdev-testing@shipshitdev
/plugin install shipshitdev-frontend@shipshitdev
/plugin install shipshitdev-backend@shipshitdev
/plugin install shipshitdev-infrastructure@shipshitdev
/plugin install shipshitdev-security@shipshitdev
/plugin install shipshitdev-session@shipshitdev
/plugin install shipshitdev-planning@shipshitdev
```
