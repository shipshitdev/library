# Entity Documentation

## Overview

This document describes all data entities in the system, their relationships, and implementation details.

---

## Entity: [EntityName]

### Description

[What this entity represents and its purpose in the system]

### Schema

```typescript
interface [Entity] {
  _id: string;           // MongoDB ObjectId

  // Core fields
  [field]: string;       // [Description]
  [field]: number;       // [Description]
  [field]?: Date;        // [Optional] [Description]

  // Relations
  [relatedId]?: string;  // Reference to [RelatedEntity]

  // System fields (auto-generated)
  userId: string;        // Owner (Clerk user ID)
  createdAt: Date;       // Auto-generated
  updatedAt: Date;       // Auto-generated
}
```

### Validation Rules

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| [field] | string | Yes | Min 1, Max 255 |
| [field] | enum | No | One of: 'low', 'medium', 'high' |
| [field] | Date | No | Must be future date |

### Indexes

```typescript
// Primary indexes
{ userId: 1 }                    // All queries filter by user
{ userId: 1, createdAt: -1 }     // List queries with sorting

// Compound indexes for specific queries
{ userId: 1, [field]: 1 }        // [Description of query this optimizes]
```

### API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | /api/[entities] | List all for user | Required |
| POST | /api/[entities] | Create new | Required |
| GET | /api/[entities]/:id | Get by ID | Required |
| PATCH | /api/[entities]/:id | Update | Required |
| DELETE | /api/[entities]/:id | Delete | Required |

### Business Rules

1. **Ownership**: All [entities] belong to a user (userId)
2. **Deletion**: [Soft delete / Hard delete] behavior
3. **Ordering**: Default sort by [field] [ASC/DESC]

---

## Entity: [AnotherEntity]

[Repeat the pattern above for each entity]

---

## Entity Relationships

```
[Entity1] ──┬── 1:N ──→ [Entity2]
            │
            └── 1:1 ──→ [Entity3]

[Entity2] ──── N:M ──→ [Entity4]
```

### Relationship Details

| From | To | Type | Description |
|------|-----|------|-------------|
| User | [Entity1] | 1:N | A user has many [entities] |
| [Entity1] | [Entity2] | 1:N | A [entity1] has many [entity2s] |
| [Entity2] | [Entity3] | N:1 | Many [entity2s] belong to one [entity3] |

---

## Migration Notes

### Version 1.0 → 1.1

- Added `[field]` to [Entity] (optional, default: null)
- Renamed `[oldField]` to `[newField]`

### Data Migrations

```javascript
// Example migration script
db.[entities].updateMany(
  { [oldField]: { $exists: true } },
  { $rename: { [oldField]: "[newField]" } }
);
```

---

## Query Patterns

### Common Queries

```typescript
// Get all entities for user
const entities = await Model.find({ userId }).sort({ createdAt: -1 });

// Get with filters
const entities = await Model.find({
  userId,
  [field]: { $in: values },
  createdAt: { $gte: startDate }
});

// Aggregate stats
const stats = await Model.aggregate([
  { $match: { userId } },
  { $group: { _id: "$[field]", count: { $sum: 1 } } }
]);
```

---

## Testing Considerations

### Test Data Factories

```typescript
const create[Entity] = (overrides = {}) => ({
  [field]: "Test Value",
  userId: "test-user-id",
  ...overrides,
});
```

### Edge Cases to Test

- Empty [field] handling
- Maximum length [field]
- Invalid [relatedId] reference
- Unauthorized access (wrong userId)
- Concurrent updates
