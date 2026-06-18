# Repository Architecture

last_verified: 2026-06-18

## Directory Map

```
skills-repo/
├── skills/                          # 141 skills (source of truth)
│   └── <skill-name>/
│       ├── SKILL.md                 # Skill definition (frontmatter + body)
│       └── plugin.json              # Skill distribution manifest
│
├── commands/                        # 11 slash commands (.md files, flat)
│   └── <command-name>.md
│
├── bundles/                         # 13 themed bundles (generated snapshots)
│   └── <bundle-name>/
│       ├── plugin.json              # Bundle manifest
│       └── skills/                  # Copies of bundled skills
│
├── scripts/                         # Build, validate, generate tooling
│   ├── generate-marketplace-bundles.js # Bundle snapshot generation
│   ├── generate-marketplace-json.js # Marketplace catalog generation
│   ├── validate-skill-sync.sh       # Skill validation (frontmatter, structure)
│   ├── validate-changed-skills.sh   # Pre-commit hook: validate only changed
│   ├── cleanup-global-duplicates.sh # Remove duplicate installs from ~/.claude
│   ├── install-skills.sh            # npx skills add entrypoint
│   ├── migrate-frontmatter.py       # Spec migration tool
│   ├── lint-shellcheck.sh           # Shell lint wrapper
│   └── plugin-categories.json       # Bundle → skills mapping data
│
├── prompts/                         # Reusable prompts
│   └── prd-interview.md
│
├── assets/                          # Static assets
│   └── banner.svg
│
├── .agents/                         # AI agent workspace
│   ├── README.md                    # Agent entry point
│   ├── memory/                      # Persistent memory (this dir)
│   │   └── system/                  # Project docs and standards
│   │       ├── architecture.md      # .agents/ folder structure
│   │       ├── ai-dev-loop.md       # /loop workflow
│   │       ├── skill-standards.md   # Skill authoring spec
│   │       ├── skill-management.md  # Sync workflow
│   │       └── platform-adaptations.md # Claude vs Codex differences
│   └── sessions/                    # Historical session logs
│
├── .claude/                         # Claude Code config
│   ├── rules/CLAUDE_RULES.md        # Project rules
│   └── settings.local.json          # Local permissions + plugins
│
├── .claude-plugin/
│   └── marketplace.json             # Full marketplace catalog (generated)
│
├── .github/workflows/
│   └── generate-bundles.yml         # CI: regenerate on push to master
│
├── .husky/                          # Git hooks (pre-commit)
├── biome.json                       # JS/JSON formatter + linter config
├── .markdownlint.json               # Markdown lint rules
└── package.json                     # Bun project config
```

## Data Flow

```
skills/<name>/SKILL.md    ──→  scripts/generate-marketplace-bundles.js  ──→  bundles/<name>/
skills/<name>/plugin.json ──→  copied into bundle snapshots
skills/<name>/SKILL.md    ──→  scripts/generate-marketplace-json.js     ──→  .claude-plugin/marketplace.json
```

All generation is triggered by: `bun run marketplace:generate`

CI auto-runs on push to master when `skills/**`, `commands/**`, or scripts change.

## Skill Anatomy

```yaml
---
name: skill-name           # Must match directory name
description: >-            # 1-1024 chars, front-loaded use case
  What this skill does.
metadata:
  version: "1.0.0"         # Semver string
  tags: "tag1, tag2"       # Comma-separated string (NOT list)
  author: "author-name"
---

# Skill Title

[Imperative, platform-neutral instructions...]
```

Required: `name`, `description`, `SKILL.md`, `plugin.json`
Optional: `license`, `compatibility`, `when_to_use`, `allowed-tools`, `model`, `context`

## Bundle Structure

13 bundles: `ai-agents`, `backend`, `dev-loop`, `dev-workflow`, `frontend`, `github`, `infrastructure`, `payments`, `planning`, `security`, `session`, `testing`, `workspace`

Each bundle = curated subset of skills for a domain. Defined in `scripts/plugin-categories.json`.

## Validation Pipeline

1. **Pre-commit hook** (`.husky/`): runs `validate-changed-skills.sh` on modified skills
2. **Local full validation**: `bun run validate` → `validate-skill-sync.sh`
3. **Lint**: `bun run lint` (markdownlint, Biome, shellcheck)
4. **CI**: GitHub Actions validates, audits, then regenerates bundles + marketplace on master push
