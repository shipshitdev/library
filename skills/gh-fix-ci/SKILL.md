---
name: gh-fix-ci
description: "GitHub Actions CI fixes."
---

# GH Fix CI

Use this skill to diagnose failing GitHub Actions checks on a PR and propose a fix plan.

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
