# Cross-Project Rules

**Purpose:** Rules that apply across all projects in this workspace.
**Last Updated:** {{DATE}}

---

## AI Entry Files

Every project MUST have these files at its root:

- `AGENTS.md` - AI agent entry point
- `CLAUDE.md` - Claude-specific entry
- `CODEX.md` - Codex-specific entry

These are NOT duplicates - they're required for AI tooling.

---

## Documentation Structure

Every project follows:

```
[project]/
├── AGENTS.md
├── CLAUDE.md
├── CODEX.md
├── README.md
└── .agents/
    ├── README.md
    ├── SYSTEM/
    ├── TASKS/
    └── SESSIONS/
```

---

## Session Files

- **One file per day:** `YYYY-MM-DD.md`
- **Location:** `.agents/SESSIONS/`
- Multiple sessions = Session 1, Session 2 in SAME file

---

## Naming Conventions

### Directories

- Top-level `.agents/` dirs: ALL-CAPS (`SYSTEM/`, `TASKS/`)
- Subdirectories: lowercase with hyphens (`user-management/`)

### Files

- Critical files: ALL-CAPS (`README.md`, `RULES.md`)
- Regular files: kebab-case (`api-development.md`)

---

## Import Rules

- Use path aliases (`@components/`, `@services/`)
- No relative imports for shared code
- No absolute paths starting with `/`

---

## Type Rules

- No `any` types
- No inline interface definitions
- Define types in dedicated files

---

## Error Handling

- All async operations need try/catch
- Use logging service, not console.log
- Provide user-friendly error messages

---

## Testing

- Tests run in CI/CD only (not locally unless asked)
- Write tests for business logic
- Mock external dependencies

---

## Git Rules

- Don't commit without explicit request
- Don't push without explicit request
- Use conventional commit messages

---

## Hierarchy of Rules

1. **This file** - Applies everywhere
2. **Project RULES.md** - Project-specific overrides
3. **Task-specific** - Can override if documented

---

## Never Delete

- `AGENTS.md`, `CLAUDE.md`, `CODEX.md` in any project root
- `.agents/` folders
- `README.md` files
