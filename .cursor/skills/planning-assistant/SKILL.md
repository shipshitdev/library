---
name: content-planning-assistant
description: This skill should be used when users need help with content planning, calendar management, research organization, content ideation, or multi-platform planning. It activates when users ask about content planning, calendar management, research organization, content ideation, or multi-platform planning.
location: .claude/skills/content/planning-assistant/
---

# Content Planning Assistant

## Overview

This skill enables Claude to assist users with comprehensive content planning including weekly/monthly planning, research organization and synthesis, content calendar creation, inspiration-to-plan conversion, and multi-platform content planning.

## When to Use This Skill

This skill activates automatically when users:

- Ask about content planning or calendar management
- Need help organizing research or bookmarks
- Request content ideation or brainstorming
- Want multi-platform content planning
- Need weekly or monthly content prep
- Ask about prioritizing content or planning ahead

## Core Capabilities

### 1. Weekly/Monthly Content Planning

To help users plan content for weeks or months:

1. **Analyze Historical Performance**

   - Review past content performance
   - Identify best-performing content types and topics
   - Determine optimal posting frequencies

2. **Create Content Plan**

   - Generate weekly/monthly content calendars
   - Plan content themes and topics
   - Balance content types (educational, entertaining, promotional)
   - Align content with business goals and events

3. **Optimize Planning**
   - Recommend content mix based on performance
   - Suggest optimal posting times per platform
   - Plan content series and campaigns
   - Ensure consistent posting schedule

**Example User Request:**
"Help me plan my content for next week"

**Integration:**

- Publishing Platform: Schedule content in calendar
- Analytics Platform: Use performance data for planning
- Content Management Platform: Organize content ideas and themes

### 2. Research Organization and Synthesis

To help users organize and synthesize research:

1. **Organize Research**

   - Categorize bookmarked research from browser extension
   - Group research by topic, theme, or content type
   - Create research collections and folders

2. **Synthesize Findings**

   - Extract key insights from research
   - Identify common themes and patterns
   - Summarize research findings
   - Create research summaries and outlines

3. **Convert to Content Plans**
   - Turn research into content ideas
   - Create content outlines from research
   - Generate content plans from research findings

**Example User Request:**
"Organize my bookmarked research and turn it into a content plan"

**Integration:**

- Browser Extension: Import bookmarked research
- Content Management Platform: Organize research collections
- Content Creation Tools: Generate content from research

### 3. Content Calendar Creation

To create comprehensive content calendars:

1. **Design Calendar Structure**

   - Choose calendar view (daily, weekly, monthly)
   - Define calendar categories and themes
   - Plan content mix and balance

2. **Populate Calendar**

   - Schedule content across platforms
   - Plan content themes and topics
   - Assign content types and formats
   - Set posting times and frequencies

3. **Optimize Calendar**
   - Ensure consistent posting schedule
   - Balance content types and themes
   - Optimize posting times per platform
   - Plan content series and campaigns

**Example User Request:**
"Create a content calendar for next month"

**Integration:**

- Publishing Platform: Visual calendar interface
- Content Management Platform: Content idea organization
- Analytics Platform: Performance-based scheduling

### 4. Inspiration-to-Plan Conversion

To convert inspiration into actionable content plans:

1. **Collect Inspiration**

   - Gather inspiring content from browser extension
   - Organize inspiration by theme or topic
   - Analyze what makes content inspiring

2. **Generate Content Ideas**

   - Convert inspiration into content ideas
   - Create variations and adaptations
   - Generate original content concepts from inspiration

3. **Create Actionable Plans**
   - Turn ideas into content plans
   - Schedule content in calendar
   - Prioritize content ideas

**Example User Request:**
"Turn my bookmarked inspiration into a content plan"

**Integration:**

- Browser Extension: Import inspiring content
- Content Management Platform: Organize inspiration and ideas
- Content Creation Tools: Generate content from inspiration
- Publishing Platform: Schedule content from plans

### 5. Multi-Platform Content Planning

To plan content across multiple platforms:

1. **Understand Platform Requirements**

   - Review platform-specific requirements (formats, lengths, best practices)
   - Identify platform-specific content types
   - Understand platform audience differences

2. **Create Platform-Specific Plans**

   - Plan content for each platform (X, LinkedIn, Instagram, TikTok, YouTube)
   - Adapt content for platform requirements
   - Optimize content for platform audiences

3. **Coordinate Multi-Platform Strategy**
   - Plan content distribution across platforms
   - Coordinate posting schedules
   - Ensure consistent messaging across platforms
   - Optimize content mix per platform

**Example User Request:**
"Help me plan content for X, LinkedIn, and Instagram for next week"

**Integration:**

- Publishing Platform: Multi-platform scheduling
- Content Creation Tools: Platform-specific content generation
- Analytics Platform: Platform performance comparison

## Project Context Discovery

**Before creating content plans, discover the project's context:**

1. **Scan Project Documentation:**
   - Check `.agent/SYSTEM/ARCHITECTURE.md` for planning tools
   - Review `.agent/SOP/` for content planning processes
   - Look for existing content calendar templates
   - Check for planning workflow documentation

2. **Identify Planning Tools:**
   - Scan codebase for calendar/scheduling features
   - Look for content idea management systems
   - Check for research/bookmarking integrations
   - Review analytics platform for planning data

3. **Discover Planning Patterns:**
   - Review existing content calendars if available
   - Check for content planning templates
   - Look for research organization patterns
   - Identify platform-specific planning requirements

4. **Use Project-Specific Skills:**
   - Check for `[project]-planning-assistant` skill
   - Look for project-specific planning templates
   - Review project's content planning best practices

5. **Match Project Style:**
   - Use project's planning terminology
   - Follow project's calendar format
   - Align with project's content organization approach

**Platform-Specific Planning:**

- X/Twitter: Short-form, real-time, trending topics
- LinkedIn: Professional, long-form, thought leadership
- Instagram: Visual, Stories, Reels, aesthetic focus
- TikTok: Short-form video, trending sounds, viral hooks
- YouTube: Long-form video, SEO, educational content

## Best Practices

1. **Discover Project Context First**: Scan project documentation to understand planning tools and processes
2. **Use Project-Specific Skills**: If project has `[project]-planning-assistant` skill, collaborate with it
3. **Match Project Patterns**: Follow project's planning templates and terminology
4. **Data-Driven Planning**: Base plans on historical performance data from the project
5. **Platform Optimization**: Adapt content for each platform's requirements
6. **Consistency**: Maintain consistent posting schedule and discovered brand voice
7. **Flexibility**: Allow room for trending topics and timely content
8. **Balance**: Mix content types (educational, entertaining, promotional)

## Resources

### references/

- `content-planning-guide.md`: Comprehensive content planning guide
- `platform-best-practices.md`: Platform-specific content best practices
- `content-calendar-templates.md`: Content calendar templates and examples

### assets/

- `weekly-planning-template.md`: Template for weekly content planning
- `monthly-planning-template.md`: Template for monthly content planning
- `research-organization-template.md`: Template for organizing research
- `content-idea-template.md`: Template for content ideation
