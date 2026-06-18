# Ship Shit Dev - Agent Workspace

You are working **ON the library**, not in a project that uses it.

## Quick Start

| Need to... | Look at... |
|------------|------------|
| Find tasks | GitHub Issues |
| Check past context | `sessions/` |
| Read docs | `memory/system/` |

## Structure

```
.agents/
├── README.md          # You are here
├── memory/            # Durable context + system docs
│   └── system/        # Architecture docs, standards, workflows
├── sessions/          # Context preservation
└── skills/            # Meta-skills for maintaining this repo
```

## This Repository

```
library/
├── skills/              # All skills (single source)
├── commands/            # All commands
├── bundles/             # Generated marketplace bundles
├── .agents/             # Library management (you are here)
└── scripts/             # Scaffolding, validation scripts
```

## Common Tasks

### Adding a New Skill

1. Create in `skills/skill-name/SKILL.md`
2. Update `scripts/plugin-categories.json` if it belongs in a bundle
3. Run `bun run marketplace:generate`

### Running the Dev Loop

See `memory/system/ai-dev-loop.md`

### Task Tracking

Plans and implementation state live on GitHub issues and PRs, not in local
`.agents/plans/` files.

## Session Documentation

Before ending a session, document in `sessions/YYYY-MM-DD.md`:

- Files changed
- Decisions made
- Incomplete work
- Next steps
