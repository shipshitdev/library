# Cursor Commands

Generic slash commands for efficient development workflow across projects.

## All Commands (Alphabetical)

```
.cursor/commands/                    # Global commands (24 commands)
├── analyze-codebase.md        # Generate architecture analysis
├── bug.md                     # Quick bug capture
├── clean.md                   # Unified cleanup (tasks/sessions)
├── code-review.md             # Comprehensive code review
├── docs-generate.md           # Generate comprehensive documentation
├── docs-update.md             # Update documentation
├── end.md                     # Document session before clearing
├── inbox.md                   # Process inbox items
├── new-cmd.md                 # Create new commands
├── new-session.md             # Create session files
├── optimize-prompt.md         # AI prompt optimization
├── quick-fix.md               # Daily task list
├── refactor-code.md           # Refactoring workflows
├── review-pr.md               # Pull request review (basic)
├── scaffold.md                # Unified project scaffolder
├── start.md                   # Bootstrap session context
├── task.md                    # Create and manage tasks
├── test.md                    # Test tracking
└── validate.md                # Unified validation (docs/sessions)
```

## Quick Reference

### Most Used Commands

```bash
/start              # Start every session with this
/task               # Create new tasks
/bug                # Quick bug capture
/clean sessions     # Cleanup session files
/validate all       # Validate docs and sessions
/code-review        # Comprehensive code review
```

### Commands by Category

#### Core Workflow

- `/start` - Load critical context at session start
- `/end` - Document session before clearing context
- `/task` - Create tasks with PRDs
- `/bug` - Fast bug documentation
- `/test` - Track testing todos
- `/inbox` - Process inbox items

#### Development & Review

- `/quick-fix` - Daily task lists
- `/refactor-code` - Refactoring helpers
- `/review-pr` - PR review checklist (basic)
- `/code-review` - Comprehensive code review (security, quality, performance)
- `/analyze-codebase` - Generate architecture analysis

#### Generators

- `/new-cmd` - Create new slash commands
- `/new-session` - Create session file from template
- `/scaffold` - Unified project scaffolder (backend, frontend, mobile, extension)

#### Maintenance

- `/clean tasks` - Empty completed task files
- `/clean sessions` - Merge daily → monthly → yearly
- `/clean all` - Run all cleanup
- `/validate docs` - Check documentation structure
- `/validate sessions` - Fix session naming
- `/validate all` - All validation checks

#### Documentation

- `/docs-update` - Update documentation
- `/docs-generate` - Generate comprehensive documentation (APIs, features, code)

#### Specialized

- `/optimize-prompt` - Optimize AI prompts using frameworks

## Command Usage

Commands are invoked with a forward slash:

```bash
/command-name
```

For commands with options:

```bash
/clean tasks
/clean sessions
/clean all

/validate docs
/validate sessions
/validate all
```

## Adapting Commands to Your Project

These commands use standard `.agent/` folder structure. Only adapt project-specific paths:

- `[project]` - Replace with your project name/path
- `[frontend-project]` - Replace with your frontend project path (e.g., `web/`, `frontend/`)
- `[backend-project]` - Replace with your backend project path (e.g., `api/`, `server/`)

### Standard Paths (Do Not Change)

All commands use these standard paths:

- `.agent/SYSTEM/` - Architecture, rules, summary
- `.agent/SESSIONS/` - Session documentation
- `.agent/TASKS/` - Task files
- `.agent/PRDS/` - Product requirement documents
- `.agent/EXAMPLES/` - Code examples

### Common Adaptations Needed

**Project Paths:**

- `[frontend-project]/` → Your frontend project name
- `[api-project]/` → Your backend project name

**Security Patterns:**

- Multi-tenancy: Adapt `organization`/`tenantId` to your field names
- Soft delete: Adapt `isDeleted` to your pattern
- Auth guards: Adapt `ClerkAuthGuard` to your auth system

**Project Structure:**

- Monorepo structure: Adapt to your workspace setup
- Task/PRD locations: Adapt to your task tracking system

## Adding New Commands

Use the generator:

```bash
/new-cmd
```

Follow the naming convention:

- Format: `{verb}-{noun}.md`
- Use kebab-case
- Place in `.cursor/commands/` directory

## Notes

- Commands use standard `.agent/` folder structure
- Only project paths need adaptation (`[frontend-project]`, `[backend-project]`)
- Security checks in `/code-review` are configurable - adapt to your requirements
- Task management commands use standard `.agent/TASKS/` and `.agent/PRDS/` structure

---

**Total Commands:** 24
**Last Updated:** 2025-12-24
