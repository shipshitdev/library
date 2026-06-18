# Skills Repo Memory

last_verified: 2026-06-18

## What This Repo Is

Public skills library at `shipshitdev/skills`. 140 skills, 11 commands, 13 bundles. Installable via `npx skills add shipshitdev/skills --skill <name>`. Works with Claude Code, Codex, Cursor, OpenClaw, Gemini.

Published through committed marketplace bundles in `bundles/` and the generated `.claude-plugin/marketplace.json` catalog. The old generated `plugins/` package tree is retired.

## Repo Identity

- **Name:** ship-shit-dev-library
- **Owner:** Vincent (decod3rs) — solo founder, zero-code workflow
- **License:** MIT
- **Runtime:** Bun (never npm/yarn/pnpm)
- **Linting:** markdownlint (markdown), biome (JSON/JS), shellcheck (bash)
- **CI:** GitHub Actions on push to master — regenerates bundles + marketplace

## Numbers (snapshot 2026-06-18)

| Asset | Count | Location |
|-------|-------|----------|
| Skills | 140 | `skills/<name>/SKILL.md` |
| Commands | 11 | `commands/<name>.md` |
| Bundles | 13 | `bundles/<bundle>/plugin.json` |
| Scripts | 15 | `scripts/` |
| Prompts | 2 | `prompts/` |

## Architecture Decisions

### Single-Source Skills (2026-02-04)

One `skills/` directory at root. No per-platform copies. Platform-neutral writing: no tool names, imperative style.

### Agent Skills Spec Compliance (2026-04-21)

Follow agentskills.io/specification as base. Claude Code extensions (`when_to_use`, `disable-model-invocation`, `allowed-tools`, etc.) added on top. `version`/`tags` go inside `metadata:` block as strings, not top-level. See `.agents/SYSTEM/SKILL-STANDARDS.md`.

### External Skills Imported (2026-04-21)

All referenced external repos now internal — no external dependencies:

| Source | Skills Imported |
|--------|----------------|
| coreyhaines31/marketingskills | 14 CRO/SEO/marketing skills |
| vercel-labs/agent-skills | vercel-react-best-practices, web-design-guidelines |
| trailofbits/skills | 10 security audit skills |
| expo/skills | 10 expo-* mobile skills |
| resend/resend-skills + email-best-practices | 5 resend-* email skills |
| sickn33/antigravity-awesome-skills | 20 cherry-picked skills (JS, NestJS, Prisma, security, marketing, etc.) |

### Consolidation Decisions (2026-04-21)

| Decision | Rationale |
|----------|-----------|
| Move content/GTM skills out of Shipshit | Shipshit is dev-workflow focused; content and GTM strategy skills live in Genfeed |
| Merge clean-code + code-refactoring-refactor-clean → refactor-code | refactor-code is best-developed; others are weaker duplicates |
| Keep all 5 security skills | Distinct: expert persona, audit workflow, API-specific, backend impl, frontend impl |
| Keep react-patterns + react-refactor + react-component-performance | Cleanly separated by concern |
| Keep all expo-*/resend-*/static-analysis-* families | Non-overlapping topics |

## Known Issues

None currently tracked.

## Key Files

- `.agents/SYSTEM/SKILL-STANDARDS.md` — authoritative spec doc
- `.agents/SYSTEM/SKILL-MANAGEMENT.md` — workflow guide
- `scripts/validate-skill-sync.sh` — validation script
- `scripts/generate-marketplace-bundles.js` — bundle snapshot generation
- `scripts/generate-marketplace-json.js` — marketplace catalog generation
- `.claude-plugin/marketplace.json` — full marketplace catalog (generated)
- `.github/workflows/generate-bundles.yml` — CI pipeline
