# Cleanup - Prune Merged Branches, Stale Worktrees, and Finished Work

Clean up what's already done. Default target is git hygiene: verify branches are
provably merged into the trunk (squash-merge aware), then prune the merged
local/remote branches and stale worktrees they leave behind. Explicit targets
extend the sweep to completed GitHub issues and old session files.

## Usage

```bash
/cleanup              # branches + worktrees: verify merged, print the prune plan (dry-run, default)
/cleanup branches     # scope to merged local + remote branches only
/cleanup worktrees    # scope to stale git worktrees only
/cleanup verify       # verification gate only — classify branches, no plan, no deletion
/cleanup prune        # execute the prune plan after you confirm it
/cleanup tasks        # close GitHub issues whose work already shipped
/cleanup sessions     # consolidate daily session files into monthly/yearly
/cleanup all          # git cleanup + tasks + sessions, sequentially
```

`prune` combines with a scope, e.g. `/cleanup prune branches`.

## Git Cleanup (default / `branches` / `worktrees` / `verify` / `prune`)

Use the `git-cleanup` skill. It is squash-merge aware: GitHub PR merge state is
the merge oracle, never `git branch --merged` ancestry alone.

1. Verify every candidate branch's work is provably in the trunk (default
   branch); report in-flight and genuinely stranded branches loudly.
2. Print the prune plan — local branches, remote branches, worktrees — plus a
   skipped list with reasons. Dry-run is the default; nothing is deleted.
3. In `prune` mode, delete only after you confirm the printed plan.

## Tasks (`tasks`)

Close completed work tracked in GitHub Issues so the open backlog stays accurate.

1. Find issues that are done (all checklist items `[x]`, or work shipped/merged)
   but still open (`gh issue list --state open`).
2. Confirm the list with the user before closing anything.
3. Close each with a short completion comment, e.g.
   `gh issue close <number> --comment "Completed — see .agents/sessions/<date>.md."`
4. Log the closed issues to today's session file.

## Sessions (`sessions`)

Merge daily sessions into monthly, monthly into yearly.

1. Back up `.agents/sessions/` to `.agents/sessions/backups/` first.
2. Consolidate `YYYY-MM-DD.md` files for past months into `YYYY-MM.md`.
3. Consolidate `YYYY-MM.md` files for past years into `YYYY-yearly-review.md`.
4. Preserve `README.md`; report what was consolidated.

## Gates

- Git cleanup never deletes anything not proven merged into the trunk, never
  touches dirty worktrees, and always shows the dry-run plan before pruning.
- `tasks` closes issues only after you confirm the list.
- `sessions` backs up before modifying and supports a preview without changes.

## Related

- `/merge` lands open PRs and then hands off to `git-cleanup` for the prune.
- `/release` cuts tags and patch notes; it no longer owns branch cleanup.
- The `worktree` skill creates worktrees; `/cleanup` is how they get removed.
