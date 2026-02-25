# Session Documenter

Document session work to `.agents/SESSIONS/YYYY-MM-DD.md`. Called by `/end` or invoked directly.

## Execution

When invoked, immediately document the current session:

1. **Check for today's file**: `.agents/SESSIONS/YYYY-MM-DD.md`
   - If exists: read it, get the last session number, append new session
   - If missing: create it with the header template

2. **Write the session entry** with ALL of the following sections:

```markdown
## Session N: [Brief Description]

**Status:** Complete

### System Flow

[Mermaid flowchart for features/complex changes, or skip for simple bug fixes]

### Affected Components

| Layer | Components |
|-------|------------|
| Frontend | ... |
| Backend | ... |
| Data | ... |

### What was done

- [x] Task 1
- [x] Task 2

### Files changed

- `path/to/file.ts` - what changed

### Key decisions

- **Decision:** What was decided
  - **Context:** Why this was needed
  - **Rationale:** Why this choice over alternatives

### Mistakes and fixes

- **Mistake:** What happened → **Fix:** How resolved

### Next steps

- [ ] What remains to be done
```

1. **Update the file header summary** at the top with today's work

## Critical Rules

- **ONE FILE PER DAY**: `.agents/SESSIONS/YYYY-MM-DD.md` — never append dates or feature names
- **Append, don't overwrite**: Multiple sessions same day = Session 1, Session 2, etc.
- **Include flowcharts** for new features and multi-component changes (mermaid preferred)
- **Track everything**: files changed, decisions with rationale, mistakes with fixes
- **Never skip "Next steps"**: Always include at least one actionable next step
- **Never include secrets**: Redact API keys, tokens, passwords from session docs

## Required Fields

Every session entry MUST have: session number, brief description, status, "What was done" (1+ item), "Files changed" (1+ file), "Next steps" (1+ item). Decisions and mistakes are recommended when applicable.
