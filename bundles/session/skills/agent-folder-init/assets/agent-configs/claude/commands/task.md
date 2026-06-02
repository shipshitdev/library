# Task Management - Create and Update GitHub Issues

Unified command for creating and updating tasks as GitHub Issues.

## When to Use

Create a task when user:

- Requests a new feature
- Describes a user story
- Asks for an enhancement
- Reports a bug that needs tracking
- Mentions a future improvement

Update a task when user:

- Says mark task X as complete
- Wants to change task status
- Asks to update priority

## Task Creation Workflow

### Step 1: Understand Request

Analyze the request to determine complexity:

- Simple task: One-shot, straightforward (< 1 hour)
- Complex feature: Multi-step, requires planning (> 1 hour)

### Step 2: Gather Requirements

Ask if not clear:

- What is the main goal/outcome?
- What is the priority? (High, Medium, Low)
- Any specific requirements?

### Step 3: Check Existing Context

Read relevant context before creating:

- `.agents/memory/` — architecture docs, existing patterns, deployment constraints
- `CLAUDE.md` — repo rules and standards
- `gh issue list --state open` — avoid duplicating an existing issue

### Step 4: Create GitHub Issue

```bash
gh issue create \
  --title "[Feature Name]" \
  --body "$(cat <<'EOF'
## Overview

[High-level description]

## Requirements

1. [Requirement 1]
2. [Requirement 2]

## Implementation Notes

[Technical approach]

## Files to Modify

- path/to/file.ts — [what changes]

## Testing

- [ ] Test case 1
- [ ] Test case 2
EOF
)" \
  --label "feature" \
  --label "priority:high"
```

### Step 5: Present to User

Show:

- Issue URL and number
- Summary of the task
- Ask if they want to proceed with implementation now

## Task Update Workflow

### Step 1: Identify Issue

```bash
gh issue list --state open
# or search by title
gh issue list --search "keyword"
```

### Step 2: Update Issue

Add a comment with status update:

```bash
gh issue comment <number> --body "Status: In Progress — starting implementation"
```

Close when done:

```bash
gh issue close <number> --comment "Completed in commit abc1234"
```

Add/change labels:

```bash
gh issue edit <number> --add-label "in-progress" --remove-label "backlog"
```

### Step 3: Confirm

Show the issue URL and what was changed.

## Status Labels

- `backlog` — Not started
- `in-progress` — Being worked on
- `needs-review` — Ready for review / testing
- `done` — Complete (closed)
- `blocked` — Waiting on something

## Type Labels

- `feature` — New functionality
- `bug` — Fix existing issue
- `enhancement` — Improve existing
- `task` — General work item
- `migration` — Move/refactor code

## Priority Labels

- `priority:high`
- `priority:medium`
- `priority:low`
- `priority:critical`

## Naming Convention

Issue titles should be short and descriptive:

Good: "Add video generation captions support"
Bad: "Feature", "Task 1"
