# Codex capability mapping

Resolve actions against the tools actually exposed by the active Codex harness.
Desktop, CLI and hosted sessions can expose different names and permissions.
This reference maps behavior; it does not enable features or change configuration.

## Actions

| Workflow action | Execution requirement |
|---|---|
| Read or search files | Use the available filesystem or command interface within the authorized workspace. |
| Edit files | Use the harness editing interface within the requested mutation scope. |
| Fetch or search external information | Prefer the available connector or web interface and preserve its restrictions. |
| Invoke another skill | Resolve the canonical Shipshit entry through the active catalog and read its installed resources. |
| Delegate independent work | Use exposed, authorized native delegation and its actual model and effort controls. |
| Wait for a delegate | Retain the returned handle and use the corresponding wait/status interface. |
| Release a delegate | Use a supported lifecycle operation if one exists; do not invent a close tool. |
| Track work | Use the available plan/task interface or a scoped written checklist. |
| Ask a structured question | Use the available question interface; otherwise ask a concise plain-text question. |

Loading a skill grants no authority to change a sandbox, enable delegation,
register a plugin, schedule work or select another provider.

## Native and external roles

Read [provider dispatch](provider-dispatch.md) and the harness's canonical role
configuration. Preserve existing assignments. There is no default four-provider
panel and no fallback model table in this distribution.

A configured external lane supplies provider, model and requested effort.
On a Codex parent, its own provider uses native delegation. An explicitly
authorized external provider uses the packaged runner. The parent resolves roles;
children cannot add providers or choose their own execution route.

If native delegation or a selected external lane is unavailable, record the
missing coverage. Continue permitted independent work. Use another route only
when the task and role policy authorize it; never claim model diversity or
independent review that did not occur.

Resolve the no-comments reviewer template relative to the installed pstack
adapter directory. Its existence does not mean a named native agent is registered.
Give writers isolated locations selected by the harness and read their actual
diffs before accepting results.

## Surface verification and pacing

A CLI or TUI needs observation through the available command/terminal interface.
A UI needs the available browser or app-driving interface. If the required
surface cannot be exercised, name the missing evidence instead of claiming proof.

Use canonical skill-creator for authoring guidance. Resolve watchers and
automations through the active harness. Scheduling, cadence and notifications
remain configured outside reusable prompts. A bounded status request is one
read-only pass and does not authorize a recurring watcher.

## Packaged tools

Resolve the installed pstack directory before invoking scripts/watch-pr/watch-pr,
scripts/orch/orch.ts or scripts/runner/pstack-runner. They require Bun; provider
and GitHub operations additionally require their documented authenticated CLI.
Do not assume a source checkout, plugin-root variable or Graphite installation.

Worktree inventory and cleanup use canonical git-cleanup and its packaged
scripts/cleanup.py. Pair immutable evidence with active harness session inventory.
No alternate Claude-specific audit path ships here.

## Configuration

Resolve the active harness's instruction and configuration sources before setup.
Preserve generators and their source-of-truth relationships. Changes require
authorization for the specific setup action; this reference never writes a
default home-directory file or enables a plugin.
