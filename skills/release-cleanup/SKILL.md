---
name: release-cleanup
description: Verify a release was fully promoted through develop, staging, and master/main, then prune merged local and remote branches and stale git worktrees. Use when the user asks to clean up branches after a deploy, prune worktrees, remove merged branches, tidy up after promoting develop to staging to master, or confirm nothing stale was left behind before pruning.
compatibility: Requires git and GitHub CLI gh access to the target repository.
metadata:
  version: "1.0.0"
  tags: "git, cleanup, branches, worktrees, release, prune, ci-cd"
allowed-tools: Bash(git *) Bash(gh *)
---

# Release Cleanup

Confirm a release was fully promoted up the branch chain, then prune the branches
and git worktrees that promotion left behind. Verification is a hard gate: never
prune until the chain is proven complete and no in-flight work is stranded.

This skill is standalone and manually triggerable. It does not promote code (use
`release-pr-gates` for that) and does not deploy (use `deploy`). It runs after a
promotion has landed and tidies up.

## Contract

Inputs:

- Repository root with a git remote
- Branch chain to verify, or permission to auto-detect (`develop` -> `staging` -> `master`/`main`)
- Optional mode: `verify` (gate only), `dry-run` (default, plan only), or `prune` (execute after confirmation)

Outputs:

- Promotion verification result per chain hop (complete / incomplete)
- List of stranded branches not merged into `develop` (potential forgotten work)
- Prune plan: local branches, remote branches, and worktrees that are safe to remove
- Final summary of what was removed and what was skipped

Creates/Modifies:

- Deletes local branches merged into the production branch (never the protected set)
- Deletes remote branches merged into the production branch
- Removes git worktrees whose branch is merged or whose upstream is gone, and runs `git worktree prune`
- Prunes stale remote-tracking refs (`git remote prune`)
- Never deletes anything with unmerged commits or a dirty worktree

External Side Effects:

- Reads and deletes GitHub remote branches via `git push origin --delete`
- Reads GitHub branch and PR state to confirm merges
- Does not merge, deploy, or rewrite history

Confirmation Required:

- Before any deletion (local branch, remote branch, or worktree) — always print the dry-run plan and require an explicit yes
- Before pruning when promotion verification is incomplete (default is to STOP, not prompt)
- Before force-removing a worktree or force-deleting a branch (never done automatically)

Delegates To:

- `release-pr-gates` when the chain is NOT fully promoted and the user wants to finish the promotion first
- `gh-fix-ci` when a promotion PR is still open with failing checks
- `git-safety` when a branch about to be pruned may contain secrets in history worth scrubbing first

## When to Use

- After promoting `develop` -> `staging` -> `master` and you want to delete the merged feature/release branches and worktrees
- Manually, any time, to verify the chain is fully promoted and see what is safe to prune
- To confirm "nothing is stale" — that every branch intended for the release actually reached the production branch — before tidying up

Do not use this skill to promote code or to delete unmerged work. It only removes
what is provably merged.

## Safety Model

Protected branches are never deleted:

```
develop  staging  master  main  + the currently checked-out branch + HEAD
```

Hard rules:

1. Pruning uses `git branch --merged` / `git branch -r --merged` against the
   production branch only. A branch with even one commit not in the production
   branch is never listed for deletion.
2. Worktrees with uncommitted changes are never removed. They are reported and skipped.
3. The default mode is `dry-run`: print the exact plan and stop. Deletion only
   happens in `prune` mode after the user confirms the printed plan.
4. Force flags (`git branch -D`, `git worktree remove --force`, `git push --delete`
   of an unmerged branch) are never used automatically. If a branch looks
   important but is unmerged, report it — do not remove it.
5. If promotion verification fails, STOP. Do not offer to prune around it.

## Phase 1: Discover Branches and Refresh State

```bash
gh auth status -h github.com
git status -sb
git remote -v
git fetch --all --prune
gh repo view --json nameWithOwner,defaultBranchRef
git branch -r --list 'origin/develop' 'origin/staging' 'origin/master' 'origin/main'
```

Determine the chain from the branches that actually exist on the remote:

- Production branch = `master` if it exists, else `main`, else the repo default branch.
- Chain = the subset of `develop` -> `staging` -> production that exists.
- If neither `develop` nor `staging` exists (e.g. a master-only repo), the chain
  collapses to "everything is merged into the production branch" and verification
  checks only that.

## Phase 2: Promotion Verification (Hard Gate)

Prove each hop carries no un-promoted commits. Each command must return empty.

```bash
# develop fully promoted into staging? (commits in develop missing from staging)
git log --oneline origin/staging..origin/develop

# staging fully promoted into production? (commits in staging missing from master/main)
git log --oneline origin/master..origin/staging
```

When `staging` does not exist, check `develop` against production directly:

```bash
git log --oneline origin/master..origin/develop
```

Also surface potential forgotten work — branches whose commits never reached
`develop`. These are "stale" candidates the user may have meant to include:

```bash
# remote branches NOT merged into develop (or production if no develop)
git branch -r --no-merged origin/develop --format '%(refname:short)' \
  | grep -vE '^origin/(develop|staging|master|main|HEAD)'
```

Gate outcome:

- Any non-empty promotion hop => promotion is INCOMPLETE. Report exactly which
  commits are un-promoted and STOP. Offer to hand off to `release-pr-gates` to
  finish the promotion. Do not prune.
- Stranded branches not merged into `develop` => report them as a warning. They
  are not pruned (they are unmerged) but the user should decide whether they were
  meant to ship. This is the "nothing is stale" check.
- All hops empty and no surprising stranded branches => verification passes;
  continue to Phase 3.

## Phase 3: Build the Prune Plan (Dry-Run, Default)

Compute the safe-to-remove sets against the production branch only.

```bash
PROD=origin/master   # or origin/main per Phase 1
CURRENT="$(git symbolic-ref --quiet --short HEAD || echo)"
PROTECT='develop|staging|master|main'

# Local branches fully merged into production (excluding protected + current)
git branch --merged "$PROD" --format '%(refname:short)' \
  | grep -vxE "$PROTECT" \
  | { [ -n "$CURRENT" ] && grep -vx "$CURRENT" || cat; }

# Remote branches fully merged into production (excluding protected)
git branch -r --merged "$PROD" --format '%(refname:short)' \
  | sed 's#^origin/##' \
  | grep -vxE "$PROTECT|HEAD"

# Worktrees: list, then classify
git worktree list --porcelain
```

For each worktree other than the main checkout, classify it:

- Branch merged into production AND no uncommitted changes (`git -C <path> status --porcelain` empty) => safe to remove.
- Uncommitted changes => SKIP, report as dirty.
- Branch unmerged => SKIP, report as unmerged.
- Upstream gone (branch deleted on remote) and merged => safe to remove.

Print the plan as three explicit lists — local branches, remote branches,
worktree paths — plus a skipped list with reasons. Then stop and ask for
confirmation. In `dry-run` (default) and `verify` modes, end here.

## Phase 4: Execute Prune (Only in `prune` Mode, After Confirmation)

Only after the user confirms the printed plan:

```bash
# Local merged branches
git branch -d <branch> ...        # -d (safe). Never -D automatically.

# Remote merged branches (origin is HTTPS or SSH; uses configured auth)
git push origin --delete <branch> ...

# Worktrees flagged safe
git worktree remove <path> ...    # never --force; refuses on dirty
git worktree prune

# Drop stale remote-tracking refs
git remote prune origin
git fetch --all --prune
```

Rules during execution:

- If `git branch -d` refuses (not fully merged), do not escalate to `-D`. Report and skip.
- If `git worktree remove` refuses (dirty/locked), do not `--force`. Report and skip.
- Delete remote branches one batch; if a delete fails (protected on the server),
  report it and continue with the rest.

## Modes

- `release-cleanup verify` — Phase 1 + 2 only. Report promotion status and stranded branches. No plan, no deletion.
- `release-cleanup` or `release-cleanup dry-run` — Phases 1-3. Verify, then print the prune plan. No deletion. (Default.)
- `release-cleanup prune` — Phases 1-4. Verify, print plan, confirm, then delete.

If the user explicitly scopes the cleanup ("only worktrees", "local branches
only", "skip remote"), honor it: still run verification, but restrict the plan
and execution to the requested resource types.

## Final Status

Report:

- Repository and production branch used
- Chain verified and each hop's result (complete / incomplete)
- Stranded branches not merged into `develop`, if any
- Local branches deleted / skipped (with reasons)
- Remote branches deleted / skipped (with reasons)
- Worktrees removed / skipped (with reasons)
- Whether anything was blocked and what the user should decide next
