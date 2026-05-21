---
name: gh-fix-ci
description: "GitHub Actions CI fixes."
---

# GH Fix CI

Use this skill to diagnose failing GitHub Actions checks on a PR and propose a fix plan.

## Contract

Inputs:

- Current branch or PR URL/number
- Optional failed run ID or job ID

Outputs:

- Failed check summary
- Root cause and impacted files
- Fix plan or applied local fix summary

Creates/Modifies:

- Local code/config changes only when the fix is clear or explicitly requested
- Does not rerun CI without approval

External Side Effects:

- Reads GitHub PR checks and Actions logs
- May rerun workflows only after approval

Confirmation Required:

- Before rerunning workflows
- Before pushing
- Before changing broad CI/deployment configuration

Delegates To:

- `testing-cicd-init` when baseline CI is missing
- `deployment-composer` when failures block a release
- `code-review` for risky fixes

## Workflow

1) Verify auth:
   - `gh auth status -h github.com`
2) Identify the PR:
   - `gh pr view --json number,title,url`
   - If no PR is found, ask for the PR URL.
3) List checks:
   - `gh pr checks`
4) For GitHub Actions failures, fetch logs:
   - `gh run view <run-id> --log`
   - If you only have a job id: `gh run view --job <job-id> --log`
5) Summarize the root cause and impacted files.
6) Propose a fix plan and get user approval before changing code.
7) For external checks (non-GitHub Actions), report the details URL and mark as out of scope.

## Notes

- Do not rerun CI unless the user asks.
- Keep the failure summary concise and actionable.
