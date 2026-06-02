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

### Step 2: Create GitHub Issue

```bash
gh issue create \
  --title "Bug: [Short Description]" \
  --label "bug" \
  --body "$(cat <<'EOF'
## What's Wrong

[User's description of the problem - exactly as they described it]

## App / Area

[App name and specific area/feature]

## Steps to Reproduce

_Unknown - to be investigated_

## Expected Behavior

[What should happen]

## Actual Behavior

[What actually happens]

## Environment (if relevant)

- Browser: [browser name/version]
- Device: [desktop/mobile/tablet]

## Error Messages (if any)

[Paste any error messages or console logs here]

## Possible Cause (if suspected)

[Any hunches about what might be causing this]

## Notes

[Any additional context, workarounds, or related information]

**Next Steps:**
- Reproduce the bug
- Identify root cause
- Assess priority and severity
- Implement fix
- Add regression test
EOF
)"
```

### Step 3: Inform User

```
Bug captured! 📝

GitHub Issue: #N — Bug: [Short Description]

You can add more details later and convert to a proper fix task when ready to implement.
```

## Naming Convention

**Issue title format:** `Bug: [short-descriptive-name]`

**Good titles:**

- `Bug: Login redirect loop`
- `Bug: Video upload fails on large files`
- `Bug: Missing captions in preview`
- `Bug: Org filter not applied on search`

**Bad titles:**

- `bug` (too generic)
- `issue 1` (use description, not numbers)
- `Video Gen broken` (not specific enough)

## Example Interaction

**User:** "The video preview is broken in Studio - it just shows a black screen"

**AI Response:**

```
Got it! Let me capture this bug quickly.

Bug captured: GitHub Issue #47 — Bug: Video preview shows black screen in Studio

I've documented:
- App: Studio
- Issue: Video preview showing black screen
- Status: Open (needs investigation)

You can add more details later when you have time to investigate. Want me to look into it now or just keep it tracked for later?
```

## Workflow After Capture

1. **Triage:** View the issue, add priority/severity labels
2. **Investigate:** Reproduce and identify root cause
3. **Fix:** Implement the fix, reference the issue number in commits
4. **Close:** `gh issue close <number> --comment "Fixed in commit <sha>."`

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
- [ ] Check recent changes (`git log`, session notes)
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
# 2. Reference the GitHub Issue number
# 3. Close the original issue when fix is merged
```

**Linking in sessions:**

```markdown
## Bugs Found

- Issue #47: Bug: Video preview shows black screen (Studio)
```

---

**Created:** 2025-10-19
**Updated:** 2026-06-02 — migrated from local task files to GitHub Issues
**Purpose:** Fast bug capture without ceremony - triage and fix later
