---
name: gh-inbox
description: "Collect and triage a GitHub work inbox from assigned issues, review requests, mentions, authored PRs with failing checks, and optional project filters. Use when checking what needs attention across GitHub or prioritizing GitHub tasks."
compatibility: Requires GitHub CLI gh access. The bundled inbox report script runs with Node.js or Bun.
disable-model-invocation: true
allowed-tools: Bash(gh *) Bash(node *) Bash(bun *)
metadata:
  version: "1.0.0"
  tags: "github, inbox, triage, issues, pull-requests"
---

# GH Inbox

Turn scattered GitHub work into a small priority queue.

## Contract

Inputs:

- Optional repository, owner, or project filter
- Optional limit and priority rules

Outputs:

- Prioritized GitHub inbox summary
- Recommended next actions
- Commands for follow-up inspection

Creates/Modifies:

- None in report mode
- May label, comment, assign, close, or move items only after approval

External Side Effects:

- Reads GitHub issues, PRs, reviews, checks, and project membership
- Writes GitHub issue/PR/project state only after approval

Confirmation Required:

- Before editing labels, assignees, comments, project fields, or issue state
- Before rerunning workflows
- Before merging or closing anything

Delegates To:

- `gh-fix-ci` for failing PR checks
- `gh-address-comments` for existing review comments
- `gh-review-suggestions` when a PR needs inline review feedback
- `gh-project-board` when board metadata is missing or inconsistent

## Workflow

1. Verify auth:

   ```bash
   gh auth status -h github.com
   gh api user --jq .login
   ```

2. Generate the inbox:

   ```bash
   node ${CLAUDE_SKILL_DIR}/scripts/gh-inbox-report.mjs
   ```

   Common filters:

   ```bash
   node ${CLAUDE_SKILL_DIR}/scripts/gh-inbox-report.mjs --owner shipshitdev
   node ${CLAUDE_SKILL_DIR}/scripts/gh-inbox-report.mjs --repo shipshitdev/shipcode
   node ${CLAUDE_SKILL_DIR}/scripts/gh-inbox-report.mjs --project shipshitdev/1
   node ${CLAUDE_SKILL_DIR}/scripts/gh-inbox-report.mjs --limit 50
   ```

3. Triage order:
   - Review requests
   - Authored PRs with failing checks
   - Assigned P0/P1 or blocking issues
   - Mentions needing a response
   - Stale assigned issues
   - Project-board items missing status or priority

4. For each item, choose one next action:
   - Inspect
   - Fix
   - Reply
   - Defer
   - Reassign
   - Close

5. Ask before applying any writes. When writing, use the smallest command:

   ```bash
   gh issue edit <number> --add-label "priority:P1"
   gh issue comment <number> --body-file <file>
   gh pr review <number> --comment --body-file <file>
   ```

## Rules

- Prefer a short queue over a complete dump.
- Keep review requests above authored work unless production is blocked.
- Treat failing checks as actionable only after reading the failure.
- Do not close or defer user-facing issues without leaving a reason.
- If GitHub search results are noisy, narrow by `--repo`, `--owner`, or `--project` before making recommendations.
