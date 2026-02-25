---
name: sentry
description: Query Sentry errors, issues, and performance data. Available via MCP in Claude Code and Cursor, and via API skill in OpenClaw.
---

# /sentry — Sentry Observability Quick Reference

## Available Tools by Platform

### Claude Code (MCP)

- **sentry_list_issues** — List issues for a project
- **sentry_get_issue** — Get issue details by ID
- **sentry_search_errors** — Search across events
- **sentry_get_event** — Get event with stacktrace
- **/seer** — AI-powered error analysis

### Cursor (MCP)

Same MCP tools as Claude Code. Access via Composer or inline chat.

### OpenClaw (API Skill)

Uses `sentry-query` skill wrapping `https://sentry.io/api/0/`. Requires `SENTRY_AUTH_TOKEN` env var.

## Organization

- **Org slug**: `genfeedai`
- **Sentry dashboard**: https://genfeedai.sentry.io

## Common Queries

### Top errors today

```
What are the top unresolved errors in the last 24 hours?
```

### Issue details

```
Show me details and stacktrace for Sentry issue {ISSUE_ID}
```

### Search for specific errors

```
Search Sentry for timeout errors in {project}
```

### Release health

```
What's the crash-free rate for the latest release of {project}?
```

### Performance

```
Show me the slowest transactions in {project} over the last 7 days
```

## Sentry Search Syntax

| Filter | Example |
|--------|---------|
| Status | `is:unresolved`, `is:resolved` |
| Level | `level:error`, `level:warning` |
| Time | `first-seen:-24h`, `last-seen:-1h` |
| Message | `message:*timeout*` |
| Tag | `browser:Chrome`, `os:iOS` |
| Assigned | `assigned:me`, `assigned:nobody` |
| Release | `release:1.2.3` |

## Tips

- Pair with OpenRouter LLM traces: errors from AI calls show in both Sentry and OpenRouter logs
- Use `/seer` in Claude Code for AI-powered root cause analysis
- Check release health after every deploy
- Set up alerts in Sentry dashboard for critical error thresholds
