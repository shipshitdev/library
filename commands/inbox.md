# Inbox Task Management

Quick task capture and expansion. Backlog only - no status tracking here.

## Usage

```bash
/inbox                    # View backlog
/inbox [task description] # Quick add
/inbox expand             # Expand task to PRD/TASK
```

---

## Instructions for Claude

### Mode 1: View Inbox (no arguments)

**When:** `/inbox` or `/inbox list`

**Steps:**

1. Read `.agents/TASKS/INBOX.md`
2. Display tasks from "Backlog" section:

   ```
   📥 Inbox (5 tasks)

   1. Add dark mode toggle (2025-11-21) - HIGH
      Users keep requesting this feature

   2. Fix analytics cron job (2025-11-20)
      Sometimes misses hourly runs

   Use `/inbox expand` to create PRD/TASK
   ```

### Mode 2: Quick Capture (arguments provided)

**When:** `/inbox Add dark mode toggle`

**Steps:**

1. Extract task title from arguments
2. Ask: "Brief context? (1-2 sentences)"
3. Add to "Backlog" section:

   ```markdown
   - [ ] **[TASK_TITLE]** ([TODAY_DATE])
     - [USER_CONTEXT]
   ```

4. Confirm: "✅ Added: [TASK_TITLE]"

### Mode 3: Expand to PRD/TASK

**When:** `/inbox expand`

**Steps:**

1. Show numbered list of backlog tasks
2. Ask: "Which task? (number)"
3. Ask clarifying questions:
   - Problem statement
   - Target users
   - Success criteria
   - Technical approach
   - Priority
4. Create PRD (`.agents/PRDS/`) or TASK (`.agents/TASKS/`)
5. **Remove task from INBOX.md** (it now lives in PRD/TASK)
6. Confirm: "✅ Created: [FILE_PATH]"

---

## File Paths

**Inbox:** `.agents/TASKS/INBOX.md`

**PRDs:** `.agents/PRDS/{category}/{name}.md`
**Tasks:** `.agents/TASKS/{category}/{name}.md`

Categories: `studio/`, `manager/`, `publisher/`, `analytics/`, `api/`, `infrastructure/`

---

## Task Format

```markdown
- [ ] **Task Title** (YYYY-MM-DD)
  - Brief context (1-2 sentences)
  - Priority: HIGH/MEDIUM/LOW (optional)
```

Keep it simple. Once expanded, remove from inbox.
