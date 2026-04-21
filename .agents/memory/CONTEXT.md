# Working Context — Skills Repo

last_verified: 2026-04-21

## You Are Working ON the Library

This is NOT a project that uses skills. You are editing/managing the skill library itself. Skills here get published to marketplace and installed by other users.

## Owner Context

- **Vincent** (decod3rs) — solo founder, zero-code workflow
- Vincent does NOT write code — AI writes all code, Vincent architects/reviews
- Cost-aware: use haiku for lookups, sonnet for work, opus for deep reasoning
- Direct communication — no fluff, no "would you like me to..."

## Tech Stack

| Tool | Purpose |
|------|---------|
| Bun | Package manager + script runner (never npm) |
| markdownlint | Markdown linting |
| biome | JSON/JS formatting + linting |
| shellcheck | Shell script linting |
| husky | Pre-commit hooks |
| GitHub Actions | CI — bundle regeneration on master push |

## Common Workflows

### Add New Skill

1. `mkdir skills/<skill-name>`
2. Create `skills/<skill-name>/SKILL.md` with spec-compliant frontmatter
3. Create `skills/<skill-name>/plugin.json`
4. Run `bun run validate`
5. Update README.md skill table
6. Commit — CI regenerates marketplace

### Validate All Skills

```bash
bun run validate
```

### Regenerate Marketplace

```bash
bun run marketplace:generate
```

### Check for Duplicates

```bash
bun run inventory
```

### Lint

```bash
bun run lint        # markdown
bun run lint:fix    # markdown auto-fix
bun run lint:sh     # shell scripts
```

## Script Quick Reference

| Script | Command |
|--------|---------|
| Full validation | `bun run validate` |
| Generate marketplace | `bun run marketplace:generate` |
| Sync marketplace | `bun run sync:marketplace` |
| Generate single plugin | `bun run generate:plugin` |
| Generate all plugins | `bun run generate:all` |
| Count skills/commands | `bun run count` |
| Check duplicate installs | `bun run inventory` |
| Clean duplicate installs | `bun run cleanup:global` |
| Update deps | `bun run deps:update` |

## File Authority

| File | Authority | Notes |
|------|-----------|-------|
| `skills/*/SKILL.md` | Source of truth | All skill content lives here |
| `skills/*/plugin.json` | Source (per-skill) | Must match SKILL.md frontmatter |
| `bundles/*/plugin.json` | Source (curated) | Manually maintained bundle definitions |
| `plugins/` | Generated | Gitignored, never edit |
| `.claude-plugin/marketplace.json` | Generated | Committed, CI-managed |
| `scripts/plugin-categories.json` | Source | Bundle → skills mapping |
| `.agents/SYSTEM/SKILL-STANDARDS.md` | Authoritative spec | Definitive frontmatter reference |

## Session Protocol

1. Check `.agents/SESSIONS/<today>.md` at start
2. Document before `/clear`: files changed, decisions, incomplete work
3. Save to `.agents/SESSIONS/YYYY-MM-DD.md`
4. Never save secrets to session files
