---
name: session-documenter
description: "Session documentation workflow."
metadata:
  version: "1.0.0"
  tags: session, documentation, workflow, productivity
---

# Session Documenter Skill

Document work, decisions, and context with explicit commands.

## Contract

Inputs:

- Current session context
- Files changed, decisions made, blockers, and next steps
- Optional task or PRD references

Outputs:

- Appended session entry in `.agents/SESSIONS/YYYY-MM-DD.md`
- Related summary/task updates when needed

Creates/Modifies:

- `.agents/SESSIONS/` daily session file
- `.agents/memory/*.md` when a decision changes durable project context (architecture, deployment, migrations, gotchas)

External Side Effects:

- None

Confirmation Required:

- Before rewriting existing session history
- Before promoting session notes into permanent rules or skills

Delegates To:

- `rules-capture` for reusable preferences discovered during the session
- `skill-capture` for reusable workflows discovered during the session
- `session-end` for wrap-up flow

## Commands

| Command | Action |
|---------|--------|
| `/start` | Begin new session - creates/appends to today's file, loads context |
| `/end` | Finalize session - writes entry with all tracked work, updates related files |

## How It Works

1. **`/start`** - Creates `.agents/SESSIONS/YYYY-MM-DD.md` if missing, or loads existing context
2. **During session** - You tell me what to track: decisions, files changed, mistakes
3. **`/end`** - I write the full session entry with flowcharts, decisions, next steps

## Critical Rules

### Session File Naming (ONE FILE PER DAY)

```
✅ CORRECT: .agents/SESSIONS/2025-11-15.md
❌ WRONG:   .agents/SESSIONS/2025-11-15-feature-name.md
```

Multiple sessions same day → Same file, Session 1, Session 2, etc.

### Flowcharts (MANDATORY for features)

Include flowchart for:

- New features
- Feature modifications
- Multi-component bug fixes

## Session Entry Structure

1. **Session number and title**
2. **System flow diagram** (mermaid or text)
3. **Affected components** (frontend, backend, data, external)
4. **What was done** (task checklist)
5. **Key decisions** (with rationale)
6. **Files changed**
7. **Mistakes and fixes**
8. **Next steps**

## Related Files to Update

- `.agents/memory/*.md` — when a decision changes durable repo context
  (architecture, deployment, migrations, gotchas). Bump the file's
  `last_verified` date when you touch it.

## References

- [Full guide: Phases, automation, validation, examples](references/full-guide.md)
