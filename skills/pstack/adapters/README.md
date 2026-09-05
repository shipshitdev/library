# Optional Pstack adapters

These files are inert installed resources. Installing the skill does not register
hooks, models, agents, routines or servers. The user-invoked `setup-pstack` workflow configures a harness when requested. Resolve this directory from the installed pstack
skill, and preserve the harness's canonical role sheet and generator.

## Session startup and agents

`hooks/session-start` prints `hooks/session-start-context.md`. For a harness
supporting a command hook, register its absolute installed path only after setup
authorization. The supplied hooks JSON is a rendering template: replace
`SHIPSHIT_PSTACK_ADAPTERS` with the actual installed adapters directory before
registration. Windows users can use the included polyglot launcher. Check the
generated command against the actual shell and harness.

Agent Markdown files are templates. Bind the configured role's model and effort
through the harness's native settings; the templates inherit unless explicitly
configured. Preserve names only where a role registration needs them. The single configured-role template supports each named role without requiring
multiple configured model families.
The comment reviewer template and general engineering template provide distinct
prompts; both resolve canonical skills through the active catalog.

## Benny issue automation

The Cursor adapter includes setup, report triage, reproduction/fix workflows,
configuration and prompt templates under `cursor/automations/benny/`.
Read those three procedure files before configuring a workflow. Confirm the
target repository, issue labels, routing, available issue/comment tools and
execution host. Bind project and schedule in the automation app, not the prompt.
Default new instances to reporting. Writes, external messages and merges require
a routine policy explicitly authorizing those actions. Preserve issue deduplication
and existing-fix verification from the reproduction resources.

On another harness, map each required capability to its supported automation and
issue interfaces and verify a report-only run first. If the harness cannot supply
the required trigger or authenticated issue interface, leave it dormant and
report the gap. Do not claim operational parity from copied prompts.

## Bot UI

`cursor/make-bot-ui.md` describes Cursor's webhook routine and secret-request
interfaces. Use it only where those interfaces are actually present. First confirm
authorization to create the routine, store its server-side secret, host the page
and expose it to the named network. Never put the sender key in chat, browser
bundles, logs or committed files. Validate webhook input and expose only the
selected actions. Probe with a harmless payload before declaring it live.

For another harness, require equivalent webhook and secure secret-entry support.
If either is unavailable, report the missing capability instead of inventing tools
or falling back to a public unauthenticated endpoint.

## Runtime path audit

The external runner requires explicit prompt, cwd, output and receipt paths.
The orchestration store requires `--store` or `ORCH_STORE`; it has no home-directory
default. The decision-log helper requires its logfile argument. The launchers call the
bootstrap library to install locked dependencies beside the installed runtime;
bootstrap is not a standalone command. Installation needs write permission there
and runs only on the authorized host.

The upstream worktree-audit script is superseded by canonical `git-cleanup`.
Its original source remains in the immutable upstream snapshot for review. Resolve
the installed cleanup skill's `scripts/cleanup.py` for candidate inventory and
immutable merge proof, and use the active harness session interface for in-use
checks. Read-only disk tools can report size without becoming deletion authority.
