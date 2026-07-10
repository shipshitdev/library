# TypeScript Expert — Full Guide

Extended examples and command sequences for the typescript-expert skill. See `SKILL.md` for workflow steps, decision tables, short inline patterns, and pointers to the other reference files in this skill.

## Migration Playbook

Incremental JavaScript → TypeScript migration:

```bash
# 1. Enable allowJs and checkJs (merge into existing tsconfig.json):
# Add to existing tsconfig.json:
# {
#   "compilerOptions": {
#     "allowJs": true,
#     "checkJs": true
#   }
# }

# 2. Rename files gradually (.js → .ts)
# 3. Add types file by file
# 4. Enable strict mode features one by one

# Automated helpers (if installed/needed)
command -v ts-migrate >/dev/null 2>&1 && bunx ts-migrate migrate . --sources 'src/**/*.js'
command -v typesync >/dev/null 2>&1 && bunx typesync  # Install missing @types packages
```

## Monorepo TypeScript Configuration

```json
// Root tsconfig.json
{
  "references": [
    { "path": "./packages/core" },
    { "path": "./packages/ui" },
    { "path": "./apps/web" }
  ],
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "declarationMap": true
  }
}
```

## Vitest Type Testing

```typescript
// in avatar.test-d.ts
import { expectTypeOf } from 'vitest'
import type { Avatar } from './avatar'

test('Avatar props are correctly typed', () => {
  expectTypeOf<Avatar>().toHaveProperty('size')
  expectTypeOf<Avatar['size']>().toEqualTypeOf<'sm' | 'md' | 'lg'>()
})
```

## CLI Debugging Tools

```bash
# Debug TypeScript files directly (if tools installed)
command -v tsx >/dev/null 2>&1 && bunx tsx --inspect src/file.ts
command -v ts-node >/dev/null 2>&1 && bunx ts-node --inspect-brk src/file.ts

# Trace module resolution issues
bunx tsc --traceResolution > resolution.log 2>&1
grep "Module resolution" resolution.log

# Debug type checking performance (use --incremental false for clean trace)
bunx tsc --generateTrace trace --incremental false
# Analyze trace (if installed)
command -v @typescript/analyze-trace >/dev/null 2>&1 && bunx @typescript/analyze-trace trace

# Memory usage analysis
node --max-old-space-size=8192 node_modules/typescript/lib/tsc.js
```

## Custom Error Classes

```typescript
// Proper error class with stack preservation
class DomainError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number
  ) {
    super(message);
    this.name = 'DomainError';
    Error.captureStackTrace(this, this.constructor);
  }
}
```
