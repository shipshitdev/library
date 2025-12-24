# Installation Guide

This guide explains how to install individual skills and commands from this repository. You can install items selectively using either symlink (recommended for auto-updates) or copy (for independence).

## Installation Methods

### Method 1: Symlink (Recommended)

Symlinks allow you to automatically receive updates when the repository is updated. Changes to the original files are immediately reflected.

**Advantages:**

- Automatic updates when you pull the repository
- No duplication of files
- Easy to update multiple installations

**Disadvantages:**

- Requires the repository to remain in the same location
- Broken if you move or delete the repository

### Method 2: Copy

Copying files gives you complete independence from the repository. You can modify files without affecting the original.

**Advantages:**

- Complete independence
- Can customize without affecting source
- Works even if repository is moved/deleted

**Disadvantages:**

- No automatic updates
- Must manually update when new versions are released
- Duplicates files on disk

## Prerequisites

1. **Clone this repository:**

   ```bash
   git clone <repository-url>
   cd skills
   ```

2. **Understand platform directories:**

   - **Cursor**: `~/.cursor/commands/` and `~/.cursor/skills/`
   - **Claude**: `~/.claude/skills/`
   - **Codex**: `~/.codex/skills/`

3. **Create target directories if they don't exist:**
   ```bash
   mkdir -p ~/.cursor/commands
   mkdir -p ~/.cursor/skills
   mkdir -p ~/.claude/skills
   mkdir -p ~/.codex/skills
   ```

## Quick Start

1. Choose a skill or command from the registry below
2. Navigate to its directory in this repository
3. Follow the installation instructions in its `INSTALL.md` file (for skills) or installation section (for commands)
4. Verify installation using the provided verification steps

## Available Skills & Commands

### Cursor Commands

Commands are single `.md` files that can be installed individually. Each command file contains installation instructions at the top.

| Command                                                  | Description                          | Installation                                                                  |
| -------------------------------------------------------- | ------------------------------------ | ----------------------------------------------------------------------------- |
| [analyze-codebase](.cursor/commands/analyze-codebase.md) | Generate architecture analysis       | See [installation section](.cursor/commands/analyze-codebase.md#installation) |
| [bug](.cursor/commands/bug.md)                           | Quick bug capture                    | See [installation section](.cursor/commands/bug.md#installation)              |
| [clean](.cursor/commands/clean.md)                       | Unified cleanup (tasks/sessions)     | See [installation section](.cursor/commands/clean.md#installation)            |
| [code-review](.cursor/commands/code-review.md)           | Comprehensive code review            | See [installation section](.cursor/commands/code-review.md#installation)      |
| [docs-generate](.cursor/commands/docs-generate.md)       | Generate comprehensive documentation | See [installation section](.cursor/commands/docs-generate.md#installation)    |
| [docs-update](.cursor/commands/docs-update.md)           | Update documentation                 | See [installation section](.cursor/commands/docs-update.md#installation)      |
| [end](.cursor/commands/end.md)                           | Document session before clearing     | See [installation section](.cursor/commands/end.md#installation)              |
| [inbox](.cursor/commands/inbox.md)                       | Process inbox items                  | See [installation section](.cursor/commands/inbox.md#installation)            |
| [new-cmd](.cursor/commands/new-cmd.md)                   | Create new commands                  | See [installation section](.cursor/commands/new-cmd.md#installation)          |
| [new-session](.cursor/commands/new-session.md)           | Create session files                 | See [installation section](.cursor/commands/new-session.md#installation)      |
| [optimize-prompt](.cursor/commands/optimize-prompt.md)   | AI prompt optimization               | See [installation section](.cursor/commands/optimize-prompt.md#installation)  |
| [quick-fix](.cursor/commands/quick-fix.md)               | Daily task list                      | See [installation section](.cursor/commands/quick-fix.md#installation)        |
| [refactor-code](.cursor/commands/refactor-code.md)       | Refactoring workflows                | See [installation section](.cursor/commands/refactor-code.md#installation)    |
| [review-pr](.cursor/commands/review-pr.md)               | Pull request review (basic)          | See [installation section](.cursor/commands/review-pr.md#installation)        |
| [start](.cursor/commands/start.md)                       | Bootstrap session context            | See [installation section](.cursor/commands/start.md#installation)            |
| [task](.cursor/commands/task.md)                         | Create and manage tasks              | See [installation section](.cursor/commands/task.md#installation)             |
| [test](.cursor/commands/test.md)                         | Test tracking                        | See [installation section](.cursor/commands/test.md#installation)             |
| [validate](.cursor/commands/validate.md)                 | Unified validation (docs/sessions)   | See [installation section](.cursor/commands/validate.md#installation)         |

### Cursor Skills

Skills are directories containing `SKILL.md` and optional supporting files. Each skill has its own `INSTALL.md` file.

| Skill                                                      | Description                                                  | Installation                                                    |
| ---------------------------------------------------------- | ------------------------------------------------------------ | --------------------------------------------------------------- |
| [analytics-expert](.cursor/skills/analytics-expert/)       | Analyze analytics data, create reports, identify trends      | See [INSTALL.md](.cursor/skills/analytics-expert/INSTALL.md)    |
| [planning-assistant](.cursor/skills/planning-assistant/)   | Content planning, calendar management, research organization | See [INSTALL.md](.cursor/skills/planning-assistant/INSTALL.md)  |
| [strategy-expert](.cursor/skills/strategy-expert/)         | Content strategy, persona building, competitive analysis     | See [INSTALL.md](.cursor/skills/strategy-expert/INSTALL.md)     |
| [workflow-automation](.cursor/skills/workflow-automation/) | Design workflows, create process documentation, automation   | See [INSTALL.md](.cursor/skills/workflow-automation/INSTALL.md) |

### Claude Skills

Skills are directories containing `SKILL.md` and optional supporting files. Each skill has its own `INSTALL.md` file.

| Skill                                                                    | Description                                       | Installation                                                           |
| ------------------------------------------------------------------------ | ------------------------------------------------- | ---------------------------------------------------------------------- |
| [agent-folder-init](.claude/skills/agent-folder-init/)                   | Initialize comprehensive .agent/ folder structure | See [INSTALL.md](.claude/skills/agent-folder-init/INSTALL.md)          |
| [changelog-generator](.claude/skills/changelog-generator/)               | Generate changelogs from git history              | See [INSTALL.md](.claude/skills/changelog-generator/INSTALL.md)        |
| [design-consistency-auditor](.claude/skills/design-consistency-auditor/) | Audit design consistency across projects          | See [INSTALL.md](.claude/skills/design-consistency-auditor/INSTALL.md) |
| [fullstack-workspace-init](.claude/skills/fullstack-workspace-init/)     | Initialize fullstack workspace structure          | See [INSTALL.md](.claude/skills/fullstack-workspace-init/INSTALL.md)   |
| [internal-comms](.claude/skills/internal-comms/)                         | Generate internal communications and updates      | See [INSTALL.md](.claude/skills/internal-comms/INSTALL.md)             |
| [micro-landing-builder](.claude/skills/micro-landing-builder/)           | Build micro landing pages                         | See [INSTALL.md](.claude/skills/micro-landing-builder/INSTALL.md)      |
| [qa-reviewer](.claude/skills/qa-reviewer/)                               | Quality assurance review assistance               | See [INSTALL.md](.claude/skills/qa-reviewer/INSTALL.md)                |
| [roadmap-analyzer](.claude/skills/roadmap-analyzer/)                     | Analyze and plan product roadmaps                 | See [INSTALL.md](.claude/skills/roadmap-analyzer/INSTALL.md)           |
| [session-documenter](.claude/skills/session-documenter/)                 | Document AI coding sessions                       | See [INSTALL.md](.claude/skills/session-documenter/INSTALL.md)         |
| [skill-creator](.claude/skills/skill-creator/)                           | Create new skills for AI assistants               | See [INSTALL.md](.claude/skills/skill-creator/INSTALL.md)              |
| [webapp-testing](.claude/skills/webapp-testing/)                         | Web application testing assistance                | See [INSTALL.md](.claude/skills/webapp-testing/INSTALL.md)             |

## Installation Method Comparison

### When to Use Symlink

- You want automatic updates
- You're comfortable with the repository location staying fixed
- You want to share installations across multiple projects
- You're actively contributing to or following the repository

### When to Use Copy

- You want to customize the skill/command for your specific needs
- You don't want to depend on the repository location
- You prefer manual control over updates
- You're using the skill/command in a production environment where stability is critical

## Troubleshooting

### Symlink Issues

**Problem**: Symlink shows as broken

```bash
ls -la ~/.cursor/commands/start.md
# Shows: start.md -> /path/to/skills/.cursor/commands/start.md (broken)
```

**Solution**:

1. Check that the repository path is correct
2. Ensure the source file exists: `ls -la /path/to/skills/.cursor/commands/start.md`
3. Recreate the symlink with the correct path

**Problem**: Permission denied when creating symlink

**Solution**: Ensure you have write permissions to the target directory:

```bash
chmod u+w ~/.cursor/commands
```

### Copy Issues

**Problem**: Command/skill not appearing in Cursor/Claude

**Solution**:

1. Verify the file/directory exists in the correct location
2. Restart Cursor/Claude
3. Check file permissions: `chmod 644 ~/.cursor/commands/start.md` (for files) or `chmod -R 755 ~/.cursor/skills/skill-name` (for directories)

### Platform-Specific Issues

**macOS/Linux**: Symlinks work natively. Use `ln -s` as shown in examples.

**Windows**:

- Use WSL (Windows Subsystem for Linux) for native symlink support
- Or use `mklink` command in Command Prompt (requires admin privileges)
- Or use the copy method instead

## Getting Help

- Check the individual `INSTALL.md` file for each skill
- Check the installation section at the top of each command file
- Review the main [README.md](README.md) for general information
- Check platform-specific documentation (Cursor, Claude, Codex)

## Contributing

If you find installation issues or want to improve the installation documentation, please contribute back to this repository!
