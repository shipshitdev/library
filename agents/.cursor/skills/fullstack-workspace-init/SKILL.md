---
name: fullstack-workspace-init
description: Scaffold a full-stack monorepo workspace with NextJS frontend, NestJS backend, React Native mobile, and shared packages. Use this skill when starting a new product that needs a complete tech stack with best practices baked in.
---

# Full Stack Workspace Init

Create a production-ready monorepo with:

- **Frontend:** NextJS + React + TypeScript + Tailwind + @agenticindiedev/ui
- **Backend:** NestJS + MongoDB + Redis + BullMQ
- **Mobile:** React Native + Expo
- **Shared:** Packages for types, serializers, enums, helpers
- **Package Manager:** bun

## Usage

```bash
# Show help
python3 ~/.cursor/skills/fullstack-workspace-init/scripts/init-workspace.py --help

# Create full workspace
python3 ~/.cursor/skills/fullstack-workspace-init/scripts/init-workspace.py \
  --root ~/www/myproject \
  --name "My Project"

# Create with custom org name (for packages)
python3 ~/.cursor/skills/fullstack-workspace-init/scripts/init-workspace.py \
  --root ~/www/myproject \
  --name "My Project" \
  --org "myorg"
```

## Generated Structure

```
myproject/
├── .agent/                  # AI documentation
├── .gitignore
├── .npmrc                   # Forces bun
├── package.json             # Workspace root
├── AGENTS.md
├── CLAUDE.md
├── CODEX.md
├── README.md
│
├── api/                     # NestJS backend
│   ├── .agent/
│   ├── apps/
│   │   └── api/
│   │       └── src/
│   │           ├── main.ts
│   │           ├── app.module.ts
│   │           ├── auth/
│   │           ├── config/
│   │           └── collections/
│   ├── package.json
│   ├── nest-cli.json
│   ├── Dockerfile
│   └── AGENTS.md, CLAUDE.md, CODEX.md
│
├── frontend/                # NextJS apps
│   ├── .agent/
│   ├── apps/
│   │   └── dashboard/
│   │       └── app/
│   ├── packages/
│   │   ├── components/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── interfaces/
│   ├── package.json
│   ├── next.config.ts
│   ├── tailwind.config.ts
│   └── AGENTS.md, CLAUDE.md, CODEX.md
│
├── mobile/                  # React Native + Expo
│   ├── .agent/
│   ├── app/
│   │   └── _layout.tsx
│   ├── package.json
│   ├── app.json
│   └── AGENTS.md, CLAUDE.md, CODEX.md
│
└── packages/                # Shared packages
    ├── .agent/
    ├── packages/
    │   ├── common/
    │   │   ├── serializers/
    │   │   ├── interfaces/
    │   │   └── enums/
    │   ├── helpers/
    │   └── constants/
    ├── package.json
    └── AGENTS.md, CLAUDE.md, CODEX.md
```

## Key Patterns Included

### Backend

- Soft deletes: `isDeleted: boolean` (not `deletedAt`)
- Multi-tenancy: Always filter by `organization`
- Collection pattern: controllers → services → schemas
- Simple indexes in schema, compound in module

### Frontend

- Path aliases: `@components/`, `@services/`, `@hooks/`
- AbortController in useEffect
- No inline interfaces
- LoggerService instead of console.log

### Shared

- Serializers in `packages/common/serializers/`
- Interfaces in `packages/common/interfaces/`
- Enums in `packages/common/enums/`

## Additional Scripts

```bash
# Add a new frontend app
python3 ~/.cursor/skills/fullstack-workspace-init/scripts/add-frontend-app.py \
  --root ~/www/myproject/frontend \
  --name admin

# Add a new API collection
python3 ~/.cursor/skills/fullstack-workspace-init/scripts/add-api-collection.py \
  --root ~/www/myproject/api \
  --name users
```

## Development Commands

After scaffolding:

```bash
cd myproject

# Install all dependencies
bun install

# Start backend
cd api && bun run start:dev

# Start frontend
cd frontend && bun run dev

# Start mobile
cd mobile && bun run start
```

## References

- `references/architecture-guide.md` - Architectural decisions
- `references/coding-standards.md` - Coding rules
- `references/deployment-guide.md` - Deployment patterns
