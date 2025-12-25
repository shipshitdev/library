# Cursor Agent Documentation

This folder contains global skills and commands for Cursor IDE.

## Documentation Links

### Commands
N/A

Cursor IDE does not currently have public documentation for creating custom slash commands. Commands in this folder are markdown files that define custom workflows and can be invoked via the `/` prefix in Cursor.

### Hooks
N/A

Cursor IDE does not currently have public documentation for hooks.

### Agents
N/A

Cursor IDE does not currently have public documentation for agents.

### Skills
N/A

Cursor IDE does not currently have public documentation for writing skills. Skills in this folder follow a similar structure to Claude skills for compatibility. Refer to the [Claude Skills Documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills) for guidance on skill structure and best practices.

## Folder Structure

```
.cursor/
├── commands/        # Custom slash commands (32 commands)
└── skills/          # Global skills (50 skills)
```

## Usage

### Commands

Commands are invoked with a forward slash in Cursor:

```bash
/start              # Bootstrap session context
/task               # Create and manage tasks
/bug                # Quick bug capture
/code-review        # Comprehensive code review
```

See [`.cursor/commands/README.md`](commands/README.md) for a complete list of available commands.

### Skills

Skills are automatically available when placed in the `.cursor/skills/` directory. They extend the AI assistant's capabilities with specialized knowledge and workflows.

## Resources

- [Cursor Documentation](https://docs.cursor.com/)
- [Claude Skills Documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills) (for skill structure reference)

