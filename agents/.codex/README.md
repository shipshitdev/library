# Codex Agent Documentation

This folder contains global skills and commands for OpenAI Codex.

## Documentation Links

### Commands
See `commands/README.md`. OpenAI Codex does not currently support custom commands.

### Hooks
N/A

OpenAI Codex does not currently have public documentation for hooks.

### Agents
N/A

OpenAI Codex does not currently have public documentation for agents.

### Skills
See `skills/` (123 skills). OpenAI Codex does not currently have public documentation for writing skills. Skills in this folder follow a similar structure to Claude skills for compatibility. The hidden `.system/` folder contains internal/system skills.

## Folder Structure

```
.codex/
├── commands/        # Custom commands (if applicable)
└── skills/          # Global skills (123 skills)
    └── .system/     # Internal/system skills
```

## Note

Codex skills follow a similar structure to Claude skills for compatibility and ease of maintenance. Refer to the [Claude Skills Documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills) for guidance on skill structure and best practices.
