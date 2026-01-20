# Leads Researcher - Full Guide

## Research Workflows

### 1. Company Information Research

Research basic company information including industry, size, location, and technology stack.

**Key Information to Gather:**

- Company name and legal name
- Industry and vertical
- Company size (employee count)
- Annual revenue (if available)
- Headquarters location
- Website and social media profiles
- Technology stack and tools used
- Recent news or funding

**Research Methodology:**

1. **Start with Company Website:**
   - Review "About Us" page
   - Check careers page for company size indicators
   - Look for technology stack on job postings
   - Note headquarters location

2. **Use Company Data APIs:**
   - Clearbit Enrichment API
   - ZoomInfo API
   - Apollo.io API
   - LinkedIn Sales Navigator
   - Crunchbase API

3. **Cross-reference Multiple Sources:**
   - Verify information across sources
   - Check for inconsistencies
   - Update outdated information
   - Flag data quality issues

**Example Implementation:**

```typescript
// Research company information
async function researchCompany(companyName: string, domain?: string) {
  const results = {
    name: companyName,
    domain: domain || "",
    industry: "",
    size: "",
    location: "",
    revenue: "",
    techStack: [],
    linkedIn: "",
    crunchbase: "",
  };

  // Use Clearbit Enrichment API
  if (domain) {
    const clearbitResponse = await fetch(
      `https://company.clearbit.com/v2/companies/find?domain=${domain}`,
      {
        headers: {
          Authorization: `Bearer ${process.env.CLEARBIT_API_KEY}`,
        },
      }
    );

    if (clearbitResponse.ok) {
      const data = await clearbitResponse.json();
      results.industry = data.category?.industry || "";
      results.size = `${data.metrics?.employees || "Unknown"} employees`;
      results.location = data.geo?.city || "";
      results.linkedIn = data.linkedin?.handle || "";
    }
  }

  return results;
}
```

### 2. Contact Information Discovery

Find email addresses, phone numbers, and social media profiles for decision makers and key contacts.

**Key Contacts to Find:**

- CEO/Founder
- CTO/Technical decision makers
- Head of Sales/Marketing
- Department heads relevant to your product
- Procurement/Finance contacts

**Research Methodology:**

1. **Start with LinkedIn:**
   - Search for company employees
   - Filter by job title and department
   - Note profile information
   - Check for email in profile

2. **Use Contact Discovery Tools:**
   - Apollo.io - Contact database and email finder
   - Hunter.io - Email finder and verifier
   - RocketReach - Contact discovery
   - Lusha - Contact data enrichment
   - ZoomInfo - B2B contact database

3. **Verify Contact Information:**
   - Verify email addresses before use
   - Check phone number validity
   - Verify social media profiles
   - Cross-reference multiple sources

**Example Implementation:**

```typescript
// Find contacts at a company
async function findContacts(companyDomain: string, jobTitle?: string) {
  const contacts = [];

  // Use Hunter.io to find emails
  const hunterResponse = await fetch(
    `https://api.hunter.io/v2/domain-search?domain=${companyDomain}&api_key=${process.env.HUNTER_API_KEY}`
  );

  if (hunterResponse.ok) {
    const data = await hunterResponse.json();
    contacts.push(
      ...data.data.emails.map((email: any) => ({
        firstName: email.first_name,
        lastName: email.last_name,
        email: email.value,
        position: email.position,
        linkedIn: email.linkedin,
        confidence: email.confidence,
      }))
    );
  }

  // Filter by job title if provided
  if (jobTitle) {
    return contacts.filter((contact) =>
      contact.position?.toLowerCase().includes(jobTitle.toLowerCase())
    );
  }

  return contacts;
}

// Verify email address
async function verifyEmail(email: string): Promise<boolean> {
  const response = await fetch(
    `https://api.hunter.io/v2/email-verifier?email=${email}&api_key=${process.env.HUNTER_API_KEY}`
  );

  if (response.ok) {
    const data = await response.json();
    return data.data.result === "deliverable";
  }

  return false;
}
```

### 3. Buyer Intent Signals

Identify signals that indicate a company is actively looking to purchase solutions.

**Buyer Intent Signals:**

1. **Job Postings:**
   - Hiring for roles related to your solution
   - Job descriptions mentioning tools you replace
   - New departments or teams being formed
   - Technology-focused hiring

2. **Technology Usage:**
   - Tools listed on company website
   - Technology mentioned in job postings
   - Stack Overflow/GitHub activity
   - App usage data (if available)

3. **Company News:**
   - Funding rounds (indicates growth/budget)
   - Acquisitions or mergers
   - New product launches
   - Leadership changes
   - Expansion announcements

4. **Online Behavior:**
   - Website visits to competitor pages
   - Content downloads (if tracked)
   - Webinar attendance
   - Social media engagement

**Research Methodology:**

```typescript
// Identify buyer intent signals
async function identifyBuyerIntent(companyName: string, domain: string) {
  const signals = {
    jobPostings: [],
    technologyStack: [],
    recentNews: [],
    funding: null,
    expansion: false,
    score: 0, // Intent score 0-100
  };

  // Check job postings
  const jobs = await searchJobPostings(companyName);
  signals.jobPostings = jobs.filter((job) =>
    job.description.includes("your-solution-keywords")
  );

  if (signals.jobPostings.length > 0) {
    signals.score += 30;
  }

  // Check technology stack
  const techStack = await researchTechStack(domain);
  signals.technologyStack = techStack;

  // Check if they use competitor tools
  const competitorTools = ["competitor-tool-1", "competitor-tool-2"];
  const usesCompetitor = techStack.some((tech) =>
    competitorTools.includes(tech)
  );

  if (usesCompetitor) {
    signals.score += 25;
  }

  // Check recent news and funding
  const news = await searchCompanyNews(companyName);
  signals.recentNews = news;

  const hasFunding = news.some(
    (item) =>
      item.title.toLowerCase().includes("funding") ||
      item.title.toLowerCase().includes("raised")
  );

  if (hasFunding) {
    signals.score += 20;
    signals.funding = news.find((item) =>
      item.title.toLowerCase().includes("funding")
    );
  }

  // Check for expansion signals
  const hasExpansion = news.some(
    (item) =>
      item.title.toLowerCase().includes("expansion") ||
      item.title.toLowerCase().includes("opening") ||
      item.title.toLowerCase().includes("hiring")
  );

  if (hasExpansion) {
    signals.expansion = true;
    signals.score += 25;
  }

  return signals;
}
```

## Data Sources and APIs

### Company Data APIs

**Clearbit Enrichment:**

- Company and domain enrichment
- Employee count, revenue, industry
- Technology stack
- Social media profiles

**ZoomInfo:**

- Comprehensive B2B database
- Company information
- Contact data
- Intent signals

**Apollo.io:**

- Company and contact database
- Email finder
- Intent data
- Technology tracking

**Crunchbase:**

- Company funding information
- Investor data
- Acquisition data
- Company profiles

**LinkedIn Sales Navigator:**

- Professional contacts
- Company information
- Employee data
- Sales insights

### Contact Discovery APIs

**Hunter.io:**

- Email finder and verifier
- Domain search
- Email verification

**RocketReach:**

- Contact discovery
- Email and phone finder
- Social profile links

**Lusha:**

- Contact data enrichment
- Email and phone numbers
- Company information

### Intent Signal Sources

**Job Postings:**

- LinkedIn Jobs API
- Indeed API
- Glassdoor API
- Company careers pages

**Technology Stack:**

- BuiltWith API
- Wappalyzer
- StackShare
- GitHub

**News and Funding:**

- News API
- Crunchbase API
- Google News
- Company blogs

## Best Practices

### Data Privacy and Compliance

- Comply with GDPR, CCPA, and other privacy regulations
- Obtain consent before contacting leads
- Respect opt-out requests
- Handle personal data securely
- Implement data retention policies

### Data Quality

- Verify information from multiple sources
- Cross-reference data for accuracy
- Flag outdated or unverified data
- Implement data validation rules
- Regularly update lead information

### Research Efficiency

- Use APIs to automate data gathering
- Cache frequently accessed data
- Batch requests when possible
- Implement rate limiting
- Use webhooks for real-time updates

### Source Verification

- Always verify contact information
- Check email deliverability
- Validate phone numbers
- Verify company information
- Cross-reference multiple sources

### Buyer Intent Scoring

- Develop consistent scoring methodology
- Weight different signals appropriately
- Update scoring based on results
- Track which signals correlate with conversions
- Refine intent detection over time

## Example User Requests

**Example 1: "Research company information for Acme Corp"**

- Gather basic company data (industry, size, location)
- Find company website and social profiles
- Research technology stack
- Check for recent news or funding
- Compile comprehensive company profile

**Example 2: "Find email addresses for decision makers at tech companies"**

- Identify target companies
- Find contacts with relevant job titles
- Discover email addresses using APIs
- Verify email addresses
- Compile contact list with metadata

**Example 3: "Identify companies with buyer intent for our solution"**

- Search for job postings indicating need
- Check technology stack for competitors
- Look for funding or growth signals
- Calculate intent scores
- Generate prioritized lead list

**Example 4: "Enrich existing lead data with additional information"**

- Match leads to company records
- Fill in missing company data
- Find additional contacts
- Add intent signals
- Update lead records with enriched data
