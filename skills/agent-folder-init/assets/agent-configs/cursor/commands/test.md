# Test Tracking - AI Agent Command

**Purpose:** Track manual testing TODOs and test scenarios that need to be verified.

## When to Use

- Need to remember to test a feature
- Want to document test scenarios
- Planning QA for a release
- Found an area that needs testing
- User mentions "we should test X"

## Process

### Step 1: Quick Questions

Ask:

- What needs to be tested?
- Which app/area?
- Any specific scenarios to check?

### Step 2: Determine File Location

**Test file location:**

- Frontend tests: `.agents/TESTS/frontend/[app]/[test-name].md`
- Backend tests: `.agents/TESTS/api/[test-name].md`
- Extension tests: `.agents/TESTS/extension/[test-name].md`
- Mobile tests: `.agents/TESTS/mobile/[test-name].md`
- Cross-cutting: `.agents/TESTS/general/[test-name].md`

**Create directory structure if it doesn't exist.**

### Step 3: Create Test File

Use template below with specific scenarios.

### Step 4: Inform User

```
Test tracked! ✅

File: .agents/TESTS/[area]/[app]/[test-name].md

You can check off scenarios as you test them.
```

## Template

```markdown
# Test: [Feature/Area Name]

**App:** [app name]  
**Type:** Manual Test | Integration Test | E2E Test | Smoke Test  
**Status:** Pending | In Progress | Completed | Blocked  
**Priority:** Critical | High | Medium | Low  
**Added:** YYYY-MM-DD

---

## What to Test

[Brief description of what needs testing and why]

## Test Scenarios

### Happy Path

- [ ] Scenario 1: [describe expected flow]
- [ ] Scenario 2: [describe expected flow]
- [ ] Scenario 3: [describe expected flow]

### Edge Cases

- [ ] Edge case 1: [describe scenario]
- [ ] Edge case 2: [describe scenario]
- [ ] Edge case 3: [describe scenario]

### Error Handling

- [ ] Error case 1: [describe error scenario]
- [ ] Error case 2: [describe error scenario]
- [ ] Error case 3: [describe error scenario]

### Performance

- [ ] Load time acceptable
- [ ] Handles large datasets
- [ ] No memory leaks
- [ ] Responsive under load

### Security

- [ ] Organization isolation verified
- [ ] Soft delete respected
- [ ] Permissions working correctly
- [ ] No data leakage

### Cross-browser/Device (if applicable)

- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Mobile (iOS)
- [ ] Mobile (Android)

## Expected Results

**For each scenario above, the expected result is:**

[Describe what should happen when tests pass]

## Test Data Needed

- [ ] Test users/accounts
- [ ] Sample data
- [ ] Specific configurations
- [ ] External services/APIs

## Environment Setup

[Any special setup required for testing]

## Known Issues/Blockers

[List any blockers preventing testing]

## Notes

[Additional context, dependencies, or considerations]

## Related

- **Task:** [link to task file if applicable]
- **PRD:** [link to PRD if applicable]
- **Related tests:** [link to related test files]

---

**Last Updated:** YYYY-MM-DD

## Test Results Log

### [Date] - [Tester Name]

**Status:** [Pass/Fail/Partial]

**Scenarios Tested:**

- [x] Scenario 1 - ✅ Pass
- [x] Scenario 2 - ❌ Fail (details below)
- [ ] Scenario 3 - Not tested yet

**Issues Found:**

- Issue 1: [description]
- Issue 2: [description]

**Notes:**
[Any observations or notes from testing]

---

[Add more test result logs as testing progresses]
```

## Naming Convention

**Format:** `[feature-or-area-name].md`

**Good names:**

- `video-generation-with-captions.md`
- `organization-isolation.md`
- `multi-platform-publishing.md`
- `payment-flow.md`

**Bad names:**

- `test.md` (too generic)
- `test-1.md` (use description, not numbers)
- `videoTest.md` (wrong case)
- `test_video.md` (use kebab-case)

## Example Interaction

**User:** "We should test the new video caption feature before shipping"

**AI Response:**

```
Good idea! Let me create a test tracking file for that.

✅ Test tracked: .agents/TESTS/frontend/studio/video-generation-with-captions.md

I've set up test scenarios for:
- Happy path (selecting, positioning, styling captions)
- Edge cases (long captions, special characters, multiple languages)
- Error handling (API failures, invalid files)
- Performance (large videos, many captions)
- Cross-browser compatibility

You can check off each scenario as you test. Want me to expand any specific test cases?
```

## Test Types

### Manual Test

Human-performed testing with specific steps and expected outcomes.

### Integration Test

Testing how components/services work together.

### E2E Test

Full user flow from start to finish.

### Smoke Test

Quick sanity check that critical functionality works.

### Regression Test

Verify that bug fixes don't break existing functionality.

### Load/Performance Test

Test system behavior under load or stress.

## Workflow

1. **Create test file** when feature is ready for testing
2. **Execute tests** and check off scenarios
3. **Log results** in the Test Results Log section
4. **Create bug files** for any issues found (use `/bug` command)
5. **Mark complete** when all scenarios pass
6. **Archive or keep** for regression testing

## Integration with Other Commands

**Creating test from task:**

After implementing a task, create a test file:

```bash
# Use /test command
# Reference the task/PRD in the test file
```

**Linking in sessions:**

```markdown
## Testing

- [Test: Video Captions](.agents/TESTS/frontend/studio/video-generation-with-captions.md) - In Progress
  - Happy path: ✅ Pass
  - Edge cases: 🔄 Testing
  - Found 2 bugs (logged in bugs/)
```

**Creating bugs from test failures:**

When a test fails, use `/bug` command to capture the issue.

## Quick vs Comprehensive

**Quick test file:**

- Basic scenarios only
- Minimal detail
- Fast to create

**Comprehensive test file:**

- All scenario types
- Detailed steps
- Performance/security checks
- Cross-browser testing

Choose based on feature complexity and criticality.

---

**Created:** 2025-10-19  
**Purpose:** Track and organize manual testing TODOs and test scenarios
