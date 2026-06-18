# Start: Bootstrap Session with Critical Context

Load all critical context at the start of each session or after `/clear`.

## Workflow

### 1. Read Project Memory

Scan `.agents/memory/` to load durable project context. Each file covers one topic and carries a `last_verified` date — skip files older than 30 days until re-verified.

```bash
ls .agents/memory/
```

Read the files most relevant to today's work. Rules and preferences are already loaded from CLAUDE.md (repo-level) and the global `~/.claude/CLAUDE.md`; no separate preferences file needed.

### 2. Read Today's Session File

Read today's session to understand what was already done before `/clear`:

```bash
cat .agents/sessions/$(date +%Y-%m-%d).md
```

If the file exists, this shows:

- What tasks were completed earlier today
- What decisions were made
- What files were changed
- What patterns were used

If the file doesn't exist yet, this is a fresh session day.

### 3. Activate Session Documenter (Claude Code only)

The `session-documenter` skill will automatically activate and track:

- All tasks completed
- Decisions made with rationale
- Files created/modified/deleted
- Patterns established
- Mistakes and fixes

Documentation is written to `.agents/sessions/YYYY-MM-DD.md` after each task completion.

**No manual action required** - this happens automatically.

**CRITICAL:** When user types `/clear`, IMMEDIATELY use `session-documenter` skill BEFORE clearing to save all context.

### 4. Display Open Issues

Show the current task backlog from GitHub Issues:

```bash
gh issue list --state open
```

Display issues in two categories if labeled:

1. **Blocking** - Issues marked as blocking or critical
2. **Ready** - Issues ready for implementation

### 5. Confirmation

After reading memory files and displaying issues, provide a brief confirmation that you've loaded:

- Project memory context loaded
- Today's session context loaded (if exists)
- Ready to follow codebase-specific patterns
- Quality-first approach active
- Session documenter active (Claude Code)
- Open issues displayed

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
- Checking what was done earlier today
- Displaying open work from GitHub Issues
- Preventing repeated mistakes from previous sessions

## What Gets Loaded

1. **`.agents/memory/*.md`**: Durable project facts (architecture, deployment, migrations, gotchas)
2. **Today's session file** (`.agents/sessions/YYYY-MM-DD.md`):
   - What was done earlier today (before /clear)
   - Context continuity across /clear boundaries

## Output Format

Simple confirmation checklist:

- ✅ Project memory loaded
- ✅ Today's session context loaded (if exists)
- ✅ Session documenter active (Claude Code)

**Open Issues:**

- 🚨 Blocking (X)
- 📋 Ready to implement (X)

Ready for tasks
