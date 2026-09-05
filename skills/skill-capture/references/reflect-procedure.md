## Distribution boundary

Use the active Shipshit skill catalog and the caller's existing authorization.
The harness owns host, account, model, effort, sandbox, worktree and schedule.
Upstream examples describe mechanisms; they do not grant permission or select
providers. Preserve report-only scope. External messages, publication, installs,
deployment and destructive actions require authorization covering that action.
Read configuration from the harness source of truth; never replace its role map
with an example here. Use only capabilities the active harness actually exposes.

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

**Dispatch contract.** Resolve every configured role through `provider-dispatch.md` (resolve the `pstack` skill through the active catalog). Reviewers need the parent's live MCP surface, so the default and supported portable route is `inherit-parent` (or its `auto` alias). Pass the transcript or digest plus any required evidence paths. On Codex, resolve remaining Claude tool names via `codex-tools.md` (resolve the `pstack` skill through the active catalog).

## When to invoke

- The user said "reflect" or "/reflect".
- A complex task (5+ tool calls) just landed cleanly and the recipe is worth keeping.
- The agent hit dead ends, found the working path, and the path generalizes.
- The user corrected the agent's approach mid-task.
- A non-trivial workflow emerged that isn't captured anywhere.

Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## Process

### 1. Locate the active transcript

Resolve the current session record through the active harness session interface or
its configured workspace-scoped transcript root. Confirm the session ID, repository
and opening request before reading. Use the provider's documented event schema;
do not assume JSONL layout or a particular message field. Never search unrelated
workspaces or substitute another provider's history.

Pass reviewers the exact session record, approved transcript path or a tightly
scoped digest. If the full record is unavailable, label that limitation and use
the digest instead of claiming transcript-backed verification.

### 2. Spawn three reviewers in parallel

Start all three read-only lanes in one fan-out phase through provider dispatch. Reviewers need MCP access for context lookups (tickets, chat threads, observability traces referenced in the transcript), so keep them native to the parent. The prompt forbids file writes; the parent applies edits.

| Lens | Model descriptor | Prompt template |
|---|---|---|
| Judgment | your configured reflect-judgment choice (default `inherit-parent`) | `references/judgment-reviewer.md` |
| Tooling | your configured reflect-tooling choice (default `inherit-parent`) | `references/tooling-reviewer.md` |
| Divergent | your configured reflect-judgment choice (default `inherit-parent`) | `references/divergent-reviewer.md` |

Pass each template verbatim, substituting the transcript path or digest where marked. Reviewers return findings in the `Agent` response body.

### 3. Synthesize

Dispatch one lane using your configured reflect-judgment descriptor (default `inherit-parent`). Preserve relevant MCP access because the synthesizer spot-verifies citations. Use `references/synthesizer.md` verbatim, with each reviewer's full output inlined where marked. The synthesizer returns a structured Accepted / Rejected / Backlog list.

### 4. Structural enforcement check

Sanity-check the synthesizer's Accepted list. For any item that would be enforced more reliably by a lint rule, script, metadata flag, or runtime check, move it from Accepted to Backlog. The synthesizer already applies this criterion; this is a final pass before edits land. See the **encode-lessons-in-structure** principle skill.

### 5. Apply

Present the synthesizer's Accepted/Rejected/Backlog output. Apply only skill edits already covered by the user's capture request and the harness's authority rules. If capture was suggested after a session without a request to persist it, leave the proposals as a report. Ask before any consequential scope expansion or unresolved routing choice.

Create backlog issues only when tracker writes are already authorized. Otherwise include them as proposals in the report.

For each approved Accepted item, follow the Routing field exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): parent does directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): hand to the **skill-creator** skill and run its draft / test / iterate loop.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): hand to `skill-creator` and run its description-optimization loop.
- `new skill via skill-creator: <kebab-name>`: hand creation to `skill-creator`. Do not invent the shape ad hoc.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done. Skip this step if it doesn't.

### 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog filed to the devex tracker: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
