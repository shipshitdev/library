# Installation: Changelog Generator

## Prerequisites
- Claude Code installed
- Clone this repository

## Install via Symlink
```bash
ln -s /path/to/skills/.claude/skills/changelog-generator ~/.claude/skills/changelog-generator
```

## Install via Copy
```bash
cp -r /path/to/skills/.claude/skills/changelog-generator ~/.claude/skills/changelog-generator
```

## Verify Installation
```bash
ls -la ~/.claude/skills/changelog-generator
cat ~/.claude/skills/changelog-generator/SKILL.md
```

## Usage
The skill activates automatically when you need to create user-facing changelogs from git commits.

## Dependencies
- Git repository with commit history

---
See main [INSTALL.md](../../../../INSTALL.md) for all available skills/commands.
