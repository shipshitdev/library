---
name: no-comments
description: Review comments on a diff, delete narration and workaround sermons, fix accepted findings, and offer encodings for claimed constraints. Use before review or when asked to strip comments.
disable-model-invocation: true
license: MIT
metadata:
  version: "1.0.1"
  tags: "comments, review, cleanup"
  author: Ship Shit Dev
  source: https://github.com/cursor/plugins/blob/main/pstack/skills/no-comments/SKILL.md
  upstream_repo: cursor/plugins
  upstream_ref: main
  upstream_commit: bdf7aa355337
  last_synced: "2026-08-26"
  license: MIT
when_to_use: "no comments, strip comments, comment review before PR"
---

# No comments

Spawn a read-only comment reviewer. Act on accepted findings.

Authoring agents defend comments. Defer to a fresh reviewer that did
not write the code.

Companion to `comment-mode` (granular feedback on prose drafts) and
`deslop` (broader AI-artifact strip). This skill is the pre-review
comment pass.

## Contract

Inputs:

- The caller's files or diff. Otherwise the current diff against trunk,
  including the working tree.

Outputs:

- Deletion count, restored comments, reruns, fixes, encoding offers,
  and open work

Creates/Modifies:

- Deletes accepted comments and applies the smallest in-scope
  root-cause fixes

External Side Effects:

- None beyond local edits

Confirmation Required:

- Before encoding a constraint comment into a type, test, or lint
- Unattended runs require caller pre-approval for encodings

Delegates To:

- `how` or `why` when an `IMPORTANT` or `do not remove` comment is
  thin
- `architect` once, sketch only, when a fix needs a new shape

## Steps

1. Spawn a read-only review subagent on the fast cheap tier. Pass the
   scope and [references/comment-review.md](references/comment-review.md).
   Do not restate the rules.
2. Inspect the report. Reject application-code edits, scope escapes,
   exception-protected deletions, and flags that treat kept
   intentional code as guilty. A keep survives only with proof it is
   about something we cannot change. If a kill is ambiguous, do not
   restore. If a keep is refuted or still ambiguous, delete it. Revert
   and rerun one rejected report with the failure named. Reject a
   second and fail this skill.
3. Fix trivial accepted flags directly. If any fix needs a shape, run
   `architect` once for the accepted set and stop at the sketch.
4. Implement the smallest root-cause fix in scope. Remove every named
   workaround. If the root cause is out of scope, land the smallest
   in-scope fix and report the rest open.
5. Constraint comments (`do not remove`, `talk to X before changing`)
   stay when they are about things we cannot change. Offer the cheapest
   in-scope type, runtime, test, or CI lint. Wait for approval. If
   approved, encode then delete. Otherwise delete, report the
   constraint open, and sketch out-of-scope work.
6. Report the deletion count, restored comments, reruns, architect
   sketch, fixes, encoding offers, encodings, and open work.
