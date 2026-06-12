---
name: gh-address-comments
description: >-
  Resolves GitHub PR review and issue comments by fetching threads, mapping them
  to code, proposing fixes, and drafting replies for approval. Triggers when the
  user asks to address PR comments, respond to review feedback, fix review
  threads, or resolve GitHub comment requests.
disable-model-invocation: true
metadata:
  version: "1.0.0"
  tags: "github, pull-requests, review-comments"
---

# GH Address Comments

Use this skill when a user wants help resolving PR review or issue comments via the GitHub CLI.

## Contract

Inputs:

- Current branch or PR URL/number
- Optional review thread IDs or issue comment IDs

Outputs:

- Review-thread summary
- Mapped code changes
- Draft reply text for each resolved thread

Creates/Modifies:

- Local code changes when fixing review comments
- Does not push or post replies without approval

External Side Effects:

- Reads GitHub PR review and issue comments
- May post GitHub replies only after approval

Confirmation Required:

- Before changing code when fixes are not obvious
- Before pushing
- Before posting replies to GitHub

Delegates To:

- `code-review` to validate proposed fixes
- `qa-reviewer` before final response
- `gh-fix-ci` if fixes cause or reveal CI failures

## Workflow

1) Verify auth:
   - `gh auth status -h github.com`
   - If not logged in, ask the user to run `gh auth login`.
2) Identify the PR:
   - `gh pr view --json number,title,url`
   - If no PR is found, ask for the PR URL.
3) Collect comments:
   - Review comments: `gh api repos/{owner}/{repo}/pulls/{number}/comments`
   - Issue comments: `gh api repos/{owner}/{repo}/issues/{number}/comments`
4) Summarize each thread and map to code changes.
5) Propose fixes and get user approval before pushing changes.
6) Draft reply text for each thread and ask before posting to GitHub.

## Notes

- Prefer quoting exact comment text in your summary.
- Keep replies short and specific to the change.
