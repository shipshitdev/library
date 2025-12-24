# Global Skills & Commands Repository

Centralized **global** skills and commands for Claude Code, OpenAI Codex, and Cursor.

## Directory Structure

```
skills/
├── .claude/
│   ├── skills/              # Claude global skills (42)
│   └── commands/            # Claude global commands
│
├── .codex/
│   ├── skills/              # Codex global skills (42)
│   └── commands/            # Codex global commands
│
└── .cursor/
    ├── skills/              # Cursor global skills (42)
    └── commands/            # Cursor global commands (24)
```

**Note:** All platforms now have complete skill parity (42 skills each). See [HARMONIZATION.md](HARMONIZATION.md) for details.

## How It Works

This repo is symlinked from each agent's home directory:

```
~/.claude/skills -> /Users/decod3rs/www/agenticindiedev/skills/.claude/skills
~/.codex/skills  -> /Users/decod3rs/www/agenticindiedev/skills/.codex/skills
~/.cursor/commands -> /Users/decod3rs/www/agenticindiedev/skills/.cursor/commands
~/.cursor/skills -> /Users/decod3rs/www/agenticindiedev/skills/.cursor/skills
```

Project repos can also symlink to specific skills here for shared functionality.

**Project Integration:**

- Projects can symlink to this repo for generic commands and skills
- Project-specific commands and skills remain in project workspace
- Skills adapt to project context by scanning project documentation

Edit skills/commands here, changes are immediately available to agents.

## Installation

This repository contains skills and commands that can be installed individually. Each item has its own installation instructions.

**Quick Start:**

1. Clone this repository
2. Choose the skills/commands you want to install
3. Follow the installation instructions in each item's directory

**Installation Methods:**

- **Symlink** (recommended): Automatically receive updates when the repository is updated
- **Copy**: Complete independence, customize without affecting source

See [INSTALL.md](INSTALL.md) for:

- Complete installation guide
- Registry of all available skills/commands
- Installation method comparison
- Troubleshooting

**Note:** Individual skill `INSTALL.md` files have been removed. Installation instructions are now in the root `INSTALL.md` file.

**Individual Installation:**

- **Commands**: Each command file (`.cursor/commands/*.md`) can be symlinked or copied to `~/.cursor/commands/`
- **Skills**: Each skill directory contains a `SKILL.md` file with usage instructions. Symlink the skill directory to `~/.cursor/skills/` or `~/.claude/skills/` or `~/.codex/skills/`

## Commands

**analyze-codebase** Generate comprehensive analysis of codebase structure, architecture, and organization.

Codex: N/A | Claude: N/A | Cursor: [`.cursor/commands/analyze-codebase.md`](.cursor/commands/analyze-codebase.md)

**api-test** Generate, run, and validate API tests for NestJS endpoints covering authentication, authorization, validation, error handling, and edge cases.

Codex: N/A | Claude: N/A | Cursor: [`.cursor/commands/api-test.md`](.cursor/commands/api-test.md)

**bug** Quick bug capture and documentation workflow for tracking issues and creating bug reports.

Codex: N/A | Claude: N/A | Cursor: [`.cursor/commands/bug.md`](.cursor/commands/bug.md)

**clean** Unified cleanup workflow for tasks and session files to maintain organized project structure.

Codex: N/A | Claude: N/A | Cursor: [`.cursor/commands/clean.md`](.cursor/commands/clean.md)

**code-review** Comprehensive code review workflow with security, performance, and best practices analysis.

Codex: N/A | Claude: N/A | Cursor: [`.cursor/commands/code-review.md`](.cursor/commands/code-review.md)

**deploy** Streamline deployment workflows for React, Next.js, NestJS applications to various environments (AWS, Vercel, etc.).

Codex: N/A | Claude: N/A | Cursor: [`.cursor/commands/deploy.md`](.cursor/commands/deploy.md)

**docs-generate** Generate comprehensive documentation from codebase including API docs, architecture diagrams, and guides.

Codex: N/A | Claude: N/A | Cursor: [`.cursor/commands/docs-generate.md`](.cursor/commands/docs-generate.md)

**docs-update** Update existing documentation to reflect codebase changes and maintain documentation accuracy.

Codex: N/A | Claude: N/A | Cursor: [`.cursor/commands/docs-update.md`](.cursor/commands/docs-update.md)

**end** Document session work and clear context before ending a development session.

Codex: N/A | Claude: N/A | Cursor: [`.cursor/commands/end.md`](.cursor/commands/end.md)

**inbox** Process inbox items and organize tasks from the project inbox into actionable items.

Codex: N/A | Claude: N/A | Cursor: [`.cursor/commands/inbox.md`](.cursor/commands/inbox.md)

**migrate** Manage MongoDB (and other database) migrations safely with version control and rollback capabilities.

Codex: N/A | Claude: N/A | Cursor: [`.cursor/commands/migrate.md`](.cursor/commands/migrate.md)

**new-cmd** Create new custom slash commands following established patterns and best practices.

Codex: N/A | Claude: N/A | Cursor: [`.cursor/commands/new-cmd.md`](.cursor/commands/new-cmd.md)

**new-session** Create new session files from templates for tracking development work and decisions.

Codex: N/A | Claude: N/A | Cursor: [`.cursor/commands/new-session.md`](.cursor/commands/new-session.md)

**optimize-prompt** Optimize AI prompts for better results, clarity, and effectiveness in agent interactions.

Codex: N/A | Claude: N/A | Cursor: [`.cursor/commands/optimize-prompt.md`](.cursor/commands/optimize-prompt.md)

**performance** Analyze and optimize performance for React, Next.js, NestJS applications covering frontend, backend, database, and infrastructure.

Codex: N/A | Claude: N/A | Cursor: [`.cursor/commands/performance.md`](.cursor/commands/performance.md)

**quick-fix** Daily task list management and quick fixes workflow for handling urgent issues.

Codex: N/A | Claude: N/A | Cursor: [`.cursor/commands/quick-fix.md`](.cursor/commands/quick-fix.md)

**refactor-code** Refactoring workflows for improving code quality, structure, and maintainability.

Codex: N/A | Claude: N/A | Cursor: [`.cursor/commands/refactor-code.md`](.cursor/commands/refactor-code.md)

**review-pr** Pull request review checklist and workflow for code quality and standards compliance.

Codex: N/A | Claude: N/A | Cursor: [`.cursor/commands/review-pr.md`](.cursor/commands/review-pr.md)

**scaffold** Unified project scaffolder for creating new projects or adding components to existing ones.

Codex: N/A | Claude: N/A | Cursor: [`.cursor/commands/scaffold.md`](.cursor/commands/scaffold.md)

**security-audit** Comprehensive security audit for React, Next.js, NestJS applications covering dependencies, code patterns, configuration, and best practices.

Codex: N/A | Claude: N/A | Cursor: [`.cursor/commands/security-audit.md`](.cursor/commands/security-audit.md)

**start** Bootstrap session context and initialize development environment for productive work sessions.

Codex: N/A | Claude: N/A | Cursor: [`.cursor/commands/start.md`](.cursor/commands/start.md)

**task** Create and manage tasks with PRDs, tracking, and documentation workflows.

Codex: N/A | Claude: N/A | Cursor: [`.cursor/commands/task.md`](.cursor/commands/task.md)

**test** Test tracking and management workflow for organizing and running test suites.

Codex: N/A | Claude: N/A | Cursor: [`.cursor/commands/test.md`](.cursor/commands/test.md)

**validate** Unified validation workflow for documentation, sessions, and tasks to ensure quality and completeness.

Codex: N/A | Claude: N/A | Cursor: [`.cursor/commands/validate.md`](.cursor/commands/validate.md)

## Skills

**accessibility** Expert in web accessibility (WCAG 2.1 AA compliance) for React/Next.js applications, ensuring all projects are usable by everyone.

Codex: [`.codex/skills/accessibility/`](.codex/skills/accessibility/) | Claude: [`.claude/skills/accessibility/`](.claude/skills/accessibility/) | Cursor: [`.cursor/skills/accessibility/`](.cursor/skills/accessibility/)

**agent-folder-init** Initialize a comprehensive `.agent/` folder structure for AI-first development workflows with session tracking, task management, and coding standards.

Codex: [`.codex/skills/agent-folder-init/`](.codex/skills/agent-folder-init/) | Claude: [`.claude/skills/agent-folder-init/`](.claude/skills/agent-folder-init/) | Cursor: [`.cursor/skills/agent-folder-init/`](.cursor/skills/agent-folder-init/)

**analytics-expert** Analyze content analytics data, create reports, identify trends, calculate ROI, and provide content optimization recommendations.

Codex: [`.codex/skills/analytics-expert/`](.codex/skills/analytics-expert/) | Claude: [`.claude/skills/analytics-expert/`](.claude/skills/analytics-expert/) | Cursor: [`.cursor/skills/analytics-expert/`](.cursor/skills/analytics-expert/)

**api-design-expert** Expert in RESTful API design, OpenAPI/Swagger documentation, versioning, error handling, and API best practices for NestJS applications.

Codex: [`.codex/skills/api-design-expert/`](.codex/skills/api-design-expert/) | Claude: [`.claude/skills/api-design-expert/`](.claude/skills/api-design-expert/) | Cursor: [`.cursor/skills/api-design-expert/`](.cursor/skills/api-design-expert/)

**artifacts-builder** Build and manage project artifacts, documentation, and deliverables from codebase and project structure.

Codex: [`.codex/skills/artifacts-builder/`](.codex/skills/artifacts-builder/) | Claude: [`.claude/skills/artifacts-builder/`](.claude/skills/artifacts-builder/) | Cursor: [`.cursor/skills/artifacts-builder/`](.cursor/skills/artifacts-builder/)

**changelog-generator** Generate user-facing changelogs from git commit history with categorization and formatting.

Codex: [`.codex/skills/changelog-generator/`](.codex/skills/changelog-generator/) | Claude: [`.claude/skills/changelog-generator/`](.claude/skills/changelog-generator/) | Cursor: [`.cursor/skills/changelog-generator/`](.cursor/skills/changelog-generator/)

**component-library** Maintain component library standards, patterns, and consistency across monorepo projects.

Codex: [`.codex/skills/component-library/`](.codex/skills/component-library/) | Claude: [`.claude/skills/component-library/`](.claude/skills/component-library/) | Cursor: [`.cursor/skills/component-library/`](.cursor/skills/component-library/)

**content-script-developer** Develop and maintain content scripts for browser extensions and web applications.

Codex: [`.codex/skills/content-script-developer/`](.codex/skills/content-script-developer/) | Claude: [`.claude/skills/content-script-developer/`](.claude/skills/content-script-developer/) | Cursor: [`.cursor/skills/content-script-developer/`](.cursor/skills/content-script-developer/)

**copywriter** Write compelling copy that adapts to project context, brand voice, and tone discovered from project documentation.

Codex: [`.codex/skills/copywriter/`](.codex/skills/copywriter/) | Claude: [`.claude/skills/copywriter/`](.claude/skills/copywriter/) | Cursor: [`.cursor/skills/copywriter/`](.cursor/skills/copywriter/)

**design-consistency-auditor** Audit and maintain design system consistency, UX/UI patterns, color palettes, and design best practices across frontend applications.

Codex: [`.codex/skills/design-consistency-auditor/`](.codex/skills/design-consistency-auditor/) | Claude: [`.claude/skills/design-consistency-auditor/`](.claude/skills/design-consistency-auditor/) | Cursor: [`.cursor/skills/design-consistency-auditor/`](.cursor/skills/design-consistency-auditor/)

**docs** Documentation expert for creating, maintaining, and organizing project documentation across all formats.

Codex: [`.codex/skills/docs/`](.codex/skills/docs/) | Claude: [`.claude/skills/docs/`](.claude/skills/docs/) | Cursor: [`.cursor/skills/docs/`](.cursor/skills/docs/)

**docusaurus-writer** Technical writing expert for Docusaurus documentation sites with API references, guides, and tutorials.

Codex: [`.codex/skills/docusaurus-writer/`](.codex/skills/docusaurus-writer/) | Claude: [`.claude/skills/docusaurus-writer/`](.claude/skills/docusaurus-writer/) | Cursor: [`.cursor/skills/docusaurus-writer/`](.cursor/skills/docusaurus-writer/)

**error-handling-expert** Expert in error handling patterns, exception management, error responses, logging, and error recovery strategies for React, Next.js, and NestJS applications.

Codex: [`.codex/skills/error-handling-expert/`](.codex/skills/error-handling-expert/) | Claude: [`.claude/skills/error-handling-expert/`](.claude/skills/error-handling-expert/) | Cursor: [`.cursor/skills/error-handling-expert/`](.cursor/skills/error-handling-expert/)

**expo-architect** Architect Expo/React Native applications with best practices, navigation, and mobile-specific patterns.

Codex: [`.codex/skills/expo-architect/`](.codex/skills/expo-architect/) | Claude: [`.claude/skills/expo-architect/`](.claude/skills/expo-architect/) | Cursor: [`.cursor/skills/expo-architect/`](.cursor/skills/expo-architect/)

**fullstack-workspace-init** Initialize fullstack workspace structure with monorepo support, frontend, backend, and shared packages.

Codex: [`.codex/skills/fullstack-workspace-init/`](.codex/skills/fullstack-workspace-init/) | Claude: [`.claude/skills/fullstack-workspace-init/`](.claude/skills/fullstack-workspace-init/) | Cursor: [`.cursor/skills/fullstack-workspace-init/`](.cursor/skills/fullstack-workspace-init/)

**gh-address-comments** Address and respond to GitHub comments and pull request feedback systematically.

Codex: [`.codex/skills/gh-address-comments/`](.codex/skills/gh-address-comments/) | Claude: [`.claude/skills/gh-address-comments/`](.claude/skills/gh-address-comments/) | Cursor: [`.cursor/skills/gh-address-comments/`](.cursor/skills/gh-address-comments/)

**gh-fix-ci** Automatically fix CI/CD pipeline issues in GitHub Actions workflows.

Codex: [`.codex/skills/gh-fix-ci/`](.codex/skills/gh-fix-ci/) | Claude: [`.claude/skills/gh-fix-ci/`](.claude/skills/gh-fix-ci/) | Cursor: [`.cursor/skills/gh-fix-ci/`](.cursor/skills/gh-fix-ci/)

**internal-comms** Generate internal communications, updates, company newsletters, and FAQ answers.

Codex: [`.codex/skills/internal-comms/`](.codex/skills/internal-comms/) | Claude: [`.claude/skills/internal-comms/`](.claude/skills/internal-comms/) | Cursor: [`.cursor/skills/internal-comms/`](.cursor/skills/internal-comms/)

**landing-page-vercel** Build and deploy landing pages optimized for Vercel with modern design and performance.

Codex: [`.codex/skills/landing-page-vercel/`](.codex/skills/landing-page-vercel/) | Claude: [`.claude/skills/landing-page-vercel/`](.claude/skills/landing-page-vercel/) | Cursor: [`.cursor/skills/landing-page-vercel/`](.cursor/skills/landing-page-vercel/)

**mcp-builder** Build and configure Model Context Protocol (MCP) servers and integrations.

Codex: [`.codex/skills/mcp-builder/`](.codex/skills/mcp-builder/) | Claude: [`.claude/skills/mcp-builder/`](.claude/skills/mcp-builder/) | Cursor: [`.cursor/skills/mcp-builder/`](.cursor/skills/mcp-builder/)

**micro-landing-builder** Build micro landing pages with customizable sections and templates using NextJS and shared UI components.

Codex: [`.codex/skills/micro-landing-builder/`](.codex/skills/micro-landing-builder/) | Claude: [`.claude/skills/micro-landing-builder/`](.claude/skills/micro-landing-builder/) | Cursor: [`.cursor/skills/micro-landing-builder/`](.cursor/skills/micro-landing-builder/)

**mongodb-migration-expert** Expert in MongoDB migration strategies, schema changes, and data transformations.

Codex: [`.codex/skills/mongodb-migration-expert/`](.codex/skills/mongodb-migration-expert/) | Claude: [`.claude/skills/mongodb-migration-expert/`](.claude/skills/mongodb-migration-expert/) | Cursor: [`.cursor/skills/mongodb-migration-expert/`](.cursor/skills/mongodb-migration-expert/)

**nestjs-queue-architect** Architect NestJS applications with BullMQ queues, workers, and asynchronous job processing patterns.

Codex: [`.codex/skills/nestjs-queue-architect/`](.codex/skills/nestjs-queue-architect/) | Claude: [`.claude/skills/nestjs-queue-architect/`](.claude/skills/nestjs-queue-architect/) | Cursor: [`.cursor/skills/nestjs-queue-architect/`](.cursor/skills/nestjs-queue-architect/)

**nestjs-testing-expert** Expert in testing strategies for NestJS applications including unit tests, integration tests, and E2E tests.

Codex: [`.codex/skills/nestjs-testing-expert/`](.codex/skills/nestjs-testing-expert/) | Claude: [`.claude/skills/nestjs-testing-expert/`](.claude/skills/nestjs-testing-expert/) | Cursor: [`.cursor/skills/nestjs-testing-expert/`](.cursor/skills/nestjs-testing-expert/)

**package-architect** Architect and structure npm packages, monorepo packages, and shared libraries.

Codex: [`.codex/skills/package-architect/`](.codex/skills/package-architect/) | Claude: [`.claude/skills/package-architect/`](.claude/skills/package-architect/) | Cursor: [`.cursor/skills/package-architect/`](.cursor/skills/package-architect/)

**performance-expert** Expert in performance optimization for React, Next.js, NestJS applications covering frontend rendering, API response times, database queries, and infrastructure optimization.

Codex: [`.codex/skills/performance-expert/`](.codex/skills/performance-expert/) | Claude: [`.claude/skills/performance-expert/`](.claude/skills/performance-expert/) | Cursor: [`.cursor/skills/performance-expert/`](.cursor/skills/performance-expert/)

**planning-assistant** Help with content planning, calendar management, research organization, content ideation, and multi-platform planning.

Codex: [`.codex/skills/planning-assistant/`](.codex/skills/planning-assistant/) | Claude: [`.claude/skills/planning-assistant/`](.claude/skills/planning-assistant/) | Cursor: [`.cursor/skills/planning-assistant/`](.cursor/skills/planning-assistant/)

**plasmo-extension-architect** Architect browser extensions using Plasmo framework with React, TypeScript, and modern web APIs.

Codex: [`.codex/skills/plasmo-extension-architect/`](.codex/skills/plasmo-extension-architect/) | Claude: [`.claude/skills/plasmo-extension-architect/`](.claude/skills/plasmo-extension-architect/) | Cursor: [`.cursor/skills/plasmo-extension-architect/`](.cursor/skills/plasmo-extension-architect/)

**project-scaffold** Unified project scaffolder for creating new projects or adding components to existing ones, supporting backend, frontend, mobile, and extension projects.

Codex: [`.codex/skills/project-scaffold/`](.codex/skills/project-scaffold/) | Claude: [`.claude/skills/project-scaffold/`](.claude/skills/project-scaffold/) | Cursor: [`.cursor/skills/project-scaffold/`](.cursor/skills/project-scaffold/)

**prompt-engineer** Engineer and optimize prompts for AI agents, LLMs, and AI-powered applications.

Codex: [`.codex/skills/prompt-engineer/`](.codex/skills/prompt-engineer/) | Claude: [`.claude/skills/prompt-engineer/`](.claude/skills/prompt-engineer/) | Cursor: [`.cursor/skills/prompt-engineer/`](.cursor/skills/prompt-engineer/)

**qa-reviewer** Quality assurance review assistance for systematically reviewing AI agent work, code quality, and feature completeness.

Codex: [`.codex/skills/qa-reviewer/`](.codex/skills/qa-reviewer/) | Claude: [`.claude/skills/qa-reviewer/`](.claude/skills/qa-reviewer/) | Cursor: [`.cursor/skills/qa-reviewer/`](.cursor/skills/qa-reviewer/)

**react-native-components** Build and maintain React Native components with platform-specific patterns and best practices.

Codex: [`.codex/skills/react-native-components/`](.codex/skills/react-native-components/) | Claude: [`.claude/skills/react-native-components/`](.claude/skills/react-native-components/) | Cursor: [`.cursor/skills/react-native-components/`](.cursor/skills/react-native-components/)

**roadmap-analyzer** Analyze and plan product roadmaps based on user needs, priorities, and feature requirements.

Codex: [`.codex/skills/roadmap-analyzer/`](.codex/skills/roadmap-analyzer/) | Claude: [`.claude/skills/roadmap-analyzer/`](.claude/skills/roadmap-analyzer/) | Cursor: [`.cursor/skills/roadmap-analyzer/`](.cursor/skills/roadmap-analyzer/)

**rules-capture** Automatically detect and document coding rules, patterns, and conventions from codebase analysis.

Codex: [`.codex/skills/rules-capture/`](.codex/skills/rules-capture/) | Claude: [`.claude/skills/rules-capture/`](.claude/skills/rules-capture/) | Cursor: [`.cursor/skills/rules-capture/`](.cursor/skills/rules-capture/)

**security-expert** Expert in application security, OWASP Top 10, authentication, authorization, data protection, and security best practices for React, Next.js, and NestJS applications.

Codex: [`.codex/skills/security-expert/`](.codex/skills/security-expert/) | Claude: [`.claude/skills/security-expert/`](.claude/skills/security-expert/) | Cursor: [`.cursor/skills/security-expert/`](.cursor/skills/security-expert/)

**serializer-specialist** Specialist in data serialization, deserialization, and transformation patterns for APIs and data pipelines.

Codex: [`.codex/skills/serializer-specialist/`](.codex/skills/serializer-specialist/) | Claude: [`.claude/skills/serializer-specialist/`](.claude/skills/serializer-specialist/) | Cursor: [`.cursor/skills/serializer-specialist/`](.cursor/skills/serializer-specialist/)

**session-documenter** Automatically document session work, decisions, and context for continuity across development sessions.

Codex: [`.codex/skills/session-documenter/`](.codex/skills/session-documenter/) | Claude: [`.claude/skills/session-documenter/`](.claude/skills/session-documenter/) | Cursor: [`.cursor/skills/session-documenter/`](.cursor/skills/session-documenter/)

**skill-creator** Guide for creating effective skills that extend agent capabilities with specialized knowledge, workflows, or tool integrations.

Codex: [`.codex/skills/skill-creator/`](.codex/skills/skill-creator/) | Claude: [`.claude/skills/skill-creator/`](.claude/skills/skill-creator/) | Cursor: [`.cursor/skills/skill-creator/`](.cursor/skills/skill-creator/)

**strategy-expert** Assist with content strategy, persona building, competitive analysis, content planning, and brand voice consistency.

Codex: [`.codex/skills/strategy-expert/`](.codex/skills/strategy-expert/) | Claude: [`.claude/skills/strategy-expert/`](.claude/skills/strategy-expert/) | Cursor: [`.cursor/skills/strategy-expert/`](.cursor/skills/strategy-expert/)

**testing-expert** Expert in testing strategies for React, Next.js, and NestJS applications covering unit tests, integration tests, E2E tests, and testing best practices.

Codex: [`.codex/skills/testing-expert/`](.codex/skills/testing-expert/) | Claude: [`.claude/skills/testing-expert/`](.claude/skills/testing-expert/) | Cursor: [`.cursor/skills/testing-expert/`](.cursor/skills/testing-expert/)

**webapp-testing** Web application testing assistance and automation for creating test scripts and validating functionality.

Codex: [`.codex/skills/webapp-testing/`](.codex/skills/webapp-testing/) | Claude: [`.claude/skills/webapp-testing/`](.claude/skills/webapp-testing/) | Cursor: [`.cursor/skills/webapp-testing/`](.cursor/skills/webapp-testing/)

**workflow-automation** Design content workflows, create process documentation, implement automation rules, design approval processes, and optimize content pipelines.

Codex: [`.codex/skills/workflow-automation/`](.codex/skills/workflow-automation/) | Claude: [`.claude/skills/workflow-automation/`](.claude/skills/workflow-automation/) | Cursor: [`.cursor/skills/workflow-automation/`](.cursor/skills/workflow-automation/)

## Adding Skills & Commands

### Adding Commands

1. Create a new `.md` file in `.cursor/commands/`
2. Follow the naming convention: `{verb}-{noun}.md` (e.g., `analyze-codebase.md`, `review-pr.md`)
3. Use standard `.agent/` folder structure:
   - `.agent/SYSTEM/` - Architecture, rules, summary
   - `.agent/SESSIONS/` - Session documentation
   - `.agent/TASKS/` - Task files
   - `.agent/PRDS/` - Product requirement documents
   - `.agent/EXAMPLES/` - Code examples
4. Use placeholders only for project-specific paths:
   - `[project]` - Project name/path
   - `[frontend-project]` - Frontend project path
   - `[backend-project]` - Backend project path
5. Update `.cursor/commands/README.md` with the new command

See `GENERICIZATION.md` for detailed guidelines on making commands generic.

### Adding Skills

1. Create a new directory in `.cursor/skills/` (or `.claude/skills/`, `.codex/skills/`)
2. Add `SKILL.md` file with YAML frontmatter
3. Include instructions and examples
4. Update the appropriate skills `README.md` with the new skill

```bash
# Cursor skill
mkdir -p .cursor/skills/my-skill
touch .cursor/skills/my-skill/SKILL.md

# Claude skill
mkdir -p .claude/skills/my-skill
touch .claude/skills/my-skill/SKILL.md

# Codex skill
mkdir -p .codex/skills/my-skill
touch .codex/skills/my-skill/SKILL.md
```

## Skill Format

```
skill-name/
├── README.md           # Description, usage
├── SKILL.md            # Main prompt/instructions (or skill.md)
├── scripts/            # Optional automation
└── templates/          # Optional templates
```

## Documentation

- `INSTALL.md` - Complete installation guide for all skills/commands
- `.cursor/commands/README.md` - Cursor commands reference
- `.cursor/skills/README.md` - Cursor skills reference

**Note:** Installation boilerplate has been removed from individual command files and skill directories. All installation instructions are centralized in the root `INSTALL.md` file.

## How Skills Adapt to Projects

Skills in this repository are designed to be **adaptive**:

1. **Discover Project Context**: Skills scan project documentation (`.agent/SYSTEM/`, `.agent/SOP/`, etc.) to understand:

   - Project architecture and structure
   - Brand voice and tone
   - Existing patterns and conventions
   - Terminology and style

2. **Use Project-Specific Skills**: If a project has its own skill (e.g., `[project]-analytics-expert`), the generic skill will collaborate with or defer to it

3. **Adapt to Project Patterns**: Skills match the project's:
   - Documentation style
   - Code patterns
   - Naming conventions
   - Workflow processes
