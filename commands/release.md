# Release - One Front Door for Cut, Gate, and Cleanup

Drive the whole release lifecycle from one command — verify CI and ship, cut a
versioned tag with patch notes, or prune merged branches after a deploy — instead
of remembering which release skill fits which step. Trunk-based: releases are tags
cut from the trunk (the repo's default branch); staging and production are
deployment environments driven by CI/CD and tags, not branch promotions.

## Usage

```bash
/release                 # status: trunk, latest tag, commits since, CI state + usage
/release gates           # verify required CI green, then cut tag/release or open a release PR
/release cut             # infer next semver from commits, preview, then tag + GitHub release
/release patch|minor|major   # force the bump, then cut
/release vX.Y.Z          # cut an explicit version
/release notes           # patch notes for the next version only — cut nothing (dry run)
/release cleanup         # verify merged, then prune merged local/remote branches + stale worktrees
```

## Steps

- **`gates`** — the `release-pr-gates` skill: verify required GitHub checks are
  green on the trunk, then cut the release or open a release PR into the default
  branch. The CI quality gate before shipping.
- **`cut` / `patch` / `minor` / `major` / `vX.Y.Z` / `notes`** — the `release`
  skill: derive the next semantic version from Conventional Commits (or honor an
  explicit bump), generate plain-English patch notes, then tag the trunk and
  publish a GitHub release. `notes` is the dry run — notes only, nothing cut.
- **`cleanup`** — the `release-cleanup` skill: verify branches are provably
  squash-merged into the trunk via the GitHub PR merge oracle, then prune merged
  local + remote branches and stale git worktrees.

## Workflow

Use the `release-dispatch` skill. It detects the trunk, parses the subcommand,
and delegates to the right engine. Read-only until the delegated skill's own
confirmation gate; it never tags a dirty/behind trunk, reuses a tag, force-pushes,
or prunes unmerged branches.

1. **Parse the argument** into a mode (`status` / `gates` / `cut` / `notes` /
   `cleanup`), forwarding any bump token (`patch`/`minor`/`major`/`vX.Y.Z`) to
   the cut engine. Unknown argument → print Usage, don't guess.
2. **Detect and verify the trunk** (`gh repo view` default branch, verified on
   the remote). If it can't be verified, stop and ask.
3. **Route** to the delegated skill (or, for `status`, print latest tag + commits
   since + CI state and stop).
4. **Defer** preconditions and confirmation to the delegated skill — this command
   does not relax them.
