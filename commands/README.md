# Cursor Commands

Generic slash commands for efficient development workflow across projects.

## All Commands (Alphabetical)

```
.cursor/commands/                    # Global commands (32 commands)
├── analyze-codebase.md        # Generate architecture analysis
├── api-test.md                # API testing workflows
├── bug.md                     # Quick bug capture
├── clean.md                   # Unified cleanup (tasks/sessions)
├── code-review.md             # Comprehensive code review
├── commit-summary.md          # Generate commit messages
├── de-slop.md                 # Clean AI artifacts (monorepo-aware)
├── deploy.md                  # Deployment workflows
├── docs-generate.md           # Generate comprehensive documentation
├── docs-update.md             # Update documentation
├── end.md                     # Document session before clearing
├── env-setup.md               # Environment variable management
├── inbox.md                   # Process inbox items
├── launch.md                  # Startup launch workflow
├── migrate.md                 # Database migrations
├── monitoring-setup.md        # Sentry & Google Analytics setup
├── mvp-plan.md                # MVP planning and scoping
├── new-cmd.md                 # Create new commands
├── new-session.md             # Create session files
├── optimize-prompt.md         # AI prompt optimization
├── performance.md             # Performance optimization
├── quick-fix.md               # Daily task list
├── refactor-code.md           # Refactoring workflows
├── review-pr.md               # Pull request review (basic)
├── scaffold.md                # Unified project scaffolder
├── security-audit.md          # Security audit workflow
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
- `/commit-summary` - Generate commit messages from staged changes

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

#### Launch & Infrastructure

- `/launch` - Full startup launch workflow (pre-flight, deploy, verify)
- `/mvp-plan` - MVP feature prioritization and scoping
- `/db-setup` - MongoDB on EC2 (Docker) and Redis setup
- `/env-setup` - Environment variable management
- `/monitoring-setup` - Sentry & Google Analytics setup
- `/de-slop` - Clean AI-generated code artifacts

#### Specialized

- `/optimize-prompt` - Optimize AI prompts using frameworks
- `/performance` - Performance analysis and optimization
- `/security-audit` - Comprehensive security audit

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

These commands use standard `.agents/` folder structure. Only adapt project-specific paths:

- `[project]` - Replace with your project name/path
- `[frontend-project]` - Replace with your frontend project path (e.g., `web/`, `frontend/`)
- `[backend-project]` - Replace with your backend project path (e.g., `api/`, `server/`)

### Standard Paths (Do Not Change)

All commands use these standard paths:

- `.agents/SYSTEM/` - Architecture, rules, summary
- `.agents/SESSIONS/` - Session documentation
- `.agents/TASKS/` - Task files
- `.agents/PRDS/` - Product requirement documents
- `.agents/EXAMPLES/` - Code examples

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

- Commands use standard `.agents/` folder structure
- Only project paths need adaptation (`[frontend-project]`, `[backend-project]`)
- Security checks in `/code-review` are configurable - adapt to your requirements
- Task management commands use standard `.agents/TASKS/` and `.agents/PRDS/` structure

---

**Total Commands:** 32
**Last Updated:** 2025-01-27
