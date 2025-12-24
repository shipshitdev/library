# {{PROJECT_NAME}} - Agent Documentation Hub

**Welcome to the {{PROJECT_NAME}} workspace!**

This is the `.agent/` folder containing AI agent documentation, session tracking, and project rules.

## Quick Start

**READ FIRST:** `SYSTEM/ai/SESSION-QUICK-START.md`

## Directory Structure

```
.agent/
├── README.md                    # This file - Navigation hub
├── SYSTEM/
│   ├── RULES.md                 # Coding standards (READ THIS)
│   ├── ARCHITECTURE.md          # What's implemented
│   ├── SUMMARY.md               # Current state
│   ├── ai/                      # AI agent protocols
│   ├── architecture/            # ADRs and project map
│   ├── critical/                # Critical rules (NEVER DO)
│   └── quality/                 # Security and quality
├── TASKS/
│   ├── README.md                # Task management guide
│   └── INBOX.md                 # Quick task capture
├── SESSIONS/
│   ├── README.md                # Session format guide
│   └── TEMPLATE.md              # Session file template
├── SOP/                         # Standard operating procedures
├── EXAMPLES/                    # Code patterns
└── FEEDBACK/                    # Improvement tracking
```

## For AI Agents

### Before Starting Work

1. Read `SYSTEM/ai/SESSION-QUICK-START.md`
2. Check `SYSTEM/critical/CRITICAL-NEVER-DO.md`
3. Read today's session file (if exists): `SESSIONS/{{DATE}}.md`

### During Work

- Follow patterns in `SYSTEM/RULES.md`
- Track tasks in `TASKS/`
- Document decisions

### After Work

- Update session file in `SESSIONS/`
- Mark completed tasks
- Note next steps

## Session Files

**ONE FILE PER DAY:** `SESSIONS/YYYY-MM-DD.md`

Multiple sessions on the same day go in the same file as Session 1, Session 2, etc.

## Tech Stack

{{TECH_STACK}}

---

**Last Updated:** {{DATE}}
