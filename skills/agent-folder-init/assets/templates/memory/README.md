# memory/

**Purpose:** Source of truth for durable project context.

Each file covers one topic. AI agents read this directory before starting work.

## Conventions

- **One file per topic:** `architecture.md`, `deployment.md`, `entities.md`, `migrations.md`, etc.
- **Every file must carry:** `last_verified: YYYY-MM-DD` in the front matter or as a trailing line.
- **Transient facts** (e.g., in-progress migration notes) add `status: temporary` — verify before citing if the date is >30 days old.

## What Goes Here

Durable facts that are NOT rules:

- Architecture decisions and current shape of the system
- Deployment steps, environments, and gotchas
- Data entities and their relationships
- Migration plans and current status
- Known gotchas and non-obvious constraints

## What Does NOT Go Here

- Coding standards and "never do" rules → `CLAUDE.md` (repo root or `~/.claude/CLAUDE.md`)
- Task tracking → GitHub Issues (`gh issue list`, `gh issue create`)
- Session logs → `.agents/sessions/YYYY-MM-DD.md`

---

**Last Updated:** {{DATE}}
