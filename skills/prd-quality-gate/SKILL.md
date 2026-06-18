---
name: prd-quality-gate
description: PRD completeness validation. Use to check that a PRD (or issue body that serves as one) contains the required sections before it is handed to a planning/execution agent, so the plan is built from a complete spec instead of hallucinated scope. Run it as a blocking gate or a warning-only lint.
metadata:
  version: "1.0.0"
  tags: "prd, planning, validation, quality-gate, spec, requirements"
---

<prd_quality_gate>
A well-formed PRD (or the issue body that serves as one) must contain ALL of the
following sections as markdown headings (## or ###). Missing sections reduce plan
quality and risk hallucinated scope.

Required sections:

- Executive Summary
- Problem Statement
- Goals
- Functional Requirements
- Acceptance Criteria
- Verification Plan

When the quality gate is ENABLED (blocking):

- Missing any required section → fail immediately with an actionable message
  listing the missing sections.
- The author must update the PRD and re-run the gate before planning proceeds.

When the quality gate is DISABLED (default, warning-only):

- Missing sections → log a warning.
- Planning proceeds. The planner should still note the gaps in its output.

Section matching is case-insensitive against ## and ### headings. Exact heading
text must appear (e.g. "## Executive Summary" or "### Goals"). Headings nested
inside code fences are ignored by convention (they are examples, not structure).
</prd_quality_gate>
