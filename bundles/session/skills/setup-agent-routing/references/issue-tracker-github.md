# Issue tracker — GitHub Issues + Projects

> Seed for `docs/agents/issue-tracker.md`. Replace `<owner>`, `<repo>`, and `<N>`
> with this repo's values before writing.

Work is tracked as **GitHub Issues** on `<owner>/<repo>`, visualized on a
**GitHub Projects** kanban board (project #`<N>`) with columns
**Backlog → In Progress → Human Review → Done** (plus **Deferred** for parked work).

## Column → state + board Status map

Status is the board `Status` field (a Projects v2 single-select), the sole source
of truth — not a label.

| Column       | Issue state | Board `Status` |
| ------------ | ----------- | -------------- |
| Backlog      | open        | Backlog        |
| In Progress  | open        | In Progress    |
| Human Review | open        | Human Review   |
| Done         | closed      | Done           |
| Deferred     | open        | Deferred       |

These are the human-facing columns; the AI loop's sub-phases ride as `loop:*` labels
inside In Progress.

Issue state (open/closed) plus the board `Status` field drive column placement.
The `gh` CLI is the agent's interface for every task operation; the board node ids
live in `.github/agent-loop.env`.

## Command vocabulary

```bash
# Create (use --body-file with a heredoc/temp file for multi-line PRDs)
gh issue create --title "<title>" --body-file /tmp/body.md --label "type:feature"

# Read one issue with full comment history (rejection + triage notes live here)
gh issue view <number> --comments

# List the dispatch queue: the gate label intersected with the board's Backlog column
# (see triage-labels.md for the dispatch:claude / dispatch:codex gates)
source .github/agent-loop.env
gh issue list --label "dispatch:claude" --json number,title,labels,assignees --jq '.'
gh project item-list "$PROJECT_NUMBER" --owner "$PROJECT_OWNER" --format json -L 500 \
  | jq -r '.items[] | select(.status == "Backlog") | .content.number'

# Comment (progress updates, claim stamps, completion summaries)
gh issue comment <number> --body "..."

# Apply / remove labels
gh issue edit <number> --add-label "..."
gh issue edit <number> --remove-label "..."

# Close (approve / wontfix)
gh issue close <number> --comment "..."
```

## Placing issues on the board

```bash
# Add an issue to the project board
gh project item-add <N> --owner <owner> --url <issue-url>

# Discover field + item IDs live — never hard-code them
gh project field-list <N> --owner <owner> --format json
gh project item-list <N> --owner <owner> -L 500 --format json   # default limit is 30
```

Use live field IDs from `gh project field-list` and item IDs from
`gh project item-list`. Do not hard-code project field IDs — they differ per board.

## Sub-issues

Link sub-issues using the repository's supported GitHub sub-issue API. If native
sub-issues are unavailable, link children in the parent body and each child body.

## Branch + PR convention

- Branch per task: `feature/<issue-number>-<slug>`.
- Commits reference the issue (`fixes #N`).
- PR opened with `gh pr create --body "Closes #N"`; the link goes in an issue comment.
