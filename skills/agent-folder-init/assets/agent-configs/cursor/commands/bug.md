# Bug Capture - AI Agent Command

**Purpose:** Quick bug capture for later triage and fixing. Don't worry about details - just get it documented fast.

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

That's it! Keep it fast.

### Step 2: Determine File Location

**CRITICAL:** Follow new Kanban Markdown structure (flat tasks directory)

**Bug file location:**

- Frontend bugs: `[frontend-project]/.agents/TASKS/bug-[short-name].md`
- Backend bugs: `[backend-project]/.agents/TASKS/bug-[short-name].md`
- Other projects: Adapt project paths to your structure
- Cross-project: `.agents/TASKS/bug-[short-name].md`

**Bug PRD location:**

- Frontend bugs: `[frontend-project]/.agents/PRDS/bugs/bug-[short-name].md`
- Backend bugs: `[backend-project]/.agents/PRDS/bugs/bug-[short-name].md`
- Other projects: Adapt project paths to your structure
- Cross-project: `.agents/PRDS/bugs/bug-[short-name].md`

**Create `bugs/` subdirectory in PRD folder if it doesn't exist.**

### Step 3: Create Bug Files (Task + PRD)

**Task file** - Structured format:

```markdown
## Task: Bug: [Short Description]

**ID:** bug-short-name
**Label:** Bug: [Short Description]
**Description:** [Brief description of the bug]
**Type:** Bug
**Status:** Backlog
**Priority:** High
**Created:** YYYY-MM-DD
**Updated:** YYYY-MM-DD
**PRD:** [Link](../PRDS/bugs/bug-short-name.md)

---

## Additional Notes

Linked PRD: ../PRDS/bugs/bug-short-name.md
```

**PRD file** - Full bug details (use template below)

### Step 4: Inform User

```
Bug captured! 📝

Task: <project>/.agents/TASKS/bug-[name].md
PRD: <project>/.agents/PRDS/bugs/bug-[name].md

You can clean it up later and convert to a proper fix task when ready to implement.
```

## Templates

### Bug Task File (Structured Format)

**File:** `<project>/.agents/TASKS/bug-[short-name].md`

```markdown
## Task: Bug: [Short Description]

**ID:** bug-short-name
**Label:** Bug: [Short Description]
**Description:** [Brief description of the bug]
**Type:** Bug
**Status:** Backlog
**Priority:** High
**Created:** YYYY-MM-DD
**Updated:** YYYY-MM-DD
**PRD:** [Link](../PRDS/bugs/bug-short-name.md)

---

## Additional Notes

Linked PRD: ../PRDS/bugs/bug-short-name.md
```

### Bug PRD File (Details)

**File:** `<project>/.agents/PRDS/bugs/bug-[short-name].md`

**CRITICAL:** No checkboxes (`- [ ]` or `- [x]`) in PRD. Use plain bullets `-`.

```markdown
# Bug: [Short Description]

**Priority:** High | Medium | Low | TBD  
**Status:** Reported | In Progress | Fixed  
**Type:** Bug  
**Severity:** Critical | High | Medium | Low | TBD  
**App:** [app name]  
**Area:** [specific area/feature if known]  
**Reported:** YYYY-MM-DD  
**Last Updated:** YYYY-MM-DD

---

## What's Wrong

[User's description of the problem - exactly as they described it]

## Steps to Reproduce

1. [Step 1]
2. [Step 2]
3. [Step 3]

_Unknown - to be investigated_

## Expected Behavior

[What should happen]

## Actual Behavior

[What actually happens]

## Environment (if relevant)

- Browser: [browser name/version]
- Device: [desktop/mobile/tablet]
- OS: [operating system]
- Other: [any other relevant info]

## Error Messages (if any)
```

[Paste any error messages or console logs here]

```

## Screenshots/Videos (if available)

[Link to screenshots or describe visual issues]

## Possible Cause (if suspected)

[Any hunches about what might be causing this]

## Root Cause (after investigation)

[Once investigated, document the root cause here]

## Fix Approach

[How this will be fixed]

## Files Affected

- `path/to/file.ts` - [what needs to change]

## Testing

- Manual testing steps
- Edge cases to verify
- Regression prevention

## Notes

[Any additional context, workarounds, or related information]

## Related Issues

- Related to: [link to related bugs/tasks if any]

---

**Next Steps:**
- Reproduce the bug
- Identify root cause
- Assess priority and severity
- Implement fix
- Add regression test
```

## Naming Convention

**Format:** `bug-[short-descriptive-name].md`

**Good names:**

- `bug-login-redirect-loop.md`
- `bug-video-upload-fails-large-files.md`
- `bug-missing-captions-preview.md`
- `bug-org-filter-not-working.md`

**Bad names:**

- `bug.md` (too generic)
- `bug-1.md` (use description, not numbers)
- `loginBug.md` (wrong case)
- `bug_login.md` (use kebab-case)

## Example Interaction

**User:** "The video preview is broken in Studio - it just shows a black screen"

**AI Response:**

```
Got it! Let me capture this bug quickly.

📝 Bug captured:
   Task: [project]/.agents/TASKS/bug-video-preview-black-screen.md
   PRD: [project]/.agents/PRDS/bugs/bug-video-preview-black-screen.md

I've documented:
- App: Studio
- Issue: Video preview showing black screen
- Status: Reported (needs investigation)
- Kanban: Added to Backlog column

You can add more details later when you have time to investigate. Want me to look into it now or just keep it tracked for later?
```

## Workflow After Capture

1. **Triage:** Review the bug, add priority/severity
2. **Investigate:** Reproduce and identify root cause
3. **Convert:** Use `/task` command to create proper task + PRD
4. **Fix:** Implement the fix following task workflow
5. **Close:** Mark bug as resolved, reference fix commit/PR

## Quick Capture vs Full Task

**Use `/bug` when:**

- Don't have time for full analysis
- Just need to track it
- Will investigate later
- Quick report from user

**Use `/task` (Bug Fix template) when:**

- Ready to fix now
- Have full context
- Need implementation plan
- Want to start immediately

## Investigation Checklist

When ready to investigate a captured bug:

**Quick Checks:**

- [ ] Can you reproduce it consistently?
- [ ] Check recent changes (git log, sessions)
- [ ] Verify organization isolation (all queries filtered)
- [ ] Check error logs
- [ ] Review related code

**For detailed debugging:** See your project's debugging documentation

**When investigation complete:** Use `/task` command to create implementation plan

## Integration with Other Commands

**Converting bug to task:**

```bash
# After investigation, convert to proper task:
# 1. Use /task command with Bug Fix template
# 2. Reference original bug file
# 3. Optionally delete or archive original bug file
```

**Linking in sessions:**

```markdown
## Bugs Found

- [Bug: Video Preview Black Screen]([project]/.agents/TASKS/bug-video-preview-black-screen.md) - [PRD]([project]/.agents/PRDS/bugs/bug-video-preview-black-screen.md)
```

---

**Created:** 2025-10-19  
**Purpose:** Fast bug capture without ceremony - triage and fix later
