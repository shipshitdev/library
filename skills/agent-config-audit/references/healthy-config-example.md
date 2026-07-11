# Healthy Config Set — Example

What a well-maintained agent config stack looks like for a monorepo workspace.

## Root Level

### AGENTS.md (~80 lines)

- Workspace overview (repo table)
- Cross-repo rules (5-7 rules, one line each)
- Agent behavior section
- Self-correction protocol
- Learned Rules section (seeded, actively used)

### AGENTS.override.md (only when needed)

- Scoped replacement guidance for a subtree with genuinely different rules
- Omitted when normal AGENTS.md inheritance is sufficient

### CLAUDE.md (optional)

- Claude-specific additions only
- References AGENTS.md instead of repeating shared project rules

### Effective .codex/config.toml (when runtime customization is needed)

- Explicit fallback instruction filenames, if any
- Approval, sandbox, and network policy for this runtime

### .cursor/rules (~100-130 lines)

- No emoji in headers
- Reading order for session start
- Session file rules (brief, since hooks enforce)
- Project navigation structure
- Documentation location table
- "Last Updated" within 90 days

### .claude/settings.json

- Denied skills with companion SETTINGS-NOTES.md documenting rationale
- MCP server config

### .claude/hooks.json

- Runtime enforcement for violations that burn the most time
- Fast timeouts (5s)
- Targeted (not duplicating what linters catch)

## Per-Repo Level

### AGENTS.md (~50-150 lines)

- Tech stack
- Commands (dev, build, test, lint)
- Repo-specific critical rules (may briefly reference cross-repo rules)
- Architecture (key directories, patterns)
- Learned Rules section (seeded)
- Does NOT repeat full cross-repo rules from root

### CLAUDE.md (optional, concise)

- Claude-specific additions not shared by other agents
- Links to AGENTS.md and `.agents/memory/`

### .cursorrules (~60-70 lines)

- No emoji
- Reading order specific to this project
- Navigation to project .agents/ structure
- "Last Updated" within 90 days

## Health Metrics

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Max rule occurrences | 2 | 3 | 4+ |
| Stale files (> 90 days) | 0 | 1-2 | 3+ |
| Unconfigured instruction fallbacks | 0 | 1 | 2+ |
| Emoji in config headers | 0 | 1-5 | 6+ |
| Hardcoded absolute paths | 0 | 1 | 2+ |
| Undocumented denied skills | 0 | 1-3 | 4+ |
| Total root config lines | < 250 | 250-400 | 400+ |
| Total per-repo config lines | < 200 | 200-300 | 300+ |
