# New Command: Create Custom Claude Commands

Guide for creating new Claude Code CLI commands with best practices and patterns.

## Purpose

This meta-command helps you create well-structured, maintainable slash commands that follow established patterns and conventions.

## Interview Process

When a user requests a new command, follow these 5 steps:

### Step 1: Understand Purpose & Users

**Ask clarifying questions:**

- What task should this command automate?
- Who will use it? (just you, team, open source)
- What's the expected frequency? (daily, weekly, rarely)
- What's the primary goal? (speed, consistency, learning)

**Example:**

```
User: "I want a command to sync our staging database"

Questions to ask:
- Which direction? (production → staging or staging → production)
- Include schema only or data too?
- Any safety checks needed? (confirmations, backups)
- Should it handle migrations?
```

### Step 2: Research Similar Commands

**Check existing commands:**

```bash
# List current commands
ls .cursor/commands/

# Read similar commands for patterns
cat .cursor/commands/*.md
```

**Identify patterns to reuse:**

- Command structure (phases, workflows)
- Safety checks (confirmations, validations)
- Error handling approaches
- Output formatting

**Common patterns found:**

- GitHub commands start with `gh-`
- Multi-phase workflows (Fetch → Analyze → Execute → Report)
- Interactive selection menus
- Safety confirmations for destructive actions

### Step 3: Determine Directory Location

**Choose between project or user directory:**

**Project Directory** (`.cursor/commands/`)

- Codebase-specific commands
- Team collaboration features
- Project workflow automation
- Examples: project setup, deploy, test

**User Directory** (`~/.cursor/commands/`)

- General-purpose utilities
- Personal workflow tools
- Cross-project functionality
- Examples: git helpers, file operations

**Project Context:**
Most commands should go in `.cursor/commands/` because:

- Team uses the same monorepo
- Consistent workflows across developers
- Project-specific patterns (NestJS, monorepo, etc.)

**Use user directory only for:**

- Personal productivity scripts
- Cross-project tools
- Experimental commands

### Step 4: Follow Structural Patterns

**Standard command structure:**

```markdown
# Command Name: Brief Description

One-line summary of what this command does.

## Purpose
[Why this command exists, what problem it solves]

## Workflow

### Phase 1: [Name]
[What happens in this phase]

### Phase 2: [Name]
[What happens in this phase]

## Usage Examples
```bash
/command-name           # Basic usage
/command-name arg       # With argument
```

## Safety & Error Handling

[Warnings, confirmations, edge cases]

## Output Format

[What the user will see]

```

**For GitHub commands specifically:**
```markdown
# GitHub Command Pattern

## Phase 1: Fetch Data
- Use `gh` CLI commands
- Authenticate if needed
- Handle different input formats

## Phase 2: Analysis
- Parse data
- Categorize findings
- Present options

## Phase 3: Action
- Apply changes
- Show progress
- Confirm completion

## Phase 4: Summary
- Show what changed
- Suggest next steps
```

### Step 5: Generate, Test & Validate

**Create the command:**

1. Write the command file
2. Include usage examples
3. Document all options
4. Add safety checks
5. Show expected output

**Test immediately:**

```bash
# Try the command
/new-command

# Verify it works as expected
# Check error handling
# Validate output format
```

**Iterate based on feedback:**

- Did it do what you expected?
- Is the output clear?
- Are there missing edge cases?
- Does it follow project patterns?

## Common Patterns

### Naming Conventions

**Prefix patterns:**

- `gh-*` - GitHub operations (gh-review-pr, gh-fix-ci)
- `db-*` - Database operations (db-sync, db-backup)
- `deploy-*` - Deployment tasks (deploy-staging, deploy-prod)
- `test-*` - Testing helpers (test-coverage, test-e2e)

**Verb-first naming:**

- `make-tests` - Create tests
- `fix-ci` - Fix CI issues
- `review-pr` - Review pull request

**Avoid:**

- Generic names (run, do, execute)
- Unclear abbreviations (mk, fx, rv)
- Overly long names (create-comprehensive-test-suite-with-coverage)

### Workflow Structures

**Single-Phase (Simple Commands):**

```markdown
## Workflow
1. Validate input
2. Execute action
3. Show result
```

**Multi-Phase (Complex Commands):**

```markdown
## Phase 1: Setup
[Gather information, validate prerequisites]

## Phase 2: Analysis
[Process data, identify patterns]

## Phase 3: Execution
[Apply changes, show progress]

## Phase 4: Summary
[Report results, suggest next steps]
```

**Interactive Workflows:**

```markdown
## Workflow
1. Present options
2. Get user selection
3. Process each selection
4. Confirm completion
5. Offer follow-up actions
```

### Safety Practices

**Always include:**

**1. Confirmation for Destructive Actions:**

```markdown
⚠️  Warning: This will delete 15 files

Files to delete:
  - temp-notes.md
  - debug-output.log
  [...]

Continue? (y/n)
```

**2. Branch Protection:**

```markdown
⚠️  Warning: You're on the main branch

This operation should use a feature branch.
Create one now? (y/n)
```

**3. Uncommitted Changes Check:**

```markdown
⚠️  Uncommitted changes detected

Options:
1. Stash changes
2. Commit first
3. Cancel
```

**4. Dry Run Mode:**

```markdown
## Safety Features
- Always dry run first (show what would change)
- Require explicit confirmation
- Display before/after comparisons
```

### Output Standards

**Structured Sections:**

```markdown
📋 SECTION NAME
[Content here]

🔍 ANOTHER SECTION
[Content here]

✅ COMPLETION
[Summary here]
```

**Status Indicators:**

- ✅ Success / Completed
- ❌ Error / Failed
- ⚠️ Warning / Attention needed
- 🔄 In progress
- 💡 Suggestion / Tip
- 📋 Information
- 🔍 Analysis / Review

**Progress Tracking:**

```markdown
Processing items... [3/10]

✅ Item 1 completed
✅ Item 2 completed
🔄 Item 3 in progress
⏳ Items 4-10 pending
```

**Clear Next Steps:**

```markdown
💡 Next Steps:
1. Review changes with: git diff
2. Run tests: npm test
3. Commit: git commit -m "message"
4. Push: git push
```

### Code Examples

**Bash Commands:**

```markdown
## Implementation

Use these GitHub CLI commands:
```bash
# Fetch PR data
gh pr view <number> --json title,body,author

# Get diff
gh pr diff <number>

# Check status
gh pr checks <number>
```

```

**Error Handling:**
```markdown
## Error Handling

**Authentication Failed:**
```

❌ Error: GitHub authentication required
Run: gh auth login

```

**Invalid Input:**
```

❌ Error: Invalid PR number
Usage: /command <pr-number>
Example: /command 123

```

**Not in Git Repo:**
```

❌ Error: Not a git repository
Run this command from inside a git repo

```
```

## Monorepo Patterns

### Monorepo Commands

When creating commands for monorepo projects:

**Package-Aware:**

```markdown
## Workflow
1. Detect which packages changed
2. Run operations per package
3. Handle inter-package dependencies
4. Show results grouped by package
```

**Example:**

```bash
# Build specific package
/build @[project]/api

# Test all affected packages
/test-affected

# Lint changed packages only
/lint-changed
```

### NestJS Commands

**Service Generation:**

```bash
/generate-service users
# Creates: service, controller, module, DTO, tests
```

**API Testing:**

```bash
/test-api /users
# Runs integration tests for specific endpoint
# Shows request/response examples
```

### Documentation Commands

**Update Project Memory:**

```bash
/update-prd "feature-name"
# Reviews .agents/memory/ files for the feature area
# Flags outdated documentation in memory files
```

**Architecture Sync:**

```bash
/sync-arch
# Updates .agents/memory/repo_architecture.md
# Reflects current package structure
```

### Compliance Commands

**Check Critical Rules:**

```bash
/check-rules
# Validates against CLAUDE.md (repo-level) rules
# Scans for violations before commit
```

### ⚠️ Critical Project Rules for Commands

When creating ANY command for a project, ALWAYS include these patterns:

**1. Reference Critical Rules First:**

```markdown
## Before Execution

**⚠️ Check critical rules:**
```bash
cat CLAUDE.md          # Repo-level rules
cat ~/.claude/CLAUDE.md # Global rules
```

Ensure command doesn't violate:

- ❌ No console.log (use logger service)
- ❌ No `any` types (strict TypeScript)
- ❌ No inline interfaces (use shared packages)
- ❌ No test execution locally (kills dev machine)
- ❌ No deletedAt (use isDeleted: boolean)
- ❌ No serializers in API repo
- ✅ Multi-tenancy always enforced

```

**2. Never Run Tests Locally:**
```markdown
## Test Execution Rule

⚠️ **CRITICAL:** Tests NEVER run locally (check project rules)

❌ WRONG:
```bash
pnpm test
npm run test:coverage
vitest run
```

✅ CORRECT:

```bash
# Write tests, commit, push to GitHub
git add .
git commit -m "test: add user service tests"
git push origin feature-branch

# Monitor on GitHub Actions
gh run watch
```

```

**3. Monorepo Structure Awareness:**
```markdown
## Monorepo Structure

Protected files across ALL projects:
- `AGENTS.md` (shared instructions) and `CLAUDE.md` when Claude-specific additions are needed
- `**/.agents/**` (All documentation)
- `**/README.md` (Standard docs)

Projects:
- `[api-project]/` - Backend (NestJS, MongoDB)
- `[frontend-project]/` - Frontend (Next.js monorepo)
- `[extension-project]/` - Browser extension (Plasmo)
- `[mobile-project]/` - Mobile app (Expo)
- `[docs-project]/` - Documentation (Docusaurus)
- `[packages-project]/` - Shared packages
```

**4. GitHub Actions Integration:**

```markdown
## CI/CD Commands

Use GitHub CLI for workflow operations:
```bash
# Check workflows
gh workflow list

# Monitor runs
gh run watch
gh run list --limit 10

# View logs
gh run view <run-id> --log-failed

# Re-run failed
gh run rerun <run-id> --failed
```

Common workflows (in project directories):

- `[api-project]/.github/workflows/deploy-production.yml`
- `[api-project]/.github/workflows/quality-gates.yml`
- `[frontend-project]/.github/workflows/staging.yml`
- `[frontend-project]/.github/workflows/ci.yml`
- `[packages-project]/.github/workflows/build.yml`

```

**5. Package Location Rules:**
```markdown
## Architecture Patterns

Serializers location:
```

[packages-project]/packages/common/serializers/

```

Interfaces location:
```

[packages-project]/packages/*/interfaces/
[packages-project]/packages/*/props/

```

Database patterns:
- Use `isDeleted: boolean` (NOT deletedAt)
- Always filter by `organization: orgId` (if multi-tenant)
- Indexes in module useFactory, NOT schema
```

### Existing Command Patterns

Reference these commands for patterns:

```bash
ls .cursor/commands/

# Current commands:
/de-slop      # Clean AI artifacts, monorepo-aware
/gh-fix-ci    # Auto-fix CI, uses GitHub Actions
/new-cmd      # This meta-command
```

**Common patterns used:**

1. **Check critical rules first** - Read the applicable AGENTS.md chain and Claude-specific CLAUDE.md when relevant
2. **Never run tests locally** - Push to GitHub Actions instead
3. **Monorepo-aware** - Handle multiple packages correctly
4. **GitHub Actions integration** - Use `gh` CLI for CI/CD
5. **Multi-tenancy checks** - Verify organization isolation
6. **Logger service** - No console.log statements
7. **Type safety** - No `any` types, interfaces in packages

## Complete Example

**Creating a Database Sync Command:**

```markdown
# DB Sync: Synchronize Staging Database

Safely sync production database schema to staging environment.

## Purpose

Automate the process of keeping staging database schema in sync with production, with built-in safety checks and rollback capability.

## Workflow

### Phase 1: Safety Checks

**Verify environment:**
```bash
# Check current environment
echo $NODE_ENV

# Must be 'staging'
if [ "$NODE_ENV" != "staging" ]; then
  echo "❌ Error: Can only sync to staging"
  exit 1
fi
```

**Confirm action:**

```
⚠️  Warning: This will update staging database schema

Current staging schema: v1.2.3
Production schema: v1.3.0

This will:
- Apply 5 new migrations
- Update 3 tables
- No data loss expected

Continue? (y/n)
```

### Phase 2: Backup

**Create backup:**

```bash
# Backup staging database
pg_dump $STAGING_DB_URL > backup-$(date +%Y%m%d-%H%M%S).sql

# Confirm backup created
ls -lh backup-*.sql
```

### Phase 3: Sync Schema

**Run migrations:**

```bash
# Run Prisma migrations
npx prisma migrate deploy

# Or run custom migrations
npm run migrate:staging
```

**Show progress:**

```
Running migrations...

✅ 20240101_add_users_table.sql
✅ 20240102_add_posts_table.sql
✅ 20240103_add_comments_table.sql
🔄 20240104_add_analytics_table.sql (in progress)
⏳ 20240105_add_indexes.sql (pending)
```

### Phase 4: Verification

**Test database:**

```bash
# Run smoke tests
npm run test:db

# Verify tables exist
psql $STAGING_DB_URL -c "\dt"
```

**Summary:**

```
✅ DATABASE SYNC COMPLETE

Applied: 5 migrations
Updated: 3 tables
Backup: backup-20241026-143022.sql

Staging schema: v1.2.3 → v1.3.0

💡 Next Steps:
1. Run integration tests: npm run test:e2e
2. Verify API endpoints work
3. If issues, rollback: /db-rollback backup-20241026-143022.sql
```

## Safety Features

- ✅ Environment validation (staging only)
- ✅ Automatic backup before changes
- ✅ User confirmation required
- ✅ Rollback capability
- ✅ Verification tests after sync

## Usage Examples

```bash
/db-sync              # Interactive sync with prompts
/db-sync --force      # Skip confirmation (dangerous!)
/db-sync --dry-run    # Show what would change
```

## Error Handling

**Wrong Environment:**

```
❌ Error: Cannot sync production database
This command only works in staging environment
Current: production
```

**Backup Failed:**

```
❌ Error: Backup creation failed
Cannot proceed without backup
Check disk space and permissions
```

**Migration Failed:**

```
❌ Error: Migration failed at step 3/5

Failed: 20240104_add_analytics_table.sql
Error: Column 'user_id' already exists

Rollback? (y/n)
```

## Rollback Procedure

If sync fails:

```bash
# Automatic rollback triggered
🔄 Rolling back to previous state...

# Restore from backup
psql $STAGING_DB_URL < backup-20241026-143022.sql

✅ Rollback complete
Database restored to previous state
```

```

## Usage

```bash
# Create a new command
/new-cmd

# Follow the prompts to:
# 1. Describe the command purpose
# 2. Review similar patterns
# 3. Choose location (project/user)
# 4. Generate command structure
# 5. Test and iterate
```

## Creation Output Format

When creating a new command, show:

```
📝 CREATING NEW COMMAND

Command: /db-sync
Location: .cursor/commands/db-sync.md
Type: Infrastructure automation

📋 STRUCTURE GENERATED

Sections:
✅ Purpose & description
✅ Multi-phase workflow
✅ Safety checks & confirmations
✅ Usage examples
✅ Error handling
✅ Rollback procedures

📄 FILE CREATED

Location: .cursor/commands/db-sync.md
Size: 2.4 KB

💡 NEXT STEPS

1. Test the command: /db-sync
2. Refine based on feedback
3. Document in team wiki
4. Share with team

Try it now? (y/n)
```

## Best Practices Summary

**DO:**

- ✅ Use clear, descriptive names
- ✅ Include safety confirmations
- ✅ Show examples
- ✅ Handle errors gracefully
- ✅ Display progress clearly
- ✅ Suggest next steps
- ✅ Follow existing patterns

**DON'T:**

- ❌ Skip error handling
- ❌ Make destructive changes without confirmation
- ❌ Use unclear abbreviations
- ❌ Forget to document usage
- ❌ Ignore existing command patterns
- ❌ Create overly complex commands (split into multiple if needed)

## Advanced: Command Composition

Create commands that call other commands:

```markdown
# Deploy All: Full Deployment Pipeline

Orchestrates multiple commands in sequence.

## Workflow

1. Run tests: `/make-tests --all`
2. Check linting: `/lint-all`
3. Build packages: `/build-all`
4. Deploy staging: `/deploy-staging`
5. Run smoke tests: `/test-e2e staging`
6. Deploy production: `/deploy-prod`

Each step must pass before proceeding to next.
```

This allows building complex workflows from simple, reusable commands.
