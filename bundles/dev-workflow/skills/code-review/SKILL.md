---
name: code-review
description: >-
  Correctness and security gate for incoming pull requests. Auto-invoked when
  reviewing a diff, evaluating a PR, running /code-review at any effort level,
  or asked "is this safe to merge?" Covers bugs, TypeScript hygiene, security,
  database safety, test existence, devex regressions, and feature-flag leaks.
metadata:
  version: "1.0.0"
  tags: "code-review, correctness, security, testing, devex, feature-flags"
  author: Ship Shit Dev
allowed-tools: Bash(git *) Bash(gh *)
when_to_use: "review this PR, is this safe to merge, /code-review, check the diff, look at my changes, review my code, code review"
---

# Code Review

Correctness and security gate. High-conviction findings only — flag issues you
are certain about. Ambiguity defaults to "request changes." Structural concerns
(cohesion, abstraction altitude, circular deps, dead code) belong to the
`structural-review` skill; trust it on those axes and own correctness + security
here.

CLAUDE.md stack rules (Bun, Tailwind v4, Next.js 16, shadcn/ui) are validated
by the /code-review harness CLAUDE.md compliance layer. Do not re-flag them here.

## Contract

Inputs:

- A diff, branch, or PR to review. Read-only `git`/`gh` commands gather scope.

Outputs:

- A findings list bucketed into Block Merge / Request Changes / Approve, each
  with file, line, and a one-sentence rationale.

Creates/Modifies:

- None. This skill reports; it does not edit files or open PRs.

External Side Effects:

- Read-only `git` and `gh` invocations only. No mutations, no deploys.

Confirmation Required:

- None. All output is advisory.

Delegates To:

- `structural-review` for cohesion/abstraction/dead-code axes.
- `security-audit` for OWASP-depth security review.

## Critical Checklist

### 1. Security and Data Isolation

- ALL queries filter by tenant/organization (if multi-tenant)
- ALL queries filter soft-deleted records (if applicable)
- No cross-tenant data access
- Auth guards on protected routes
- No unintended public endpoints — every route's auth posture is intentional
- Input validation via DTOs/schemas
- No secrets, tokens, or credentials committed or logged

### 2. TypeScript

- No `any` types — define proper interfaces or named types in `*.types.ts`
- No bare `unknown` without a type guard — bare `unknown` is deferred `any`
- No `as X` casts without an explanatory comment
- Interfaces/props in dedicated files, not inline in component or service files
- Return types on all functions
- No `console.log` — use the project logger (LoggerService, pino, winston)
- No `@ts-ignore` or `@ts-expect-error` without an explanatory comment

### 3. Pattern Compliance

- Follows existing codebase patterns (verify 3+ real examples before flagging)
- Path aliases over relative imports

### 4. Database

- Tenant/organization filter in ALL queries (if applicable)
- Soft delete filter in ALL queries (if applicable)
- Projections for large documents
- Indexes exist for query patterns
- No N+1 queries visible in the diff
- Sequential `await db.update()` calls that can leave the DB half-written on
  failure must be wrapped in a transaction or collapsed to a single atomic write

### 5. Error Handling

- Try/catch blocks present
- Framework-specific exceptions (not generic `Error`)
- Errors logged via logger service
- Generic messages to client (no internals exposed)

### 6. Testing

- Unit tests exist and pass
- All public methods tested
- Error cases tested
- Tests assert behavior, not just that code runs (no hollow snapshot tests)

### 7. Frontend

- Cleanup in `useEffect` with async calls (`AbortController`)
- Loading and error states handled
- Semantic HTML with ARIA labels where interactive elements are added

### 8. API

- Proper HTTP status codes
- DTOs for request/response
- API documentation decorators present where the project uses them (e.g.
  `@ApiOperation` / `@ApiResponse`)
- No internal stack traces leaked to API consumers

### 9. Devex Regressions

Changes that silently break the local dev loop for other engineers:

- **Env var renames or additions** — is there a corresponding update to
  `.env.example` / `.env.template`? Is the rename announced (migration note,
  changelog, or PR description)?
- **Secret-read changes** — new secrets accessed at runtime that are not in the
  documented setup path; access moved from one provider/vault path to another
  without updating the runbook
- **Port or network remaps** — service, dev-server, or docker-compose port
  changed without updating README/setup docs and all dependent config files
- **New mandatory setup scripts** — a migration, seed, or one-time bootstrap
  that must be run before the app starts; not documented in the PR description
  or setup guide
- **Build-flow changes** — new required build steps, changed output directories,
  added pre/post scripts in `package.json` that break the existing
  `bun run dev` / `bun run build` contract without a clear migration note

Block merge when a devex regression is unannounced. Request changes when it is
documented but the documentation is in the wrong place.

### 10. Feature-Flag / Gate Leaks

Features meant to be gated that are shipping unflagged or partially flagged:

- **Obvious leaks** — a new route, component, or API endpoint that the PR
  description says is behind a flag, but the flag check is absent or only
  applied to the UI, not the API handler
- **Subtle leaks** — flag check present in the happy path but absent in an
  error handler, a background job, or an admin-only path that calls the same
  service method
- **Always-on constants** — `const ENABLE_NEW_CHECKOUT = true` standing in for
  a real flag evaluation; will never be cleaned up and bypasses the flag service
- **Flag introduced without a cleanup plan** — no linked issue or TODO comment
  for flag removal; flag names should make the intended lifetime obvious
- **Rollout config inconsistencies** — flag defined in the PR but the rollout
  percentage / targeting rule is missing or set to 100% default, defeating the
  purpose of gating

Flag leaks that expose unreleased functionality to all users are merge blockers.
Missing cleanup tickets are a "request changes."

## Approval Criteria

### Block Merge

- Security issues present
- Missing tenant/organization filtering (if required)
- `any` types or bare `unknown` without type guards
- Tests failing or tests entirely absent for new public methods
- Build failing
- Feature-flag leak exposing unreleased functionality
- Unannounced devex regression (broken env, port, or build contract)
- Non-atomic multi-step DB mutations with no transaction

### Request Changes

- Missing documentation for env var additions or setup-script requirements
- Performance concerns clearly visible in the diff (N+1, missing index)
- Pattern violations (raw HTML in files that already import the UI library)
- Feature flag introduced without a cleanup issue/TODO
- Hollow tests that assert execution rather than behavior

### Approve

- All security checks pass
- Tests pass and assert real behavior
- Follows codebase patterns
- Devex impact documented
- Feature flags have cleanup plan

## Scope Boundary

This skill = **correctness + security gate**.

Structural and maintainability concerns — module cohesion, abstraction altitude,
circular dependencies, dead-code introduction, API surface sprawl, whether the
implementation matches the stated architecture — belong to the `structural-review`
skill. Do not re-litigate those axes here; trust `structural-review` to own them.

Security-audit depth (OWASP rubric, dependency CVEs, timing attacks, privilege
escalation paths) belongs to the `security-audit` skill. Surface obvious issues
found in the diff, but do not attempt a full security audit in this skill.
