![Ship Shit Dev Library](./assets/banner.svg)

# Ship Shit Dev Library

![Project Type](https://img.shields.io/badge/Project-Library-blue)

100+ AI agent skills for indie developers. Works with Claude Code, OpenAI Codex, and Cursor.

## Directory Structure

```
library/
├── skills/              # All skills (124 skills)
├── commands/            # All commands (35 commands)
├── bundles/             # Generated marketplace bundles
├── .agents/              # Library management (sessions, tasks)
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
# Install all skills globally — pick your agents
npx skills add shipshitdev/library -g --agent claude-code cursor codex openclaw --skill '*' -y

# Install specific skills
npx skills add shipshitdev/library -g --skill stripe-implementer -y

# List available skills
npx skills add shipshitdev/library --list
```

> **Do NOT use `--all`** — it installs to every agent the CLI knows about (30+).
> Always use `--agent` to target only the agents you use.

### Project-local Install

```bash
npx skills add shipshitdev/library --agent claude-code cursor
```

### Claude Code Plugin (Alternative)

```bash
/plugin marketplace add shipshitdev/library
/plugin install shipshitdev-startup@shipshitdev    # or any category bundle
```

### For Contributors

Clone the repo and use the CLI to install:

```bash
git clone https://github.com/shipshitdev/library.git ~/shipshitdev-library
cd ~/shipshitdev-library
npx skills add . -g --agent claude-code cursor codex openclaw --skill '*' -y
```

After making changes, reinstall to update:

```bash
npx skills add shipshitdev/library -g --agent claude-code cursor codex openclaw --skill '*' -y
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

- `.agents/SYSTEM/ARCHITECTURE.md` - .agent folder structure explained
- `.agents/SYSTEM/AI-DEV-LOOP.md` - The /loop autonomous workflow
- `.agents/SYSTEM/PLATFORM-ADAPTATIONS.md` - Claude vs Codex vs Cursor differences
- `.agents/SYSTEM/SKILL-MANAGEMENT.md` - Syncing skills across platforms

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

| Skill | Description | Install |
|-------|-------------|---------|
| [accessibility](https://skills.sh/shipshitdev/library/accessibility) | WCAG 2.1 AA compliance for React/Next.js | `npx skills add shipshitdev/library --skill accessibility` |
| [advanced-evaluation](https://skills.sh/shipshitdev/library/advanced-evaluation) | LLM-as-a-Judge evaluation techniques | `npx skills add shipshitdev/library --skill advanced-evaluation` |
| [agent-browser](https://skills.sh/shipshitdev/library/agent-browser) | Browser automation for testing & scraping | `npx skills add shipshitdev/library --skill agent-browser` |
| [agent-folder-init](https://skills.sh/shipshitdev/library/agent-folder-init) | Initialize .agents/ folder structure | `npx skills add shipshitdev/library --skill agent-folder-init` |
| [ai-dev-loop](https://skills.sh/shipshitdev/library/ai-dev-loop) | Autonomous AI development workflow | `npx skills add shipshitdev/library --skill ai-dev-loop` |
| [ai-loading-ux](https://skills.sh/shipshitdev/library/ai-loading-ux) | AI loading & progress indicator UX | `npx skills add shipshitdev/library --skill ai-loading-ux` |
| [analytics-expert](https://skills.sh/shipshitdev/library/analytics-expert) | Content analytics & metrics | `npx skills add shipshitdev/library --skill analytics-expert` |
| [api-design-expert](https://skills.sh/shipshitdev/library/api-design-expert) | RESTful API design & OpenAPI docs | `npx skills add shipshitdev/library --skill api-design-expert` |
| [artifacts-builder](https://skills.sh/shipshitdev/library/artifacts-builder) | Multi-component claude.ai artifacts | `npx skills add shipshitdev/library --skill artifacts-builder` |
| [aws-infrastructure](https://skills.sh/shipshitdev/library/aws-infrastructure) | AWS EC2/VPC/ALB infrastructure setup | `npx skills add shipshitdev/library --skill aws-infrastructure` |
| [biome-validator](https://skills.sh/shipshitdev/library/biome-validator) | Validate Biome 2.3+ configuration | `npx skills add shipshitdev/library --skill biome-validator` |
| [brand-architect](https://skills.sh/shipshitdev/library/brand-architect) | Brand strategy & identity development | `npx skills add shipshitdev/library --skill brand-architect` |
| [brand-name-generator](https://skills.sh/shipshitdev/library/brand-name-generator) | Creative brand & product naming | `npx skills add shipshitdev/library --skill brand-name-generator` |
| [bun-validator](https://skills.sh/shipshitdev/library/bun-validator) | Validate Bun workspace configuration | `npx skills add shipshitdev/library --skill bun-validator` |
| [business-model-auditor](https://skills.sh/shipshitdev/library/business-model-auditor) | Stress test business models | `npx skills add shipshitdev/library --skill business-model-auditor` |
| [business-operator](https://skills.sh/shipshitdev/library/business-operator) | Multi-business operations management | `npx skills add shipshitdev/library --skill business-operator` |
| [changelog-generator](https://skills.sh/shipshitdev/library/changelog-generator) | Auto-generate changelogs from git | `npx skills add shipshitdev/library --skill changelog-generator` |
| [channel-validator](https://skills.sh/shipshitdev/library/channel-validator) | Validate marketing channels | `npx skills add shipshitdev/library --skill channel-validator` |
| [clerk-validator](https://skills.sh/shipshitdev/library/clerk-validator) | Validate Clerk auth configuration | `npx skills add shipshitdev/library --skill clerk-validator` |
| [cofounder-evaluator](https://skills.sh/shipshitdev/library/cofounder-evaluator) | Evaluate potential co-founders | `npx skills add shipshitdev/library --skill cofounder-evaluator` |
| [comment-mode](https://skills.sh/shipshitdev/library/comment-mode) | Granular feedback without rewriting | `npx skills add shipshitdev/library --skill comment-mode` |
| [competitive-intelligence-analyst](https://skills.sh/shipshitdev/library/competitive-intelligence-analyst) | Competitor analysis & monitoring | `npx skills add shipshitdev/library --skill competitive-intelligence-analyst` |
| [component-library](https://skills.sh/shipshitdev/library/component-library) | React/Next.js component architecture | `npx skills add shipshitdev/library --skill component-library` |
| [constraint-eliminator](https://skills.sh/shipshitdev/library/constraint-eliminator) | Remove customer friction points | `npx skills add shipshitdev/library --skill constraint-eliminator` |
| [content-creator](https://skills.sh/shipshitdev/library/content-creator) | Newsletters & tweets in your voice | `npx skills add shipshitdev/library --skill content-creator` |
| [content-script-developer](https://skills.sh/shipshitdev/library/content-script-developer) | Browser extension content scripts | `npx skills add shipshitdev/library --skill content-script-developer` |
| [context-degradation](https://skills.sh/shipshitdev/library/context-degradation) | Diagnose & mitigate context issues | `npx skills add shipshitdev/library --skill context-degradation` |
| [context-fundamentals](https://skills.sh/shipshitdev/library/context-fundamentals) | Context mechanics for agent systems | `npx skills add shipshitdev/library --skill context-fundamentals` |
| [context-optimization](https://skills.sh/shipshitdev/library/context-optimization) | Extend effective context capacity | `npx skills add shipshitdev/library --skill context-optimization` |
| [copy-validator](https://skills.sh/shipshitdev/library/copy-validator) | Validate sales copy & landing pages | `npx skills add shipshitdev/library --skill copy-validator` |
| [copywriter](https://skills.sh/shipshitdev/library/copywriter) | Brand voice & conversion copywriting | `npx skills add shipshitdev/library --skill copywriter` |
| [cto-advisor](https://skills.sh/shipshitdev/library/cto-advisor) | Technical leadership guidance | `npx skills add shipshitdev/library --skill cto-advisor` |
| [design-consistency-auditor](https://skills.sh/shipshitdev/library/design-consistency-auditor) | Design system consistency audit | `npx skills add shipshitdev/library --skill design-consistency-auditor` |
| [devcontainer-setup](https://skills.sh/shipshitdev/library/devcontainer-setup) | VS Code devcontainer with Docker | `npx skills add shipshitdev/library --skill devcontainer-setup` |
| [docker-expert](https://skills.sh/shipshitdev/library/docker-expert) | Docker & docker-compose patterns | `npx skills add shipshitdev/library --skill docker-expert` |
| [docs](https://skills.sh/shipshitdev/library/docs) | Technical documentation creation | `npx skills add shipshitdev/library --skill docs` |
| [early-hiring-advisor](https://skills.sh/shipshitdev/library/early-hiring-advisor) | Early-stage hiring guidance | `npx skills add shipshitdev/library --skill early-hiring-advisor` |
| [ec2-backend-deployer](https://skills.sh/shipshitdev/library/ec2-backend-deployer) | Deploy backends to EC2 with CI/CD | `npx skills add shipshitdev/library --skill ec2-backend-deployer` |
| [email-finder](https://skills.sh/shipshitdev/library/email-finder) | Find email addresses for contacts | `npx skills add shipshitdev/library --skill email-finder` |
| [error-handling-expert](https://skills.sh/shipshitdev/library/error-handling-expert) | Error handling patterns & strategies | `npx skills add shipshitdev/library --skill error-handling-expert` |
| [evaluation](https://skills.sh/shipshitdev/library/evaluation) | Agent evaluation frameworks | `npx skills add shipshitdev/library --skill evaluation` |
| [execution-accelerator](https://skills.sh/shipshitdev/library/execution-accelerator) | Unblock decisions & execution | `npx skills add shipshitdev/library --skill execution-accelerator` |
| [execution-validator](https://skills.sh/shipshitdev/library/execution-validator) | Validate launch plans & execution | `npx skills add shipshitdev/library --skill execution-validator` |
| [expert-architect](https://skills.sh/shipshitdev/library/expert-architect) | Build positioning & authority | `npx skills add shipshitdev/library --skill expert-architect` |
| [expert-validator](https://skills.sh/shipshitdev/library/expert-validator) | Validate positioning & messaging | `npx skills add shipshitdev/library --skill expert-validator` |
| [expo-architect](https://skills.sh/shipshitdev/library/expo-architect) | Scaffold Expo React Native apps | `npx skills add shipshitdev/library --skill expo-architect` |
| [financial-operations-expert](https://skills.sh/shipshitdev/library/financial-operations-expert) | Business finances & operations | `npx skills add shipshitdev/library --skill financial-operations-expert` |
| [frontend-design](https://skills.sh/shipshitdev/library/frontend-design) | Production-grade frontend interfaces | `npx skills add shipshitdev/library --skill frontend-design` |
| [fullstack-workspace-init](https://skills.sh/shipshitdev/library/fullstack-workspace-init) | Full-stack monorepo scaffolding | `npx skills add shipshitdev/library --skill fullstack-workspace-init` |
| [fundraise-advisor](https://skills.sh/shipshitdev/library/fundraise-advisor) | Fundraising & pitch deck guidance | `npx skills add shipshitdev/library --skill fundraise-advisor` |
| [funnel-architect](https://skills.sh/shipshitdev/library/funnel-architect) | Design sales funnels | `npx skills add shipshitdev/library --skill funnel-architect` |
| [funnel-validator](https://skills.sh/shipshitdev/library/funnel-validator) | Validate existing sales funnels | `npx skills add shipshitdev/library --skill funnel-validator` |
| [gh-address-comments](https://skills.sh/shipshitdev/library/gh-address-comments) | Address GitHub PR/issue comments | `npx skills add shipshitdev/library --skill gh-address-comments` |
| [gh-fix-ci](https://skills.sh/shipshitdev/library/gh-fix-ci) | Fix failing GitHub Actions CI | `npx skills add shipshitdev/library --skill gh-fix-ci` |
| [git-safety](https://skills.sh/shipshitdev/library/git-safety) | Scan & clean git history secrets | `npx skills add shipshitdev/library --skill git-safety` |
| [html-style](https://skills.sh/shipshitdev/library/html-style) | Apply styling to barebones HTML | `npx skills add shipshitdev/library --skill html-style` |
| [humanizer](https://skills.sh/shipshitdev/library/humanizer) | Remove AI writing patterns | `npx skills add shipshitdev/library --skill humanizer` |
| [husky-test-coverage](https://skills.sh/shipshitdev/library/husky-test-coverage) | Husky hooks for test coverage | `npx skills add shipshitdev/library --skill husky-test-coverage` |
| [idea-validator](https://skills.sh/shipshitdev/library/idea-validator) | Validate startup ideas (Hexa framework) | `npx skills add shipshitdev/library --skill idea-validator` |
| [incremental-fetch](https://skills.sh/shipshitdev/library/incremental-fetch) | Resilient API data pipelines | `npx skills add shipshitdev/library --skill incremental-fetch` |
| [internal-comms](https://skills.sh/shipshitdev/library/internal-comms) | Internal communications templates | `npx skills add shipshitdev/library --skill internal-comms` |
| [landing-page-vercel](https://skills.sh/shipshitdev/library/landing-page-vercel) | Static landing pages for Vercel | `npx skills add shipshitdev/library --skill landing-page-vercel` |
| [lead-channel-optimizer](https://skills.sh/shipshitdev/library/lead-channel-optimizer) | Optimize lead generation channels | `npx skills add shipshitdev/library --skill lead-channel-optimizer` |
| [leads-researcher](https://skills.sh/shipshitdev/library/leads-researcher) | Research leads & prospects | `npx skills add shipshitdev/library --skill leads-researcher` |
| [linter-formatter-init](https://skills.sh/shipshitdev/library/linter-formatter-init) | Set up Biome or ESLint + Prettier | `npx skills add shipshitdev/library --skill linter-formatter-init` |
| [market-sizer](https://skills.sh/shipshitdev/library/market-sizer) | Calculate TAM/SAM/SOM market size | `npx skills add shipshitdev/library --skill market-sizer` |
| [mcp-builder](https://skills.sh/shipshitdev/library/mcp-builder) | Build MCP servers for LLMs | `npx skills add shipshitdev/library --skill mcp-builder` |
| [memory-systems](https://skills.sh/shipshitdev/library/memory-systems) | Memory architectures for agents | `npx skills add shipshitdev/library --skill memory-systems` |
| [micro-landing-builder](https://skills.sh/shipshitdev/library/micro-landing-builder) | Config-driven NextJS landing pages | `npx skills add shipshitdev/library --skill micro-landing-builder` |
| [mongodb-atlas-checker](https://skills.sh/shipshitdev/library/mongodb-atlas-checker) | Verify MongoDB Atlas configuration | `npx skills add shipshitdev/library --skill mongodb-atlas-checker` |
| [mongodb-migration-expert](https://skills.sh/shipshitdev/library/mongodb-migration-expert) | MongoDB schema & migration guidance | `npx skills add shipshitdev/library --skill mongodb-migration-expert` |
| [monitoring-setup](https://skills.sh/shipshitdev/library/monitoring-setup) | Sentry & Google Analytics setup | `npx skills add shipshitdev/library --skill monitoring-setup` |
| [multi-agent-patterns](https://skills.sh/shipshitdev/library/multi-agent-patterns) | Multi-agent architecture design | `npx skills add shipshitdev/library --skill multi-agent-patterns` |
| [mvp-architect](https://skills.sh/shipshitdev/library/mvp-architect) | Scope MVPs & minimum features | `npx skills add shipshitdev/library --skill mvp-architect` |
| [nestjs-queue-architect](https://skills.sh/shipshitdev/library/nestjs-queue-architect) | BullMQ queue patterns for NestJS | `npx skills add shipshitdev/library --skill nestjs-queue-architect` |
| [nestjs-testing-expert](https://skills.sh/shipshitdev/library/nestjs-testing-expert) | NestJS testing patterns with Jest | `npx skills add shipshitdev/library --skill nestjs-testing-expert` |
| [nextjs-validator](https://skills.sh/shipshitdev/library/nextjs-validator) | Validate Next.js 16 configuration | `npx skills add shipshitdev/library --skill nextjs-validator` |
| [nextra-writer](https://skills.sh/shipshitdev/library/nextra-writer) | Nextra documentation sites | `npx skills add shipshitdev/library --skill nextra-writer` |
| [offer-architect](https://skills.sh/shipshitdev/library/offer-architect) | Create irresistible offers | `npx skills add shipshitdev/library --skill offer-architect` |
| [offer-validator](https://skills.sh/shipshitdev/library/offer-validator) | Validate offers (Hormozi framework) | `npx skills add shipshitdev/library --skill offer-validator` |
| [open-source-checker](https://skills.sh/shipshitdev/library/open-source-checker) | Detect secrets & private info | `npx skills add shipshitdev/library --skill open-source-checker` |
| [outbound-optimizer](https://skills.sh/shipshitdev/library/outbound-optimizer) | Optimize cold outreach & sales | `npx skills add shipshitdev/library --skill outbound-optimizer` |
| [package-architect](https://skills.sh/shipshitdev/library/package-architect) | TypeScript packages in monorepos | `npx skills add shipshitdev/library --skill package-architect` |
| [partnership-builder](https://skills.sh/shipshitdev/library/partnership-builder) | Build revenue partnerships | `npx skills add shipshitdev/library --skill partnership-builder` |
| [performance-expert](https://skills.sh/shipshitdev/library/performance-expert) | Performance optimization patterns | `npx skills add shipshitdev/library --skill performance-expert` |
| [planning-assistant](https://skills.sh/shipshitdev/library/planning-assistant) | Content planning & scheduling | `npx skills add shipshitdev/library --skill planning-assistant` |
| [plasmo-extension-architect](https://skills.sh/shipshitdev/library/plasmo-extension-architect) | Chrome MV3 extensions with Plasmo | `npx skills add shipshitdev/library --skill plasmo-extension-architect` |
| [playwright-e2e-init](https://skills.sh/shipshitdev/library/playwright-e2e-init) | Playwright E2E testing setup | `npx skills add shipshitdev/library --skill playwright-e2e-init` |
| [positioning-angles](https://skills.sh/shipshitdev/library/positioning-angles) | Find unique marketing angles | `npx skills add shipshitdev/library --skill positioning-angles` |
| [pricing-strategist](https://skills.sh/shipshitdev/library/pricing-strategist) | Pricing strategy & optimization | `npx skills add shipshitdev/library --skill pricing-strategist` |
| [project-init-orchestrator](https://skills.sh/shipshitdev/library/project-init-orchestrator) | Orchestrate project initialization | `npx skills add shipshitdev/library --skill project-init-orchestrator` |
| [project-scaffold](https://skills.sh/shipshitdev/library/project-scaffold) | Cross-platform project scaffolding | `npx skills add shipshitdev/library --skill project-scaffold` |
| [prompt-engineer](https://skills.sh/shipshitdev/library/prompt-engineer) | Prompt engineering for content | `npx skills add shipshitdev/library --skill prompt-engineer` |
| [qa-reviewer](https://skills.sh/shipshitdev/library/qa-reviewer) | Review AI work for quality | `npx skills add shipshitdev/library --skill qa-reviewer` |
| [quick-view](https://skills.sh/shipshitdev/library/quick-view) | Generate HTML preview pages | `npx skills add shipshitdev/library --skill quick-view` |
| [react-native-components](https://skills.sh/shipshitdev/library/react-native-components) | React Native 0.79.5 components | `npx skills add shipshitdev/library --skill react-native-components` |
| [retention-engine](https://skills.sh/shipshitdev/library/retention-engine) | Reduce churn & increase retention | `npx skills add shipshitdev/library --skill retention-engine` |
| [roadmap-analyzer](https://skills.sh/shipshitdev/library/roadmap-analyzer) | Analyze features against ICP | `npx skills add shipshitdev/library --skill roadmap-analyzer` |
| [rules-capture](https://skills.sh/shipshitdev/library/rules-capture) | Detect & document coding rules | `npx skills add shipshitdev/library --skill rules-capture` |
| [scale-validator](https://skills.sh/shipshitdev/library/scale-validator) | Validate business scalability | `npx skills add shipshitdev/library --skill scale-validator` |
| [search-domain-validator](https://skills.sh/shipshitdev/library/search-domain-validator) | Validate domain availability | `npx skills add shipshitdev/library --skill search-domain-validator` |
| [security-expert](https://skills.sh/shipshitdev/library/security-expert) | OWASP Top 10 & app security | `npx skills add shipshitdev/library --skill security-expert` |
| [serializer-specialist](https://skills.sh/shipshitdev/library/serializer-specialist) | JSON:API serialization patterns | `npx skills add shipshitdev/library --skill serializer-specialist` |
| [session-documenter](https://skills.sh/shipshitdev/library/session-documenter) | Document session work automatically | `npx skills add shipshitdev/library --skill session-documenter` |
| [shadcn-setup](https://skills.sh/shipshitdev/library/shadcn-setup) | shadcn/ui with Tailwind CSS v4 | `npx skills add shipshitdev/library --skill shadcn-setup` |
| [skill-creator](https://skills.sh/shipshitdev/library/skill-creator) | Guide for creating new skills | `npx skills add shipshitdev/library --skill skill-creator` |
| [spec-first](https://skills.sh/shipshitdev/library/spec-first) | Spec → plan → execute workflow | `npx skills add shipshitdev/library --skill spec-first` |
| [startup-icp-definer](https://skills.sh/shipshitdev/library/startup-icp-definer) | Define ideal customer profile | `npx skills add shipshitdev/library --skill startup-icp-definer` |
| [strategy-expert](https://skills.sh/shipshitdev/library/strategy-expert) | Content strategy planning | `npx skills add shipshitdev/library --skill strategy-expert` |
| [stripe-implementer](https://skills.sh/shipshitdev/library/stripe-implementer) | Stripe payments & subscriptions | `npx skills add shipshitdev/library --skill stripe-implementer` |
| [support-systems-architect](https://skills.sh/shipshitdev/library/support-systems-architect) | Customer support system setup | `npx skills add shipshitdev/library --skill support-systems-architect` |
| [table-filters](https://skills.sh/shipshitdev/library/table-filters) | Optimal filtering UX for tables | `npx skills add shipshitdev/library --skill table-filters` |
| [tailwind-validator](https://skills.sh/shipshitdev/library/tailwind-validator) | Validate Tailwind CSS v4 config | `npx skills add shipshitdev/library --skill tailwind-validator` |
| [task-prd-creator](https://skills.sh/shipshitdev/library/task-prd-creator) | Task files & PRD creation | `npx skills add shipshitdev/library --skill task-prd-creator` |
| [testing-cicd-init](https://skills.sh/shipshitdev/library/testing-cicd-init) | Vitest & GitHub Actions CI/CD | `npx skills add shipshitdev/library --skill testing-cicd-init` |
| [testing-expert](https://skills.sh/shipshitdev/library/testing-expert) | Testing strategies for React/NestJS | `npx skills add shipshitdev/library --skill testing-expert` |
| [theme-factory](https://skills.sh/shipshitdev/library/theme-factory) | Theme toolkit for artifacts | `npx skills add shipshitdev/library --skill theme-factory` |
| [tool-design](https://skills.sh/shipshitdev/library/tool-design) | Design effective agent tools | `npx skills add shipshitdev/library --skill tool-design` |
| [traffic-architect](https://skills.sh/shipshitdev/library/traffic-architect) | Traffic strategy & Dream 100 | `npx skills add shipshitdev/library --skill traffic-architect` |
| [traffic-validator](https://skills.sh/shipshitdev/library/traffic-validator) | Validate traffic strategy | `npx skills add shipshitdev/library --skill traffic-validator` |
| [workflow-automation](https://skills.sh/shipshitdev/library/workflow-automation) | Content workflow automation | `npx skills add shipshitdev/library --skill workflow-automation` |
| [workspace-performance-audit](https://skills.sh/shipshitdev/library/workspace-performance-audit) | Full-stack performance audits | `npx skills add shipshitdev/library --skill workspace-performance-audit` |
| [x-algorithm-optimizer](https://skills.sh/shipshitdev/library/x-algorithm-optimizer) | Optimize X/Twitter for algorithm | `npx skills add shipshitdev/library --skill x-algorithm-optimizer` |
| [youtube-video-analyst](https://skills.sh/shipshitdev/library/youtube-video-analyst) | Deconstruct YouTube videos | `npx skills add shipshitdev/library --skill youtube-video-analyst` |

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
npx skills add shipshitdev/library -g --skill '*' -y

# Tactical execution
npx skills add coreyhaines31/marketingskills -g --skill '*' -y
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
npx skills add vercel-labs/agent-skills -g --skill '*' -y
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
npx skills add trailofbits/skills -g --skill '*' -y
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
npx skills add expo/skills -g --skill '*' -y
```

### [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills)

Massive community skill collection (610+ skills) covering nearly every development domain.

| Category | Example Skills |
|----------|---------------|
| **Frontend** | react-patterns, nextjs-best-practices, tailwind-patterns, svelte, vue |
| **Backend** | nestjs-expert, django-pro, fastapi-pro, rails, golang-pro |
| **Security** | penetration-testing, vulnerability-scanner, malware-analyst, red-team |
| **DevOps** | kubernetes-architect, terraform-specialist, docker, gitops |
| **AI/ML** | rag-engineer, ml-engineer, prompt-engineering, langchain |
| **Data** | data-engineer, database-architect, redis-expert, postgresql |
| **Testing** | tdd-workflows, playwright, vitest, e2e-testing-patterns |
| **Mobile** | react-native-architecture, flutter-expert, ios-developer |

```bash
npx skills add sickn33/antigravity-awesome-skills -g --skill '*' -y
```

### Other Community Repos

Smaller repos that provide focused skills:

| Repo | Skills | Install |
|------|--------|---------|
| [vercel-labs/skills](https://github.com/vercel-labs/skills) | find-skills | `npx skills add vercel-labs/skills -g --skill '*' -y` |
| [vercel/turborepo](https://github.com/vercel/turborepo) | turborepo | `npx skills add vercel/turborepo -g --skill '*' -y` |
| [resend/resend-skills](https://github.com/resend/resend-skills) | Email with Resend | `npx skills add resend/resend-skills -g --skill '*' -y` |
| [resend/email-best-practices](https://github.com/resend/email-best-practices) | Email best practices | `npx skills add resend/email-best-practices -g --skill '*' -y` |
| [glebis/claude-skills](https://github.com/glebis/claude-skills) | Claude utilities | `npx skills add glebis/claude-skills -g --skill '*' -y` |
| [pproenca/dot-skills](https://github.com/pproenca/dot-skills) | General dev | `npx skills add pproenca/dot-skills -g --skill '*' -y` |
| [lammesen/skills](https://github.com/lammesen/skills) | Additional skills | `npx skills add lammesen/skills -g --skill '*' -y` |
| [clawdbot/skills](https://github.com/clawdbot/skills) | Bot/automation | `npx skills add clawdbot/skills -g --skill '*' -y` |
| [SpillwaveSolutions/running-marketing-campaigns-agent-skill](https://github.com/SpillwaveSolutions/running-marketing-campaigns-agent-skill) | Marketing campaigns | `npx skills add SpillwaveSolutions/running-marketing-campaigns-agent-skill -g --skill '*' -y` |

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

# Install category bundles
/plugin install shipshitdev-startup@shipshitdev
/plugin install shipshitdev-testing@shipshitdev
/plugin install shipshitdev-frontend@shipshitdev
```
