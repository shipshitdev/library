# Ship Shit Dev - Agent Workspace

This is the **library repository** containing skills and commands for distribution to Claude, Codex, and Cursor agents.

## Important Context

**You are working ON the library, not IN a project that uses it.**

- `agents/` - Contains distributable skills/commands (symlinked from `~/.claude/`, `~/.codex/`, `~/.cursor/`)
- `.agent/` - This folder, for managing work on the library itself

## Structure

```
library/
├── .agent/              # Library management (you are here)
│   ├── README.md
│   ├── SESSIONS/        # Session documentation
│   ├── TASKS/           # Library tasks
│   └── SYSTEM/          # Library-specific rules
│
├── agents/              # DISTRIBUTABLE CONTENT
│   ├── .claude/
│   │   ├── skills/      # 42 skills
│   │   └── commands/    # Commands
│   ├── .codex/
│   │   ├── skills/      # 42 skills
│   │   └── commands/
│   └── .cursor/
│       ├── skills/      # 42 skills
│       └── commands/    # 24 commands
│
├── docs/                # Library documentation
│   ├── PLATFORM-ADAPTATIONS.md
│   └── SKILL-MANAGEMENT.md
│
└── scripts/             # Scaffolding, sync scripts
```

## Common Tasks

### Adding a New Skill

1. Create in `agents/.claude/skills/skill-name/SKILL.md`
2. Sync to other platforms using patterns in `docs/PLATFORM-ADAPTATIONS.md`
3. Update README.md skill table

### Syncing Skills Between Platforms

See `docs/SKILL-MANAGEMENT.md` for workflow.

### Updating Symlinks

See `docs/SYMLINK-CONFIG.md` for current symlink configuration.

## Session Documentation

Document sessions in `.agent/SESSIONS/YYYY-MM-DD.md`
