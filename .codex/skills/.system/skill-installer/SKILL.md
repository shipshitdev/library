---
name: skill-installer
description: Install Codex skills into $CODEX_HOME/skills from a curated list or a local repo path, using copy or symlink based on user preference.
---

# Skill Installer

Use this skill when a user wants to list installable skills, install a curated skill, or install skills from another repo path (including private repos).

## Workflow

1) Verify the source path exists.
2) Confirm install scope: global (`~/.codex/skills`) or project (`./.codex/skills`).
3) Prefer symlinks for shared repos; copy only when a snapshot is desired.
4) Never overwrite an existing skill without confirmation.
5) Tell the user to restart Codex after installing.

## Common Commands

List skills in a repo:
```
ls -1 /path/to/repo/.codex/skills
```

Install via symlink:
```
ln -s /path/to/repo/.codex/skills/skill-name ~/.codex/skills/skill-name
```

Install via copy:
```
cp -R /path/to/repo/.codex/skills/skill-name ~/.codex/skills/
```
