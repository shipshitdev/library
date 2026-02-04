# Task Management - AI Agent Command

**MANDATORY: When user requests a new feature/task, CREATE TASK + PRD FILES FIRST before implementing anything.**

## Purpose

Unified command for **creating** and **updating** tasks - from simple one-shots to complex features. Ensures proper planning, documentation, and status tracking.

## Operations

### 1. Create New Task

Create task + PRD files with full planning before implementation.

### 2. Update Task Status

Quickly update existing task status, priority, or metadata.

## When to Use

**Create a task when user:**

- Requests a new feature
- Describes a user story
- Asks for an enhancement
- Reports a bug that needs tracking
- Mentions a future improvement
- Asks for a technical task

**Update a task when user:**

- Says "mark task X as complete"
- Wants to change task status
- Asks to update priority
- Needs to modify task metadata

**Examples:**

- CREATE: "I want to add multi-platform analytics"
- CREATE: "Can you implement a thread composer for Twitter?"
- UPDATE: "Mark the video generation task as complete"
- UPDATE: "Change priority of analytics task to high"

---

# PART 1: Create New Task Workflow

### Step 1: Understand Request (Detect Complexity)

**AI Actions:**

1. Analyze the request to determine complexity:

   - **Simple task:** One-shot, straightforward implementation (< 1 hour, few files)
   - **Complex feature:** Multi-step, requires planning (> 1 hour, multiple files/systems)

2. Ask clarifying questions:
   - What problem does this solve?
   - Who are the users?
   - What's the expected behavior?
   - Any constraints or requirements?

### Step 2: Gather Requirements

**AI Actions:**

Ask these questions if not clear from request:

- Which app is this for? (admin, manager, studio, analytics, publisher, dashboard, automation, stock, business, or cross-app)
- What's the priority? (CRITICAL, High, Medium, Low, Future)
- What's the main goal/outcome?
- Are there dependencies on other tasks?
- Any specific technical requirements?

### Step 3: Check Existing System

**AI Actions:**

1. Read relevant architecture docs:

   ```bash
   # For API features
   cat [api-project]/.agents/SYSTEM/ARCHITECTURE.md
   cat [api-project]/.agents/SYSTEM/RULES.md

   # For Frontend features
   cat [frontend-project]/.agents/SYSTEM/ARCHITECTURE.md
   cat [frontend-project]/.agents/SYSTEM/RULES.md
   ```

2. Search for similar implementations:

   ```bash
   # Find similar features/patterns
   grep -r "similar_pattern" [project]/
   ```

3. Check examples:

   ```bash
   cat .agents/EXAMPLES/[category]/[example-name].md
   ```

### Step 4: Fetch Latest Library Docs (MANDATORY)

**AI Actions:**

1. Use Context7 for all relevant libraries:

```typescript
// Example for Next.js feature
await mcp_context7_resolve_library_id("nextjs");
await mcp_context7_get_library_docs(
  "/vercel/next.js",
  "app router server actions"
);

// Example for NestJS feature
await mcp_context7_resolve_library_id("nestjs");
await mcp_context7_get_library_docs(
  "/nestjs/docs.nestjs.com",
  "guards decorators"
);
```

1. Document which libraries will be used in PRD

### Step 5: Create Files (Task + PRD)

**AI Actions:**

#### 5.1 Determine File Locations

**CRITICAL:** Follow your project's task structure (adapt to your conventions)

**Task file locations:**

- **Frontend tasks:**

  - Task: `[frontend-project]/.agents/TASKS/[task-name].md`
  - PRD: `[frontend-project]/.agents/PRDS/[subfolder]/[task-name].md`

- **Backend tasks:**

  - Task: `[backend-project]/.agents/TASKS/[task-name].md`
  - PRD: `[backend-project]/.agents/PRDS/[task-name].md`

- **Other projects:** Adapt project paths to your structure

- **Cross-project tasks:**
  - Task: `.agents/TASKS/[task-name].md` (workspace root)
  - PRD: `.agents/PRDS/[task-name].md`

#### 5.2 Choose Template Type

**User Story** - Feature from user perspective
**Technical Task** - Implementation-focused
**Bug Fix** - Fix existing issue
**Enhancement** - Improve existing feature
**Migration** - Move/refactor existing code
**Research** - Investigation/audit task

#### 5.3 Create Task File

Use appropriate template (see Templates section below).

#### 5.4 Create PRD File

Create companion PRD with implementation details (see PRD Template section below).

### Step 6: Present to User & Get Approval

**AI Actions:**

1. Present to user:

   - Show both file locations (task + PRD)
   - Summary of the task breakdown
   - Explain approach and scope
   - List what will be created/modified
   - Mention any risks or concerns

2. Ask if they want to proceed with implementation or adjust the task

3. **WAIT for user approval before coding**

### Step 7: Implementation Plan

**AI Actions (after approval):**

1. Break down into sub-tasks:

   - Backend changes
   - Frontend changes
   - Database changes
   - Tests
   - Documentation

2. Identify dependencies and order

3. Estimate complexity:
   - Simple (< 1 hour)
   - Medium (1-4 hours)
   - Complex (> 4 hours)

### Step 8: Implementation

**AI Actions:**

1. Follow examples from `.agents/EXAMPLES/`
2. Implement in this order:

   - Database/schema changes (if needed)
   - Backend (API, services)
   - Frontend (components, services)
   - Tests
   - Documentation

3. After each major piece:
   - Run linter
   - Check for errors
   - Verify [tenant/organization] filtering (if multi-tenant)
   - Verify soft delete handling (if using soft delete)

### Step 9: Testing

**AI Actions:**

1. Write unit tests:

   ```typescript
   // See .agents/EXAMPLES/TESTING/
   ```

2. Test manually:

   - Happy path
   - Error cases
   - Edge cases
   - [Tenant/organization] isolation (if multi-tenant)

3. Run test suite:

   ```bash
   npm test
   ```

### Step 10: Documentation & Cleanup

**AI Actions:**

1. Update docs:

   ```bash
   # Update relevant files
   [project]/.agents/SYSTEM/ARCHITECTURE.md  # If architectural change
   [project]/.agents/SYSTEM/SUMMARY.md       # Current state
   ```

2. Add session entry:

   ```bash
   [project]/.agents/SESSIONS/YYYY-MM-DD.md
   ```

3. Update task file and PRD:
   - Mark status as complete
   - Update timestamps
   - Note any deviations from plan

## Templates

### Task Template: Structured Format

**CRITICAL:** All tasks MUST follow this exact structured format for Kaiban Markdown extension compatibility.

```markdown
## Task: [Feature Name]

**ID:** feature-name-slug
**Label:** [App]: [Feature Name]
**Description:** [Brief description of what this task accomplishes]
**Type:** Feature
**Status:** Backlog
**Priority:** High
**Created:** YYYY-MM-DD
**Updated:** YYYY-MM-DD
**PRD:** [Link](../PRDS/[path]/feature-name.md)

---
```

**Metadata Fields:**

- `ID`: kebab-case-slug (filename without .md)
- `Label`: Human-readable title with app prefix
- `Description`: Brief description of what this task accomplishes
- `Type`: Feature | Bug | Enhancement | Task | Migration | Audit | Planning
- `Status`: Backlog | To Do | Testing | Done
- `Priority`: High | Medium | Low
- `Created`: YYYY-MM-DD (when task was first created)
- `Updated`: YYYY-MM-DD (when task was last modified)
- `PRD`: Link to PRD file (relative path)

**Status Rules:**

- Not started: `Status: Backlog`
- In progress: `Status: To Do`
- Testing: `Status: Testing`
- Complete: `Status: Done`

**Examples:**

```markdown
## Task: Studio: Batch Content Generation

**ID:** studio-batch-content-generation
**Label:** Studio: Batch Content Generation
**Description:** Enable batch generation of multiple content pieces from a single prompt
**Type:** Feature
**Status:** Backlog
**Priority:** High
**Created:** 2025-10-07
**Updated:** 2025-10-19
**PRD:** [Link](../PRDS/studio/studio-batch-content-generation.md)

---
```

```markdown
## Task: API: Replicate JSON Prompt Improvements

**ID:** api-replicate-json-prompt-improvements
**Label:** API: Replicate JSON Prompt Improvements
**Description:** Improve JSON prompt structure for better model performance
**Type:** Enhancement
**Status:** Backlog
**Priority:** Medium
**Created:** 2025-10-16
**Updated:** 2025-10-19
**PRD:** [Link](../PRDS/api-replicate-json-prompt-improvements.md)

---
```

```markdown
## Task: Accounts to Brands Migration

**ID:** accounts-to-brands-migration
**Label:** Accounts to Brands Migration
**Description:** Rename all account references to brands across the codebase
**Type:** Migration
**Status:** Done
**Priority:** High
**Created:** 2025-10-15
**Updated:** 2025-10-19
**PRD:** [Link](PRDS/accounts-to-brands-migration.md)

---
```

**NOTE:** Task file contains structured metadata + PRD link. All implementation details go in the PRD file.

## PRD Template

**File naming:** Same as task file: `[task-name].md`

**Location:** `<project>/.agents/PRDS/[subdirs]/[task-name].md` (SEPARATE from task file)

**CRITICAL:** PRDs MUST NOT contain checkboxes (`- [ ]` or `- [x]`). Use plain bullets `-` instead.

````markdown
# [App]: [Feature Name]

**Priority:** High | Medium | Low  
**Status:** Not Started | In Progress | Done  
**Type:** Feature | Bug | Enhancement | Task | Migration | Audit  
**Created:** YYYY-MM-DD  
**Last Updated:** YYYY-MM-DD

## Overview

[High-level description of what needs to be built and why]

## User Story (if applicable)

**As a** [type of user]  
**I want** [goal/desire]  
**So that** [benefit/value]

## Description

[Detailed description of the feature/task]

## Context

[Why is this needed? What problem does it solve? Background information]

## Implementation Overview

[Technical approach, patterns to follow, architectural decisions]

## Features / Requirements

1. **Feature 1**

   - Detail about feature 1
   - Specific behaviors and requirements

2. **Feature 2**
   - Detail about feature 2
   - Specific behaviors and requirements

## Files to Create

- `path/to/new/file.ts` - [description and purpose]
- `path/to/component.tsx` - [description and purpose]
- `path/to/service.ts` - [description and purpose]

## Files to Modify

- `path/to/existing/file.ts` - [what changes are needed]
- `path/to/another.tsx` - [what changes are needed]

## API Endpoints (if applicable)

**New endpoints to create:**

- `POST /api/[resource]` - [description]
- `GET /api/[resource]/:id` - [description]
- `PATCH /api/[resource]/:id` - [description]
- `DELETE /api/[resource]/:id` - [description]

**Existing endpoints to modify:**

- `PATCH /api/[resource]/:id` - [changes needed]

## Database Changes (if applicable)

```javascript
// Schema changes
{
  fieldName: Type,
  newField: Type,
}

// Indexes to add
db.collection.createIndex({ field: 1 });
```

## Libraries/Dependencies

**CRITICAL:** Use Context7 MCP to fetch latest docs before implementing.

**Libraries to use:**

- **[Library Name]** (Context7 ID: `/org/project`) - [specific feature/API needed]
- **[Framework]** (Context7 ID: `/org/project`) - [specific feature needed]

**Example:**

- **MongoDB** (Context7 ID: `/mongodb/docs`) - Aggregation pipeline for analytics
- **Next.js** (Context7 ID: `/vercel/next.js`) - Server Actions for form handling

**Fetch docs:**

```typescript
mcp_context7_get_library_docs({
  context7CompatibleLibraryID: "/mongodb/docs",
  topic: "aggregation pipeline",
});
```

## Technical Implementation

### Architecture Approach

[Describe the technical approach, patterns to follow, architectural decisions]

### Database Changes (if applicable)

```javascript
// Schema changes
{
  fieldName: Type,
  newField: Type,
  // ...
}

// Indexes to add
db.collection.createIndex({ field: 1 });
```

### Technical Considerations

- [Performance concern]
- [Security consideration]
- [Scalability issue]
- [Browser compatibility]
- [Tenant/organization filtering - if multi-tenant]
- [Soft delete handling - if using soft delete]

### Design/UX Considerations

- [User flow]
- [Wireframe/mockup reference]
- [Accessibility requirements]
- [Responsive design notes]

## Testing Requirements

### Unit Tests

- [ ] Test for [component/service] - [specific scenario]
- [ ] Test for [function] - [edge case]

### Integration Tests

- [ ] Test for [workflow] - [happy path]
- [ ] Test for [workflow] - [error cases]

### E2E Tests

- [ ] Test user flow: [describe flow]
- [ ] Test edge case: [describe scenario]

### Manual Testing Checklist

- [ ] Happy path works
- [ ] Error handling works
- [ ] Edge cases handled
- [ ] [Tenant/organization] isolation verified (if multi-tenant)
- [ ] Soft delete respected (if using soft delete)
- [ ] Performance acceptable

---

**Implementation Notes:**

[Any additional notes, gotchas, or things to watch out for during implementation]

```

## Naming Conventions

**File naming:** `kebab-case-task-name.md`

**Good names:**

- `video-generation-with-captions.md`
- `quick-actions-audit.md`
- `multi-platform-integration.md`
- `organization-review.md`

**Bad names:**

- `feature.md` (too generic)
- `VideoGeneration.md` (wrong case)
- `video_generation.md` (use kebab, not snake)
- `video-gen.md` (don't abbreviate)

## Example Interaction

**User:** "I want to add video generation with captions to Studio"

**AI Response:**

```

Great! Let me create a proper task and PRD for this.

A few quick questions:

1. Priority: Is this critical for this week, or can it wait?
2. Should captions be embedded in video or overlaid?
3. Any specific caption styling requirements?

[After getting answers]

[AI checks architecture, fetches Context7 docs for ffmpeg, Next.js, etc.]

I've created the task files:
📄 [project]/.agents/TASKS/video-generation-with-captions.md
📄 [project]/.agents/PRDS/video-generation-with-captions.md

This task includes:

- Integration with caption API
- Caption positioning options
- Styling controls
- Preview with captions
- Multi-language support

The PRD includes detailed implementation steps, files to create/modify, and testing requirements.

Review the files and let me know if you'd like to proceed with implementation or make changes!
````

## Critical Rules

**BEFORE implementing ANY new feature:**

1. ✅ Create task file
2. ✅ Create PRD file
3. ✅ Link them together
4. ✅ Present to user for review
5. ✅ Get approval
6. ✅ Then implement

**This ensures:**

- No surprise implementations
- User knows what's being built
- Clear scope and acceptance criteria
- Better planning and estimation
- Documentation exists from start
- Separation of what (task) and how (PRD)

## Red Flags (Stop and Ask User)

- Feature requires breaking changes
- Affects multiple projects
- Security implications
- Performance concerns
- Requires external services
- Unclear requirements

## Integration with Other Commands

**At end of session:**

- Task file status updated (Not Started → In Progress → Complete)
- PRD status updated
- Session file references both task and PRD
- If complete, mark in SUMMARY.md
- If blocked, note in task file

**Use documentation update checklist** to ensure all documentation is updated.

## Quick Reference

| Step       | Action         | Tool             |
| ---------- | -------------- | ---------------- |
| Understand | Detect scope   | -                |
| Clarify    | Ask questions  | -                |
| Research   | Check system   | grep, cat        |
| Fetch Docs | Get latest     | Context7 MCP     |
| Plan       | Create files   | task + PRD       |
| Approve    | Get permission | Present to user  |
| Code       | Implement      | .agents/EXAMPLES/ |
| Test       | Verify         | npm test         |
| Document   | Update docs    | upt-doc.md       |

---

# PART 2: Update Task Status Workflow

## When to Use Update

User says:

- "Mark [task] as complete"
- "Update status of [task] to in progress"
- "Change priority of [task] to high"
- "Set [task] status to blocked"

## Update Workflow Steps

### Step 1: Identify Task

**Ask user if not clear:**

- Which task file? (full path or task name)
- What field to update? (status, priority, description)
- What's the new value?

### Step 2: Read Task File

```bash
cat [project]/.agents/TASKS/task-name.md
```

Verify:

- Task exists
- Current status/priority
- Task format (Kanban structured)

### Step 3: Update Task Fields

**Status changes:**

- Backlog → To Do → Testing → Done
- Also: Blocked, Cancelled

**Priority changes:**

- High, Medium, Low

**Update these fields:**

- `**Status:**` → new status
- `**Updated:**` → current date (YYYY-MM-DD)
- `**Priority:**` (if changing)

### Step 4: Update PRD (if status changed to Done)

If marking as complete:

1. Read PRD file (linked in task)
2. Update PRD status to "Done"
3. Update "Last Updated" date

### Step 5: Confirm with User

```
✅ Task updated!

Task: [project]/.agents/TASKS/task-name.md
- Status: [old] → [new]
- Updated: [date]

PRD: [project]/.agents/PRDS/[path]/task-name.md
- Status: [old] → [new]
```

## Status Reference

| Status    | Meaning     | When to Use                 |
| --------- | ----------- | --------------------------- |
| Backlog   | Not started | Initial state, in backlog   |
| To Do     | In progress | Actively working on it      |
| Testing   | Testing     | Code complete, being tested |
| Done      | Complete    | Finished and verified       |
| Blocked   | Waiting     | Blocked on dependencies     |
| Cancelled | Won't do    | No longer needed            |

## Update Examples

### Example 1: Mark as Complete

**User:** "Mark the video generation task as complete"

**AI:**

1. Searches for task file with "video generation" in name
2. Reads task file
3. Updates status to "Done"
4. Updates timestamp
5. Updates linked PRD status
6. Confirms with user

### Example 2: Change Priority

**User:** "Change priority of analytics task to high"

**AI:**

1. Finds analytics task file
2. Updates `**Priority:**` field
3. Updates `**Updated:**` timestamp
4. Confirms with user

### Example 3: Mark as Blocked

**User:** "Set queue migration task as blocked"

**AI:**

1. Finds queue migration task
2. Asks: "What's blocking it?"
3. Updates status to "Blocked"
4. Optionally adds blocker note
5. Updates timestamp
6. Confirms

## Quick Update Commands

For common patterns, detect and execute directly:

**Pattern:** "mark [task-name] as [status]"
**Action:** Find task → Update status → Confirm

**Pattern:** "set [task-name] priority to [priority]"
**Action:** Find task → Update priority → Confirm

**Pattern:** "[task-name] is complete"
**Action:** Find task → Set status to Done → Update PRD → Confirm

## Integration with Other Commands

**After updating task status:**

- If "Done" → Consider adding to session notes (`/docs-update`)
- If "Blocked" → Note in current session
- If priority changed → May affect roadmap

**Clean up completed/cancelled tasks periodically** (if using task tracking).

---

**Created:** 2025-10-19
**Updated:** 2025-11-21
**Purpose:** Unified command for task creation and updates - simple to complex

```

```

```

```
