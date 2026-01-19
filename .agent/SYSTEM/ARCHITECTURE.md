# .agent/ Folder Architecture

The `.agent/` folder is a standardized workspace for AI agents to manage tasks, preserve context across sessions, and access project-specific documentation.

## Why It Exists

AI agents face three challenges:

1. **Context loss** - Sessions end, context disappears
2. **Task tracking** - No persistent state between invocations
3. **Documentation access** - Project rules scattered or missing

The `.agent/` folder solves these with file-based state that any AI platform can read/write.

## Folder Structure

```
.agent/
├── README.md          # Quick-start for AI agents (entry point)
├── SESSIONS/          # Context preservation across sessions
├── TASKS/             # Task queue (Kanban-style)
└── SYSTEM/            # Project documentation (you are here)
```

### README.md

The entry point. AI agents read this first to understand:

- What project they're working on
- Where to find documentation
- How to manage tasks and sessions

Keep it short. Link to SYSTEM/ docs for details.

### SESSIONS/

Preserves context when sessions end. Each file is a dated snapshot:

```
SESSIONS/
├── 2024-01-15.md      # What happened on Jan 15
├── 2024-01-16.md      # What happened on Jan 16
└── ...
```

**Session file format:**

```markdown
# Session: 2024-01-16

## Summary
Brief description of what was accomplished.

## Files Changed
- `path/to/file.ts` - What changed and why
- `path/to/other.ts` - What changed and why

## Decisions Made
- Decision 1: Rationale
- Decision 2: Rationale

## Incomplete Work
- Task that needs finishing
- Known issue to address

## Next Steps
- What to do next session
```

**When to write:** Before ending any non-trivial session. Before `/clear`.

### TASKS/

File-based task queue. Each task is a markdown file:

```
TASKS/
├── Kaiban.md          # Visual task board (optional)
├── 001-feature-name.md
├── 002-bug-fix.md
└── ...
```

**Task file format:**

```markdown
---
id: 001
title: Implement user authentication
status: To Do
priority: high
created: 2024-01-15
claimed_by: null
claimed_at: null
expires_at: null
---

## Description
What needs to be done.

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Notes
Additional context, links, decisions.
```

**Task statuses:**

| Status | Meaning |
|--------|---------|
| `Backlog` | Not ready to work on |
| `To Do` | Ready to be picked up |
| `In Progress` | Currently being worked on |
| `Testing` | Implementation done, needs QA |
| `Done` | Completed and verified |

### SYSTEM/

Project documentation. Everything an AI agent needs to understand the project:

```
SYSTEM/
├── ARCHITECTURE.md        # This file - .agent/ folder structure
├── AI-DEV-LOOP.md         # The /loop workflow
├── PRD.md                 # Product Requirements (optional)
├── PLATFORM-ADAPTATIONS.md
├── SKILL-MANAGEMENT.md
└── SYMLINK-CONFIG.md
```

**Rule:** All project documentation lives here. No scattered docs.

## Task Workflow (Kanban)

Tasks flow through statuses:

```
BACKLOG → TO DO → IN PROGRESS → TESTING → DONE
                       ↑             │
                       └──Rejected───┘
```

- **Backlog:** Ideas, not ready
- **To Do:** Prioritized, ready to pick up
- **In Progress:** Agent is working on it
- **Testing:** Done, awaiting human QA
- **Done:** Approved and complete

Rejected tasks go back to "To Do" with feedback.

## Claim System

Tasks can be "claimed" to prevent conflicts:

```yaml
claimed_by: claude-code
claimed_at: 2024-01-16T10:30:00Z
expires_at: 2024-01-16T11:00:00Z
```

**Why claims expire:** If an agent hits rate limits, crashes, or the user switches platforms, claims expire after 30 minutes. Another agent can then pick up the task.

## PRD Integration

Product Requirements Documents (PRDs) in `SYSTEM/PRD.md` define features. Tasks reference PRD sections:

```markdown
---
title: Implement login form
prd_section: "3.1 Authentication"
---
```

This links implementation tasks to product requirements.

## Multi-Platform Support

The `.agent/` folder works across platforms:

| Platform | How it works |
|----------|--------------|
| Claude Code | Native file access |
| Cursor | File access via IDE |
| Codex | File access via tools |

All platforms read/write the same files. The claim system handles handoffs.

## Quick Reference

| Need to... | Look at... |
|------------|------------|
| Understand the project | `.agent/README.md` |
| Find what to work on | `.agent/TASKS/` |
| Check past context | `.agent/SESSIONS/` |
| Read project docs | `.agent/SYSTEM/` |
| Understand task flow | This file (ARCHITECTURE.md) |
| Run the dev loop | `AI-DEV-LOOP.md` |
