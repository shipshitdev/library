# Git Safety - Full Guide

## 1. SCAN - Detect Sensitive Files

### Sensitive File Patterns

```bash
# Environment files
.env
.env.*
*.env
.envrc

# Credential files
credentials.json
service-account*.json
*-credentials.json
*.pem
*.key
*.p12
*.pfx
id_rsa*
id_ed25519*
id_ecdsa*

# Cloud provider configs
.aws/credentials
.aws/config
.gcp/credentials.json
.azure/credentials

# Database
*.sql (check for passwords)
database.yml (check for passwords)

# API/Secret files
secrets.yml
secrets.json
*.secret
api_keys.*
auth.json

# Package manager tokens
.npmrc (with auth tokens)
.pypirc
.gem/credentials

# Other
*.log (may contain secrets)
.htpasswd
.netrc
.docker/config.json
kubeconfig
```

### Scan Commands

**Step 1: Check current working directory**

```bash
# List potentially sensitive files in current state
find . -type f \( \
  -name ".env" -o \
  -name ".env.*" -o \
  -name "*.env" -o \
  -name "credentials.json" -o \
  -name "service-account*.json" -o \
  -name "*.pem" -o \
  -name "*.key" -o \
  -name "id_rsa*" -o \
  -name "secrets.*" -o \
  -name ".npmrc" -o \
  -name "*.secret" \
\) 2>/dev/null | grep -v node_modules | grep -v .git
```

**Step 2: Check git history for sensitive files**

```bash
# Search all commits for sensitive filenames
git log --all --full-history --diff-filter=A -- \
  "*.env" ".env" ".env.*" \
  "credentials.json" "service-account*.json" \
  "*.pem" "*.key" "id_rsa*" \
  "secrets.*" ".npmrc" "*.secret" \
  --name-only --pretty=format:"%h %s" 2>/dev/null

# Alternative: List all files ever committed
git log --all --pretty=format: --name-only --diff-filter=A | sort -u | grep -E '\.(env|pem|key|secret)$|credentials|secrets\.|id_rsa'
```

**Step 3: Search for secrets in file contents**

```bash
# Search for common secret patterns in tracked files
git grep -E "(api[_-]?key|apikey|secret[_-]?key|password|passwd|pwd|token|auth[_-]?token|access[_-]?token|private[_-]?key|client[_-]?secret)" --cached -- ':!*.lock' ':!package-lock.json' ':!yarn.lock' 2>/dev/null | head -50

# Search git history for secret patterns (expensive but thorough)
git log -p --all -S 'API_KEY' --source -- ':(exclude)*.lock' 2>/dev/null | head -100
```

**Step 4: Check .gitignore coverage**

```bash
# Verify sensitive patterns are in .gitignore
for pattern in ".env" ".env.*" "*.pem" "*.key" "credentials.json" "secrets.*"; do
  if ! grep -q "$pattern" .gitignore 2>/dev/null; then
    echo "Missing from .gitignore: $pattern"
  fi
done
```

### Scan Report Format

```
## Git Safety Scan Results

### Current Directory
- [ ] No sensitive files found
- [X] Found: .env.local (not tracked - OK)
- [!] Found: credentials.json (TRACKED - DANGER)

### Git History
- [ ] No sensitive files in history
- [!] Found in history: .env (commit abc1234, 2024-01-15)
- [!] Found in history: api-keys.json (commit def5678, 2024-02-20)

### Secret Patterns in Code
- [ ] No hardcoded secrets detected
- [!] Possible API key in: src/config.ts:42

### .gitignore Coverage
- [X] .env patterns covered
- [ ] Missing: *.pem
- [ ] Missing: credentials.json

### Recommendations
1. [URGENT] Rotate any exposed credentials immediately
2. Run `/git-safety clean` to remove files from history
3. Run `/git-safety prevent` to update .gitignore
```

---

## 2. CLEAN - Remove from Git History

### Prerequisites Check

```bash
# Check if git-filter-repo is installed (preferred)
which git-filter-repo

# Check if BFG is available (alternative)
which bfg
```

### Installation (if needed)

```bash
# Install git-filter-repo (recommended)
pip install git-filter-repo

# Or via Homebrew on macOS
brew install git-filter-repo

# BFG alternative (Java required)
brew install bfg
```

### Cleaning Process

**IMPORTANT: Before cleaning, ensure:**

1. All team members have pushed their changes
2. You have a backup of the repository
3. You understand this rewrites history (force push required)

**Step 1: Create backup**

```bash
# Clone a backup
git clone --mirror . ../repo-backup-$(date +%Y%m%d)
```

**Step 2: Remove specific files with git-filter-repo**

```bash
# Remove a single file from all history
git filter-repo --path .env --invert-paths

# Remove multiple files
git filter-repo --path .env --path credentials.json --path secrets.yml --invert-paths

# Remove by pattern
git filter-repo --path-glob '*.env' --invert-paths
git filter-repo --path-glob '*.pem' --invert-paths
```

**Step 3: Alternative - BFG Repo Cleaner**

```bash
# Remove specific file
bfg --delete-files .env

# Remove files matching pattern
bfg --delete-files '*.pem'

# Remove files containing secrets (by content)
bfg --replace-text passwords.txt  # File containing patterns to remove
```

**Step 4: Clean up and force push**

```bash
# Expire old references
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push to remote (DESTRUCTIVE - requires --force)
# WARNING: This rewrites history for ALL collaborators
git push origin --force --all
git push origin --force --tags
```

**Step 5: Notify team**
All collaborators must:

```bash
# Delete local repo and re-clone
rm -rf local-repo
git clone <remote-url>

# OR rebase on new history (advanced)
git fetch origin
git rebase origin/main
```

### Post-Clean Verification

```bash
# Verify file is gone from all history
git log --all --full-history -- .env
# Should return empty

# Verify content is gone
git log -p --all -S 'YOUR_SECRET_VALUE' --source
# Should return empty
```

---

## 3. PREVENT - Set Up Protection

### Update .gitignore

```gitignore
# Environment files
.env
.env.*
*.env
.envrc
!.env.example
!.env.template

# Credentials and secrets
credentials.json
*-credentials.json
service-account*.json
secrets.yml
secrets.json
*.secret
api_keys.*
auth.json

# Private keys
*.pem
*.key
*.p12
*.pfx
id_rsa
id_rsa.*
id_ed25519
id_ed25519.*
id_ecdsa
id_ecdsa.*

# Cloud provider configs
.aws/
.gcp/
.azure/
kubeconfig
.kube/config

# Package manager auth
.npmrc
.pypirc
.gem/credentials
.docker/config.json

# Database
*.sql
!schema.sql
!migrations/*.sql

# Logs (may contain secrets)
*.log
logs/

# OS files
.DS_Store
Thumbs.db

# IDE with potential secrets
.idea/
.vscode/settings.json
```

### Set Up Pre-commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Pre-commit hook to prevent committing sensitive files

RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Files that should never be committed
FORBIDDEN_FILES=(
  ".env"
  "credentials.json"
  "secrets.yml"
  "secrets.json"
  "*.pem"
  "*.key"
  "id_rsa"
  ".npmrc"
)

# Patterns that indicate secrets in file content
SECRET_PATTERNS=(
  "PRIVATE KEY"
  "api_key.*=.*['\"][a-zA-Z0-9]"
  "apiKey.*:.*['\"][a-zA-Z0-9]"
  "password.*=.*['\"][^'\"]+['\"]"
  "secret.*=.*['\"][a-zA-Z0-9]"
  "AWS_SECRET"
  "ANTHROPIC_API_KEY"
  "OPENAI_API_KEY"
)

ERRORS=0

# Check for forbidden files
for pattern in "${FORBIDDEN_FILES[@]}"; do
  files=$(git diff --cached --name-only | grep -E "$pattern" || true)
  if [ -n "$files" ]; then
    echo -e "${RED}ERROR: Attempting to commit forbidden file matching '$pattern':${NC}"
    echo "$files"
    ERRORS=$((ERRORS + 1))
  fi
done

# Check for secret patterns in staged content
for pattern in "${SECRET_PATTERNS[@]}"; do
  matches=$(git diff --cached -U0 | grep -E "^\+" | grep -iE "$pattern" || true)
  if [ -n "$matches" ]; then
    echo -e "${YELLOW}WARNING: Possible secret detected matching '$pattern':${NC}"
    echo "$matches" | head -5
    ERRORS=$((ERRORS + 1))
  fi
done

if [ $ERRORS -gt 0 ]; then
  echo ""
  echo -e "${RED}Commit blocked due to potential secrets.${NC}"
  echo "If this is a false positive, use: git commit --no-verify"
  echo "But first, verify these files don't contain real secrets!"
  exit 1
fi

exit 0
```

Make executable:

```bash
chmod +x .git/hooks/pre-commit
```

### Set Up git-secrets (Optional - AWS)

```bash
# Install git-secrets
brew install git-secrets

# Set up for AWS patterns
git secrets --install
git secrets --register-aws

# Add custom patterns
git secrets --add 'ANTHROPIC_API_KEY.*=.*sk-ant-'
git secrets --add 'OPENAI_API_KEY.*=.*sk-'
```

### Create .env.example Template

```bash
# .env.example - Safe template for environment variables
# Copy to .env and fill in your values
# NEVER commit .env files!

# API Keys
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Auth
JWT_SECRET=generate_a_secure_random_string
SESSION_SECRET=generate_another_secure_string
```

---

## Handling Specific Platforms

### GitHub

- Enable secret scanning in repository settings
- Use GitHub Actions secrets for CI/CD
- Consider using GitHub's push protection

### GitLab

- Enable Secret Detection CI/CD component
- Use CI/CD variables for secrets

### Vercel/Netlify

- Use environment variables in dashboard
- Never commit production secrets

---

## Emergency Response Checklist

If you've leaked credentials:

1. **IMMEDIATELY rotate the credential** (this is the only real fix)
2. Check access logs for unauthorized usage
3. Run `/git-safety clean` to remove from history
4. Force push the cleaned history
5. Notify affected team members to re-clone
6. Update .gitignore to prevent recurrence
7. Set up pre-commit hooks
8. Document the incident
