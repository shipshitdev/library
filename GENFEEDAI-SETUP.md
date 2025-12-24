# Genfeedai Integration Setup

This document describes how genfeedai projects are configured to use centralized commands from this repository.

## Architecture

### Command Sources

**Centralized (Generic Commands):**
- Location: `/Users/decod3rs/www/agenticindiedev/skills/.cursor/commands/`
- Contains: Generic, reusable commands (18 commands)
- Used by: All genfeedai projects via symlinks

**Genfeedai-Specific (Project Commands):**
- Location: `/Users/decod3rs/www/genfeedai/.cursor/commands/`
- Contains: Genfeed-specific commands (gen-model, gen-template, co-founder, etc.)
- Used by: Genfeedai workspace only

### Project Structure

Each genfeedai project has:
```
[project]/.cursor/
├── commands -> /Users/decod3rs/www/agenticindiedev/skills/.cursor/commands  (symlink)
└── settings.json  (project-specific Cursor settings)
```

Genfeedai workspace has:
```
genfeedai/.cursor/
├── commands/  (genfeed-specific commands)
└── rules  (genfeed-specific rules)
```

## Setup

### Initial Setup

Run the setup script:

```bash
cd /Users/decod3rs/www/agenticindiedev/skills
bash scripts/setup-genfeedai-symlinks.sh
```

This script:
1. Backs up existing symlinks/directories
2. Creates symlinks in each project pointing to centralized commands
3. Preserves project-specific `settings.json` files

### Projects Configured

- `api.genfeed.ai/.cursor/commands` → centralized repo
- `genfeed.ai/.cursor/commands` → centralized repo
- `extension.genfeed.ai/.cursor/commands` → centralized repo
- `mobile.genfeed.ai/.cursor/commands` → centralized repo
- `docs.genfeed.ai/.cursor/commands` → centralized repo
- `packages.genfeed.ai/.cursor/commands` → centralized repo

## How It Works

### Command Resolution

When Cursor looks for commands in a project:

1. **Project level**: Checks `[project]/.cursor/commands/` → Points to centralized repo
2. **Workspace level**: Checks `genfeedai/.cursor/commands/` → Genfeed-specific commands
3. **Global level**: Checks `~/.cursor/commands/` → Also points to centralized repo (via symlink)

### Command Types

**Generic Commands** (in centralized repo):
- `/start`, `/task`, `/bug`, `/code-review`, `/analyze-codebase`, etc.
- Work across all projects
- Updated in one place, available everywhere

**Genfeed-Specific Commands** (in genfeedai workspace):
- `/gen-model` - Replicate model integration
- `/gen-template` - Template management
- `/co-founder` - Strategic planning
- `/check-coverage` - Coverage checks
- etc.

## Benefits

1. **Single Source of Truth**: Generic commands maintained in one place
2. **Automatic Updates**: Changes propagate to all projects via symlinks
3. **Project-Specific**: Genfeed-specific commands stay in genfeedai workspace
4. **Flexibility**: Projects can override with local commands if needed

## Maintenance

### Adding New Generic Commands

1. Add command to `/Users/decod3rs/www/agenticindiedev/skills/.cursor/commands/`
2. Automatically available in all genfeedai projects (via symlink)

### Adding Genfeed-Specific Commands

1. Add command to `/Users/decod3rs/www/genfeedai/.cursor/commands/`
2. Only available in genfeedai workspace context

### Updating Project Settings

Edit `[project]/.cursor/settings.json` directly (not symlinked, project-specific)

## Verification

Check symlinks are working:

```bash
# Check a project symlink
ls -la /Users/decod3rs/www/genfeedai/api.genfeed.ai/.cursor/commands

# Should show:
# commands -> /Users/decod3rs/www/agenticindiedev/skills/.cursor/commands
```

## Troubleshooting

**Symlink broken:**
```bash
# Re-run setup script
bash /Users/decod3rs/www/agenticindiedev/skills/scripts/setup-genfeedai-symlinks.sh
```

**Commands not appearing:**
- Verify symlink exists: `ls -la [project]/.cursor/commands`
- Check Cursor is reading from `.cursor/commands/`
- Restart Cursor if needed

**Need project-specific command:**
- Create in `genfeedai/.cursor/commands/` (workspace-level)
- Or create local override in project (not recommended)

---

**Last Updated:** 2025-12-24
