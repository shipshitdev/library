---
name: email-finder
description: This skill should be used when users need to find email addresses associated with a domain. It activates when users ask to scan a domain for emails, find contact emails, discover email addresses, or replace email hunter functionality.
metadata:
  short-description: Find email addresses for a domain
---

# Email Finder

Discover email addresses associated with a domain using free methods (web scraping, pattern guessing, WHOIS) first, then API methods (Hunter.io, Apollo.io, etc.) if keys are available.

## When to Use

Use when:
- Scanning a domain for email addresses
- Finding contact emails for a company
- Replacing email hunter functionality
- Discovering email patterns
- Verifying found emails

## Project Context Discovery

Before finding emails:

1. Check project docs for existing email discovery tools
2. Check for available API keys (Hunter.io, Apollo.io, etc.)
3. Review compliance/privacy requirements
4. Look for `[project]-email-finder` skill

## Methodology

Use hybrid approach: **free methods first**, then **API methods** (if keys available).

### Free Methods

#### 1. Web Scraping

Scan domain pages to extract emails from public content.

Target pages: `/contact`, `/about`, `/team`, footer, header, blog author pages.

```typescript
// Extract emails from domain pages
async function scrapeDomainForEmails(domain: string): Promise<string[]> {
  const emails = new Set<string>();
  const emailRegex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
  const pagesToCheck = ['/contact', '/about', '/team', '/people'];

  for (const page of pagesToCheck) {
    try {
      const url = `https://${domain}${page}`;
      const html = await fetch(url).then(r => r.text());
      const foundEmails = html.match(emailRegex);
      if (foundEmails) {
        foundEmails.forEach((email) => {
          if (email.includes(domain)) {
            emails.add(email.toLowerCase());
          }
        });
      }
    } catch (error) {
      continue;
    }
  }

  return Array.from(emails);
}
```

Best practices:
- Respect robots.txt
- Rate limit (delay between requests)
- Filter non-personal emails if needed

#### 2. WHOIS Lookup

Query WHOIS databases for registration contact emails.

```python
# Extract emails from WHOIS data
import whois

def get_whois_emails(domain: str) -> list[str]:
    emails = []
    try:
        w = whois.whois(domain)
        if w.emails:
            emails.extend(w.emails if isinstance(w.emails, list) else [w.emails])
        if hasattr(w, 'registrar_email') and w.registrar_email:
            emails.append(w.registrar_email)
    except Exception:
        pass
    return list(set(e.lower() for e in emails if e))
```

Note: Many domains use privacy protection, so WHOIS emails may be masked.

#### 3. Pattern Guessing

Generate potential emails based on common patterns and names.

Common patterns: `firstname.lastname@domain`, `firstnamelastname@domain`, `firstname@domain`, `f.lastname@domain`.

```typescript
// Generate email patterns from names
function generateEmailPatterns(
  firstName: string,
  lastName: string,
  domain: string
): string[] {
  return [
    `${firstName}.${lastName}@${domain}`,
    `${firstName}${lastName}@${domain}`,
    `${firstName}@${domain}`,
    `${firstName.charAt(0)}.${lastName}@${domain}`,
    `${firstName}_${lastName}@${domain}`,
    `${firstName.charAt(0)}${lastName}@${domain}`,
  ].map(e => e.toLowerCase());
}
```

Note: Verify guessed emails before use.

### API Methods (Optional)

#### Hunter.io

Setup: Sign up at https://hunter.io, get API key, add `HUNTER_API_KEY=...` to env.

```typescript
// Domain search
async function findEmailsWithHunter(domain: string): Promise<any[]> {
  const response = await fetch(
    `https://api.hunter.io/v2/domain-search?domain=${domain}&api_key=${process.env.HUNTER_API_KEY}`
  );
  const data = await response.json();
  return data.data.emails || [];
}

// Email verification
async function verifyEmailWithHunter(email: string): Promise<boolean> {
  const response = await fetch(
    `https://api.hunter.io/v2/email-verifier?email=${email}&api_key=${process.env.HUNTER_API_KEY}`
  );
  const data = await response.json();
  return data.data.result === 'deliverable';
}
```

#### Apollo.io

Setup: Sign up at https://www.apollo.io, get API key, add `APOLLO_API_KEY=...` to env.

```typescript
async function findEmailsWithApollo(domain: string): Promise<any[]> {
  const response = await fetch('https://api.apollo.io/v1/mixed_people/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      api_key: process.env.APOLLO_API_KEY,
      q_organization_domains: domain,
      page: 1,
      per_page: 25,
    }),
  });
  const data = await response.json();
  return data.people || [];
}
```

#### Snov.io

Setup: Sign up at https://snov.io, get client ID/secret, add `SNOV_CLIENT_ID=...`, `SNOV_CLIENT_SECRET=...` to env.

```typescript
async function findEmailsWithSnov(domain: string): Promise<any[]> {
  // Get access token
  const tokenResponse = await fetch('https://api.snov.io/v1/oauth/access_token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      grant_type: 'client_credentials',
      client_id: process.env.SNOV_CLIENT_ID,
      client_secret: process.env.SNOV_CLIENT_SECRET,
    }),
  });
  const { access_token } = await tokenResponse.json();

  // Search for emails
  const response = await fetch(
    `https://api.snov.io/v2/domain-emails-with-info?domain=${domain}&access_token=${access_token}&type=all&limit=100`
  );
  const data = await response.json();
  return data.result?.emails || [];
}
```

#### Clearbit

Setup: Sign up at https://clearbit.com, get API key, add `CLEARBIT_API_KEY=...` to env.

```typescript
async function findEmailsWithClearbit(domain: string): Promise<any[]> {
  const response = await fetch(
    `https://person.clearbit.com/v2/combined/find?domain=${domain}`,
    {
      headers: { Authorization: `Bearer ${process.env.CLEARBIT_API_KEY}` },
    }
  );
  const data = await response.json();
  return data.person ? [data.person] : [];
}
```

## Complete Implementation

Hybrid approach example:

```typescript
interface EmailResult {
  email: string;
  source: 'web-scraping' | 'whois' | 'pattern-guessing' | 'hunter' | 'apollo' | 'snov' | 'clearbit';
  confidence?: number;
  firstName?: string;
  lastName?: string;
  position?: string;
  verified?: boolean;
}

async function findEmailsForDomain(domain: string): Promise<EmailResult[]> {
  const results: EmailResult[] = [];
  const seenEmails = new Set<string>();

  // Free methods first
  try {
    const scrapedEmails = await scrapeDomainForEmails(domain);
    scrapedEmails.forEach((email) => {
      if (!seenEmails.has(email)) {
        results.push({ email, source: 'web-scraping' });
        seenEmails.add(email);
      }
    });
  } catch (error) {
    console.error('Web scraping failed:', error);
  }

  // API methods if keys available
  if (process.env.HUNTER_API_KEY) {
    try {
      const hunterEmails = await findEmailsWithHunter(domain);
      hunterEmails.forEach((emailData: any) => {
        const email = emailData.value?.toLowerCase();
        if (email && !seenEmails.has(email)) {
          results.push({
            email,
            source: 'hunter',
            confidence: emailData.confidence_score,
            firstName: emailData.first_name,
            lastName: emailData.last_name,
            position: emailData.position,
          });
          seenEmails.add(email);
        }
      });
    } catch (error) {
      console.error('Hunter.io failed:', error);
    }
  }

  if (process.env.APOLLO_API_KEY) {
    try {
      const apolloContacts = await findEmailsWithApollo(domain);
      apolloContacts.forEach((contact: any) => {
        const email = contact.email?.toLowerCase();
        if (email && !seenEmails.has(email)) {
          results.push({
            email,
            source: 'apollo',
            firstName: contact.first_name,
            lastName: contact.last_name,
            position: contact.title,
          });
          seenEmails.add(email);
        }
      });
    } catch (error) {
      console.error('Apollo.io failed:', error);
    }
  }

  // Verify emails if Hunter.io key available
  if (process.env.HUNTER_API_KEY) {
    for (const result of results) {
      if (!result.verified) {
        try {
          result.verified = await verifyEmailWithHunter(result.email);
        } catch (error) {
          // Skip if verification fails
        }
      }
    }
  }

  return results;
}
```

## Email Verification

Always verify emails before use, especially guessed or scraped ones.

### Basic Validation

```typescript
function isValidEmailFormat(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
```

### MX Record Check

```typescript
import { promises as dns } from 'dns';

async function hasValidMXRecord(domain: string): Promise<boolean> {
  try {
    const mxRecords = await dns.resolveMx(domain);
    return mxRecords.length > 0;
  } catch {
    return false;
  }
}
```

### API Verification

Use Hunter.io or other services for reliable verification (see Hunter.io example above).

## Best Practices

### Rate Limiting

```typescript
class RateLimiter {
  private delay: number;
  private lastRequest: number = 0;

  constructor(delayMs: number) {
    this.delay = delayMs;
  }

  async wait(): Promise<void> {
    const now = Date.now();
    const timeSince = now - this.lastRequest;
    if (timeSince < this.delay) {
      await new Promise(resolve => setTimeout(resolve, this.delay - timeSince));
    }
    this.lastRequest = Date.now();
  }
}
```

### Error Handling

Handle errors gracefully and continue with other methods:

```typescript
async function findEmailsWithFallback(domain: string): Promise<EmailResult[]> {
  const methods = [
    () => scrapeDomainForEmails(domain),
    () => findEmailsWithHunter(domain).catch(() => []),
    () => findEmailsWithApollo(domain).catch(() => []),
  ];

  const allResults: EmailResult[] = [];
  for (const method of methods) {
    try {
      allResults.push(...await method());
    } catch (error) {
      // Continue with next method
    }
  }

  return allResults;
}
```

### Data Quality

- Deduplicate emails
- Normalize (lowercase, trim)
- Filter non-personal addresses if needed
- Verify when possible
- Include metadata (source, confidence, position)

## Legal & Ethical Considerations

### Compliance

- **GDPR/CCPA:** Comply with data protection regulations
- **CAN-SPAM:** Comply if sending emails
- **Terms of Service:** Respect website ToS and robots.txt
- **Rate Limiting:** Don't overwhelm servers

### Ethical Use

- Only use publicly available information
- Respect privacy settings
- Use emails responsibly (don't spam)
- Provide value in communications
- Honor unsubscribe requests

### Robots.txt Compliance

```typescript
async function checkRobotsTxt(domain: string, path: string): Promise<boolean> {
  try {
    const robotsUrl = `https://${domain}/robots.txt`;
    const robotsContent = await fetch(robotsUrl).then(r => r.text());
    
    // Simple check - use proper parser in production
    const lines = robotsContent.split('\n');
    for (const line of lines) {
      if (line.startsWith('Disallow:')) {
        const disallowedPath = line.substring(9).trim();
        if (path.startsWith(disallowedPath)) {
          return false;
        }
      }
    }
    return true;
  } catch {
    return true; // Proceed with caution if robots.txt unavailable
  }
}
```

## Example Requests

1. **"Scan example.com and find all email addresses"**
   - Use web scraping, WHOIS, APIs if available
   - Return deduplicated list with sources

2. **"Find emails for contact@example.com domain"**
   - Focus on contact page
   - Use pattern guessing
   - Verify emails

3. **"Replace email hunter - find emails for acme.com"**
   - Use hybrid approach
   - Provide results similar to email hunter format
   - Include verification and confidence scores

## Integration

Works with:
- **leads-researcher:** Use email-finder after researching companies
- **copywriter:** Use found emails for outreach campaigns
- Project-specific lead generation workflows

