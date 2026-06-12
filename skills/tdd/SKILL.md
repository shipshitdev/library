---
name: tdd
description: Test-driven development workflow for feature work and bug fixes. Use when the user asks for TDD, red-green-refactor, test-first implementation, regression-first bug fixes, or vertical-slice delivery.
license: MIT
metadata:
  version: "1.0.0"
  tags: "testing, tdd, red-green-refactor, quality"
  author: "Matt Pocock (MIT), adapted by Ship Shit Dev"
---

# Test-Driven Development

Build or fix behavior one verified slice at a time.

## Contract

Inputs:

- Feature request, bug report, PRD, issue, or implementation plan
- Existing test commands and project conventions
- Public interface or user-facing behavior to protect

Outputs:

- Test-first implementation plan
- New or updated tests and code when implementation is requested
- Verification commands and results

Creates/Modifies:

- Test files and production code needed for the requested behavior
- No unrelated refactors or broad test-suite rewrites

External Side Effects:

- None by default
- Do not use production data or live external writes for tests

Confirmation Required:

- Before changing public APIs, schemas, migrations, or user-visible behavior beyond the request

Delegates To:

- `testing-expert` for broad test strategy or framework setup
- `ai-regression-testing` for bug-specific regression coverage and path parity
- `debug` when the root cause is still unknown

## Core Rule

Write one failing behavior test, make it pass, then refactor. Repeat.

Tests should verify behavior through public interfaces. They should survive an
internal refactor. If a test fails because a private helper was renamed while
the behavior still works, the test is too coupled to implementation.

## Before Writing Tests

1. Find at least 3 existing tests or implementations that match the local pattern.
2. Identify the highest useful test boundary: user flow, route, service API, CLI, or pure function.
3. State the behavior in user or caller language.
4. Choose the narrowest command that runs the new test.
5. List only the first 1-3 behaviors needed for a useful vertical slice.

Ask only when the public behavior or interface is genuinely unclear. Otherwise
make a conservative assumption and proceed.

## Red-Green-Refactor Loop

### 1. Red

Add one test for one observable behavior.

The test must fail for the right reason:

- It exercises the public behavior, not a private detail.
- It fails because the behavior is missing or broken.
- It is deterministic and small enough to run repeatedly.

### 2. Green

Write the smallest production change that makes the test pass.

Do not add speculative options, future branches, or unrelated cleanup while the
test is red.

### 3. Refactor

After the test passes:

- Remove duplication.
- Improve naming around the domain language already used in the repo.
- Move complexity behind clearer interfaces only when the current slice proves it is needed.
- Re-run the narrow test after each refactor step.

## Vertical Slices

Prefer thin end-to-end slices over horizontal batches.

Good:

- One behavior test
- One implementation path
- One verification command
- A demoable or inspectable outcome

Bad:

- All tests first, then all implementation
- Tests for imagined data structures before behavior exists
- Mocking internal collaborators just to fit a planned design
- Splitting work by layer when no slice is independently useful

## Bug Fixes

For bugs, reproduce first. If the cause is unknown, use `debug`.

When the cause is known:

1. Convert the reproduction into a failing regression test.
2. Verify the test fails on the broken behavior.
3. Fix the behavior.
4. Verify the regression test passes.
5. Re-run the original reproduction or user flow.

If there is no good test boundary, state that as a design finding. Add the best
available verification and note the residual risk.

## Mocking Rules

- Mock network, time, randomness, payment providers, email, storage, and other external systems.
- Avoid mocking code owned by the module under test.
- Prefer fakes or fixtures when they keep behavior realistic.
- Do not assert implementation calls unless the call itself is the public contract.

## Done Checklist

- [ ] New behavior is covered by at least one failing-then-passing test.
- [ ] Test name describes the behavior, not the implementation.
- [ ] Test uses the public interface available to callers or users.
- [ ] Narrow verification command passes.
- [ ] Relevant broader suite, typecheck, or lint command passes when practical.
- [ ] No unrelated refactor or broad rewrite was bundled into the slice.
