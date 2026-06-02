# {{PROJECT_NAME}} - Agent Documentation Hub

**Welcome to the {{PROJECT_NAME}} workspace!**

This is the `.agents/` folder — source of truth for AI agent context, session tracking, and durable project facts.

## Directory Structure

```
.agents/
├── README.md                    # This file — navigation hub
├── memory/
│   └── README.md                # Source of truth for durable project facts
└── SESSIONS/
    ├── README.md                # Session format guide
    └── TEMPLATE.md              # Session file template
```

## For AI Agents

### Before Starting Work

1. Read `.agents/memory/` files relevant to the current task
2. Check today's session file (if exists): `SESSIONS/{{DATE}}.md`
3. Check open tasks: `gh issue list`

### During Work

- Follow coding standards in `CLAUDE.md` (repo root) and `~/.claude/CLAUDE.md`
- Document significant decisions in `.agents/memory/<topic>.md`
- Track new work items as GitHub Issues

### After Work

- Update the session file in `SESSIONS/`
- Update any `.agents/memory/` files whose facts changed
- Note next steps

## Session Files

**ONE FILE PER DAY:** `SESSIONS/YYYY-MM-DD.md`

Multiple sessions on the same day go in the same file as Session 1, Session 2, etc.

## Rules & Standards

Coding standards, "never do" rules, and user preferences live in:

- `CLAUDE.md` (repo root) — project-specific rules
- `~/.claude/CLAUDE.md` — global rules (all projects)

Do not duplicate rules inside `.agents/`.

## Task Tracking

Use GitHub Issues:

```bash
gh issue list
gh issue create --title "..." --body "..."
```

## Tech Stack

{{TECH_STACK}}

---

**Last Updated:** {{DATE}}
