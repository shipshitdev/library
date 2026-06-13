---
name: merge-open-prs
description: Review every open pull request targeting the develop branch, merge the approved ones into develop, then prune the merged branches and stale worktrees left behind. Confirmation-gated and squash-merge aware via delegated cleanup. Use when the user asks to merge all open PRs into develop, review and land the open PRs, batch-merge to develop and clean up afterward, or runs /merge.
compatibility: Requires git, GitHub CLI gh, and jq access to the target repository.
metadata:
  version: "1.0.0"
  tags: "git, github, pull-request, merge, review, develop, cleanup, batch"
allowed-tools: Bash(git *) Bash(gh *) Bash(jq *)
disable-model-invocation: true
---

# Merge Open PRs

Review every open pull request aimed at the develop branch, merge the ones that
pass review and CI into develop, then tidy up the branches and worktrees the
merges leave behind. This is an orchestrator: it reviews with `code-review`,
merges with `gh`, and prunes with `release-cleanup`. It never bypasses a failing
gate and never deletes work that is not provably merged.

This skill is standalone and manually triggerable (exposed as `/merge`). It does
not promote develop onward to staging or production (use `release-pr-gates`) and
does not deploy (use `deploy`). It lands the open feature/fix PRs onto develop
and cleans up.

## Contract

Inputs:

- Repository root with a git remote and open GitHub pull requests
- A develop branch on the remote (auto-detected), or an explicit base override
- Optional mode: `review` (review only), `merge` (review + merge), or `full`
  (review + merge + prune, the default)

Outputs:

- Per-PR review verdict plus CI and mergeability status
- A consolidated merge plan: the mergeable, reviewed PRs versus the excluded ones
  (draft, conflicted, failing checks, unresolved findings) with a reason each
- Merge result per PR
- The prune summary delegated to `release-cleanup`

Creates/Modifies:

- Merges approved open PRs into the develop branch through GitHub
- Deletes each merged PR's head branch (`--delete-branch`)
- Delegates local branch, remote branch, and worktree pruning to `release-cleanup`
- Never merges a draft, a conflicted PR, or a PR with failing required checks
  without explicit per-PR confirmation

External Side Effects:

- Reads PR, check, and review state from GitHub; merges PRs and deletes remote
  branches via `gh`
- Does not deploy, promote up the branch chain, or rewrite history

Confirmation Required:

- Before merging anything — always print the consolidated plan and require an
  explicit yes
- Before merging a PR whose checks are failing or still pending, or that carries
  an unaddressed review finding
- Before pruning — handled by `release-cleanup`, which runs its own dry-run and
  confirmation gate

Delegates To:

- `code-review` to review each open PR before it is merged
- `gh-fix-ci` when a PR's required checks are failing and the user wants them fixed
- `release-cleanup` to prune merged branches and stale worktrees after merges land
- `release-pr-gates` to promote develop onward to staging or production once the
  open PRs are merged

## When to Use

- To review and land all open PRs targeting develop in one pass, then clean up
- After a sprint, to clear the develop queue: review, merge the green ones, prune
- When the user wants one confirm-gated sweep instead of merging PRs one by one

Do not use this skill to promote develop up the release chain or to force-merge
PRs that fail review or CI. It only lands PRs that pass their gates.

## Safety Model

Hard rules:

1. The merge base is **develop**. If develop does not exist on the remote, STOP
   and report — this flow is develop-centric. Honor an explicit base override only
   after confirming that branch exists on the remote.
2. **Drafts are never merged.** Report and skip.
3. **Conflicted PRs are never merged.** A PR whose `mergeable` is `CONFLICTING`
   is reported and skipped; the author must rebase first.
4. **Failing or pending required checks block the merge.** Such a PR is excluded
   from the default plan. Merge it only if the user explicitly confirms that
   specific PR after seeing the failing checks.
5. **Review is a gate, not a formality.** Every non-draft candidate is reviewed
   with `code-review` before it can enter the merge plan. PRs with unresolved
   high-confidence findings are surfaced and excluded unless the user overrides.
6. The default plan contains only PRs that are non-draft, mergeable, green, and
   review-clean. Everything else is listed with its reason and skipped.
7. No deletion happens here beyond the merged PR's own head branch. All other
   branch and worktree pruning is delegated to `release-cleanup`, which gates it.

## Phase 1: Discover Open PRs Into Develop

```bash
gh auth status -h github.com
git status -sb
git fetch --all --prune
gh repo view --json nameWithOwner,defaultBranchRef,mergeCommitAllowed,squashMergeAllowed,rebaseMergeAllowed
git branch -r --list 'origin/develop'
```

If `origin/develop` is absent, STOP and report the available remote branches. If
the user passed an explicit base, confirm it exists before continuing.

Snapshot every open PR targeting develop in one query — this drives the rest of
the run:

```bash
gh pr list --base develop --state open --limit 200 \
  --json number,title,headRefName,isDraft,mergeable,mergeStateStatus,reviewDecision,statusCheckRollup,url \
  > /tmp/mop_prs.json
```

Raise `--limit` if there are more than 200 open PRs into develop.

Pick the merge method once from the repository's allowed modes (prefer squash so
cleanup's squash-aware oracle stays consistent):

- `squashMergeAllowed` -> `--squash`
- else `mergeCommitAllowed` -> `--merge`
- else `rebaseMergeAllowed` -> `--rebase`

Honor an explicit user preference if one is given and allowed by the repo.

## Phase 2: Classify and Review Each Candidate

For each PR in the snapshot, classify before reviewing:

```bash
jq -r '.[] | "\(.number)\t\(.isDraft)\t\(.mergeable)\t\(.mergeStateStatus)\t\(.reviewDecision)\t\(.title)"' \
  /tmp/mop_prs.json
```

Buckets:

- `DRAFT` — `isDraft == true`. Skip, report.
- `CONFLICTING` — `mergeable == "CONFLICTING"`. Skip, report (author must rebase).
- `CHECKS_FAILING` / `CHECKS_PENDING` — derive from `statusCheckRollup` (any
  `conclusion` of `FAILURE`/`TIMED_OUT`/`CANCELLED` => failing; any `status` not
  `COMPLETED` => pending). Exclude from the default plan, report.
- `CANDIDATE` — non-draft, `mergeable == "MERGEABLE"`, all required checks green.

Confirm CI per candidate when the rollup is ambiguous:

```bash
gh pr checks <number>
```

Review every candidate (and any borderline PR the user wants landed) before it
enters the plan. Run the `code-review` skill against the PR's diff:

```bash
gh pr diff <number>
```

Capture each review verdict as `clean` or `has-findings` (with a one-line
summary of the most serious finding). A candidate with unresolved high-confidence
bug findings moves to a `REVIEW_BLOCKED` bucket and is excluded unless the user
explicitly overrides after seeing the finding.

## Phase 3: Present the Merge Plan and Confirm

Print one consolidated plan, then stop and wait for an explicit yes:

- **Will merge** (the default set): each PR number, title, head branch, review
  verdict, and the merge method to be used.
- **Excluded**: each skipped PR with its reason (`DRAFT`, `CONFLICTING`,
  `CHECKS_FAILING`, `CHECKS_PENDING`, `REVIEW_BLOCKED`).
- The merge method and whether head branches will be deleted on merge.

In `review` mode, end here — report verdicts and the plan, merge nothing.

Do not proceed to Phase 4 until the user confirms the printed plan. If the user
opts to include an excluded PR (e.g. to merge despite pending checks), require
that explicit per-PR yes and note it in the final status.

## Phase 4: Merge the Approved PRs

Only after the user confirms, merge each PR in the approved set. Merge oldest
first so dependent branches see their predecessors:

```bash
for n in <approved-pr-numbers>; do
  gh pr merge "$n" <method> --delete-branch
done
```

Where `<method>` is the Phase 1 choice (`--squash` / `--merge` / `--rebase`).

Rules during execution:

- If a merge fails because the PR became out of date (base moved), report it and
  continue with the rest; the user can re-run for the stragglers.
- If required checks regressed to failing between plan and merge, skip that PR and
  report it rather than forcing the merge.
- Never pass a force or admin override flag to bypass a protected-branch rule.
  Report the block and let the user decide.

After the batch, refresh local state so the prune phase sees the merges:

```bash
git fetch --all --prune
```

## Phase 5: Prune (Delegated)

In `full` mode (default), hand off to `release-cleanup` in `prune` mode once the
merges have landed. It re-derives what is provably merged with its squash-aware
merge oracle, prints its own dry-run plan, and requires its own confirmation
before deleting any local branch, remote branch, or worktree. Do not delete
branches or worktrees directly from this skill beyond the per-PR
`--delete-branch` already done in Phase 4.

If any PR was left unmerged (conflicted, failing, or skipped), tell
`release-cleanup` to treat those branches as in-flight so they are not pruned.

In `merge` mode, stop after Phase 4 and report; do not prune.

## Modes

- `merge-open-prs review` — Phases 1-3. Review every open PR into develop and
  print the plan. Merge nothing, prune nothing.
- `merge-open-prs merge` — Phases 1-4. Review, confirm, merge. No prune.
- `merge-open-prs` or `merge-open-prs full` — Phases 1-5. Review, confirm, merge,
  then delegate prune to `release-cleanup`. (Default.)

If the user scopes the run ("only PRs labeled X", "skip the prune", "merge
mode"), honor it: still review and gate, but restrict the candidate set or stop
before the phase they excluded.

## Final Status

Report:

- Repository and the base branch used (develop or the confirmed override)
- Merge method used
- PRs merged, with numbers and titles
- PRs excluded, grouped by reason (draft, conflicting, checks, review-blocked)
- Any merge that failed mid-batch and why
- The `release-cleanup` prune summary, or that pruning was skipped
- What the user should decide next (e.g. rebase a conflicted PR, fix CI via
  `gh-fix-ci`, or promote develop onward via `release-pr-gates`)
