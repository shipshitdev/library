## Distribution boundary

Use the active Shipshit skill catalog and the caller's existing authorization.
The harness owns host, account, model, effort, sandbox, worktree and schedule.
Upstream examples describe mechanisms; they do not grant permission or select
providers. Preserve report-only scope. External messages, publication, installs,
deployment and destructive actions require authorization covering that action.
Read configuration from the harness source of truth; never replace its role map
with an example here. Use only capabilities the active harness actually exposes.

# What did I get done

## Trigger

Need a short, high-signal summary of work completed in a specific time range (for example: yesterday, last 3 days, or last week).

## Workflow

1. Resolve the requested time window into concrete dates.
2. Read commits authored by the current git user email within that range.
3. Exclude merge commits and uncommitted changes.
4. Synthesize the most important shipped changes into a concise status update.
5. Include the actual date range used in the final summary.

## Guardrails

- Be extremely concise and information-dense.
- Prioritize substantial behavior or architecture changes.
- Omit cosmetic-only changes (formatting, imports, minor renames).
- Do not infer intent or motivation. Describe changes functionally.

## Output

- One short summary suitable for a status update
- Real date range
- Optional 2-5 bullets for major changes only
