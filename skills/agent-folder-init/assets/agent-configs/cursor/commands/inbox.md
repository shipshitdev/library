# Inbox Task Management

Quick task capture and triage via GitHub Issues. Backlog lives in GitHub — not local files.

## Usage

```bash
/inbox                    # View open issues
/inbox [task description] # Quick capture as GitHub Issue
/inbox expand             # Expand a captured issue into a full implementation plan
```

---

## Instructions for Claude

### Mode 1: View Inbox (no arguments)

**When:** `/inbox` or `/inbox list`

**Steps:**

1. Run `gh issue list --state open`
2. Display open issues:

   ```
   📥 Open Issues (5)

   #12  Add dark mode toggle (2025-11-21) - HIGH
        Users keep requesting this feature

   #11  Fix analytics cron job (2025-11-20)
        Sometimes misses hourly runs

   Use `/inbox expand` to create an implementation plan
   ```

### Mode 2: Quick Capture (arguments provided)

**When:** `/inbox Add dark mode toggle`

**Steps:**

1. Extract task title from arguments
2. Ask: "Brief context? (1-2 sentences)"
3. Create a GitHub Issue:

   ```bash
   gh issue create --title "[TASK_TITLE]" --body "[USER_CONTEXT]"
   ```

4. Confirm: "✅ Issue created: #N [TASK_TITLE]"

### Mode 3: Expand to Implementation Plan

**When:** `/inbox expand`

**Steps:**

1. Show numbered list from `gh issue list --state open`
2. Ask: "Which issue? (number)"
3. Fetch full issue: `gh issue view <number>`
4. Ask clarifying questions:
   - Problem statement
   - Target users
   - Success criteria
   - Technical approach
   - Priority
5. Use `/task` command to create the full implementation plan
6. Reference the GitHub Issue number in the task
7. Confirm: "✅ Implementation plan ready. Issue #N linked."

---

## GitHub Issues Workflow

**View:** `gh issue list --state open`

**Create:** `gh issue create --title "..." --body "..."`

**View detail:** `gh issue view <number>`

**Label/assign:** `gh issue edit <number> --add-label "..." --assignee "..."`

**Close when done:** `gh issue close <number>`

---

## Task Format (for quick capture body)

Keep the issue body simple. Once expanded into a full implementation plan, update the issue with a link to the session notes.

```
Brief context (1-2 sentences).
Priority: HIGH/MEDIUM/LOW
```

Keep it simple. Once expanded into a full plan, close or update the issue.
