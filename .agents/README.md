# Ship Shit Dev - Agent Workspace

You are working **ON the library**, not in a project that uses it.

## Quick Start

| Need to... | Look at... |
|------------|------------|
| Find tasks | GitHub Issues |
| Check past context | `SESSIONS/` |
| Read docs | `SYSTEM/` |

## Structure

```
.agents/
├── README.md          # You are here
├── SESSIONS/          # Context preservation
└── SYSTEM/            # All documentation
    ├── ARCHITECTURE.md         # .agents/ folder explained
    ├── AI-DEV-LOOP.md          # The /loop workflow
    ├── PLATFORM-ADAPTATIONS.md # Claude vs Codex differences
    └── SKILL-MANAGEMENT.md     # Sync workflow
```

## This Repository

```
library/
├── skills/              # All skills (single source)
├── commands/            # All commands
├── bundles/             # Generated marketplace bundles
├── .agents/             # Library management (you are here)
└── scripts/             # Scaffolding, validation scripts
```

## Common Tasks

### Adding a New Skill

1. Create in `skills/skill-name/SKILL.md`
2. Update main README.md skill table

### Running the Dev Loop

See `SYSTEM/AI-DEV-LOOP.md`

## Session Documentation

Before ending a session, document in `SESSIONS/YYYY-MM-DD.md`:

- Files changed
- Decisions made
- Incomplete work
- Next steps
