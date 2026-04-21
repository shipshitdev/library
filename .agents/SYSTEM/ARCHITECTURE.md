# .agents/ Folder Architecture

The `.agents/` folder is a standardized workspace for AI agents to preserve context across sessions and access project-specific documentation.

## Why It Exists

AI agents face three challenges:

1. **Context loss** - Sessions end, context disappears
2. **Task tracking** - No persistent state between invocations
3. **Documentation access** - Project rules scattered or missing

The `.agents/` folder solves these with file-based state that any AI platform can read/write.

## Folder Structure

```
.agents/
├── README.md          # Quick-start for AI agents (entry point)
├── SESSIONS/          # Context preservation across sessions
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

### SYSTEM/

Project documentation. Everything an AI agent needs to understand the project:

```
SYSTEM/
├── ARCHITECTURE.md        # This file - .agents/ folder structure
├── AI-DEV-LOOP.md         # The /loop workflow
├── PRD.md                 # Product Requirements (optional)
├── PLATFORM-ADAPTATIONS.md
└── SKILL-MANAGEMENT.md
```

**Rule:** All project documentation lives here. No scattered docs.

## Task Tracking

Tasks are tracked via **GitHub Issues**. Use the repository's issue tracker to:

- Create new tasks with labels (backlog, in-progress, testing, done)
- Assign and claim work
- Document acceptance criteria and context
- Link PRs to issues for traceability

## Multi-Platform Support

The `.agents/` folder works across platforms:

| Platform | How it works |
|----------|--------------|
| Claude Code | Native file access |
| Cursor | File access via IDE |
| Codex | File access via tools |

All platforms read/write the same files.

## Quick Reference

| Need to... | Look at... |
|------------|------------|
| Understand the project | `.agents/README.md` |
| Find what to work on | GitHub Issues |
| Check past context | `.agents/SESSIONS/` |
| Read project docs | `.agents/SYSTEM/` |
| Run the dev loop | `AI-DEV-LOOP.md` |
