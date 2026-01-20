# Product Requirements Document

## Overview

[1-2 paragraph product description. What problem does this solve? Who is it for?]

---

## Core Entities

| Entity | Description | Key Fields |
|--------|-------------|------------|
| [Entity1] | [What it represents] | id, name, userId, createdAt |
| [Entity2] | [What it represents] | id, [field], [field], userId |

---

## Features

### MVP Features (Must Have)

- [ ] **[Feature 1]**: [Description of what this feature does]
- [ ] **[Feature 2]**: [Description of what this feature does]
- [ ] **[Feature 3]**: [Description of what this feature does]

### Nice to Have (Post-MVP)

- [ ] [Feature 4]: [Description]
- [ ] [Feature 5]: [Description]

---

## User Flows

### Primary Flow: [Main User Journey]

1. User [action]
2. System [response]
3. User [action]
4. System [response]

### Secondary Flow: [Another Journey]

1. [Step 1]
2. [Step 2]

---

## Routes / Pages

### Frontend Routes

| Route | Description | Auth Required |
|-------|-------------|---------------|
| `/` | Home / Dashboard | Yes |
| `/[entity]` | List view | Yes |
| `/[entity]/[id]` | Detail view | Yes |
| `/sign-in` | Sign in | No |
| `/sign-up` | Sign up | No |

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/[entities]` | List all |
| POST | `/api/[entities]` | Create new |
| GET | `/api/[entities]/:id` | Get by ID |
| PATCH | `/api/[entities]/:id` | Update |
| DELETE | `/api/[entities]/:id` | Delete |

---

## Technical Requirements

### Authentication

- [ ] Clerk authentication
- [ ] Protected routes
- [ ] User context in API

### Database

- [ ] MongoDB with Mongoose
- [ ] User-scoped queries (multi-tenancy)
- [ ] Soft deletes (if applicable)

### Quality

- [ ] 80% test coverage
- [ ] Biome linting
- [ ] TypeScript strict mode

---

## Success Criteria

1. [ ] User can [primary action]
2. [ ] User can [secondary action]
3. [ ] All tests pass with 80%+ coverage
4. [ ] `bun dev` starts successfully

---

## Out of Scope (for MVP)

- [Feature X] - Will be added in v2
- [Feature Y] - Depends on [external factor]

---

## Open Questions

1. [Question about requirement]?
2. [Question about design decision]?
