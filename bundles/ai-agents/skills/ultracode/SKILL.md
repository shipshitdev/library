---
name: ultracode
description: >-
  Routes maximum-depth coding requests to the harness's native deep mode
  instead of reimplementing orchestration in prompt policy: Claude Code's
  built-in ultracode multi-agent orchestration, or Codex's native `ultra`
  reasoning effort (GPT-5.6+), falling back to a manual workflow only where no
  native mode exists. Use when invoked with $ultracode, /ultracode,
  "ultracode", "ultra effort", "maximum-depth", "split across agents",
  "parallel agents", or "deep autonomous implementation" on a non-trivial
  coding task.
compatibility: Claude Code or Codex CLI. Native ultra effort requires a GPT-5.6+ model with ultra access enabled on the account; older setups use the legacy workflow in references/.
metadata:
  version: "2.0.0"
  tags: "orchestration, subagents, autonomy, deep-mode, effort"
  author: Ship Shit Dev
---

# Ultracode

Deep, high-autonomy execution is a **native harness capability** now. This
skill routes to the native mode; it no longer supplies a hand-rolled
orchestration workflow. (v1 of this skill was a manual Codex workflow written
before Codex had a native deep mode — it survives as the fallback in
`references/legacy-workflow.md`.)

## Routing

| Harness | Native deep mode | How to engage |
|---|---|---|
| Claude Code | ultracode multi-agent orchestration | Include the keyword "ultracode" in the prompt (per-turn opt-in) or enable it for the session. The harness plans, fans out subagents, verifies, and synthesizes natively. |
| Codex, GPT-5.6+ | `ultra` reasoning effort — native parallel subagent orchestration | Pick ultra via `/model`, or set `model_reasoning_effort = "ultra"` in `config.toml`. Pair with a rollout token budget (e.g. `rollout_token_budget = 500000`) — ultra consumes materially more tokens per turn. |
| Codex without ultra access, or pre-5.6 model | none | Use the strongest available effort (`xhigh`) and follow `references/legacy-workflow.md`. |

Ultra access note: ultra effort is rolling out per account. If setting it is
rejected, do not fake it — fall back to the last row and say so.

## Rules

- **Never reimplement the native mode in prompt policy.** If the harness has a
  deep mode, engage it and get out of its way. The legacy workflow exists only
  for harnesses that lack one.
- **Deep mode is not a substitute for completion criteria.** State the
  objective, constraints, and "done when" evidence explicitly — native
  orchestration decides *how* to work, not *what done means*. On Codex, pair
  ultra with `/goal` for long-running work.
- **Cost gate.** Native deep modes multiply token spend. Reserve them for
  genuinely hard, parallelizable work — wide-open design questions, broad
  audits, migrations, risky-diff reviews. A single-file fix never needs them.
- **Side-effect policy is unchanged.** Deep mode grants no extra permission:
  no commit, push, publish, deploy, or production changes unless the user
  explicitly requested that side effect.

## Prompt shape (either harness)

```text
Objective: <one durable outcome>
Constraints: <what not to change>
Context: <files/docs/issues/logs to inspect first>
Done when: <tests/checks/artifacts that prove completion>
```

## Delegates To

- `multi-agent-patterns` when packet boundaries or topology are unclear
- `qa-reviewer` for final independent verification
- `references/legacy-workflow.md` when no native deep mode is available
