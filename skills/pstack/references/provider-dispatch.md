# Provider dispatch

The active harness owns the role map, account, model, requested effort, permitted
providers, workspace and execution host. Read its canonical configuration before
launching a role. Preserve existing choices, including generated adapters with a
separate source of truth. This distribution ships no default model assignments.

## Descriptor contract

A configured external lane supplies an explicit provider, model and requested
effort. The launcher requires every value; it never chooses a weaker fallback.
Resolve role aliases in the parent. Pass the resulting values as separate argv
entries, never interpolate them into shell code. Keep credentials in the provider
CLI's existing account configuration. Never copy authentication between hosts.

## Routes

| Parent | Same provider | Different supported provider |
|---|---|---|
| Claude | Native agent with the configured model and effort | External launcher |
| Codex | Native agent with the configured model and effort | External launcher |
| Other harness | Its documented native delegation | Report unsupported launcher parent |

The bundled launcher supports Claude, Codex and Grok children. It rejects a child
whose provider matches its parent. Native execution must retain task boundaries
and tool limits. Mixed panels use only providers explicitly authorized by the user.
If one is unavailable, report that lane as dropped; preserve the intended evidence
coverage and do useful remaining work without silently substituting a provider.

## External launcher

Resolve the installed pstack directory and run
`scripts/runner/pstack-runner --help`. Supply `--parent`, `--provider`,
`--model`, `--effort`, `--mode`, `--prompt`, `--cwd`, `--output` and
`--receipt` from the authorized task and harness configuration.

Modes are `read-only` and `isolated-write`. The harness must enforce host and
filesystem restrictions; the runner is not an operating-system sandbox. In
particular, Claude plan mode and tool exclusions do not make shell execution a
security boundary. Use read-only credentials and a real sandbox where required.
Give each writer its own harness-selected worktree. Pass `--timeout` only when
the task supplies a deadline. The default has no implicit timeout.

The runner checks CLI availability and credentials, captures output in exclusive
files and writes a receipt with status, requested argv, reported model, timings
and available usage. Inspect both the receipt and resulting artifact. A successful
process is not proof of task success. Receipts prove requested effort, not hidden
provider reasoning depth. A model/account probe is billable; run it only for a
user-selected lane within the task budget.

## Packaged tools

- `scripts/bootstrap.ts` installs this runtime's locked dependencies.
- `scripts/watch-pr/watch-pr` observes and drives a PR using its selected mode.
- `scripts/orch/orch.ts` manages the local orchestration state store.
- `scripts/check-plan.mjs` checks the multi-phase plan contract.
- Worktree inventory and cleanup use the canonical `git-cleanup` skill's
  `scripts/cleanup.py` helper, resolved through that skill's installed directory.
  The old audit script is superseded; no second cleanup runtime ships here.

Read each tool’s CLI contract before use and preserve the caller’s mutation scope.
The plan checker accepts `node scripts/check-plan.mjs <plan.md>`; it has no
`--help` option. Other entrypoints expose `--help`.
Runtime installation and execution happen only on the harness-approved host.
