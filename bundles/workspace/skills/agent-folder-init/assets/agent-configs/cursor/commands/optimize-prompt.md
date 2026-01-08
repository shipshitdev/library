# Optimize Prompt (Lyra-Inspired)

**Purpose:** Transform vague prompts into precision-crafted, effective AI prompts using systematic optimization.

## When to Use

- Optimizing AI generation prompts (posts, images, videos)
- Improving `/gen-template` prompt templates
- Enhancing AI instructions in services
- Creating better system prompts
- Debugging poor AI responses

## The 4-D Optimization Framework

### 1. DECONSTRUCT

**Extract Core Elements:**

```
- [ ] Core intent: What's the goal?
- [ ] Key entities: What are we working with?
- [ ] Context: What background info matters?
- [ ] Output format: What should the result look like?
- [ ] Constraints: What are the limitations?
- [ ] Missing info: What's unclear?
```

**Example:**

```markdown
INPUT: "Write me a post about AI"

DECONSTRUCT:

- Intent: Generate social media content
- Entity: AI topic (vague)
- Context: Missing (platform? audience? tone?)
- Output: Social media post (which platform?)
- Constraints: Unknown (length? style?)
- Missing: Platform, audience, key message, tone
```

### 2. DIAGNOSE

**Audit for Issues:**

```
- [ ] Clarity: Is intent clear?
- [ ] Specificity: Are requirements concrete?
- [ ] Completeness: Is all needed info present?
- [ ] Structure: Is prompt well-organized?
- [ ] Complexity: Does it match task difficulty?
```

**Common Issues:**

- **Vague:** "Make it good" → Define "good"
- **Ambiguous:** "Professional tone" → What kind of professional?
- **Missing context:** "Write about AI" → For whom? Why?
- **No examples:** Shows instead of tells
- **Poor structure:** Wall of text vs. organized sections

### 3. DEVELOP

**Select Optimization Techniques:**

#### For Creative Tasks (Posts, Marketing)

```
✅ Use:
- Multi-perspective analysis
- Tone emphasis
- Audience specification
- Example-driven guidance
- Brand voice constraints
```

#### For Technical Tasks (Code, Analysis)

```
✅ Use:
- Constraint-based approaches
- Precision focus
- Step-by-step structure
- Error handling specs
- Output format specification
```

#### For Educational Content

```
✅ Use:
- Few-shot examples
- Clear structure
- Progressive complexity
- Explanation requirements
```

#### For Complex Requests

```
✅ Use:
- Chain-of-thought reasoning
- Systematic frameworks
- Break into subtasks
- Validation steps
```

### 4. DELIVER

**Construct Optimized Prompt:**

```markdown
# Template Structure

## Role & Context

[Who the AI should act as and what context matters]

## Task

[Clear, specific description of what to do]

## Requirements

- [Specific requirement 1]
- [Specific requirement 2]
- [Etc.]

## Constraints

- [Limitation 1]
- [Limitation 2]

## Output Format

[Exactly how the result should be structured]

## Examples (if applicable)

[Show, don't just tell]
```

## Optimization Techniques

### Foundation Techniques

**1. Role Assignment**

```markdown
❌ BEFORE: "Write a tweet"
✅ AFTER: "You are a social media expert specializing in tech content for B2B SaaS companies."
```

**2. Context Layering**

```markdown
❌ BEFORE: "Create a post about our product"
✅ AFTER: "Create a LinkedIn post about our AI-powered content generation tool. Target audience: Marketing teams at SMBs (10-100 employees) who struggle with consistent social media presence. Key benefit: Save 10 hours/week on content creation."
```

**3. Output Specifications**

```markdown
❌ BEFORE: "Make it short"
✅ AFTER: "Length: 150-200 characters (Twitter limit). Include 2-3 relevant hashtags. End with a call-to-action question."
```

**4. Task Decomposition**

```markdown
❌ BEFORE: "Create a marketing campaign"
✅ AFTER:
"Create a marketing campaign in 3 steps:

1. Analyze target audience pain points
2. Draft 3 post concepts addressing each pain point
3. Select the strongest concept and expand into full copy"
```

### Advanced Techniques

**5. Chain-of-Thought Reasoning**

```markdown
"Before writing the post:

1. Identify the core message (1 sentence)
2. List 3 supporting points
3. Choose the most compelling hook
4. Structure the narrative arc
5. Write the post following this structure"
```

**6. Few-Shot Learning**

```markdown
"Example 1:
Input: AI automation
Output: 'Just automated 3 hours of daily tasks with AI. What repetitive work are you still doing manually? 🤖 #ProductivityHack #AITools'

Example 2:
Input: Team collaboration
Output: 'Best team wins: The one that communicates async. Here's how we cut meetings by 60% 👇 #RemoteWork #TeamWork'

Now create a similar post for: [your topic]"
```

**7. Constraint Optimization**

```markdown
"Constraints:

- MUST include specific numbers/metrics
- MUST start with a hook (question or bold statement)
- MUST be under 280 characters
- MUST NOT use corporate jargon
- MUST include call-to-action
- MUST match brand voice: Friendly, data-driven, helpful (not salesy)"
```

## Platform-Specific Optimization

### For OpenAI (GPT-4)

```markdown
✅ Use:

- Structured sections with headers
- Clear role definitions
- Specific constraints
- Example outputs

⚠️ Watch:

- Very long prompts (may lose focus)
- Complex nested instructions
```

### For Anthropic (Claude)

```markdown
✅ Use:

- Longer context (100K tokens)
- Multi-step reasoning frameworks
- Document analysis tasks
- Nuanced instructions

⚠️ Watch:

- Be explicit about format
- Provide clear success criteria
```

### For Replicate (Image/Video)

```markdown
✅ Use:

- Detailed visual descriptions
- Style specifications
- Composition guidance
- Negative prompts (what to avoid)

⚠️ Watch:

- Abstract concepts need concrete visual descriptions
- Multiple subjects can be confusing
```

## Common Use Cases

### 1. Social Media Post Generation

**Before Optimization:**

```
"Write a post about {topic}"
```

**After Optimization:**

```markdown
You are a social media expert creating content for {platform}.

AUDIENCE: {audience_description}
BRAND VOICE: {brand_voice}
TOPIC: {topic}

REQUIREMENTS:

- Length: {character_limit}
- Include {num_hashtags} relevant hashtags
- Start with a compelling hook (question or bold statement)
- Include specific data/numbers if relevant
- End with call-to-action or engagement question
- Match platform best practices ({platform} style)

CONSTRAINTS:

- No corporate jargon
- No emojis unless brand voice allows
- Must be authentic and valuable (not salesy)
- Must align with brand voice tone

OUTPUT FORMAT:
[Post text]
[Hashtags]
[Emoji suggestions (optional)]
```

### 2. Image Generation Prompts

**Before Optimization:**

```
"A professional photo for social media"
```

**After Optimization:**

```markdown
Create a professional photo for {platform} social media post.

SUBJECT: {description}
STYLE: {style} (e.g., "modern flat design", "photorealistic", "minimalist")
COMPOSITION: {composition} (e.g., "centered subject, rule of thirds")
LIGHTING: {lighting} (e.g., "soft natural light", "dramatic side lighting")
COLOR PALETTE: {colors} (e.g., "warm earth tones", "vibrant blues and greens")
MOOD: {mood} (e.g., "energetic", "calm and professional")

TECHNICAL SPECS:

- Aspect ratio: {ratio} (e.g., 1:1 for Instagram, 16:9 for LinkedIn)
- Resolution: High (for social media)
- Focus: Sharp foreground, subtle background blur

AVOID (Negative prompt):

- {unwanted_elements}
- {bad_styles}
- Text in image
- Watermarks
```

### 3. Template Optimization (/gen-template)

**Before Optimization:**

```markdown
# Prompt

Generate {type}

# Input

{user_input}
```

**After Optimization:**

```markdown
# System Prompt

You are an expert {role} creating {type} for {platform}.

# Context

- Platform: {platform}
- Audience: {target_audience}
- Brand: {brand_voice_summary}
- Goal: {primary_goal}

# Instructions

1. Analyze the user input for key themes
2. Identify 2-3 main value propositions
3. Structure content following {platform} best practices
4. Ensure {specific_requirement}
5. Validate against constraints below

# Requirements

{requirements_list}

# Constraints

{constraints_list}

# User Input

{user_input}

# Output Format

{expected_output_structure}

# Quality Checks

Before delivering:

- [ ] Meets length requirements
- [ ] Matches brand voice
- [ ] Includes required elements
- [ ] Avoids prohibited elements
- [ ] Clear call-to-action present
```

## Prompt Optimization Workflow

### Step 1: Identify Current Prompt

```bash
# For template optimization
cat apps/api/src/prompts/templates/{template-name}.md
```

### Step 2: Apply 4-D Framework

1. **Deconstruct:** Break down what it's trying to do
2. **Diagnose:** Find gaps, ambiguity, missing context
3. **Develop:** Choose appropriate techniques
4. **Deliver:** Write optimized version

### Step 3: Test & Iterate

```typescript
// Test in service
const result = await this.openai.chat.completions.create({
  model: "gpt-4",
  messages: [
    { role: "system", content: optimizedPrompt },
    { role: "user", content: testInput },
  ],
});

// Compare results
console.log("Before:", originalResult);
console.log("After:", result);
```

### Step 4: Measure Improvement

```
Metrics to track:
- [ ] Output relevance (1-10)
- [ ] Output quality (1-10)
- [ ] Consistency across runs
- [ ] Tokens used (cost)
- [ ] Time to generate
- [ ] User satisfaction
```

## Common Optimization Patterns

### Pattern 1: Add Constraints

```markdown
❌ BEFORE: "Write professionally"
✅ AFTER: "Use professional tone: clear, concise, no jargon. Active voice. Second person ('you'). Max 200 words."
```

### Pattern 2: Provide Examples

```markdown
❌ BEFORE: "Make it engaging"
✅ AFTER: "Engaging style example: 'Ever wonder why...? Here's what we learned: [insight]. Try this: [action]'"
```

### Pattern 3: Specify Format

```markdown
❌ BEFORE: "List the benefits"
✅ AFTER: "Format: 3 benefits, each as: [Emoji] [Bold title]: [One sentence explanation]"
```

### Pattern 4: Add Reasoning Steps

```markdown
❌ BEFORE: "Create a summary"
✅ AFTER: "Create a summary by: 1) Identifying 3 main points, 2) Distilling each to one sentence, 3) Connecting with transitions"
```

## Integration Examples

### Update Prompt Templates

```bash
# After optimization, update template
# Location: [project]/src/prompts/templates/

# Then apply optimized prompt structure
```

### Test in Services

```typescript
// Example: [project]/src/services/content.service.ts
async generateContent(prompt: string, platform: string) {
  const optimizedPrompt = this.buildOptimizedPrompt({
    platform,
    userInput: prompt,
    brandVoice: await this.getBrandVoice(),
    requirements: this.getPlatformRequirements(platform)
  });

  return this.aiService.generate(optimizedPrompt);
}
```

## Best Practices

```
✅ DO:
- Be specific about output format
- Provide concrete examples
- Define constraints clearly
- Test multiple variations
- Measure results objectively

❌ DON'T:
- Use vague terms ("good", "professional")
- Over-complicate simple tasks
- Forget platform-specific requirements
- Skip testing phase
- Ignore token costs
```

## Quick Reference

**Quick Prompt Checklist:**

```
- [ ] Clear role/persona defined
- [ ] Specific task description
- [ ] Context provided
- [ ] Output format specified
- [ ] Constraints listed
- [ ] Examples included (if helpful)
- [ ] Quality criteria defined
```

---

**Created:** 2025-11-21
**Category:** Specialized
**Inspired by:** claudecodecommands.directory/Lyra
