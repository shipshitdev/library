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

### 1. Analytics Expert

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

### 2. Planning Assistant

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

### 3. Strategy Expert

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

### 4. Workflow Automation

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

**Total Skills:** 4
**Last Updated:** 2025-12-24
