# {{PROJECT_NAME}} - Agent Documentation Hub

**Welcome to the {{PROJECT_NAME}} workspace!**

This is the `.agents/` folder — source of truth for AI agent context, session tracking, and durable project facts.

## Directory Structure

```
.agents/
├── README.md                    # This file — navigation hub
├── memory/
│   └── README.md                # Source of truth for durable project facts
└── sessions/
    ├── README.md                # Session format guide
    └── TEMPLATE.md              # Session file template
```

## For AI Agents

### Before Starting Work

1. Read `.agents/memory/` files relevant to the current task
2. Check today's session file (if exists): `sessions/{{DATE}}.md`
3. Check open tasks: `gh issue list`

### During Work

- Follow shared coding standards in the applicable `AGENTS.md`; load a
  platform-specific entry file only when the selected harness requires one
- Document significant decisions in `.agents/memory/<topic>.md`
- Track new work items as GitHub Issues

### After Work

- Update the session file in `sessions/`
- Update any `.agents/memory/` files whose facts changed
- Note next steps

## Session Files

**ONE FILE PER DAY:** `sessions/YYYY-MM-DD.md`

Multiple sessions on the same day go in the same file as Session 1, Session 2, etc.

## Rules & Standards

Coding standards, "never do" rules, and user preferences live in:

- `AGENTS.md` (repo root or nearest parent) — shared project instructions
- `AGENTS.override.md` — scoped replacement instructions, only where intentionally present
- Platform-specific entry files — optional, generated only for an explicitly selected
  supported harness

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
