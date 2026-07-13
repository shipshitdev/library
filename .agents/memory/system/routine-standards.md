# Routine Authoring Standard

Routines are unattended or recurring invocations of a reusable objective. Write
one platform-neutral routine family, parameterize the repository-specific inputs,
and let the Claude or Codex app own execution configuration.

This standard applies to scheduled-task prompts, automation prompt bodies, and
templates used to create them. It does not create or enable live schedules.

## Ownership Boundary

| Routine content owns | Harness/app owns |
|---|---|
| Objective and completion condition | Schedule, recurrence, and timezone |
| Named input parameters and defaults | Model and reasoning effort |
| Preconditions and read/write scope | Target project, cwd, workspace, and checkout |
| Safety gates and prohibited actions | Execution environment and sandbox policy |
| Evidence to collect and output schema | Notification and delivery configuration |
| Failure and escalation behavior | Enabled/paused state and concurrency policy |

Never repeat an app-owned value in the routine body. The body may consume a named
input such as `repository`, but it must not pin a concrete repository, checkout,
model, effort level, schedule, cwd, or environment.

## Canonical Routine Contract

Every routine family defines:

1. **Objective** — one measurable outcome.
2. **Parameters** — named inputs such as `repository`, `lookback_window`, and
   `report_destination`; no concrete project values in the reusable source.
3. **Preconditions** — required access, clean-state assumptions, and data sources.
4. **Procedure** — deterministic steps that use the parameters.
5. **Mutation policy** — read-only, local-write, external-write, or destructive.
6. **Safety gates** — explicit conditions that must be satisfied before each side
   effect class.
7. **Evidence** — facts, links, diffs, or command results that prove completion.
8. **Output** — a stable summary schema, including blocked/no-op outcomes.

## Parameterized Family Pattern

Maintain one source for a repeated family instead of project copies:

```markdown
# Dependency health sweep

Parameters:

- `repository` — repository selected by the app target/cwd
- `lookback_window` — reporting window supplied by the invocation
- `report_destination` — optional destination; defaults to draft-only output

Objective:

Identify actionable dependency risk in `repository` during `lookback_window` and
return a prioritized report with source evidence.

Mutation policy:

- Read-only by default.
- Do not open issues, send messages, update dependencies, or push changes unless
  the corresponding invocation gate is explicitly enabled.
```

Project variants supply only parameter values. They do not copy or rewrite the
procedure. If a project truly needs different steps, add a named policy parameter
or define a separate family with a different objective.

## Unattended Safety Gates

| Action class | Default | Gate required |
|---|---|---|
| Read local or remote state | Allowed | Access stays within the configured target |
| Write local files | Denied | Explicit `allow_local_writes`, allowed path scope, and a clean-state preflight |
| Create/update issues or PRs | Denied | Explicit `allow_external_writes` plus repository and action allowlists |
| Send email/chat/notifications | Draft only | Explicit `allow_send`, destination allowlist, and final content validation |
| Merge, deploy, delete, rotate secrets, charge, or publish | Prohibited unattended | Stop and request a separately authenticated human action |

An app-level permission or broad sandbox is not routine-level authorization. The
routine must still enforce its own narrow action gate. Never infer a send/write gate
from phrases such as “keep going,” “autonomous,” or “handle everything.”

For every allowed side effect:

- Re-read the target immediately before mutation.
- Make the operation idempotent or detect an already-complete state.
- Record what changed without printing credentials, tokens, environment values, or
  private prompt bodies.
- Stop on ambiguous ownership, destination, or destructive impact.

## Claude Scheduled-Task Adapter

Keep the scheduled task's `SKILL.md` body thin and route to the canonical family:

```markdown
---
name: dependency-health-sweep
description: Run the dependency health routine with app-supplied project inputs.
---

Apply the canonical dependency health sweep routine.

Parameters:

- `repository`: use the project selected by the scheduled-task app
- `lookback_window`: use the invocation input or the routine default
- `report_destination`: draft-only unless an explicit send gate is present
```

Select recurrence, model, effort, project, workspace, and delivery in the Claude
scheduled-task UI/configuration. Do not restate them in `SKILL.md`.

## Codex Automation Adapter

Keep the TOML prompt focused on routing and parameters. The surrounding automation
record owns execution fields:

```toml
name = "Dependency health sweep"
prompt = """
Apply the canonical dependency health sweep routine.
Use the repository selected by the automation target and return the standard report.
All external actions remain draft-only unless an explicit routine gate is present.
"""

# App-owned examples; values are selected in Codex, not copied into prompt text.
rrule = "<app-owned>"
model = "<app-owned>"
reasoning_effort = "<app-owned>"
cwds = ["<app-owned>"]
execution_environment = "<app-owned>"
target = "<app-owned>"
```

Treat the field list as a placement example, not an automation to install. Do not
write an `automation.toml` into a user's Codex home or create a live automation from
this repository.

## Read-Only Audit Mode

Run the local auditor against explicit roots or its standard user-level defaults:

```bash
python3 scripts/audit-routines.py
python3 scripts/audit-routines.py \
  --claude-dir ~/.claude/scheduled-tasks \
  --codex-dir ~/.codex/automations
```

The auditor reports anonymous source identifiers by default. It detects:

- exact and near-duplicate normalized routine bodies;
- model, effort, schedule, cwd/workspace/worktree, and environment directives in
  prompt content;
- app-owned Codex field names that are present, without emitting their values.

It never prints prompt bodies, environment values, or TOML values. Add
`--show-paths` only when local filenames are safe to reveal. Audit mode is read-only
and returns success with findings unless `--fail-on-findings` is explicitly set.

## Safe Migration

1. Pause or disable existing schedules in the owning app. Do not create replacements
   during discovery.
2. Run the read-only auditor and group duplicates by family.
3. Choose one representative body; remove app-owned settings and concrete project
   values.
4. Extract named parameters and add the canonical routine contract and safety gates.
5. Replace each paused copy with a thin adapter that routes to the family and supplies
   only parameters.
6. Dry-run each adapter in read-only/draft-only mode and compare its output schema.
7. Re-enable schedules manually in the owning app after review. Preserve the app's
   existing recurrence, target, model, effort, and environment rather than copying
   those values into the prompt.

Never migrate authentication material, environment values, or private prompt output
into this public repository.
