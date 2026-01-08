# Symlink Configuration

Current symlink configuration for the Ship Shit Dev Library.

## Active Symlinks

| Source | Target |
|--------|--------|
| `~/.claude/skills` | `/Users/decod3rs/www/shipshitdev/library/agents/.claude/skills` |
| `~/.claude/commands` | `/Users/decod3rs/www/shipshitdev/library/agents/.claude/commands` |
| `~/.codex/skills` | `/Users/decod3rs/www/shipshitdev/library/agents/.codex/skills` |
| `~/.cursor/skills` | `/Users/decod3rs/www/shipshitdev/library/agents/.cursor/skills` |
| `~/.cursor/commands` | `/Users/decod3rs/www/shipshitdev/library/agents/.cursor/commands` |

## Setup Commands

To recreate these symlinks:

```bash
# Claude
rm -f ~/.claude/skills ~/.claude/commands
ln -s /Users/decod3rs/www/shipshitdev/library/agents/.claude/skills ~/.claude/skills
ln -s /Users/decod3rs/www/shipshitdev/library/agents/.claude/commands ~/.claude/commands

# Codex
rm -f ~/.codex/skills
ln -s /Users/decod3rs/www/shipshitdev/library/agents/.codex/skills ~/.codex/skills

# Cursor
rm -f ~/.cursor/skills ~/.cursor/commands
ln -s /Users/decod3rs/www/shipshitdev/library/agents/.cursor/skills ~/.cursor/skills
ln -s /Users/decod3rs/www/shipshitdev/library/agents/.cursor/commands ~/.cursor/commands
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

2026-01-08
