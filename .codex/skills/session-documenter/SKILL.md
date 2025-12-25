---
name: session-documenter
description: Automatically document session work after each task completion. Tracks decisions, file changes, flowcharts, and context for session continuity. Use this skill proactively throughout sessions to maintain comprehensive documentation in `.agent/SESSIONS/`.
location: project
auto_activate: true
---
# Session Documenter Skill

**Purpose:** Automatically document all work, decisions, and context throughout the session for continuity.

**Auto-activation:** This skill activates automatically when you complete tasks to ensure documentation is not skipped.

## When This Skill Activates

Trigger conditions:

1. When a task from TodoList is marked as completed
2. When files are modified, created, or deleted
3. When architectural decisions are made
4. When new patterns are established
5. At session end (mandatory)

## Required Files and Protocols

- `.agent/SYSTEM/ai/SESSION-DOCUMENTATION-PROTOCOL.md`
- `.agent/SESSIONS/TEMPLATE.md`
- `.agent/SESSIONS/README.md`
- `scripts/sh/validate-session-start.sh`
- `scripts/sh/new-session.sh`

## Workflow (Short)

1. Start: validate or create today's session file.
2. During work: track decisions, file changes, and patterns.
3. End: append a session entry with summary, decisions, and file changes; include a flowchart when required.

## References

- [Full guide: formatting rules, flowchart requirements, and examples](references/full-guide.md)
