---
name: writing-prds
disable-model-invocation: true
description: Drafts, scopes, and formalizes features as PRDs — a planning agent can consume the output in one shot without re-elicitation. Triggers on "write a PRD for X", "let's plan X", "scope this out", "what should X do", or when a tracker issue needs to be fleshed out before planning. Do NOT use for code edits, debugging, or PR reviews.
metadata:
  version: "1.1.0"
  tags: "prd, planning, requirements, spec, github-issue, scoping"
---

# Writing PRDs

A PRD is the input contract for the planning phase. A good PRD lets a planning
agent produce a usable plan in one shot instead of burning turns asking "what did
you mean by X?". A bad PRD causes planner thrash, review rejection, and
verification failures downstream.

This skill is platform-agnostic. It assumes a plan → review → verify → ship flow
where a PRD is written first, a planner decomposes it into steps, and a verifier
checks the result against the PRD's acceptance criteria. Adapt the storage and
field mechanics below to whatever tracker you use.

## Storage Location

**Prefer making the tracker issue body the PRD.** One document per work item, one
location: the body of an issue in the project's tracker (a GitHub issue is the
recommended default). Avoid scattering PRDs across local sidecar files that drift
out of sync the moment work starts.

- **Create** a PRD by creating an issue whose body is clean PRD markdown.
- **Edit** a PRD by editing that issue's body.
- **Version history** is the tracker's edit history — no manual `updated` field.
- **The planner reads the issue body verbatim.** What you write in the body is
  exactly what the planning agent sees, so it must stand alone.

If there is no connected tracker, decide on the single canonical location for the
PRD before writing — do not draft into a throwaway scratch file that nobody will
find again.

## Native Tracker Metadata

Do not put YAML frontmatter at the top of issue bodies. Trackers render
issue-body frontmatter as visible noise and already have native fields for this
metadata.

Use native tracker / project-board fields instead:

- **Issue type:** `Feature`, `Bug`, or `Task`.
- **Status:** `Backlog`, `To Do`, `Testing`, or `Done`.
- **Priority:** `P0`, `P1`, `P2`, or `P3`.
- **Complexity:** `Low`, `Medium`, or `High`.
- **Blast radius:** `Contained`, `Cross-package`, `Cross-app`, or `Infra`.

Rules:

- The PRD body starts with `# PRD: <name>` and contains only human-readable PRD content.
- Put card/list summaries in the issue title, project fields, or a short Executive Summary, not in hidden metadata.
- If you cannot estimate complexity, set the field to `Medium` and explain why in Risks & Open Questions.
- `Draft` is workflow state, not body text. Keep draft PRDs off the runnable board path through status fields, not by editing the body.

## Issue Title Style

The issue title is what the board shows most of the time. Keep it short.

- Prefer **4-7 words** when possible.
- Prefer an **imperative verb + object** shape: `Add pipeline checkpoints`, `Track CI blockers on issues`, `Expose model selectors in settings`.
- Put the detail in the Executive Summary and body, not in the title.
- Avoid titles chained together with `and` / `while` / `during` unless the feature is truly one inseparable unit.
- Avoid titles that restate the full implementation loop. The title names the work item; the PRD explains it.
- Keep the `# PRD:` name aligned with the final issue title's slugified form. If you shorten the title, shorten the PRD heading too.

Bad:

- `Open draft PR during execution and ingest PR feedback into stabilization loop`
- `Treat CI failures as blocker state on GitHub issue tasks`

Better:

- `Add draft PR feedback loop`
- `Track CI blockers on issues`

## Required Sections

Every PRD must have these sections, in this order. Missing sections fail quality gate.

```markdown
# PRD: <name>

## Executive Summary
<2–4 sentences. What is this feature, why now, who wins.>

## Problem Statement
<The concrete pain. Reference real incidents, real users, real metrics where possible.
Avoid "users might want..." — if you can't name the user, you don't have a problem yet.>

## Goals
- <measurable, verifiable goal>
- <measurable, verifiable goal>

## Non-Goals
- <thing this explicitly does NOT do — the more you list, the less scope creep downstream>

## User Stories
- As a <role>, I want <capability> so that <outcome>.
- Each story ends with "**Acceptance:**" followed by 1–3 concrete checks.

## Functional Requirements
<Numbered list. Each item must be verifiable by reading code or running it.
NO implementation details — "the system must do X", not "use Zustand to do X".>

## Non-Functional Requirements
<Performance, accessibility, error-handling, offline, observability.
Only list the ones that actually matter for this feature.>

## Success Criteria
<The bar the verification phase will check against.
Every bullet here becomes an acceptance criterion the verifier asserts on.
Write them like test assertions.>

## Out of Scope
<Be ruthless. Future-proofs the review phase against scope creep.>

## Dependencies
<Other PRDs, packages, external APIs, feature flags. Reference by path or URL.>

## Verification Plan
<How the verifier will know this shipped correctly.
`tests`: list the test files/suites that must exist and pass.
`manual`: list the manual QA steps a human will run post-merge.
`both`: both sections. The clearer this section, the fewer verification retries you burn.>

## Risks & Open Questions
<Unknowns, edge cases, things that could kill the plan mid-execution.
Open questions get tracked here until answered, then deleted.>
```

## Mapping PRD Sections to the Plan

A PRD is read by the planning agent. Every section has a downstream consumer:

| PRD section | Feeds | Consumer |
|---|---|---|
| Executive Summary | Plan objective | Plan display, PR title, board card |
| Goals + Functional Requirements | Plan steps | Planner decomposition |
| Success Criteria | Acceptance criteria | Verification phase |
| Out of Scope | Plan out-of-scope list | Review phase (rejects scope creep) |
| Complexity field | Estimated complexity | Review rubric, retry budget |
| Verification Plan | Verification prompt input | Verification phase |
| Non-Goals + Out of Scope | Review gate | Reviewer rejects patches that violate these |

**Do not write sections that describe files to change, function names, or implementation choices.** Those belong in the plan, not the PRD. If you can't resist writing pseudo-code, put it under "Risks & Open Questions" as "I suspect we'll need to touch X" — not as a requirement.

## Quality Gates

Before marking a PRD ready for a planner to consume, every one of these must be true:

- [ ] No placeholder text (`TODO`, `TBD`, `<fill this in>`) remains in any section.
- [ ] `Goals` has at least one measurable bullet.
- [ ] `Success Criteria` has at least one bullet, and every bullet is **verifiable without judgement** — it either passes or fails. "Feels fast" is not verifiable. "p95 latency < 300ms on the issues query" is.
- [ ] `Out of Scope` has at least one bullet. Empty `Out of Scope` is a tell that the author didn't scope the feature.
- [ ] `User Stories` has at least one story with explicit Acceptance bullets.
- [ ] Every external dependency in `Dependencies` is named (package, PRD path, or URL), not described vaguely.
- [ ] `Verification Plan` names either test file paths, suite names, or concrete manual steps — not "write some tests".

If any gate fails, keep it in draft/on-hold workflow state and do not mark it ready to plan.

## Workflow

### When the user says "write a PRD for X"

1. **Confirm where the PRD will live.** If using a tracker, confirm the target repo/project. If nothing is connected, agree on the single canonical location first — there must be exactly one.

2. **Do not start writing immediately.** Run a short elicitation pass first — you need answers before section-filling is meaningful:
   - What problem does this solve, and for whom specifically?
   - What does success look like — how would we measure it?
   - What is explicitly out of scope?
   - What's the complexity gut feel (low/medium/high) and why?
   - Any hard constraints — deadlines, other projects in flight, package boundaries?

3. **Check for an existing issue.** If using GitHub, run `gh issue list --search "<keywords>" --state all` in the target repo. If a matching issue already exists, ask whether to edit it or create a fresh one.

4. **Kebab-case the PRD name.** If the proposed name has spaces, camelCase, or punctuation, kebab-case it: `"Notification Center"` → `notification-center`. This slug goes in the `# PRD:` heading.

5. **Compress the issue title before writing the body.** Default to a short imperative title, then derive the `# PRD:` heading from that final title. Put nuance in the Executive Summary, not the title.

6. **Draft the PRD body** using the template above, in a scratch buffer. Fill every required section. If you can't fill a section, ask the user — don't hallucinate requirements.

7. **Run the quality gates** against the draft. If any fail, keep the issue in draft/on-hold workflow state and tell the user which gates failed. If they all pass, mark it ready through native project state.

8. **Create the issue (with user approval).** Show the drafted body first. On approval, create it — e.g. `gh issue create --title "<Human Readable Title>" --body-file -` with the PRD markdown piped on stdin.

9. **Confirm the outcome** to the user with the issue URL. Suggest the next step: "Ready to hand this to the planner? Say: plan issue #N".

### When the user says "plan the X PRD"

1. Fetch the current issue body (e.g. `gh issue view <N> --json body --jq .body`). Read it fully before producing anything.
2. Verify the issue is ready through native project state — never plan a draft/on-hold issue.
3. Translate directly: Executive Summary → objective, Success Criteria → acceptance criteria, Out of Scope → out-of-scope, complexity field → estimated complexity.
4. The plan phase owns file changes and step breakdown — do not copy those out of the PRD (there shouldn't be any).
5. The resulting plan is posted back as a `## Implementation Plan` comment on the same issue (see `writing-plans`) — it lives on the issue, not in a local file, so it stays in sync with the PRD and reaches the loop.

### When the user says "update the X PRD"

1. Fetch the current issue body (prefer the tracker's live read to guarantee freshness).
2. Make the requested edit in a scratch buffer.
3. Write it back (e.g. `gh issue edit <N> --body-file -`). The tracker records the edit history automatically.
4. If the change invalidates an in-flight plan (new acceptance criterion, new out-of-scope item), flag that explicitly — the user may want to kill the thread and re-plan.

## Anti-Patterns

Observed failure modes — do not repeat:

- **PRD full of implementation details.** Writing `use TanStack Query v5 for caching` in Functional Requirements. The PRD describes the *what*; the plan owns the *how*. This leaks into review and causes the reviewer to flag the plan for violating the PRD, which the planner then "fixes" by copying the implementation detail verbatim. Dead loop.
- **Success Criteria written as vibes.** "Users should find the flow intuitive." Unverifiable → verification retries forever.
- **Empty Out of Scope.** Always a sign the author is planning to sneak scope in later. Force the listing.
- **Authoring a PRD with nowhere to put it.** If there's no agreed canonical location, the PRD becomes an orphan document that drifts out of sync. Decide the location first.
- **Editing a cached copy instead of the source.** If your tracker caches issue bodies locally, the cache is downstream of the tracker, not upstream. Always edit via the tracker's API/CLI, never the cache.
- **Creating an issue without running the quality gates first.** Half-formed PRDs thrash the planner and burn verification retries. Running gates after the issue is already public is embarrassing and harder to fix than running them first.
- **Writing a PRD for something you should just ticket.** A typo fix does not need a PRD. A dependency bump does not need a PRD. Reserve PRDs for features and architectural changes that will run through plan / review / verify / ship.

## Minimal Example

The text below is the exact issue body to push (e.g. `gh issue create --body-file -`). Tracker metadata belongs in native fields, not in this body.

```markdown
# PRD: copy-issue-url-action

## Executive Summary
Users working in the board frequently need to paste an issue URL into chat,
commit messages, or an external ticketing tool. Today the only way to get the
URL is to click into the issue, then copy from the header — three clicks and
a context switch. Add a "Copy URL" action to the card's context menu so it
takes one click.

## Problem Statement
Observed on 2026-04-09: the user mentioned needing to paste an issue URL
into a chat thread five times in a single session, each requiring a detour
through the issue detail view. This is pure friction — the URL is already known.

## Goals
- Right-clicking a board card shows a context menu with "Copy URL".
- Clicking "Copy URL" writes the issue's URL to the clipboard and
  shows a toast confirming the copy.

## Non-Goals
- Copying anything other than the URL (title, body, ID — all separate actions
  if demand appears).
- A multi-select "copy all URLs" bulk action.
- Keyboard shortcut for copy — mouse-only for v1.

## User Stories
- As a developer pasting issue links into chat, I want to copy an issue's
  URL without leaving the board, so that I don't break my flow.
  **Acceptance:**
  - Right-click on a card surfaces a context menu including "Copy URL".
  - Clicking it results in the URL being on the system clipboard.
  - A toast appears within 200ms confirming the copy.

## Functional Requirements
1. The card component must support a right-click context menu.
2. The context menu must include an action labeled "Copy URL".
3. The URL written to the clipboard must be the canonical issue URL.
4. The toast notification must use the existing UI toast primitive.

## Non-Functional Requirements
- Clipboard write must succeed or fail cleanly — no silent failures. On
  permission denial, surface an error toast.

## Success Criteria
- Right-clicking any card opens a context menu with a "Copy URL" item.
- Clicking "Copy URL" puts the exact canonical issue URL on the clipboard.
- A success toast appears when the copy succeeds.
- An error toast appears if the clipboard API rejects the write.

## Out of Scope
- Copying other fields (title, body, branch name).
- Bulk selection + copy.
- Keyboard shortcut bindings.
- A "Share" action that opens the URL in the browser.

## Dependencies
- The existing UI toast primitive in the project's component library.
- The issue number and repo identifier for URL construction.

## Verification Plan
- **tests:** add a test that simulates a right-click and asserts the context
  menu includes a "Copy URL" item wired to a mocked clipboard write.
- **manual:** right-click three cards from different projects, paste the
  clipboard into a browser tab, verify the URL loads the correct issue.

## Risks & Open Questions
- Which clipboard API does the renderer use today? Check the existing
  implementation before writing new clipboard code.
- Do we need focus-management so the context menu doesn't fight with
  drag-and-drop handlers on the same card?
```

Note: no `created`, `updated`, `status`, `complexity`, or `blast radius` fields in the body — the tracker and project board track those natively. No file path — the PRD lives in the issue body itself.
