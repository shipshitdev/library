# Code Refactoring Workflow

Systematic approach to refactoring code safely.

## When to Use

- Code is complex/hard to understand
- Duplicate code found
- Performance issues
- Need to improve maintainability
- Technical debt reduction

## Refactoring Steps

### Step 1: Identify the Problem

Common Refactoring Triggers:

- Function > 50 lines
- File > 300 lines
- Duplicate code (3+ instances)
- Complex conditionals (> 3 levels deep)
- Hard to test
- Hard to understand
- any types (TypeScript)

### Step 2: Write Tests First

CRITICAL: Test before refactoring!

Write comprehensive tests for current behavior, run them, verify they pass.

### Step 3: Check Examples

Find similar patterns in the codebase before refactoring.

### Step 4: Make Small Changes

Refactor incrementally:

1. Extract Function - Break large functions into smaller ones
2. Extract Constants - Replace magic numbers
3. Replace any with Types - Add proper TypeScript types

### Step 5: Run Tests After Each Change

After EVERY change, run tests to verify behavior unchanged.

### Step 6: Common Patterns

- Extract Service: Move business logic from controllers to services
- Extract Component: Break large UI components into smaller ones
- Replace Conditionals: Use strategy pattern for complex if/else

### Step 7: Performance Refactoring

- Fix N+1 queries with batch operations
- Add memoization for expensive React components
- Use proper database indexes

### Step 8: Refactoring Checklist

Before starting:

- All tests passing
- Understanding what the code does
- Have example pattern to follow
- Committed current working code

During refactoring:

- Make one change at a time
- Run tests after each change
- Keep same public API
- Document why (not just what)

After refactoring:

- All tests still passing
- No behavior changes
- Code is more readable
- Performance same or better

## Safe Refactoring Rules

1. Always have tests first
2. One change at a time
3. Run tests after each change
4. Keep same behavior
5. Dont change public API
6. Commit working states
7. Document why, not just what

## Quick Wins

Low-risk, high-value refactorings:

1. Replace any with proper types
2. Extract magic numbers to constants
3. Extract duplicate code to functions
4. Add missing error handling
5. Rename unclear variables
6. Add TypeScript return types

Remember: Refactoring = Behavior stays same, structure improves.
