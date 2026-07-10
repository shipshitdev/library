---
name: session-start
description: >-
  Loads critical project context and recent session history at the start of
  each session or after `/clear` — reads `.agents/memory/` source-of-truth
  files, surfaces open next steps from the latest session log, and activates
  the session-documenter. Triggers on: session start, `/clear`, "load context",
  "start session", or first message in a new agent session.
metadata:
  version: "1.1.1"
  tags: "session, workflow, context, productivity"
---

# Session Start

Load critical context and recent history at the start of each session or after `/clear`.

## Contract

Inputs:

- Project root
- Current date
- Existing `.agents/memory/` and `.agents/sessions/` files

Outputs:

- Loaded repo memory summary
- Today's session context (if any)
- Open next-steps surfaced from the latest session log

Creates/Modifies:

- No required writes
- May create today's session file only through `session-documenter`

External Side Effects:

- None

Confirmation Required:

- Before creating or rewriting session files when paths are ambiguous

Delegates To:

- `session-documenter` to track the active session
- `rules-capture` if startup reveals uncaptured preferences

## Workflow

### 1. Read Repo Memory (CRITICAL — source of truth)

Read the repo's memory files at `.agents/memory/`. These are the source of truth
for current project context: architecture, deployment state, migrations, known
gotchas, and operating decisions. Apply the staleness and temporary-file checks
defined in the global `CLAUDE.md` / `MEMORY.md` before citing any entry.

### 2. Read Today's Session File

Read today's session to understand what was already done before `/clear`:

Read today's session file at `.agents/sessions/YYYY-MM-DD.md` (where YYYY-MM-DD
is today's date).

If the file exists, it shows tasks completed, decisions made, files changed,
mistakes, and next steps. If it doesn't exist yet, this is a fresh session day.

### 3. Activate Session Documenter

Run the `session-documenter` skill to track work throughout the session.

### 4. Confirmation

After reading memory and the session file, provide a brief confirmation (5-7 bullet points max):

- Critical rules understood
- Repo memory loaded (flag any stale `last_verified` or `status: temporary` files)
- Today's session context loaded (if it exists)
- Session documenter active
- Open next-steps surfaced from the latest session log (if any)

## Related Skills

- **session-end** — Document session before clearing context
- **session-documenter** — Tracks work throughout the session
