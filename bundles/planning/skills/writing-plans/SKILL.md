---
name: writing-plans
description: >-
  Turn a spec or requirements doc into a comprehensive, bite-sized implementation plan: map every file, define 2-5 minute TDD tasks with complete code, and enforce DRY/YAGNI/frequent-commits discipline. Use when you have requirements ready and need a concrete execution plan before touching code, when a feature spans multiple files and needs decomposition, or when you want agentic workers to execute tasks reliably without guessing.
metadata:
  version: "1.0.0"
  tags: "planning, implementation-plan, tasks, tdd, dry, yagni, decomposition"
  author: Ship Shit Dev
when_to_use: "write a plan, create implementation plan, plan this feature, break this into tasks, plan before coding, spec to tasks"
---

# Writing Plans

Write a comprehensive implementation plan assuming the implementer has zero context about the codebase and questionable test instincts. Document everything: which files to touch, complete code, exact commands, expected output, and how to verify. Deliver the whole plan as bite-sized checkboxed tasks. DRY. YAGNI. TDD. Frequent commits.

## Scope Check

If the spec covers multiple independent subsystems, consider breaking it into separate plans — one per subsystem. Each plan should produce working, testable software on its own. Deeply coupled work can share a plan; independently deployable subsystems should not.

## File Mapping (Before Any Tasks)

Before defining tasks, map out which files will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
- Prefer smaller, focused files over large files that do too much. The agent edits most reliably when it can hold the full file in context.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns. If the codebase uses large files, do not unilaterally restructure — but if a file you are modifying has grown unwieldy, including a split in the plan is reasonable.

This structure informs task decomposition. Each task should produce self-contained changes that make sense independently.

## Bite-Sized Task Granularity

Each step is one action, completable in 2-5 minutes:

- "Write the failing test" — one step
- "Run it to confirm it fails" — one step
- "Write the minimal implementation to make it pass" — one step
- "Run the tests and confirm they pass" — one step
- "Commit" — one step

Never combine steps. Never skip the failure confirmation.

## Plan Document Header

Every plan MUST start with this header:

```markdown
# [Feature Name] Implementation Plan

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries used]

---
```

## Task Structure Template

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.ts`
- Modify: `exact/path/to/existing.ts`
- Test: `tests/exact/path/to/file.test.ts`

- [ ] **Step 1: Write the failing test**

```typescript
it('describes specific behavior', () => {
  const result = functionUnderTest(input)
  expect(result).toBe(expectedValue)
})
```

- [ ] **Step 2: Run test to verify it fails**

```bash
bun run test tests/path/to/file.test.ts
```

Expected: FAIL — `functionUnderTest is not defined` (or similar)

- [ ] **Step 3: Write minimal implementation**

```typescript
export function functionUnderTest(input: InputType): OutputType {
  return expectedValue
}
```

- [ ] **Step 4: Run test to verify it passes**

```bash
bun run test tests/path/to/file.test.ts
```

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/to/file.test.ts src/path/to/file.ts
git commit -m "feat: add specific behavior"
```
````

## No Placeholders

Every step must contain the actual content the implementer needs. The following are **plan failures** — never write them:

- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" without the actual test code
- "Similar to Task N" — repeat the code; the implementer may read tasks out of order
- Steps that describe what to do without showing how (every code step requires a code block)
- References to types, functions, or methods not defined anywhere in the plan

## Iron Rules

- Exact file paths always — no "somewhere in src/"
- Complete code in every step — if a step changes code, show the full changed code
- Exact commands with expected output or expected failure message
- Every test written before the implementation it tests
- Every task ends with a commit
- DRY, YAGNI — no speculative abstractions, no future-proofing not required by the spec

## Self-Review Checklist

After writing the complete plan, review it against the spec before handing it off. Run this yourself — do not delegate it.

**1. Spec coverage.** Skim each requirement in the spec. Can you point to a task that implements it? List any gaps and add tasks for them.

**2. Placeholder scan.** Search the plan for any pattern from the "No Placeholders" section above. Fix every hit before proceeding.

**3. Type and name consistency.** Do the types, method signatures, and property names used in later tasks match what is defined in earlier tasks? A function named `clearItems()` in Task 3 and `clearAllItems()` in Task 7 is a bug in the plan. Fix it.

If you find issues, fix them inline. Then hand off.

## Saving the Plan

Save the plan to a file in the project before execution. A sensible default location is `docs/plans/YYYY-MM-DD-<feature-name>.md`, but defer to any project convention or user preference.

## Execution Handoff

After saving the plan, offer the user two execution paths:

> **Plan saved. Two options for execution:**
>
> **1. Subagent-per-task (recommended)** — dispatch a fresh subagent for each task with a review checkpoint between tasks. Faster iteration, isolated context per task, catches drift early.
>
> **2. Inline execution** — work through tasks sequentially in the current session, checking off each step before moving to the next.
>
> Which approach?

Whichever path the user chooses, enforce strict task-by-task execution: complete every checkbox in a task before starting the next task. No skipping steps. No batching tasks.
