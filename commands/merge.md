# Merge - Review and Land Open PRs Into Develop

Review every open pull request targeting the develop branch, merge the approved
ones into develop, then prune the merged branches and stale worktrees left
behind. One confirm-gated sweep instead of merging PRs one by one.

## Usage

```bash
/merge          # review all open PRs into develop, merge approved, then prune (default)
/merge review   # review only — print the plan, merge nothing
/merge merge    # review + merge, skip the prune
/merge <base>   # use an explicit base branch instead of develop
```

## Workflow

Use the `merge-open-prs` skill.

1. Auto-detect the `develop` branch on the remote. Stop if it is missing, unless
   the user passed an explicit base that exists.
2. Snapshot every open PR targeting develop (number, draft state, mergeability,
   checks, review decision).
3. Classify each: draft, conflicting, checks failing/pending, or candidate.
4. Review every candidate with the `code-review` skill against its diff.
5. Print one consolidated plan — the PRs that will merge versus the excluded ones
   with a reason each — and wait for explicit confirmation.
6. Merge the approved PRs into develop (oldest first), deleting each head branch.
7. Hand off to the `release-cleanup` skill to prune merged branches and stale
   worktrees. It runs its own dry-run and confirmation before deleting anything.

## Gates

- Never merge a draft, a conflicted PR, or a PR with failing or pending required
  checks without explicit per-PR confirmation.
- Never force-merge past a protected-branch rule — report the block instead.
- All branch and worktree deletion beyond the merged PR's own head branch is
  delegated to `release-cleanup`, which confirms before pruning.
- This command lands PRs onto develop only. To promote develop onward to staging
  or production, use the `release-pr-gates` skill.
