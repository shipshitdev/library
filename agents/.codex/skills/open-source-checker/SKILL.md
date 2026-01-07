---
name: open-source-checker
description: Expert in detecting private information, secrets, API keys, credentials, and sensitive data in codebases before open sourcing. Scans for hardcoded secrets, API keys, passwords, private keys, personal information, database credentials, and other sensitive data that should not be exposed in public repositories. Can also set up git hooks and pre-commit hooks to prevent committing secrets.
metadata:
  short-description: Check for private info before open sourcing
---

# Open Source Checker

Expert in detecting private information, secrets, and sensitive data in codebases. Use when preparing to open source a repository or auditing for exposed secrets. Can set up automated checks via git hooks to prevent future issues.

## When to Use

- Preparing to open source a repository
- Reviewing code for exposed secrets
- Auditing codebase for sensitive data
- Checking for hardcoded credentials
- Validating that no private information is committed
- Reviewing pull requests for secrets
- Performing security audits before public release

## What to Check For

### 1. API Keys and Tokens

**Common patterns:**
- API keys (OpenAI, Stripe, AWS, Google, etc.)
- Authentication tokens
- OAuth tokens
- JWT secrets
- Session keys
- Webhook secrets

**Patterns to detect:**
```typescript
// ❌ BAD: Hardcoded API keys
const apiKey = 'sk-1234567890abcdef';
const stripeKey = 'sk_live_...';
const awsKey = 'AKIAIOSFODNN7EXAMPLE';

// ✅ GOOD: Environment variables
const apiKey = process.env.API_KEY;
const stripeKey = process.env.STRIPE_SECRET_KEY;
```

**Common locations:**
- Configuration files
- Source code files
- Environment files (`.env` files that might be committed)
- Test files
- Documentation files
- Example files

### 2. Database Credentials

**Check for:**
- Database connection strings
- Usernames and passwords
- MongoDB URIs
- PostgreSQL connection strings
- Redis credentials
- Database host addresses

**Patterns:**
```typescript
// ❌ BAD: Hardcoded credentials
const mongoUri = 'mongodb://user:password@host:27017/db';
const dbPassword = 'mySecretPassword123';

// ✅ GOOD: Environment variables
const mongoUri = process.env.MONGODB_URI;
```

### 3. Private Keys and Certificates

**Check for:**
- SSH private keys
- SSL/TLS certificates
- Private key files (`.pem`, `.key`, `.p12`)
- Certificate files
- Signing keys

**Files to check:**
- `*.pem`, `*.key`, `*.p12`, `*.pfx`
- `id_rsa`, `id_dsa`, `id_ecdsa`
- `*.crt`, `*.cer`, `*.cert`

### 4. Personal Information

**Check for:**
- Email addresses
- Phone numbers
- Physical addresses
- Personal names
- Social security numbers
- Credit card numbers
- Bank account numbers

**Patterns:**
```typescript
// ❌ BAD: Personal information
const adminEmail = 'john.doe@example.com';
const phone = '+1-555-123-4567';

// ✅ GOOD: Placeholder or environment variable
const adminEmail = process.env.ADMIN_EMAIL;
```

### 5. Environment Files

**Check for:**
- `.env` files (should be in `.gitignore`)
- `.env.local`, `.env.production`
- Files containing actual secrets (not `.env.example`)

**Verify:**
- `.env` is in `.gitignore`
- Only `.env.example` is committed (with placeholder values)
- No actual secrets in any committed `.env` files

## Scanning Workflow

### Phase 1: File System Scan

**1.1 Check for Common Secret Files**

```bash
# Find potential secret files
find . -name "*.env" -o -name "*.key" -o -name "*.pem" -o -name "id_rsa*"
find . -name "secrets.*" -o -name "*secret*"
find . -name ".env*" ! -name ".env.example"
```

**1.2 Check .gitignore**

```bash
# Verify .env is ignored
cat .gitignore | grep -E "\.env|secrets|\.key|\.pem"
```

**1.3 Scan for Common Patterns**

```bash
# Search for API key patterns
grep -r "sk-[a-zA-Z0-9]" --include="*.ts" --include="*.js" --include="*.json"
grep -r "AKIA[0-9A-Z]" --include="*.ts" --include="*.js"
grep -r "sk_live_" --include="*.ts" --include="*.js"
```

### Phase 2: Code Pattern Analysis

**2.1 Search for Hardcoded Secrets**

Look for:
- String literals that look like API keys
- Hardcoded passwords
- Connection strings with credentials
- Token values in code

**2.2 Check Configuration Files**

Review:
- All config files for hardcoded values
- Environment variable usage (should use `process.env`)
- Default values that might be secrets

**2.3 Review Test Files**

Check:
- Test credentials (should be mocks, not real)
- Test API keys (should be fake/test keys)
- Test database connections

### Phase 3: Content Analysis

**3.1 Check Documentation**

- README files
- Documentation files
- Comments in code
- Example code snippets

**3.2 Check Example Files**

- `.env.example` should have placeholders
- Example configs should not have real values
- Sample code should not include real keys

### Phase 4: Git History Check

**⚠️ CRITICAL: Secrets remain in git history even if removed from current files.**

**4.1 Comprehensive Git History Scan**

```bash
# Search entire history for API keys
git log --all --full-history -p -S "sk-" | grep -B 5 -A 5 "sk-"
git log --all --full-history -p -S "AKIA" | grep -B 5 -A 5 "AKIA"
git log --all --full-history -p -S "sk_live_" | grep -B 5 -A 5 "sk_live_"

# Search all branches and tags
git log --all --branches --tags --full-history -p -S "sk-" | grep -B 5 -A 5 "sk-"

# Search deleted files
git log --all --full-history --diff-filter=D --summary | grep -E "\.env|secrets"

# Search specific file types
git log --all --full-history -p -- "*.env" | grep -E "(sk-|password|AKIA)"
```

**4.2 Using Tools for Git History**

**gitleaks (Recommended):**

```bash
# Scan entire git history
gitleaks detect --source . --verbose --log-opts="--all"

# Scan specific branch
gitleaks detect --source . --verbose --log-opts="--all --branches=main"
```

**truffleHog:**

```bash
# Scan entire git history
trufflehog --regex --entropy=False git file://.
```

**git-secrets:**

```bash
# Scan entire history
git secrets --scan-history
```

**4.3 Cleaning Git History (If Secrets Found)**

**⚠️ WARNING: Rewrites history. Coordinate with team first.**

**Using git-filter-repo:**

```bash
pip install git-filter-repo
git filter-repo --invert-paths --path-glob "*.env"
git filter-repo --replace-text <(echo "sk-OLD-KEY==>sk-REMOVED")
```

**Using BFG Repo-Cleaner:**

```bash
brew install bfg
bfg --delete-files secrets.json
echo "sk-OLD-KEY==>sk-REMOVED" > replacements.txt
bfg --replace-text replacements.txt
```

**Fresh Repository (if history too contaminated):**

```bash
git checkout --orphan fresh-start
git add .
git commit -m "Initial commit (cleaned history)"
git branch -D main
git branch -m main
git push -f origin main  # Coordinate with team!
```

**4.4 Verify History is Clean**

```bash
# Re-scan after cleaning
gitleaks detect --source . --verbose --log-opts="--all"
git log --all --full-history -p -S "sk-" | grep "sk-"
```

## Common Patterns to Detect

### API Key Patterns

```typescript
// OpenAI
sk-[a-zA-Z0-9]{32,}

// AWS
AKIA[0-9A-Z]{16}

// Stripe
sk_live_[a-zA-Z0-9]{24,}
sk_test_[a-zA-Z0-9]{24,}

// GitHub
ghp_[a-zA-Z0-9]{36}

// Generic
[a-zA-Z0-9_-]{20,}  // Long alphanumeric strings
```

### Password Patterns

```typescript
// Common patterns
password\s*[:=]\s*['"][^'"]+['"]
pwd\s*[:=]\s*['"][^'"]+['"]
pass\s*[:=]\s*['"][^'"]+['"]
```

### Connection String Patterns

```typescript
// MongoDB
mongodb://[^:]+:[^@]+@
mongodb\+srv://[^:]+:[^@]+@

// PostgreSQL
postgres://[^:]+:[^@]+@
postgresql://[^:]+:[^@]+@

// MySQL
mysql://[^:]+:[^@]+@

// Redis
redis://[^:]+:[^@]+@
```

### Email Patterns

```typescript
// Email addresses
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}
```

## Automated Tools

### Recommended Tools

**1. git-secrets**
```bash
# Install
brew install git-secrets

# Setup
git secrets --install
git secrets --register-aws

# Scan
git secrets --scan
```

**2. truffleHog**
```bash
# Install
pip install truffleHog

# Scan
trufflehog --regex --entropy=False .
```

**3. detect-secrets**
```bash
# Install
pip install detect-secrets

# Scan
detect-secrets scan --all-files
```

**4. gitleaks**
```bash
# Install
brew install gitleaks

# Scan
gitleaks detect --source . --verbose
```

## Git Hooks and Pre-Commit Hooks

Set up git hooks to prevent committing secrets before they enter the repository.

### Pre-Commit Hook Setup

**1. Using git-secrets**

```bash
# Install and initialize
brew install git-secrets
cd /path/to/your/repo
git secrets --install
git secrets --register-aws

# Add custom patterns
git secrets --add 'sk-[a-zA-Z0-9]{32,}'
git secrets --add 'AKIA[0-9A-Z]{16}'
```

**2. Using gitleaks**

```bash
# Install and create hook
brew install gitleaks
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/sh
gitleaks detect --staged --verbose
if [ $? -ne 0 ]; then
    echo "❌ gitleaks detected secrets. Commit aborted."
    exit 1
fi
EOF
chmod +x .git/hooks/pre-commit
```

**3. Using detect-secrets**

```bash
# Install and create baseline
pip install detect-secrets
detect-secrets scan > .secrets.baseline

# Create hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/sh
detect-secrets scan --baseline .secrets.baseline
if [ $? -ne 0 ]; then
    echo "❌ New secrets detected. Commit aborted."
    exit 1
fi
EOF
chmod +x .git/hooks/pre-commit
```

**4. Using Husky (Node.js)**

```bash
npm install --save-dev husky
npx husky install
npx husky add .husky/pre-commit "gitleaks detect --staged --verbose"
```

**5. Manual Pre-Commit Hook**

Create `.git/hooks/pre-commit`:

```bash
#!/bin/sh
# Check for API keys
if git diff --cached --name-only | xargs grep -E "(sk-[a-zA-Z0-9]{32,}|AKIA[0-9A-Z]{16})" 2>/dev/null; then
    echo "❌ API keys detected!"
    exit 1
fi

# Check for .env files
if git diff --cached --name-only | grep -E "\.env$" | grep -v "\.env\.example"; then
    echo "❌ .env file detected!"
    exit 1
fi

exit 0
```

Make executable: `chmod +x .git/hooks/pre-commit`

### CI/CD Integration

**GitHub Actions:**

```yaml
name: Secret Scanning
on: [push, pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@v2
```

## Checklist

### Before Open Sourcing

- [ ] No hardcoded API keys in code
- [ ] No database credentials in code
- [ ] No private keys or certificates committed
- [ ] `.env` files in `.gitignore`
- [ ] Only `.env.example` committed (with placeholders)
- [ ] **Git history scanned for secrets (CRITICAL)**
- [ ] All branches checked for secrets
- [ ] All tags checked for secrets
- [ ] Deleted files checked for secrets
- [ ] Merge commits checked for secrets
- [ ] No secrets found in git history
- [ ] Git history cleaned if secrets were found
- [ ] No personal information in code
- [ ] No real credentials in test files
- [ ] No secrets in documentation
- [ ] Configuration files use environment variables
- [ ] All sensitive files in `.gitignore`

### Files to Verify

- [ ] `.env` - Should be ignored
- [ ] `.env.local` - Should be ignored
- [ ] `.env.production` - Should be ignored
- [ ] `config.json` - Should not contain secrets
- [ ] `secrets.json` - Should not exist or be ignored
- [ ] `*.key`, `*.pem` - Should be ignored
- [ ] `id_rsa*` - Should be ignored
- [ ] README.md - Should not contain real secrets
- [ ] Documentation files - Should not contain secrets

## Output Format

When checking for private information:

```
🔍 PRIVATE INFORMATION SCAN REPORT

Repository: [repo-name]
Date: [date]
Scanner: [tool/agent]

📊 SUMMARY
- Critical issues: 3
- Warnings: 5
- Files scanned: 150
- Patterns checked: 12
- Git history scanned: Yes
- Branches checked: 5
- Commits in history: 1,234

🚨 CRITICAL ISSUES

1. Hardcoded API Key Found
   File: src/config/api.ts:23
   Line: const apiKey = 'sk-1234567890abcdef';
   Issue: OpenAI API key exposed in code
   Fix: Move to environment variable
   Severity: CRITICAL
   Action: Remove immediately and rotate key

2. Database Credentials in Code
   File: src/database/config.ts:12
   Line: const mongoUri = 'mongodb://user:password@host:27017/db';
   Issue: Database credentials exposed
   Fix: Use environment variable
   Severity: CRITICAL
   Action: Remove and change database password

3. Secrets Found in Git History
   Commit: abc123def (2024-01-15)
   File: config/secrets.json (now deleted)
   Issue: API key was committed and then deleted, but still in history
   Fix: Clean git history using git-filter-repo
   Severity: CRITICAL
   Action: Remove from history and rotate exposed keys

⚠️  WARNINGS

1. .env File Not in .gitignore
   File: .env
   Issue: Environment file may be committed
   Fix: Add .env to .gitignore
   Severity: HIGH

[... more issues ...]

✅ SAFE FILES

- ✅ .env.example contains only placeholders
- ✅ All config files use environment variables
- ✅ No secrets in documentation
- ✅ Test files use mock credentials

📜 GIT HISTORY SCAN RESULTS

- ✅ Current files: No secrets detected
- ⚠️  Git history: 2 secrets found in old commits
- ✅ All branches scanned: main, develop, feature/*
- ✅ All tags scanned: v1.0.0, v1.1.0
- ⚠️  Action required: Clean git history before open sourcing

💡 RECOMMENDATIONS

1. Add .env to .gitignore if not already
2. Use environment variables for all secrets
3. Rotate any exposed API keys
4. Clean git history if secrets were committed
5. Set up pre-commit hooks to prevent future commits
6. Use secret scanning in CI/CD

📋 NEXT STEPS

1. Fix critical issues immediately
2. Rotate any exposed credentials
3. Clean git history if needed
4. Set up automated scanning
5. Review and approve before open sourcing
```

## Best Practices

1. **Never commit secrets**: Always use environment variables
2. **Use .env.example**: Provide template with placeholders
3. **Rotate exposed secrets**: If secrets were committed, rotate them
4. **Clean git history**: Remove secrets from history if committed
5. **Automate scanning**: Use pre-commit hooks and CI/CD checks
6. **Document requirements**: List required environment variables
7. **Use secret management**: Consider services like AWS Secrets Manager
8. **Regular audits**: Scan before each release

## Resources

### Tools
- git-secrets: https://github.com/awslabs/git-secrets
- truffleHog: https://github.com/trufflesecurity/trufflehog
- detect-secrets: https://github.com/Yelp/detect-secrets
- gitleaks: https://github.com/gitleaks/gitleaks

### Guides
- GitHub: Removing sensitive data from a repository
- OWASP: Secrets Management Cheat Sheet
- Git: Rewriting History

---

**When this skill is active**, you will:
1. Scan the codebase for private information patterns
2. Check for hardcoded secrets and credentials
3. Verify .gitignore includes sensitive files
4. Review git history for exposed secrets
5. Provide actionable recommendations
6. Generate a comprehensive report
7. Help clean up any found issues before open sourcing

