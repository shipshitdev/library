# Analyze Codebase

**Purpose:** Generate comprehensive analysis of the codebase structure, architecture, and organization.

## When to Use

- Onboarding new developers
- Architecture documentation
- Project health assessment
- Before major refactoring
- Understanding system complexity

## What This Command Does

Systematically analyzes the project to produce:

1. **Project Overview** - Tech stack, purpose, structure
2. **Directory Structure** - Organization and module layout
3. **Architecture Patterns** - Design patterns and conventions
4. **Dependencies** - External services and libraries
5. **Code Quality** - Patterns, anti-patterns, tech debt
6. **Security Analysis** - Multi-tenancy, auth, data isolation
7. **Performance Insights** - Bottlenecks and optimizations

## Analysis Process

### Step 1: Discovery Phase

**Project Structure:**

```bash
# Get high-level directory tree (exclude noise)
tree -L 3 -I 'node_modules|.next|dist|build|coverage'

# Count files by type
find . -type f -name "*.ts" | wc -l
find . -type f -name "*.tsx" | wc -l
find . -type f -name "*.md" | wc -l
```

**Project Configuration:**

```bash
# Package management
cat package.json | grep -A 20 '"dependencies"'
cat pnpm-workspace.yaml  # Monorepo structure

# Build tools
ls -la | grep -E "vite|webpack|next.config|nest-cli"

# Environment
cat .env.example | grep -v "^#"
```

### Step 2: Architecture Analysis

**Module Organization:**

```bash
# Find all modules/packages
find apps packages -maxdepth 2 -type d

# Identify main entry points
find . -name "main.ts" -o -name "index.ts" -o -name "_app.tsx"
```

**API Structure:**

```bash
# Controllers (endpoints)
find . -name "*.controller.ts" -type f

# Services (business logic)
find . -name "*.service.ts" -type f

# Models/Schemas
find . -name "*.schema.ts" -o -name "*.model.ts"
```

**Frontend Components:**

```bash
# Component organization
find apps -name "components" -type d
find packages -name "components" -type d

# Pages/Routes
find apps -name "pages" -o -name "app" -type d
```

### Step 3: Patterns & Standards

**Code Patterns:**

- Check `.agents/EXAMPLES/` for established patterns
- Review `.agents/SOP/` for documented procedures
- Analyze common service patterns (singletons, CRUD)

**Type System:**

```bash
# Shared types and interfaces
find packages -name "interfaces" -o -name "props" -o -name "types"

# DTOs (Data Transfer Objects)
find . -name "*.dto.ts"
```

**Security Patterns:**

```typescript
// Multi-tenancy enforcement (if applicable)
grep -r "[tenant-field]:" [backend-path] --include="*.ts" | head -5

// Soft delete pattern (if applicable)
grep -r "isDeleted:" [backend-path] --include="*.ts" | head -5

// Authentication guards
grep -r "[AuthGuard]" [backend-path] --include="*.ts" | head -5
```

### Step 4: Dependencies Analysis

**External Services:**

- **Authentication:** Clerk
- **Database:** MongoDB (via Mongoose)
- **Cache:** Redis
- **Queues:** BullMQ
- **AI:** OpenAI, Anthropic, Replicate
- **Storage:** AWS S3
- **Monitoring:** (check package.json)

**Frontend Dependencies:**

- **Framework:** Next.js (check which apps)
- **UI:** Tailwind CSS, custom components
- **State:** React Context/hooks
- **API Client:** Fetch/Axios (check patterns)

### Step 5: Generate Analysis Report

Create comprehensive report in: `.agents/SYSTEM/CODEBASE-ANALYSIS.md`

## Report Structure

```markdown
# Codebase Analysis

**Generated:** YYYY-MM-DD
**Analyst:** Claude Code

## Executive Summary

3-5 sentence overview of project health, complexity, and key insights.

## 1. Project Overview

**Name:** [Project Name]
**Type:** [Monorepo / Single Repo / etc.]
**Tech Stack:**

- Backend: [Framework, Database, etc.]
- Frontend: [Framework, UI Library, etc.]
- Services: [External services used]

**Purpose:** [Brief description]

**Architecture Style:** Microservices / Modular Monolith / etc.

## 2. Directory Structure
```

[project-name]/
├── apps/                    # Applications (if monorepo)
│ ├── api/                   # Backend API
│ ├── web/                   # Main web app
│ └── [other-apps]/          # Other applications
├── packages/                 # Shared packages (if monorepo)
│ ├── types/                 # Shared TypeScript types
│ ├── components/            # Shared UI components
│ └── utils/                 # Shared utilities
├── [docs-folder]/           # Documentation & context
└── [workspace-config]        # Monorepo config (if applicable)

```

## 3. Architecture Patterns

### Backend (NestJS)

**Module Structure:**
```

src/
├── auth/ # Authentication (Clerk)
├── users/ # User management
├── posts/ # Post CRUD + generation
├── brands/ # Brand management
└── common/ # Shared utilities

````

**Key Patterns:**
- **Base Classes:** [Base classes used for DRY]
- **Guards:** [Authentication guards used]
- **Decorators:** [Custom decorators for dependency injection]
- **DTOs:** [Validation approach]
- **Multi-tenancy:** [If applicable: organization/tenant filtering]
- **Soft Delete:** [If applicable: soft delete pattern]

**Example Pattern:**
```typescript
// Standard service method (example - adapt to your patterns)
async findByTenant(tenantId: string) {
  return this.model.find({
    tenantId,              // Multi-tenancy (if applicable)
    isDeleted: false       // Soft delete (if applicable)
  });
}
````

### Frontend ([Framework])

**Structure:**

```
apps/[app-name]/
├── app/                         # App directory (if Next.js)
├── components/                 # Feature components
├── services/                    # API clients
└── contexts/                    # Global state (if React)
```

**Key Patterns:**

- **Service Pattern:** [Singleton pattern or other approach]
- **Component Organization:** [By feature/domain/etc.]
- **Type Organization:** [How types/interfaces are organized]
- **Styling:** [CSS approach: Tailwind, CSS Modules, etc.]

## 4. Security Analysis

### Multi-Tenancy (if applicable)

**Implementation:**

- [Tenant/organization field] required on all resources
- All queries filter by [tenant field]
- No cross-tenant data leaks possible
- Enforced at service layer

**Example:**

```typescript
// ✅ Correct - Multi-tenant query (if applicable)
await this.model.find({
  tenantId: user.tenantId,
  isDeleted: false,
});

// ❌ Wrong - No tenant filter (if multi-tenant)
await this.model.find({ isDeleted: false });
```

### Authentication

**Provider:** [Auth provider: JWT, OAuth, etc.]

**Implementation:**

- [Auth guard/middleware] on all protected routes
- [Token validation approach]
- User context via [decorator/middleware pattern]

### Data Isolation ✅

**Soft Delete:**

- `isDeleted: boolean` field (NOT deletedAt)
- All queries filter `isDeleted: false`
- No hard deletes in production

**Validation:**

- DTOs with class-validator decorators
- Input sanitization
- ObjectId validation

## 5. Performance Insights

### Database

**Indexes:**

- Check MongoDB indexes for common queries
- Compound indexes for org + other fields

**Query Optimization:**

- Projections used for large documents
- Pagination implemented
- No N+1 query patterns

### Caching

**Redis Usage:**

- Session storage
- Rate limiting
- Cache invalidation strategies

### Background Jobs

**BullMQ Queues:**

- Post generation (AI)
- Email notifications
- Webhook processing
- Long-running operations

## 6. Code Quality

### Strengths

- ✅ Consistent patterns (Base classes)
- ✅ Type safety (TypeScript throughout)
- ✅ Documentation (`.agents/` folder)
- ✅ Multi-tenancy enforced
- ✅ Error handling with NestJS exceptions

### Areas for Improvement

- ⚠️ Test coverage (needs assessment)
- ⚠️ API documentation (Swagger completeness)
- ⚠️ Performance monitoring (APM needed?)

### Technical Debt

Document any identified technical debt:

- Legacy code to refactor
- Missing features
- Known bugs
- Performance bottlenecks

## 7. Dependencies

### Critical Dependencies

**Backend:**

- [Framework] - [Purpose]
- [ORM/Database client] - [Purpose]
- [Auth library] - [Purpose]
- [Queue library] - [Purpose]
- [Cache library] - [Purpose]

**Frontend:**

- [Framework] - [Purpose]
- [UI library] - [Purpose]
- [Auth library] - [Purpose]
- [Styling library] - [Purpose]

**External Services:**

- [Service 1] - [Purpose]
- [Service 2] - [Purpose]

### Version Matrix

| Package | Version | Status     | Notes         |
| ------- | ------- | ---------- | ------------- |
| NestJS  | 10.x    | ✅ Current | Latest stable |
| Next.js | 14.x    | ✅ Current | App router    |
| MongoDB | 7.x     | ✅ Current |               |

## 8. Testing Strategy

**Test Files:**

```bash
# Unit tests
find . -name "*.spec.ts" | wc -l

# E2E tests
find . -name "*.e2e-spec.ts" | wc -l
```

**Coverage:** [Run tests to get coverage %]

**Testing Patterns:**

- Unit tests: All services
- Integration tests: Controllers
- E2E tests: Critical user flows

## 9. Deployment & Infrastructure

**Hosting:**

- API: [Platform - AWS/Vercel/Railway/etc]
- Web: [Platform]
- Database: [MongoDB Atlas/etc]

**CI/CD:**

- GitHub Actions (check `.github/workflows/`)
- Automated testing
- Deployment triggers

**Monitoring:**

- Error tracking: [Sentry/etc]
- Performance: [New Relic/etc]
- Logs: [CloudWatch/etc]

## 10. Recommendations

### Immediate Actions

1. [Priority 1 item]
2. [Priority 2 item]

### Short-term Improvements

1. [Enhancement 1]
2. [Enhancement 2]

### Long-term Considerations

1. [Strategic item 1]
2. [Strategic item 2]

## Appendix

### Key Files

- **Architecture:** `.agents/SYSTEM/ARCHITECTURE.md`
- **SOPs:** `.agents/SOP/*.md` (if applicable)
- **Examples:** `.agents/EXAMPLES/` (if applicable)
- **Sessions:** `.agents/SESSIONS/` (if applicable)

### Metrics

- Total Files: [count]
- Total Lines of Code: [count]
- TypeScript Files: [count]
- Test Files: [count]
- Components: [count]
- API Endpoints: [count]

---

**Analysis Date:** YYYY-MM-DD
**Next Review:** [Recommended date]

````

## Output Location

**Primary:** `.agents/SYSTEM/CODEBASE-ANALYSIS.md`

**Updates:** Regenerate quarterly or after major changes

## Quick Analysis Mode

For faster analysis (skip detailed metrics):

```bash
# Just show structure
tree -L 3 -I 'node_modules|.next|dist'

# Count key files
echo "TypeScript: $(find . -name '*.ts' -o -name '*.tsx' | wc -l)"
echo "Controllers: $(find . -name '*.controller.ts' | wc -l)"
echo "Services: $(find . -name '*.service.ts' | wc -l)"
````

## Integration with Other Commands

Use with:

- `/start` - Initial context loading
- `/docs-update` - Keep analysis current
- `/refactor-code` - Inform refactoring decisions

---

**Created:** 2025-11-21
**Category:** Development
**Inspired by:** claudecodecommands.directory/Analyze Codebase
