# Skills Repo — Agent Instructions

This is the shipshitdev/skills repo: 216 AI agent skills for Claude Code and Codex.

## Repo Structure

- `skills/` — All public skills (SKILL.md + optional references/, scripts/, plugin.json)
- `commands/` — Workflow commands (.md files)
- `bundles/` — Generated marketplace bundles (do not edit manually)
- `.agents/` — Repo management (memory, meta-skills, system docs)
- `scripts/` — Validation, generation, migration scripts

## Rules

- Follow the Agent Skills spec: `.agents/SYSTEM/SKILL-STANDARDS.md`
- `version`/`tags` go inside `metadata:` block as quoted strings, never top-level
- No `auto_activate`, `auto_trigger`, or `risk` fields
- Skills are platform-neutral: no tool names, imperative style
- Run `bunx markdownlint-cli --ignore bundles --ignore dist --ignore plugins "**/*.md"` before committing
- Run `./scripts/validate-skill-sync.sh` for cross-validation

## Code Standards

- TypeScript: no `any`, no `console.log`, interfaces in dedicated files
- Conventional commits: `fix:`, `feat:`, `refactor:`, `chore:`
- Never commit secrets (.env, API keys)
- Use `bun` as package manager, not npm/yarn

## Before Editing Skills

1. Read the SKILL.md you'll modify
2. Find 3+ similar skills to follow their patterns
3. Check `.agents/memory/MEMORY.md` for repo decisions
