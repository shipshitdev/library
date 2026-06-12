---
name: commit-summary
description: "Generate Conventional Commit messages from staged or unstaged git changes, split unrelated changes into logical commits, detect breaking changes, and optionally create commits after approval. Use when writing commit messages, preparing commits, or committing local work."
compatibility: Requires git.
disable-model-invocation: true
allowed-tools: Bash(git *)
metadata:
  version: "1.0.0"
  tags: "git, workflow, commits, productivity"
---

# Commit Summary

Generate accurate Conventional Commits from real git diffs.

## Contract

Inputs:

- Repository root
- Staged changes, unstaged changes, or approved paths to stage
- Optional commit type, scope, and breaking-change context

Outputs:

- Commit message candidate
- Logical commit grouping when changes are mixed
- Created commit hash after approval, if requested

Creates/Modifies:

- No changes in message-only mode
- May stage files and create commits after approval

External Side Effects:

- None unless another workflow pushes the commit later

Confirmation Required:

- Before staging files
- Before creating a commit
- Before amending or squashing existing commits

Delegates To:

- `gh-pr-publish` when the commit should be pushed and opened as a PR
- `git-safety` when secrets or sensitive files appear in the diff

## Workflow

1. Inspect repository state:

   ```bash
   git status -sb
   git log --oneline -5
   git diff --stat
   git diff --cached --stat
   ```

2. Determine whether changes are already staged:
   - If staged changes exist, generate the message from `git diff --staged`.
   - If nothing is staged, inspect unstaged changes and propose logical groups.
   - If unrelated changes are mixed, recommend separate commits.

3. Guard against unsafe commits:
   - Do not stage secrets, `.env`, credentials, private keys, local databases,
     build caches, or large generated artifacts.
   - If sensitive files appear, stop and delegate to `git-safety`.
   - Do not include unrelated formatting churn in a feature/fix commit unless
     it is required by the change.

4. Choose the Conventional Commit type:

   - `feat`: user-visible feature or capability
   - `fix`: bug fix
   - `docs`: documentation only
   - `style`: formatting only, no behavior change
   - `refactor`: code restructuring without behavior change
   - `perf`: performance improvement
   - `test`: tests only
   - `build`: build system, package manager, dependencies
   - `ci`: CI/CD workflow changes
   - `chore`: maintenance with no user-facing behavior
   - `revert`: revert a previous commit

5. Detect scope:
   - Prefer package, app, domain, or subsystem names already used in history.
   - Omit scope if it would be vague (`misc`, `stuff`, `changes`).

6. Detect breaking changes:
   - Public API contract changes
   - CLI flags or output changes
   - Database/schema migrations requiring user action
   - Removed config keys, env vars, routes, events, or exported symbols

   Format as `type(scope)!: summary` and include a `BREAKING CHANGE:` footer.

7. Generate the commit message:

   ```text
   type(scope): imperative summary

   Optional body explaining why and any non-obvious implementation detail.

   Optional footer such as:
   BREAKING CHANGE: migration required because ...
   Refs: #123
   ```

8. If the user asked to commit, show the exact message and get approval:

   ```bash
   git add <approved-paths>
   git diff --staged --stat
   git commit -m "<subject>" -m "<body-or-footer>"
   ```

## Quality Bar

- Subject is imperative and under 72 characters.
- Body explains why when the diff alone is not enough.
- Message does not overstate behavior.
- Commit contains one logical change.
- Verification commands are not placed in the commit message unless the repo
  convention asks for them.

## Gotchas

- **`git add .` can stage unintended files.** If `.gitignore` does not exclude `node_modules`, `.env*`, or build artifacts, always prefer `git add <specific-paths>`. Verify with `git diff --staged --stat` before committing.
- **Breaking-change footer is case-sensitive.** The token must be exactly `BREAKING CHANGE:` (with a space, all caps) for tools like `semantic-release` and `conventional-changelog` to detect it. `BREAKING-CHANGE:` is not equivalent.
- **Amended commits rewrite history.** Never amend a commit that has already been pushed to a shared branch. If the commit exists on the remote, create a new fix commit instead.
- **Co-authored-by trailers conflict with repo conventions.** Some repos (including this project) explicitly forbid `Co-Authored-By` trailers. Check `CLAUDE.md` or recent commit history for the project convention before adding them.

## Examples

- `feat(auth): add password reset flow`
- `fix(api): handle null provider response`
- `ci(actions): restrict pull request token permissions`
- `refactor(utils): extract date formatting helper`
- `docs: update GitHub project board workflow`
