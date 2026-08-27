# Evidence categories

One investigator per available category. Adapt the query vocabulary to
the connector that is actually present.

## 1. Source control

Always spawn. git history, `gh` for PRs, code comments, tests. Best at
implementation-time rationale captured during review.

Search: `git log --follow`, PR bodies, review threads, test names that
encode edge cases, commit messages that link tickets.

## 2. Issue / ticket tracker

GitHub Issues, Linear, Jira, or whatever issue connector exists. Best at
the product or business forcing function: customer requests, compliance
deadlines, parent-initiative framing.

## 3. Long-form documents

Notion, Confluence, repo docs, ADRs, RFCs, postmortems. Best at
alternatives considered and rejected approaches.

## 4. Real-time team chat

Slack, Discord, or similar. Best at fire-drill decisions that never
reached a doc. Skip only when no connector exists, and say so.

## 5. Infrastructure observability

Datadog, Grafana, Honeycomb, or similar. Best when the target reacts to
an infra signal: timeouts, retries, rate limits, circuit breakers.

## 6. Error / exception tracking

Sentry or similar. Best for catch blocks, null guards, and defenses
whose first-seen window brackets the PR ship date.

## 7. Product analytics warehouse

Warehouse or product-analytics events. Best for flag-gated code,
experiment-driven ships, and "where did this number come from".

## Incident overlay

If the target looks defensive (retries, timeouts, rate limits, feature
flags, OOM handlers), also search postmortems and incident channels
across the categories you already spawned.
