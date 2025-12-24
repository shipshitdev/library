# Security Checklist

**Purpose:** Security considerations for the project.
**Last Updated:** {{DATE}}

---

## Before Deployment

### Authentication & Authorization

- [ ] All endpoints require authentication (where appropriate)
- [ ] Role-based access control implemented
- [ ] JWT tokens have reasonable expiration
- [ ] Sensitive operations require re-authentication

### Input Validation

- [ ] All user input is validated
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output encoding)
- [ ] File upload validation (type, size, content)

### Data Protection

- [ ] Sensitive data encrypted at rest
- [ ] HTTPS enforced
- [ ] Passwords properly hashed (bcrypt, argon2)
- [ ] PII handled according to regulations

### API Security

- [ ] Rate limiting implemented
- [ ] CORS properly configured
- [ ] API keys not exposed in frontend
- [ ] Sensitive data not in URLs

---

## Environment & Configuration

### Secrets Management

- [ ] No secrets in code
- [ ] Environment variables for configuration
- [ ] Different secrets per environment
- [ ] Secrets rotation policy

### Dependencies

- [ ] Dependencies regularly updated
- [ ] No known vulnerabilities (npm audit)
- [ ] Lock files committed
- [ ] Minimal dependencies

---

## Logging & Monitoring

- [ ] Security events logged
- [ ] No sensitive data in logs
- [ ] Alerting for suspicious activity
- [ ] Audit trail for sensitive operations

---

## Error Handling

- [ ] Generic error messages to users
- [ ] Detailed errors only in logs
- [ ] No stack traces in production
- [ ] Graceful degradation

---

## Infrastructure

- [ ] Firewall rules configured
- [ ] Unnecessary ports closed
- [ ] Regular backups
- [ ] Disaster recovery plan

---

## Code Review Security Checks

When reviewing code, check for:

1. **Injection vulnerabilities**
2. **Authentication bypass**
3. **Authorization flaws**
4. **Sensitive data exposure**
5. **Security misconfiguration**
6. **Insecure dependencies**

---

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)

---

## Project-Specific Security Notes

<!-- Add project-specific security considerations below -->
