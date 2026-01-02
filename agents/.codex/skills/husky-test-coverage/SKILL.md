---
name: husky-test-coverage
description: Set up or verify Husky git hooks to ensure all tests run and coverage stays above 80% (configurable) for Node.js/TypeScript projects. Use when users want to enforce test coverage through pre-commit hooks, verify existing Husky/test setup, or configure coverage thresholds for Jest, Vitest, or Mocha test runners.
metadata:
  short-description: Set up Husky git hooks for test coverage enforcement
---
# Husky Test Coverage

To set up or verify Husky git hooks that run tests and enforce coverage thresholds on every commit.

## When to Use

Use when setting up test coverage enforcement, verifying existing Husky/test setup, or configuring coverage thresholds for Jest, Vitest, or Mocha.

## Workflow

1. Discover project context: check package.json for test runner (Jest/Vitest/Mocha), existing Husky setup, and coverage configuration.
2. Detect test runner and coverage tool from dependencies and config files.
3. Install or verify Husky, initialize hooks, add prepare script if needed.
4. Configure coverage thresholds (default 80%) in runner-specific config files.
5. Create pre-commit hook that runs tests with coverage and enforces thresholds.
6. Verify setup by reviewing configuration and testing with a commit.

## Quick Start

```bash
# Basic setup (80% threshold, blocks commits below)
python3 ~/.codex/skills/husky-test-coverage/scripts/setup-husky-coverage.py --root /path/to/project

# Custom threshold
python3 ~/.codex/skills/husky-test-coverage/scripts/setup-husky-coverage.py --root /path/to/project --threshold 85

# Warn only (don't block)
python3 ~/.codex/skills/husky-test-coverage/scripts/setup-husky-coverage.py --root /path/to/project --no-fail-on-below
```

## Tech Stack Detection

Auto-detects test runner from package.json dependencies:

- **Jest**: Uses `jest --coverage --watchAll=false` in hook
- **Vitest**: Uses `vitest --coverage --run` in hook
- **Mocha**: Uses `nyc` or `c8` with mocha test command

Detects package manager (npm/yarn/pnpm/bun) and uses appropriate commands.

## Configuration

**Command line:**

- `--root <path>`: Project root (required)
- `--threshold <number>`: Coverage percentage (default: 80)
- `--no-fail-on-below`: Warn only, don't block commits
- `--skip-if-no-tests`: Skip hook if no test files found
- `--dry-run`: Preview changes

**Config file (`.husky-test-coverage.json`):**

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

**Package.json:**

```json
{
  "huskyTestCoverage": { "threshold": 80, "failOnBelow": true }
}
```

## Test Runner Configuration

**Jest:** Creates/updates `jest.config.json` with `coverageThreshold`.

**Vitest:** Creates/updates `vitest.config.ts/js` with `coverage.thresholds`.

**Mocha + nyc:** Creates/updates `.nycrc.json` with coverage settings.

Default thresholds: 80% lines, 75% branches, 80% functions, 80% statements.

## What Gets Created

- Husky installation (if missing) and initialization
- `.husky/pre-commit` hook running tests with coverage
- Coverage configuration file for detected test runner
- `prepare` script in package.json (if missing)

## Integration

Works alongside `linter-formatter-init` (both configure Husky but focus on different concerns). Complements `testing-expert` skill for coverage targets. Safely adds to existing Husky setups without breaking existing hooks.

## Troubleshooting

**Hook not running:** Run `npx husky install && chmod +x .husky/pre-commit`

**Coverage not checked:** Verify test command includes coverage flag, check config file exists.

**Hook fails when tests pass:** Check coverage thresholds are achievable, review coverage report.