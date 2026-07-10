# Bun Validator — Full Examples

## Workspace Structure Example (GOOD)

```
my-monorepo/
├── package.json          # Root with workspaces, private: true
├── bun.lockb             # Single lockfile at root
├── apps/
│   ├── web/
│   │   └── package.json  # Own dependencies
│   └── api/
│       └── package.json  # Own dependencies
└── packages/
    ├── ui/
    │   └── package.json  # Shared package
    └── config/
        └── package.json  # Shared config
```

## Validation Output Example

```
=== Bun Workspace Validation Report ===

Bun Version: 1.3.2 ✓

Root package.json:
  ✓ private: true
  ✓ workspaces defined
  ✗ Found dependencies in root (should be empty)

Workspace Structure:
  ✓ apps/web - valid workspace
  ✓ apps/api - valid workspace
  ✓ packages/ui - valid workspace
  ✗ apps/web/bun.lockb - lockfile should only be at root

Dependencies:
  ✓ Using workspace:* protocol
  ✗ @myorg/ui uses hardcoded version "1.0.0"

Catalogs:
  ✗ No dependency catalog found (recommended for Bun 1.3+)

Summary: 3 issues found
```
