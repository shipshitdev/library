# Env Setup - Environment Variable Management

**Purpose:** Manage environment variables across services, scaffold .env files, validate required variables, and set up secrets

## Usage

```bash
/env-setup              # Interactive environment setup
/env-setup --validate   # Validate existing .env files
/env-setup --scaffold   # Generate .env template files
```

## When to Use

Use this command when:

- Starting a new project
- Setting up a new environment (development, staging, production)
- Need to validate environment configuration
- Want to document required environment variables
- Setting up secrets management

## What This Command Does

Helps manage environment variables:

1. **Scaffold .env Files** - Generate .env templates from codebase analysis
2. **Validate Configuration** - Check that required variables are set
3. **Document Variables** - Create .env.example files
4. **Secrets Management** - Guide for secure secret handling

---

## Workflow

### Phase 1: Discover Required Variables

**1.1 Scan Codebase for Environment Variables**

```bash
# Find environment variable usage
grep -r "process.env\." --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" . | grep -v node_modules | sort -u

# Find NEXT_PUBLIC_ variables (Next.js public env vars)
grep -r "NEXT_PUBLIC_" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" . | grep -v node_modules | sort -u

# Check for common patterns
grep -r "DATABASE_URL\|MONGODB_URI\|REDIS_URL\|API_KEY\|SECRET" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" . | grep -v node_modules
```

**1.2 Check Configuration Files**

```bash
# Check for existing .env files
ls -la .env* 2>/dev/null || true

# Check for .env.example
cat .env.example 2>/dev/null || true

# Check config files that might reference env vars
cat next.config.js 2>/dev/null || true
cat nest-cli.json 2>/dev/null || true
```

**1.3 Identify Service-Specific Variables**

**Backend (NestJS):**
- Database connection strings
- API keys and secrets
- Authentication keys
- External service credentials

**Frontend (Next.js):**
- API URLs
- Public keys (NEXT_PUBLIC_*)
- Analytics IDs
- Feature flags

**Infrastructure:**
- AWS credentials
- Deployment configuration
- Monitoring credentials

### Phase 2: Generate .env Templates

**2.1 Create .env.example**

Based on discovered variables, create comprehensive template:

```env
# Application
NODE_ENV=development
PORT=3001

# Database (MongoDB on EC2)
MONGODB_URI=mongodb://user:password@localhost:27017/database?authSource=admin

# Redis
REDIS_URL=redis://:password@localhost:6379

# Authentication (Clerk)
CLERK_SECRET_KEY=sk_test_...
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...

# Sentry
SENTRY_DSN=https://...
NEXT_PUBLIC_SENTRY_DSN=https://...
SENTRY_ORG=your-org
SENTRY_PROJECT=your-project

# Google Analytics
NEXT_PUBLIC_GA_MEASUREMENT_ID=G-XXXXXXXXXX

# API Configuration
API_URL=http://localhost:3001
NEXT_PUBLIC_API_URL=http://localhost:3001

# Stripe (if using)
STRIPE_SECRET_KEY=sk_test_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# AWS (if using)
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1

# Other Services
# Add other service credentials here
```

**2.2 Create Service-Specific Templates**

**Backend (.env.example in api/):**

```env
# Backend Environment Variables

NODE_ENV=development
PORT=3001

# Database
MONGODB_URI=mongodb://user:password@localhost:27017/database?authSource=admin

# Redis
REDIS_URL=redis://:password@localhost:6379

# Authentication
CLERK_SECRET_KEY=sk_test_...

# Sentry
SENTRY_DSN=https://...

# AWS
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
```

**Frontend (.env.local.example in frontend/):**

```env
# Frontend Environment Variables

# API
NEXT_PUBLIC_API_URL=http://localhost:3001

# Authentication
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...

# Monitoring
NEXT_PUBLIC_SENTRY_DSN=https://...
NEXT_PUBLIC_GA_MEASUREMENT_ID=G-XXXXXXXXXX

# Payments
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

### Phase 3: Validate Environment Variables

**3.1 Check Required Variables**

```bash
# Check if .env file exists
if [ ! -f .env ]; then
  echo "❌ .env file not found"
  exit 1
fi

# Source .env file
set -a
source .env
set +a

# Check required variables
REQUIRED_VARS=(
  "NODE_ENV"
  "MONGODB_URI"
  "CLERK_SECRET_KEY"
)

MISSING_VARS=()

for var in "${REQUIRED_VARS[@]}"; do
  if [ -z "${!var}" ]; then
    MISSING_VARS+=("$var")
  fi
done

if [ ${#MISSING_VARS[@]} -ne 0 ]; then
  echo "❌ Missing required variables:"
  printf '%s\n' "${MISSING_VARS[@]}"
  exit 1
fi

echo "✅ All required variables are set"
```

**3.2 Validate Variable Formats**

```bash
# Validate MongoDB URI format
if [[ ! "$MONGODB_URI" =~ ^mongodb:// ]]; then
  echo "❌ MONGODB_URI must start with mongodb://"
  exit 1
fi

# Validate GA Measurement ID format
if [[ ! "$NEXT_PUBLIC_GA_MEASUREMENT_ID" =~ ^G-[A-Z0-9]+$ ]]; then
  echo "❌ NEXT_PUBLIC_GA_MEASUREMENT_ID must be in format G-XXXXXXXXXX"
  exit 1
fi

# Validate Sentry DSN format
if [[ ! "$SENTRY_DSN" =~ ^https://.*@.*\.ingest\.sentry\.io/.*$ ]]; then
  echo "❌ SENTRY_DSN format is invalid"
  exit 1
fi
```

**3.3 Create Validation Script**

```typescript
// scripts/validate-env.ts
import * as fs from 'fs';
import * as path from 'path';

const requiredVars = {
  // Backend
  MONGODB_URI: /^mongodb:\/\//,
  CLERK_SECRET_KEY: /^sk_(test|live)_/,
  
  // Frontend
  NEXT_PUBLIC_API_URL: /^https?:\/\//,
  NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: /^pk_(test|live)_/,
  
  // Optional but validated if present
  SENTRY_DSN: /^https:\/\/.*@.*\.ingest\.sentry\.io\/.*$/,
  NEXT_PUBLIC_GA_MEASUREMENT_ID: /^G-[A-Z0-9]+$/,
};

function validateEnv() {
  const envFile = path.join(process.cwd(), '.env');
  
  if (!fs.existsSync(envFile)) {
    console.error('❌ .env file not found');
    process.exit(1);
  }

  const envContent = fs.readFileSync(envFile, 'utf-8');
  const envVars: Record<string, string> = {};
  
  envContent.split('\n').forEach(line => {
    const match = line.match(/^([^=]+)=(.*)$/);
    if (match) {
      envVars[match[1].trim()] = match[2].trim();
    }
  });

  const missing: string[] = [];
  const invalid: string[] = [];

  Object.entries(requiredVars).forEach(([varName, pattern]) => {
    const value = envVars[varName];
    
    if (!value) {
      missing.push(varName);
    } else if (!pattern.test(value)) {
      invalid.push(`${varName} (format: ${pattern})`);
    }
  });

  if (missing.length > 0) {
    console.error('❌ Missing required variables:');
    missing.forEach(v => console.error(`  - ${v}`));
    process.exit(1);
  }

  if (invalid.length > 0) {
    console.error('❌ Invalid variable formats:');
    invalid.forEach(v => console.error(`  - ${v}`));
    process.exit(1);
  }

  console.log('✅ All environment variables are valid');
}

validateEnv();
```

### Phase 4: Secrets Management

**4.1 Environment-Specific Secrets**

**Development (.env.local):**
- Use test/development keys
- Can commit to git (but use .gitignore)
- Use local database connections

**Staging (.env.staging):**
- Use staging/test keys
- Never commit to git
- Use staging database
- Set up via deployment platform

**Production (.env.production):**
- Use production/live keys
- Never commit to git
- Store in secure secret management
- Set up via deployment platform (AWS Secrets Manager, Vercel env vars, etc.)

**4.2 Secret Storage Best Practices**

**Never commit:**
- `.env` (actual secrets)
- `.env.local`
- `.env.production`
- `.env.staging`

**Always commit:**
- `.env.example` (template, no secrets)

**.gitignore:**
```gitignore
# Environment variables
.env
.env.local
.env*.local
.env.production
.env.staging
.env.development

# But keep examples
!.env.example
```

**4.3 AWS Secrets Manager (Production)**

For production, use AWS Secrets Manager:

```typescript
// scripts/load-secrets.ts
import { SecretsManagerClient, GetSecretValueCommand } from '@aws-sdk/client-secrets-manager';
import * as fs from 'fs';

async function loadSecrets() {
  const client = new SecretsManagerClient({ region: process.env.AWS_REGION });
  const command = new GetSecretValueCommand({
    SecretId: process.env.SECRET_NAME,
  });

  const response = await client.send(command);
  const secrets = JSON.parse(response.SecretString || '{}');

  // Write to .env file
  const envContent = Object.entries(secrets)
    .map(([key, value]) => `${key}=${value}`)
    .join('\n');
  
  fs.writeFileSync('.env', envContent);
}

loadSecrets();
```

### Phase 5: Documentation

**5.1 Create Environment Documentation**

```markdown
# Environment Variables

## Required Variables

### Backend
- `MONGODB_URI` - MongoDB connection string
- `CLERK_SECRET_KEY` - Clerk authentication secret key

### Frontend
- `NEXT_PUBLIC_API_URL` - Backend API URL
- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` - Clerk publishable key

## Optional Variables

### Monitoring
- `SENTRY_DSN` - Sentry error tracking DSN
- `NEXT_PUBLIC_GA_MEASUREMENT_ID` - Google Analytics ID

## Setup Instructions

1. Copy `.env.example` to `.env`
2. Fill in all required variables
3. Run `npm run validate-env` to validate
```

**5.2 Update README**

Add environment setup section to README.md:

```markdown
## Environment Setup

1. Copy `.env.example` to `.env`
2. Fill in required variables
3. See [Environment Variables](./docs/ENV.md) for details
```

---

## Manual Checklist for AI Agent

When user runs `/env-setup`:

### Discovery Phase

- [ ] Scan codebase for `process.env.*` usage
- [ ] Identify all environment variables
- [ ] Check for existing .env files
- [ ] Document service-specific variables

### Template Generation

- [ ] Create .env.example template
- [ ] Create service-specific templates (backend, frontend)
- [ ] Document each variable
- [ ] Include format examples

### Validation

- [ ] Create validation script
- [ ] Define required variables
- [ ] Define format validations
- [ ] Test validation script

### Secrets Management

- [ ] Update .gitignore (exclude .env files)
- [ ] Ensure .env.example is committed
- [ ] Document secret storage practices
- [ ] Provide AWS Secrets Manager guidance (if applicable)

### Documentation

- [ ] Create environment variable documentation
- [ ] Update README with setup instructions
- [ ] Document environment-specific configurations
- [ ] Save setup in session file

---

## Examples

### Example 1: Scaffold Environment Files

**User:** `/env-setup --scaffold`

**AI Actions:**
1. Scan codebase for environment variables
2. Generate .env.example files
3. Create service-specific templates
4. Document all variables
5. Update .gitignore

### Example 2: Validate Environment

**User:** `/env-setup --validate`

**AI Actions:**
1. Check if .env files exist
2. Validate required variables are set
3. Validate variable formats
4. Report missing/invalid variables
5. Provide remediation steps

### Example 3: Full Setup

**User:** `/env-setup`

**AI Actions:**
1. Discover all environment variables
2. Generate templates
3. Create validation scripts
4. Set up secrets management
5. Document everything

---

## Common Environment Variables

**Standard Variables:**
- `NODE_ENV` - Environment (development, staging, production)
- `PORT` - Server port

**Database:**
- `MONGODB_URI` - MongoDB connection string
- `REDIS_URL` - Redis connection URL

**Authentication:**
- `CLERK_SECRET_KEY` - Clerk secret key
- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` - Clerk publishable key

**Monitoring:**
- `SENTRY_DSN` - Sentry DSN
- `NEXT_PUBLIC_GA_MEASUREMENT_ID` - Google Analytics ID

**API:**
- `API_URL` - Backend API URL
- `NEXT_PUBLIC_API_URL` - Public API URL

**Payments:**
- `STRIPE_SECRET_KEY` - Stripe secret key
- `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` - Stripe publishable key
- `STRIPE_WEBHOOK_SECRET` - Stripe webhook secret

---

## Best Practices

**Security:**
- Never commit .env files
- Use strong, unique secrets
- Rotate secrets regularly
- Use secret management services for production

**Organization:**
- Group related variables
- Use clear naming conventions
- Document purpose of each variable
- Keep .env.example up to date

**Validation:**
- Validate on application startup
- Use type-safe env loading (e.g., zod)
- Fail fast if required vars missing
- Provide clear error messages

---

**Created:** 2025-01-27
**Purpose:** Manage environment variables across services with validation and documentation

