# Symlink Configuration

Current symlink configuration for the Agentic Indie Library.

## Active Symlinks

| Source | Target |
|--------|--------|
| `~/.claude/skills` | `/path/to/library/agents/.claude/skills` |
| `~/.claude/commands` | `/path/to/library/agents/.claude/commands` |
| `~/.codex/skills` | `/path/to/library/agents/.codex/skills` |
| `~/.cursor/skills` | `/path/to/library/agents/.cursor/skills` |
| `~/.cursor/commands` | `/path/to/library/agents/.cursor/commands` |

## Setup Commands

To recreate these symlinks:

```bash
# Claude
rm -f ~/.claude/skills ~/.claude/commands
ln -s /path/to/library/agents/.claude/skills ~/.claude/skills
ln -s /path/to/library/agents/.claude/commands ~/.claude/commands

# Codex
rm -f ~/.codex/skills
ln -s /path/to/library/agents/.codex/skills ~/.codex/skills

# Cursor
rm -f ~/.cursor/skills ~/.cursor/commands
ln -s /path/to/library/agents/.cursor/skills ~/.cursor/skills
ln -s /path/to/library/agents/.cursor/commands ~/.cursor/commands
```

## Verification

Check symlinks are working:

```bash
ls -la ~/.claude/skills ~/.claude/commands ~/.codex/skills ~/.cursor/skills ~/.cursor/commands
```

## Directory Structure

```
library/
├── agents/                    # Symlink targets
│   ├── .claude/
│   │   ├── skills/           # <- ~/.claude/skills
│   │   └── commands/         # <- ~/.claude/commands
│   ├── .codex/
│   │   └── skills/           # <- ~/.codex/skills
│   └── .cursor/
│       ├── skills/           # <- ~/.cursor/skills
│       └── commands/         # <- ~/.cursor/commands
```

## Last Updated

2025-12-25
