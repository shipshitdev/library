---
name: mongodb-atlas-checker
description: Expert in verifying MongoDB Atlas setup and configuration for backend applications. Checks connection strings, environment variables, database configuration, connection pooling, and ensures proper setup for Next.js and NestJS applications. This skill activates when users need to verify their MongoDB Atlas backend setup is correct.
---

# MongoDB Atlas Checker

You are an expert in verifying MongoDB Atlas setup and configuration for backend applications. This skill helps identify configuration issues, missing environment variables, incorrect connection strings, and ensures proper database setup for Next.js and NestJS applications.

## When to Use This Skill

This skill activates automatically when you're:

- Verifying MongoDB Atlas backend setup
- Checking if connection strings are correctly configured
- Validating environment variable setup
- Ensuring database connection is properly established
- Reviewing MongoDB Atlas configuration
- Troubleshooting database connection issues
- Auditing database setup before deployment

## Project Context Discovery

**Before checking MongoDB Atlas setup, discover the project's context:**

1. **Scan Project Documentation:**
   - Check `.agent/SYSTEM/ARCHITECTURE.md` for database architecture
   - Review existing database patterns
   - Look for environment variable usage
   - Check for existing MongoDB integration

2. **Identify Framework:**
   - Determine if using Next.js (App Router or Pages Router)
   - Check if using NestJS backend
   - Review existing database connection patterns
   - Check for ORM/ODM usage (Mongoose, TypeORM, Prisma)

3. **Use Project-Specific Skills:**
   - Check for `[project]-mongodb-atlas-checker` skill
   - Review project-specific database patterns
   - Follow project's configuration standards

## Checklist: MongoDB Atlas Setup Verification

### 1. Environment Variables

**Check for required environment variables:**

```bash
# Required for MongoDB Atlas
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/database?retryWrites=true&w=majority
# OR
DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/database?retryWrites=true&w=majority
```

**Verification Steps:**

- [ ] Environment variable exists (check `.env.local`, `.env`, or deployment config)
- [ ] Variable name is consistent across codebase
- [ ] Connection string uses `mongodb+srv://` protocol (required for Atlas)
- [ ] Connection string includes authentication credentials
- [ ] Connection string includes database name
- [ ] Connection string includes query parameters (`retryWrites=true&w=majority`)
- [ ] No hardcoded connection strings in source code
- [ ] `.env.example` or `.env.template` has placeholder (not real credentials)

**Common Issues:**

```typescript
// ❌ BAD: Hardcoded connection string
const mongoUri = 'mongodb+srv://user:pass@cluster.mongodb.net/db';

// ❌ BAD: Wrong protocol (not supported by Atlas)
const mongoUri = 'mongodb://user:pass@cluster.mongodb.net/db';

// ❌ BAD: Missing database name
const mongoUri = 'mongodb+srv://user:pass@cluster.mongodb.net';

// ✅ GOOD: Environment variable
const mongoUri = process.env.MONGODB_URI;
```

### 2. Connection String Format

**MongoDB Atlas connection strings must:**

- Use `mongodb+srv://` protocol (not `mongodb://`)
- Include username and password
- Include cluster hostname (e.g., `cluster0.xxxxx.mongodb.net`)
- Include database name
- Include query parameters for production readiness

**Valid Format:**

```
mongodb+srv://<username>:<password>@<cluster-host>/<database>?retryWrites=true&w=majority
```

**Check for:**

- [ ] Protocol is `mongodb+srv://`
- [ ] Username and password are URL-encoded if they contain special characters
- [ ] Cluster hostname is correct (from Atlas dashboard)
- [ ] Database name is specified
- [ ] Query parameters include `retryWrites=true&w=majority`
- [ ] Optional: `appName` parameter for monitoring
- [ ] Optional: `maxPoolSize` for connection pooling

**Example with all parameters:**

```
mongodb+srv://user:pass@cluster0.xxxxx.mongodb.net/mydb?retryWrites=true&w=majority&appName=MyApp&maxPoolSize=10
```

### 3. Database Driver Installation

**Check if MongoDB driver is installed:**

**For Mongoose (ODM):**

```bash
# Check package.json
npm list mongoose
# or
pnpm list mongoose
```

**For Native MongoDB Driver:**

```bash
npm list mongodb
```

**Verification:**

- [ ] `mongoose` or `mongodb` package is installed
- [ ] Version is compatible with MongoDB Atlas
- [ ] Package is listed in `package.json` dependencies (not devDependencies for production)

### 4. Connection Setup

**Next.js (App Router or Pages Router):**

**Check for proper connection pattern:**

```typescript
// ✅ GOOD: Singleton pattern for Next.js
// lib/mongodb.ts or utils/mongodb.ts
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

**Verification:**

- [ ] Connection uses singleton pattern (prevents multiple connections in Next.js)
- [ ] Connection is cached globally (for Next.js serverless functions)
- [ ] Error handling is implemented
- [ ] Connection options are configured (bufferCommands: false recommended)
- [ ] Connection is called before database operations

**NestJS:**

**Check for MongooseModule configuration:**

```typescript
// ✅ GOOD: NestJS MongooseModule
// app.module.ts
import { Module } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose';

@Module({
  imports: [
    MongooseModule.forRoot(process.env.MONGODB_URI, {
      retryWrites: true,
      w: 'majority',
    }),
  ],
})
export class AppModule {}
```

**Or with connection options:**

```typescript
MongooseModule.forRoot(process.env.MONGODB_URI, {
  retryWrites: true,
  w: 'majority',
  maxPoolSize: 10,
  serverSelectionTimeoutMS: 5000,
  socketTimeoutMS: 45000,
})
```

**Verification:**

- [ ] `@nestjs/mongoose` package is installed
- [ ] `MongooseModule.forRoot()` is configured in root module
- [ ] Connection string comes from environment variable
- [ ] Connection options are set appropriately
- [ ] Error handling is in place

### 5. Connection Options

**Recommended connection options for MongoDB Atlas:**

```typescript
{
  retryWrites: true,
  w: 'majority',
  maxPoolSize: 10,              // Connection pool size
  serverSelectionTimeoutMS: 5000, // Timeout for server selection
  socketTimeoutMS: 45000,        // Socket timeout
  connectTimeoutMS: 10000,       // Connection timeout
  bufferCommands: false,          // Disable mongoose buffering
  bufferMaxEntries: 0,           // Disable mongoose buffering
}
```

**Verification:**

- [ ] `retryWrites: true` is set (required for Atlas)
- [ ] `w: 'majority'` is set (write concern)
- [ ] Connection pool size is appropriate for your use case
- [ ] Timeouts are configured appropriately
- [ ] Buffer commands is disabled for serverless (Next.js)

### 6. Error Handling

**Check for proper error handling:**

```typescript
// ✅ GOOD: Error handling
try {
  await connectDB();
  // Database operations
} catch (error) {
  console.error('MongoDB connection error:', error);
  // Handle error appropriately
  throw error;
}
```

**Verification:**

- [ ] Connection errors are caught and handled
- [ ] Error messages are logged appropriately
- [ ] Application doesn't crash on connection failure
- [ ] Retry logic is implemented if needed
- [ ] Error handling is consistent across the codebase

### 7. Database Name Configuration

**Check if database name is correctly specified:**

- [ ] Database name is in connection string
- [ ] Database name matches your application's needs
- [ ] Database name doesn't contain special characters
- [ ] Database name is consistent across environments (dev/staging/prod)

### 8. SSL/TLS Configuration

**MongoDB Atlas requires SSL/TLS by default:**

- [ ] Connection string doesn't explicitly disable SSL (Atlas requires it)
- [ ] No `ssl=false` in connection string
- [ ] TLS/SSL is enabled by default with `mongodb+srv://`

### 9. Network Access

**Check Atlas Network Access settings:**

- [ ] IP whitelist includes your deployment IPs
- [ ] For development: `0.0.0.0/0` allows all IPs (not recommended for production)
- [ ] For production: Specific IPs or VPC peering configured
- [ ] Network access rules are documented

### 10. Database User Configuration

**Check Atlas Database User settings:**

- [ ] Database user exists in Atlas
- [ ] User has appropriate permissions (read/write for application database)
- [ ] Password is strong and secure
- [ ] User credentials match connection string
- [ ] User is not using admin credentials for application

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

**Create a test script to verify connection:**

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
# Load environment variables and run
node -r dotenv/config scripts/test-mongodb-connection.ts
# or
ts-node scripts/test-mongodb-connection.ts
```

## Summary Checklist

Before considering MongoDB Atlas setup complete, verify:

- [ ] `MONGODB_URI` environment variable exists and is correct
- [ ] Connection string uses `mongodb+srv://` protocol
- [ ] Connection string includes database name
- [ ] MongoDB driver (mongoose or mongodb) is installed
- [ ] Connection setup follows framework best practices
- [ ] Connection options are configured appropriately
- [ ] Error handling is implemented
- [ ] Network access is configured in Atlas
- [ ] Database user has appropriate permissions
- [ ] No hardcoded credentials in source code
- [ ] Connection test script passes

## Next Steps

After verifying setup:

1. Test connection with verification script
2. Create initial database schema/models
3. Set up database indexes
4. Configure connection pooling for production
5. Set up monitoring and alerts in Atlas dashboard
6. Document connection setup in project documentation
