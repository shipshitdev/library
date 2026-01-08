# Security Audit - Security Scanning Command

**Purpose:** Comprehensive security audit for React, Next.js, NestJS applications covering dependencies, code patterns, configuration, and best practices.

## When to Use

- Before deploying to production
- After adding new dependencies
- Regular security reviews
- After security incidents
- Compliance audits

## Project Context Discovery

**Before auditing, discover the project's setup:**

1. **Identify Project Type:**
   - Check for React/Next.js/NestJS structure
   - Identify authentication system (Clerk, Auth0, custom)
   - Check for API endpoints
   - Review database setup (MongoDB)

2. **Discover Security Configurations:**
   - Check for `.env` files and secrets management
   - Review authentication/authorization patterns
   - Check CORS configuration
   - Review rate limiting setup

3. **Identify Dependencies:**
   - Check `package.json` for dependencies
   - Review `package-lock.json` or `pnpm-lock.yaml`
   - Check for security-related packages

## Security Audit Workflow

### Phase 1: Dependency Security

**1.1 Dependency Vulnerability Scan**

```bash
# NPM
npm audit

# PNPM
pnpm audit

# Yarn
yarn audit

# Fix automatically (review first!)
npm audit fix
```

**1.2 Check for Outdated Packages**

```bash
# Check outdated packages
npm outdated

# Review security advisories
npm audit --json > audit-report.json
```

**1.3 License Compliance**

```bash
# Check licenses
npm license-checker --summary

# Review for problematic licenses
npm license-checker --onlyAllow 'MIT;Apache-2.0;ISC'
```

### Phase 2: Code Security Patterns

**2.1 Authentication & Authorization**

**Check for:**

- ✅ All API endpoints protected
- ✅ Authentication guards applied
- ✅ Authorization checks present
- ✅ JWT token validation
- ✅ Session management secure
- ✅ Password hashing (bcrypt, argon2)
- ✅ No hardcoded credentials

**Common Issues:**

```typescript
// ❌ BAD: No authentication
@Get('/users')
async getUsers() {
  return this.usersService.findAll();
}

// ✅ GOOD: Protected endpoint
@Get('/users')
@UseGuards(AuthGuard)
async getUsers(@CurrentUser() user) {
  return this.usersService.findAll(user.organizationId);
}
```

**2.2 Input Validation**

**Check for:**

- ✅ DTOs with validation decorators
- ✅ Input sanitization
- ✅ SQL injection prevention (if using SQL)
- ✅ NoSQL injection prevention (MongoDB)
- ✅ XSS prevention
- ✅ CSRF protection

**Common Issues:**

```typescript
// ❌ BAD: No validation
@Post('/users')
async createUser(@Body() data: any) {
  return this.usersService.create(data);
}

// ✅ GOOD: Validated DTO
@Post('/users')
async createUser(@Body() dto: CreateUserDto) {
  return this.usersService.create(dto);
}

// DTO with validation
export class CreateUserDto {
  @IsEmail()
  @IsNotEmpty()
  email: string;
  
  @IsString()
  @MinLength(8)
  password: string;
}
```

**2.3 Data Isolation (Multi-Tenancy)**

**Check for:**

- ✅ Organization/tenant filtering in all queries
- ✅ No cross-tenant data access
- ✅ User can only access their org's data
- ✅ Soft delete filtering (`isDeleted: false`)

**Common Issues:**

```typescript
// ❌ BAD: No organization filter
async findAll() {
  return this.model.find({});
}

// ✅ GOOD: Organization filtering
async findAll(organizationId: string) {
  return this.model.find({
    organization: organizationId,
    isDeleted: false
  });
}
```

**2.4 Secrets Management**

**Check for:**

- ✅ No hardcoded secrets in code
- ✅ Environment variables used
- ✅ `.env` files in `.gitignore`
- ✅ Secrets not in version control
- ✅ Proper secret rotation

**Common Issues:**

```typescript
// ❌ BAD: Hardcoded secret
const apiKey = 'sk-1234567890';

// ✅ GOOD: Environment variable
const apiKey = process.env.API_KEY;
```

### Phase 3: Configuration Security

**3.1 Environment Variables**

**Check:**

- `.env.example` exists (without secrets)
- `.env` in `.gitignore`
- Required variables documented
- Default values are safe
- No secrets in config files

**3.2 CORS Configuration**

```typescript
// ✅ GOOD: Restrictive CORS
app.enableCors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || [],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
});

// ❌ BAD: Allow all origins
app.enableCors({ origin: '*' });
```

**3.3 Rate Limiting**

```typescript
// ✅ GOOD: Rate limiting enabled
@UseGuards(ThrottlerGuard)
@Throttle(10, 60) // 10 requests per minute
@Get('/api/data')
async getData() {
  return this.dataService.findAll();
}
```

**3.4 HTTPS/TLS**

- ✅ HTTPS enforced in production
- ✅ TLS certificates valid
- ✅ HSTS headers configured
- ✅ Secure cookie flags

### Phase 4: Frontend Security

**4.1 XSS Prevention**

**Check for:**

- ✅ React's automatic escaping
- ✅ No `dangerouslySetInnerHTML` without sanitization
- ✅ Content Security Policy headers
- ✅ Input sanitization libraries

**4.2 Authentication Tokens**

**Check for:**

- ✅ Tokens stored securely (httpOnly cookies preferred)
- ✅ No tokens in localStorage (if XSS risk)
- ✅ Token expiration handling
- ✅ Refresh token rotation

**4.3 API Security**

**Check for:**

- ✅ API keys not exposed in frontend
- ✅ Sensitive operations require authentication
- ✅ Request validation
- ✅ Error messages don't leak information

### Phase 5: Database Security

**5.1 MongoDB Security**

**Check for:**

- ✅ Connection string secure (not hardcoded)
- ✅ Database user with minimal privileges
- ✅ Network access restricted
- ✅ Encryption at rest enabled
- ✅ Regular backups

**5.2 Query Security**

**Check for:**

- ✅ No user input in queries without validation
- ✅ Parameterized queries
- ✅ Injection prevention
- ✅ Index usage (performance = security)

**Common Issues:**

```typescript
// ❌ BAD: Injection risk
const query = { [userInput]: value };

// ✅ GOOD: Validated input
const query = { 
  organization: validatedOrgId,
  email: validatedEmail 
};
```

### Phase 6: Infrastructure Security

**6.1 AWS Security**

**Check for:**

- ✅ IAM roles with least privilege
- ✅ Security groups properly configured
- ✅ S3 buckets not publicly accessible
- ✅ Secrets in AWS Secrets Manager
- ✅ CloudTrail logging enabled
- ✅ VPC configuration secure

**6.2 Docker Security**

**Check for:**

- ✅ Non-root user in containers
- ✅ Minimal base images
- ✅ No secrets in Dockerfile
- ✅ Image scanning enabled
- ✅ Regular updates

## Security Checklist

### Critical (Must Fix)

- [ ] No hardcoded secrets
- [ ] All endpoints authenticated
- [ ] Input validation on all inputs
- [ ] SQL/NoSQL injection prevention
- [ ] XSS prevention
- [ ] CSRF protection
- [ ] Multi-tenancy enforced
- [ ] Secrets in environment variables
- [ ] HTTPS enforced
- [ ] Dependencies up to date

### High Priority

- [ ] Rate limiting configured
- [ ] CORS properly configured
- [ ] Error messages don't leak info
- [ ] Logging doesn't expose secrets
- [ ] Password hashing secure
- [ ] Session management secure
- [ ] Database access restricted
- [ ] Backups encrypted

### Medium Priority

- [ ] Security headers configured
- [ ] Content Security Policy
- [ ] Dependency licenses reviewed
- [ ] Security monitoring enabled
- [ ] Incident response plan
- [ ] Security documentation updated

## Automated Security Tools

**Run these tools:**

```bash
# Dependency scanning
npm audit
pnpm audit

# Code scanning (if available)
npm run lint:security

# SAST tools (if configured)
# SonarQube, Snyk, etc.

# Container scanning (if using Docker)
docker scan [image-name]
```

## Common Vulnerabilities to Check

### 1. OWASP Top 10

1. **Broken Access Control**
   - Check authorization on all endpoints
   - Verify multi-tenancy
   - Test privilege escalation

2. **Cryptographic Failures**
   - Check password hashing
   - Verify encryption in transit
   - Check encryption at rest

3. **Injection**
   - SQL injection (if using SQL)
   - NoSQL injection (MongoDB)
   - Command injection
   - LDAP injection

4. **Insecure Design**
   - Review architecture
   - Check threat modeling
   - Verify security requirements

5. **Security Misconfiguration**
   - Check default configurations
   - Verify security headers
   - Review error handling

6. **Vulnerable Components**
   - Check dependencies
   - Review versions
   - Update regularly

7. **Authentication Failures**
   - Check password policies
   - Verify session management
   - Review MFA implementation

8. **Software and Data Integrity**
   - Check CI/CD security
   - Verify code signing
   - Review update mechanisms

9. **Security Logging Failures**
   - Check audit logs
   - Verify log retention
   - Review monitoring

10. **SSRF**
    - Check URL handling
    - Verify input validation
    - Review network access

## Output Format

When running security audit:

```
🔒 SECURITY AUDIT REPORT

Project: [project-name]
Date: [date]
Auditor: [name]

📊 SUMMARY
- Critical issues: 2
- High priority: 5
- Medium priority: 8
- Low priority: 3

🚨 CRITICAL ISSUES

1. Hardcoded API Key Found
   File: src/config.ts:45
   Issue: API key exposed in code
   Fix: Move to environment variable
   Severity: CRITICAL

2. Missing Authentication Guard
   File: src/users/users.controller.ts:23
   Issue: Endpoint not protected
   Fix: Add @UseGuards(AuthGuard)
   Severity: CRITICAL

⚠️  HIGH PRIORITY ISSUES

1. No Input Validation
   File: src/posts/posts.controller.ts:12
   Issue: DTO missing validation decorators
   Fix: Add class-validator decorators
   Severity: HIGH

[... more issues ...]

✅ SECURITY STRENGTHS

- ✅ All dependencies up to date
- ✅ HTTPS enforced
- ✅ Rate limiting configured
- ✅ Multi-tenancy implemented correctly

💡 RECOMMENDATIONS

1. Enable dependency scanning in CI/CD
2. Add security headers middleware
3. Implement security monitoring
4. Regular security audits (quarterly)

📋 NEXT STEPS

1. Fix critical issues immediately
2. Address high priority within 1 week
3. Plan medium priority fixes
4. Schedule follow-up audit
```

---

**Created:** 2025-12-24
**Purpose:** Comprehensive security auditing for React, Next.js, NestJS applications
**Focus:** OWASP Top 10, dependency security, code patterns, configuration
