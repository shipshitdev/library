# Project Map - {{PROJECT_NAME}}

**Purpose:** Quick reference for project structure and responsibilities.
**Last Updated:** {{DATE}}

---

## Directory Overview

```
{{PROJECT_NAME}}/
├── .agents/              # AI documentation (you are here)
├── src/                 # Source code
│   ├── components/      # UI components
│   ├── services/        # Business logic
│   ├── utils/           # Utilities
│   └── types/           # Type definitions
├── tests/               # Test files
├── docs/                # Documentation
└── config/              # Configuration files
```

---

## Key Directories

### `/src/components/`

**Purpose:** UI components
**Patterns:** React components, Tailwind styling

### `/src/services/`

**Purpose:** Business logic and API calls
**Patterns:** Service classes, async operations

### `/src/utils/`

**Purpose:** Utility functions
**Patterns:** Pure functions, helpers

### `/src/types/`

**Purpose:** TypeScript type definitions
**Patterns:** Interfaces, type aliases

---

## File Naming

| Type | Pattern | Example |
|------|---------|---------|
| Component | PascalCase | `UserProfile.tsx` |
| Service | kebab-case | `user-service.ts` |
| Utility | kebab-case | `string-helpers.ts` |
| Type | kebab-case | `user-types.ts` |
| Test | `.test.ts` suffix | `user-service.test.ts` |

---

## Entry Points

| File | Purpose |
|------|---------|
| `src/index.ts` | Main entry point |
| `src/app.ts` | Application setup |

---

## Configuration Files

| File | Purpose |
|------|---------|
| `package.json` | Dependencies and scripts |
| `tsconfig.json` | TypeScript configuration |
| `.env` | Environment variables |

---

## Related Documentation

- `../ARCHITECTURE.md` - System architecture
- `../RULES.md` - Coding standards
- `DECISIONS.md` - Architectural decisions
