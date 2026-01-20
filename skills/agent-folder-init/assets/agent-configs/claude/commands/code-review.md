# Code Review - Comprehensive Review

Comprehensive code review focusing on quality, security, performance, and testing.

## When to Use

- Before merging PRs
- After completing features
- During refactoring
- Self-review before submission
- Security audit

## Quick Review

For fast pre-commit checks:

- git status
- git diff HEAD~1
- git log --oneline -5

Then review against critical checklist.

## Review Categories

### 1. Code Quality

TypeScript Excellence:

- No any types (use proper types)
- Interfaces in dedicated files
- Return types on all functions
- No unused imports
- Proper logging (not console.log)

Pattern Compliance:

- Follows existing codebase patterns
- Consistent with similar code
- Uses established abstractions

### 2. Security

Critical Checks:

- Input validation present
- Auth checks before operations
- No sensitive data in responses
- No hardcoded secrets

### 3. Database Operations

Query Review:

- Proper filtering applied
- Projections for large documents
- Indexes exist for query patterns
- No N+1 query problems
- Pagination for large result sets

### 4. Error Handling

Required:

- Try/catch blocks present
- Errors logged properly
- Generic error messages to client
- Dont expose internal details

### 5. Testing

Required:

- Unit tests exist
- All public methods tested
- Error cases tested
- Tests passing

### 6. Performance

Check:

- No blocking operations in API routes
- Heavy operations use queues
- Database queries optimized
- Caching where appropriate

### 7. Documentation

Check:

- Code comments for complex logic
- API documentation updated
- README updated if needed

## Review Checklist

Before approval:

- All tests passing
- No security issues
- No any types
- Follows patterns
- Documentation updated
- Performance acceptable

## Approval Criteria

BLOCK if:

- Security issues present
- Tests failing
- Build failing

REQUEST CHANGES if:

- Coverage too low
- Missing documentation
- Performance concerns

APPROVE if:

- All checks pass
- Code is clean
- Ready for production
