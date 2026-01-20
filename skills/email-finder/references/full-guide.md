# Email Finder - Full Guide

## Methodology

This skill uses a hybrid approach: **free methods first**, then **API methods** (if API keys are available).

### Free Methods (Primary)

#### 1. Web Scraping

Scan the domain's website pages to extract email addresses from publicly available content.

**Target Pages:**

- Contact page (`/contact`, `/contact-us`)
- About page (`/about`, `/about-us`, `/team`)
- Team page (`/team`, `/people`)
- Footer and header sections
- Blog author pages
- Press/media pages

**Implementation:**

```typescript
// Web scraping to find emails on a domain
async function scrapeDomainForEmails(domain: string): Promise<string[]> {
  const emails = new Set<string>();
  const emailRegex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;

  // Common pages to check
  const pagesToCheck = [
    '/contact',
    '/contact-us',
    '/about',
    '/about-us',
    '/team',
    '/people',
  ];

  for (const page of pagesToCheck) {
    try {
      const url = `https://${domain}${page}`;
      const response = await fetch(url);
      const html = await response.text();

      // Extract emails using regex
      const foundEmails = html.match(emailRegex);
      if (foundEmails) {
        foundEmails.forEach((email) => {
          // Filter to only emails from the target domain
          if (email.includes(domain)) {
            emails.add(email.toLowerCase());
          }
        });
      }
    } catch (error) {
      // Skip pages that don't exist or can't be accessed
      continue;
    }
  }

  return Array.from(emails);
}
```

**Best Practices:**

- Respect robots.txt
- Implement rate limiting (delay between requests)
- Handle errors gracefully
- Filter out common non-personal emails (noreply@, donotreply@, etc.) if needed
- Use User-Agent header to identify your scraper

#### 2. WHOIS Lookup

Query WHOIS databases to find registration contact emails.

**Implementation:**

```python
# Python example using python-whois
import whois

def get_whois_emails(domain: str) -> list[str]:
    """Extract email addresses from WHOIS data"""
    emails = []
    try:
        w = whois.whois(domain)
        # Check various WHOIS fields for emails
        if w.emails:
            if isinstance(w.emails, list):
                emails.extend(w.emails)
            else:
                emails.append(w.emails)
        if hasattr(w, 'registrar_email') and w.registrar_email:
            emails.append(w.registrar_email)
        if hasattr(w, 'admin_email') and w.admin_email:
            emails.append(w.admin_email)
    except Exception as e:
        print(f"WHOIS lookup failed: {e}")

    # Filter and deduplicate
    return list(set(email.lower() for email in emails if email))
```

**Note:** Many domains use privacy protection services, so WHOIS emails may be masked.

#### 3. Pattern Guessing

Generate potential email addresses based on common patterns and names found on the website.

**Common Patterns:**

- `firstname.lastname@domain.com`
- `firstnamelastname@domain.com`
- `firstname@domain.com`
- `f.lastname@domain.com`
- `firstname_lastname@domain.com`
- `firstinitial.lastname@domain.com`

**Implementation:**

```typescript
// Generate email patterns from names
function generateEmailPatterns(
  firstName: string,
  lastName: string,
  domain: string
): string[] {
  const patterns = [
    `${firstName}.${lastName}@${domain}`,
    `${firstName}${lastName}@${domain}`,
    `${firstName}@${domain}`,
    `${firstName.charAt(0)}.${lastName}@${domain}`,
    `${firstName}_${lastName}@${domain}`,
    `${firstName.charAt(0)}${lastName}@${domain}`,
  ];

  return patterns.map((email) => email.toLowerCase());
}

// Find names on website and generate patterns
async function guessEmailsFromWebsite(domain: string): Promise<string[]> {
  // First, scrape the website for names (from team pages, about pages, etc.)
  const names = await extractNamesFromWebsite(domain);

  const guessedEmails: string[] = [];
  for (const name of names) {
    const patterns = generateEmailPatterns(name.first, name.last, domain);
    guessedEmails.push(...patterns);
  }

  return guessedEmails;
  // Note: These guessed emails should be verified before use
}
```

#### 4. Social Media Profile Scraping

Extract emails from social media profiles (when publicly available).

**Sources:**

- LinkedIn company page employee profiles
- GitHub organization member profiles
- Twitter/X bios and profiles

**Note:** Most social media platforms restrict email access in their APIs, so this method has limited applicability.

### API Methods (Optional - Requires API Keys)

#### 1. Hunter.io API

Hunter.io provides domain search and email verification.

**Setup:**

1. Sign up at https://hunter.io
2. Get API key from dashboard
3. Add to environment: `HUNTER_API_KEY=...`

**Implementation:**

```typescript
// Hunter.io domain search
async function findEmailsWithHunter(domain: string): Promise<any[]> {
  const apiKey = process.env.HUNTER_API_KEY;
  if (!apiKey) {
    throw new Error('HUNTER_API_KEY not set');
  }

  const response = await fetch(
    `https://api.hunter.io/v2/domain-search?domain=${domain}&api_key=${apiKey}`
  );

  if (!response.ok) {
    throw new Error(`Hunter.io API error: ${response.statusText}`);
  }

  const data = await response.json();
  return data.data.emails || [];
}

// Email verification with Hunter.io
async function verifyEmailWithHunter(email: string): Promise<boolean> {
  const apiKey = process.env.HUNTER_API_KEY;
  if (!apiKey) {
    throw new Error('HUNTER_API_KEY not set');
  }

  const response = await fetch(
    `https://api.hunter.io/v2/email-verifier?email=${email}&api_key=${apiKey}`
  );

  if (!response.ok) {
    return false;
  }

  const data = await response.json();
  return data.data.result === 'deliverable';
}
```

#### 2. Apollo.io API

Apollo.io provides comprehensive contact discovery.

**Setup:**

1. Sign up at https://www.apollo.io
2. Get API key from settings
3. Add to environment: `APOLLO_API_KEY=...`

**Implementation:**

```typescript
// Apollo.io domain search
async function findEmailsWithApollo(domain: string): Promise<any[]> {
  const apiKey = process.env.APOLLO_API_KEY;
  if (!apiKey) {
    throw new Error('APOLLO_API_KEY not set');
  }

  const response = await fetch(
    'https://api.apollo.io/v1/mixed_people/search',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
      },
      body: JSON.stringify({
        api_key: apiKey,
        q_organization_domains: domain,
        page: 1,
        per_page: 25,
      }),
    }
  );

  if (!response.ok) {
    throw new Error(`Apollo.io API error: ${response.statusText}`);
  }

  const data = await response.json();
  return data.people || [];
}
```

#### 3. Snov.io API

Snov.io provides email finder and verification.

**Setup:**

1. Sign up at https://snov.io
2. Get client ID and client secret
3. Add to environment: `SNOV_CLIENT_ID=...`, `SNOV_CLIENT_SECRET=...`

**Implementation:**

```typescript
// Snov.io domain search
async function findEmailsWithSnov(domain: string): Promise<any[]> {
  const clientId = process.env.SNOV_CLIENT_ID;
  const clientSecret = process.env.SNOV_CLIENT_SECRET;

  if (!clientId || !clientSecret) {
    throw new Error('Snov.io credentials not set');
  }

  // First, get access token
  const tokenResponse = await fetch('https://api.snov.io/v1/oauth/access_token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      grant_type: 'client_credentials',
      client_id: clientId,
      client_secret: clientSecret,
    }),
  });

  const tokenData = await tokenResponse.json();
  const accessToken = tokenData.access_token;

  // Then search for emails
  const response = await fetch(
    `https://api.snov.io/v2/domain-emails-with-info?domain=${domain}&access_token=${accessToken}&type=all&limit=100`
  );

  if (!response.ok) {
    throw new Error(`Snov.io API error: ${response.statusText}`);
  }

  const data = await response.json();
  return data.result?.emails || [];
}
```

#### 4. Clearbit API

Clearbit provides company and contact enrichment.

**Setup:**

1. Sign up at https://clearbit.com
2. Get API key
3. Add to environment: `CLEARBIT_API_KEY=...`

**Implementation:**

```typescript
// Clearbit domain search (includes employee emails)
async function findEmailsWithClearbit(domain: string): Promise<any[]> {
  const apiKey = process.env.CLEARBIT_API_KEY;
  if (!apiKey) {
    throw new Error('CLEARBIT_API_KEY not set');
  }

  const response = await fetch(
    `https://person.clearbit.com/v2/combined/find?domain=${domain}`,
    {
      headers: {
        Authorization: `Bearer ${apiKey}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error(`Clearbit API error: ${response.statusText}`);
  }

  const data = await response.json();
  // Clearbit returns person data which includes email
  return data.person ? [data.person] : [];
}
```

## Complete Implementation Example

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

  // 1. Try free methods first
  try {
    // Web scraping
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

  // 2. Try API methods if keys are available
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
      console.error('Hunter.io API failed:', error);
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
      console.error('Apollo.io API failed:', error);
    }
  }

  // 3. Verify emails (if Hunter.io key available)
  if (process.env.HUNTER_API_KEY) {
    for (const result of results) {
      if (!result.verified) {
        try {
          result.verified = await verifyEmailWithHunter(result.email);
        } catch (error) {
          // Skip verification if it fails
        }
      }
    }
  }

  return results;
}
```

## Email Verification

### Basic Validation

```typescript
// Basic email format validation
function isValidEmailFormat(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}
```

### MX Record Check

```typescript
// Check if domain has valid MX records
import { promises as dns } from 'dns';

async function hasValidMXRecord(domain: string): Promise<boolean> {
  try {
    const mxRecords = await dns.resolveMx(domain);
    return mxRecords.length > 0;
  } catch (error) {
    return false;
  }
}

// Extract domain from email and check MX
async function verifyDomainHasEmail(email: string): Promise<boolean> {
  const domain = email.split('@')[1];
  return hasValidMXRecord(domain);
}
```

## Best Practices

### Rate Limiting

```typescript
// Simple rate limiter
class RateLimiter {
  private delay: number;
  private lastRequest: number = 0;

  constructor(delayMs: number) {
    this.delay = delayMs;
  }

  async wait(): Promise<void> {
    const now = Date.now();
    const timeSinceLastRequest = now - this.lastRequest;
    if (timeSinceLastRequest < this.delay) {
      await new Promise((resolve) =>
        setTimeout(resolve, this.delay - timeSinceLastRequest)
      );
    }
    this.lastRequest = Date.now();
  }
}

// Usage
const limiter = new RateLimiter(1000); // 1 second between requests
for (const url of urls) {
  await limiter.wait();
  await fetch(url);
}
```

### Error Handling

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
      const results = await method();
      allResults.push(...results);
    } catch (error) {
      console.error('Method failed:', error);
      // Continue with next method
    }
  }

  return allResults;
}
```

### Data Quality

- Deduplicate emails
- Normalize email addresses (lowercase, trim)
- Filter out common non-personal addresses (noreply@, donotreply@, etc.) if needed
- Verify emails when possible
- Include metadata (source, confidence, position) for context

## Legal & Ethical Considerations

### Compliance

- **GDPR/CCPA:** Ensure compliance with data protection regulations
- **CAN-SPAM:** If sending emails, comply with CAN-SPAM Act requirements
- **Terms of Service:** Respect website terms of service and robots.txt
- **Rate Limiting:** Don't overwhelm servers with requests

### Ethical Use

- Only use publicly available information
- Respect privacy settings and opt-out requests
- Use emails responsibly (don't spam)
- Provide value in communications
- Honor unsubscribe requests immediately

### Robots.txt Compliance

```typescript
// Check robots.txt before scraping
async function checkRobotsTxt(domain: string, path: string): Promise<boolean> {
  try {
    const robotsUrl = `https://${domain}/robots.txt`;
    const response = await fetch(robotsUrl);
    const robotsContent = await response.text();

    // Simple check - in production, use a proper robots.txt parser
    // Check if path is disallowed
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
  } catch (error) {
    // If robots.txt doesn't exist or can't be fetched, proceed with caution
    return true;
  }
}
```
