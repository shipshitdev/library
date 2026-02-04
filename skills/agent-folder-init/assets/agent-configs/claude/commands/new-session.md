# New Session - Create Session File

Create a new session entry for todays work.

## Usage

/new-session

## What This Command Does

1. Creates or appends to .agents/SESSIONS/YYYY-MM-DD.md
2. Adds a new session header with timestamp
3. Sets up structure for documenting work

## Session File Rules

### One File Per Day

CORRECT:

- .agents/SESSIONS/2025-01-15.md
- .agents/SESSIONS/2025-01-16.md

WRONG:

- .agents/SESSIONS/2025-01-15-feature-name.md

Multiple sessions on same day go in the same file.

## Session Template

# Session: YYYY-MM-DD

## Session 1 (HH:MM AM/PM)

### Goal

[To be filled]

### Changes Made

- [To be documented]

### Decisions

- [To be documented]

### Incomplete

- [To be documented]

## Related Commands

- /start - Bootstrap session with context
- /end - Document and prepare to clear session
