# Ship Shit Dev - Agent Workspace

You are working **ON the library**, not in a project that uses it.

## Quick Start

| Need to... | Look at... |
|------------|------------|
| Find tasks | `TASKS/` |
| Check past context | `SESSIONS/` |
| Read docs | `SYSTEM/` |

## Structure

```
.agent/
├── README.md          # You are here
├── SESSIONS/          # Context preservation
├── TASKS/             # Task queue
└── SYSTEM/            # All documentation
    ├── ARCHITECTURE.md         # .agent/ folder explained
    ├── AI-DEV-LOOP.md          # The /loop workflow
    ├── PLATFORM-ADAPTATIONS.md # Claude vs Codex differences
    ├── SKILL-MANAGEMENT.md     # Sync workflow
    └── SYMLINK-CONFIG.md       # Symlink setup
```

## This Repository

```
library/
├── .agent/              # Library management (you are here)
├── agents/              # DISTRIBUTABLE CONTENT
│   ├── .claude/skills/  # Skills for Claude
│   ├── .codex/skills/   # Skills for Codex
│   └── .cursor/skills/  # Skills for Cursor
└── scripts/             # Scaffolding, sync scripts
```

## Common Tasks

### Adding a New Skill

1. Create in `agents/.claude/skills/skill-name/SKILL.md`
2. Sync to other platforms (see `SYSTEM/PLATFORM-ADAPTATIONS.md`)
3. Update main README.md skill table

### Syncing Skills

See `SYSTEM/SKILL-MANAGEMENT.md`

### Setting Up Symlinks

See `SYSTEM/SYMLINK-CONFIG.md`

### Running the Dev Loop

See `SYSTEM/AI-DEV-LOOP.md`

## Session Documentation

Before ending a session, document in `SESSIONS/YYYY-MM-DD.md`:

- Files changed
- Decisions made
- Incomplete work
- Next steps
