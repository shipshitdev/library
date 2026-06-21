# Prd - One Front Door for PRDs and Feature Planning

Drive the full product-spec lifecycle from one command — create a GitHub issue
or local PRD, enforce a spec-first loop, validate completeness, draft a full PRD,
intake a stakeholder requirement to a kanban board, or run a discovery interview
— instead of remembering which planning skill fits which step.

## Usage

```bash
/prd                  # status: domain overview + usage
/prd new              # create a GitHub issue or local PRD/task file for a feature or bug
/prd spec             # enforce spec → plan → execute → verify loop before writing code
/prd gate             # validate a PRD for completeness before handing it to a planning agent
/prd write            # draft and formalize a feature as a full PRD ready for a planning agent
/prd intake           # turn a client or stakeholder requirement into kanban issues on GitHub Projects
/prd interview        # run a repo-grounded discovery interview before PRD writing or planning
```

## Steps

- **`new`** — the `task-prd-creator` skill: create a well-written PRD, task, or
  GitHub issue/sub-issue for a feature, bug, or enhancement.
- **`spec`** — the `spec-first` skill: enforce a spec → plan → execute → verify
  loop before writing code, producing `spec.md`, `todo.md`, and `decisions.md`
  as durable artifacts.
- **`gate`** — the `prd-quality-gate` skill: validate that a PRD contains all
  required sections (Executive Summary, Problem Statement, Goals, Functional
  Requirements, Acceptance Criteria, Verification Plan) before it is handed to a
  planning agent.
- **`write`** — the `writing-prds` skill: draft, scope, and formalize a feature
  as a PRD that a planning agent can consume in one shot without re-elicitation.
- **`intake`** — the `feature-intake` skill: capture a client or stakeholder
  feature request, turn it into a planner-ready PRD epic with scoped sub-issues,
  check for duplicate work, and place approved issues on a GitHub Projects kanban.
- **`interview`** — the `interview` skill: conduct a repo-grounded discovery
  interview before PRD writing, feature intake, or implementation planning,
  producing a concise handoff brief with focused follow-up questions.

## Workflow

Use the `prd-dispatch` skill. It parses the subcommand and delegates to the
right planning engine. Read-only until the delegated skill's own confirmation
gate; it never creates issues, writes files, or places items on a board without
the delegated skill's gate firing.

1. **Parse the argument** into a mode (`status` / `new` / `spec` / `gate` /
   `write` / `intake` / `interview`). Unknown argument → print Usage, don't guess.
2. **Route** to the delegated skill (or, for `status`, print the domain overview
   and Usage block and stop).
3. **Defer** preconditions and confirmation to the delegated skill — this command
   does not relax them.
