# Commit Summary - Generate Commit Messages

Generate meaningful commit messages based on staged changes.

## When to Use

- Before committing changes
- When summarizing work done
- For PR descriptions

## Workflow

### Step 1: Review Changes

Check what has changed:

- git status - see modified files
- git diff --staged - see staged changes
- git log --oneline -5 - see recent commits for style

### Step 2: Analyze Changes

Categorize the changes:

- feat: New feature
- fix: Bug fix
- refactor: Code restructuring
- docs: Documentation only
- test: Adding/updating tests
- chore: Maintenance tasks

### Step 3: Generate Message

Create commit message following conventional commits:

Format:
type(scope): short description

- What changed
- Why it changed (if not obvious)

### Step 4: Review

Ensure message:

- Accurately describes changes
- Follows project conventions
- Is concise but complete

## Commit Message Guidelines

Good commit messages:

- Start with type (feat, fix, refactor, etc.)
- Include scope if applicable
- Use imperative mood (Add not Added)
- Keep first line under 72 chars
- Explain why, not just what

Examples:

- feat(auth): add password reset flow
- fix(api): handle null response from external service
- refactor(utils): extract date formatting to shared helper
- docs: update API endpoint documentation

## What NOT to Do

- Vague messages (fix stuff, update code)
- Too long first lines
- Missing context for non-obvious changes
- Committing unrelated changes together
