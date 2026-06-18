# Task Management - AI Agent Command

**MANDATORY: When user requests a new feature/task, CREATE A GITHUB ISSUE + plan FIRST before implementing anything.**

## Purpose

Unified command for **creating** and **updating** tasks - from simple one-shots to complex features. Ensures proper planning, documentation, and status tracking via GitHub Issues.

## Operations

### 1. Create New Task

Create a GitHub Issue with full planning before implementation.

### 2. Update Task Status

Update an existing GitHub Issue (close, label, comment with status).

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

1. Read relevant architecture docs from `.agents/memory/`:

   ```bash
   ls .agents/memory/
   # Read the files most relevant to this feature area
   ```

2. Search for similar implementations in the codebase

3. Check open issues for related work:

   ```bash
   gh issue list --state open
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

1. Document which libraries will be used in the issue body

### Step 5: Create GitHub Issue

**AI Actions:**

#### 5.1 Choose Issue Type

**User Story** - Feature from user perspective
**Technical Task** - Implementation-focused
**Bug Fix** - Fix existing issue
**Enhancement** - Improve existing feature
**Migration** - Move/refactor existing code
**Research** - Investigation/audit task

#### 5.2 Create the Issue

```bash
gh issue create \
  --title "[App]: [Feature Name]" \
  --body "$(cat <<'EOF'
## Overview
[Brief description of what needs to be built and why]

## User Story (if applicable)
As a [user], I want [goal] so that [benefit].

## Requirements
1. Requirement one
2. Requirement two

## Technical Approach
[Architecture approach, patterns to follow]

## Files to Create/Modify
- `path/to/file.ts` — description
- `path/to/component.tsx` — description

## Libraries
- **[Library]** (Context7 ID: `/org/project`) — specific feature needed

## Acceptance Criteria
- [ ] Criterion one
- [ ] Criterion two

## Priority
High | Medium | Low
EOF
)" \
  --label "[type]"
```

#### 5.3 Note the Issue Number

After creation, note the issue number (e.g., `#42`) for reference in session notes.

### Step 6: Present to User & Get Approval

**AI Actions:**

1. Present to user:

   - Show the GitHub Issue link
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

1. Follow existing codebase patterns (find 3+ examples first)
2. Implement in this order:

   - Database/schema changes (if needed)
   - Backend (API, services)
   - Frontend (components, services)
   - Tests
   - Documentation

3. After each major piece:
   - Run linter
   - Check for errors
   - Verify tenant/organization filtering (if multi-tenant)
   - Verify soft delete handling (if using soft delete)

### Step 9: Testing

**AI Actions:**

1. Write unit tests
2. Test manually:

   - Happy path
   - Error cases
   - Edge cases
   - Tenant isolation (if multi-tenant)

3. Run test suite:

   ```bash
   bun run test
   ```

### Step 10: Documentation & Cleanup

**AI Actions:**

1. Update `.agents/memory/` files if architectural changes were made
2. Add session entry to `.agents/sessions/YYYY-MM-DD.md`
3. Close or update the GitHub Issue:

   ```bash
   gh issue close <number> --comment "Implemented in commit <sha>. <brief summary>"
   ```

## Issue Body Template

```markdown
## Overview

[High-level description of what needs to be built and why]

## User Story (if applicable)

**As a** [type of user]
**I want** [goal/desire]
**So that** [benefit/value]

## Requirements

1. **Requirement 1** — detail
2. **Requirement 2** — detail

## Technical Approach

[Architecture approach, patterns to follow, key decisions]

## Files to Create

- `path/to/new/file.ts` — description and purpose
- `path/to/component.tsx` — description and purpose

## Files to Modify

- `path/to/existing/file.ts` — what changes are needed

## API Endpoints (if applicable)

- `POST /api/[resource]` — description
- `GET /api/[resource]/:id` — description

## Libraries/Dependencies

- **[Library Name]** (Context7 ID: `/org/project`) — specific feature/API needed

## Acceptance Criteria

- [ ] Criterion one
- [ ] Criterion two
- [ ] Tests pass
- [ ] No regression

## Priority

High | Medium | Low

## Notes

[Any additional gotchas or things to watch out for]
```

## Naming Conventions

**Issue titles:** `[App]: Feature Name` or `[Type]: Brief Description`

**Good titles:**

- `Studio: Batch Content Generation`
- `API: Replicate JSON Prompt Improvements`
- `Bug: Video preview shows black screen`
- `Infra: Accounts to Brands Migration`

**Bad titles:**

- `feature` (too generic)
- `fix bug` (not specific enough)
- `Video Gen` (don't abbreviate)

## Example Interaction

**User:** "I want to add video generation with captions to Studio"

**AI Response:**

```
A few quick questions:

1. Priority: Is this critical for this week, or can it wait?
2. Should captions be embedded in video or overlaid?
3. Any specific caption styling requirements?

[After getting answers]

[AI checks .agents/memory/, fetches Context7 docs for ffmpeg, Next.js, etc.]

I've created the issue:
🔗 GitHub Issue #47: Studio: Video Generation with Captions

This covers:
- Integration with caption API
- Caption positioning options
- Styling controls
- Preview with captions
- Multi-language support

Review the issue and let me know if you'd like to proceed with implementation or make changes!
```

## Critical Rules

**BEFORE implementing ANY new feature:**

1. ✅ Create GitHub Issue
2. ✅ Document approach and acceptance criteria
3. ✅ Present to user for review
4. ✅ Get approval
5. ✅ Then implement

**This ensures:**

- No surprise implementations
- User knows what's being built
- Clear scope and acceptance criteria
- Better planning and estimation

## Red Flags (Stop and Ask User)

- Feature requires breaking changes
- Affects multiple projects
- Security implications
- Performance concerns
- Requires external services
- Unclear requirements

## Integration with Other Commands

**At end of session:**

- Session file references the GitHub Issue number
- Issue closed with implementation summary if complete
- If blocked, note in issue comments

## Quick Reference

| Step       | Action         | Tool             |
| ---------- | -------------- | ---------------- |
| Understand | Detect scope   | —                |
| Clarify    | Ask questions  | —                |
| Research   | Check system   | gh issue list, codebase search |
| Fetch Docs | Get latest     | Context7 MCP     |
| Plan       | Create issue   | gh issue create  |
| Approve    | Get permission | Present to user  |
| Code       | Implement      | follow codebase patterns |
| Test       | Verify         | bun run test     |
| Document   | Update docs    | session + memory |

---

# PART 2: Update Task Status Workflow

## When to Use Update

User says:

- "Mark [task] as complete"
- "Update status of [issue #N] to in progress"
- "Change priority of [issue] to high"
- "Set [issue] status to blocked"

## Update Workflow Steps

### Step 1: Identify Issue

**Ask user if not clear:**

- Which issue? (number or title)
- What needs to update? (status, priority, comment)
- What's the new value?

### Step 2: View Current Issue

```bash
gh issue view <number>
```

Verify:

- Issue exists
- Current status/labels
- Issue details

### Step 3: Update

**Close when complete:**

```bash
gh issue close <number> --comment "Done. Implemented in <sha>. <summary>"
```

**Add status comment:**

```bash
gh issue comment <number> --body "Status update: [details]"
```

**Update labels:**

```bash
gh issue edit <number> --add-label "blocked"
gh issue edit <number> --remove-label "in-progress" --add-label "done"
```

### Step 4: Confirm with User

```
✅ Issue #N updated!

- Status: [old] → [new]
- Comment added: [summary]
```

## Status Reference

| Status    | GitHub Action              | When to Use                 |
| --------- | -------------------------- | --------------------------- |
| Backlog   | Open, no label             | Not yet started             |
| In Progress | Label: `in-progress`     | Actively working on it      |
| Blocked   | Label: `blocked` + comment | Waiting on dependency       |
| Done      | Closed with summary        | Finished and verified       |
| Cancelled | Closed with reason         | No longer needed            |

## Update Examples

### Example 1: Mark as Complete

**User:** "Mark the video generation issue as complete"

**AI:**

1. Searches open issues: `gh issue list --search "video generation"`
2. Views the issue: `gh issue view <number>`
3. Closes it: `gh issue close <number> --comment "Implemented. See commit <sha>."`
4. Confirms with user

### Example 2: Mark as Blocked

**User:** "Set queue migration issue as blocked"

**AI:**

1. Finds the issue
2. Asks: "What's blocking it?"
3. Adds label: `gh issue edit <number> --add-label "blocked"`
4. Comments: `gh issue comment <number> --body "Blocked: [reason]"`
5. Confirms

## Integration with Other Commands

**After updating issue:**

- If "Done" → Add to session notes
- If "Blocked" → Note in current session
- If priority changed → May affect roadmap planning

---

**Created:** 2025-10-19
**Updated:** 2026-06-02 — migrated from local task files to GitHub Issues
**Purpose:** Unified command for task creation and updates - simple to complex
