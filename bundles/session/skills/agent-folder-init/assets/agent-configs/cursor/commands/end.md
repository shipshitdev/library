# End - Document Session Before Clearing

**⚠️ CRITICAL: This command documents your session but does NOT clear the context.**

## What This Command Does

1. **Activates the `session-documenter` skill** to save all session context to `.agents/SESSIONS/YYYY-MM-DD.md`
2. **Tells you to manually run `/clear`** (Claude Code's built-in command) to clear the context

**Note:** `/end` only documents. You must manually run `/clear` (built-in) after `/end` completes to actually clear the conversation context.

## Workflow

### Step 1: Document Session Immediately

When user types `/end`, you MUST:

1. **Activate session-documenter skill:**

   ```
   Use the Skill tool to activate session-documenter
   ```

2. **Let it complete** - The skill will:
   - Document all tasks completed
   - Save decisions made with rationale
   - Record files created/modified/deleted
   - Note patterns established
   - Track mistakes and fixes
   - Write everything to `.agents/SESSIONS/YYYY-MM-DD.md`

3. **Confirm documentation saved:**

   ```
   ✅ Session documented to .agents/SESSIONS/YYYY-MM-DD.md
   ```

### Step 2: Remind User to Clear Manually

After documentation is complete, tell the user:

```
✅ Session documented successfully!

📋 NEXT STEP:
Run /clear (Claude Code's built-in command) to clear the conversation context.
Your session is safely preserved in .agents/SESSIONS/YYYY-MM-DD.md

Next time you run /start, it will load this documented session.
```

**IMPORTANT:** Tell the user to manually run `/clear` after `/end` completes. The `/end` command does NOT clear context automatically.

## Why This Matters

**WITHOUT documentation before /clear:**

- All context is lost forever
- Next `/start` has no idea what was done
- You repeat work or make conflicting changes
- User gets frustrated

**WITH documentation before /clear:**

- Context preserved in `.agents/SESSIONS/YYYY-MM-DD.md`
- Next `/start` reads the session file
- Continuity maintained across clear boundaries
- User can pick up exactly where they left off

## User Experience

**User types:** `/end`

**AI responds:**

```
🔄 Documenting session...

[session-documenter skill activates]

✅ Session documented to .agents/SESSIONS/2025-11-23.md

Session saved with:
- 3 tasks completed
- 5 files changed
- 2 key decisions documented

📋 NEXT STEP: Run /clear to clear the conversation context.
Your session is safely preserved and will be loaded when you run /start again.
```

**Then:** User manually types `/clear` to clear the conversation context using Claude Code's built-in command

**Next session:** User runs `/start` → reads `.agents/SESSIONS/2025-11-23.md` → knows everything that was done

## How This Works

**Technical details:**

1. Custom `/end` command (this file) triggers when user types `/end`
2. AI executes session documentation via `session-documenter` skill
3. Session data is saved to `.agents/SESSIONS/YYYY-MM-DD.md`
4. AI tells user to manually run `/clear` (Claude Code's built-in command)
5. User runs `/clear` to clear conversation context

**This is a TWO-STEP process:**

- `/end` = document session
- `/clear` = clear context (built-in Claude Code command)

## Important Notes

- **ONE FILE PER DAY:** Session documenter appends to `.agents/SESSIONS/YYYY-MM-DD.md`
- **Multiple /ends:** Each /end adds a new session to the same day's file
- **Automatic documentation:** Session documenter skill handles everything
- **Manual clear required:** User must run `/clear` after `/end` to clear context
- **Best practice:** Always run `/end` before `/clear` to preserve session history

## Related Commands

- `/start` - Loads preferences and today's session file after clearing
- `/docs-update` - Manual session documentation (fallback if skill fails)

---

## Troubleshooting

**If context doesn't clear after running /clear:**

1. Make sure you're using the built-in `/clear` command (not a custom command)
2. Try restarting Claude Code CLI if `/clear` doesn't work
3. Verify you're using Claude Code CLI (not a different tool)

**If you want to clear WITHOUT documentation:**

Simply run `/clear` directly without running `/end` first.

**WARNING:** Clearing without documentation means you lose all session context.
Best practice is to ALWAYS run `/end` before `/clear`.

---

**Created:** 2025-11-21
**Updated:** 2025-11-23
**Purpose:** Document session before clearing context manually with `/clear`

## Workflow Summary

```
/start               → Load preferences and session history
  ↓
[work on tasks]      → Make changes, complete tasks
  ↓
/end                 → Document session to .agents/SESSIONS/YYYY-MM-DD.md
  ↓
/clear               → Clear conversation context (built-in command)
  ↓
/start               → Begin new session with documented history
```
