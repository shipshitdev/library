# Claude Code Plugins

Documentation for installed and recommended Claude Code plugins.

**Last Updated:** 2025-12-31

---

## Currently Installed Plugins (10)

| Plugin | Marketplace | Purpose |
|--------|-------------|---------|
| **claude-mem** | thedotmack | Memory/context persistence across sessions |
| **dev-browser** | dev-browser-marketplace | Browser automation and web testing |
| **frontend-design** | claude-plugins-official | Design guidance to avoid generic AI aesthetics |
| **swift-lsp** | claude-plugins-official | Swift language server for macOS development |
| **typescript-lsp** | claude-plugins-official | TypeScript/JavaScript language server |
| **commit-commands** | claude-code-plugins | `/commit`, `/commit-push-pr` git workflow commands |
| **code-review** | claude-code-plugins | Automated PR review with parallel agents |
| **pr-review-toolkit** | claude-code-plugins | Comprehensive PR review for tests, errors, types |
| **security-guidance** | claude-code-plugins | Security monitoring for common vulnerabilities |
| **github** | claude-plugins-official | GitHub integration for issues/PRs |

---

## Optional Plugins (Not Installed)

| Plugin | Marketplace | Why |
|--------|-------------|-----|
| **hookify** | claude-code-plugins | Create custom hooks to prevent unwanted behaviors |
| **Stripe** | claude-plugins-official (external) | Payment integration (if applicable) |
| **Linear** | claude-plugins-official (external) | If using Linear for project management |
| **Slack** | claude-plugins-official (external) | If using Slack for notifications |
| **Playwright** | claude-plugins-official (external) | Browser automation/testing |
| **Supabase** | claude-plugins-official (external) | If migrating from MongoDB |

---

## Plugin Management Commands

```bash
# List available marketplaces
claude plugin marketplace list

# Browse available plugins
claude plugin  # Then go to Discover tab

# Install a plugin
claude plugin install <plugin-name>@<marketplace>

# Update a plugin
claude plugin update <plugin-name>@<marketplace>

# Enable/disable a plugin
claude plugin enable <plugin-name>@<marketplace>
claude plugin disable <plugin-name>@<marketplace>

# Uninstall a plugin
claude plugin uninstall <plugin-name>@<marketplace>

# Update all plugins (run each individually)
claude plugin update claude-mem@thedotmack
claude plugin update dev-browser@dev-browser-marketplace
claude plugin update frontend-design@claude-plugins-official
claude plugin update swift-lsp@claude-plugins-official
claude plugin update typescript-lsp@claude-plugins-official
claude plugin update commit-commands@claude-code-plugins
claude plugin update code-review@claude-code-plugins
claude plugin update pr-review-toolkit@claude-code-plugins
claude plugin update security-guidance@claude-code-plugins
claude plugin update github@claude-plugins-official
```

---

## Available Marketplaces

| Marketplace | Source | Description |
|-------------|--------|-------------|
| **claude-plugins-official** | anthropics/claude-plugins-official | Official Anthropic plugins |
| **claude-code** | anthropics/claude-code | Demo/example plugins |
| **thedotmack** | thedotmack/claude-mem | Memory persistence plugin |
| **dev-browser-marketplace** | sawyerhood/dev-browser | Browser automation plugin |

### Add a Marketplace

```bash
claude plugin marketplace add <name> --source github --owner <owner> --repo <repo>
```

---

## Plugin Categories

### LSP Plugins (Language Server Protocol)
Code intelligence for specific languages:
- `typescript-lsp` - TypeScript/JavaScript
- `pyright-lsp` - Python
- `rust-analyzer-lsp` - Rust
- `gopls-lsp` - Go
- `swift-lsp` - Swift (installed)
- `jdtls-lsp` - Java
- `php-lsp` - PHP
- `lua-lsp` - Lua
- `clangd-lsp` - C/C++
- `csharp-lsp` - C#

### Workflow Plugins
- `commit-commands` - Git workflow automation
- `code-review` - Automated PR review
- `pr-review-toolkit` - Comprehensive PR analysis
- `hookify` - Custom behavior hooks
- `security-guidance` - Security pattern monitoring

### Development Plugins
- `plugin-dev` - Create your own plugins
- `agent-sdk-dev` - Agent SDK development
- `feature-dev` - Feature development workflow

### External Integrations
- `GitHub` - GitHub integration
- `GitLab` - GitLab integration
- `Linear` - Linear project management
- `Slack` - Slack messaging
- `Stripe` - Payment processing
- `Firebase` - Firebase backend
- `Supabase` - Supabase backend
- `Asana` - Asana project management

---

## Notes

- Always restart Claude Code after installing/updating plugins
- Check plugin updates regularly: plugins can have breaking changes
- Trust plugins before installing - Anthropic doesn't verify third-party plugins
- Some plugins require additional setup (API keys, config files)

---

## Sources

- [Claude Plugins Official](https://github.com/anthropics/claude-plugins-official)
- [Claude Code Plugins](https://github.com/anthropics/claude-code/tree/main/plugins)
- [Plugin Documentation](https://code.claude.com/docs/en/discover-plugins)
