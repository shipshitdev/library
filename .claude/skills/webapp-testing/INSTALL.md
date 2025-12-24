# Installation: Webapp Testing

## Prerequisites
- Claude Code installed
- Clone this repository

## Install via Symlink
```bash
ln -s /path/to/skills/.claude/skills/webapp-testing ~/.claude/skills/webapp-testing
```

## Install via Copy
```bash
cp -r /path/to/skills/.claude/skills/webapp-testing ~/.claude/skills/webapp-testing
```

## Verify Installation
```bash
ls -la ~/.claude/skills/webapp-testing
cat ~/.claude/skills/webapp-testing/SKILL.md
```

## Usage
The skill activates automatically when you need to interact with and test local web applications using Playwright.

## Dependencies
- Python 3
- Playwright (`pip install playwright && playwright install`)

---
See main [INSTALL.md](../../../../INSTALL.md) for all available skills/commands.
