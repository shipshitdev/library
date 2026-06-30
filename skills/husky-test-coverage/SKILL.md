---
name: husky-test-coverage
description: Sets up or verifies Husky git hooks to enforce test coverage above 80% (configurable) for Node.js/TypeScript projects. Activates when enforcing coverage through pre-commit hooks, verifying existing Husky/test setup, or configuring coverage thresholds for Jest, Vitest, or Mocha test runners.
metadata:
  version: "1.0.0"
  tags: "husky, testing, coverage"
---

# Husky Test Coverage

Set up or verify Husky git hooks to ensure tests run and coverage thresholds are enforced on every commit.

## When to Use

- Setting up test coverage enforcement for the first time
- Verifying existing Husky/test setup is correctly configured
- Configuring pre-commit hooks for test coverage
- Adapting coverage setup to different test runners

## Project Context Discovery

1. **Check package.json:**
   - Review existing test scripts
   - Detect test runner from dependencies (jest, vitest, mocha)
   - Check for existing Husky installation
   - Review existing coverage configuration

2. **Identify Test Runner:**
   - Jest: Check for `jest` in dependencies, look for `jest.config.js` or `jest.config.json`
   - Vitest: Check for `vitest` in dependencies, look for `vitest.config.ts` or `vitest.config.js`
   - Mocha: Check for `mocha` in dependencies, check for coverage tool (nyc, c8)

3. **Check Coverage Configuration:**
   - Jest: Look for `coverageThreshold` in jest.config.*
   - Vitest: Look for `coverage.thresholds` in vitest.config.*
   - Mocha: Look for `.nycrc.json` or coverage config in package.json

4. **Verify Existing Husky Setup:**
   - Check if `.husky/` directory exists
   - Review existing pre-commit hook
   - Check if Husky is in package.json dependencies

5. **Detect Test Files:**
   - Scan for `*.test.*` or `*.spec.*` files
   - Verify tests exist before enforcing coverage

## Quick Start

```bash
# Basic setup (80% coverage threshold, blocks commits below threshold)
python3 ${CLAUDE_SKILL_DIR}/scripts/setup-husky-coverage.py \
  --root /path/to/project

# Custom threshold (85%)
python3 ${CLAUDE_SKILL_DIR}/scripts/setup-husky-coverage.py \
  --root /path/to/project \
  --threshold 85

# Warn only (don't block commits)
python3 ${CLAUDE_SKILL_DIR}/scripts/setup-husky-coverage.py \
  --root /path/to/project \
  --no-fail-on-below

# Skip if no tests found
python3 ${CLAUDE_SKILL_DIR}/scripts/setup-husky-coverage.py \
  --root /path/to/project \
  --skip-if-no-tests

# Dry run to preview changes
python3 ${CLAUDE_SKILL_DIR}/scripts/setup-husky-coverage.py \
  --root /path/to/project \
  --dry-run
```

## What Gets Configured

### Husky Setup

- Installs Husky if not already present
- Initializes Husky (`bunx husky install`)
- Creates `.husky/pre-commit` hook that runs tests with coverage
- Adds `prepare` script to package.json (if missing)

### Test Runner Detection

The skill automatically detects:

- **Jest**: Uses `jest --coverage --watchAll=false` in pre-commit hook
- **Vitest**: Uses `vitest --coverage --run` in pre-commit hook
- **Mocha**: Uses `nyc` or `c8` with mocha test command

### Coverage Configuration

**Jest:**

- Creates or updates `jest.config.json` with `coverageThreshold`
- Default thresholds: 80% lines, 75% branches, 80% functions, 80% statements

**Vitest:**

- Creates or updates `vitest.config.ts/js` with coverage thresholds
- Configures v8 coverage provider
- Sets same default thresholds as Jest

**Mocha + nyc:**

- Creates or updates `.nycrc.json` with coverage thresholds
- Configures text, html, and lcov reporters

### Pre-commit Hook

The created hook:

- Runs tests with coverage before every commit
- Fails the commit if coverage is below threshold (configurable)
- Can skip if no test files are found (optional)

## Configuration Options

### Command Line Arguments

- `--root <path>`: Project root directory (required)
- `--threshold <number>`: Coverage threshold percentage (default: 80)
- `--fail-on-below`: Fail commit if coverage below threshold (default: true)
- `--no-fail-on-below`: Allow commit even if coverage below threshold
- `--skip-if-no-tests`: Skip hook if no test files found
- `--dry-run`: Show what would be done without making changes

### Configuration File

Create `.husky-test-coverage.json` in project root:

```json
{
  "coverageThreshold": {
    "lines": 80,
    "branches": 75,
    "functions": 80,
    "statements": 80
  },
  "failOnCoverageBelowThreshold": true,
  "skipIfNoTests": false
}
```

### Package.json Configuration

Alternatively, add to `package.json`:

```json
{
  "huskyTestCoverage": {
    "threshold": 80,
    "failOnBelow": true
  }
}
```

## Tech Stack Adaptation

### Jest Projects

**Detection:**

- Checks for `jest` in dependencies
- Looks for `jest.config.js` or `jest.config.json`

**Configuration:**

- Updates or creates `jest.config.json` with coverage thresholds
- Pre-commit hook: `bun run test -- --coverage --watchAll=false`

**Example jest.config.json:**

```json
{
  "coverageThreshold": {
    "global": {
      "lines": 80,
      "branches": 75,
      "functions": 80,
      "statements": 80
    }
  }
}
```

### Vitest Projects

**Detection:**

- Checks for `vitest` in dependencies
- Looks for `vitest.config.ts` or `vitest.config.js`

**Configuration:**

- Updates or creates Vitest config with coverage thresholds
- Pre-commit hook: `bun run test -- --coverage --run`

**Example vitest.config.ts:**

```typescript
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      thresholds: {
        lines: 80,
        branches: 75,
        functions: 80,
        statements: 80
      }
    }
  }
})
```

### Mocha Projects

**Detection:**

- Checks for `mocha` in dependencies
- Checks for coverage tool (`nyc` or `c8`)

**Configuration:**

- Creates or updates `.nycrc.json` for nyc
- Pre-commit hook: `nyc --reporter=text --reporter=html bun run test`

**Example .nycrc.json:**

```json
{
  "check-coverage": true,
  "lines": 80,
  "branches": 75,
  "functions": 80,
  "statements": 80,
  "reporter": ["text", "text-summary", "html", "lcov"]
}
```

## Package Manager Support

The skill automatically detects and uses:

- **bun**: `bun run test` (preferred)
- **yarn**: `yarn test`
- **pnpm**: `pnpm run test`

## Workflow

1. Scan package.json for test runner, dependencies, existing Husky config, and coverage config files. Verify test files exist.
2. Identify Jest, Vitest, or Mocha; detect coverage tool (built-in or nyc/c8); determine package manager.
3. Install Husky if missing; initialize hooks; add `prepare` script if needed.
4. Create or update coverage configuration; set thresholds (default 80%); configure reporters.
5. Generate pre-commit hook script; set enforcement behavior (block or warn).
6. Verify setup; test hook with a commit; adjust thresholds if needed.

## Integration with Other Skills

| Skill | How It Works Together |
|-------|----------------------|
| **fullstack-workspace-init** | Auto-invoked after scaffolding; sets Vitest + 80% threshold + CI/CD. Run this skill separately only when adding to an existing project. |
| **linter-formatter-init** | Both configure Husky; this skill covers test coverage, linter-formatter-init covers linting/formatting |
| **testing-expert** | Uses testing patterns and coverage targets from testing-expert skill |

### Manual Integration (existing projects)

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/setup-husky-coverage.py \
  --root /path/to/project \
  --threshold 80
```

## Troubleshooting

### Pre-commit hook not running

```bash
# Reinstall Husky
bunx husky install
chmod +x .husky/pre-commit
```

### Coverage not being checked

- Verify test command includes coverage flag
- Check coverage configuration file exists and is correct
- Ensure coverage tool is installed (nyc/c8 for Mocha)

### Hook fails even when tests pass

- Check coverage thresholds are achievable
- Review coverage report to see what's below threshold
- Consider adjusting thresholds or improving test coverage

### Tests run but coverage not enforced

- Verify coverage configuration file has correct thresholds
- Check test runner supports coverage (Jest/Vitest have built-in, Mocha needs nyc/c8)
- Review pre-commit hook script for correct command

### Multiple test runners detected

The skill uses the first detected runner in priority order: Vitest > Jest > Mocha

## Resources

- Husky Documentation: https://typicode.github.io/husky/
- Jest Coverage: https://jestjs.io/docs/configuration#coveragethreshold-object
- Vitest Coverage: https://vitest.dev/config/#coverage
- nyc (Istanbul): https://github.com/istanbuljs/nyc
