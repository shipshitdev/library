# Review PR - Pull Request Review

Review a pull request for quality, correctness, and best practices.

## When to Use

- Reviewing incoming PRs
- Before merging feature branches
- Code quality gates

## Workflow

### Step 1: Understand Context

Get PR information:
- gh pr view [PR_NUMBER]
- Read PR description
- Understand the goal

### Step 2: Review Changes

Check the diff:
- gh pr diff [PR_NUMBER]
- Review each file changed
- Understand the implementation

### Step 3: Check CI Status

Verify automated checks:
- gh pr checks [PR_NUMBER]
- All tests passing?
- Build succeeding?
- Linting clean?

### Step 4: Evaluate Code

Review against criteria:
- Does it solve the stated problem?
- Is the approach sound?
- Are there edge cases missed?
- Is it maintainable?
- Does it follow patterns?

### Step 5: Provide Feedback

For issues found:
- Be specific about location
- Explain why its a problem
- Suggest alternatives
- Distinguish blocking vs nice-to-have

### Step 6: Decision

- APPROVE if ready to merge
- REQUEST CHANGES if blocking issues
- COMMENT if suggestions only

## Review Criteria

Must Check:
- Tests included for new code
- No security vulnerabilities
- No breaking changes (unless intended)
- Documentation updated

Should Check:
- Code style consistent
- Error handling present
- Performance acceptable
- No unnecessary complexity

## Providing Feedback

Good feedback:
- Specific (line numbers, examples)
- Constructive (how to fix)
- Prioritized (blocking vs suggestion)
- Respectful

Bad feedback:
- Vague (this is wrong)
- Unconstructive (I dont like this)
- Nitpicky on style
- Personal attacks
