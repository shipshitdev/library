---
name: prd-task-creator
description: 'Create a well-written PRD, task, or GitHub issue/sub-issue for a feature, bug, or enhancement. Use when planning work, writing GitHub issues, breaking down epics into sub-issues, or creating local task files. Common prompts: create a task, write a PRD, open a GitHub issue, create a sub-issue, plan this feature, write up this bug, break this down into issues, I want to add X, implement Y.'
disable-model-invocation: true
allowed-tools: Bash(gh *)
metadata:
  version: "1.2.0"
  tags: "tasks, prd, github, ears"
---

# PRD Task Creator

Write a clear, actionable PRD or task — output depends on where the user tracks work.

## Contract

Inputs:

- Feature, bug, enhancement, or planning request
- Destination preference: GitHub issue, local PRD/task file, or both
- Optional parent issue, labels, assignee, and priority

Outputs:

- Draft PRD or task body
- Destination-specific create command or file path
- Created issue/file URL or path after approval

Creates/Modifies:

- Local `.agents/memory/<kebab-name>.md` PRD files only after draft approval
- GitHub issues/sub-issues only after draft approval

External Side Effects:

- Reads GitHub issue state
- May create GitHub issues, sub-issues, or issue branches

Confirmation Required:

- Always show the draft before creating files or GitHub issues
- Ask before linking sub-issues or creating issue branches

Delegates To:

- `spec-first` when implementation constraints are still unclear
- `tdd` when the work should be executed test-first
- `gh-fix-ci` for CI failures after implementation
- `roadmap-analyzer` for roadmap-level planning
- `cto-advisor` for technical strategy and architecture tradeoffs

## Step 1: Detect workflow preference

Check in order:

1. User explicitly says "GitHub issue", "local file", or both
2. Check if `gh auth status` succeeds and a GitHub remote exists → GitHub available
3. If ambiguous, ask: "GitHub issue, local PRD file in `.agents/memory/`, or both?"

## Step 2: Understand the request

Ask only what's missing:

- What problem does this solve?
- Who's affected? (user-facing, internal, infra)
- Any hard constraints or dependencies?
- Is this part of a larger epic? (→ sub-issue)
- Priority: critical / high / medium / low

## Step 3: Research before writing

- Read relevant architecture docs in `.agents/memory/` (look for architecture, summary, or context files)
- Search codebase for related patterns
- Check for existing issues: `gh issue list --search "[keyword]"`

## Step 4: Write the PRD

See `references/full-guide.md` for the full PRD structure.

A good PRD has:

- **Problem** — why this exists, what breaks without it
- **Goal** — one sentence, measurable outcome
- **Scope** — what's in, what's explicitly out
- **Acceptance criteria** — EARS (`WHEN/WHILE/WHERE/IF … THE SYSTEM SHALL …`), testable, not vague
- **Technical notes** — approach, risks, dependencies

Acceptance criteria must be EARS-shaped and checkable by a human.

### Agent-ready issue rules

When the output is an issue for an autonomous or AFK agent, write it as an
agent brief, not a stream-of-consciousness plan:

- Describe behavior and contracts, not file-by-file instructions.
- Avoid line numbers and brittle file paths unless the path is itself the contract.
- Include current behavior, desired behavior, acceptance criteria, and out of scope.
- Name public interfaces, CLI commands, API shapes, config keys, or data contracts when known.
- Keep implementation notes as constraints, not a script the agent must follow.

### Vertical-slice breakdown

When breaking an epic, PRD, or plan into issues:

- Prefer thin vertical slices that produce a verifiable outcome.
- Mark each issue as `AFK` when an agent can complete it without more human input.
- Mark each issue as `HITL` when it needs a human decision, design review, credential, or product judgment.
- Publish blockers before blocked issues so dependencies can reference real issue IDs.
- Keep each sub-issue small enough for one focused PR.

## Step 5: Output to correct destination

### GitHub (primary if available)

**New issue:**

```bash
gh issue create \
  --title "[type]: clear title" \
  --body "$(cat <<'BODY'
[PRD content here]
BODY
)" \
  --label "type:feature" \
  --assignee "@me"
```

**Sub-issue** (linked to parent):

```bash
# Create sub-issue
gh issue create --title "..." --body "..." 

# Link as sub-issue to parent #N
gh issue develop N --checkout  # only if needed
# Use: gh api repos/{owner}/{repo}/issues/{parent}/sub_issues --method POST -f sub_issue_id={child_id}
```

**Draft PR from issue:**

```bash
gh issue develop [issue-number] --branch "feature/[name]"
```

### Local files (optional, or when no GitHub)

- PRD: `.agents/memory/[kebab-name].md`

See `references/full-guide.md` for local file templates.

## Step 6: Get approval before creating

Show the draft PRD. Wait for "looks good" or edits. Then create.

## Rules

- `disable-model-invocation: true` → only runs when user explicitly invokes
- Never create files or GitHub issues without user seeing the draft first
- Sub-issues should be small enough to ship in one PR
- If requirements are unclear, write the problem statement first — not the solution
- If rejecting an enhancement as out of scope, record durable reasoning in `.out-of-scope/<concept>.md` when the repo uses local out-of-scope memory.

## Related

- `spec-first` — spec-driven development before writing code
- `tdd` — red-green-refactor execution for tasks with clear behavior
- `gh-fix-ci` — fix CI on existing PRs
- `roadmap-analyzer` — broader roadmap planning
- `cto-advisor` — technical strategy and architecture tradeoffs
