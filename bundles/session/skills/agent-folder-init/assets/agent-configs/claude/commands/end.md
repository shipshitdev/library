# End - Document Session Before Clearing

**CRITICAL: This command documents your session but does NOT clear the context.**

## What This Command Does

1. **Activates the session-documenter skill** to save all session context to .agents/SESSIONS/YYYY-MM-DD.md
2. **Tells you to manually run /clear** (Claude Code built-in command) to clear the context

## Workflow

### Step 1: Document Session Immediately

When user types /end, activate session-documenter skill to:

- Document all tasks completed
- Save decisions made with rationale
- Record files created/modified/deleted
- Note patterns established
- Write everything to .agents/SESSIONS/YYYY-MM-DD.md

### Step 2: Remind User to Clear Manually

After documentation completes, tell user to run /clear manually.

## Important Notes

- ONE FILE PER DAY: Session documenter appends to .agents/SESSIONS/YYYY-MM-DD.md
- Multiple /ends: Each /end adds a new session to the same days file
- Manual clear required: User must run /clear after /end to clear context

## Workflow Summary

/start -> Load preferences and session history
[work] -> Make changes, complete tasks
/end   -> Document session to .agents/SESSIONS/YYYY-MM-DD.md
/clear -> Clear conversation context (built-in command)
/start -> Begin new session with documented history
