---
name: spec-first
description: Enforces a spec → plan → execute → verify loop before writing code, preventing "looks right" failures. Activates on "build X", "implement...", "add a feature that...", or any multi-file/unclear-requirements request. Creates spec.md, todo.md, and decisions.md as durable artifacts.
metadata:
  version: "1.1.0"
  tags: "specification, planning, execution, ears"
---

# Spec-First Development

## Contract

Inputs:

- User request describing a feature, project, or non-trivial implementation task.

Outputs:

- Stage A framing with 3 approaches and tradeoffs.
- Draft `spec-[feature-name].md` content for `.agents/memory/`.
- Draft `todo.md` checklist with per-step verification commands.

Creates/Modifies:

- `.agents/memory/spec-[feature-name].md` (spec artifact).
- `.agents/memory/decisions-[feature-name].md` (decision log).
- GitHub Issue (checklist body for active todo tracking).

External Side Effects:

- Creates GitHub Issues via the gh CLI when creating todo tracking.

Confirmation Required:

- Before creating GitHub Issues.
- Before proceeding from Stage C to Stage D (execution).

Delegates To:

- `prd-task-creator` for PRD-style issue creation.
- `executing-plans` for Stage D autonomous execution.

A structured workflow for LLM-assisted coding that delays implementation until decisions are explicit.

## When This Activates

- "Build X" or "Create Y" (new features/projects)
- "Implement..." (non-trivial functionality)
- "Add a feature that..." (multi-step work)
- Any request requiring 3+ files or unclear requirements

## When to Skip

- Single-file changes under 50 lines
- Typo fixes, log additions, config tweaks
- User explicitly says "just do it" or "quick fix"

## Core Principles

1. **Delay implementation until tradeoffs are explicit** — Use conversation to clarify constraints, compare options, surface risks. Only then write code.

2. **Treat the model like a junior engineer with infinite typing speed** — Provide structure: clear interfaces, small tasks, explicit acceptance criteria. Code is cheap; understanding and correctness are scarce.

3. **Specs beat prompts** — For anything non-trivial, create a durable artifact (spec file) that can be re-fed, diffed, and reused across sessions.

4. **Generated code is disposable; tests are not** — Assume rewrites. Design for easy replacement: small modules, minimal coupling, clean seams, strong tests.

5. **The model is over-confident; reality is the judge** — Everything important gets verified by execution: tests, linters, typecheckers, reproducible builds.

## The 6-Stage Workflow

### Stage A: Frame the Problem (conversation mode)

**Goal:** Decide before you implement.

Prompts that work:

- "List 3 viable approaches. Compare on: complexity, failure modes, testability, future change, time to first demo."
- "What assumptions are you making? Which ones are risky?"
- "Propose a minimal version that can be deleted later without regret."

**Output:** Decision notes in `.agents/memory/decisions-[feature-name].md`

### Stage B: Write spec.md (freeze decisions)

**Goal:** Turn decisions into unambiguous requirements.

**File:** `.agents/memory/spec-[feature-name].md`

```markdown
# [Feature Name] Spec

## Purpose
One paragraph: what this is for.

## Non-Goals
Explicitly state what you are NOT building.

## Interfaces
Inputs/outputs, data types, file formats, API endpoints, CLI commands.

## Key Decisions
Libraries, architecture, persistence choices, constraints.

## Edge Cases and Failure Modes
Timeouts, retries, partial failures, invalid input, concurrency, idempotency.

## Acceptance Criteria
Bullet list of EARS statements (`WHEN`/`WHILE`/`WHERE`/`IF … THE SYSTEM SHALL …`,
or a bare `THE SYSTEM SHALL …`) — testable, pass/fail, no judgement.
Avoid "should be fast." Prefer: "WHEN given 1k items THE SYSTEM SHALL process them under 2s on M1 Mac."

## Test Plan
Unit/integration boundaries, fixtures, golden files, what must be mocked.
```

### Stage C: Generate todo.md (planning mode)

**Goal:** Stepwise checklist where each step has a verification command.

**Tracking:** a GitHub Issue per feature — the checklist below is the issue body.

```markdown
# [Feature Name] TODO

- [ ] Add project scaffolding (build/run/test commands)
  Verify: `bun run build && bun run test`

- [ ] Implement module X with interface Y
  Verify: `bun run test -- --grep "module X"`

- [ ] Add tests for edge cases A/B/C
  Verify: `bun run test -- --grep "edge cases"`

- [ ] Wire integration
  Verify: `bun run integration`

- [ ] Add docs
  Verify: `bun run docs && open docs/index.html`
```

Each item must be independently checkable. This prevents "looks right" progress.

### Stage D: Execute Changes (implementation mode)

**Goal:** Small diffs, frequent verification, controlled context.

Rules:

- One logical change per step
- Keep focus on one interface at a time
- After each change: run verification command, paste actual output back
- Commit early and often

For large codebases:

- Provide only relevant files plus spec/todo
- If summarizing repo, do it once and keep as reusable artifact

### Stage E: Verify and Review (adversarial mode)

**Goal:** Force the model to try to break its own work.

Prompts:

- "Act as a hostile reviewer. Find correctness bugs, not style nits. List concrete failing scenarios."
- "Given these acceptance criteria, which are not actually satisfied? Be specific."
- "Propose 5 tests that would fail if the implementation is wrong."

### Stage F: Decide What Lasts

**Goal:** Keep the system easy to delete and rewrite.

Heuristics:

- Keep "policy" (business rules) separate from "mechanism" (I/O, DB, HTTP)
- Prefer shallow abstractions that can be removed without cascade
- Invest in tests and fixtures more than clever architecture

## The Three-Artifact Convention

Durable spec + decisions live in `.agents/memory/` (not project root); the stepwise todo is tracked as a GitHub Issue:

```
.agents/memory/
├── spec-[feature-name].md       # what/why/constraints
└── decisions-[feature-name].md  # tradeoffs, rejected options, assumptions

GitHub Issue (one per feature)   # steps + verification commands (checklist body)
```

**Naming:** Use the feature/task name (e.g., `user-auth`, `api-refactor`) as the filename suffix and the issue title.

**Why memory/ + Issues:**

- Keeps project root clean
- Durable spec/decisions stay in `.agents/memory/` (the source of truth)
- Active todos live in GitHub Issues, where work is tracked
- Works with prd-task-creator and executing-plans skills
- Persists across sessions

## Agent Readiness Checklist (IMPACT)

Before running autonomous/agentic execution, verify:

| Dimension | Question | If No... |
|-----------|----------|----------|
| **Intent** | Do you have acceptance criteria and a test harness? | Don't run agent |
| **Memory** | Do you have durable artifacts (spec/todo) so it can resume? | It will thrash |
| **Planning** | Can it produce/update a plan with checkpoints? | It will improvise badly |
| **Authority** | Is what it can do restricted (edit, test, commit)? | Too risky |
| **Control Flow** | Does it decide next step based on tool output? | It's just generating blobs |
| **Tools** | Does it have minimum necessary tooling and nothing extra? | Attack surface too large |

Approve at meaningful checkpoints (end of todo item, after test suite passes), not every micro-step.

## Prompt Patterns

**Authoritarian (for correctness):**

```
Edit these files: [paths]
Interface: [exact signatures]
Acceptance criteria: [list]
Required tests: [list]
Don't change anything else.
```

**Options and tradeoffs (for design):**

```
Give me 3 options and a recommendation.
Make the recommendation conditional on constraints A/B/C.
```

**Context discipline (for large codebases):**

```
Only use the files I provided.
If you need more context, ask for a specific file and explain why.
```

**Make it provable:**

```
Add a test that fails on the buggy version and passes on the correct one.
```

## Output Format

When this skill activates, produce:

```
SPEC-FIRST WORKFLOW

STAGE A - FRAMING:
[3 approaches with tradeoffs]
[Recommendation]

STAGE B - SPEC:
[Draft spec.md content]

STAGE C - TODO:
[Draft todo.md with verification commands]

Ready to proceed to Stage D (execution)?
```
