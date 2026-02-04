# De-Slop: Clean AI Artifacts

**Purpose:** Remove AI-generated artifacts and code sloppiness while maintaining monorepo structure

## Usage

```bash
/de-slop              # Clean all AI artifacts in current package/project
/de-slop --all        # Clean across entire monorepo
/de-slop --check      # Show what would be cleaned (dry run)
```

## What This Command Does

Removes common AI-generated code artifacts:

1. **Console statements** → Replace with logger service
2. **`any` types** → Replace with proper types/interfaces
3. **Unused imports** → Remove completely
4. **Commented-out code** → Remove dead code blocks
5. **Temporary/debug code** → Remove TODO/FIXME debug statements
6. **Obvious AI comments** → Remove redundant comments
7. **Unused variables** → Remove if truly unused

## Monorepo Awareness

- ✅ Works per-package or monorepo-wide
- ✅ Respects package boundaries
- ✅ Handles shared dependencies correctly
- ✅ Updates imports across packages if needed

---

## When to Use

Use this command:

- After AI-assisted coding sessions
- Before committing code
- When codebase feels "slobby" with AI artifacts
- During code review preparation
- As part of pre-commit cleanup

---

## Workflow

### Step 1: Check CRITICAL Rules

**MANDATORY:** Before making any changes, check critical rules:

```bash
# Check for critical rules that might affect cleanup
cat .agents/SYSTEM/critical/CRITICAL-NEVER-DO.md 2>/dev/null || true
cat .agents/SYSTEM/critical/CROSS-PROJECT-RULES.md 2>/dev/null || true
```

**Critical constraints:**

- Never delete critical files (README.md, configs, entry points)
- Never work outside workspace
- Respect logger service patterns (no console.log)
- Type safety requirements (no `any` types)

### Step 2: Detect Monorepo Structure

Determine if this is a monorepo:

```bash
# Check for common monorepo indicators
ls -la packages/ 2>/dev/null || ls -la packages/*/package.json 2>/dev/null || true
ls -la pnpm-workspace.yaml 2>/dev/null || ls -la lerna.json 2>/dev/null || true
```

**If monorepo detected:**

- Process each package separately
- Respect package boundaries
- Check shared dependencies

**If single project:**

- Process entire project at once

### Step 3: Identify Artifacts to Clean

#### 3.1 Console Statements

**Find console.log/warn/error/debug:**

```bash
# Search for console statements
grep -r "console\." --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" .
```

**For each found:**

```typescript
// BEFORE (AI artifact)
console.log("User logged in:", user);
console.error("Failed to fetch:", error);

// AFTER (proper logger)
this.logger.info("User logged in", { userId: user.id });
this.logger.error("Failed to fetch", { error: error.message });
```

**Action:**

- Replace with logger service (check for LoggerService pattern)
- If no logger exists, create minimal logger or use appropriate service
- Remove console statements

#### 3.2 Any Types

**Find `any` types:**

```bash
# Search for any types
grep -r ": any" --include="*.ts" --include="*.tsx" .
grep -r "<any>" --include="*.ts" --include="*.tsx" .
```

**For each found:**

```typescript
// BEFORE (AI artifact)
function processData(data: any) {
  return data.value;
}

// AFTER (proper type)
interface DataInput {
  value: string;
}

function processData(data: DataInput): string {
  return data.value;
}
```

**Action:**

- Define proper interfaces/types
- Place interfaces in `packages/*/interfaces/` or `packages/*/props/` (monorepo)
- Replace `any` with specific types

#### 3.3 Unused Imports

**Find unused imports:**

```bash
# Use TypeScript compiler or ESLint to find unused imports
# Check each file for imports that aren't used
```

**Action:**

- Remove unused imports completely
- Be careful with side-effect imports (CSS, polyfills)

#### 3.4 Commented-Out Code

**Find commented code blocks:**

```bash
# Search for large commented blocks
grep -r "^[[:space:]]*//[[:space:]]*[A-Z]" --include="*.ts" --include="*.tsx" .
```

**Action:**

- Remove commented-out code blocks (> 3 lines)
- Keep single-line explanatory comments if helpful
- Remove debug comments (TODO/FIXME for debugging)

#### 3.5 Temporary/Debug Code

**Find temporary code:**

```bash
# Search for debug markers
grep -r "// DEBUG\|// TEMP\|// HACK\|// FIXME: debug" --include="*.ts" --include="*.tsx" -i .
```

**Action:**

- Remove debug-only code blocks
- Remove temporary workarounds that should be fixed properly

#### 3.6 Obvious AI Comments

**Find redundant comments:**

```typescript
// BEFORE (obvious AI comment)
// This function calculates the sum
function sum(a: number, b: number) {
  return a + b;
}

// AFTER (clean code)
function sum(a: number, b: number): number {
  return a + b;
}
```

**Action:**

- Remove comments that just restate the code
- Keep comments that explain "why", not "what"

#### 3.7 Unused Variables

**Find unused variables:**

```bash
# TypeScript compiler will catch these, or use ESLint
```

**Action:**

- Remove truly unused variables
- Check if variable is used in ways that might not be detected (template strings, etc.)

### Step 4: Execute Cleanup (Per Package in Monorepo)

**For each package/project:**

1. **Console statements** → Replace with logger
2. **Any types** → Create interfaces, replace types
3. **Unused imports** → Remove
4. **Commented code** → Remove blocks
5. **Debug code** → Remove temporary code
6. **Obvious comments** → Remove redundant comments
7. **Unused variables** → Remove

### Step 5: Verify Changes

**After cleanup, verify:**

```bash
# TypeScript should still compile
npm run build
# or
npm run type-check

# Tests should still pass (push to GitHub Actions)
# Never run tests locally - push instead
git push origin HEAD
# Check GitHub Actions for test results
```

### Step 6: Update Documentation

**Log cleanup in session file:**

```markdown
## De-Slop Cleanup - [Date]

**Packages cleaned:**

- packages/api/
- packages/frontend/

**Artifacts removed:**

- 23 console.log statements → Replaced with logger
- 8 `any` types → Replaced with proper interfaces
- 15 unused imports removed
- 5 commented code blocks removed
- 3 debug code blocks removed
```

---

## Manual Checklist for AI Agent

When user runs `/de-slop`:

### Pre-Cleanup

- [ ] Check `.agents/SYSTEM/critical/` rules
- [ ] Detect monorepo structure
- [ ] Identify target packages/projects

### Detection Phase

- [ ] Find all console.\* statements
- [ ] Find all `any` types
- [ ] Find unused imports
- [ ] Find commented code blocks
- [ ] Find temporary/debug code
- [ ] Find obvious AI comments
- [ ] Find unused variables

### Cleanup Phase (Per Package)

- [ ] Replace console statements with logger service
- [ ] Create interfaces for `any` types (in correct package location)
- [ ] Remove unused imports
- [ ] Remove commented code blocks
- [ ] Remove debug/temporary code
- [ ] Remove redundant comments
- [ ] Remove unused variables

### Verification

- [ ] TypeScript compiles (or push to CI)
- [ ] No breaking changes introduced
- [ ] Logger service pattern followed
- [ ] Type safety maintained

### Documentation

- [ ] Log cleanup in `.agents/SESSIONS/[today].md`
- [ ] List files modified
- [ ] Note any interfaces created
- [ ] Summary of artifacts removed

---

## Examples

### Example 1: Single Package Cleanup

**User:** `/de-slop`

**AI Actions:**

1. Check critical rules
2. Detect it's a single project (no monorepo)
3. Find artifacts:
   - 5 console.log statements
   - 2 `any` types
   - 3 unused imports
4. Clean artifacts:
   - Replace console.log with logger
   - Create interfaces, replace `any`
   - Remove unused imports
5. Verify TypeScript compiles
6. Document cleanup

### Example 2: Monorepo Cleanup

**User:** `/de-slop --all`

**AI Actions:**

1. Check critical rules
2. Detect monorepo structure
3. Process each package:
   - `packages/api/` - Clean artifacts
   - `packages/frontend/` - Clean artifacts
   - `packages/common/` - Clean artifacts
4. Verify all packages compile
5. Document cleanup per package

### Example 3: Dry Run

**User:** `/de-slop --check`

**AI Actions:**

1. Detect structure
2. Find all artifacts
3. List what would be cleaned:

   ```
   Found artifacts:
   - 12 console.log statements
   - 5 `any` types
   - 8 unused imports
   - 3 commented code blocks

   Would clean: [list of files]
   ```

4. User can review before cleanup

---

## Safety Checks

**Before cleanup:**

- ✅ Verify critical rules don't prevent cleanup
- ✅ Check if logger service exists (for console replacement)
- ✅ Ensure interfaces directory exists (for type definitions)
- ✅ Create backup if major refactoring needed

**After cleanup:**

- ✅ TypeScript compiles successfully
- ✅ No runtime errors introduced
- ✅ Logger service used correctly
- ✅ All types properly defined
- ✅ No unused imports remain

---

## Error Handling

**If logger service not found:**

- Check for logger pattern in codebase
- Create minimal logger or use existing service
- Document logger requirement

**If interfaces directory missing:**

- Create `packages/*/interfaces/` (monorepo)
- Or create `interfaces/` (single project)
- Follow existing project structure

**If TypeScript errors after cleanup:**

- Revert problematic changes
- Fix type errors properly
- Re-run cleanup for remaining artifacts

**If tests fail:**

- Review changes made
- Fix any breaking changes
- Verify tests pass in CI

---

## Monorepo-Specific Considerations

### Package Boundaries

- ✅ Don't modify shared packages without need
- ✅ Keep interfaces in correct package locations
- ✅ Update imports if interfaces moved

### Shared Dependencies

- ✅ Check if logger is in shared package
- ✅ Verify interface locations match project structure
- ✅ Update cross-package imports if needed

### Build Order

- ✅ Clean packages in dependency order
- ✅ Shared packages first, then dependents

---

## Philosophy

**De-sloping means:**

- ✅ Removing AI artifacts that humans wouldn't write
- ✅ Maintaining code quality standards
- ✅ Keeping codebase professional and clean
- ✅ Following project patterns (logger, types, etc.)

**Not de-sloping:**

- ❌ Removing all comments (keep helpful ones)
- ❌ Changing working code unnecessarily
- ❌ Removing code that's actually needed
- ❌ Breaking functionality for "cleanliness"

---

**Created:** 2025-01-27
**Purpose:** Remove AI-generated code artifacts while maintaining monorepo structure and code quality
