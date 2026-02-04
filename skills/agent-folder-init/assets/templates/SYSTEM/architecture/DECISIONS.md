# Architectural Decision Records (ADRs)

**Purpose:** Document significant architectural decisions.
**Last Updated:** {{DATE}}

---

## How to Use

When making a significant architectural decision, add an entry below using this format:

```markdown
## ADR-XXX: Title

**Date:** YYYY-MM-DD
**Status:** Proposed / Accepted / Deprecated / Superseded

### Context
What is the issue that we're seeing that is motivating this decision?

### Decision
What is the change that we're proposing and/or doing?

### Consequences
What becomes easier or more difficult because of this change?

### Alternatives Considered
What other options were considered?
```

---

## Decisions

### ADR-001: Use .agents/ Folder for AI Documentation

**Date:** {{DATE}}
**Status:** Accepted

#### Context

Need a structured way to organize AI agent documentation, session tracking, and project rules.

#### Decision

Use a `.agents/` folder at the project root with standardized subdirectories:

- `SYSTEM/` for rules and architecture
- `TASKS/` for task tracking
- `SESSIONS/` for daily session documentation
- `SOP/` for standard procedures

#### Consequences

- **Easier:** AI agents have consistent documentation structure
- **Easier:** Session continuity across conversations
- **More difficult:** Initial setup overhead

#### Alternatives Considered

- Inline documentation in code (rejected: not AI-friendly)
- Single README (rejected: doesn't scale)
- Wiki (rejected: separate from codebase)

---

<!-- Add new ADRs above this line -->
