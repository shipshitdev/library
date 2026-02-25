# Canonical Rule Ownership

Each rule should live in ONE file. Other files may reference it but should not repeat it.

## Ownership Map

| Rule | Canonical Home | May Reference | Runtime Enforcement |
|------|---------------|---------------|---------------------|
| No `any` types | `CLAUDE.md` (cross-repo rules) | Per-repo CLAUDE.md (brief mention OK) | hooks.json |
| No `console.log` | `CLAUDE.md` (cross-repo rules) | Per-repo CLAUDE.md (brief mention OK) | — |
| Path aliases over relative imports | `CLAUDE.md` (cross-repo rules) | — | — |
| Conventional commits | `CLAUDE.md` (cross-repo rules) | — | — |
| Never commit secrets | `CLAUDE.md` (cross-repo rules) | — | — |
| Import order (detailed) | `CLAUDE_RULES.md` (global rules) | — | — |
| AbortController in useEffect | `CLAUDE_RULES.md` (global rules) | CRITICAL-NEVER-DO.md (one-liner) | — |
| Session file naming | hooks.json (runtime) | CRITICAL-NEVER-DO.md (one mention) | hooks.json |
| Multi-tenancy (org filter) | `CRITICAL-NEVER-DO.md` | Per-repo CLAUDE.md (brief mention OK) | — |
| Soft delete (isDeleted) | `CRITICAL-NEVER-DO.md` | — | — |
| Serializer location | `CRITICAL-NEVER-DO.md` | Per-repo CLAUDE.md (brief mention OK) | — |
| No inline interfaces | `CRITICAL-NEVER-DO.md` | — | — |
| Naming conventions | `RULES.md` (.agents/SYSTEM/critical/) | — | — |
| Function declaration style | `RULES.md` (.agents/SYSTEM/critical/) | — | — |
| Testing standards | `RULES.md` (.agents/SYSTEM/critical/) | — | — |
| Performance patterns | `RULES.md` (.agents/SYSTEM/critical/) | — | — |

## File Roles

| File | Role | Contains |
|------|------|----------|
| `CLAUDE.md` (root) | Workspace overview | Cross-repo "do this" rules, repo table, agent behavior |
| `CLAUDE.md` (per-repo) | Repo-specific guide | Tech stack, commands, repo-specific rules, architecture |
| `CLAUDE_RULES.md` (global) | Behavioral preferences | Tool usage, code standards detail, session management |
| `CRITICAL-NEVER-DO.md` | Violations only | "NEVER do X" rules with examples of what breaks |
| `RULES.md` (.agents/) | Extended standards | Naming, functions, testing — details beyond CLAUDE.md |
| `CODEX.md` | Codex-specific | Sandbox constraints, key entry points, no-network notes |
| `AGENTS.md` | Generic agent nav | Entry points for any AI agent (Cursor, Copilot, etc.) |
| `.cursorrules` | Cursor-specific | Project navigation, reading order, .agents/ structure |
| `hooks.json` | Runtime enforcement | Catches violations at tool-call time (session files, any types, tests) |
| `settings.json` | Permission control | Denied skills, MCP config |

## Referencing vs Repeating

**Good reference** (brief, points to canonical):

```markdown
No `any` types — see CLAUDE.md cross-repo rules for details.
```

**Bad repetition** (full rule restated):

```markdown
No `any` types — use `unknown` or proper interfaces. Define all interfaces in `packages/interfaces/` or `packages/props/`.
```

The second version will drift when the canonical source gets updated.
