# Bug Capture - Quick Bug Documentation

Quick bug capture for later triage and fixing.

## When to Use

- User reports something is broken
- You discover a bug during development
- User describes unexpected behavior
- Need to track an issue for later

## Process

### Step 1: Minimal Questions

Ask only the essentials:

- Which app/area is affected?
- Whats broken? (brief description)

Keep it fast.

### Step 2: Determine File Location

Bug file location (adjust paths for your project):

- Frontend bugs: <project>/.agents/TASKS/bug-[short-name].md
- Backend bugs: <project>/.agents/TASKS/bug-[short-name].md
- Cross-project: .agents/TASKS/bug-[short-name].md

### Step 3: Create Bug File

Use structured format:

## Task: Bug: [Short Description]

**ID:** bug-short-name
**Label:** Bug: [Short Description]
**Description:** [Brief description of the bug]
**Type:** Bug
**Status:** Backlog
**Priority:** High
**Created:** YYYY-MM-DD
**Updated:** YYYY-MM-DD

---

## Bug Details

### Whats Wrong

[User description of the problem]

### Steps to Reproduce

1. [Step 1]
2. [Step 2]

### Expected Behavior

[What should happen]

### Actual Behavior

[What actually happens]

### Step 4: Inform User

Bug captured!

File: <project>/.agents/TASKS/bug-[name].md

You can add more details later when ready to fix.

## Naming Convention

Format: bug-[short-descriptive-name].md

Good names:

- bug-login-redirect-loop.md
- bug-video-upload-fails.md
- bug-missing-captions.md

Bad names:

- bug.md (too generic)
- bug-1.md (use description)

## Quick Capture vs Full Task

Use /bug when:

- Dont have time for full analysis
- Just need to track it
- Will investigate later

Use /task when:

- Ready to fix now
- Have full context
- Need implementation plan
