---
name: gh-project-board
description: "Configure GitHub Projects v2 kanban boards with Ship Shit Dev defaults: the Backlog / In Progress / Human Review / Done / Deferred Status columns (the dev-loop board-as-truth model) and P0-P3 Priority. Use when setting up, copying, auditing, or normalizing GitHub project boards."
compatibility: Requires GitHub CLI gh with project scope. The bundled normalizer script runs with Node.js or Bun.
allowed-tools: Bash(gh *) Bash(node *) Bash(bun *)
metadata:
  version: "1.2.0"
  tags: "github, projects, kanban, triage"
---

# GH Project Board

## Contract

Inputs:

- GitHub owner login and project number, or permission to process every open
  project for an owner
- Optional new board title when copying the reference board
- Optional exact Status and Priority option names

Outputs:

- Project field audit summary
- Field normalization plan or applied status
- Board-layout verification result

Creates/Modifies:

- May create or update GitHub Projects v2 single-select fields
- May copy a GitHub Project when creating a new board
- Does not delete project items

External Side Effects:

- Reads GitHub Projects metadata
- Writes GitHub Projects field configuration only after approval
- May create a new GitHub Project only after approval

Confirmation Required:

- Before running field normalization with `--apply`
- Before copying a project
- Before processing every open project for an owner
- Before using `--exact`, because removed single-select options can clear item
  values that used those options

Delegates To:

- `prd-task-creator` when board setup reveals missing task structure
- `gh-fix-ci` when project automation depends on failing GitHub Actions

## Canonical Board Shape

Use GitHub Projects v2.

- Board view layout: `Board`
- Kanban column field: `Status`
- Status options: `Backlog`, `In Progress`, `Human Review`, `Done`, `Deferred` —
  the dev-loop board-as-truth model. `In Progress` holds the running AI loop
  (its `loop:planning/executing/testing/shipping` sub-phases are labels, not
  columns); `Human Review` is the human PR-review gate
- Priority source: organization-native Issue Field when present; project-local
  single-select only when the organization has no native Priority (or a user
  project uses project-local fields)
- Project-local defaults: `P0 🔥`, `P1`, `P2`, `P3`. Native Priority keeps its
  organization schema and option names; do not create a duplicate project field.

The Ship Shit Dev reference board is
`https://github.com/orgs/shipshitdev/projects/1`. `Human Review` is the human gate
column; automated testing is a phase inside `In Progress` (label `loop:testing` +
CI on the PR), not its own column. An older board with `To Do` / `Testing` lanes
should be normalized to the five-column model.

## Workflow

1. Verify GitHub CLI auth and project scope:

   ```bash
   gh auth status -h github.com
   gh project list --owner <owner>
   ```

2. Inspect the reference board or target board:

   ```bash
   gh project view 1 --owner shipshitdev --format json
   gh project field-list 1 --owner shipshitdev --format json
   gh project view <number> --owner <owner> --format json
   gh project field-list <number> --owner <owner> --format json
   ```

3. For a new board, prefer copying the reference board so the kanban view is
   preserved:

   ```bash
   gh project copy 1 \
     --source-owner shipshitdev \
     --target-owner <owner> \
     --title "<project title>" \
     --format json
   ```

   Then normalize the copied board to add any missing approval lane:

   ```bash
   node ${CLAUDE_SKILL_DIR}/scripts/setup-gh-project-board.mjs \
     --owner <owner> \
     --project <number> \
     --apply
   ```

4. For an existing board, audit first:

   ```bash
   node ${CLAUDE_SKILL_DIR}/scripts/setup-gh-project-board.mjs \
     --owner <owner> \
     --project <number>
   ```

5. Show the audit summary and get approval before applying:

   ```bash
   node ${CLAUDE_SKILL_DIR}/scripts/setup-gh-project-board.mjs \
     --owner <owner> \
     --project <number> \
     --apply
   ```

6. To audit every open project for an owner:

   ```bash
   node ${CLAUDE_SKILL_DIR}/scripts/setup-gh-project-board.mjs \
     --owner <owner> \
     --all-open
   ```

   Apply to every open project only when the user explicitly asks:

   ```bash
   node ${CLAUDE_SKILL_DIR}/scripts/setup-gh-project-board.mjs \
     --owner <owner> \
     --all-open \
     --apply
   ```

## Native Priority discovery

Before normalization, the script reads the board owner and issue repository
owners represented by the board. For each organization, it reads
`GET /orgs/{org}/issue-fields`. It skips project Priority normalization whenever
native Priority exists. An unavailable/ambiguous schema withholds the Priority
plan and marks the read-only audit incomplete while preserving available Status
and view evidence. Apply fails before writes. A 404 is not proof that native Priority does not exist. Status stays project-scoped.

Native field configuration affects every repository in the organization. It is
outside this project-normalization contract; report differences for a separately
scoped organization change. On mixed-organization boards, inspect the linked
issue's repository organization before routing value changes. The reconciliation
report resolves that source per issue. A copied reference board can contain an
old project Priority; leave it intact pending an explicitly reviewed migration,
and use the native issue value as authoritative.

For native Priority value changes, resolve its numeric REST field ID and exact
option name, obtain approval, and use the additive POST endpoint documented in
[Issue field values](https://docs.github.com/en/rest/issues/issue-field-values).
Do not use project item field mutations for an organization Issue Field.

## Normalizer Options

- `--status "Backlog,In Progress,Human Review,Done,Deferred"` overrides the Status
  option list (this is the default — the dev-loop five-column model).
- `--priority "P0,P1,P2,P3"` uses ASCII-only priority names.
- `--exact` removes non-canonical options after explicit approval.
- `--include-closed` includes closed projects when used with `--all-open`.

## Rules

- `Human Review` is the human-gate `Status` column, not a label. Automated testing
  is a phase inside `In Progress` (the `loop:testing` label + PR CI), not a column.
- Preserve unknown Status or Priority options unless the user explicitly asks
  for exact normalization.
- Preserve existing option IDs when renaming or recoloring options so existing
  item values remain attached.
- If no board view exists, report the blocker. GitHub exposes project field
  mutations through the public API, but not public mutations for creating a
  board view; copy the reference board or create the board view in GitHub, then
  rerun verification.
- Do not apply changes to closed projects unless the user explicitly asks.
