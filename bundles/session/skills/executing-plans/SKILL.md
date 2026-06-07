---
name: executing-plans
description: Orchestrate autonomous AI development with task-based workflow and QA gates. Use when implementing a development plan, picking tasks from a queue, or running multi-platform parallel execution with QA gates.
metadata:
  version: "2.1.0"
  tags: "execution, planning, agents"
---

# Executing Plans

Autonomous task execution with QA gates across multiple AI platforms.

## Overview

The AI Development Loop enables fully autonomous feature development where:

- AI agents pick up and implement tasks from a GitHub Issues queue
- You do QA only (approve or reject issues in the Testing column)
- Multiple platforms (Claude CLI, Cursor, Codex) can work in parallel
- Rate limits are maximized by switching between platforms

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   BACKLOG   │────▶│   TO DO     │────▶│  TESTING    │────▶│    DONE     │
│             │     │             │     │             │     │             │
│ Issues open │     │ Agent picks │     │ YOU review  │     │  Shipped    │
│  (no label) │     │ & builds    │     │ & approve   │     │  (closed)   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                          │                   │
                    ┌─────┴─────┐       ┌─────┴─────┐
                    │  Claude   │       │  Reject   │
                    │  Cursor   │       │  → To Do  │
                    │  Codex    │       └───────────┘
                    └───────────┘
```

Columns map to GitHub Issues state + labels:

| Column  | Issue state | Label            |
| ------- | ----------- | ---------------- |
| Backlog | open        | _(none)_         |
| To Do   | open        | `status:todo`    |
| Testing | open        | `status:testing` |
| Done    | closed      | _(none needed)_  |

Use a GitHub Projects board with these columns for a visual Kanban view.

## Task Lifecycle

### 1. Task Creation

Each task is a GitHub Issue. The issue body carries structured metadata:

```markdown
## Task: [Feature Name]

**Priority:** High | Medium | Low
**PRD:** #[linked-issue-number] or URL

### Progress

**Agent-Notes:** [real-time updates]

### QA Checklist

- [ ] Code compiles/lints
- [ ] Tests pass (CI)
- [ ] User acceptance
- [ ] Visual review

### Rejection History

[Add rejection notes as comments; rejection count tracked via `rejection:N` label]
```

Create issues with:

```bash
gh issue create --title "[Feature Name]" --body "..." --label "status:todo" --assignee "@me"
```

### Agent-ready issue contract

Before an issue enters `status:todo`, make sure it is ready for an agent:

- It has an agent brief or PRD link with current behavior, desired behavior, acceptance criteria, verification, and out of scope.
- It identifies key public contracts: API shape, CLI command, UI behavior, config key, data model, or generated artifact.
- It avoids brittle instructions such as line numbers and file-by-file scripts unless the path is the product.
- It is marked `AFK` when an agent can complete it from written context, or `HITL` when a human decision is required.
- It is a vertical slice with a verifiable result, not a horizontal layer task.

### 2. Task Claiming

When an agent runs `/loop`:

1. Lists open issues labeled `status:todo` via `gh issue list --label status:todo`
2. Sorts by priority label (High > Medium > Low)
3. Skips issues already assigned with a `claimed` label added < 30 min ago (check the claim comment timestamp)
4. Assigns itself and adds a `claimed` label + comment with ISO timestamp

```bash
gh issue edit <number> --add-label "claimed"
gh issue comment <number> --body "Claimed-By: claude-cli | Claimed-At: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

### 3. Implementation

Agent works on the task:

1. Reads the issue body and linked PRD issue/URL
2. Reads all comments, especially prior rejection or triage notes
3. Checks `.agents/SESSIONS/` for related past work
4. Checks `.out-of-scope/` if the issue appears to revive a previously rejected enhancement
5. Chooses the narrowest verification loop before editing
6. Uses `tdd` for behavior changes when the behavior is clear enough to test first
7. Implements the feature/fix
8. Appends progress to the issue as comments (`gh issue comment <number> --body "..."`)
9. Creates branch and commits

### 4. Quality Check

Before moving to Testing:

1. Runs qa-reviewer skill
2. Checks off QA-Checklist items in the issue body (edit the issue to tick boxes)
3. Ensures code compiles/lints

### 5. Completion

Agent finalizes:

1. Removes `status:todo` label, adds `status:testing` label
2. Posts a completion comment with timestamp and final summary
3. Removes the `claimed` label
4. Prompts for next action

```bash
gh issue edit <number> --remove-label "status:todo,claimed" --add-label "status:testing"
gh issue comment <number> --body "Completed-At: $(date -u +%Y-%m-%dT%H:%M:%SZ)\n\n**Summary:** ..."
```

### 6. QA Gate (Your Turn)

In the GitHub Projects board (or `gh issue list --label status:testing`):

1. Review the Testing column
2. Open the issue to see agent notes and the linked PR
3. Check the PR diff
4. **Approve**: Remove `status:testing`, close the issue (or move to Done column)
5. **Reject**: Remove `status:testing`, add `status:todo`, post a rejection comment with notes

### 7. Rejection Handling

When rejected:

1. Issue moves back to To Do (`status:todo` label restored)
2. Rejection count bumped via label (`rejection:1`, `rejection:2`, …) or tracked in comments
3. Rejection note added as a comment on the issue
4. Next `/loop` picks up the issue with full comment history as context

If the rejection means the requested enhancement should not be built, do not
keep cycling it through To Do. Close it as `wontfix` and, when the reasoning is
durable, record the concept under `.out-of-scope/<concept>.md` so future triage
does not re-litigate the same request.

## Multi-Platform Strategy

### Platform Strengths

| Platform   | Best For                             |
| ---------- | ------------------------------------ |
| Claude CLI | Complex logic, backend, architecture |
| Cursor     | UI components, styling, visual work  |
| Codex      | Bulk refactoring, migrations, docs   |

### Parallel Execution

Multiple platforms can work simultaneously:

- Each claims different issues (assignee + `claimed` label)
- Claim comments with timestamps prevent conflicts (30-min lock)
- Shared state lives in GitHub Issues — visible to all platforms

### Rate Limit Handling

When rate limited:

1. Agent posts progress to the issue as a comment
2. Removes the `claimed` label (releases claim)
3. Suggests switching platform
4. User continues with different platform; new agent reads comment history for context

## Daily Workflow

### Morning QA Session

1. Open the GitHub Projects board (or run `gh issue list --label status:testing`)
2. Review issues in the Testing column
3. Approve good work → close the issue (Done)
4. Reject with notes → comment + restore `status:todo` label

### Throughout Day

```bash
# Claude CLI
claude
> /loop   # Process one issue
> /loop   # Next issue
# Rate limited? Switch to Cursor
```

```bash
# Quick queue check at any time
gh issue list --label status:todo --assignee @me
gh issue list --label status:testing
```

### Rate Limit Strategy

```
Claude limit? → Switch to Cursor
Cursor limit? → Switch to Codex
All limited? → QA time (review Testing issues)
```

## Integration Points

### GitHub Issues + Projects

- GitHub Projects board provides the visual Kanban view (Backlog / To Do / Testing / Done columns)
- Issue state (open/closed) + labels drive column placement
- `gh` CLI is the agent's interface for all task operations
- PR links go in issue comments or the issue body

### Existing Skills

- **qa-reviewer**: 6-phase quality verification
- **session-documenter**: Auto-document completed work
- **rules-capture**: Learn from rejection feedback

### Git Workflow

- Branch per task: `feature/[issue-number]-[slug]`
- Commits with clear messages referencing the issue (`fixes #N`)
- PR linked in issue via `gh pr create --body "Closes #N"`

## Not a Daemon

Important: `/loop` is NOT a background process.

- Each invocation handles ONE issue
- Returns control to user
- User decides to continue or stop
- Respects "never run background processes" rule

## Claim Expiration

Claims expire after 30 minutes:

- Check the `Claimed-At` timestamp in the most recent claim comment on the issue
- If > 30 min old and `claimed` label is still present, the claim is stale — safe to take over
- Handles agent crashes and rate limit interruptions
- Previous comments provide full context for pickup by any platform

## Best Practices

### For Task Creation

- Write clear, actionable issue titles and bodies
- Link to the PRD issue or URL in the body
- Apply the correct priority label (`priority:high`, `priority:medium`, `priority:low`)
- Include testing criteria in the QA Checklist section
- Include explicit out-of-scope boundaries
- Prefer vertical slices that can be verified independently
- Split `HITL` decisions from `AFK` implementation work

### For Agents

- Read the issue body and all comments before starting
- Post progress updates as issue comments regularly
- Run qa-reviewer before completing
- Create clean, focused commits referencing the issue number

### For QA (You)

- Review the linked PRD alongside the implementation PR
- Provide specific rejection feedback in issue comments
- Approve incrementally (don't batch)
- Keep the Testing column short
