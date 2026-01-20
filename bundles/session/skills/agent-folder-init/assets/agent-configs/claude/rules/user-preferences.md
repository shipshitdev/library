# User Personal Preferences & Instructions

**CRITICAL: READ THIS FIRST - EVERY SESSION**

This file contains specific preferences and instructions that override or supplement standard documentation. These are non-negotiable rules.

---

## 1. NEVER RUN BACKGROUND PROCESSES

**FORBIDDEN:**

```bash
# NEVER use run_in_background parameter
Bash(command: "any command", run_in_background: true)

# NEVER background with &
npm run dev &
pnpm dev &
any-long-running-command &
```

**ALLOWED:**

- Run commands in foreground ONLY
- User must see exactly what is running
- User must know when processes start and stop

**WHY:** Background processes kill CPU without user visibility.

---

## 2. NEVER BUILD/TEST LOCALLY AFTER CODE CHANGES

**FORBIDDEN:**

```bash
pnpm run build
pnpm run test
npm run build
npm test
```

**ALLOWED:**

- Make code changes
- Commit and push to GitHub
- Let CI/CD handle builds and tests

**WHY:** Building locally wastes time and kills the dev machine. Tests run in GitHub Actions ONLY.

---

## 3. CHECK RECENT SESSIONS BEFORE IMPLEMENTING

**MANDATORY BEFORE ANY CODE:**

1. Search for similar work in session history
2. Read the actual implementation from past sessions
3. Find the files that were changed
4. Copy that exact pattern
5. DO NOT re-implement something already solved

**WHY:** Prevents forgetting previous fixes and implementing worse solutions.

---

## 4. FOLLOW EXISTING CODEBASE PATTERNS

**MANDATORY BEFORE ANY CODE:**

1. Find 3-5 REAL examples in the codebase
2. Read those files completely (not just skim)
3. Copy the EXACT pattern from those files:
   - Same import structure
   - Same decorator usage
   - Same error handling
   - Same naming conventions
   - Same method signatures
4. DO NOT invent new patterns or use generic "best practices"

**WHY:** The codebase has established patterns. Follow them exactly.

---

## 5. QUALITY OVER SPEED

**STOP:**

- Rushing through implementations
- Giving half-assed explanations
- Suggesting generic solutions without checking codebase first
- Assuming anything - verify by reading actual code

**DO:**

1. Read the actual codebase for every question/task
2. Find real examples of similar code
3. Think through the implementation before writing
4. Test logic mentally against edge cases
5. Give precise, specific answers based on actual code

---

## 6. ALWAYS DOCUMENT BEFORE /clear

**FORBIDDEN:**

```bash
# User types /clear
# AI does nothing and loses all context
```

**MANDATORY:**

1. IMMEDIATELY document the session when user types /clear
2. Wait for documentation to complete before clearing
3. Confirm documentation is saved
4. THEN allow /clear to proceed

**WHY:** Without documentation, all context is lost. Next session must know what was done.

---

## 7. NEVER WORK OUTSIDE WORKSPACE DIRECTORY

**FORBIDDEN:**

```bash
# NEVER use /tmp or any directory outside workspace
python3 /tmp/validation_script.py
echo "script" > /tmp/temp.sh
cat /private/tmp/data.json

# NEVER create files outside workspace
/tmp/analyze.py
/var/tmp/cleanup.sh
~/Desktop/temp-files/
```

**ALLOWED:**

- ALL operations within the current workspace directory
- If temp files needed, use a temp directory within workspace
- All scripts, validation, and operations stay in workspace

**WHY:** Working outside workspace creates invisible file pollution.

---

## 8. NEVER COMMIT/PUSH WITHOUT EXPLICIT REQUEST

**FORBIDDEN:**

```bash
# NEVER commit without explicit user request
git add .
git commit -m "any message"

# NEVER push without explicit user request
git push origin branch
```

**ALLOWED:**

- Make code changes
- Show user what changed (git diff, git status)
- WAIT for user to review and approve
- User commits and pushes when ready

**WHY:** The user owns the git history.

---

## 9. Communication Style

- Acknowledge when something was done wrong
- Don't make excuses
- Fix it properly
- Move on

---

## Session Start Checklist

Before EVERY response, verify:

- [ ] Read this file
- [ ] Checked for user-specific preferences on this topic
- [ ] Following user's preferred patterns
- [ ] Not repeating past mistakes

---

## Feedback Loop

When user corrects me or expresses frustration:

1. **STOP** - acknowledge the correction
2. **UPDATE** preferences immediately
3. **CONFIRM** understanding with user
4. **APPLY** going forward

---

**Remember:** This file represents USER preferences, not generic best practices. When in conflict, USER PREFERENCES WIN.
