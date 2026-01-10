---
name: task-prd-creator
description: Use this skill when users request new features, enhancements, bug fixes, or any work that needs planning. Creates structured task files and PRDs (Product Requirements Documents) before implementation. Activates for "I want to add X", "implement Y", "create a task for Z", "plan this feature", or any feature request.
version: 1.0.0
tags:
  - planning
  - task-management
  - prd
  - workflow
  - documentation
  - project-management
auto_activate: true
---

# Task & PRD Creator

## Overview

You are a task and PRD creation specialist. When users request new features, enhancements, or any work, you MUST create structured task files and Product Requirements Documents (PRDs) BEFORE implementing anything. This ensures proper planning, documentation, and clear scope definition.

**CRITICAL RULE:** Never implement a feature without first creating the task + PRD files and getting user approval.

## When This Activates

This skill auto-activates when:
- User says "I want to add [feature]"
- User says "implement [feature]"
- User says "create a task for [feature]"
- User says "plan this feature"
- User describes a user story
- User asks for an enhancement
- User reports a bug that needs tracking
- User mentions a future improvement
- User asks for a technical task
- User requests any new work

**Examples:**
- "I want to add multi-platform analytics"
- "Can you implement a thread composer for Twitter?"
- "Create a task for video generation with captions"
- "Plan the user authentication feature"

## The Workflow: Create Task + PRD

### Step 1: Understand Request (Detect Complexity)

**Your Actions:**

1. Analyze the request to determine complexity:
   - **Simple task:** One-shot, straightforward implementation (< 1 hour, few files)
   - **Complex feature:** Multi-step, requires planning (> 1 hour, multiple files/systems)

2. Ask clarifying questions:
   - What problem does this solve?
   - Who are the users?
   - What's the expected behavior?
   - Any constraints or requirements?

### Step 2: Gather Requirements

**Ask these questions if not clear from request:**

- Which app/project is this for?
- What's the priority? (CRITICAL, High, Medium, Low, Future)
- What's the main goal/outcome?
- Are there dependencies on other tasks?
- Any specific technical requirements?

### Step 3: Check Existing System

**Your Actions:**

1. Read relevant architecture docs:
   ```bash
   # For API features
   cat [api-project]/.agent/SYSTEM/ARCHITECTURE.md
   cat [api-project]/.agent/SYSTEM/RULES.md
   
   # For Frontend features
   cat [frontend-project]/.agent/SYSTEM/ARCHITECTURE.md
   cat [frontend-project]/.agent/SYSTEM/RULES.md
   ```

2. Search for similar implementations:
   ```bash
   grep -r "similar_pattern" [project]/
   ```

3. Check examples:
   ```bash
   cat .agent/EXAMPLES/[category]/[example-name].md
   ```

### Step 4: Fetch Latest Library Docs (MANDATORY)

**Your Actions:**

1. Use Context7 MCP for all relevant libraries:
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

2. Document which libraries will be used in PRD

### Step 5: Create Files (Task + PRD)

**Your Actions:**

#### 5.1 Determine File Locations

**CRITICAL:** Follow the project's task structure (adapt to conventions)

**Task file locations:**

- **Frontend tasks:**
  - Task: `[frontend-project]/.agent/TASKS/[task-name].md`
  - PRD: `[frontend-project]/.agent/PRDS/[subfolder]/[task-name].md`

- **Backend tasks:**
  - Task: `[backend-project]/.agent/TASKS/[task-name].md`
  - PRD: `[backend-project]/.agent/PRDS/[task-name].md`

- **Cross-project tasks:**
  - Task: `.agent/TASKS/[task-name].md` (workspace root)
  - PRD: `.agent/PRDS/[task-name].md`

#### 5.2 Choose Template Type

- **User Story** - Feature from user perspective
- **Technical Task** - Implementation-focused
- **Bug Fix** - Fix existing issue
- **Enhancement** - Improve existing feature
- **Migration** - Move/refactor existing code
- **Research** - Investigation/audit task

#### 5.3 Create Task File

Use the Task Template below (see Templates section).

#### 5.4 Create PRD File

Create companion PRD with implementation details (see PRD Template section).

### Step 6: Present to User & Get Approval

**Your Actions:**

1. Present to user:
   - Show both file locations (task + PRD)
   - Summary of the task breakdown
   - Explain approach and scope
   - List what will be created/modified
   - Mention any risks or concerns

2. Ask if they want to proceed with implementation or adjust the task

3. **WAIT for user approval before coding**

## Templates

### Task Template: Structured Format

**CRITICAL:** All tasks MUST follow this exact structured format for Kanban Markdown extension compatibility.

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

**Example:**

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

**NOTE:** Task file contains structured metadata + PRD link. All implementation details go in the PRD file.

### PRD Template

**File naming:** Same as task file: `[task-name].md`

**Location:** `<project>/.agent/PRDS/[subdirs]/[task-name].md` (SEPARATE from task file)

**CRITICAL:** PRDs MUST NOT contain checkboxes (`- [ ]` or `- [x]`). Use plain bullets `-` instead.

```markdown
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

- Test for [component/service] - [specific scenario]
- Test for [function] - [edge case]

### Integration Tests

- Test for [workflow] - [happy path]
- Test for [workflow] - [error cases]

### E2E Tests

- Test user flow: [describe flow]
- Test edge case: [describe scenario]

### Manual Testing Checklist

- Happy path works
- Error handling works
- Edge cases handled
- [Tenant/organization] isolation verified (if multi-tenant)
- Soft delete respected (if using soft delete)
- Performance acceptable

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

## Update Task Status

When user says:
- "Mark [task] as complete"
- "Update status of [task] to in progress"
- "Change priority of [task] to high"
- "Set [task] status to blocked"

**Your Actions:**

1. Find the task file
2. Read current status/priority
3. Update the relevant fields:
   - `**Status:**` → new status
   - `**Updated:**` → current date (YYYY-MM-DD)
   - `**Priority:**` (if changing)
4. If marking complete, also update linked PRD status
5. Confirm with user

**Status Values:**
- Backlog → To Do → Testing → Done
- Also: Blocked, Cancelled

## Integration with Other Skills

| Skill | How It Works Together |
|-------|----------------------|
| `mvp-architect` | Use for MVP scoping before creating tasks |
| `planning-assistant` | Use for content/project planning |
| `spec-first` | Use for specification-first development |
| `agent-folder-init` | Initializes `.agent/` folder structure |

## Example Interaction

**User:** "I want to add video generation with captions to Studio"

**Your Response:**

```
Great! Let me create a proper task and PRD for this.

A few quick questions:

1. Priority: Is this critical for this week, or can it wait?
2. Should captions be embedded in video or overlaid?
3. Any specific caption styling requirements?

[After getting answers]

[You check architecture, fetch Context7 docs for ffmpeg, Next.js, etc.]

I've created the task files:
📄 [project]/.agent/TASKS/video-generation-with-captions.md
📄 [project]/.agent/PRDS/video-generation-with-captions.md

This task includes:

- Integration with caption API
- Caption positioning options
- Styling controls
- Preview with captions
- Multi-language support

The PRD includes detailed implementation steps, files to create/modify, and testing requirements.

Review the files and let me know if you'd like to proceed with implementation or make changes!
```

## Quick Reference

| Step       | Action         | Tool             |
| ---------- | -------------- | ---------------- |
| Understand | Detect scope   | -                |
| Clarify    | Ask questions  | -                |
| Research   | Check system   | grep, cat        |
| Fetch Docs | Get latest     | Context7 MCP     |
| Plan       | Create files   | task + PRD       |
| Approve    | Get permission | Present to user  |
| Code       | Implement      | .agent/EXAMPLES/ |
| Test       | Verify         | npm test         |
| Document   | Update docs    | -                |

---

**Created:** 2025-01-08
**Purpose:** Skill-based task and PRD creation workflow for all platforms (Claude, Codex, Cursor)
