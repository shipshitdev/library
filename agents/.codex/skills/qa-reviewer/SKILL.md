---
name: qa-reviewer
description: Systematically review AI agent work for quality, accuracy, and completeness. Catches bugs, verifies patterns, checks against requirements, and suggests improvements before committing changes.
---
# QA Reviewer: Systematic Work Verification

## Purpose

This skill provides a structured framework for reviewing AI agent work before finalizing changes. It catches bugs, verifies accuracy, ensures completeness, and validates that solutions match requirements.

## When to Use

Use when:

- User says "check your work" or "review this" or "verify"
- After completing complex multi-step implementations
- Before committing major refactors or significant changes
- When making changes to critical files
- After implementing features with multiple requirements
- Proactively after any task >5 steps

Always Use when:

- Modifying commands or skills
- Updating critical documentation (CRITICAL-NEVER-DO.md, etc.)
- Making architectural changes
- Implementing new features
- Fixing reported bugs

## Workflow

1. Gather context and list requirements and constraints.
2. Verify each requirement and check for regressions.
3. Validate correctness with tests or inspection.
4. Summarize findings, risks, and follow-ups.

## References

- [Full guide: QA checklist, templates, and examples](references/full-guide.md)