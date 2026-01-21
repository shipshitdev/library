![Ship Shit Dev Library](./assets/banner.svg)

# Ship Shit Dev Library

![Project Type](https://img.shields.io/badge/Project-Library-blue)

100+ AI agent skills for indie developers. Works with Claude Code, OpenAI Codex, and Cursor.

## Directory Structure

```
library/
├── skills/              # All skills (123 skills)
├── commands/            # All commands (35 commands)
├── bundles/             # Generated marketplace bundles
├── .agent/              # Library management (sessions, tasks)
│   └── SYSTEM/          # Library documentation
└── scripts/             # Scaffolding, validation scripts
```

## What's Included

- **Skills**: Specialized agent capabilities for specific domains (e.g., `stripe-implementer`, `mongodb-migration-expert`)
- **Commands**: Workflow commands for structured tasks (e.g., `code-review`, `deploy`, `mvp-plan`)
- **Documentation**: Platform-specific adaptations and management guides
- **Scripts**: Tooling for syncing, validation, and generation

## Installation

### Quick Install (Recommended)

```bash
# Install all skills globally to all agents
npx skills add shipshitdev/library --all

# Install specific skills
npx skills add shipshitdev/library --skill stripe-implementer

# List available skills
npx skills add shipshitdev/library --list
```

### Project-local Install

```bash
npx skills add shipshitdev/library
```

### Claude Code Plugin (Alternative)

```bash
/plugin marketplace add shipshitdev/library
/plugin install shipshitdev-full@shipshitdev
```

### For Contributors

Clone the repo and use the CLI to install:

```bash
git clone https://github.com/shipshitdev/library.git ~/shipshitdev-library
cd ~/shipshitdev-library
npx skills add . --all
```

After making changes, reinstall to update:

```bash
npx skills add shipshitdev/library --all
```

## Adding Skills & Commands

### Adding a Skill

1. Create directory in `skills/skill-name/`
2. Add `SKILL.md` with YAML frontmatter
3. Update this README

```bash
mkdir -p skills/my-skill
touch skills/my-skill/SKILL.md
```

### Adding a Command

1. Create `.md` file in `commands/`
2. Follow naming: `{verb}-{noun}.md`
3. Update this README

## Documentation

- `.agent/SYSTEM/ARCHITECTURE.md` - .agent folder structure explained
- `.agent/SYSTEM/AI-DEV-LOOP.md` - The /loop autonomous workflow
- `.agent/SYSTEM/PLATFORM-ADAPTATIONS.md` - Claude vs Codex vs Cursor differences
- `.agent/SYSTEM/SKILL-MANAGEMENT.md` - Syncing skills across platforms

## Commands

| Command          | Description                                    | Cursor                                                      |
|------------------|------------------------------------------------|-------------------------------------------------------------|
| analyze-codebase | Codebase analysis                               | [analyze-codebase](commands/analyze-codebase.md) |
| api-test         | API test generation                            | [api-test](commands/api-test.md)             |
| bug              | Bug capture workflow                            | [bug](commands/bug.md)                       |
| check-domain     | Domain name generator & availability checker   | [check-domain](commands/check-domain.md)       |
| clean            | Cleanup workflow                                | [clean](commands/clean.md)                     |
| code-review      | Code review                                     | [code-review](commands/code-review.md)        |
| db-setup         | MongoDB/Redis setup                             | [db-setup](commands/db-setup.md)              |
| de-slop          | Clean AI code artifacts                         | [de-slop](commands/de-slop.md)                |
| deploy           | Deployment workflows                            | [deploy](commands/deploy.md)                   |
| docs-generate    | Documentation generation                        | [docs-generate](commands/docs-generate.md)     |
| docs-update      | Documentation updates                           | [docs-update](commands/docs-update.md)        |
| end              | End session                                     | [end](commands/end.md)                         |
| env-setup        | Environment variables                           | [env-setup](commands/env-setup.md)            |
| inbox            | Process inbox items                             | [inbox](commands/inbox.md)                     |
| launch           | Launch workflow                                 | [launch](commands/launch.md)                    |
| migrate          | Database migrations                             | [migrate](commands/migrate.md)                 |
| monitoring-setup| Sentry/Analytics setup                         | [monitoring-setup](commands/monitoring-setup.md) |
| mvp-plan         | MVP planning                                    | [mvp-plan](commands/mvp-plan.md)               |
| new-cmd          | Create new commands                             | [new-cmd](commands/new-cmd.md)                 |
| new-session      | Create session files                            | [new-session](commands/new-session.md)         |
| optimize-prompt  | Prompt optimization                             | [optimize-prompt](commands/optimize-prompt.md)  |
| performance      | Performance analysis                            | [performance](commands/performance.md)           |
| quick-fix        | Quick fixes                                     | [quick-fix](commands/quick-fix.md)              |
| refactor-code    | Code refactoring                                | [refactor-code](commands/refactor-code.md)     |
| review-pr        | PR review                                       | [review-pr](commands/review-pr.md)              |
| scaffold         | Project scaffolding                             | [scaffold](commands/scaffold.md)                |
| security-audit   | Security audit                                  | [security-audit](commands/security-audit.md)   |
| start            | Start session                                   | [start](commands/start.md)                      |
| task             | Task management                                 | [task](commands/task.md)                         |
| test             | Test tracking                                   | [test](commands/test.md)                        |
| validate         | Validation workflow                             | [validate](commands/validate.md)                 |

## Skills

| Skill                      | Description                            |
|----------------------------|----------------------------------------|
| accessibility              | WCAG 2.1 AA compliance                 |
| agent-folder-init          | Initialize .agent/ folder              |
| analytics-expert           | Content analytics                      |
| api-design-expert          | RESTful API design                     |
| artifacts-builder          | Project artifacts                      |
| aws-infrastructure         | AWS EC2/VPC/ALB setup                  |
| changelog-generator        | Git changelogs                         |
| clerk-validator            | Clerk auth validation                  |
| component-library          | Component standards                    |
| content-creator            | Newsletters & tweets with your voice   |
| content-script-developer   | Browser extensions                     |
| copywriter                 | Brand copywriting                      |
| design-consistency-auditor | Design system                          |
| docker-expert              | Docker/compose                         |
| docs                       | Documentation                          |
| docusaurus-writer          | Docusaurus sites                       |
| error-handling-expert      | Error patterns                         |
| expo-architect             | Expo/React Native                      |
| fullstack-workspace-init   | Monorepo setup                         |
| gh-address-comments        | GitHub comments                        |
| gh-fix-ci                  | Fix CI/CD                              |
| internal-comms             | Internal comms                         |
| landing-page-vercel        | Vercel landing pages                   |
| leads-researcher           | Lead research                          |
| mcp-builder                | MCP servers                            |
| micro-landing-builder      | Micro landing pages                    |
| mongodb-migration-expert   | MongoDB migrations                     |
| monitoring-setup           | Sentry/Analytics                       |
| nestjs-queue-architect     | BullMQ queues                          |
| nestjs-testing-expert      | NestJS testing                         |
| package-architect          | npm packages                           |
| performance-expert         | Performance                            |
| planning-assistant         | Content planning                       |
| plasmo-extension-architect | Plasmo extensions                      |
| project-scaffold           | Project scaffolding                    |
| prompt-engineer            | Prompt engineering                     |
| qa-reviewer                | QA review                              |
| react-native-components    | RN components                          |
| roadmap-analyzer           | Product roadmap                        |
| rules-capture              | Coding rules                           |
| search-domain-validator    | Domain validation                      |
| security-expert            | App security                           |
| serializer-specialist      | Data serialization                     |
| session-documenter         | Session docs                           |
| skill-creator              | Skill creation                         |
| strategy-expert            | Content strategy                       |
| stripe-implementer         | Stripe payments                        |
| task-prd-creator           | Task & PRD creation workflow           |
| testing-expert             | Testing strategies                     |
| workflow-automation        | Workflow automation                    |

## Complementary Skills (External)

These external skill repositories complement this library. Install them separately when needed.

### [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills)

Tactical marketing execution: CRO, SEO, paid ads, and email sequences.

**How it complements this library:**

| This Library (Strategic) | coreyhaines31 (Tactical) |
|--------------------------|--------------------------|
| Hormozi/Brunson frameworks | CRO, SEO, ads execution |
| `offer-architect` → Build offers | `page-cro` → Optimize where offers live |
| `funnel-architect` → Design funnels | `form-cro`, `email-sequence` → Optimize steps |
| `traffic-architect` → Plan traffic | `paid-ads`, `programmatic-seo` → Execute traffic |
| `expert-architect` → Build positioning | `launch-strategy` → Execute launches |

**Install both for full coverage:**

```bash
# Strategic frameworks (this library)
npx skills add shipshitdev/library --all

# Tactical execution
npx skills add coreyhaines31/marketingskills --all
```

| Category | Skills |
|----------|--------|
| **CRO** | form-cro, page-cro, onboarding-cro, signup-flow-cro, popup-cro, paywall-upgrade-cro |
| **SEO** | programmatic-seo, seo-audit, schema-markup |
| **Paid** | paid-ads |
| **Testing** | ab-test-setup |
| **Email** | email-sequence |
| **Launch** | launch-strategy |
| **Psychology** | marketing-psychology (70+ mental models) |
| **Ideas** | marketing-ideas (140 tactics) |

> **Note:** Skills can be enabled or disabled per project via `.claude/settings.json`:
>
> ```json
> {
>   "enabledPlugins": {
>     "web-design-guidelines@vercel-labs": true,
>     "static-analysis@trailofbits": true
>   }
> }
> ```
>
> Use `/plugin menu` to browse and toggle skills interactively.

### [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)

Frontend development and design guidelines.

| Category | Skill | Description |
|----------|-------|-------------|
| **Frontend** | react-best-practices | React/Next.js performance optimization patterns |
| | web-design-guidelines | Review UI for Web Interface Guidelines compliance |

```bash
npx skills add vercel-labs/agent-skills --all
```

### [trailofbits/skills](https://github.com/trailofbits/skills)

Security auditing, smart contracts, and vulnerability analysis.

| Category | Skill | Description |
|----------|-------|-------------|
| **Audit Lifecycle** | fix-review | Verify fix commits address audit findings |
| **Code Auditing** | audit-context-building | Deep architectural context analysis |
| | burpsuite-project-parser | Search and extract data from Burp Suite files |
| | differential-review | Security-focused code change review |
| | semgrep-rule-creator | Custom Semgrep rule creation |
| | sharp-edges | Identify error-prone APIs and footgun designs |
| | static-analysis | CodeQL, Semgrep, SARIF toolkit |
| | testing-handbook-skills | Fuzzers, sanitizers, coverage tools |
| | variant-analysis | Find similar vulnerabilities across codebases |
| **Development** | ask-questions-if-underspecified | Clarify requirements before implementing |
| | culture-index | Interpret Culture Index survey results |
| **Reverse Engineering** | dwarf-expert | DWARF debugging format expertise |
| **Smart Contracts** | building-secure-contracts | Security toolkit for 6 blockchains |
| | entry-point-analyzer | Identify state-changing entry points |
| **Verification** | constant-time-analysis | Detect timing side-channels in crypto code |
| | property-based-testing | Property-based testing for multiple languages |
| | spec-to-code-compliance | Specification compliance checker |

```bash
npx skills add trailofbits/skills --all
```

### [expo/skills](https://github.com/expo/skills)

Official Expo skills for React Native development.

| Category | Skill | Description |
|----------|-------|-------------|
| **UI** | building-ui | Complete guide for building beautiful apps with Expo Router |
| | building-native-ui | Native app development patterns |
| **Data** | data-fetching | Network requests, React Query, caching, offline support |
| **Deployment** | deployment | iOS App Store, Play Store, web hosting |
| | dev-client | Build and distribute development clients |
| **Infrastructure** | api-routes | API routes in Expo Router with EAS Hosting |
| | cicd-workflows | EAS workflow YAML files for CI/CD |
| **Setup** | tailwind-setup | Tailwind CSS v4 with NativeWind v5 |
| | upgrading-expo | SDK version upgrades and dependency fixes |
| **Advanced** | use-dom | Run web code in webviews on native platforms |

**How it complements this library:**

| This Library | expo/skills |
|--------------|-------------|
| `expo-architect` → Scaffold new apps | Develop and maintain existing apps |

```bash
npx skills add expo/skills --all
```

---

## How Skills Adapt to Projects

Skills are **adaptive** - they scan project documentation to understand:

- Project architecture and structure
- Brand voice and tone
- Existing patterns and conventions
- Terminology and style

If a project has its own skill, the generic skill will collaborate with or defer to it.

## Publishing & CI/CD

When you push to `master`, GitHub Actions automatically regenerates the `bundles/` directory to keep marketplace plugins in sync with skills.

### Claude Marketplace

Users install directly from GitHub:

```bash
# Add the marketplace
/plugin marketplace add shipshitdev/library

# Install full library
/plugin install shipshitdev-full@shipshitdev

# Or install specific bundles
/plugin install shipshitdev-startup@shipshitdev
/plugin install shipshitdev-testing@shipshitdev
/plugin install shipshitdev-frontend@shipshitdev
```
