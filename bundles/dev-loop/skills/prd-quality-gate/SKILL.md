---
name: prd-quality-gate
description: PRD completeness validation. Use to check that a PRD (or issue body that serves as one) contains the required sections before it is handed to a planning/execution agent, so the plan is built from a complete spec instead of hallucinated scope. Run it as a blocking gate or a warning-only lint.
metadata:
  version: "1.1.0"
  tags: "prd, planning, validation, quality-gate, spec, requirements, ears"
---

<prd_quality_gate>
A well-formed PRD (or the issue body that serves as one) must contain ALL of the
following sections as markdown headings (## or ###).

Required sections:

- Executive Summary
- Problem Statement
- Goals
- Functional Requirements
- Acceptance Criteria
- Verification Plan

Acceptance Criteria must be written in EARS (Easy Approach to Requirements
Syntax) so each bullet is machine-checkable and pass/fail without judgement.
Every bullet under Acceptance Criteria must match one of:

- WHEN <trigger> THE SYSTEM SHALL <response>        (event-driven)
- WHILE <state> THE SYSTEM SHALL <response>         (state-driven)
- WHERE <feature> THE SYSTEM SHALL <response>       (optional feature)
- IF <condition> THEN THE SYSTEM SHALL <response>   (unwanted behavior)
- THE SYSTEM SHALL <invariant>                      (ubiquitous)

A bullet that does not match this grammar (case-insensitive regex
`^\s*(\d+\.\s*)?(WHEN|WHILE|WHERE|IF|THE SYSTEM)\b.*\bSHALL\b`) is free-form
prose, not a verifiable criterion.

When the quality gate is ENABLED (blocking):

- Missing any required section → fail immediately with an actionable message
  listing the missing sections.
- Any Acceptance Criteria bullet that is not EARS-shaped → fail, quoting each
  offending bullet and the EARS pattern it should take.
- The author must update the PRD and re-run the gate before planning proceeds.

When the quality gate is DISABLED (default, warning-only):

- Missing sections → log a warning.
- Non-EARS Acceptance Criteria bullets → log a warning listing each offending
  bullet.
- Planning proceeds. The planner should still note the gaps in its output.

Section matching is case-insensitive against ## and ### headings. Exact heading
text must appear (e.g. "## Executive Summary" or "### Goals"). Headings nested
inside code fences are ignored by convention (they are examples, not structure).
</prd_quality_gate>
