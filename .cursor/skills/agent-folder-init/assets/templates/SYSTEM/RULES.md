# Coding Rules - {{PROJECT_NAME}}

**Purpose:** Coding standards and patterns for this project.
**Last Updated:** {{DATE}}

---

## General Principles

1. **Follow existing patterns** - Search for 3+ similar implementations before writing new code
2. **Quality over speed** - Think through implementations before coding
3. **No inline types** - Define interfaces/types in dedicated files
4. **No `any` types** - Use proper TypeScript types
5. **No `console.log`** - Use a logging service

---

## File Organization

### Naming Conventions

- **Directories:** lowercase with hyphens (`user-settings/`)
- **Files:** kebab-case (`user-service.ts`)
- **Components:** PascalCase (`UserProfile.tsx`)
- **Interfaces:** PascalCase with `I` prefix (`IUserProfile`)

### Import Order

1. External packages
2. Internal packages/aliases
3. Relative imports
4. Types/interfaces

```typescript
// External
import { useState } from 'react';

// Internal aliases
import { Button } from '@components/ui';
import { UserService } from '@services/user';

// Relative
import { helpers } from './utils';

// Types
import type { IUser } from '@interfaces/user';
```

---

## TypeScript

### Do

- Use strict mode
- Define return types for functions
- Use path aliases (`@components/`, `@services/`)
- Export types from dedicated files

### Don't

- Use `any` type
- Use inline interface definitions
- Use relative imports for shared code
- Ignore TypeScript errors

---

## Error Handling

```typescript
try {
  const result = await operation();
  return result;
} catch (error) {
  logger.error('Operation failed', { error, context });
  throw new AppError('User-friendly message', error);
}
```

---

## Testing

- Write tests for business logic
- Use descriptive test names
- Mock external dependencies
- Test edge cases

---

## Git

### Commit Messages

```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Branch Naming

- `feature/description`
- `fix/description`
- `chore/description`

---

## Documentation

- Document public APIs
- Add JSDoc for complex functions
- Keep README up to date
- Document architectural decisions in `SYSTEM/architecture/DECISIONS.md`

---

## Project-Specific Rules

<!-- Add your project-specific rules below -->

---

**Remember:** When in doubt, check existing code for patterns.
