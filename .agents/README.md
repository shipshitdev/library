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
├── skills/              # All skills (single source)
├── commands/            # All commands
├── bundles/             # Generated marketplace bundles
├── .agent/              # Library management (you are here)
└── scripts/             # Scaffolding, validation scripts
```

## Common Tasks

### Adding a New Skill

1. Create in `skills/skill-name/SKILL.md`
2. Update main README.md skill table

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
