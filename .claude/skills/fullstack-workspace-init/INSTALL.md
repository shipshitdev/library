# Installation: Fullstack Workspace Init

## Prerequisites
- Claude Code installed
- Clone this repository

## Install via Symlink
```bash
ln -s /path/to/skills/.claude/skills/fullstack-workspace-init ~/.claude/skills/fullstack-workspace-init
```

## Install via Copy
```bash
cp -r /path/to/skills/.claude/skills/fullstack-workspace-init ~/.claude/skills/fullstack-workspace-init
```

## Verify Installation
```bash
ls -la ~/.claude/skills/fullstack-workspace-init
cat ~/.claude/skills/fullstack-workspace-init/SKILL.md
```

## Usage
The skill activates automatically when you need to scaffold a full-stack monorepo workspace with NextJS frontend, NestJS backend, and React Native mobile.

## Dependencies
- Python 3 (for init scripts)
- bun (package manager)

---
See main [INSTALL.md](../../../../INSTALL.md) for all available skills/commands.
