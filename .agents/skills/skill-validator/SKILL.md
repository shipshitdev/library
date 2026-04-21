---
name: skill-validator
description: |
  Validate SKILL.md files against the Agent Skills spec and Claude Code extensions.
  Run on new or modified skills before committing.
metadata:
  version: "1.0.0"
  tags: "validation, skills, spec-compliance, quality"
---

# Skill Validator

Validate SKILL.md files against the Agent Skills specification and Claude Code extensions.

## When to Run

- After creating a new skill
- After modifying a skill's SKILL.md frontmatter
- Before committing skill changes
- During periodic repo audits

## Validation Rules

### Required Fields (Agent Skills Spec)

Every SKILL.md must have YAML frontmatter with:

- `name` — kebab-case, matches directory name
- `description` — 1-3 sentences, under 1024 chars, starts with verb or domain noun

### Metadata Block

`version` and `tags` must be inside `metadata:`, never top-level:

```yaml
# CORRECT
metadata:
  version: "1.0.0"
  tags: "react, performance, optimization"

# WRONG — top-level version
version: 1.0.0

# WRONG — tags as YAML list
metadata:
  tags:
    - react
    - performance
```

### Forbidden Fields

These are not part of any spec:

- `auto_activate` / `auto_trigger` — removed in 2026-04 migration
- `risk` — not in Agent Skills or Claude Code specs

### Claude Code Extensions (Optional)

Valid extension fields:

| Field | Purpose |
|-------|---------|
| `when_to_use` | Trigger phrases for auto-activation |
| `disable-model-invocation` | Prevent auto-triggering (for destructive skills) |
| `user-invocable` | Slash command name |
| `allowed-tools` | Pre-approved tool patterns |
| `model` | Model override |
| `effort` | Effort level |
| `context` | `fork` for subagent isolation |

### Content Rules

- No hardcoded `/workspace/` paths
- No tool names in instructions (say "search for" not "use Grep")
- Imperative/infinitive style ("Configure X" not "You should configure X")
- Code blocks use real backtick fences, not escaped `\`\`\``

## Validation Process

1. Read the SKILL.md frontmatter
2. Check `name` matches parent directory name
3. Check `description` exists and is under 1024 chars
4. Check `version`/`tags` are NOT top-level (must be inside `metadata:`)
5. Check for forbidden fields (`auto_activate`, `auto_trigger`, `risk`)
6. Check for escaped backtick fences in content
7. Check for hardcoded paths (`/workspace/`, project-specific paths)
8. Run `bunx markdownlint-cli` on the file
9. Run `./scripts/validate-skill-sync.sh` for cross-validation

## Quick Validation Command

```bash
# Single skill
bunx markdownlint-cli skills/<name>/SKILL.md skills/<name>/references/*.md

# All skills
bunx markdownlint-cli --ignore bundles --ignore dist "**/*.md"

# Sync validation
./scripts/validate-skill-sync.sh
```
