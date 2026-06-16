# Plan: board-as-truth status + full label namespacing + ubuntu-latest CI

## Context

Three problems in the autonomous dev loop, fixed together because they touch the
same files (workflows, setup script, executing-plans, docs):

1. **Status is duplicated.** Status lives in BOTH the GitHub Projects v2 `Status`
   single-select field (the board column) AND in `status:todo` / `status:testing`
   labels. Two sources of truth drift. Decision: **the board `Status` field is the
   SOLE source of truth.** Delete the two `status:*` labels. The setup skill must
   provision the board so this is not a manual step ("included in the set up skill").

2. **Labels are half-namespaced.** `priority:*` and `rejection:*` are already
   `prefix:value`. The rest are bare: `ready-for-agent`, `ready-for-codex`,
   `claimed`, `feature`. Decision: **namespace everything** —
   `ready-for-agent`→`dispatch:claude`, `ready-for-codex`→`dispatch:codex`,
   `claimed`→`claim:active`, `feature`→`type:feature`.

3. **CI runs on a dead runner.** All three workflows pin
   `runs-on: blacksmith-4vcpu-ubuntu-2404`. Blacksmith is gone — purge it.
   Decision: **`runs-on: ubuntu-latest`** in every workflow.

**Orthogonal axes (the load-bearing distinction):** *status* (where the issue is)
and *dispatch* (which engine may pick it up) are independent. Status becomes a
board field. **Dispatch must STAY a label** — workflows trigger on
`issues: [labeled]` and key off `github.event.label.name`; a Projects v2 field
change does not reliably fire a repo workflow. So `dispatch:claude` /
`dispatch:codex` remain labels by design, not by omission.

## Locked decisions (from the user)

- Status = board field only; `status:todo` / `status:testing` labels deleted;
  board provisioned by the setup skill.
- Full namespacing: `dispatch:claude`, `dispatch:codex`, `claim:active`,
  `type:feature` (priority/rejection already done).
- CI: `ubuntu-latest`. **Blacksmith fully purged — zero residual references.**

## Rename / delete map

| Old label | New | Action |
|-----------|-----|--------|
| `status:todo` | — | **delete** (board "To Do" column) |
| `status:testing` | — | **delete** (board "Testing" column) |
| `ready-for-agent` | `dispatch:claude` | rename |
| `ready-for-codex` | `dispatch:codex` | rename |
| `claimed` | `claim:active` | rename |
| `feature` | `type:feature` | rename |
| `priority:*`, `rejection:*`, `wontfix` | (unchanged) | keep |

This repo (`shipshitdev/skills`) has **no live dev-loop labels** — it ships the
*tooling*, it isn't run through the loop. So here the rename is a pure
source/doc edit. The live `gh label edit <old> --name <new>` migration (which
auto-moves the label on all issues) is guidance baked into the setup script for
**consumer repos**.

## Board model (4 columns)

`Status` single-select options: **Backlog · To Do · Testing · Done**. Maps to
issue state: Backlog/To Do/Testing = open, Done = closed. The agent reads/writes
the field via `gh project`:

- Read: `gh project item-list <num> --owner <org> --format json -L 500`
  (default limit is 30 — must pass `-L 500`); the column surfaces as `.status`.
- Write: `gh project item-edit --id <PVTI_itemId> --field-id <STATUS_FIELD_ID>
  --project-id <PVT_nodeId> --single-select-option-id <optId>`
  (`item-edit` needs the `PVTI_*` item id, not the issue number → look it up from
  `item-list` filtered by `.content.number == N`).

**Hard auth constraint:** the Actions default `GITHUB_TOKEN` **cannot** read/write
an org-owned Projects v2 board. The dispatch workflows that write the board need a
`project`-scoped PAT, stored as secret **`PROJECTS_TOKEN`** (classic: `project` +
`repo`; or fine-grained: org Projects read/write + repo write). Local `/loop` runs
under the user's own `gh` auth, which already has `project` scope — no PAT needed
locally.

> **Security:** `PROJECTS_TOKEN` is created and entered by the **user** via the
> `gh secret set` hidden prompt in the setup script. Claude never generates,
> types, echoes, or stores the token value.

## Deliverable 1 — CI runner: ubuntu-latest (purge blacksmith)

Replace `runs-on: blacksmith-4vcpu-ubuntu-2404` → `runs-on: ubuntu-latest` in:

- `.github/workflows/generate-bundles.yml:25`
- `.github/workflows/agent-dispatch.yml:35`
- `.github/workflows/codex-dispatch.yml:34`

Grep-verify zero `blacksmith` references remain anywhere in the repo after the
edit. (The `github-actions[bot]` `Co-Authored-By` in generate-bundles' auto-commit
message is the bot's own commit trailer — leave it.)

## Deliverable 2 — board as the status source of truth

### 2a. Dispatch workflows write the board, not status labels

**`agent-dispatch.yml`** (Claude lane):

- Trigger gate `:34`: `github.event.label.name == 'ready-for-agent'` →
  `'dispatch:claude'`.
- Auth `:46`: `github_token: ${{ secrets.GITHUB_TOKEN }}` →
  `${{ secrets.PROJECTS_TOKEN }}` (needs board write).
- Claim step (prompt ~`:68,70`): add label `claim:active` (was `claimed`).
- Completion/transition (prompt ~`:78-79,83`): replace "strip
  `status:todo`/`claimed`/`ready-for-agent` + add `status:testing`" with:
  → set board `Status` = **Testing** via `gh project item-edit` (look up item id
  first), and remove labels `claim:active,dispatch:claude`. No status labels touched
  (they no longer exist).
- Header comment `:5`: update prose to "board Status, not labels."

**`codex-dispatch.yml`** (Codex lane): identical shape —

- Gate `:33`: `== 'ready-for-codex'` → `'dispatch:codex'`.
- Auth `:45-46`: `GH_TOKEN` / `GITHUB_TOKEN` → `${{ secrets.PROJECTS_TOKEN }}`.
- Prompt `:59,62,72-73,77`: `claimed`→`claim:active`; transition writes board
  Testing + removes `claim:active,dispatch:codex`.
- Header `:3-4`: prose update.

Both prompts keep "Read the issue body, the linked PRD, and ALL comments" and the
`## Implementation Plan` convention (already shipped) untouched.

### 2b. `.github/agent-loop.env` (new, committed — non-secret IDs)

The workflows need the board's node ids to call `item-edit`. Store them in a
committed env file (ids are not secret; only the PAT is). Schema:

```
PROJECT_OWNER=<org-or-user>
PROJECT_NUMBER=<n>
PROJECT_NODE_ID=PVT_xxx
STATUS_FIELD_ID=PVTSSF_xxx
STATUS_BACKLOG_OPTION_ID=xxx
STATUS_TODO_OPTION_ID=xxx
STATUS_TESTING_OPTION_ID=xxx
STATUS_DONE_OPTION_ID=xxx
```

Written by the setup script after it provisions the board; workflows + `/loop`
`source` it.

### 2c. `scripts/setup-dev-loop.sh` — provision the board

Currently installs labels + workflows + secrets. Add:

- **New LABELS block** (`:68-82`) — drop both `status:*`, rename gate/claim/feature,
  colors preserved:

  ```bash
  LABELS=(
    "claim:active|5319e7|An agent currently holds this issue (30-min claim lock)"
    "priority:high|b60205|Queue ordering — picked first"
    "priority:medium|d93f0b|Queue ordering — picked after high"
    "priority:low|0e8a16|Queue ordering — picked last"
    "rejection:1|e99695|QA rejection count — 1st kickback from Testing"
    "rejection:2|e99695|QA rejection count — 2nd kickback from Testing"
    "rejection:3|e99695|QA rejection count — 3rd kickback from Testing"
    "dispatch:claude|006b75|Dispatch gate (human opt-in) — Claude lane runs only on issues carrying this"
    "dispatch:codex|10a37f|Dispatch gate (human opt-in) — Codex/GPT lane runs only on issues carrying this"
    "type:feature|a2eeef|Applied by feature-intake to PRD epics and their sub-issues"
    "wontfix|ffffff|Closed; will not be actioned"
  )
  ```

- **For existing consumer repos:** before seeding, `gh label edit` the four renamed
  labels in place (migrates them on all open issues), then `gh label delete` the two
  `status:*` labels (idempotent / `|| true`).
- **Board provisioning step:** create-or-reuse the project
  (`gh project create` / `gh project link`), then normalize the `Status` options to
  the 4-column model by calling the existing board skill:

  ```bash
  node skills/gh-project-board/scripts/setup-gh-project-board.mjs \
    --owner <owner> --project <num> \
    --status "Backlog,To Do,Testing,Done" --exact --apply
  ```

  (That script defaults to a 6-option set — Backlog/Todo/In Progress/Human
  Review/Done/Deferred — so we MUST pass `--status` explicitly. It normalizes
  names, so `To Do` matches an existing `Todo`. It operates on an existing
  project; it does not create one — hence the `gh project create` step first.)
  Then query the field/option ids and write `.github/agent-loop.env`.
- **`setup_one_secret "PROJECTS_TOKEN" ...`** alongside the existing
  `CLAUDE_CODE_OAUTH_TOKEN` / `OPENAI_API_KEY` (hidden `gh secret set` prompt —
  user pastes the PAT; never echoed).
- **`--skip-board` flag** (parallels `--skip-workflows` / `--skip-secrets`).
- Update header/usage/`print_summary` prose (`:8-11,204,207,241-249,276-278`):
  Status now a board column; new label names; board + PROJECTS_TOKEN steps.

## Deliverable 3 — namespacing + board sweep across skills/docs

Pure find-and-replace of label names, plus swap status-label queries for board
reads. Representative edits:

- **`skills/executing-plans/SKILL.md`** — the column→label table (`:42-49`) becomes
  column→board-Status; create `:82` drops `--label status:todo` (issue enters via
  board To Do); candidate query `:99-101`
  (`--label "ready-for-agent" --label "status:todo"`) → filter on `dispatch:claude`
  AND board Status == To Do (via `gh project item-list`); claim `:105-109`
  `claimed`→`claim:active`; completion `:139-145` strips
  `status:todo,claimed,ready-for-agent`+adds `status:testing` → board `item-edit`
  Testing + remove `claim:active,dispatch:claude`; QA `:151-172` and daily queries
  `:208-226` reference board columns; claim-expiry `:191-272` `claimed`→`claim:active`.
- **`commands/loop.md`** — candidate `:28`, completion `:40-41`, rules
  `:10-12,20,25,50-54`; add **Step 0: `source .github/agent-loop.env`** so `/loop`
  has the board ids.
- **`.agents/SYSTEM/AI-DEV-LOOP.md`** — status described as a board column
  throughout; label table renamed (`:10-13,54-63,82-99,105,142-160,171,183,208-253`).
- **`skills/setup-agent-routing/SKILL.md`** (`:65,102-108,113,148-149,168`) +
  **`references/triage-labels.md`** (`:10-55`) + **`references/issue-tracker-github.md`**
  (`:15-16,26,31-32`): drop `status:*`, rename, add board `Status` map + record the
  project number.
- **`skills/writing-plans/SKILL.md`** `:176-177` — gate label names in the handoff
  note (`ready-for-agent`→`dispatch:claude`, etc.).
- **`feature`→`type:feature`** in: `skills/feature-intake/SKILL.md:308-309`,
  `skills/task-prd-creator/SKILL.md:123`,
  `skills/task-prd-creator/references/full-guide.md:217`.

**Exclusions — do NOT touch (different vocab, not dev-loop labels):**
`skills/agent-folder-init/assets/agent-configs/claude/commands/task.md:75` and
`validate.md:65` (their own backlog/in-progress/done/blocked/feature vocabulary);
`README.md` `/feature` (a slash command, not a label).

**Bundles are generated** — after editing any skill, regenerate, never hand-edit
`bundles/**` or `.claude-plugin/marketplace.json`:

```bash
bun run marketplace:generate
```

## Why dispatch stays a label (not a board field)

Workflows fire on `on: issues: [labeled]` and branch on
`github.event.label.name`. A Projects v2 `Status` change does not reliably emit a
repo `workflow`-triggering event, and `projects_v2_item` events are org-level and
awkward to gate per-repo. Keeping `dispatch:claude` / `dispatch:codex` as labels
preserves the existing one-line trigger and the human opt-in gate. Status moves to
the board; dispatch stays a label — by design.

## Verification

1. **Static gates** (all green):

   ```bash
   actionlint .github/workflows/*.yml
   bun run validate
   bunx markdownlint-cli <edited .md files>
   bash scripts/lint-shellcheck.sh
   bash -n scripts/setup-dev-loop.sh
   ```

2. **Blacksmith purged:** `grep -rn blacksmith .` → no matches.
3. **No stale labels in source:** `grep -rn "status:todo\|status:testing\|ready-for-agent\|ready-for-codex\|\bclaimed\b\|--label \"feature\"" skills commands .github .agents`
   → only intended hits (none in dev-loop paths).
4. **Bundles synced:** after `bun run marketplace:generate`, `git diff --stat`
   shows bundle copies match edited sources.
5. **Setup dry-run:** `bash scripts/setup-dev-loop.sh --dry-run` prints the new
   label set, the board-provision step, and the `PROJECTS_TOKEN` prompt — without
   mutating anything.
6. **Manual smoke (optional, real consumer repo):** run setup → board has
   Backlog/To Do/Testing/Done; labels renamed on existing issues; `agent-loop.env`
   populated; apply `dispatch:claude` to a To Do issue → workflow runs, claims with
   `claim:active`, on completion the board flips to Testing and `claim:active` clears.

## Riskiest steps (verify hardest)

1. **Board write from CI** — `item-edit` flags + `PROJECTS_TOKEN` scope. If the PAT
   lacks `project` scope the transition silently no-ops. Smoke-test on a throwaway
   issue.
2. **`gh project item-list` default limit 30** — must pass `-L 500` or large boards
   drop items from the candidate scan.
3. **Consumer-repo label migration ordering** — `gh label edit` (rename, preserves
   assignments) must run BEFORE seeding the new names, else duplicate-name errors.
4. **gh-project-board default columns** — must pass `--status "Backlog,To Do,Testing,Done"`
   or it provisions the wrong 6-option set.

## Files touched

| File | Change |
|------|--------|
| `.github/workflows/generate-bundles.yml` | runner → `ubuntu-latest` |
| `.github/workflows/agent-dispatch.yml` | runner; gate `dispatch:claude`; `PROJECTS_TOKEN`; board Testing write; `claim:active` |
| `.github/workflows/codex-dispatch.yml` | runner; gate `dispatch:codex`; `PROJECTS_TOKEN`; board Testing write; `claim:active` |
| `.github/agent-loop.env` | **new** — committed non-secret board ids |
| `scripts/setup-dev-loop.sh` | new LABELS; consumer-repo rename+delete; board provision via gh-project-board; `PROJECTS_TOKEN` secret; `--skip-board`; prose |
| `skills/executing-plans/SKILL.md` | board as status source; candidate query + transition rewritten; label renames |
| `skills/gh-project-board/scripts/setup-gh-project-board.mjs` | (called as-is; no change unless smoke reveals a gap) |
| `commands/loop.md` | Step 0 `source agent-loop.env`; board queries; label renames |
| `.agents/SYSTEM/AI-DEV-LOOP.md` | status = board column; label table renamed |
| `skills/setup-agent-routing/SKILL.md` + `references/{triage-labels,issue-tracker-github}.md` | drop status labels; board Status map; renames |
| `skills/writing-plans/SKILL.md` | gate label names in handoff note |
| `skills/feature-intake/SKILL.md`, `skills/task-prd-creator/SKILL.md` + `references/full-guide.md` | `feature` → `type:feature` |
| `bundles/**`, `.claude-plugin/marketplace.json` | regenerated via `bun run marketplace:generate` (never hand-edited) |
