# Cursor Skills

Generic skills for content strategy, planning, analytics, and workflow automation.

## 📚 What are Skills?

Skills are folders containing:

- A `SKILL.md` file with YAML frontmatter and instructions
- Optional example files, scripts, or resources
- Specialized knowledge for specific tasks

**Key Benefits:**

- 🎯 **Automatic activation**: Claude loads them based on task context
- 🔄 **Composable**: Multiple skills can work together
- 💾 **Efficient**: Only loaded into context when needed
- 🚀 **Portable**: Work across different projects

## 🎮 How to Use Skills

Skills in `.cursor/skills/` are **automatically discovered** by Cursor. Just start working and Claude will invoke relevant skills based on your task.

**Note:** Skills activate automatically based on your task context. There is no manual invocation command - simply describe what you want to do and Claude will load the appropriate skills.

## 📦 Available Skills

### 1. Agent Folder Init

**Purpose**: Initialize a comprehensive `.agent/` folder structure for AI-first development workflows.

**When it activates:**
- Starting a new project that needs AI agent documentation
- Setting up AI-first development workflows
- Migrating an existing project to use structured AI documentation

**Key capabilities:**
- Scaffold complete `.agent/` folder structure
- Generate session tracking templates
- Create task management structure
- Set up coding standards and rules
- Initialize architecture decision records

### 2. Analytics Expert

**Purpose**: Analyze analytics data, create reports, identify trends, calculate ROI, and provide content optimization recommendations.

**When it activates:**

- Analytics questions
- Report generation requests
- Performance analysis needs
- ROI calculations
- Trend identification
- Content optimization recommendations

**Key capabilities:**

- Generate comprehensive analytics reports
- Identify performance trends
- Calculate ROI and revenue attribution
- Provide actionable insights for optimization

### 3. Changelog Generator

**Purpose**: Generate user-facing changelogs from git commit history.

**When it activates:**
- Creating release notes
- Generating changelog entries
- Documenting version changes

**Key capabilities:**
- Parse git commit history
- Generate formatted changelogs
- Categorize changes by type
- Create user-friendly release notes

### 4. Design Consistency Auditor

**Purpose**: Audit design consistency across projects and identify inconsistencies.

**When it activates:**
- Design review requests
- Consistency audit needs
- Style guide compliance checks

**Key capabilities:**
- Audit design patterns
- Identify inconsistencies
- Generate audit reports
- Recommend improvements

### 5. Fullstack Workspace Init

**Purpose**: Initialize fullstack workspace structure with monorepo support.

**When it activates:**
- Setting up new fullstack projects
- Creating monorepo workspaces
- Initializing workspace structure

**Key capabilities:**
- Scaffold fullstack workspace
- Set up monorepo structure
- Initialize API and frontend projects
- Configure workspace dependencies

### 6. Internal Comms

**Purpose**: Generate internal communications, updates, and company newsletters.

**When it activates:**
- Creating internal communications
- Generating company updates
- Writing FAQ answers
- Creating newsletters

**Key capabilities:**
- Generate internal communications
- Create company newsletters
- Write FAQ answers
- Format updates and announcements

### 7. Micro Landing Builder

**Purpose**: Build micro landing pages with customizable sections and templates.

**When it activates:**
- Creating landing pages
- Building marketing pages
- Designing product pages

**Key capabilities:**
- Generate landing page structure
- Create customizable sections
- Apply templates
- Optimize for conversion

### 8. Planning Assistant

**Purpose**: Help with content planning, calendar management, research organization, content ideation, and multi-platform planning.

**When it activates:**

- Content planning requests
- Calendar management needs
- Research organization tasks
- Content ideation requests
- Multi-platform planning

**Key capabilities:**

- Weekly/monthly planning assistance
- Research organization and synthesis
- Content calendar creation
- Inspiration-to-plan conversion
- Multi-platform content planning

### 9. Project Scaffold

**Purpose**: Unified project scaffolder for creating new projects or adding components to existing ones.

**When it activates:**
- Starting new projects from scratch
- Adding components to existing projects
- Setting up monorepo or separate repositories

**Key capabilities:**
- Scaffold `.agent/` folder structure
- Create backend (NestJS) projects
- Create frontend (NextJS) projects
- Set up mobile (Expo) projects
- Initialize browser extensions (Plasmo)

### 10. QA Reviewer

**Purpose**: Quality assurance review assistance for code and features.

**When it activates:**
- Code review requests
- Quality assurance checks
- Testing review needs

**Key capabilities:**
- Review code quality
- Identify potential issues
- Suggest improvements
- Validate test coverage

### 11. Roadmap Analyzer

**Purpose**: Analyze and plan product roadmaps based on user needs and priorities.

**When it activates:**
- Roadmap planning requests
- Feature prioritization needs
- Product planning assistance

**Key capabilities:**
- Analyze roadmap requirements
- Prioritize features
- Plan product roadmaps
- Generate roadmap documentation

### 12. Session Documenter

**Purpose**: Automatically document session work, decisions, and context for continuity.

**When it activates:**
- After task completion
- When files are modified
- When architectural decisions are made
- At session end (mandatory)

**Key capabilities:**
- Document session work
- Track decisions and changes
- Maintain session continuity
- Generate session summaries

### 13. Strategy Expert

**Purpose**: Assist with content strategy, persona building, competitive analysis, content planning, and brand voice consistency.

**When it activates:**

- Content strategy questions
- Persona/target audience building
- Competitive analysis requests
- Content planning and ideation
- Brand voice questions

**Key capabilities:**

- Build customer personas from analytics data
- Conduct competitive content analysis
- Plan content calendars
- Manage research-to-content workflows
- Ensure brand voice consistency

### 14. Webapp Testing

**Purpose**: Web application testing assistance and automation.

**When it activates:**
- Testing web applications
- Creating test scripts
- Automating test scenarios

**Key capabilities:**
- Create test scripts
- Automate web testing
- Generate test reports
- Validate functionality

### 15. Workflow Automation

**Purpose**: Design content workflows, create process documentation, implement automation rules, design approval processes, and optimize content pipelines.

**When it activates:**

- Workflow design requests
- Process documentation needs
- Automation rule creation
- Approval workflow design
- Content pipeline optimization

**Key capabilities:**

- Design content workflows
- Create process documentation
- Suggest automation rules
- Document approval processes
- Optimize content pipelines

## Adapting Skills to Your Project

These skills are designed for content platforms but can be adapted:

- **Platform references**: Replace platform-specific references with your project's terminology
- **Data sources**: Adapt analytics/data source references to your system
- **Workflows**: Customize workflow examples to your processes
- **Integration points**: Update integration examples to your architecture

## Adding New Skills

Create a new directory in `.cursor/skills/` with:

1. `SKILL.md` file with YAML frontmatter:

   ```yaml
   ---
   name: skill-name
   description: Brief description of when this skill activates
   ---
   ```

2. Instructions and examples in the SKILL.md file

3. Optional supporting files (examples, scripts, etc.)

## Notes

- Skills activate automatically based on task context
- Skills can work together (composable)
- Adapt platform-specific references to your project
- Update integration examples to match your architecture

---

**Total Skills:** 15
**Last Updated:** 2025-01-XX
