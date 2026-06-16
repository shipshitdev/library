# Issue tracker — GitHub Issues + Projects

> Seed for `docs/agents/issue-tracker.md`. Replace `<owner>`, `<repo>`, and `<N>`
> with this repo's values before writing.

Work is tracked as **GitHub Issues** on `<owner>/<repo>`, visualized on a
**GitHub Projects** kanban board (project #`<N>`) with columns
**Backlog → To Do → Testing → Done**.

## Column → state + label map

| Column  | Issue state | Label            |
| ------- | ----------- | ---------------- |
| Backlog | open        | _(none)_         |
| To Do   | open        | `status:todo`    |
| Testing | open        | `status:testing` |
| Done    | closed      | _(none needed)_  |

Issue state (open/closed) plus labels drive column placement. The `gh` CLI is the
agent's interface for every task operation.

## Command vocabulary

```bash
# Create (use --body-file with a heredoc/temp file for multi-line PRDs)
gh issue create --title "<title>" --body-file /tmp/body.md --label "feature"

# Read one issue with full comment history (rejection + triage notes live here)
gh issue view <number> --comments

# List the dispatch queue (see triage-labels.md for the ready-for-agent gate)
gh issue list --label "ready-for-agent" --label "status:todo" \
  --json number,title,labels,assignees --jq '.'

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
gh project item-list <N> --owner <owner> --limit 100 --format json
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
