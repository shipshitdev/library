---
name: setup-agent-routing
description: Sets up an `## Agent skills` routing block in CLAUDE.md/AGENTS.md plus docs/agents/ so the dev-loop skills (executing-plans, feature-intake, prd-writer, qa-reviewer) know this repo's GitHub issue tracker, kanban label vocabulary, and domain doc layout. Run once per repo before first use of the loop, or when those skills appear to lack tracker, label, or domain context.
license: MIT
metadata:
  version: "1.1.0"
  tags: "setup, routing, github, labels, dev-loop"
  author: Ship Shit Dev
allowed-tools: Bash(git remote*) Bash(gh label list*) Bash(gh project list*) Bash(gh repo view*)
disable-model-invocation: true
---

# Setup Agent Routing

Write a machine-readable routing block so the dev-loop skills know where this repo tracks work, which labels drive the loop, and how its domain docs are laid out. Run once per consumer repo; bridges `executing-plans`, `feature-intake`, `prd-writer`, and `qa-reviewer` into a new repo.

Prompt-driven, not deterministic. Explore first, present findings, confirm each decision, show drafts, then write. Never write speculatively.

## Contract

Inputs:

- Target repository: its git remote, existing `CLAUDE.md` / `AGENTS.md`, and `docs/agents/`
- Existing label vocabulary and GitHub Projects board, read live via `gh`
- User overrides for label strings, the project board number, and the domain layout

Outputs:

- A draft `## Agent skills` routing block
- Draft `docs/agents/{issue-tracker,triage-labels,domain}.md` files seeded from `references/`
- A short summary of present vs. missing routing state

Creates/Modifies:

- Writes the `## Agent skills` block into `CLAUDE.md` (preferred) or `AGENTS.md`, in place
- Creates `docs/agents/*.md` from the reference seeds, updating in place when they already exist
- Never creates a second routing file when one already exists, and never duplicates the block

External Side Effects:

- Reads git remote, GitHub labels, and project boards via read-only `gh` calls
- Writes local files only; performs no GitHub mutations

Confirmation Required:

- Before writing the routing block or any `docs/agents/` file
- Before choosing `CLAUDE.md` vs. `AGENTS.md` when neither exists

Delegates To:

- `executing-plans`, `feature-intake`, `prd-writer`, and `qa-reviewer` consume the
  routing block this skill writes — it produces their machine-readable context, then hands off

## What it produces

1. An `## Agent skills` block in `CLAUDE.md` (preferred) or `AGENTS.md`.
2. Three docs under `docs/agents/`:
   - `issue-tracker.md` — how issues are created, labeled, and placed on the board.
   - `triage-labels.md` — full label vocabulary, including `dispatch:claude`/`dispatch:codex`/`dispatch:openrouter` execution gates and the `dispatch:plan` planning gate (status lives on the board, not a label).
   - `domain.md` — the domain glossary layout (single- or multi-context).

The `CLAUDE.md`/`AGENTS.md` block is a thin index; detail lives in `docs/agents/`.

## Process

### 1. Explore (read-only, assume nothing)

```bash
git remote -v
gh repo view --json nameWithOwner,defaultBranchRef 2>/dev/null
gh label list --limit 100 2>/dev/null
gh project list --owner "@me" 2>/dev/null
```

Also read, if present: `CLAUDE.md`, `AGENTS.md`, `CONTEXT.md`, `CONTEXT-MAP.md`,
`docs/agents/`, `docs/adr/`. Note what already exists vs. what is missing — you will
update in place, not duplicate.

### 2. Present findings, then confirm — one decision at a time

Summarize present/missing state in one short block. Walk the three decisions **individually**, each prefaced by a plain-English explainer. Do not present all three at once.

**A. Issue tracker.** Default: GitHub Issues + a GitHub Projects kanban
(Backlog / In Progress / Human Review / Done / Deferred), detected from the `origin` remote. Confirm the
repo `owner/name` and the project board number. If the remote is not GitHub, ask
how work is tracked instead of assuming.

**B. Label vocabulary.** Show the canonical set (below) and let the user override the
strings. The roles are fixed; the exact label text is theirs to rename.

Status is the board `Status` field (Backlog / In Progress / Human Review / Done / Deferred), the sole
source of truth — it is **not** a label. The labels that ride alongside it:

| Label | Role |
| ----- | ---- |
| `claim:active` | An agent currently holds the issue (30-min claim lock). |
| `loop:planning` / `loop:executing` / `loop:testing` / `loop:shipping` | AI-loop sub-phase inside the In Progress column (observability). |
| `priority:high` / `priority:medium` / `priority:low` | Queue ordering. |
| `rejection:N` | QA rejection count; bumped on each kickback. |
| `dispatch:plan` | **Planning gate → drafts a plan for human review.** Human opt-in: runs `writing-plans`, posts a `## Implementation Plan` comment, stops at Human Review. Applies no execution gate. |
| `dispatch:claude` | **Dispatch gate → Claude lane.** Human opt-in: the agent only runs on issues that carry it. |
| `dispatch:codex` | **Dispatch gate → Codex/GPT lane.** The Codex-lane twin; apply at most one gate per issue. |
| `dispatch:openrouter` | **Dispatch gate → OpenRouter lane.** Hosts Codex CLI via OpenRouter; apply at most one gate per issue. |
| `type:feature` | Created by `feature-intake` on PRD epics and sub-issues. |

Also explain the **AFK / HITL** body markers (not labels): `AFK` = an agent can
finish from written context; `HITL` = a human decision is required. HITL issues must
never receive any dispatch gate — neither the execution gates (`dispatch:claude`,
`dispatch:codex`, `dispatch:openrouter`) nor the planning gate (`dispatch:plan`).

**C. Domain docs layout.** Single-context (`CONTEXT.md` at root) vs. multi-context
(`CONTEXT-MAP.md` indexing several `CONTEXT.md` files). Default to single-context for
a solo or single-product repo.

### 3. Show drafts, allow edits

Render the full `## Agent skills` block and all three `docs/agents/*.md` files. Let
the user edit label strings, the project number, and the domain layout before
anything is written.

### 4. Write — only after approval

File-selection rules (copied from the conventions that make this safe):

- If `CLAUDE.md` exists → edit it.
- Else if `AGENTS.md` exists → edit it.
- If neither exists → ask which to create. Never pick for the user.
- Never create the second file when one already exists.
- If an `## Agent skills` section already exists → update it in place, do not append a duplicate.
- Seed `docs/agents/*.md` from the templates in `references/`. If a file already exists, show a diff and update in place.

## The `## Agent skills` block

```markdown
## Agent skills

### Issue tracker

GitHub Issues + GitHub Projects kanban (Backlog / In Progress / Human Review / Done / Deferred) on
`<owner>/<repo>`, project #<N>. See `docs/agents/issue-tracker.md`.

### Triage labels

`claim:active` · `loop:*` (AI-loop phases) · `priority:*` · `rejection:*` ·
`type:feature` · `dispatch:plan` (planning gate) · `dispatch:claude` (Claude gate) ·
`dispatch:codex` (Codex gate) · `dispatch:openrouter` (OpenRouter gate). Status is the
board `Status` field, not a label. See `docs/agents/triage-labels.md`.

### Domain docs

<single-context | multi-context>. See `docs/agents/domain.md`.
```

## References (template seeds)

- `references/issue-tracker-github.md` — the `gh` / `gh project` command vocabulary and the column→label map.
- `references/triage-labels.md` — the full label table and AFK/HITL markers.
- `references/domain.md` — single- vs multi-context glossary layout.

## Rules

- Never write any file before the user approves the drafts.
- Update in place; never duplicate an existing `## Agent skills` block or `docs/agents/*.md`.
- Keep the `CLAUDE.md`/`AGENTS.md` block as a thin index — detail lives in `docs/agents/`.
- `dispatch:plan` (planning) / `dispatch:claude` / `dispatch:codex` / `dispatch:openrouter` (execution) are the human opt-in gates. HITL issues never carry any of them.
- Do not invent a project board number — read it live with `gh project list` or ask.
