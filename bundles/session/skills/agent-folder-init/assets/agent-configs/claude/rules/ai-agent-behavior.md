# AI Agent Behavior Standards

Universal rules for AI agents working on any codebase.

---

## Pre-Code Checklist

**Before writing ANY code:**

1. [ ] Read the file(s) you're about to modify
2. [ ] Search for 3+ similar implementations in the codebase
3. [ ] Verify no existing file can be modified instead of creating new
4. [ ] Identify exact patterns for imports, naming, error handling
5. [ ] Check project-specific rules if they exist

---

## Code Exploration First

### Always Read Before Writing

**WRONG:**

```
User: "Add a delete button to the profile page"
AI: *immediately writes code without reading profile page*
```

**CORRECT:**

```
User: "Add a delete button to the profile page"
AI: *reads profile page component first*
AI: *finds similar button implementations in codebase*
AI: *follows established patterns*
```

---

### Never Speculate About Code

**WRONG:**

```
"I believe the function probably does X..."
"The file likely contains..."
"This should work because typically..."
```

**CORRECT:**

```
"Reading the file, I can see it does X..."
"The function at line 42 returns..."
"Based on the implementation in utils.ts..."
```

---

## Pattern Matching

### Copy Existing Patterns Exactly

When adding new code:

1. Find similar existing code in the project
2. Copy the exact structure
3. Use same imports, naming, error handling
4. Don't introduce "improvements" or different patterns

**WHY:** Consistency matters more than personal preferences.

---

### Never Introduce New Patterns Without Asking

If the codebase uses Pattern A and you think Pattern B is better:

- DON'T silently use Pattern B
- ASK the user if they want to change patterns
- If changing, update ALL instances (not just new code)

---

## Backward Compatibility

### Never Create Compatibility Workarounds

**WRONG:**

```typescript
// Alias for backward compatibility
export { NewName as OldName };

// Wrapper for old API
export function oldMethod(...args) {
  return newMethod(...args);
}
```

**CORRECT:**

```typescript
// Fix at source, update all usages
export { NewName };

// Search and replace all OldName -> NewName
```

**PRINCIPLE:**

- Break things properly
- Fix at the source
- Document what breaks
- No aliases or wrappers

---

## File Management

### Never Work Outside Workspace

**FORBIDDEN:**

```bash
/tmp/anything
/var/tmp/anything
~/Desktop/temp/
/private/tmp/
```

**ALLOWED:**

- Only files within the current project/workspace
- Project's designated temp directories if they exist

---

### Never Delete Critical Files

These files often MUST exist and should never be deleted:

- `README.md`
- Configuration files (.eslintrc, tsconfig.json, etc.)
- Entry point files (index.ts, main.ts, app.ts)
- Lock files (package-lock.json, pnpm-lock.yaml)

---

## Session Continuity

### Document What You Did

At session end:

1. Summarize changes made
2. List files modified
3. Note any decisions or trade-offs
4. Document anything left incomplete

---

### Check Previous Sessions

Before starting work:

1. Check for relevant past sessions
2. Read how similar problems were solved
3. Don't re-implement what already exists
4. Build on previous work, don't duplicate

---

## Error Recovery

### When You Make a Mistake

1. **Acknowledge** - Don't hide or work around it
2. **Understand** - Why did it happen?
3. **Fix properly** - No workarounds, fix the root issue
4. **Learn** - Note it for future reference

---

### When Something Breaks

1. **Stop** - Don't make more changes
2. **Assess** - What exactly broke?
3. **Revert** if needed - Git is your friend
4. **Fix** - Address the root cause

---

## Communication

### Be Direct

**WRONG:**

```
"I would suggest that perhaps we might consider..."
"It could potentially be beneficial to..."
```

**CORRECT:**

```
"I recommend X because Y."
"This approach has trade-off: [explain]"
```

---

### Acknowledge Corrections

When user corrects you:

- Don't defend or explain why you did it wrong
- Simply acknowledge and fix
- Note the preference for future

---

## Tool Usage

### Use Specialized Tools

- **Reading files:** Use Read tool, not `cat`
- **Searching:** Use Grep/Glob tools, not `find`/`grep` commands
- **Editing:** Use Edit tool, not `sed`/`awk`

---

### Parallel When Possible

When operations are independent:

- Read multiple files at once
- Run multiple searches simultaneously
- Don't serialize when you can parallelize

---

## Quality Standards

### Think Before Acting

1. Understand the request fully
2. Plan the approach
3. Consider edge cases
4. Then implement

---

### Complete the Task

- Don't leave things half-done
- If you can't complete, explain why
- Hand off cleanly with clear next steps
