# Merge - Merge ALL Approved Open PRs Into the Trunk

**Default = merge them all.** `/merge` reviews every open pull request targeting
the trunk, shows you one consolidated plan, and after your yes merges the whole
approved set — then prunes the merged branches and stale worktrees left behind.
It is not a single-PR tool and not review-only (that's `/merge review`).

## Usage

```bash
/merge              # merge ALL approved open PRs: review, confirm, merge, prune (default)
/merge review       # plan only — review everything, merge nothing
/merge force        # drain WIP — merge green PRs, narrowly fix red PRs, keep moving
/merge --no-prune   # review + merge all, but skip the prune step
/merge <base>       # use an explicit base branch instead of the auto-detected trunk
```

`review` and `--no-prune` combine with an explicit base, e.g.
`/merge my-branch --no-prune` or `/merge review my-branch`.

`force` is a standalone mode and cannot combine with `review`, `--no-prune`, or
a base override. Dependency order can follow it, for example `/merge force #12
before #18`.

## Workflow

Use the `merge-open-prs` skill.

Exact `/merge force` takes the Force Mode path: snapshot every open PR before
acting, merge independent green PRs first, narrowly fix red PRs, and move on
while unrelated CI remains pending. It stops after queue draining and does not
run branch/worktree cleanup.

All other modes use the confirm-gated sweep:

1. Auto-detect the default/trunk branch via
   `gh repo view --json defaultBranchRef --jq .defaultBranchRef.name`. Stop if it
   is missing, unless the user passed an explicit base that exists.
2. Snapshot every open PR targeting the trunk (number, draft state, mergeability,
   checks, review decision).
3. Classify each: draft, conflicting, checks failing/pending, or candidate.
4. Review every candidate with the `code-review` skill against its diff — the
   same per-PR quick gate `/review prs` runs report-only (via `review-dispatch`).
   Use `/review prs` when you want the sweep without merging.
5. Print one consolidated plan — the PRs that will merge versus the excluded ones
   with a reason each — and wait for explicit confirmation.
6. Merge the approved PRs into the trunk (oldest first), deleting each head branch.
7. Hand off to the `git-cleanup` skill (the `/cleanup` engine) to prune merged
   branches and stale worktrees. It runs its own dry-run and confirmation before
   deleting anything.

## Gates

- Never merge a draft, a conflicted PR, or a PR with failing or pending required
  checks without explicit per-PR confirmation.
- Never force-merge past a protected-branch rule — report the block instead.
- In `/merge force`, `force` means force queue progress. It never authorizes a
  force-push, admin merge, required-check bypass, history rewrite, or deploy.
- All branch and worktree deletion beyond the merged PR's own head branch is
  delegated to `git-cleanup`, which confirms before pruning.
- This command lands PRs onto the trunk only. To cut a release, use the `release`
  skill to tag from trunk after the PRs are merged.

## Command Boundary

`/merge force` is the sole public non-serial queue-drain command.
