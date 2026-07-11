# Canonical Rule Ownership

Each rule should live in ONE file. Other files may reference it but should not repeat it.

## Ownership Map

| Rule | Canonical Home | May Reference | Runtime Enforcement |
|------|---------------|---------------|---------------------|
| No `any` types | `AGENTS.md` (cross-agent rule) | Scoped AGENTS.md (brief mention OK) | hooks.json |
| No `console.log` | `AGENTS.md` (cross-agent rule) | Scoped AGENTS.md (brief mention OK) | — |
| Path aliases over relative imports | `AGENTS.md` (cross-agent rule) | — | — |
| Conventional commits | `AGENTS.md` (cross-agent rule) | — | — |
| Never commit secrets | `AGENTS.md` (cross-agent rule) | `.agents/memory/security.md` (detail) | hooks.json |
| Import order (detailed) | `.agents/memory/coding-standards.md` | AGENTS.md (brief mention OK) | — |
| AbortController in useEffect | `.agents/memory/coding-standards.md` | AGENTS.md (brief mention OK) | — |
| Session file naming | hooks.json (runtime) | AGENTS.md (one mention) | hooks.json |
| Multi-tenancy (org filter) | `.agents/memory/security.md` | AGENTS.md (brief mention OK) | — |
| Soft delete (isDeleted) | `.agents/memory/data-guardrails.md` | AGENTS.md (brief mention OK) | — |
| Serializer location | `.agents/memory/architecture.md` | AGENTS.md (brief mention OK) | — |
| No inline interfaces | `.agents/memory/coding-standards.md` | AGENTS.md (brief mention OK) | — |
| Naming conventions | `AGENTS.md` (repo-level) | `.agents/memory/coding-standards.md` (detail) | — |
| Function declaration style | `AGENTS.md` (repo-level) | `.agents/memory/coding-standards.md` (detail) | — |
| Testing standards | `AGENTS.md` (repo-level) | `.agents/memory/testing.md` (detail) | — |
| Performance patterns | `AGENTS.md` (repo-level) | `.agents/memory/performance.md` (detail) | — |

## File Roles

| File | Role | Contains |
|------|------|----------|
| `AGENTS.md` (root or scoped) | Native shared instructions | Workspace overview, commands, repo rules, navigation |
| `AGENTS.override.md` | Native scoped override | Intentional replacement guidance for one subtree |
| `CLAUDE.md` | Claude-specific additions | Claude-only behavior that does not belong in shared instructions |
| `.agents/memory/*.md` | Durable project facts | Architecture, naming conventions, gotchas, and extended standards linked from AGENTS.md |
| `.cursorrules` | Cursor-specific | Project navigation, reading order, .agents/ structure |
| `hooks.json` | Runtime enforcement | Catches violations at tool-call time (session files, any types, tests) |
| Effective `.codex/config.toml` | Codex runtime configuration | Fallback instruction filenames, approvals, sandbox and network policy |
| `settings.json` | Claude permission control | Denied skills, MCP config |

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
