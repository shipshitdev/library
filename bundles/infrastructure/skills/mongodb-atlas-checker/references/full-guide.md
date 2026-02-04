# MongoDB Atlas Checker - Full Guide

Complete guide to verifying MongoDB Atlas setup for Next.js and NestJS applications.

## Project Context Discovery

Before checking MongoDB Atlas setup:

1. **Scan Project Documentation:**
   - Check `.agents/SYSTEM/ARCHITECTURE.md` for database architecture
   - Review existing database patterns
   - Check for existing MongoDB integration

2. **Identify Framework:**
   - Determine if using Next.js (App Router or Pages Router)
   - Check if using NestJS backend
   - Check for ORM/ODM usage (Mongoose, TypeORM, Prisma)

## Connection Setup Patterns

### Next.js Singleton Pattern

```typescript
// lib/mongodb.ts
import mongoose from 'mongoose';

const MONGODB_URI = process.env.MONGODB_URI!;

if (!MONGODB_URI) {
  throw new Error('Please define MONGODB_URI environment variable');
}

interface MongooseCache {
  conn: typeof mongoose | null;
  promise: Promise<typeof mongoose> | null;
}

declare global {
  var mongoose: MongooseCache | undefined;
}

let cached: MongooseCache = global.mongoose || { conn: null, promise: null };

if (!global.mongoose) {
  global.mongoose = cached;
}

async function connectDB() {
  if (cached.conn) {
    return cached.conn;
  }

  if (!cached.promise) {
    const opts = {
      bufferCommands: false,
    };

    cached.promise = mongoose.connect(MONGODB_URI, opts).then((mongoose) => {
      return mongoose;
    });
  }

  try {
    cached.conn = await cached.promise;
  } catch (e) {
    cached.promise = null;
    throw e;
  }

  return cached.conn;
}

export default connectDB;
```

### NestJS MongooseModule

```typescript
// app.module.ts
import { Module } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose';

@Module({
  imports: [
    MongooseModule.forRoot(process.env.MONGODB_URI, {
      retryWrites: true,
      w: 'majority',
      maxPoolSize: 10,
      serverSelectionTimeoutMS: 5000,
      socketTimeoutMS: 45000,
    }),
  ],
})
export class AppModule {}
```

## Recommended Connection Options

```typescript
{
  retryWrites: true,           // Required for Atlas
  w: 'majority',               // Write concern
  maxPoolSize: 10,             // Connection pool size
  serverSelectionTimeoutMS: 5000,
  socketTimeoutMS: 45000,
  connectTimeoutMS: 10000,
  bufferCommands: false,       // Disable for serverless (Next.js)
  bufferMaxEntries: 0,
}
```

## Common Issues and Solutions

### Issue 1: Connection String Not Found

**Problem:** `MONGODB_URI` environment variable is missing

**Solution:**

```bash
# Add to .env.local (Next.js) or .env (NestJS)
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/database?retryWrites=true&w=majority
```

### Issue 2: Wrong Protocol

**Problem:** Using `mongodb://` instead of `mongodb+srv://`

**Solution:** Change to `mongodb+srv://` (required for Atlas)

### Issue 3: Multiple Connections in Next.js

**Problem:** Creating new connection on each API call

**Solution:** Use singleton pattern to cache connection (see Connection Setup section)

### Issue 4: Connection Timeout

**Problem:** Connection times out

**Solution:**

- Check network access in Atlas dashboard
- Verify IP whitelist
- Increase `connectTimeoutMS` and `serverSelectionTimeoutMS`
- Check firewall settings

### Issue 5: Authentication Failed

**Problem:** Username/password incorrect

**Solution:**

- Verify credentials in Atlas dashboard
- Check if password contains special characters (needs URL encoding)
- Verify database user exists and has permissions

## Verification Script

```typescript
// scripts/test-mongodb-connection.ts
import mongoose from 'mongoose';

const MONGODB_URI = process.env.MONGODB_URI;

if (!MONGODB_URI) {
  console.error('❌ MONGODB_URI environment variable is missing');
  process.exit(1);
}

async function testConnection() {
  try {
    await mongoose.connect(MONGODB_URI, {
      retryWrites: true,
      w: 'majority',
    });

    console.log('✅ Successfully connected to MongoDB Atlas');

    // Test a simple operation
    const collections = await mongoose.connection.db.listCollections().toArray();
    console.log(`✅ Found ${collections.length} collections`);

    await mongoose.disconnect();
    console.log('✅ Connection closed');
    process.exit(0);
  } catch (error) {
    console.error('❌ MongoDB connection error:', error);
    process.exit(1);
  }
}

testConnection();
```

**Run the test:**

```bash
node -r dotenv/config scripts/test-mongodb-connection.ts
# or
ts-node scripts/test-mongodb-connection.ts
```

## Detailed Checklist

### Environment Variables

- [ ] Environment variable exists (check `.env.local`, `.env`, or deployment config)
- [ ] Variable name is consistent across codebase
- [ ] Connection string uses `mongodb+srv://` protocol
- [ ] Connection string includes authentication credentials
- [ ] Connection string includes database name
- [ ] Connection string includes query parameters
- [ ] No hardcoded connection strings in source code
- [ ] `.env.example` has placeholder (not real credentials)

### Connection String Format

- [ ] Protocol is `mongodb+srv://`
- [ ] Username and password are URL-encoded if special characters
- [ ] Cluster hostname is correct
- [ ] Database name is specified
- [ ] Query parameters include `retryWrites=true&w=majority`

### Connection Setup

- [ ] Connection uses singleton pattern (Next.js)
- [ ] Connection is cached globally
- [ ] Error handling is implemented
- [ ] Connection options are configured
- [ ] Connection is called before database operations

### Network Access

- [ ] IP whitelist includes deployment IPs
- [ ] For development: `0.0.0.0/0` allows all (not for production)
- [ ] For production: Specific IPs or VPC peering

### Database User

- [ ] Database user exists in Atlas
- [ ] User has appropriate permissions
- [ ] Password is strong and secure
- [ ] User credentials match connection string
- [ ] Not using admin credentials for application

## Next Steps

After verifying setup:

1. Test connection with verification script
2. Create initial database schema/models
3. Set up database indexes
4. Configure connection pooling for production
5. Set up monitoring and alerts in Atlas dashboard
