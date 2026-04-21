# Repository Architecture

last_verified: 2026-04-21

## Directory Map

```
skills-repo/
├── skills/                          # 216 skills (source of truth)
│   └── <skill-name>/
│       ├── SKILL.md                 # Skill definition (frontmatter + body)
│       └── plugin.json              # Claude Code plugin manifest (generated)
│
├── commands/                        # 26 slash commands (.md files, flat)
│   └── <command-name>.md
│
├── bundles/                         # 14 themed bundles (generated + curated)
│   └── <bundle-name>/
│       ├── plugin.json              # Bundle manifest
│       └── skills/                  # Symlinks or copies of bundled skills
│
├── plugins/                         # GENERATED — gitignored
│   ├── bundles/@agenticdev/         # 14 bundle packages
│   └── individual/@agenticdev/      # 245 individual packages
│
├── scripts/                         # Build, validate, generate tooling
│   ├── generate-bundle.js           # Bundle generation
│   ├── generate-manifest.js         # plugin.json from SKILL.md frontmatter
│   ├── generate-plugin.js           # Full plugin package generation
│   ├── generate-marketplace-*.js    # Marketplace catalog generation
│   ├── sync-marketplace.js          # Full sync pipeline
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
│   ├── SESSIONS/                    # Session logs (gitignored)
│   └── SYSTEM/                      # Project docs
│       ├── ARCHITECTURE.md          # .agents/ folder structure
│       ├── AI-DEV-LOOP.md           # /loop workflow
│       ├── SKILL-STANDARDS.md       # Skill authoring spec
│       ├── SKILL-MANAGEMENT.md      # Sync workflow
│       └── PLATFORM-ADAPTATIONS.md  # Claude vs Codex differences
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
skills/<name>/SKILL.md    ──→  scripts/generate-manifest.js   ──→  plugin.json (per skill)
                          ──→  scripts/generate-plugin.js      ──→  plugins/individual/
                          ──→  scripts/generate-bundle.js      ──→  bundles/<name>/
                          ──→  scripts/generate-marketplace-*  ──→  .claude-plugin/marketplace.json
```

All generation triggered by: `bun run marketplace:generate` or `bun run sync:marketplace`

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

14 bundles: `ai-agents`, `backend`, `branding`, `content`, `frontend`, `github`, `infrastructure`, `payments`, `planning`, `sales`, `session`, `startup`, `testing`, `workspace`

Each bundle = curated subset of skills for a domain. Defined in `scripts/plugin-categories.json`.

## Validation Pipeline

1. **Pre-commit hook** (`.husky/`): runs `validate-changed-skills.sh` on modified skills
2. **Local full validation**: `bun run validate` → `validate-skill-sync.sh`
3. **Lint**: `bun run lint` (markdownlint), biome handles JSON
4. **CI**: GitHub Actions regenerates bundles + marketplace on master push
