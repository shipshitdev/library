# Test - Testing Workflow

Systematic approach to writing and running tests.

## When to Use

- After implementing new features
- Before refactoring
- When fixing bugs
- For test coverage improvement

## Testing Steps

### Step 1: Identify What to Test

- New functionality added
- Bug fixes (regression tests)
- Edge cases
- Error handling paths

### Step 2: Find Similar Tests

Search for existing test patterns in the codebase:
- How are similar features tested?
- What mocking patterns are used?
- What assertion styles?

### Step 3: Write Tests

Follow existing patterns:
- Unit tests for isolated logic
- Integration tests for workflows
- E2E tests for critical paths

### Step 4: Run Tests

Execute the test suite and verify all pass.

### Step 5: Check Coverage

Ensure new code has adequate test coverage (target: 70%+).

## Test Types

### Unit Tests
- Test isolated functions/methods
- Mock all dependencies
- Fast execution
- High coverage

### Integration Tests
- Test component interactions
- Use real dependencies where practical
- Test API endpoints
- Test database operations

### E2E Tests
- Test user flows
- Browser automation
- Critical path coverage
- Slower but comprehensive

## Testing Best Practices

DO:
- Write tests before or with code
- Test edge cases
- Use descriptive test names
- Mock external dependencies
- Keep tests fast

DONT:
- Skip error case testing
- Write flaky tests
- Test implementation details
- Ignore failing tests
- Over-mock (test nothing)

## Test Quality Checklist

- Tests are independent (no shared state)
- Tests are deterministic (same result every run)
- Tests are fast (< 1 second each)
- Tests are readable (clear intent)
- Tests cover happy path and error cases
