---
name: workflow-automation
description: This skill should be used when users need help designing content workflows, creating process documentation, implementing automation rules, designing approval processes, or optimizing content pipelines. It activates when users ask about workflow design, process documentation, automation, approval workflows, or content pipeline optimization.
---

# Content Workflow Automation

## Overview

This skill enables Claude to help users design and implement content workflows, create process documentation, suggest automation rules, document approval processes, and optimize content pipelines for efficiency and quality.

## When to Use This Skill

This skill activates automatically when users:

- Ask about workflow design or content processes
- Need help documenting content workflows
- Request automation suggestions or implementation
- Want to design approval workflows
- Need content pipeline optimization
- Ask about process improvement or efficiency

## Core Capabilities

### 1. Design Content Workflows

To design effective content workflows:

1. **Understand Current Process**

   - Map existing content creation process
   - Identify workflow steps and stakeholders
   - Document current pain points and bottlenecks

2. **Design Optimal Workflow**

   - Create workflow structure: Input → Processing → Output
   - Define workflow steps and decision points
   - Identify automation opportunities
   - Design workflow for efficiency and quality

3. **Document Workflow**
   - Create visual workflow diagrams
   - Document step-by-step procedures
   - Define roles and responsibilities
   - Specify tools and integrations needed

**Example User Request:**
"Design a content workflow for my team that includes approval steps"

**Integration:**

- Content Management Platform: Store workflow documentation
- Publishing Platform: Implement workflow automation
- Content Creation Tools: Integrate workflow steps into content generation

### 2. Create Process Documentation

To create comprehensive process documentation:

1. **Document Content Processes**

   - Content creation process
   - Content approval process
   - Content publishing process
   - Content optimization process

2. **Create Visual Flowcharts**

   - Convert written procedures into flowcharts
   - Visualize complex processes
   - Make processes easier to follow and share

3. **Maintain Documentation**
   - Keep documentation up-to-date
   - Version control for process changes
   - Share documentation with team

**Example User Request:**
"Create a flowchart for my content creation process"

**Integration:**

- Content Management Platform: Store process documentation
- Team collaboration features: Share workflows with team

### 3. Automation Rule Suggestions

To suggest and implement automation rules:

1. **Identify Automation Opportunities**

   - Review workflow for repetitive tasks
   - Identify manual steps that can be automated
   - Assess automation feasibility and impact

2. **Design Automation Rules**

   - Define trigger conditions
   - Specify automation actions
   - Design error handling and fallbacks

3. **Implement Automation**
   - Configure automation rules in content platform
   - Test automation workflows
   - Monitor automation performance

**Example User Request:**
"What parts of my content workflow can be automated?"

**Integration:**

- Publishing Platform: Automated scheduling and distribution
- Content Management Platform: Automated content organization
- Analytics Platform: Automated report generation

### 4. Approval Process Design

To design content approval workflows:

1. **Define Approval Requirements**

   - Identify approval stakeholders
   - Define approval criteria
   - Specify approval workflow steps

2. **Design Approval Workflow**

   - Create approval process structure
   - Define roles and permissions
   - Design approval notifications and reminders

3. **Implement Approval System**
   - Configure approval workflow in content platform
   - Set up notifications and alerts
   - Track approval status and history

**Example User Request:**
"Design an approval workflow where content needs manager approval before publishing"

**Integration:**

- Content Management Platform: Approval workflow management
- Mobile App: Approval notifications and actions
- Publishing Platform: Approval-gated publishing

### 5. Content Pipeline Optimization

To optimize content pipelines for efficiency:

1. **Analyze Current Pipeline**

   - Map content pipeline from ideation to publishing
   - Identify bottlenecks and inefficiencies
   - Measure pipeline performance metrics

2. **Optimize Pipeline**

   - Remove unnecessary steps
   - Parallelize independent tasks
   - Automate repetitive processes
   - Optimize resource allocation

3. **Monitor and Improve**
   - Track pipeline performance
   - Identify optimization opportunities
   - Continuously improve workflow efficiency

**Example User Request:**
"Help me optimize my content pipeline to reduce time from ideation to publishing"

**Integration:**

- All Platforms: Optimize workflows across platform
- Analytics Platform: Track pipeline performance metrics
- Content Management Platform: Monitor workflow efficiency

## Project Context Discovery

**Before designing workflows, discover the project's context:**

1. **Scan Project Documentation:**
   - Check `.agent/SYSTEM/ARCHITECTURE.md` for workflow architecture
   - Review `.agent/SOP/` for existing process documentation
   - Look for workflow diagrams or process maps
   - Check for automation documentation

2. **Identify Workflow Components:**
   - Scan codebase for content creation tools
   - Look for publishing/distribution systems
   - Check for analytics integrations
   - Review approval/notification systems
   - Identify browser extensions or bookmarking features

3. **Discover Existing Processes:**
   - Review `.agent/SOP/` for documented workflows
   - Look for existing automation rules
   - Check for approval process documentation
   - Identify current pain points from project docs

4. **Use Project-Specific Skills:**
   - Check for `[project]-workflow-automation` skill
   - Look for project-specific automation patterns
   - Review project's automation best practices

5. **Match Project Patterns:**
   - Use project's terminology from documentation
   - Follow project's workflow documentation style
   - Align with project's automation approach

## Best Practices

1. **Discover Project Context First**: Scan project documentation to understand existing workflows and automation
2. **Use Project-Specific Skills**: If project has `[project]-workflow-automation` skill, collaborate with it
3. **Match Project Patterns**: Follow project's workflow documentation style and terminology
4. **Start Simple**: Begin with basic workflows and add complexity gradually
5. **Document Everything**: Maintain clear documentation matching project's documentation standards
6. **Test Thoroughly**: Test automation rules before full implementation
7. **Monitor Performance**: Track workflow efficiency and optimize continuously
8. **User-Centric Design**: Design workflows that serve users, not just automate tasks

## Resources

### references/

- `workflow-design-guide.md`: Best practices for workflow design
- `automation-patterns.md`: Common automation patterns and examples
- `approval-workflow-examples.md`: Approval workflow templates and examples

### assets/

- `workflow-template.md`: Template for documenting workflows
- `process-flowchart-template.md`: Template for creating process flowcharts
- `automation-rule-template.md`: Template for defining automation rules
