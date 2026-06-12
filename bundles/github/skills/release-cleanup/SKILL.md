---
name: release-cleanup
description: Verify a release was fully promoted through develop, staging, and master/main, then prune merged local and remote branches and stale git worktrees. Squash-merge aware — uses GitHub PR merge state as the merge oracle, not commit ancestry. Use when the user asks to clean up branches after a deploy, prune worktrees, remove merged branches, tidy up after promoting develop to staging to master, or confirm nothing stale was left behind before pruning.
compatibility: Requires git, GitHub CLI gh, and jq access to the target repository.
metadata:
  version: "2.0.0"
  tags: "git, cleanup, branches, worktrees, release, prune, ci-cd, squash-merge"
allowed-tools: Bash(git *) Bash(gh *) Bash(jq *)
disable-model-invocation: true
---

# Release Cleanup

Confirm a release was fully promoted up the branch chain, then prune the branches
and git worktrees that promotion left behind. Verification is a hard gate: never
prune until each branch's work is proven to have reached the production branch and
no in-flight work is stranded.

This skill is standalone and manually triggerable. It does not promote code (use
`release-pr-gates` for that) and does not deploy (use `deploy`). It runs after a
promotion has landed and tidies up.

## The Merge Oracle (read this first)

**Commit ancestry is NOT a reliable merge signal.** GitHub's default merge mode is
**squash**, which collapses a branch into a single new commit on the base. After a
squash merge the branch tip is *not* an ancestor of the base, so `git branch
--merged` / `--no-merged` and `A..B` ranges all report a fully-merged branch as
**unmerged**. Rebase-merges have the same property.

Consequence if you trust ancestry on a squash repo:

- Merged branches look "stranded" → false alarms about forgotten work.
- The prune set is empty → the skill deletes nothing and is useless.
- `git branch -d` refuses every local merged branch.

Therefore this skill's merge oracle is **GitHub PR state first, ancestry second**:

A branch's work is IN the production branch iff EITHER

1. its most-recent PR is `MERGED` and that PR's `mergeCommit` is an ancestor of the
   production branch (covers squash, rebase, and merge-commit), OR
2. the branch tip is an ancestor of the production branch (covers
   no-PR fast-forwards and merge-commit merges that predate the PR API).

Only branches that satisfy this are prunable. Everything else is reported, never
deleted.

## Contract

Inputs:

- Repository root with a git remote
- Branch chain to verify, or permission to auto-detect (`develop` -> `staging` -> `master`/`main`)
- Optional mode: `verify` (gate only), `dry-run` (default, plan only), or `prune` (execute after confirmation)

Outputs:

- Promotion verification result per chain hop (complete / incomplete), with a squash caveat where ancestry and PR state disagree
- Branch classification: prunable (in prod), merged-but-not-yet-promoted, in-flight (open PR), and genuinely stranded
- Prune plan: local branches, remote branches, and worktrees that are safe to remove
- Final summary of what was removed and what was skipped

Creates/Modifies:

- Deletes local branches whose work is proven in the production branch (never the protected set)
- Deletes remote branches whose work is proven in the production branch
- Removes git worktrees whose branch is proven-merged or whose upstream is gone, and runs `git worktree prune`
- Prunes stale remote-tracking refs (`git remote prune`)
- Never deletes anything not proven-in-prod or with a dirty worktree

External Side Effects:

- Reads PR + branch state from GitHub; deletes remote branches via `git push origin --delete`
- Does not merge, deploy, or rewrite history

Confirmation Required:

- Before any deletion (local branch, remote branch, or worktree) — always print the dry-run plan and require an explicit yes
- Before pruning when promotion verification is incomplete (default is to STOP, not prompt)
- Before force-removing a worktree (never done automatically)

Delegates To:

- `release-pr-gates` when the chain is NOT fully promoted and the user wants to finish the promotion first
- `gh-fix-ci` when a promotion PR is still open with failing checks
- `git-safety` when a branch about to be pruned may contain secrets in history worth scrubbing first

## When to Use

- After promoting `develop` -> `staging` -> `master` and you want to delete the merged feature/release branches and worktrees
- Manually, any time, to verify the chain is fully promoted and see what is safe to prune
- To confirm "nothing is stale" — that every branch intended for the release actually reached the production branch — before tidying up

Do not use this skill to promote code or to delete unmerged work. It only removes
what is provably in the production branch.

## Safety Model

Protected branches are never deleted:

```
develop  staging  master  main  + the currently checked-out branch + HEAD
```

Hard rules:

1. Merge detection uses the **Merge Oracle** above (PR state first, ancestry
   second), never `git branch --merged` alone. A branch is prunable only when its
   work is proven to be in the production branch.
2. Worktrees with uncommitted changes are never removed. They are reported and skipped.
3. The default mode is `dry-run`: print the exact plan and stop. Deletion only
   happens in `prune` mode after the user confirms the printed plan.
4. `git branch -D` (force local delete) is used ONLY for a local branch the oracle
   has proven is in the production branch — squash/rebase merges legitimately
   require it because `-d` cannot see them. For any branch NOT proven-in-prod,
   force flags are never used; report it instead.
5. `git worktree remove --force` and deleting a remote branch the oracle has NOT
   proven-in-prod are never done automatically.
6. If promotion verification fails, STOP. Do not offer to prune around it.

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

Snapshot every PR once — this is the data the Merge Oracle runs against:

```bash
gh pr list --state all --limit 1000 \
  --json number,headRefName,baseRefName,state,mergedAt,mergeCommit \
  > /tmp/rc_prs.json
```

Raise `--limit` if the repo has more open+closed PRs than that.

## Phase 2: Promotion Verification (Hard Gate)

### 2a. Trunk hops

Prove each trunk hop carries no un-promoted commits. Ancestry is the first signal,
but trunk promotions are occasionally squash-merged too, so corroborate any
non-empty result against the latest merged promotion PR for that hop before
declaring the release incomplete.

```bash
# develop -> staging
git log --oneline origin/staging..origin/develop
gh pr list --base staging --head develop --state merged --limit 1 \
  --json number,mergedAt,mergeCommit

# staging -> production
git log --oneline origin/master..origin/staging
gh pr list --base master --head staging --state merged --limit 1 \
  --json number,mergedAt,mergeCommit
```

When `staging` does not exist, check `develop` against production directly
(`origin/master..origin/develop` + the `--base master --head develop` PR).

Interpreting a non-empty hop:

- The listed commits are genuine direct commits on the lower branch not yet in the
  upper one => promotion INCOMPLETE. Report the commits and STOP.
- The listed commits all belong to PRs already squash-merged up the chain => an
  ancestry artifact, not a real gap. Note the caveat and treat the hop as complete.
- Distinguish the two by checking whether each ahead-commit's PR (if any) is already
  merged into the upper branch.

### 2b. Branch classification (the "nothing is stale" check)

Run the Merge Oracle over every non-protected remote branch. Do NOT use
`git branch -r --no-merged` for this — it lies on squash repos.

```bash
PROD=origin/master   # or origin/main per Phase 1

classify_branch() {        # arg: branch name without origin/
  local b="$1" rec st mc base num
  rec=$(jq -c --arg b "$b" \
    '[.[]|select(.headRefName==$b)]|sort_by(.number)|last' /tmp/rc_prs.json)

  if [ -z "$rec" ] || [ "$rec" = "null" ]; then
    git merge-base --is-ancestor "refs/remotes/origin/$b" "$PROD" 2>/dev/null \
      && { echo "PRUNABLE_NO_PR_FF"; return; }
    git merge-base --is-ancestor "refs/remotes/origin/$b" origin/develop 2>/dev/null \
      && echo "IN_DEVELOP_NO_PR" || echo "STRANDED_NO_PR"
    return
  fi

  st=$(jq -r '.state' <<<"$rec")
  mc=$(jq -r '.mergeCommit.oid // empty' <<<"$rec")
  base=$(jq -r '.baseRefName' <<<"$rec")
  num=$(jq -r '.number' <<<"$rec")

  case "$st" in
    OPEN)   echo "IN_FLIGHT_OPEN_PR(#$num->$base)";;
    CLOSED) git merge-base --is-ancestor "refs/remotes/origin/$b" "$PROD" 2>/dev/null \
              && echo "PRUNABLE_CLOSED_PR_IN_PROD(#$num)" \
              || echo "STRANDED_CLOSED_UNMERGED(#$num)";;
    MERGED)
      if [ -n "$mc" ] && git merge-base --is-ancestor "$mc" "$PROD" 2>/dev/null; then
        echo "PRUNABLE_IN_PROD(#$num)"
      elif git merge-base --is-ancestor "refs/remotes/origin/$b" "$PROD" 2>/dev/null; then
        echo "PRUNABLE_IN_PROD(#$num)"
      else
        echo "MERGED_NOT_YET_IN_PROD(#$num->$base)"
      fi;;
  esac
}

# Drive it over all non-protected remote branches:
git branch -r --format '%(refname:short)' \
  | grep -v -- '->' \
  | sed 's#^origin/##' \
  | grep -vxE 'origin|develop|staging|master|main|HEAD' \
  | while read -r b; do printf '%-50s %s\n' "$b" "$(classify_branch "$b")"; done
```

Buckets and what they mean:

- `PRUNABLE_*` — work is in the production branch. Safe to prune.
- `MERGED_NOT_YET_IN_PROD` — PR merged into develop/staging but not yet promoted to
  production. NOT prunable yet; this is a real "release not fully promoted" signal
  for that branch. Report it.
- `IN_FLIGHT_OPEN_PR` — open PR. In progress. Skip, never prune.
- `IN_DEVELOP_NO_PR` — landed on develop with no PR (direct push). Treat like
  develop content; prune only if also in prod by ancestry.
- `STRANDED_*` — no merged PR and not in develop. **Genuinely forgotten work.**
  Report loudly, never prune.

Gate outcome:

- Any real (non-artifact) incomplete trunk hop => STOP. Offer `release-pr-gates`.
- Any `STRANDED_*` branch => report as a warning; the user decides whether it was
  meant to ship. This is the "nothing is stale" guarantee.
- Trunk hops complete (or only artifacts) and stranded set understood => continue.

## Phase 3: Build the Prune Plan (Dry-Run, Default)

The prunable remote set is exactly the branches the oracle tagged `PRUNABLE_*` in
Phase 2b. Now compute the local and worktree sets the same way.

```bash
CURRENT="$(git symbolic-ref --quiet --short HEAD || echo)"
PROTECT="develop|staging|master|main|${CURRENT:-__none__}"

# Local branches — classify each with the SAME oracle (reuse classify_branch,
# but test the LOCAL ref, not origin/, for the ancestry fallback).
git branch --format '%(refname:short)' \
  | grep -vxE "$PROTECT" \
  | while read -r b; do
      rec=$(jq -c --arg b "$b" \
        '[.[]|select(.headRefName==$b)]|sort_by(.number)|last' /tmp/rc_prs.json)
      mc=$(jq -r '.mergeCommit.oid // empty' <<<"${rec:-null}")
      st=$(jq -r '.state // empty' <<<"${rec:-null}")
      if { [ "$st" = "MERGED" ] && [ -n "$mc" ] \
             && git merge-base --is-ancestor "$mc" "$PROD" 2>/dev/null; } \
         || git merge-base --is-ancestor "$b" "$PROD" 2>/dev/null; then
        echo "PRUNABLE_LOCAL  $b  (needs -D if squash-merged)"
      else
        echo "KEEP_LOCAL      $b  ($st)"
      fi
    done

# Worktrees
git worktree list --porcelain
```

For each worktree other than the main checkout, classify it:

- Branch proven-in-prod by the oracle AND `git -C <path> status --porcelain` empty => safe to remove.
- Uncommitted changes => SKIP, report as dirty.
- Branch not proven-in-prod => SKIP, report as unmerged.
- Upstream gone (deleted on remote) and proven-in-prod => safe to remove.

Print the plan as three explicit lists — local branches, remote branches,
worktree paths — each annotated with the oracle verdict and PR number, plus a
skipped list with reasons (`MERGED_NOT_YET_IN_PROD`, `IN_FLIGHT_OPEN_PR`,
`STRANDED_*`, dirty worktree). Then stop and ask for confirmation. In `dry-run`
(default) and `verify` modes, end here.

## Phase 4: Execute Prune (Only in `prune` Mode, After Confirmation)

Only after the user confirms the printed plan:

```bash
# Local branches proven-in-prod. Try -d first; fall back to -D ONLY when the
# oracle proved the branch is in prod (squash/rebase merges require it).
for b in <prunable-local-branches>; do
  git branch -d "$b" 2>/dev/null || git branch -D "$b"
done

# Remote branches proven-in-prod
git push origin --delete <branch> ...

# Worktrees flagged safe
git worktree remove <path> ...    # never --force; refuses on dirty
git worktree prune

# Drop stale remote-tracking refs
git remote prune origin
git fetch --all --prune
```

Rules during execution:

- `-D` is permitted ONLY for branches the Phase-3 oracle tagged `PRUNABLE_LOCAL`.
  Never blind-force a branch that is not proven-in-prod.
- If `git worktree remove` refuses (dirty/locked), do not `--force`. Report and skip.
- Delete remote branches in a batch; if a delete fails (protected on the server),
  report it and continue with the rest.

## Modes

- `release-cleanup verify` — Phase 1 + 2 only. Report promotion status and the branch classification. No plan, no deletion.
- `release-cleanup` or `release-cleanup dry-run` — Phases 1-3. Verify, then print the prune plan. No deletion. (Default.)
- `release-cleanup prune` — Phases 1-4. Verify, print plan, confirm, then delete.

If the user explicitly scopes the cleanup ("only worktrees", "local branches
only", "skip remote"), honor it: still run verification, but restrict the plan
and execution to the requested resource types.

## Final Status

Report:

- Repository and production branch used
- Each trunk hop's result (complete / incomplete / squash-artifact)
- Genuinely stranded branches (`STRANDED_*`), if any
- Branches merged but not yet promoted to prod (`MERGED_NOT_YET_IN_PROD`), if any
- Local branches deleted / skipped (with reasons, and whether `-D` was needed)
- Remote branches deleted / skipped (with reasons)
- Worktrees removed / skipped (with reasons)
- Whether anything was blocked and what the user should decide next
