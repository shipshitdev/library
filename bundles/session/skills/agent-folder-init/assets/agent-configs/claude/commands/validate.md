# Validate - Unified Validation Command

Validate documentation, sessions, and tasks.

## Usage

/validate docs      - Validate documentation structure
/validate sessions  - Validate session file naming
/validate tasks     - Validate task files
/validate all       - Run all validation checks

## Option 1: Validate Documentation

Checks required files and broken links.

### What This Checks

- Required files exist (.agents/README.md, etc.)
- Internal links work
- Proper folder organization

### Files to Check

Workspace level:

- .agents/README.md
- .agents/SYSTEM/ directory
- .agents/TASKS/ directory
- .agents/SESSIONS/ directory

Project level:

- <project>/.agents/README.md
- <project>/.agents/SYSTEM/SUMMARY.md

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

## Option 3: Validate Tasks

Validate task file format and metadata.

### What This Checks

- Kanban Markdown format
- Required metadata present (ID, Label, Type, Status, Priority)
- Valid status values (Backlog, To Do, Testing, Done)
- Valid type values (Feature, Bug, Enhancement, Task)
- Valid priority values (High, Medium, Low)

### Valid Values

Status: Backlog, To Do, Testing, Done, Blocked
Type: Feature, Bug, Enhancement, Task, Migration
Priority: High, Medium, Low, CRITICAL

## Option 4: Validate All

Runs all validation checks and provides comprehensive report:

1. Documentation validation
2. Session validation
3. Task validation
4. Summary with total issues found

## Error Handling

If validation fails:

- Report specific errors
- Provide fix suggestions
- Offer auto-fix where possible
