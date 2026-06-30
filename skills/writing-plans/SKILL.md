---
name: writing-plans
description: >-
  Turn a spec or requirements doc into a comprehensive, bite-sized implementation plan: map every file, define 2-5 minute TDD tasks with complete code, and enforce DRY/YAGNI/frequent-commits discipline. Use when you have requirements ready and need a concrete execution plan before touching code, when a feature spans multiple files and needs decomposition, or when you want agentic workers to execute tasks reliably without guessing.
metadata:
  version: "1.1.0"
  source: https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md
  upstream_repo: obra/superpowers
  upstream_ref: main
  upstream_commit: f2cbfbefebbf
  last_synced: "2026-06-12"
  license: MIT
  tags: "planning, implementation-plan, tasks, tdd, dry, yagni, decomposition"
when_to_use: "write a plan, create implementation plan, plan this feature, break this into tasks, plan before coding, spec to tasks"
---
# Writing Plans

Write a comprehensive implementation plan assuming the implementer has zero context about the codebase and questionable test instincts. Document everything: which files to touch, complete code, exact commands, expected output, and how to verify. Deliver the whole plan as bite-sized checkboxed tasks. DRY. YAGNI. TDD. Frequent commits.

## Scope Check

If the spec covers multiple independent subsystems, consider breaking it into separate plans — one per subsystem. Each plan should produce working, testable software on its own. Deeply coupled work can share a plan; independently deployable subsystems should not.

## File Mapping (Before Any Tasks)

Map out which files will be created or modified and what each one is responsible for before defining tasks.

- Each file has one clear responsibility.
- Prefer smaller, focused files. The agent edits most reliably when it can hold the full file in context.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns. If the codebase uses large files, do not unilaterally restructure — but if a file you are modifying has grown unwieldy, including a split in the plan is reasonable.

Each task should produce self-contained changes that make sense independently.

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

Never write:

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

## Storing the Plan

**Post the plan as a comment on the work/PRD issue** — the same GitHub issue the
PRD lives on (or the work item the loop will pick up). The issue is the single
source of truth: the executor and all execution lanes read the issue body, the
linked PRD, and all comments, so a plan posted as a comment crosses to CI for
either engine. Do **not** save the plan to a local `docs/plans/*.md` file — that
file desyncs from the project the moment work starts and never reaches the loop.

- The comment **must start with the heading `## Implementation Plan`** so the
  executor can find it among the issue's comments.
- Post it with the plan markdown piped on stdin:

  ```bash
  gh issue comment <N> --body-file -   # plan markdown on stdin
  ```

- **Show the drafted plan first. Post only on approval** — never post speculatively.
- The plan is the *how*; the PRD body is the *what*. Keep the plan out of the PRD
  body — a comment co-locates the two on one issue without polluting the body.
- **No connected tracker?** Agree on the single canonical location with the user
  before writing — never default to a throwaway `docs/plans/` file.
- **Long plans:** if the plan exceeds one comment's limit (~65k chars), post it as
  sequential `## Implementation Plan (n/m)` comments rather than truncating.

## Execution Handoff

The plan lives on the issue, so hand off via the dispatch gate, not a file.

> **Plan posted to issue #N.** To dispatch it, move the issue to **Backlog** on the
> board (set `Status` = Backlog) and apply one gate: `dispatch:claude` (Claude lane)
> or `dispatch:codex` (Codex lane). The loop claims it, reads the
> `## Implementation Plan` comment, and works it task by task.

For execution **outside** the loop (working the plan directly in this session),
offer the two standalone paths — both read the plan from the issue comment, not a
file:

> **1. Subagent-per-task (recommended)** — dispatch a fresh subagent for each task with a review checkpoint between tasks. Faster iteration, isolated context per task, catches drift early.
>
> **2. Inline execution** — work through tasks sequentially in the current session, checking off each step before moving to the next.
>
> Which approach?

Whichever path runs, enforce strict task-by-task execution: complete every
checkbox in a task before starting the next task. No skipping steps. No batching tasks.
