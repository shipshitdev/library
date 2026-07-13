---
name: pr-merge-train
description: >-
  Drains open GitHub pull request queues without serial blocking. Use for
  multi-PR and WIP-drain prompts such as review all PRs, drain open PRs, merge
  clean PRs, reduce WIP, merge train, clean up pull requests, or land everything
  that is safe to merge.
compatibility: Requires git and GitHub CLI gh access to the target repository.
metadata:
  version: "1.0.1"
  tags: "github, pull-requests, merge-train, ci, wip"
  author: Ship Shit Dev
allowed-tools: Bash(git *) Bash(gh *)
disable-model-invocation: true
when_to_use: "review all PRs, drain open PRs, merge clean PRs, reduce WIP, merge train, clean up pull requests, land green PRs, drain WIP"
---

# PR Merge Train

Drain open PR queues by merging safe independent PRs first, fixing blocked PRs
narrowly, and moving on whenever unrelated CI is still pending. The goal is lower
WIP, not a serial full review of every branch.

## Contract

Inputs:

- Repository with open GitHub PRs
- Optional explicit dependency order from the user, such as "merge #12 before #18"

Outputs:

- Queue classification for every open PR
- PRs merged, PRs fixed and pushed with CI pending, and PRs blocked with exact blockers
- Checks and review evidence used for each decision

Creates/Modifies:

- Commits and pushes narrow fixes to PR branches when the root cause is clear
- Merges clean independent PRs using a merge method the repository allows
- Does not deploy, promote releases, delete unrelated branches, or rewrite unrelated history

External Side Effects:

- Reads GitHub PRs, checks, reviews, and Actions logs
- May rerun or cancel setup-stuck GitHub Actions jobs
- May push commits and merge PRs after the user has asked to drain, merge, or clean up the queue
- Never runs deploy commands, deployment workflows, release promotion, or environment changes

Confirmation Required:

- The user's merge-train, WIP-drain, "review all PRs", or merge request authorizes
  normal queue actions: classify, merge green PRs, rerun setup-stuck CI, commit
  narrow fixes, push, and move on.
- Ask before force-pushing, broad CI/deployment config changes, deleting branches
  outside the PR merge action, or doing anything that could deploy. Deploys are
  forbidden even if a workflow name looks like a CI check.
- Ask for explicit confirmation before any admin merge that bypasses branch
  protection. A queue-drain or merge-train request authorizes normal merges only.

Delegates To:

- `gh-fix-ci` for red or setup-stuck CI diagnosis.
- `gh-address-comments` for actionable review comments that require a code change.
- `code-review` only for a single risky diff, not as a serial full-review pass over the queue.

## Rules

1. Batch-query all open PRs before fixing, checking out, or merging any one PR.
2. Classify every PR into exactly one bucket: `green`, `red`, `pending`,
   `conflict`, `needs-review`, or `dependency-blocked`.
3. Merge clean independent `green` PRs immediately, before feature or fix work.
4. Respect explicit dependency order from the user. A requested "A before B"
   order becomes a hard edge in the merge graph.
5. For `red` PRs, inspect only failing checks, setup-stuck pending jobs, and
   actionable review comments. Patch narrowly, push, report "CI pending, moved
   on", then continue with the queue.
6. Do not synchronously wait for unrelated pending CI unless that PR is the next
   required merge in the dependency order.
7. If a GitHub Actions job stays in setup, checkout, dependency install, or tool
   install for 5-8 minutes with no repo-code step running, cancel and rerun that
   job or workflow instead of waiting indefinitely.
8. Never deploy.
9. Do not run heavy local suites. Use focused local checks for changed files or a
   single relevant spec only; rely on PR CI for broad validation.
10. Use squash, rebase, or merge commit according to repository settings. If the
    normal merge is blocked only by branch policy while checks are green, classify
    the PR as blocked and request explicit confirmation before using an admin path.
    Do not treat the original queue-drain request as approval to bypass protection.
11. Preserve unrelated dirty local changes. Use a clean worktree for PR fixes
    when the current checkout is dirty or belongs to a different branch.
12. Final reporting must include PRs merged, PRs fixed and pushed but still
    pending CI, PRs blocked with exact blockers, checks used as evidence, and a
    statement that no deploy ran.

## Workflow

### 1. Establish Guardrails

```bash
gh auth status -h github.com
git status --short
git fetch --all --prune
gh repo view --json nameWithOwner,defaultBranchRef
gh api repos/{owner}/{repo} --jq '{allow_squash_merge,allow_rebase_merge,allow_merge_commit}'
```

Record any dirty local files before touching PR branches. Never stash or revert
unrelated work. If local changes could be disturbed, create an isolated worktree
for each PR fix.

Parse the user's prompt for dependency edges: PR numbers, branch names, or titles
that must land before another PR. Also infer dependency blocking from stacked PRs
when a PR's base branch is another open PR branch.

### 2. Batch-Query the Queue

Start with one queue snapshot:

```bash
gh pr list --state open --limit 200 \
  --json number,title,url,isDraft,headRefName,baseRefName,author,mergeable,reviewDecision,statusCheckRollup,updatedAt
```

If more than 200 PRs are open, paginate with the GitHub API before classifying.
Collect unresolved review threads in the same discovery phase, using GraphQL when
needed so every open PR has review-thread state before individual work begins.
Summarize comments; do not quote long review text.

### 3. Classify Every PR

Use the first matching bucket in this order:

- `dependency-blocked` — an explicit user edge or stacked base branch requires
  another open PR to merge first.
- `conflict` — GitHub reports merge conflicts, unknown mergeability after refresh,
  or a base/head state that cannot be merged without conflict resolution.
- `red` — at least one required check failed, was cancelled, or timed out.
- `pending` — required CI is queued, in progress, waiting, or expected.
- `needs-review` — draft PR, unresolved requested changes, or unresolved material
  review comments that block merge confidence.
- `green` — required checks pass, the PR is mergeable, dependencies are satisfied,
  and there are no unresolved blocker comments.

Do not treat optional experimental checks as blockers unless the repository
marks them required or the PR's change scope makes them clearly material.

### 4. Merge Green PRs First

Topologically sort `green` PRs by explicit dependency edges. Merge every
independent `green` PR before fixing `red`, `conflict`, or `needs-review` PRs.

Choose the merge strategy from repository settings. Prefer the repo's normal
strategy; if unknown, try squash first, then rebase, then merge commit only when
the repository allows it:

```bash
gh pr merge <number> --squash --delete-branch
gh pr merge <number> --rebase --delete-branch
gh pr merge <number> --merge --delete-branch
```

If merge is blocked only by branch policy despite green required checks, record
the policy message and stop with the PR classified as blocked. Only after the user
explicitly approves bypassing branch protection may you use an available admin
merge path:

```bash
gh pr merge <number> --squash --delete-branch --admin
```

If confirmation is absent or admin merge is unavailable, keep the PR blocked with
the exact policy message. After each merge batch, refresh PR metadata for dependent
or overlapping PRs before continuing.

### 5. Fix Red PRs Without Serial Blocking

For each `red` PR that is not dependency-blocked:

1. Inspect only failing required checks and setup-stuck pending jobs.
2. Fetch failed logs, not full logs by default.
3. Inspect actionable review comments only when they explain the failure or block
   the fix.
4. Patch the smallest root cause in a clean PR worktree.
5. Run only focused local checks that directly cover the changed files.
6. Commit, push, and immediately continue with the queue.

Use `gh-fix-ci` behavior for setup-stuck jobs. If a job has spent 5-8 minutes in
setup, checkout, dependency install, or tool install without a repo-code step
running, cancel and rerun the job or workflow:

```bash
gh run view <run-id> --json jobs
gh run cancel <run-id>
gh run rerun <run-id> --failed
gh run rerun <run-id> --job <job-id>
```

After pushing a fix, do not wait for broad CI unless that PR is the next required
merge in the user's dependency order. Report: `CI pending, moved on`.

### 6. Handle Pending, Conflicts, and Review Blocks

- `pending`: leave it pending unless it is the next required merge. If it is next,
  poll only that PR's required checks and apply the setup-stuck rule.
- `conflict`: report the conflict exactly. Resolve only if the user asked for
  conflict resolution as part of the queue drain and the fix is narrow.
- `needs-review`: report the requested changes or material unresolved comments.
  Address comments only when the requested fix is clear and scoped; otherwise
  leave the PR blocked with the comment summary as evidence.
- `dependency-blocked`: report the upstream PR or explicit user order that blocks
  it. Reclassify after the upstream PR merges.

## Final Report

End every run with these sections:

- `PRs merged` — PR number, title, merge strategy, and checks used as evidence.
- `PRs fixed and pushed, CI pending` — PR number, commit pushed, failed check
  fixed, focused local check run, and pending CI checks.
- `PRs blocked` — PR number, bucket, and exact blocker: failed check, pending
  required check, conflict, requested changes, dependency edge, policy block, or
  unavailable admin path.
- `Evidence` — check names, review decisions, relevant workflow/job names, and
  any setup-stuck reruns or cancellations.
- `Deploy status` — explicitly state that no deploy ran.
