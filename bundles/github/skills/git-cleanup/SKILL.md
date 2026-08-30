---
name: git-cleanup
description: Clean up the git working state — verify branches are provably merged into the trunk (default branch) via the squash-aware GitHub PR merge oracle, then prune merged local and remote feature branches and stale git worktrees. Squash-merge aware — uses GitHub PR merge state as the merge oracle, not commit ancestry. Use when the user asks to clean up branches or worktrees, prune what is already merged, run /cleanup, or confirm nothing stale was left behind before pruning.
compatibility: Requires git, GitHub CLI gh, and jq access to the target repository.
metadata:
  version: "3.1.0"
  tags: "git, cleanup, branches, worktrees, prune, ci-cd, squash-merge, trunk-based"
allowed-tools: Bash(git *) Bash(gh *) Bash(jq *)
disable-model-invocation: true
---

# Git Cleanup

Confirm each branch's work has reached the trunk (default branch), then prune the
feature branches and git worktrees that are no longer needed. Verification is a
hard gate: never prune until each branch's work is proven to have reached the trunk
and no in-flight work is stranded.

This skill is standalone and manually triggerable (exposed as `/cleanup`). It does
not promote code (use `release-pr-gates` for that) and does not deploy (use
`deploy`). It runs after merges have landed and tidies up.

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

A branch's work is IN the production branch iff ANY of:

1. its most-recent PR is `MERGED` and that PR's `mergeCommit` is an ancestor of the
   production branch (covers squash, rebase, and merge-commit), OR
2. the branch tip is an ancestor of the production branch (covers
   no-PR fast-forwards and merge-commit merges that predate the PR API), OR
3. everything the branch changes is already in the trunk **by patch identity** —
   either every ahead commit has a patch-identical twin upstream (`git cherry`),
   or the branch's cumulative diff is patch-identical to a single trunk commit
   added since the merge base (covers local retarget/rebase copies whose name no
   longer matches a PR head).

Only branches that satisfy this are prunable. Everything else is reported, never
deleted.

**A matching commit subject is never proof of a merge.** Subjects like `fix: lint`
or `chore: bump deps` recur across unrelated branches, so subject equality would
classify genuinely unmerged work as prunable and hand it to `git branch -D`. Worse,
subject matching barely helps in the case it was meant for: a squash merge
rewrites the branch's several subjects into one PR title, so they no longer match
anyway. Rule 3 therefore never compares subjects — the proof is always
`git patch-id`, scanning the trunk commits added since the merge base. The scan is
bounded (`--max-count=500`); if the squashed commit falls outside that window the
branch is reported unproven, never deleted.

## Contract

Inputs:

- Repository root with a git remote
- Trunk (default branch) to verify against — auto-detected via `gh repo view --json defaultBranchRef` if not supplied
- Optional mode: `verify` (gate only), `dry-run` (default, plan only), or `prune` (execute after confirmation)
- Optional scope: `branches`, `worktrees`, or all resource types (default)

Outputs:

- Verification result: whether each feature branch's work is provably in the trunk, with a squash caveat where ancestry and PR state disagree
- Branch classification: prunable (in trunk), merged-but-not-yet-in-trunk, in-flight (open PR), and genuinely stranded
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

- `release-pr-gates` when a branch is NOT yet merged into the trunk and the user wants to open or land the PR first
- `gh-fix-ci` when a PR targeting the trunk is still open with failing checks
- `git-safety` when a branch about to be pruned may contain secrets in history worth scrubbing first

## When to Use

- After merging a feature or release PR into the trunk and you want to delete the merged feature branches and worktrees
- Manually, any time, to verify the trunk is up to date and see what is safe to prune
- To confirm "nothing is stale" — that every branch intended for the release actually reached the trunk — before tidying up

Do not use this skill to promote code or to delete unmerged work. It only removes
what is provably in the production branch.

## Safety Model

Protected branches are never deleted:

```
master  main  (trunk / default branch)  + the currently checked-out branch + HEAD
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
7. Run `git`/`gh`/`jq` in the agent shell. If a command is missing, restore
   `PATH` in that same shell (`/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin`).
   Never write a helper script to disk for this skill.

## Phase 1: Discover Branches and Refresh State

```bash
command -v git >/dev/null || export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
gh auth status -h github.com
git status -sb
git remote -v
git fetch --all --prune
gh repo view --json nameWithOwner,defaultBranchRef --jq '.defaultBranchRef.name'
```

Determine the trunk from the repo metadata:

- Trunk = the repo's default branch as returned by `gh repo view --json defaultBranchRef --jq .defaultBranchRef.name`. Never hardcode `master` or `main`.
- All feature/release branches are short-lived and eventually merged into the trunk.
- Verification checks only that each candidate branch's work has reached the trunk.

Look up the latest PR **per candidate head**. If a snapshot file is needed, write
it under the current repo's `.tmp/` (create it). Never `/tmp` or `/private/tmp`.
Do not cap the search at 1000 PRs.

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
mkdir -p "$REPO_ROOT/.tmp"

latest_pr_for_head() {   # arg: branch name without origin/
  gh pr list --head "$1" --state all --limit 1 \
    --json number,headRefName,baseRefName,state,mergedAt,mergeCommit
}
```

After a squash merge, GitHub often deletes the remote head. Remotes can already
be just `origin/<trunk>` while leftover **local** branches and worktrees remain.
Classify remotes, locals, and extra worktrees. A remote-only pass is not enough.

## Phase 2: Trunk Verification (Hard Gate)

### 2a. Check candidate refs against the trunk

For each candidate (remote branch, local branch, or extra worktree HEAD), verify
that its work has reached the trunk. Ancestry is the first signal, but squash
merges require corroboration — the merged PR for that head, or failing that,
patch identity against the trunk (`squash_artifact` in 2b).

```bash
TRUNK=$(gh repo view --json defaultBranchRef --jq .defaultBranchRef.name)
PROD="origin/${TRUNK}"

# Commits on a ref not in the trunk
git log --oneline "$PROD".."<ref>"
# PR that landed this head name
latest_pr_for_head "<branch>"
```

Interpreting a non-empty ahead range:

- Genuine commits not yet in the trunk => NOT MERGED. Report and STOP.
- Every ahead commit is patch-identical to work already in the trunk => squash
  artifact, not a real gap. Treat as merged. This is how local retarget/rebase
  copies (`*-onto-<trunk>`, `pr-N-rebase`, detached worktree HEADs) get
  classified when their name no longer matches a PR head.
- A matching subject with a *different* patch => NOT MERGED. Two branches can
  carry the same commit message and different changes; only patch identity
  settles it.

### 2b. Branch classification (the "nothing is stale" check)

Run the Merge Oracle over every non-protected **remote and local** branch, plus
each extra worktree. Do NOT use `git branch --merged` / `-r --no-merged`.

```bash
TRUNK=$(gh repo view --json defaultBranchRef --jq .defaultBranchRef.name)
PROD="origin/${TRUNK}"
CURRENT="$(git symbolic-ref --quiet --short HEAD || echo)"
PROTECT="${TRUNK}|${CURRENT:-__none__}|HEAD"

# Proves a ref's changes are already in the trunk by PATCH IDENTITY.
# Never matches on commit subjects: unrelated branches reuse subjects like
# "fix: lint", and a subject match would send live work to `git branch -D`.
squash_artifact() {      # arg: git ref. 0 = the ref's changes are provably in trunk
  local ref="$1" base mine c pid
  base=$(git merge-base "$PROD" "$ref" 2>/dev/null) || return 1
  # Nothing ahead of the merge base => this rule has nothing to prove.
  [ -n "$(git log --format=%H "$base".."$ref" 2>/dev/null)" ] || return 1

  # (a) Per-commit equivalence: every ahead commit has a patch-identical twin
  #     upstream. `git cherry` marks those '-'; a surviving '+' means real work.
  git cherry "$PROD" "$ref" 2>/dev/null | grep -q '^+' || return 0

  # (b) Squash equivalence: the ref's cumulative diff is patch-identical to the
  #     patch a single trunk commit introduced. Scan only trunk commits added
  #     since the merge base — the squash commit can only live in that window.
  mine=$(git diff "$base".."$ref" | git patch-id --stable | awk '{print $1}')
  [ -n "$mine" ] || return 1
  for c in $(git rev-list --max-count=500 "$base".."$PROD" 2>/dev/null); do
    pid=$(git show "$c" | git patch-id --stable | awk '{print $1}')
    [ "$pid" = "$mine" ] && return 0
  done
  return 1   # unproven => caller reports it, never deletes it
}

classify_ref() {         # args: head-name, git-ref to test for ancestry
  local b="$1" ref="$2" rec st mc base num
  rec=$(latest_pr_for_head "$b")
  rec=$(jq -c 'if type=="array" then .[0] else . end' <<<"${rec:-null}")

  if [ -z "$rec" ] || [ "$rec" = "null" ]; then
    git merge-base --is-ancestor "$ref" "$PROD" 2>/dev/null \
      && { echo "PRUNABLE_NO_PR_FF"; return; }
    squash_artifact "$ref" \
      && { echo "PRUNABLE_SQUASH_ARTIFACT"; return; }
    echo "STRANDED_NO_PR"
    return
  fi

  st=$(jq -r '.state' <<<"$rec")
  mc=$(jq -r '.mergeCommit.oid // empty' <<<"$rec")
  base=$(jq -r '.baseRefName' <<<"$rec")
  num=$(jq -r '.number' <<<"$rec")

  case "$st" in
    OPEN)   echo "IN_FLIGHT_OPEN_PR(#$num->$base)";;
    CLOSED) git merge-base --is-ancestor "$ref" "$PROD" 2>/dev/null \
              && echo "PRUNABLE_CLOSED_PR_IN_PROD(#$num)" \
              || echo "STRANDED_CLOSED_UNMERGED(#$num)";;
    MERGED)
      if [ -n "$mc" ] && git merge-base --is-ancestor "$mc" "$PROD" 2>/dev/null; then
        echo "PRUNABLE_IN_TRUNK(#$num)"
      elif git merge-base --is-ancestor "$ref" "$PROD" 2>/dev/null; then
        echo "PRUNABLE_IN_TRUNK(#$num)"
      elif squash_artifact "$ref"; then
        echo "PRUNABLE_SQUASH_ARTIFACT(#$num)"
      else
        echo "MERGED_NOT_YET_IN_TRUNK(#$num->$base)"
      fi;;
  esac
}

git branch -r --format '%(refname:short)' | grep -v -- '->' | sed 's#^origin/##' \
  | grep -vxE "origin|${TRUNK}|HEAD" \
  | while read -r b; do printf 'REMOTE  %-50s %s\n' "$b" "$(classify_ref "$b" "refs/remotes/origin/$b")"; done

git branch --format '%(refname:short)' | grep -vxE "$PROTECT" \
  | while read -r b; do printf 'LOCAL   %-50s %s\n' "$b" "$(classify_ref "$b" "$b")"; done
```

For each extra worktree from `git worktree list --porcelain`, classify its
checked-out branch the same way. Detached HEAD: use `PRUNABLE_SQUASH_ARTIFACT`
when `squash_artifact HEAD` succeeds at that path.

Buckets and what they mean:

- `PRUNABLE_*` — work is in the trunk. Safe to prune.
- `MERGED_NOT_YET_IN_TRUNK` — PR was merged into an intermediate branch that has not
  yet been merged into the trunk. NOT prunable yet; this is a real "not yet in trunk"
  signal for that branch. Report it.
- `IN_FLIGHT_OPEN_PR` — open PR. In progress. Skip, never prune.
- `STRANDED_*` — no merged PR and not in the trunk. **Genuinely forgotten work.**
  Report loudly, never prune.

Gate outcome:

- Any real (non-artifact) branch not yet in the trunk => STOP. Offer `release-pr-gates`.
- Any `STRANDED_*` branch => report as a warning; the user decides whether it was
  meant to ship. This is the "nothing is stale" guarantee.
- All candidate branches confirmed in trunk (or only squash-artifacts) and stranded
  set understood => continue.

## Phase 3: Build the Prune Plan (Dry-Run, Default)

The prunable set is exactly the refs the oracle tagged `PRUNABLE_*` in Phase 2b.
Print three lists from that classification:

- **Local branches** tagged `PRUNABLE_*` (annotate `needs -D` for squash/rebase).
- **Remote branches** tagged `PRUNABLE_*`.
- **Worktrees** whose branch is `PRUNABLE_*` and whose `git -C <path> status --porcelain`
  is empty. Dirty => SKIP. Unmerged => SKIP. Upstream gone and proven-in-prod =>
  safe to remove.

Plus a skipped list with reasons (`MERGED_NOT_YET_IN_TRUNK`, `IN_FLIGHT_OPEN_PR`,
`STRANDED_*`, dirty worktree). Then stop and ask for confirmation. In `dry-run`
(default) and `verify` modes, end here.

## Phase 4: Execute Prune (Only in `prune` Mode, After Confirmation)

Only after the user confirms the printed plan. **Worktrees first**: a branch
checked out in a worktree cannot be deleted.

```bash
# Worktrees flagged safe. Never --force; refuses on dirty.
git worktree remove <path> ...
git worktree prune

# Local branches proven-in-prod. Try -d first; fall back to -D ONLY when the
# oracle proved the branch is in prod (squash/rebase merges require it).
for b in <prunable-local-branches>; do
  git branch -d "$b" 2>/dev/null || git branch -D "$b"
done

# Remote branches proven-in-prod
git push origin --delete <branch> ...

# Drop stale remote-tracking refs
git remote prune origin
git fetch --all --prune
```

Rules during execution:

- `-D` is permitted ONLY for branches the Phase-3 oracle tagged `PRUNABLE_*`.
  Never blind-force a branch that is not proven-in-prod.
- If `git worktree remove` refuses (dirty/locked), do not `--force`. Report and skip.
- Delete remote branches in a batch; if a delete fails (protected on the server),
  report it and continue with the rest.

## Modes

- `git-cleanup verify` — Phase 1 + 2 only. Report trunk verification status and the branch classification. No plan, no deletion.
- `git-cleanup` or `git-cleanup dry-run` — Phases 1-3. Verify, then print the prune plan. No deletion. (Default.)
- `git-cleanup prune` — Phases 1-4. Verify, print plan, confirm, then delete.

If the caller scopes the cleanup (`branches`, `worktrees`, "local branches only",
"skip remote"), honor it: still run verification, but restrict the plan and
execution to the requested resource types. The default scope is everything —
branches and worktrees.

## Final Status

Report:

- Repository and trunk (default branch) used
- Verification result for each candidate branch (in trunk / not yet in trunk / squash-artifact)
- Genuinely stranded branches (`STRANDED_*`), if any
- Branches with open or unmerged PRs not yet in the trunk (`MERGED_NOT_YET_IN_TRUNK`), if any
- Local branches deleted / skipped (with reasons, and whether `-D` was needed)
- Remote branches deleted / skipped (with reasons)
- Worktrees removed / skipped (with reasons)
- Whether anything was blocked and what the user should decide next
