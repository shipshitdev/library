# Bug Capture - Quick Bug Documentation

Quick bug capture as a GitHub Issue for later triage and fixing.

## When to Use

- User reports something is broken
- You discover a bug during development
- User describes unexpected behavior
- Need to track an issue for later

## Process

### Step 1: Minimal Questions

Ask only the essentials:

- Which app/area is affected?
- What's broken? (brief description)

Keep it fast.

### Step 2: Create GitHub Issue

```bash
gh issue create \
  --title "Bug: [Short Description]" \
  --body "$(cat <<'EOF'
## What's Wrong

[User description of the problem]

## Steps to Reproduce

1. [Step 1]
2. [Step 2]

## Expected Behavior

[What should happen]

## Actual Behavior

[What actually happens]

## Area Affected

[App / service / component]
EOF
)" \
  --label "bug" \
  --label "priority:high"
```

### Step 3: Inform User

Bug captured!

Issue: <URL from gh output>

You can add more details or fix it now — just reference the issue number.

## Issue Title Convention

Format: `Bug: [short-descriptive-name]`

Good titles:

- Bug: Login redirect loop
- Bug: Video upload fails on large files
- Bug: Missing captions in export

Bad titles:

- Bug (too generic)
- Bug #1 (use description)

## Quick Capture vs Full Task

Use /bug when:

- Don't have time for full analysis
- Just need to track it
- Will investigate later

Use /task when:

- Ready to fix now
- Have full context
- Need an implementation plan
