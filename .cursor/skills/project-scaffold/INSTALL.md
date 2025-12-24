# Installation: Project Scaffold

## Prerequisites

- Claude Code installed
- Python 3 installed
- Clone this repository

## Install via Symlink

```bash
ln -s /path/to/skills/.cursor/skills/project-scaffold ~/.cursor/skills/project-scaffold
```

## Install via Copy

```bash
cp -r /path/to/skills/.cursor/skills/project-scaffold ~/.cursor/skills/project-scaffold
```

## Make Script Executable

```bash
chmod +x ~/.claude/skills/project-scaffold/scripts/scaffold.py
```

## Verify Installation

```bash
ls -la ~/.cursor/skills/project-scaffold
python ~/.cursor/skills/project-scaffold/scripts/scaffold.py --help
```

## Usage

The skill activates automatically when you need to scaffold a new project or add components to an existing project.

Run the scaffold script:

```bash
python ~/.cursor/skills/project-scaffold/scripts/scaffold.py
```

## Dependencies

- Python 3 (for scaffold script)
- bun (recommended package manager, but not required)
- agent-folder-init skill (optional, for .agent folder scaffolding)

## Optional: Install agent-folder-init

For full .agent folder support, also install the agent-folder-init skill:

```bash
ln -s /path/to/skills/.cursor/skills/agent-folder-init ~/.cursor/skills/agent-folder-init
```

---

See main [INSTALL.md](../../../../INSTALL.md) for all available skills/commands.
