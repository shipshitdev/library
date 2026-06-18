# Validate - Unified Validation Command

Validate the agents folder structure, sessions, and project context.

## Usage

/validate docs      - Validate .agents/ structure and memory files
/validate sessions  - Validate session file naming
/validate issues    - List open GitHub Issues for triage
/validate all       - Run all validation checks

## Option 1: Validate Documentation

Checks that the `.agents/` folder follows the canonical lean structure.

### What This Checks

- Required files exist (`.agents/README.md`)
- `.agents/memory/` exists and contains at least one `.md` file
- `.agents/sessions/` exists
- Each memory file carries a `last_verified` date
- None of the old layout directories exist (any of: `memory/system/`, `TASKS/`, `PRDS/`, `SOP/`, `EXAMPLES/`, `FEEDBACK/` inside `.agents/`)

### Canonical Structure

```
.agents/
├── README.md
├── memory/      ← durable project facts, one topic per *.md file
└── sessions/    ← daily logs YYYY-MM-DD.md
```

Rules and preferences live in `CLAUDE.md` (repo-level and `~/.claude/CLAUDE.md`), not inside `.agents/`.

## Option 2: Validate Sessions

Ensure session files follow ONE FILE PER DAY rule.

### Allowed Filenames

- README.md
- TEMPLATE.md
- YYYY-MM-DD.md (e.g., 2025-01-15.md)

### Forbidden Filenames

- 2025-01-15-feature-name.md
- SECURITY-AUDIT-2025-01-15.md
- Any descriptive names

### Auto-Fix

Violations are consolidated into proper date-based files.

## Option 3: Validate Issues

Fetch open GitHub Issues and flag any that appear stale or missing metadata.

```bash
gh issue list --state open --limit 50
```

Look for:

- Issues with no label (add `backlog`, `bug`, `feature`, etc.)
- Issues open for >30 days with no activity (comment or close)
- Duplicate issues (consolidate)

## Option 4: Validate All

Runs all checks and provides a comprehensive report:

1. `.agents/` structure validation
2. Session file naming validation
3. Open GitHub Issues triage
4. Summary with total issues found

## Error Handling

If validation fails:

- Report specific errors
- Provide fix suggestions
- Offer auto-fix where possible
