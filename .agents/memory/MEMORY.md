# Skills Repo Memory

last_verified: 2026-04-21

## What This Repo Is

Public skills library at `shipshitdev/skills`. 250+ AI agent skills installable via `npx skills add shipshitdev/skills --skill <name>`. Works with Claude Code, Codex, Cursor, OpenClaw, Gemini.

## Architecture Decisions

### Single-Source Skills (2026-02-04)

One `skills/` directory at root. No per-platform copies (`.claude/skills/`, `.codex/skills/`). Platform-neutral writing: no tool names, imperative style.

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
| Keep copywriter + copywriting separate | copywriter = brand-aware persona, copywriting = guardrailed landing page copy |
| Merge clean-code + code-refactoring-refactor-clean → refactor-code | refactor-code is best-developed; others are weaker duplicates |
| Keep all 5 security skills | Distinct: expert persona, audit workflow, API-specific, backend impl, frontend impl |
| Keep react-patterns + react-refactor + react-component-performance | Cleanly separated by concern |
| Keep all expo-*/resend-*/static-analysis-* families | Non-overlapping topics |

### Nested Directory Cleanup (2026-04-21)

Removed 34 orphaned `skills/<name>/<name>/` nested duplicates. Root cause: old structure was `skills/<name>/<name>/SKILL.md`, flattened to `skills/<name>/SKILL.md` without cleanup.

## Known Issues

- `prompt-engineer` has hardcoded project paths (`packages/models/content/prompt*.ts`) — needs scrubbing
- `skill-capture` Phase 3 template teaches wrong frontmatter (top-level `version`, list-style `tags`)
- 3 meta-skills have `metadata.tags` as YAML lists instead of strings

## Key Files

- `.agents/SYSTEM/SKILL-STANDARDS.md` — authoritative spec doc
- `.agents/SYSTEM/SKILL-MANAGEMENT.md` — workflow guide
- `scripts/validate-skill-sync.sh` — validation script
- `scripts/generate-manifest.js` — manifest generation
- `scripts/generate-plugin.js` — plugin.json generation
