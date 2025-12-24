---
name: content-analytics-expert
description: This skill should be used when users need help analyzing Genfeed analytics data, creating reports, identifying trends, calculating ROI, or providing content optimization recommendations. It activates when users ask analytics questions, request reports, need performance analysis, ROI calculations, trend identification, or content optimization recommendations.
location: .claude/skills/content/analytics-expert/
---

# Content Analytics Expert

## Overview

This skill enables Claude to analyze Genfeed analytics data, generate comprehensive reports, identify performance trends, calculate ROI and revenue attribution, and provide actionable insights for content optimization.

## When to Use This Skill

This skill activates automatically when users:

- Ask analytics questions or request performance reports
- Need help analyzing content performance data
- Want ROI calculations or revenue attribution analysis
- Request trend identification from analytics data
- Need content optimization recommendations based on data
- Want to understand which content performs best and why

## Core Capabilities

### 1. Generate Analytics Reports

To generate comprehensive analytics reports from Genfeed data:

1. **Collect Analytics Data**

   - Access Genfeed Analytics app data
   - Aggregate performance metrics across platforms
   - Gather engagement data (views, likes, comments, shares)
   - Collect conversion and revenue data (if available)

2. **Create Report Structure**

   - Weekly/Monthly performance reports
   - Platform-specific performance analysis
   - Content type performance comparison
   - Audience engagement reports
   - ROI and revenue attribution reports

3. **Generate Report Content**
   - Summarize key metrics and insights
   - Create data visualizations (charts, graphs)
   - Identify top-performing content
   - Highlight trends and patterns
   - Provide actionable recommendations

**Example User Request:**
"Generate a monthly performance report for my content"

**Genfeed Integration:**

- Analytics App: Access performance data
- Manager App: Store and share reports
- Publisher App: Use insights for scheduling optimization

### 2. Identify Top-Performing Content Patterns

To identify patterns in top-performing content:

1. **Analyze Performance Data**

   - Review content performance metrics
   - Identify top-performing content pieces
   - Analyze common characteristics of successful content

2. **Extract Patterns**

   - Content topics and themes
   - Content formats and types
   - Posting times and frequencies
   - Platform-specific patterns
   - Engagement drivers (hooks, CTAs, visuals)

3. **Generate Insights**
   - Document successful content patterns
   - Recommend content strategies based on patterns
   - Suggest content replication opportunities

**Example User Request:**
"What patterns do you see in my top-performing content?"

**Genfeed Integration:**

- Analytics App: Analyze performance data
- Studio App: Apply patterns to new content generation
- Manager App: Store pattern insights

### 3. Predict Content Performance

To predict content performance before publishing:

1. **Analyze Historical Data**

   - Review similar content performance
   - Identify factors that correlate with success
   - Build performance prediction models

2. **Evaluate New Content**

   - Compare new content to historical patterns
   - Assess content against success factors
   - Calculate predicted performance scores

3. **Provide Recommendations**
   - Suggest content improvements
   - Recommend optimal posting times
   - Identify best platforms for content
   - Predict viral potential

**Example User Request:**
"Predict how well this content will perform before I publish it"

**Genfeed Integration:**

- Analytics App: Use historical data for predictions
- Studio App: Optimize content before generation
- Publisher App: Optimize scheduling based on predictions

### 4. ROI Analysis and Attribution

To calculate ROI and revenue attribution:

1. **Track Revenue Metrics**

   - Link content to conversions and revenue
   - Track attribution through genfeed.ai/u/[handle] links
   - Calculate cost per content piece (API costs, time)

2. **Calculate ROI**

   - Revenue per content piece
   - Cost to create content
   - ROI percentage calculation
   - Revenue per platform/channel

3. **Generate ROI Reports**
   - Content-level ROI analysis
   - Platform ROI comparison
   - Campaign ROI tracking
   - Revenue optimization recommendations

**Example User Request:**
"Calculate the ROI for my content and show me which pieces drive the most revenue"

**Genfeed Integration:**

- Analytics App: Track conversions and revenue
- Manager App: Store ROI data and reports
- Publisher App: Optimize distribution based on ROI

### 5. Trend Identification

To identify trends from analytics data:

1. **Analyze Time-Series Data**

   - Review performance trends over time
   - Identify growth or decline patterns
   - Detect seasonal trends

2. **Identify Emerging Trends**

   - Content topics gaining traction
   - Platform trends and shifts
   - Audience behavior changes
   - Engagement pattern shifts

3. **Provide Trend Insights**
   - Document identified trends
   - Recommend actions based on trends
   - Predict future trend directions

**Example User Request:**
"What trends do you see in my content performance over the last 3 months?"

**Genfeed Integration:**

- Analytics App: Analyze time-series data
- Manager App: Store trend insights
- Studio App: Apply trends to content generation

## Genfeed Analytics Context

**Available Analytics Data:**

- Post-level metrics: Views, Likes, Comments, Shares, Engagement Rate
- Platform-specific metrics: Performance by platform (X, LinkedIn, Instagram, TikTok, YouTube)
- Time-based metrics: Performance over time (7d, 30d, 90d)
- Conversion metrics: Clicks, signups, revenue (via genfeed.ai/u/[handle] links)
- Content type metrics: Performance by content type (video, image, article)

**Analytics App Features:**

- Post Analytics Dashboard (`/analytics/posts`)
- Real-time performance tracking
- Filters: Platform, Timeframe, Sort by metric
- Hourly analytics refresh (automated cron job)

**Key Metrics:**

- Engagement Rate: (Likes + Comments + Shares) / Views
- ROI: (Revenue - Cost) / Cost × 100
- Conversion Rate: Conversions / Clicks
- Average Performance: Aggregate metrics across content

## Best Practices

1. **Data-Driven Insights**: Base all recommendations on actual analytics data
2. **Context Matters**: Consider platform, timing, and audience when analyzing data
3. **Actionable Recommendations**: Provide specific, actionable insights, not just data
4. **Comparative Analysis**: Compare performance against benchmarks and historical data
5. **Continuous Monitoring**: Recommend regular analytics review and optimization

## Resources

### references/

- `analytics-api-reference.md`: Genfeed Analytics API endpoints and data structures
- `roi-calculation-guide.md`: ROI calculation methods and formulas
- `performance-benchmarks.md`: Industry benchmarks for content performance

### assets/

- `analytics-report-template.md`: Template for analytics reports
- `roi-report-template.md`: Template for ROI analysis reports
- `trend-analysis-template.md`: Template for trend identification reports
