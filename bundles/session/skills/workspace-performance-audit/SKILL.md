---
name: workspace-performance-audit
description: Orchestrates comprehensive performance audits across full-stack monorepos. Coordinates performance-expert, design-consistency-auditor, accessibility, security-expert, and qa-reviewer skills to audit frontend, backend, database, browser extensions, and shared packages. Use when asked for a full workspace performance review, monorepo audit, or to identify bottlenecks across frontend, backend, and extensions.
disable-model-invocation: true
metadata:
  version: "1.0.0"
  tags: "performance, audit, monorepo"
---

# Workspace Performance Audit

## Contract

Inputs:

- Monorepo root path (defaults to current working directory)
- Optional: target domain(s) to focus on (frontend, backend, database, extension)
- Optional: audit mode (quick or full)

Outputs:

- Consolidated performance audit report
- Prioritized recommendations with severity ratings

Creates/Modifies:

- `.agents/memory/performance-audit-YYYY-MM-DD.md` — writes the audit report

External Side Effects:

- None. Read-only analysis only; does not deploy, modify, or install anything.

Confirmation Required:

- Before writing the output report if the target path is outside the current workspace

Delegates To:

- `performance-expert` for metrics and optimization
- `design-consistency-auditor` for UI/UX consistency
- `qa-reviewer` for validation and prioritization

## Skills Orchestrated

| Skill | Focus Area | Phase |
|-------|------------|-------|
| `performance-expert` | Performance metrics & optimization | 1-4 |
| `design-consistency-auditor` | UI/UX consistency & design debt | 1 |
| `accessibility` | WCAG 2.1 AA compliance | 1 |
| `security-expert` | Security validation | 2 |
| `qa-reviewer` | Validation & prioritization | 5 |

## Orchestration Flow

```
Phase 0: Workspace Discovery
    → Identify apps, packages, tech stacks

Phase 1: Frontend Audit (Next.js)
    → Core Web Vitals, Bundle Analysis, Design, A11y

Phase 2: Backend Audit (NestJS)
    → API Response Times, N+1 Queries, Security

Phase 3: Database Audit (MongoDB)
    → Query Performance, Index Analysis

Phase 4: Extension & Packages
    → Bundle Sizes, Memory, Dependencies

Phase 5: Consolidation
    → Aggregate, Score, Prioritize, Report
```

## Key Metrics by Domain

| Domain | Key Metrics | Targets |
|--------|-------------|---------|
| Frontend | LCP, FID, CLS | <2.5s, <100ms, <0.1 |
| Backend | p50, p95 response | <100ms, <200ms |
| Database | Query p95, Index hit | <50ms, >95% |
| Extension | Content script size | <50KB |

## Usage Modes

**Quick Audit:** Essential checks only → 1-page summary
**Full Audit:** All phases → Complete report
**Domain-Specific:** Single domain focus

---

**For detailed phase execution, metric collection commands, report templates, and example interactions:** load `${CLAUDE_SKILL_DIR}/references/full-guide.md` when starting a full audit or when a specific phase requires detailed guidance.
