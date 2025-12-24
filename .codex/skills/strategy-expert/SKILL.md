---
name: content-strategy-expert
description: This skill should be used when users need help with content strategy, persona building, competitive analysis, content planning, or brand voice consistency for Genfeed. It activates when users ask about content strategy, building personas or target audiences, competitive analysis requests, content planning and ideation, or brand voice questions.
location: .claude/skills/content/strategy-expert/
---

# Content Strategy Expert

## Overview

This skill enables Claude to assist Genfeed users with comprehensive content strategy tasks including building customer personas from analytics data, conducting competitive content analysis, planning content calendars, managing research-to-content workflows, and ensuring brand voice consistency across all content.

## When to Use This Skill

This skill activates automatically when users:

- Ask about content strategy or strategic planning
- Request help building personas or defining target audiences
- Need competitive analysis or competitor research
- Want content planning assistance or ideation
- Ask about brand voice, brand guidelines, or content consistency
- Need help organizing research into actionable content plans

## Core Capabilities

### 1. Build Customer Personas from Analytics Data

To build customer personas from Genfeed analytics:

1. **Analyze Engagement Data**

   - Review analytics data from Genfeed Analytics app
   - Identify patterns in audience engagement
   - Segment audiences by content preferences, platform behavior, and engagement patterns
   - Extract demographics, goals, and pain points from content performance data

2. **Synthesize Persona Profiles**

   - Create persona cards with:
     - Demographics (age, location, interests)
     - Goals and motivations
     - Pain points and challenges
     - Content preferences (topics, formats, platforms)
     - Engagement patterns (best times, preferred content types)
   - Use analytics data to validate persona assumptions

3. **Generate Persona Documentation**
   - Create structured persona profiles in Genfeed Manager app
   - Link personas to content performance data
   - Enable persona-based content targeting in Studio

**Example User Request:**
"Build a persona for my top-performing content audience based on my analytics data"

**Genfeed Integration:**

- Analytics App: Extract engagement data
- Manager App: Store and manage personas
- Studio App: Use personas for content targeting

### 2. Competitive Content Analysis

To conduct competitive content analysis:

1. **Identify Competitors**

   - Help users identify relevant competitors in their niche
   - Set up competitor tracking via browser extension
   - Monitor competitor accounts and content

2. **Analyze Competitor Content**

   - Review competitor content performance
   - Identify trending topics and formats
   - Analyze engagement patterns and best practices
   - Compare competitor content to user's content

3. **Generate Competitive Intelligence**
   - Create competitive analysis reports
   - Identify content gaps and opportunities
   - Recommend content strategies based on competitor insights
   - Benchmark user's content performance against competitors

**Example User Request:**
"Analyze my competitors' content and tell me what topics they're covering that I'm not"

**Genfeed Integration:**

- Browser Extension: Track competitor accounts
- Analytics App: Compare performance metrics
- Manager App: Store competitive intelligence

### 3. Content Calendar Planning

To help users plan content calendars:

1. **Analyze Historical Performance**

   - Review past content performance data
   - Identify best-performing content types and topics
   - Determine optimal posting times and frequencies

2. **Create Content Calendar**

   - Generate weekly/monthly content calendars
   - Plan content themes and topics
   - Schedule content across multiple platforms
   - Balance content types (educational, entertaining, promotional)

3. **Optimize Calendar Strategy**
   - Recommend content mix based on performance data
   - Suggest optimal posting times per platform
   - Plan content series and campaigns
   - Align calendar with business goals and events

**Example User Request:**
"Create a content calendar for next month based on my top-performing content"

**Genfeed Integration:**

- Publisher App: Schedule content in calendar
- Analytics App: Use performance data for planning
- Manager App: Organize content ideas and themes

### 4. Research-to-Content Workflow

To convert research into actionable content:

1. **Organize Research**

   - Help users organize bookmarked research from browser extension
   - Categorize research by topic, theme, or content type
   - Identify key insights and findings from research

2. **Generate Content Outlines**

   - Convert research findings into content outlines
   - Create structured content plans from research
   - Identify content opportunities from research data

3. **Create Content from Research**
   - Generate video/article scripts from research outlines
   - Convert research into presentation-style content
   - Ensure research is properly cited and attributed

**Example User Request:**
"Turn my bookmarked research into a content plan for next week"

**Genfeed Integration:**

- Browser Extension: Import bookmarked research
- Studio App: Generate content from research outlines
- Manager App: Organize research and content plans

### 5. Brand Voice Consistency

To ensure brand voice consistency across content:

1. **Understand Brand Guidelines**

   - Review user's brand guidelines (if available)
   - Identify brand voice characteristics
   - Understand brand values and messaging

2. **Enforce Brand Voice**

   - Ensure all generated content matches brand voice
   - Review content for brand consistency
   - Suggest improvements to align with brand guidelines

3. **Maintain Brand Standards**
   - Check content for brand compliance
   - Ensure consistent messaging across platforms
   - Recommend brand voice improvements

**Example User Request:**
"Review my content to ensure it matches my brand voice"

**Genfeed Integration:**

- Studio App: Apply brand voice in content generation
- Manager App: Store and manage brand guidelines
- Publisher App: Ensure brand consistency in distribution

## Genfeed Platform Context

**Current Genfeed Architecture:**

- Browser Extension: Trend discovery and bookmarking
- Studio App: AI content generation
- Publisher App: Multi-platform distribution
- Analytics App: Performance tracking
- Manager App: Content library and organization

**Content Intelligence Workflow:**

```
Trend Detection → Content Generation → Distribution → Analytics → Optimization
```

**Key Genfeed Features:**

- Multi-platform publishing (X, LinkedIn, Instagram, TikTok, YouTube)
- AI-powered content generation (videos, images, voices, music, articles)
- Performance analytics and ROI tracking
- Brand voice training and consistency
- Content library and organization

## Best Practices

1. **Data-Driven Decisions**: Always base recommendations on actual analytics data from Genfeed
2. **Platform-Specific Strategy**: Consider platform-specific requirements and best practices
3. **Brand Consistency**: Ensure all content recommendations align with brand guidelines
4. **Competitive Intelligence**: Use competitor analysis to identify opportunities, not to copy
5. **Continuous Optimization**: Recommend iterative improvements based on performance data

## Resources

### references/

- `genfeed-architecture.md`: Genfeed platform architecture and features
- `content-strategy-guide.md`: Content strategy best practices and frameworks

### assets/

- `persona-template.md`: Template for creating customer personas
- `content-calendar-template.md`: Template for content calendar planning
- `competitive-analysis-template.md`: Template for competitive analysis reports
