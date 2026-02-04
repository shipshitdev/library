# Start: Bootstrap Session with Critical Context

Load all critical preferences and instructions at the start of each session or after `/clear`.

## Workflow

### 1. Read Session Quick Start (if exists)

Check for project entry point documentation:

```bash
cat .agents/SYSTEM/ai/SESSION-QUICK-START.md 2>/dev/null || cat .agents/SYSTEM/SESSION-QUICK-START.md 2>/dev/null || echo "No session quick start found"
```

This document will guide you to any other necessary documentation.

### 2. Read User Preferences (CRITICAL)

Read the user's non-negotiable preferences:

```bash
cat .agents/SYSTEM/ai/USER-PREFERENCES.md 2>/dev/null || cat .claude/rules/user-preferences.md 2>/dev/null || echo "No user preferences found"
```

This file contains:

- Critical rules (NEVER build/test locally, check recent sessions, follow codebase patterns)
- Quality standards
- Communication preferences
- Past corrections and lessons learned

### 3. Read Today's Session File

Read today's session to understand what was already done before `/clear`:

```bash
TODAY=$(date +%Y-%m-%d)
cat .agents/SESSIONS/$TODAY.md 2>/dev/null || echo "No session file for today yet"
```

If the file exists, this shows:

- What tasks were completed earlier today
- What decisions were made
- What files were changed
- What patterns were used

If the file doesn't exist yet, this is a fresh session day.

### 4. Activate Session Documenter (if available)

The `session-documenter` skill will automatically activate and track:

- All tasks completed
- Decisions made with rationale
- Files created/modified/deleted
- Patterns established
- Mistakes and fixes

Documentation is written to `.agents/SESSIONS/YYYY-MM-DD.md` after each task completion.

**No manual action required** - this happens automatically.

**CRITICAL:** When user types `/clear`, IMMEDIATELY use `session-documenter` skill BEFORE clearing to save all context.

### 5. Display Inbox Tasks (if exists)

Show the current inbox backlog:

```bash
cat .agents/TASKS/INBOX.md 2>/dev/null || echo "No inbox found"
```

Display inbox in two categories:

1. **Human QA (Blocking Production)** - Tasks requiring manual testing before production build
2. **Features to Prompt** - Tasks ready for AI implementation

### 6. Confirmation

After reading all files and displaying inbox, provide a brief confirmation that you've loaded:

- Critical rules understood (no background processes, no builds/tests, document before /clear)
- Today's session context loaded (if exists)
- Ready to follow codebase-specific patterns
- Quality-first approach active
- Session documenter active (if available)
- Inbox tasks displayed (if exists)

Keep confirmation concise (5-7 bullet points max).

## Usage

```bash
# After clearing conversation history
/clear
/start

# Or at the beginning of a new session
/start
```

## Purpose

This command ensures consistent behavior across sessions by:

- Loading user-specific preferences that override default behavior
- Preventing repeated mistakes from previous sessions
- Ensuring awareness of critical "never do" rules
- Maintaining quality standards

## What Gets Loaded

1. **SESSION-QUICK-START.md** (optional): Navigation guide to all documentation
2. **USER-PREFERENCES.md** (critical):
   - No background processes (foreground only)
   - No local builds/tests (CI/CD only)
   - Document before /clear (session-documenter skill)
   - Check `.agents/SESSIONS/` before implementing
   - Find and follow real codebase examples (not generic patterns)
   - Quality over speed
   - Session memory is critical
3. **Today's session file** (`.agents/SESSIONS/YYYY-MM-DD.md`):
   - What was done earlier today (before /clear)
   - Context continuity across /clear boundaries

## Output Format

Simple confirmation checklist:

- ✅ Session quick start loaded (if exists)
- ✅ User preferences understood
- ✅ Critical rules active (no background processes, no builds, document before /clear)
- ✅ Today's session context loaded (if exists)
- ✅ Session documenter active (if available)

**📥 Inbox:**

- 🚨 Human QA (X) - blocking production
- 📋 Features (X) - ready to prompt

Ready for tasks

---

**Created:** 2025-01-01
**Purpose:** Universal session bootstrap command for any project
