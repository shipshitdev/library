---
name: interview
description: Conducts a repo-grounded discovery interview before PRD writing, feature intake, UX shaping, or implementation planning. Use when a user invokes /interview, asks to be grilled, wants requirements clarified, or needs a concise handoff brief from existing docs plus focused follow-up questions.
user-invocable: true
argument-hint: "[topic, feature, issue, or decision]"
metadata:
  version: "1.0.0"
  tags: "interview, discovery, requirements, planning"
  author: Ship Shit Dev
when_to_use: "interview me, grill me, grill-me, grill me with docs, discovery interview, requirements interview, before PRD, clarify requirements, /interview"
---

# Interview

Run a focused discovery interview before creating a PRD, writing a plan, shaping
UX, or starting implementation. Ground the questions in the repo first, then ask
only for decisions that cannot be inferred.

This skill does not write code, create issues, or produce a final PRD by default.
It produces an interview brief that downstream planning skills can consume.

## Contract

Inputs:

- Rough feature idea, issue number, product decision, bug class, or architecture
  question.
- Optional docs, links, transcripts, screenshots, or existing tracker context.

Outputs:

- Concise context scan summary.
- Focused question batches, no more than three questions at a time.
- Running assumptions, decisions, and open questions.
- Final interview brief ready for `prd-writer`, `feature-intake`, `shape`,
  `spec-first`, or direct implementation.

Creates/Modifies:

- None by default.
- May write tracker comments, PRD bodies, or memory files only when explicitly
  requested after the interview.

External Side Effects:

- None by default.
- Reads local repo context and, when needed, tracker or linked documentation.
- Writes external systems only after explicit approval.

Confirmation Required:

- Before creating or editing GitHub issues, PRDs, comments, memory files, or
  other durable artifacts.

Delegates To:

- `prd-writer` when the brief is ready to become a formal PRD.
- `feature-intake` when the brief should become GitHub issues or board items.
- `shape` when the main unknowns are UX, UI, interaction, content, or states.
- `spec-first` when the work is implementation-ready but still needs a durable
  technical spec.
- `prd-quality-gate` after a PRD exists and needs validation.

## When To Use

- A user asks for `/interview`, "grill me", "grill me with docs", or equivalent.
- A feature idea is too vague to turn directly into a PRD.
- Existing repo docs probably answer part of the question, but missing decisions
  still need the user.
- A planning agent would otherwise ask basic re-elicitation questions later.
- A user wants to decide whether the next step is PRD, design shaping, issue
  intake, or implementation.

Skip this skill when:

- The user already provided a complete PRD or issue with acceptance criteria.
- The request is a small, obvious edit and the user said to implement directly.
- The only missing context is discoverable from the repo with no user decision.

## Workflow

### 1. Ground In Repo Context

Read repo context before asking questions:

- Start with `.agents/README.md` when present.
- Read relevant `.agents/memory/` files, especially `.agents/memory/memory.md`,
  `.agents/memory/context.md`, and any task-relevant `.agents/memory/system/`
  docs.
- Check recent `.agents/sessions/` entries only when they are relevant to the
  topic.
- Read root agent entry files such as `AGENTS.md`, `CLAUDE.md`, or `CODEX.md`
  for routing and repo rules.
- Search docs, README files, source code, and issues for the topic before
  asking the user to repeat known context.

Do not look for a local plans directory under `.agents`; plans live on GitHub
issues and PR comments.
Use `writing-plans` when an implementation plan is needed.

When the user provides external docs or says "with docs", read only the relevant
sections and keep a short source list for the final brief.

### 2. State What Is Known

Before asking questions, summarize the context scan in three compact bullets:

- What the repo already says.
- What is still ambiguous.
- Which downstream artifact this interview is likely feeding.

If the repo gives enough context, ask for confirmation instead of running a long
interview.

### 3. Ask Focused Question Batches

Ask no more than three questions at a time. Prefer questions that unblock scope,
acceptance criteria, risk, or product decisions. Avoid asking implementation
questions unless the answer changes the scope or constraints.

Useful question areas:

- Problem: What pain, failure, or opportunity is this addressing?
- User: Who specifically experiences it, and in what workflow?
- Outcome: What must be true when this is done?
- Scope: What is version one, and what is explicitly out of scope?
- Constraints: Deadlines, platform limits, dependencies, data rules, security,
  accessibility, performance, or cost ceilings.
- Evidence: Existing examples, docs, customer requests, metrics, incidents, or
  screenshots.
- Acceptance: What would make a reviewer say this is complete?
- Risk: What would make the work fail or need human decision mid-flight?

After each user answer, update the working assumptions and ask the next smallest
set of questions.

### 4. Stop At The Right Time

Stop interviewing when one of these is true:

- The brief can feed the next skill without re-elicitation.
- Remaining questions are implementation details for the planner or executor.
- The user says "enough", "write it", "make the PRD", or equivalent.
- A blocker requires a separate research pass, stakeholder decision, or external
  access.

## Final Interview Brief

End with this structure:

```markdown
## Interview Brief: <topic>

### Context Read
- <files, issues, docs, or links used>

### Problem And User
<who has the problem, where it appears, and why it matters>

### Desired Outcome
<what must be true after the work ships>

### Version-One Scope
- <included behavior or decision>

### Non-Goals
- <explicitly excluded behavior or decision>

### Constraints And Dependencies
- <technical, business, timing, data, security, or UX constraints>

### Acceptance Signals
- <reviewable or testable completion signal>

### Risks And Open Questions
- <unresolved item, or "None">

### Recommended Next Step
<prd-writer | feature-intake | shape | spec-first | direct implementation>
```

Keep the brief concise enough to paste into a tracker issue or hand to a PRD
writer. Include inference notes when a fact came from repo context rather than
direct user confirmation.

## Anti-Patterns

- Do not dump a long questionnaire before reading repo context.
- Do not turn the interview into a PRD unless the user asks.
- Do not ask questions whose answers are already in `.agents/memory/`, root
  agent files, docs, code, or tracker context.
- Do not save plans in local agent plan files.
- Do not start implementation during the interview.
