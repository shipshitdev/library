# Release - Cut a Trunk Release with Patch Notes

Cut a versioned release straight from the trunk (the repo's default branch) and
generate plain-English patch notes. Trunk-based: releases are tags cut from the
trunk — there is no develop/staging branch promotion. Staging and production are
deployment environments, not branches.

## Usage

```bash
/release                 # infer next semver from commits, preview, then tag + GitHub release (default)
/release patch|minor|major   # force the bump
/release vX.Y.Z          # cut an explicit version
/release notes           # generate the next version + patch notes only — cut nothing (dry run)
```

## Workflow

Use the `release` skill.

1. Detect the trunk (default branch). Require the checkout to be on it, clean, and
   in sync with the remote.
2. Check the trunk HEAD's required CI checks. If not green, surface it and require
   an explicit override (or hand off to `gh-fix-ci`).
3. Find the latest release tag and the commits since it; derive the next semantic
   version (Conventional Commits), or honor an explicit bump/version argument.
4. Generate plain-English patch notes grouped by impact (features, fixes,
   performance, breaking changes, internal).
5. Print one consolidated plan — version, commit range, notes preview — and wait
   for explicit confirmation.
6. Tag the trunk HEAD (`vX.Y.Z`), push the tag, and publish a GitHub release with
   the notes.

## Gates

- Release only from a clean, synced trunk; never tag a dirty or behind tree.
- Never reuse or overwrite an existing tag without explicit confirmation.
- Never rewrite history, force-push, or move long-lived branches.
- This command tags the trunk and writes notes — it does not deploy. To ship the
  tag, use the `deploy` or `deployment-composer` skill; to prune merged branches
  afterward, use `release-cleanup`.
