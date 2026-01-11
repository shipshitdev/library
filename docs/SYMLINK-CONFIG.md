# Symlink Configuration

Configure symlinks to use Ship Shit Dev Library skills and commands globally.

## Quick Setup

Run the setup script from anywhere:

```bash
# From the library directory
./scripts/setup-symlinks.sh

# Or with npm
npm run setup:symlinks

# Preview changes without applying
./scripts/setup-symlinks.sh --dry-run

# Force replace existing files/directories
./scripts/setup-symlinks.sh --force
```

## What Gets Linked

| Target | Source |
|--------|--------|
| `~/.claude/skills` | `<library>/agents/.claude/skills` |
| `~/.claude/commands` | `<library>/agents/.claude/commands` |
| `~/.claude/agents` | `<library>/agents/.claude/agents` |
| `~/.claude/rules` | `<library>/agents/.claude/rules` |
| `~/.codex/skills` | `<library>/agents/.codex/skills` |
| `~/.cursor/skills` | `<library>/agents/.cursor/skills` |
| `~/.cursor/commands` | `<library>/agents/.cursor/commands` |

The script automatically detects the library location - no hardcoded paths needed.

## Verification

Check symlinks are working:

```bash
npm run check-symlinks
```

Or manually:

```bash
ls -la ~/.claude/skills ~/.claude/commands
```

## Directory Structure

```
library/
├── scripts/
│   └── setup-symlinks.sh    # Setup script
├── agents/                   # Symlink targets
│   ├── .claude/
│   │   ├── skills/          # <- ~/.claude/skills
│   │   ├── commands/        # <- ~/.claude/commands
│   │   ├── agents/          # <- ~/.claude/agents
│   │   └── rules/           # <- ~/.claude/rules
│   ├── .codex/
│   │   └── skills/          # <- ~/.codex/skills
│   └── .cursor/
│       ├── skills/          # <- ~/.cursor/skills
│       └── commands/        # <- ~/.cursor/commands
```

## Devcontainer Note

When using devcontainers, the setup script in `.devcontainer/setup.sh` automatically fixes symlinks to use container paths (`/workspace/...`) instead of host paths.

## Troubleshooting

**Symlinks point to wrong path:**

```bash
./scripts/setup-symlinks.sh
```

**Target exists and is not a symlink:**

```bash
./scripts/setup-symlinks.sh --force
```

**Commands not showing in Claude Code:**

1. Run `./scripts/setup-symlinks.sh`
2. Restart Claude Code
3. Run `/help` to see available commands
