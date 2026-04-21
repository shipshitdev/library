# Do and Don't — Skills Repo

last_verified: 2026-04-21

## DO

### Skills

- DO put every skill in `skills/<skill-name>/SKILL.md` — one directory per skill
- DO include `plugin.json` alongside every `SKILL.md`
- DO match `name:` frontmatter to directory name exactly
- DO keep `description:` between 1-1024 chars, front-load use case
- DO put `version` and `tags` inside `metadata:` block as strings
- DO write platform-neutral instructions — no "use Claude" or "use Cursor"
- DO write imperative style — "Analyze the code" not "You should analyze"
- DO keep SKILL.md under 500 lines
- DO run `bun run validate` after adding/modifying skills
- DO check `.agents/SYSTEM/SKILL-STANDARDS.md` for authoritative spec

### Commands

- DO put commands as flat `.md` files in `commands/` — no subdirectories
- DO follow same frontmatter conventions as skills

### Generation

- DO run `bun run marketplace:generate` after changing skills/commands
- DO let CI handle regeneration on master — don't commit generated `plugins/`
- DO commit `bundles/` and `.claude-plugin/marketplace.json` — CI generates these

### Git

- DO use conventional commits: `feat:`, `fix:`, `refactor:`, `chore:`, `docs:`
- DO let pre-commit hooks run (markdownlint, biome, validate-changed-skills)
- DO use Bun for everything: `bun run`, `bun add`, `bunx`

### Quality

- DO scrub hardcoded paths from imported skills before committing
- DO check for duplicate/overlapping skills before adding new ones
- DO verify frontmatter with validation script, not just visual inspection

## DON'T

### Structure

- DON'T create per-platform copies (`.claude/skills/`, `.codex/skills/`) — single source only
- DON'T nest skill directories (`skills/foo/foo/SKILL.md`) — flat structure
- DON'T put skills in bundles directly — bundles reference skills from `skills/`
- DON'T manually edit `plugins/` — it's generated and gitignored
- DON'T create `.md` docs unless explicitly asked — no README bloat

### Frontmatter

- DON'T put `version` or `tags` at top-level frontmatter — goes inside `metadata:`
- DON'T use YAML list syntax for tags — use comma-separated string
- DON'T use `any` or skip typing in JS scripts
- DON'T reference specific AI tools/platforms in skill body text

### Git / CI

- DON'T use npm/yarn/pnpm — Bun only
- DON'T commit `node_modules/`, `plugins/`, `.agents/SESSIONS/`
- DON'T skip pre-commit hooks (`--no-verify`)
- DON'T force push to master
- DON'T commit `.env` files or secrets

### Common Mistakes

- DON'T run `npx skills add ~/.agents/skills` — treats install target as source, wipes content
- DON'T run `bun test` with no filter locally — CI only. Use `bun run test --filter=<name>`
- DON'T add error handling for impossible scenarios in generation scripts
- DON'T build abstractions for one-off script operations
- DON'T import external skills without checking for hardcoded paths, project-specific references

## WATCH OUT FOR

- `prompt-engineer` skill has hardcoded project paths — needs cleanup
- `skill-capture` Phase 3 teaches wrong frontmatter format
- 3 meta-skills have `metadata.tags` as YAML lists instead of strings
- Orphaned nested directories can appear after structure migrations — check with `find skills -mindepth 3`
- Bundle `plugin.json` files are curated, not generated — treat as source
