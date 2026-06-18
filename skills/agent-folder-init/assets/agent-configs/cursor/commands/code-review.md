# Enhanced Code Review

**Purpose:** Comprehensive code review focusing on quality, security, performance, and testing.

## When to Use

- Before merging PRs
- After completing features
- During refactoring
- Self-review before submission
- Security audit

## Quick Review

For fast pre-commit checks:

```bash
# Git context
git status
git diff HEAD~1
git log --oneline -5
git branch --show-current
```

Then review against critical checklist (see below).

## Comprehensive Review Process

### 1. Code Quality

#### TypeScript Excellence

```
✅ REQUIRED:
- [ ] No `any` types (use proper types)
- [ ] All interfaces in packages/interfaces/
- [ ] Props in packages/props/
- [ ] Return types on all functions
- [ ] No unused imports
- [ ] No console.log (use LoggerService)

⚠️ PREFERRED:
- [ ] Generic types where appropriate
- [ ] Utility types used (Pick, Omit, Partial)
- [ ] Type guards for runtime checks
- [ ] Discriminated unions for variants
```

**Examples:**

```typescript
// ❌ BAD
async function getData(id: any) {
  const data = await fetch(`/api/${id}`);
  return data;
}

// ✅ GOOD
async function getData(id: string): Promise<DataResponse> {
  const response = await fetch(`/api/${id}`);
  return response.json();
}
```

#### Pattern Compliance

```
- [ ] Follows patterns established in codebase (find 3+ real examples)
- [ ] Uses BaseCRUDController (when appropriate)
- [ ] Uses BaseService (when appropriate)
- [ ] Service singletons use .getInstance()
- [ ] Consistent with existing codebase
- [ ] No reinventing existing patterns
```

**Pattern Check:**

```bash
# Find similar implementations
grep -r "class.*Service" apps/api/src --include="*.ts" | head -5

# Check for pattern usage
grep -r "BaseCRUDController" apps/api/src --include="*.ts"
```

### 2. Security & Multi-Tenancy

#### Critical Security Checks

```
🚨 BLOCKING ISSUES (adapt to your project):
- [ ] Multi-tenancy: ALL queries filter by [tenant/organization field] (if applicable)
- [ ] Soft delete: ALL queries filter [isDeleted/deletedAt] (if applicable)
- [ ] No cross-tenant data access (if multi-tenant)
- [ ] User can only access their authorized data
- [ ] [AuthGuard/Middleware] on protected routes
- [ ] [User injection pattern] used correctly
- [ ] Input validation via [DTOs/schemas]
- [ ] [ID validation] present (ObjectId, UUID, etc.)
```

**Security Pattern Examples:**

```typescript
// ✅ CORRECT - Multi-tenant query (if applicable)
async findPosts(user: User) {
  return this.postsModel.find({
    tenantId: user.tenantId,      // ✅ Multi-tenancy (if applicable)
    isDeleted: false               // ✅ Soft delete (if applicable)
  });
}

// ❌ CRITICAL BUG - No tenant filter (if multi-tenant)
async findPosts() {
  return this.postsModel.find({
    isDeleted: false
  }); // ❌ Data leak! Returns all tenants! (if multi-tenant)
}

// ❌ CRITICAL BUG - No soft delete filter (if using soft delete)
async findPosts(tenantId: string) {
  return this.postsModel.find({
    tenantId
  }); // ❌ Returns deleted items! (if using soft delete)
}
```

#### Authentication Review

```
- [ ] JWT validation in place
- [ ] Token expiration handled
- [ ] Refresh token flow correct
- [ ] No public endpoints (unless intended)
- [ ] Authorization checks before operations
- [ ] Rate limiting implemented
```

### 3. Database Operations

#### Query Review

```
✅ REQUIRED:
- [ ] [Tenant/organization] filter in ALL queries (if multi-tenant)
- [ ] [isDeleted/deletedAt] filter in ALL queries (if using soft delete)
- [ ] Projections for large documents
- [ ] Indexes exist for query patterns
- [ ] No N+1 query problems
- [ ] Pagination for large result sets

⚠️ PERFORMANCE:
- [ ] Batch operations where possible
- [ ] Aggregation pipelines optimized
- [ ] No unnecessary populate()
- [ ] Lean queries when appropriate
```

**Query Examples:**

```typescript
// ✅ GOOD - Optimized query
async findWithPagination(tenantId: string, page: number, limit: number) {
  return this.model
    .find(
      { tenantId, isDeleted: false },  // Adapt filters to your project
      { _id: 1, title: 1, createdAt: 1 }  // Projection
    )
    .sort({ createdAt: -1 })
    .skip((page - 1) * limit)
    .limit(limit)
    .lean();  // Better performance (if using Mongoose)
}

// ⚠️ WARNING - N+1 problem
async getPosts() {
  const posts = await this.postsModel.find();
  return Promise.all(
    posts.map(post => this.getUserForPost(post.userId))  // N queries!
  );
}

// ✅ BETTER - Single query with populate (if using Mongoose)
async getPosts() {
  return this.postsModel
    .find({ tenantId, isDeleted: false })  // Adapt to your filters
    .populate('userId')  // One query with join
    .lean();
}
```

#### Schema Review

```
✅ REQUIRED:
- [ ] Timestamps enabled (if using ORM that supports it)
- [ ] [isDeleted/deletedAt] field present (if using soft delete)
- [ ] [Tenant/organization] field required (if multi-tenant)
- [ ] Simple indexes in schema/model file
- [ ] Compound indexes defined appropriately

📋 CONVENTIONS:
- [ ] Field naming: camelCase
- [ ] References use string type
- [ ] Required fields marked
- [ ] Default values appropriate
- [ ] Validation rules present
```

### 4. Error Handling

```
✅ REQUIRED:
- [ ] Try/catch blocks present
- [ ] NestJS exceptions used (not generic Error)
- [ ] Errors logged via LoggerService
- [ ] Generic error messages to client
- [ ] Don't expose internal details
- [ ] Re-throw NestJS exceptions (don't convert)

⚠️ COMMON MISTAKES:
- [ ] Not catching async errors
- [ ] Swallowing errors silently
- [ ] Exposing stack traces to client
- [ ] Not logging errors
```

**Error Handling Examples:**

```typescript
// ✅ GOOD
async createPost(data: CreatePostDto, user: User) {
  try {
    const post = await this.postsModel.create({
      ...data,
      tenantId: user.tenantId,  // Adapt to your multi-tenancy approach
      isDeleted: false           // Adapt to your soft delete approach
    });
    return post;
  } catch (error) {
    this.logger.error('Failed to create post', error.stack);
    throw new InternalServerErrorException('Failed to create post');
  }
}

// ❌ BAD - Exposing internals
async createPost(data: CreatePostDto) {
  try {
    return await this.postsModel.create(data);
  } catch (error) {
    throw new Error(error.message);  // ❌ Exposes DB error
  }
}

// ❌ BAD - Converting NestJS exception
async findPost(id: string, org: string) {
  const post = await this.postsModel.findOne({
    _id: id,
    organization: org,
    isDeleted: false
  });

  if (!post) {
    throw new NotFoundException('Post not found');  // ✅ Good
  }

  try {
    return this.processPost(post);
  } catch (error) {
    if (error instanceof NotFoundException) {
      throw new Error('Not found');  // ❌ Don't convert!
    }
    throw error;  // ✅ Re-throw as-is
  }
}
```

### 5. Testing Review

```
✅ REQUIRED (Blocking):
- [ ] Unit tests exist
- [ ] All public methods tested
- [ ] Error cases tested
- [ ] Tests passing
- [ ] Coverage > 70% for new code

⚠️ PREFERRED:
- [ ] Edge cases tested
- [ ] Mock all dependencies
- [ ] Test organization isolation
- [ ] Test soft delete filtering
- [ ] Integration tests for flows
```

**Test Quality Examples:**

```typescript
// ✅ GOOD - Tests isolation (if multi-tenant)
it("should only return posts from user tenant", async () => {
  const tenant1Post = await createPost({ tenantId: "tenant1" });
  const tenant2Post = await createPost({ tenantId: "tenant2" });

  const user = { tenantId: "tenant1" };
  const result = await service.findPosts(user);

  expect(result).toContainEqual(tenant1Post);
  expect(result).not.toContainEqual(tenant2Post);
});

// ✅ GOOD - Tests soft delete
it("should not return deleted posts", async () => {
  const post = await createPost({ isDeleted: true });
  const result = await service.findPosts(user);

  expect(result).not.toContainEqual(post);
});

// ⚠️ WEAK - Not testing the right thing
it("should find posts", async () => {
  const result = await service.findPosts(user);
  expect(result).toBeDefined(); // Too generic
});
```

### 6. Performance Review

```
⚠️ CHECK:
- [ ] No blocking operations in API routes
- [ ] Heavy operations use queues (BullMQ)
- [ ] Database queries optimized
- [ ] Proper use of indexes
- [ ] Caching strategy appropriate
- [ ] Images/assets optimized
- [ ] No memory leaks (cleanup in useEffect)
- [ ] Bundle size impact acceptable
```

**Performance Patterns:**

```typescript
// ✅ GOOD - Async processing (if using queues)
async generatePost(prompt: string, user: User) {
  const job = await this.processingQueue.add('generate', {
    prompt,
    userId: user._id,
    tenantId: user.tenantId  // Adapt to your multi-tenancy approach
  });

  return {
    jobId: job.id,
    status: 'processing'
  };
}

// ❌ BAD - Blocking API
async generatePost(prompt: string) {
  const result = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [{ role: 'user', content: prompt }]
  }); // ❌ Blocks for 2-4 seconds!

  return result;
}
```

### 7. Frontend Specific

```
✅ REQUIRED:
- [ ] Components organized appropriately (shared vs local)
- [ ] Type/prop interfaces organized consistently
- [ ] Services use appropriate pattern (singleton, factory, etc.)
- [ ] Styling approach consistent ([Tailwind/CSS Modules/etc.])
- [ ] Loading states handled
- [ ] Error states handled
- [ ] Cleanup in useEffect/hooks (no memory leaks)

⚠️ ACCESSIBILITY:
- [ ] Semantic HTML used
- [ ] ARIA labels present
- [ ] Keyboard navigation works
- [ ] Focus management correct
- [ ] Color contrast sufficient
```

### 8. API Specific

```
✅ REQUIRED:
- [ ] Swagger decorators present
- [ ] Proper HTTP status codes
- [ ] DTOs for request/response
- [ ] Validation pipes enabled
- [ ] Rate limiting considered
- [ ] .http file updated (co-located)

📋 HTTP STATUS CODES:
- 200: Success (GET)
- 201: Created (POST)
- 204: No Content (DELETE)
- 400: Bad Request (validation)
- 401: Unauthorized (auth)
- 403: Forbidden (permissions)
- 404: Not Found
- 429: Rate Limit
- 500: Server Error
```

### 9. Documentation Review

```
- [ ] Session file created (`.agents/sessions/YYYY-MM-DD.md`)
- [ ] Flowchart included (for complex features)
- [ ] .agents/memory/ updated (if architectural change)
- [ ] GitHub Issue closed or commented (if applicable)
- [ ] API docs updated (if applicable)
- [ ] Comments for complex logic
- [ ] JSDoc for public APIs
```

### 10. Best Practices

```
- [ ] SOLID principles followed
- [ ] DRY (Don't Repeat Yourself)
- [ ] YAGNI (You Aren't Gonna Need It)
- [ ] Self-documenting code
- [ ] Meaningful variable names
- [ ] Functions < 50 lines
- [ ] Files < 300 lines
- [ ] No premature optimization
```

## Review Commands

Run these before review:

```bash
# Check git context
git status
git diff HEAD~1
git log --oneline -5

# Run linter
pnpm lint

# Run tests
pnpm test

# Type check
pnpm type-check

# Build check
pnpm build:all
```

## Critical Blockers

These MUST be fixed before merge:

```
🚨 SECURITY:
- Missing [tenant/organization] filter in queries (if multi-tenant)
- Missing [isDeleted/deletedAt] filter in queries (if using soft delete)
- Using `any` types
- Exposing sensitive data in errors

🚨 FUNCTIONALITY:
- Tests failing
- Build failing
- Linter errors
- TypeScript errors

🚨 DATA INTEGRITY:
- Cross-tenant data leaks (if multi-tenant)
- Hard deletes (if soft delete pattern expected)
- Missing validation
```

## Approval Criteria

### ❌ Block Merge

- Security issues present
- No [tenant/organization] filtering (if multi-tenant required)
- No soft delete filtering (if soft delete pattern required)
- `any` types used
- Tests failing
- Build failing

### ⚠️ Request Changes

- Coverage < 70%
- Missing documentation
- Performance concerns
- Accessibility issues
- Pattern violations

### ✅ Approve

- All security checks pass
- Tests passing with good coverage
- Documentation updated
- Follows patterns
- Performance acceptable

## AI-Assisted Review

Use this prompt template:

```
Review this code against project standards:

CONTEXT:
- Current branch: [branch]
- Files changed: [list]
- Purpose: [description]

CRITICAL CHECKS:
1. [Tenant/organization] filtering in ALL queries (if multi-tenant)
2. [isDeleted/deletedAt] filtering in ALL queries (if soft delete)
3. No `any` types
4. [AuthGuard/Middleware] on protected routes
5. Error handling present
6. Tests exist and pass

PATTERN COMPLIANCE:
7. Check .agents/memory/ and codebase examples for patterns
8. Verify [service pattern] usage
9. Check [type organization] location
10. Verify [validation approach]

SECURITY:
11. No cross-tenant data leaks (if multi-tenant)
12. Input validation present
13. Auth checks before operations
14. No sensitive data in responses

PROVIDE:
- ✅ What's good
- ❌ Critical issues (block merge)
- ⚠️ Improvements needed
- 📝 Suggestions
- 🎯 Overall recommendation: Approve / Request Changes / Block
```

## Quick Decision Tree

```
Are queries filtering by [tenant/organization]? (if multi-tenant)
  NO → ❌ BLOCK MERGE (if required)
  YES → Continue

Are queries filtering [isDeleted/deletedAt]? (if soft delete)
  NO → ❌ BLOCK MERGE (if required)
  YES → Continue

Any `any` types?
  YES → ❌ BLOCK MERGE
  NO → Continue

Tests passing?
  NO → ❌ BLOCK MERGE
  YES → Continue

Build successful?
  NO → ❌ BLOCK MERGE
  YES → Continue

Coverage > 70%?
  NO → ⚠️ REQUEST MORE TESTS
  YES → Continue

Documentation updated?
  NO → ⚠️ REQUEST UPDATE
  YES → ✅ APPROVE
```

## Post-Review Checklist

After approval:

```
- [ ] PR approved in GitHub
- [ ] CI/CD checks passed
- [ ] Merge conflicts resolved
- [ ] Session file updated
- [ ] TODO.md files updated
```

---

**Created:** 2025-11-21
**Category:** Development
**Inspired by:** claudecodecommands.directory/Code Review
**Note:** Adapt security checks (multi-tenancy, soft delete) to your project's requirements
