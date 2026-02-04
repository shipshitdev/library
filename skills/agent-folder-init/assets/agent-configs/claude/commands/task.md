# Task Management - Create and Update Tasks

Unified command for creating and updating tasks.

## When to Use

Create a task when user:

- Requests a new feature
- Describes a user story
- Asks for an enhancement
- Reports a bug that needs tracking
- Mentions a future improvement

Update a task when user:

- Says mark task X as complete
- Wants to change task status
- Asks to update priority

## Task Creation Workflow

### Step 1: Understand Request

Analyze the request to determine complexity:

- Simple task: One-shot, straightforward (< 1 hour)
- Complex feature: Multi-step, requires planning (> 1 hour)

### Step 2: Gather Requirements

Ask if not clear:

- What is the main goal/outcome?
- What is the priority? (High, Medium, Low)
- Any specific requirements?

### Step 3: Check Existing System

Read relevant documentation:

- Architecture docs
- Similar implementations
- Existing patterns

### Step 4: Create Task File

File location: <project>/.agents/TASKS/[task-name].md

Task Template:

## Task: [Feature Name]

**ID:** feature-name-slug
**Label:** [Feature Name]
**Description:** [Brief description]
**Type:** Feature
**Status:** Backlog
**Priority:** High
**Created:** YYYY-MM-DD
**Updated:** YYYY-MM-DD

---

### Overview

[High-level description]

### Requirements

1. [Requirement 1]
2. [Requirement 2]

### Implementation Notes

[Technical approach]

### Files to Modify

- path/to/file.ts - [what changes]

### Testing

- [ ] Test case 1
- [ ] Test case 2

### Step 5: Present to User

Show:

- Task file location
- Summary of the task
- Ask if they want to proceed

## Task Update Workflow

### Step 1: Identify Task

Find the task file to update.

### Step 2: Update Fields

Status changes:

- Backlog -> To Do -> Testing -> Done

Priority changes:

- High, Medium, Low

Update the Updated date.

### Step 3: Confirm

Show what was changed.

## Status Values

- Backlog: Not started
- To Do: In progress
- Testing: Being tested
- Done: Complete
- Blocked: Waiting on something

## Type Values

- Feature: New functionality
- Bug: Fix existing issue
- Enhancement: Improve existing
- Task: General work item
- Migration: Move/refactor code

## Naming Convention

Format: [short-descriptive-name].md

Good: video-generation-captions.md
Bad: feature.md, task1.md
