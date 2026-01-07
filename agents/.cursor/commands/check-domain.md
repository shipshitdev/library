# Check Domain: Domain Name Generator & Availability Checker

Generate domain name suggestions and check availability using Namecheap API.

## Purpose

This command helps users:
- Generate creative domain name suggestions based on keywords
- Check domain availability using Namecheap API
- Get domain suggestions with availability status
- Validate domain name formats

## When to Use

Use this command when:
- User needs domain name ideas for a new project/startup
- User wants to check if specific domains are available
- User needs to find available domains based on keywords
- User wants to validate domain name formats

## Usage

### Basic Usage

```bash
/check-domain
```

The AI will:
1. Ask for keywords or domain ideas
2. Generate domain name suggestions
3. Check availability using Namecheap API
4. Present results with availability status

### With Specific Domain

```bash
/check-domain example.com
```

Checks availability for a specific domain.

### With Keywords

```bash
/check-domain --keywords "productivity app remote teams"
```

Generates domain suggestions based on keywords and checks availability.

## Instructions for AI

When user invokes `/check-domain`:

### Step 1: Gather Requirements

Ask the user:
- What keywords or concepts should the domain represent?
- Any specific domain names to check?
- Preferred TLDs (.com, .io, .ai, etc.)?
- Any constraints (length, style, etc.)?

### Step 2: Generate Domain Suggestions

Use the `brand-name-generator` skill to generate domain name ideas:
- Generate 10-20 domain suggestions
- Use multiple naming strategies (portmanteau, invented, compound, etc.)
- Consider user's keywords and preferences

### Step 3: Validate Domain Formats

Use the `search-domain-validator` skill to:
- Validate all generated domains meet RFC 1035/1123 standards
- Filter out invalid domain formats before checking availability

### Step 4: Check Availability with Namecheap

For each valid domain, check availability using Namecheap API:

**Required Environment Variables:**
- `NAMECHEAP_API_USER` - Namecheap API username
- `NAMECHEAP_API_KEY` - Namecheap API key
- `NAMECHEAP_CLIENT_IP` - Your public IP address (required by Namecheap)

**API Implementation:**

```typescript
async function checkNamecheapAvailability(domain: string): Promise<{
  available: boolean;
  error?: string;
}> {
  const apiUser = process.env.NAMECHEAP_API_USER;
  const apiKey = process.env.NAMECHEAP_API_KEY;
  const clientIp = process.env.NAMECHEAP_CLIENT_IP;

  if (!apiUser || !apiKey || !clientIp) {
    throw new Error('Namecheap API credentials not configured. Set NAMECHEAP_API_USER, NAMECHEAP_API_KEY, and NAMECHEAP_CLIENT_IP environment variables.');
  }

  const url = `https://api.namecheap.com/xml.response?ApiUser=${apiUser}&ApiKey=${apiKey}&UserName=${apiUser}&Command=namecheap.domains.check&ClientIp=${clientIp}&DomainList=${domain}`;

  try {
    const response = await fetch(url);
    const xml = await response.text();

    // Parse XML response
    // Available domains: <DomainCheckResult Domain="example.com" Available="true"/>
    // Unavailable: <DomainCheckResult Domain="example.com" Available="false"/>
    const availableMatch = xml.match(/Available="(true|false)"/);
    const available = availableMatch?.[1] === 'true';

    // Check for errors
    const errorMatch = xml.match(/<Error>(.*?)<\/Error>/);
    if (errorMatch) {
      return { available: false, error: errorMatch[1] };
    }

    return { available: available ?? false };
  } catch (error) {
    return { available: false, error: error.message };
  }
}
```

**Python Implementation:**

```python
import os
import requests
import xml.etree.ElementTree as ET

def check_namecheap_availability(domain: str) -> dict:
    """Check domain availability using Namecheap API."""
    api_user = os.getenv('NAMECHEAP_API_USER')
    api_key = os.getenv('NAMECHEAP_API_KEY')
    client_ip = os.getenv('NAMECHEAP_CLIENT_IP')

    if not all([api_user, api_key, client_ip]):
        raise ValueError(
            'Namecheap API credentials not configured. '
            'Set NAMECHEAP_API_USER, NAMECHEAP_API_KEY, and NAMECHEAP_CLIENT_IP environment variables.'
        )

    url = (
        f'https://api.namecheap.com/xml.response?'
        f'ApiUser={api_user}&'
        f'ApiKey={api_key}&'
        f'UserName={api_user}&'
        f'Command=namecheap.domains.check&'
        f'ClientIp={client_ip}&'
        f'DomainList={domain}'
    )

    try:
        response = requests.get(url)
        root = ET.fromstring(response.text)

        # Find DomainCheckResult
        domain_result = root.find('.//DomainCheckResult')
        if domain_result is not None:
            available = domain_result.get('Available') == 'true'
            return {'available': available}

        # Check for errors
        error = root.find('.//Error')
        if error is not None:
            return {'available': False, 'error': error.text}

        return {'available': False, 'error': 'Unknown response format'}
    except Exception as e:
        return {'available': False, 'error': str(e)}
```

### Step 5: Present Results

Display results in a clear format:

```
Domain Availability Results
==========================

✅ Available:
- example.com
- tryexample.io
- exampleapp.ai

❌ Unavailable:
- example.net (taken)
- example.org (taken)

⚠️  Errors:
- example.co (API error: Rate limit exceeded)
```

### Step 6: Provide Next Steps

Suggest:
- Which available domains to consider
- How to register domains (link to Namecheap)
- Alternative TLDs if .com is unavailable
- Additional suggestions if needed

## Environment Setup

Before using this command, ensure Namecheap API credentials are set:

```bash
export NAMECHEAP_API_USER="your_username"
export NAMECHEAP_API_KEY="your_api_key"
export NAMECHEAP_CLIENT_IP="your_public_ip"
```

Or add to `.env` file:
```
NAMECHEAP_API_USER=your_username
NAMECHEAP_API_KEY=your_api_key
NAMECHEAP_CLIENT_IP=your_public_ip
```

**Getting Namecheap API Credentials:**
1. Log in to Namecheap account
2. Go to Profile → Tools → API Access
3. Enable API access
4. Get API key and whitelist your IP address
5. Use your Namecheap username as API user

## Error Handling

Handle common errors:
- **Missing credentials**: Prompt user to set environment variables
- **Invalid IP**: Namecheap requires whitelisted IP - check NAMECHEAP_CLIENT_IP
- **Rate limiting**: Implement delays between requests (100-200ms)
- **Invalid domain format**: Filter out before API call
- **API errors**: Display error message to user

## Best Practices

- **Rate Limiting**: Add 100-200ms delay between API calls
- **Batch Checking**: Check multiple domains efficiently
- **Caching**: Consider caching results for repeated checks
- **Validation First**: Always validate format before API call
- **User Feedback**: Show progress for multiple domain checks

## Integration with Skills

This command leverages:
- `brand-name-generator` - For generating domain name ideas
- `search-domain-validator` - For validating domain formats

## Example Workflow

**User:** `/check-domain --keywords "AI writing assistant"`

**AI Response:**
1. Generates 15 domain suggestions using brand-name-generator
2. Validates all domains using search-domain-validator
3. Checks availability for each using Namecheap API
4. Presents results with availability status
5. Recommends top 3 available domains

