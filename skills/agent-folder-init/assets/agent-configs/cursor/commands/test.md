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

### Step 2: Label the Area

Track the test as a GitHub Issue, labeled by area so it stays filterable:

- Frontend: `--label "test,area:frontend"`
- Backend: `--label "test,area:api"`
- Extension: `--label "test,area:extension"`
- Mobile: `--label "test,area:mobile"`
- Cross-cutting: `--label "test,area:general"`

### Step 3: Create the Issue

Use the template below as the issue body, with specific scenarios:

```bash
gh issue create --title "Test: [Feature/Area Name]" --label "test,area:[area]" --body "$(cat <<'BODY'
[template body here]
BODY
)"
```

### Step 4: Inform User

```
Test tracked! ✅

Issue: #[number] — Test: [Feature/Area Name]

You can check off scenarios in the issue as you test them.
```

## Issue Body Template

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

- **Issue:** [link to the feature/task issue if applicable]
- **PRD:** [link to PRD issue if applicable]
- **Related tests:** [link to related test issues]

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

## Title Convention

**Format:** `Test: [feature-or-area-name]`

**Good titles:**

- `Test: video generation with captions`
- `Test: organization isolation`
- `Test: multi-platform publishing`
- `Test: payment flow`

**Bad titles:**

- `Test` (too generic)
- `Test 1` (use a description, not numbers)

## Example Interaction

**User:** "We should test the new video caption feature before shipping"

**AI Response:**

```
Good idea! Let me create a test tracking file for that.

✅ Test tracked as issue #142 (labeled test, area:frontend)

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

1. **Create the tracking issue** when feature is ready for testing
2. **Execute tests** and check off scenarios in the issue
3. **Log results** in a Test Results Log comment on the issue
4. **Open bug issues** for any issues found (use `/bug` command)
5. **Close the issue** when all scenarios pass
6. **Keep closed / reopen** for regression testing

## Integration with Other Commands

**Creating test from task:**

After implementing a task, create a test issue:

```bash
# Use /test command
# Reference the task/PRD issue in the test issue
```

**Linking in sessions:**

```markdown
## Testing

- Test: Video Captions (#142) - In Progress
  - Happy path: ✅ Pass
  - Edge cases: 🔄 Testing
  - Found 2 bugs (logged as issues)
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
