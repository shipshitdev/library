---
name: release-pr-gates
description: Promote releases through GitHub pull requests between develop, staging, and master/main branches, including branch discovery, target selection, PR creation, and waiting for required quality gates. Use when the user asks to release, promote develop, open a release PR, push to staging, promote staging to production, or wait for GitHub checks to go green.
compatibility: Requires git and GitHub CLI gh access to the target repository.
metadata:
  version: "1.0.0"
  tags: "release, github, pull-request, ci-cd, quality-gates"
allowed-tools: Bash(git *) Bash(gh *)
disable-model-invocation: true
---

# Release PR Gates

Promote code through protected branches with GitHub pull requests and wait for
quality gates before reporting the release as ready.

## Contract

Inputs:

- Repository root with git remote
- Source branch and target branch, or permission to auto-detect release branches
- Optional existing PR number

Outputs:

- PR URL or existing PR reused
- Source/target branch summary
- Quality gate status
- Failing check summary when gates fail

Creates/Modifies:

- May create a GitHub release PR
- May create a local PR body file
- Does not merge unless explicitly confirmed

External Side Effects:

- Reads and writes GitHub pull request state
- Watches GitHub checks
- Reads GitHub Actions logs for failures

Confirmation Required:

- Before creating a PR unless the user explicitly asked to open a release PR
- Before marking a PR ready when repository convention is unclear
- Before merging into `master` or `main`
- Before rerunning workflows

Delegates To:

- `gh-fix-ci` when checks fail
- `changelog-generator` when a release body needs commit summaries
- `deploy` after release gates pass and provider deployment is needed

## Use Case

Use this skill for release promotion flows such as:

- `develop` -> `staging` -> `master`
- `develop` -> `staging` -> `main`
- `develop` -> `master` when no `staging` branch exists
- `develop` -> `main` when no `staging` branch exists

Always discover the repository's real branches before choosing the PR target.

## Preconditions

1. Verify GitHub CLI and auth:

   ```bash
   gh --version
   gh auth status -h github.com
   ```

2. Verify clean release context:

   ```bash
   git status -sb
   git remote -v
   git fetch --all --prune
   ```

3. Identify the repository and default branch:

   ```bash
   gh repo view --json nameWithOwner,defaultBranchRef
   ```

4. List release branches on the remote:

   ```bash
   git branch -r --list 'origin/develop' 'origin/staging' 'origin/master' 'origin/main'
   ```

Stop and explain the blocker if `develop` does not exist. This release flow
starts from `develop` by default.

## Branch Target Rules

Choose the PR base in this order:

1. If the user explicitly names a base branch, use it after confirming it exists
   on the remote.
2. If `origin/staging` exists, open the release PR from `develop` to `staging`.
3. If `origin/staging` does not exist, open the release PR from `develop` to
   `master` when `origin/master` exists.
4. If `origin/master` does not exist, open the release PR from `develop` to
   `main` when `origin/main` exists.
5. If none of these targets exist, stop and report the available remote branches.

For a second production promotion after staging has gone green, use:

- `staging` -> `master` when `master` exists
- `staging` -> `main` when `master` does not exist and `main` exists

Require explicit user confirmation before merging into `master` or `main`.

## Release PR Workflow

1. Run local quality gates before opening or updating the release PR. Format,
   lint, and type-check are mandatory because they mirror GitHub Actions and are
   cheap to run locally:

   ```bash
   bun run format || npm run format || npx biome check --write .
   bun run lint || npm run lint || bunx turbo lint
   bun run typecheck || bun run type-check || npm run typecheck || npm run type-check || npx tsc --noEmit
   ```

   Fix failures before pushing. Do not open a release PR with known local
   format, lint, or type errors.

2. Inspect branch divergence:

   ```bash
   git log --oneline origin/<base>..origin/<head>
   git diff --stat origin/<base>...origin/<head>
   ```

3. Check for an existing open PR:

   ```bash
   gh pr list --head <head> --base <base> --state open --json number,title,url,headRefName,baseRefName
   ```

4. If no open PR exists, create one:

   ```bash
   gh pr create --head <head> --base <base> --title "Release: <head> to <base>" --body-file <body-file>
   ```

   The PR body should include:

   - Source and target branches
   - Commit summary from `<base>..<head>`
   - Local checks already run, if any
   - Release risk notes or migrations, if visible from commits

5. If an open PR already exists, reuse it. Do not create duplicates.

6. Mark the PR ready for review only if the user requested a non-draft PR or the
   repository release convention requires ready PRs.

## Waiting for Quality Gates

After creating or finding the PR, wait for GitHub checks:

```bash
gh pr checks <number> --watch
```

If `--watch` is not available or fails, poll checks:

```bash
gh pr checks <number>
```

Quality gate outcomes:

- `pass`: report the PR is green and ready for review or merge.
- `fail`: fetch the failing workflow logs and summarize root cause.
- `pending`: keep waiting unless the user asks for a status-only update.
- `skipping` or no checks: report exactly what GitHub shows; do not call it green
  unless required checks are passing or absent by repository policy.

For failed GitHub Actions runs, inspect logs:

```bash
gh run view <run-id> --log
```

Do not rerun workflows unless the user asks.

## Merge Policy

- Do not merge production PRs without explicit confirmation.
- Do not bypass failing required checks.
- If staging exists, prefer a staged rollout: `develop` -> `staging`, then
  `staging` -> production after gates are green.
- If staging does not exist, use the direct `develop` -> production PR and make
  the missing staging branch explicit in the final status.

## Final Status

Report:

- Repository
- PR URL
- Source and target branches
- Whether this was a staged or direct production release
- Quality gate state
- Any failing check names and root cause summary
- Whether user confirmation is needed to merge
