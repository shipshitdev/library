# Session Quick Start

**Read this at the START of every session.**

---

## Before You Start

1. **Read critical rules:**
   - `../critical/CRITICAL-NEVER-DO.md`

2. **Check today's session file:**
   - `../../SESSIONS/{{DATE}}.md` (if exists, read it first)

3. **Review recent context:**
   - Last 2-3 session files for context

---

## During Session

### Track Everything

- Decisions made and why
- Files changed
- Patterns used
- Mistakes and fixes

### Follow Patterns

- Check `../RULES.md` for coding standards
- Search for similar implementations before writing new code
- Use existing utilities and helpers

### Ask When Unsure

- Security implications
- Breaking changes
- Architecture decisions

---

## After Session

### Document in Session File

Add entry to `../../SESSIONS/YYYY-MM-DD.md`:

```markdown
## Session N: Brief Description

**Duration:** ~X hours
**Status:** Complete / In Progress

**What was done:**
- Task 1
- Task 2

**Files changed:**
- `path/to/file.ts` - what changed

**Decisions:**
- Decision with rationale

**Next steps:**
- [ ] Next task
```

### Update Task Status

Mark completed tasks in `../../TASKS/`

---

## Session File Rules

- **ONE file per day:** `YYYY-MM-DD.md`
- Multiple sessions same day = Session 1, Session 2, etc. in SAME file
- Never create `YYYY-MM-DD-description.md` (wrong!)

---

## Quick Reference

| What | Where |
|------|-------|
| Coding rules | `../RULES.md` |
| Critical violations | `../critical/CRITICAL-NEVER-DO.md` |
| Architecture | `../ARCHITECTURE.md` |
| Tasks | `../../TASKS/` |
| Session template | `../../SESSIONS/TEMPLATE.md` |

---

**Remember:** Document as you go, not at the end.
