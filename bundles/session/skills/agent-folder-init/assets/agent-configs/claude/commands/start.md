# Start: Bootstrap Session with Critical Context

Load project context at the start of each session or after `/clear`.

## Workflow

### 1. Read Memory Files

Scan `.agents/memory/` for durable project facts:

```bash
ls .agents/memory/ 2>/dev/null && for f in .agents/memory/*.md; do echo "=== $f ==="; cat "$f"; echo; done
```

These files are the source of truth for architecture, deployment, migrations, gotchas, and any other project-specific context. Each file carries a `last_verified` date — treat entries older than 30 days as unverified.

### 2. Read Today's Session File

Read today's session to understand what was already done before `/clear`:

```bash
TODAY=$(date +%Y-%m-%d)
cat .agents/sessions/$TODAY.md 2>/dev/null || echo "No session file for today yet"
```

If the file exists, this shows:

- What tasks were completed earlier today
- What decisions were made
- What files were changed
- What patterns were used

If the file doesn't exist yet, this is a fresh session day.

### 3. Activate Session Documenter (if available)

The `session-documenter` skill will automatically activate and track:

- All tasks completed
- Decisions made with rationale
- Files created/modified/deleted
- Patterns established
- Mistakes and fixes

Documentation is written to `.agents/sessions/YYYY-MM-DD.md` after each task completion.

**No manual action required** - this happens automatically.

**CRITICAL:** When user types `/clear`, IMMEDIATELY use `session-documenter` skill BEFORE clearing to save all context.

### 4. Show Open GitHub Issues (Backlog)

Display open issues to surface pending work:

```bash
gh issue list --state open --limit 20
```

### 5. Confirmation

After loading context, provide a brief confirmation:

- Memory files loaded (count and topics)
- Today's session context loaded (if exists)
- Ready to follow codebase-specific patterns
- Session documenter active (if available)
- Open issues count

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

- Loading project-specific facts from `.agents/memory/`
- Surfacing today's prior work to avoid duplication
- Displaying the open issue backlog

## What Gets Loaded

1. **`.agents/memory/*.md`** — durable project context (architecture, deployment, migrations, gotchas, entities)
2. **Today's session file** (`.agents/sessions/YYYY-MM-DD.md`) — what was done earlier today before `/clear`
3. **GitHub Issues** — open backlog via `gh issue list`

Rules and preferences are loaded automatically by the harness via CLAUDE.md — no manual step needed.

## Output Format

Simple confirmation checklist:

- ✅ Memory files loaded (N topics)
- ✅ Today's session context loaded (if exists)
- ✅ Session documenter active (if available)

**📋 Open Issues:** N open

Ready for tasks

---

**Created:** 2025-01-01
**Purpose:** Universal session bootstrap command for any project
