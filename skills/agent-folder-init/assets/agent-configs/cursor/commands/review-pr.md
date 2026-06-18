# Pull Request Review Checklist

**Purpose:** Systematic code review for quality, security, and consistency

## When to Use

- Reviewing PRs before merge
- Self-review before submitting PR
- Quality check before deployment

## Review Checklist

### 1. Code Quality

#### TypeScript

```
- [ ] No `any` types used
- [ ] All interfaces/types in separate files (packages/props/ or packages/interfaces/)
- [ ] Proper return types on all functions
- [ ] No unused imports
- [ ] No console.log statements (use LoggerService)
```

#### Patterns

```
- [ ] Follows patterns established in codebase (find 3+ real examples)
- [ ] Uses service singletons (.getInstance())
- [ ] BaseCRUDController used when appropriate
- [ ] BaseService used when appropriate
- [ ] Props in packages/props/
- [ ] Services in packages/services/
```

### 2. Security & Data Isolation

#### Multi-Tenancy

```
- [ ] ALL queries filter by organization
- [ ] ALL queries filter isDeleted: false
- [ ] No cross-organization data leaks possible
- [ ] User can only access their org's data
```

#### Input Validation

```
- [ ] DTOs with validation decorators
- [ ] Sanitize user input
- [ ] Check permissions before operations
- [ ] Validate IDs are valid ObjectIds
```

#### Authentication

```
- [ ] ClerkAuthGuard applied
- [ ] @CurrentUser() decorator used
- [ ] JWT token validated
- [ ] No public endpoints (unless intended)
```

### 3. Database Operations

#### Queries

```
- [ ] Always include organization filter
- [ ] Always include isDeleted: false
- [ ] Use projections for large docs
- [ ] Indexes exist for common queries
- [ ] No N+1 query problems
```

#### Schema

```
- [ ] Timestamps enabled ({ timestamps: true })
- [ ] isDeleted: boolean (NOT deletedAt)
- [ ] organization field required
- [ ] Simple indexes in schema
- [ ] Compound indexes in module
```

### 4. Error Handling

```
- [ ] Try/catch blocks present
- [ ] Appropriate NestJS exceptions thrown
- [ ] Errors logged with LoggerService
- [ ] Generic error messages to client (no internals)
- [ ] Re-throw NestJS exceptions (don't convert)
```

### 5. Testing

#### Coverage

```
- [ ] Unit tests written
- [ ] All public methods tested
- [ ] Error cases tested
- [ ] Edge cases tested
- [ ] Tests passing
- [ ] Coverage > 70% for new code
```

#### Test Quality

```
- [ ] Tests are meaningful (not just for coverage)
- [ ] Mocks all dependencies
- [ ] Tests organization isolation
- [ ] Tests soft delete filtering
- [ ] Tests error scenarios
```

### 6. Frontend Specific

```
- [ ] Components in packages/components/
- [ ] Props interfaces in packages/props/
- [ ] Services use singleton pattern
- [ ] No inline styles (use Tailwind)
- [ ] Loading states handled
- [ ] Error states handled
- [ ] Accessibility (aria labels, keyboard nav)
```

### 7. API Specific

```
- [ ] Swagger decorators present
- [ ] Proper HTTP status codes
- [ ] DTOs for request/response
- [ ] Rate limiting considered
- [ ] Queue jobs for heavy operations
- [ ] WebSocket events for real-time updates
```

### 8. Performance

```
- [ ] No unnecessary re-renders (React)
- [ ] Database queries optimized
- [ ] Proper use of indexes
- [ ] No blocking operations in API
- [ ] Images/assets optimized
- [ ] Bundle size impact checked
```

### 9. Documentation

```
- [ ] .agents/memory/ updated (if architectural change)
- [ ] Session file created in .agents/sessions/
- [ ] GitHub Issue closed or commented (if applicable)
- [ ] Comments for complex logic
- [ ] README updated if needed
```

### 10. Best Practices

```
- [ ] Follows SOLID principles
- [ ] DRY (Don't Repeat Yourself)
- [ ] YAGNI (You Aren't Gonna Need It)
- [ ] Code is self-documenting
- [ ] Meaningful variable names
- [ ] Functions < 50 lines
- [ ] Files < 300 lines
```

## Common Issues to Check

### ❌ Critical Issues (Must Fix)

1. **Security Vulnerability**

   ```typescript
   // BAD
   const items = await this.model.find({}); // ❌ No org filter
   ```

2. **Data Leak**

   ```typescript
   // BAD
   return await this.model.find({ _id: id }); // ❌ Could be different org
   ```

3. **Type Safety**

   ```typescript
   // BAD
   function process(data: any) {} // ❌ any type
   ```

4. **Missing Error Handling**

   ```typescript
   // BAD
   const result = await externalAPI.call(); // ❌ No try/catch
   ```

### ⚠️ Warning Issues (Should Fix)

1. **Performance**

   ```typescript
   // Warning
   const items = await Promise.all(
     ids.map((id) => this.model.findById(id)) // Could batch
   );
   ```

2. **Maintainability**

   ```typescript
   // Warning
   if (x && y && z && a && b && c) {
   } // Too complex
   ```

3. **Consistency**

   ```typescript
   // Warning - Inconsistent with codebase patterns
   export default MyComponent; // We use named exports
   ```

## Review Commands

### Run Linter

```bash
npm run lint
npm run format
```

### Run Tests

```bash
npm test
npm test -- --coverage
```

### Check Types

```bash
npm run type-check
```

### Check Bundle Size

```bash
npm run build:all
npm run analyze
```

## AI Review Prompt

Use this prompt for AI-assisted review:

```
Review this PR against project standards:

1. Read: CLAUDE.md (repo-level) for project rules
2. Read: .agents/memory/ for architecture and patterns
3. Verify: Organization filtering in all queries
4. Verify: isDeleted: false filtering
5. Check: No `any` types
6. Check: Props in separate files
7. Check: Error handling present
8. Check: Tests exist and pass

Report:
- ✅ What's good
- ❌ What must be fixed
- ⚠️ What should be improved
- 📝 Suggestions
```

## Approval Criteria

### Must Have (Block Merge)

- ✅ No security issues
- ✅ All queries filter by organization
- ✅ All queries filter isDeleted: false
- ✅ No `any` types
- ✅ Tests passing
- ✅ Linter passing

### Should Have (Strong Recommendation)

- ✅ > 70% test coverage
- ✅ Follows existing patterns
- ✅ Documentation updated
- ✅ Performance considered

### Nice to Have

- ✅ > 80% test coverage
- ✅ Accessibility improvements
- ✅ Performance optimizations

## Quick Decision Tree

```
Is there a security issue?
  YES → ❌ Block merge
  NO → Continue

Does it filter by organization?
  NO → ❌ Block merge
  YES → Continue

Does it filter isDeleted: false?
  NO → ❌ Block merge
  YES → Continue

Are there `any` types?
  YES → ❌ Block merge
  NO → Continue

Do tests pass?
  NO → ❌ Block merge
  YES → Continue

Is coverage > 70%?
  NO → ⚠️ Request more tests
  YES → Continue

Documentation updated?
  NO → ⚠️ Request update
  YES → ✅ Approve
```

---

**Remember:** Security and data isolation are NON-NEGOTIABLE. Always verify organization filtering!
