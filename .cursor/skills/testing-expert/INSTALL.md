# Testing Expert Skill Installation

## Installation

### Via Symlink (Recommended)

```bash
ln -s /path/to/skills/.cursor/skills/testing-expert ~/.cursor/skills/testing-expert
```

### Via Copy

```bash
cp -r /path/to/skills/.cursor/skills/testing-expert ~/.cursor/skills/testing-expert
```

## Verification

```bash
ls -la ~/.cursor/skills/testing-expert/SKILL.md
```

## Usage

This skill activates automatically when you're working on:
- Writing unit tests
- Creating integration tests
- Setting up E2E tests
- Testing React components
- Testing API endpoints

No manual activation needed - Claude will load this skill based on context.
