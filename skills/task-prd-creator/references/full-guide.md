# Task & PRD Creator — Full Guide

## Workflow detection

| Situation | Output |
|-----------|--------|
| `gh auth status` OK + git remote is GitHub | GitHub issue (default) |
| No GitHub access | Local PRD in `.agents/memory/` |
| Both available | Ask user which, or both |
| No GitHub + no repo | Create `.agents/memory/` PRD, suggest `gh auth login` |

---

## PRD structure

Every PRD — whether GitHub issue body or local file — uses this structure.
Skip sections that don't apply. Never leave placeholder text in.

```markdown
## Problem

[What breaks, what's missing, why this matters. 2-4 sentences max.]

## Goal

[One sentence. Measurable. "Users can X without Y friction."]

## Scope

**In:**
- [specific thing 1]
- [specific thing 2]

**Out:**
- [explicitly excluded thing — prevents scope creep]

## Acceptance criteria

- [ ] WHEN [trigger] THE SYSTEM SHALL [observable response].
- [ ] WHILE [state] THE SYSTEM SHALL [response].
- [ ] IF [edge or failure condition] THEN THE SYSTEM SHALL [handled response].

## Technical notes

**Approach:** [Pattern to follow, key architectural decision]
**Risks:** [What could go wrong, unknowns]
**Dependencies:** [Other issues, external services, env vars needed]
**Files likely affected:** [rough list if known]

## Links

- Parent issue: #N (if sub-issue)
- Related: #N, #N
- Design: [Figma/Linear link if any]
```

---

## Agent brief structure

Use this when the issue is intended for an autonomous agent to implement.
The brief is the durable contract; prior comments and PRDs are supporting
context.

```markdown
## Agent Brief

**Type:** bug | enhancement | refactor | chore
**Mode:** AFK | HITL
**Priority:** critical | high | medium | low

## Current behavior

[What happens now. For bugs, name the broken user or caller behavior.]

## Desired behavior

[What should be true after this issue is complete. Include edge cases.]

## Key contracts

- `[public interface, endpoint, CLI command, config key, or data shape]`:
  [what must be preserved or changed]

## Acceptance criteria

- [ ] WHEN [trigger] THE SYSTEM SHALL [observable response].
- [ ] IF [edge condition] THEN THE SYSTEM SHALL [handled response].

## Verification

- [ ] [Exact command, manual check, or browser flow]

## Out of scope

- [Thing that should not be changed]
- [Adjacent feature that belongs in a separate issue]
```

Write from behavior to implementation. Do not include line numbers. Avoid file
paths unless the task is explicitly about a file path, generated artifact, or
configuration location.

---

## Vertical-slice issue breakdown

Break large work into independently grabbable slices:

```markdown
## Slice

**Mode:** AFK | HITL
**Blocked by:** None | #123
**User stories covered:** [short list]

## What to build

[One narrow end-to-end behavior, not a layer-by-layer task list.]

## Acceptance criteria

- [ ] WHEN [trigger] THE SYSTEM SHALL [demoable, mechanically verifiable result].

## Verification

- [ ] [Narrow command or review step]
```

Use `AFK` for issues an agent can complete from the written context. Use `HITL`
for issues that require product judgment, design approval, credentials, manual
access, legal/compliance review, or a human-only decision.

Prefer many thin issues over a few thick ones, but do not split so far that a
completed issue has no user, caller, or maintainer-visible result.

---

## Out-of-scope memory

When an enhancement is rejected as `wontfix`, preserve the decision if future
requests are likely:

```markdown
# [Concept Name]

## Decision

This project does not support [concept].

## Why this is out of scope

[Durable reasoning: project scope, technical constraint, strategy, or product
positioning. Avoid temporary reasons like "not this sprint".]

## Prior requests

- #123 - [short title]
```

Create one `.out-of-scope/<concept>.md` file per concept, not per issue. When a
new issue matches an existing rejected concept, surface the prior decision and
ask whether it still stands before closing or reopening the idea.

---

## Issue types and titles

Format: `[type]: [clear imperative title]`

| Type | When to use | Example |
|------|-------------|---------|
| `feat` | New capability | `feat: add CSV export to reports` |
| `fix` | Bug, broken behavior | `fix: auth token not refreshing on 401` |
| `chore` | Infra, deps, config | `chore: upgrade NestJS to v11` |
| `refactor` | Same behavior, different code | `refactor: extract payment service` |
| `perf` | Performance improvement | `perf: lazy load dashboard charts` |
| `docs` | Documentation | `docs: add API authentication guide` |

---

## GitHub issue creation

### Standard issue

```bash
gh issue create \
  --title "feat: add CSV export to reports" \
  --body "$(cat <<'BODY'
## Problem
Users need to export report data for external analysis. Currently only PDF is supported, which isn't usable in spreadsheets.

## Goal
Users can download any report as CSV in one click.

## Scope
**In:**
- CSV export button on report detail page
- All visible columns included
- Filename: `report-[id]-[date].csv`

**Out:**
- Scheduled/automated exports
- Custom column selection

## Acceptance criteria
- [ ] WHERE a report detail page is shown THE SYSTEM SHALL display an Export button.
- [ ] WHEN a user exports a report THE SYSTEM SHALL produce a valid CSV file with a header row.
- [ ] WHEN a report has 10k+ rows THE SYSTEM SHALL complete the export without timing out.
- [ ] IF a report has no rows THEN THE SYSTEM SHALL download a headers-only CSV.

## Technical notes
**Approach:** Stream response, don't buffer full dataset in memory
**Dependencies:** None
BODY
)" \
  --label "type:feature" \
  --assignee "@me"
```

### Sub-issue (part of epic)

```bash
# 1. Create the sub-issue
CHILD_ID=$(gh issue create \
  --title "feat: CSV export — streaming backend endpoint" \
  --body "..." \
  --json number --jq '.number')

# 2. Link it to parent epic #42
gh api repos/{owner}/{repo}/issues/42/sub_issues \
  --method POST \
  -f sub_issue_id=$CHILD_ID
```

Get `{owner}/{repo}` from:

```bash
gh repo view --json nameWithOwner --jq '.nameWithOwner'
```

### Update existing issue

```bash
# Add comment with update
gh issue comment 42 --body "Scope change: removing X, adding Y. See updated description."

# Edit body
gh issue edit 42 --body "$(cat updated-prd.md)"

# Close with reason
gh issue close 42 --comment "Shipped in #87"
```

---

## Local file format (optional)

Use when: no GitHub access, or user explicitly wants local tracking.

**PRD file:** `.agents/memory/[kebab-name].md`

Use the PRD structure from above. Add `# [Feature Name]` as h1. Include a `last_verified: YYYY-MM-DD` frontmatter field so the memory file stays auditable.

**File naming rules:**

- kebab-case only: `video-generation-with-captions.md`
- Full words, no abbreviations: not `vid-gen.md`
- No dates in filename (use metadata)

---

## Sub-issue sizing rules

A sub-issue should:

- Ship in one PR
- Be completable in 1 session (not 5 hours of work)
- Have its own acceptance criteria, independent of siblings
- NOT depend on an unmerged sibling

If you're writing a sub-issue that says "do X after Y is merged" — that's a dependency, list it. Don't assume order.

---

## When to push back on requirements

Stop and flag to user if:

- Acceptance criteria can't be tested (too vague)
- Scope includes 3+ unrelated things (split the issue)
- "Out of scope" section is empty on anything >medium complexity
- Breaking change with no migration path defined
- Security-sensitive and no threat model mentioned

---

## Quick reference

| Action | Command |
|--------|---------|
| List open issues | `gh issue list` |
| Search issues | `gh issue list --search "keyword"` |
| View issue | `gh issue view 42` |
| Create branch from issue | `gh issue develop 42` |
| Link sub-issue | `gh api repos/OWNER/REPO/issues/PARENT/sub_issues --method POST -f sub_issue_id=CHILD` |
| Close issue | `gh issue close 42 --comment "reason"` |
