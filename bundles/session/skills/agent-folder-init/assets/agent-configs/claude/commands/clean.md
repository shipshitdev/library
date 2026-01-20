# Clean - Cleanup Operations

Perform various cleanup operations on the codebase.

## Usage

/clean [type]

Types:

- imports: Remove unused imports
- types: Fix any types
- console: Remove console.log statements
- dead: Remove dead code
- all: Run all cleanups

## Cleanup Operations

### Clean Imports

Find and remove unused imports:

- Search for import statements
- Check if imported items are used
- Remove unused ones

### Clean Types

Fix TypeScript any types:

- Find any type usages
- Replace with proper types
- Add interfaces where needed

### Clean Console

Remove console.log statements:

- Find console.log/warn/error
- Replace with proper logger
- Or remove if not needed

### Clean Dead Code

Find potentially dead code:

- Unused functions
- Unused variables
- Commented code blocks

## Workflow

### Step 1: Identify Target

What type of cleanup?

- Specific type (imports, types, etc.)
- All cleanups

### Step 2: Scan Codebase

Search for items to clean:

- Use grep/glob to find instances
- List all occurrences

### Step 3: Review

Show what will be changed:

- File paths
- Line numbers
- Current vs proposed

### Step 4: Execute

Make the changes:

- One file at a time
- Verify after each change

### Step 5: Verify

Run checks:

- TypeScript compiles
- Tests pass
- No runtime errors

## Safety

Before cleaning:

- Commit current changes
- Have tests passing
- Understand what youre removing

After cleaning:

- Run full test suite
- Verify build works
- Review git diff
