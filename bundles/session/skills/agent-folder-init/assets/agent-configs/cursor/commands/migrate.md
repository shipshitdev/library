# Migrate - Database Migration Command

**Purpose:** Manage MongoDB (and other database) migrations safely with version control and rollback capabilities.

## When to Use

- Creating new database migrations
- Running pending migrations
- Rolling back migrations
- Managing schema changes
- Data transformations

## Project Context Discovery

**Before creating migrations, discover the project's setup:**

1. **Identify Database Type:**
   - Check for MongoDB connection strings
   - Look for Mongoose schemas
   - Check for Prisma schema (if using Prisma)
   - Review database configuration files

2. **Discover Migration Tool:**
   - Check for `migrate-mongo` (MongoDB)
   - Check for `prisma migrate` (Prisma)
   - Check for custom migration scripts
   - Review `package.json` for migration scripts

3. **Identify Migration Location:**
   - Check for `migrations/` directory
   - Look for `db/migrations/` or `database/migrations/`
   - Review project structure for migration patterns

4. **Check Migration State:**
   - Review existing migrations
   - Check migration changelog
   - Identify current schema version

## Migration Workflow

### Phase 1: Create Migration

**1.1 Analyze Schema Changes**

```bash
/migrate create add-user-indexes
```

**Process:**

1. Identify what changed:
   - New collections/tables
   - Modified schemas
   - New indexes
   - Data transformations needed

2. **For MongoDB:**

   ```javascript
   // migrations/[timestamp]-add-user-indexes.js
   module.exports = {
     async up(db) {
       await db.collection('users').createIndex({ email: 1 }, { unique: true });
       await db.collection('users').createIndex({ organization: 1, createdAt: -1 });
     },
     
     async down(db) {
       await db.collection('users').dropIndex('email_1');
       await db.collection('users').dropIndex('organization_1_createdAt_-1');
     }
   };
   ```

3. **For Mongoose Schema Changes:**
   - Create migration to update existing documents
   - Handle data transformation
   - Add indexes

**1.2 Migration Template**

```javascript
// Template for MongoDB migrations
module.exports = {
  async up(db, client) {
    // Migration logic here
    // Use db.collection() for MongoDB operations
    // Use client for transactions if needed
  },
  
  async down(db, client) {
    // Rollback logic here
    // Should reverse the 'up' operation
  }
};
```

### Phase 2: Test Migration

**2.1 Test Locally**

```bash
# Run migration on local database
npm run migrate:up

# Or with migrate-mongo
npx migrate-mongo up
```

**2.2 Verify Changes**

```bash
# Check migration status
npm run migrate:status

# Verify schema changes
# Check indexes created
# Verify data transformations
```

**2.3 Test Rollback**

```bash
# Test rollback works
npm run migrate:down

# Verify rollback successful
# Re-run migration
npm run migrate:up
```

### Phase 3: Apply Migration

**3.1 Pre-Migration Checklist**

- [ ] Migration tested locally
- [ ] Rollback tested
- [ ] Backup created (for production)
- [ ] Migration reviewed
- [ ] Team notified (for production)

**3.2 Run Migration**

```bash
# Staging
npm run migrate:up --env=staging

# Production (with confirmation)
⚠️  WARNING: Running migration on PRODUCTION database

Migration: [migration-name]
Changes: [description]
Estimated time: [duration]

Continue? (y/n)
```

**3.3 Monitor Migration**

- Watch migration progress
- Check for errors
- Monitor database performance
- Verify data integrity

## MongoDB-Specific Patterns

### Schema Changes

**Adding Fields:**

```javascript
async up(db) {
  await db.collection('users').updateMany(
    {},
    { $set: { newField: null } }
  );
}
```

**Removing Fields:**

```javascript
async up(db) {
  await db.collection('users').updateMany(
    {},
    { $unset: { deprecatedField: "" } }
  );
}
```

**Changing Field Types:**

```javascript
async up(db) {
  const users = await db.collection('users').find({}).toArray();
  
  for (const user of users) {
    await db.collection('users').updateOne(
      { _id: user._id },
      { $set: { field: convertType(user.field) } }
    );
  }
}
```

### Index Management

**Create Indexes:**

```javascript
async up(db) {
  // Single field index
  await db.collection('users').createIndex({ email: 1 });
  
  // Compound index
  await db.collection('posts').createIndex(
    { organization: 1, createdAt: -1 },
    { name: 'org_created_idx' }
  );
  
  // Text index
  await db.collection('content').createIndex({ title: 'text', body: 'text' });
}
```

**Drop Indexes:**

```javascript
async down(db) {
  await db.collection('users').dropIndex('email_1');
  await db.collection('posts').dropIndex('org_created_idx');
}
```

### Data Migrations

**Transform Data:**

```javascript
async up(db) {
  const cursor = db.collection('users').find({});
  
  while (await cursor.hasNext()) {
    const user = await cursor.next();
    
    // Transform data
    const transformed = {
      ...user,
      fullName: `${user.firstName} ${user.lastName}`,
      updatedAt: new Date()
    };
    
    await db.collection('users').replaceOne(
      { _id: user._id },
      transformed
    );
  }
}
```

**Bulk Operations:**

```javascript
async up(db) {
  const bulkOps = [];
  
  const users = await db.collection('users').find({}).toArray();
  
  for (const user of users) {
    bulkOps.push({
      updateOne: {
        filter: { _id: user._id },
        update: { $set: { migrated: true } }
      }
    });
  }
  
  if (bulkOps.length > 0) {
    await db.collection('users').bulkWrite(bulkOps);
  }
}
```

## Migration Best Practices

### 1. Idempotency

**Migrations should be safe to run multiple times:**

```javascript
async up(db) {
  // Check if index exists before creating
  const indexes = await db.collection('users').indexes();
  const hasIndex = indexes.some(idx => idx.name === 'email_1');
  
  if (!hasIndex) {
    await db.collection('users').createIndex({ email: 1 });
  }
}
```

### 2. Backward Compatibility

**Maintain compatibility during migration:**

```javascript
async up(db) {
  // Add new field, keep old field temporarily
  await db.collection('users').updateMany(
    {},
    { 
      $set: { 
        newField: null,
        // Keep old field for compatibility
        oldField: { $ifNull: ['$oldField', null] }
      } 
    }
  );
}
```

### 3. Large Data Migrations

**For large collections, use batches:**

```javascript
async up(db) {
  const BATCH_SIZE = 1000;
  let skip = 0;
  let hasMore = true;
  
  while (hasMore) {
    const users = await db.collection('users')
      .find({})
      .skip(skip)
      .limit(BATCH_SIZE)
      .toArray();
    
    if (users.length === 0) {
      hasMore = false;
      break;
    }
    
    // Process batch
    const bulkOps = users.map(user => ({
      updateOne: {
        filter: { _id: user._id },
        update: { $set: { migrated: true } }
      }
    }));
    
    await db.collection('users').bulkWrite(bulkOps);
    skip += BATCH_SIZE;
  }
}
```

### 4. Transaction Safety

**Use transactions for critical operations:**

```javascript
async up(db, client) {
  const session = client.startSession();
  
  try {
    await session.withTransaction(async () => {
      // Migration operations
      await db.collection('users').updateMany(
        {},
        { $set: { field: 'value' } },
        { session }
      );
    });
  } finally {
    await session.endSession();
  }
}
```

## Rollback Procedures

**Always implement rollback:**

```javascript
async down(db) {
  // Reverse the 'up' operation
  await db.collection('users').updateMany(
    { newField: { $exists: true } },
    { $unset: { newField: "" } }
  );
  
  await db.collection('users').dropIndex('email_1');
}
```

**Test rollback:**

```bash
# Run migration
npm run migrate:up

# Test rollback
npm run migrate:down

# Verify rollback successful
# Re-run migration
npm run migrate:up
```

## Migration Status

**Check migration status:**

```bash
# List pending migrations
npm run migrate:status

# Output:
# ✅ 20250101000000-add-user-indexes (applied)
# ⏳ 20250102000000-add-posts-collection (pending)
# ⏳ 20250103000000-update-schema (pending)
```

## Common Migration Patterns

### 1. Add Collection

```javascript
async up(db) {
  // Collection created automatically on first insert
  await db.collection('posts').insertOne({
    _id: new ObjectId(),
    createdAt: new Date(),
    // Initial document structure
  });
  
  // Create indexes
  await db.collection('posts').createIndex({ organization: 1 });
}

async down(db) {
  await db.collection('posts').drop();
}
```

### 2. Rename Collection

```javascript
async up(db) {
  await db.collection('oldName').rename('newName');
}

async down(db) {
  await db.collection('newName').rename('oldName');
}
```

### 3. Add Required Field

```javascript
async up(db) {
  // Add field with default value
  await db.collection('users').updateMany(
    { newField: { $exists: false } },
    { $set: { newField: 'default-value' } }
  );
  
  // Then make required in application code
}

async down(db) {
  await db.collection('users').updateMany(
    {},
    { $unset: { newField: "" } }
  );
}
```

## Safety Features

**Always include:**

1. **Backup Before Production:**

   ```bash
   # Create backup
   mongodump --uri="[connection-string]" --out=backup-[date]
   ```

2. **Dry Run Mode:**

   ```bash
   # Test migration without applying
   npm run migrate:up --dry-run
   ```

3. **Confirmation for Production:**

   ```
   ⚠️  WARNING: Running migration on PRODUCTION database
   
   Migration: [name]
   Changes: [description]
   Estimated time: [duration]
   Backup created: backup-[date]
   
   Continue? (y/n)
   ```

## Error Handling

**Common Issues:**

1. **Migration Fails Mid-Execution:**
   - Check error logs
   - Verify partial changes
   - Rollback if needed
   - Fix migration script
   - Re-run migration

2. **Index Creation Fails:**
   - Check for duplicate keys
   - Verify index doesn't already exist
   - Check index size limits
   - Review index definition

3. **Data Transformation Errors:**
   - Check data types
   - Verify field existence
   - Handle null/undefined values
   - Test with sample data first

## Integration with NestJS

**If using NestJS with Mongoose:**

```typescript
// migrations/[timestamp]-migration.ts
import { Connection } from 'mongoose';

export async function up(connection: Connection) {
  await connection.collection('users').createIndex({ email: 1 });
}

export async function down(connection: Connection) {
  await connection.collection('users').dropIndex('email_1');
}
```

## Output Format

When running migrations:

```
🔄 MIGRATION STATUS

Pending migrations: 2
Applied migrations: 15

📋 PENDING MIGRATIONS
1. 20250101000000-add-user-indexes
   - Creates email index
   - Creates compound index
   
2. 20250102000000-update-schema
   - Adds newField to users
   - Transforms existing data

🚀 RUNNING MIGRATION: add-user-indexes

✅ Creating email index...
✅ Creating compound index...
✅ Migration complete

📊 RESULTS
- Indexes created: 2
- Documents affected: 0
- Duration: 1.2s

✅ MIGRATION COMPLETE
```

---

**Created:** 2025-12-24
**Purpose:** Manage database migrations safely with version control
**Databases:** MongoDB (primary), adaptable to other databases
