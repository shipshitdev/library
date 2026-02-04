# CRITICAL: Never Do This

**Purpose:** Quick reference for violations that break builds, lose data, or violate architecture.
**Read this FIRST before making ANY changes.**
**Last Updated:** {{DATE}}

---

## File Management

### Never Delete Required Files

These files MUST exist at project root:

- `AGENTS.md`
- `CLAUDE.md`
- `CODEX.md`
- `README.md`

### Never Create Root-Level .md Files

Only these 4 `.md` files allowed at project root:

1. `AGENTS.md`
2. `CLAUDE.md`
3. `CODEX.md`
4. `README.md`

Everything else goes in `.agents/`.

---

## Session Files

### One File Per Day

**Correct:**

```
.agents/SESSIONS/2025-01-15.md
```

**Wrong:**

```
.agents/SESSIONS/2025-01-15-feature.md  ❌
.agents/SESSIONS/FEATURE-2025-01-15.md  ❌
```

Multiple sessions same day → Same file, Session 1, Session 2, etc.

---

## Git

### Never Commit Without Approval

- Don't run `git commit` unless explicitly asked
- Don't run `git push` unless explicitly asked
- Make changes, show diff, wait for approval

### Never Force Push to Main

- No `git push --force` to main/master
- No `git reset --hard` on shared branches

---

## Coding

### Never Use `any` Type

```typescript
// Wrong
function process(data: any) { }

// Correct
function process(data: UserData) { }
```

### Never Skip Error Handling

```typescript
// Wrong
const result = await operation();

// Correct
try {
  const result = await operation();
} catch (error) {
  logger.error('Operation failed', error);
  throw error;
}
```

### Never Use console.log

Use a logging service instead.

---

## Project-Specific Rules

<!-- Add your project-specific "never do" rules below -->

---

## Pre-Code Checklist

Before writing ANY code:

- [ ] Read this file
- [ ] Check `../RULES.md` for patterns
- [ ] Search for similar implementations
- [ ] Understand existing code before modifying

---

## If You Violate These Rules

1. **Acknowledge** - Don't hide it
2. **Fix properly** - No workarounds
3. **Document** - Add to session file
4. **Learn** - Update this file if needed

---

**5 minutes reading this = hours saved debugging later.**
