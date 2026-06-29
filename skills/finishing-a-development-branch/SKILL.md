---
name: finishing-a-development-branch
description: >-
  Structured "done coding, now what?" workflow: verify tests pass, detect the
  repository environment (normal repo vs worktree, named branch vs detached
  HEAD), present exactly the right merge / PR / keep / discard options, and
  execute the chosen path including safe worktree cleanup. Use when
  implementation is complete and the branch needs to be integrated, published,
  or abandoned.
metadata:
  version: "1.0.0"
  source: https://github.com/obra/superpowers/blob/main/skills/finishing-a-development-branch/SKILL.md
  upstream_repo: obra/superpowers
  upstream_ref: main
  upstream_commit: f2cbfbefebbf
  last_synced: "2026-06-12"
  license: MIT
  tags: "git, branch, merge, pull-request, workflow, worktree, cleanup"
allowed-tools: Bash(git *) Bash(gh *)
disable-model-invocation: true
when_to_use: "finish branch, done coding, ready to merge, create PR, close branch, wrap up feature, branch cleanup, integration workflow"
---
# Finishing a Development Branch

**Core principle:** Verify tests → Detect environment → Present options →
Execute choice → Clean up.

## Contract

Inputs:

- A completed branch or worktree, the project's test results, and the user's
  chosen integration path (merge / PR / keep / discard).

Outputs:

- The executed integration action plus a summary of what happened and where the
  work now lives.

Creates/Modifies:

- Git branches, merge commits, and pull requests; removes worktrees during
  cleanup.

External Side Effects:

- `git push`, `gh pr create`, branch deletion, and worktree removal.

Confirmation Required:

- Before discarding a branch, running any force operation, or removing a
  worktree that still holds uncommitted work.

Delegates To:

- `git-safety` for history secret scrubbing before publishing.
- `code-review` for a pre-merge correctness pass when requested.

## The Process

### Step 1: Verify Tests

Before presenting any options, run the project's test suite:

```bash
# Use whichever test runner the project uses
npm test / bun test / cargo test / pytest / go test ./...
```

If tests fail:

```
Tests failing (<N> failures). Must fix before completing:

[show failures]

Cannot proceed with merge/PR until tests pass.
```

Stop. Do not continue to Step 2 while tests are red.

If tests pass, continue to Step 2.

### Step 2: Detect Environment

Determine workspace state before presenting options:

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
```

| State | Menu | Cleanup |
|-------|------|---------|
| `GIT_DIR == GIT_COMMON` (normal repo) | 4-option menu | No worktree to clean up |
| `GIT_DIR != GIT_COMMON`, named branch | 4-option menu | Provenance-based (see Step 6) |
| `GIT_DIR != GIT_COMMON`, detached HEAD | 3-option menu (no local merge) | Externally managed — do not remove |

### Step 3: Determine Base Branch

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

If neither resolves, ask the user: "This branch appears to split from `main` —
is that correct?"

### Step 4: Present Options

**Normal repo and named-branch worktree — exactly 4 options:**

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (handle it later)
4. Discard this work

Which option?
```

**Detached HEAD — exactly 3 options:**

```
Implementation complete. You're on a detached HEAD (externally managed workspace).

1. Push as new branch and create a Pull Request
2. Keep as-is (handle it later)
3. Discard this work

Which option?
```

Do not add explanation text to the menu — keep it concise.

### Step 5: Execute Choice

#### Option 1: Merge Locally

```bash
# Resolve main repo root first (safe when running inside a worktree)
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"

git checkout <base-branch>
git pull
git merge <feature-branch>
```

Run the test suite again on the merged result. Only after tests pass on the
merge: run Step 6 to clean up the worktree, then delete the branch:

```bash
git branch -d <feature-branch>
```

#### Option 2: Push and Create PR

```bash
git push -u origin <feature-branch>

gh pr create --title "<descriptive title>" --body "$(cat <<'EOF'
## Summary
- <what changed, 2-3 bullets>

## Test Plan
- [ ] <verification steps>
EOF
)"
```

Do **not** clean up the worktree — the user needs it alive to iterate on PR
feedback.

#### Option 3: Keep As-Is

Report: "Keeping branch `<name>`. Worktree preserved at `<path>`."

Do not clean up the worktree.

#### Option 4: Discard

Require typed confirmation before destroying anything:

```
This will permanently delete:
- Branch <name>
- All commits: <commit list>
- Worktree at <path> (if applicable)

Type 'discard' to confirm.
```

Wait for the exact word. If confirmed:

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
```

Run Step 6 to clean up the worktree, then force-delete the branch:

```bash
git branch -D <feature-branch>
```

### Step 6: Cleanup Workspace

This step runs **only for Options 1 and 4**. Options 2 and 3 always preserve
the worktree.

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
WORKTREE_PATH=$(git rev-parse --show-toplevel)
```

**If `GIT_DIR == GIT_COMMON`:** This is a normal repo checkout. No worktree to
clean up. Done.

**If the worktree path is under `.worktrees/` or `worktrees/` relative to the
main repo root:** The current workflow created this worktree — it is safe to
remove it.

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
git worktree remove "$WORKTREE_PATH"
git worktree prune   # clean up any stale registrations
```

**Otherwise:** The host environment owns this workspace. Do **not** remove it.
Leave the workspace in place and report the path to the user.

## Quick Reference

| Option | Merge | Push | Keep Worktree | Delete Branch |
|--------|-------|------|---------------|---------------|
| 1. Merge locally | yes | — | — | yes (safe `-d`) |
| 2. Create PR | — | yes | yes | — |
| 3. Keep as-is | — | — | yes | — |
| 4. Discard | — | — | — | yes (force `-D`) |

## Common Mistakes

**Skipping test verification**

- Problem: Broken code gets merged or published as a PR.
- Fix: Always verify tests before offering options.

**Open-ended questions instead of the menu**

- Problem: "What should I do next?" is ambiguous and stalls the workflow.
- Fix: Present exactly 4 structured options (or 3 for detached HEAD).

**Cleaning up the worktree for Option 2**

- Problem: The user needs the worktree alive to iterate on PR feedback.
- Fix: Only clean up for Options 1 and 4.

**Deleting the branch before removing the worktree**

- Problem: `git branch -d` fails because the worktree still references it.
- Fix: Remove the worktree first, then delete the branch.

**Running `git worktree remove` from inside the worktree**

- Problem: The command fails or silently does nothing.
- Fix: Always `cd` to the main repo root before calling `git worktree remove`.

**Cleaning up externally-managed worktrees**

- Problem: Removing a workspace the host environment created causes phantom state.
- Fix: Only clean up worktrees under `.worktrees/` or `worktrees/` paths that
  the current workflow owns. If provenance is unclear, leave it.

**No confirmation for discard**

- Problem: Work is accidentally destroyed.
- Fix: Require the exact word `discard` typed by the user before proceeding.

## Iron Rules

Never:

- Proceed with failing tests.
- Merge without re-verifying tests on the merged result.
- Delete work without explicit typed confirmation.
- Force-push without an explicit request from the user.
- Remove a worktree before confirming the merge succeeded.
- Clean up worktrees whose provenance is unknown or externally managed.
- Run `git worktree remove` from inside the worktree being removed.

Always:

- Verify tests before offering options.
- Detect environment before presenting the menu.
- Present exactly 4 options (or 3 for detached HEAD) — no more, no less.
- Get typed `discard` confirmation for Option 4.
- Clean up the worktree for Options 1 and 4 only.
- `cd` to the main repo root before any worktree removal.
- Run `git worktree prune` after removal.
