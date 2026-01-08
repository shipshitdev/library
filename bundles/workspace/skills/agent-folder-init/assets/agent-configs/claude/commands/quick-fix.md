# Quick Fix - Fast Bug Resolution

Rapid bug fix workflow for straightforward issues.

## When to Use

- Simple, isolated bugs
- Clear reproduction steps
- Obvious fix location
- No architectural changes needed

## Quick Fix Steps

### Step 1: Understand the Bug

Read the bug report or user description. Identify:

- What is broken?
- Where does it happen?
- What is expected behavior?

### Step 2: Locate the Code

Search for relevant files:

- Use grep/glob to find related code
- Read the file(s) involved
- Understand the current implementation

### Step 3: Find Similar Fixes

Search for how similar bugs were fixed before:

- Check git history for related fixes
- Look for patterns in the codebase

### Step 4: Implement Fix

Make the minimal change needed:

- Fix the root cause, not symptoms
- Follow existing code patterns
- Dont refactor while fixing

### Step 5: Verify Fix

- Test the fix manually
- Check edge cases
- Ensure no regression

### Step 6: Document

Brief note of what was fixed and why.

## Quick Fix Rules

DO:

- Fix one thing at a time
- Follow existing patterns
- Test after fixing
- Keep changes minimal

DONT:

- Refactor while fixing
- Add new features
- Change unrelated code
- Skip testing

## When NOT to Quick Fix

Escalate to full task if:

- Root cause is unclear
- Multiple files affected
- Architectural change needed
- Security implications
- Database changes required
