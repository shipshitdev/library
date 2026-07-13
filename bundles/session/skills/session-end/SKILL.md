---
name: session-end
description: >-
  Save session wrap-up documentation before clearing context by running the
  session-documenter workflow and writing `.agents/sessions/YYYY-MM-DD.md`.
  Use when ending a session, preparing to run `/clear`, or asked to document
  what changed before context is reset.
metadata:
  version: "1.0.0"
  tags: "session, workflow, documentation, productivity"
---

# Session End

Document your session before clearing context. This is a TWO-STEP process: `/session-end` documents, then user manually runs `/clear`.

## Contract

Inputs:

- Redacted session context and changed-file summary
- Pending tasks, blockers, decisions, and reusable rules/workflows

Outputs:

- Saved session documentation with secrets removed
- Clear next-step instruction for context reset

Creates/Modifies:

- `.agents/sessions/YYYY-MM-DD.md`
- Related `.agents/` task or summary files when delegated to `session-documenter`

External Side Effects:

- None

Confirmation Required:

- Before rewriting existing session entries
- Before promoting captured rules or skills outside session docs

Delegates To:

- `session-documenter`
- `rules-capture` for unresolved reusable preferences
- `skill-capture` for reusable workflows that should become skills

## Workflow

### Step 1: Document Session

When invoked, immediately:

1. Run the `session-documenter` skill to save a redacted session summary
2. Let it complete — it will document tasks, decisions, files changed, patterns, and mistakes without storing secrets
3. Confirm documentation saved

> **Cross-platform note**: If your agent platform doesn't support skill invocation, follow the session-documenter workflow manually by reading the `session-documenter` skill definition.

### Step 2: Remind User to Clear

After documentation is complete, tell the user:

```
Session documented to .agents/sessions/YYYY-MM-DD.md

NEXT STEP: Run /clear to clear the conversation context.
Your session is safely preserved and will be loaded on next /session-start.
```

## Important Notes

- **ONE FILE PER DAY**: Session documenter appends to the same day's file
- **Multiple invocations**: Each one adds a new session entry
- **Does NOT clear context**: User must run `/clear` manually after
- **Redaction is mandatory**: Do not store API keys, tokens, passwords, cookies,
  private credentials, or secret values from the conversation. Replace them with
  `[REDACTED_SECRET]` and summarize the surrounding context.

## Related Skills

- **session-start** — Loads preferences and today's session after clearing
- **session-documenter** — The underlying documentation skill
