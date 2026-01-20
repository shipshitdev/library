# Advanced Evaluation - Full Guide

This guide covers production-grade techniques for evaluating LLM outputs using LLMs as judges. It synthesizes research from academic papers, industry practices, and practical implementation experience.

## Metric Selection Framework

Choose metrics based on the evaluation task structure:

| Task Type | Primary Metrics | Secondary Metrics |
|-----------|-----------------|-------------------|
| Binary classification (pass/fail) | Recall, Precision, F1 | Cohen's κ |
| Ordinal scale (1-5 rating) | Spearman's ρ, Kendall's τ | Cohen's κ (weighted) |
| Pairwise preference | Agreement rate, Position consistency | Confidence calibration |
| Multi-label | Macro-F1, Micro-F1 | Per-label precision/recall |

**Critical insight**: High absolute agreement matters less than systematic disagreement patterns. A judge that consistently disagrees with humans on specific criteria is more problematic than one with random noise.

## Evaluation Approaches

### Direct Scoring Implementation

Direct scoring requires three components: clear criteria, a calibrated scale, and structured output format.

**Criteria Definition Pattern**:

```
Criterion: [Name]
Description: [What this criterion measures]
Weight: [Relative importance, 0-1]
```

**Scale Calibration**:

- 1-3 scales: Binary with neutral option, lowest cognitive load
- 1-5 scales: Standard Likert, good balance of granularity and reliability
- 1-10 scales: High granularity but harder to calibrate, use only with detailed rubrics

**Prompt Structure for Direct Scoring**:

```
You are an expert evaluator assessing response quality.

## Task
Evaluate the following response against each criterion.

## Original Prompt
{prompt}

## Response to Evaluate
{response}

## Criteria
{for each criterion: name, description, weight}

## Instructions
For each criterion:
1. Find specific evidence in the response
2. Score according to the rubric (1-{max} scale)
3. Justify your score with evidence
4. Suggest one specific improvement

## Output Format
Respond with structured JSON containing scores, justifications, and summary.
```

**Chain-of-Thought Requirement**: All scoring prompts must require justification before the score. Research shows this improves reliability by 15-25% compared to score-first approaches.

### Pairwise Comparison Implementation

Pairwise comparison is inherently more reliable for preference-based evaluation but requires bias mitigation.

**Position Bias Mitigation Protocol**:

1. First pass: Response A in first position, Response B in second
2. Second pass: Response B in first position, Response A in second
3. Consistency check: If passes disagree, return TIE with reduced confidence
4. Final verdict: Consistent winner with averaged confidence

**Prompt Structure for Pairwise Comparison**:

```
You are an expert evaluator comparing two AI responses.

## Critical Instructions
- Do NOT prefer responses because they are longer
- Do NOT prefer responses based on position (first vs second)
- Focus ONLY on quality according to the specified criteria
- Ties are acceptable when responses are genuinely equivalent

## Original Prompt
{prompt}

## Response A
{response_a}

## Response B
{response_b}

## Comparison Criteria
{criteria list}

## Instructions
1. Analyze each response independently first
2. Compare them on each criterion
3. Determine overall winner with confidence level

## Output Format
JSON with per-criterion comparison, overall winner, confidence (0-1), and reasoning.
```

**Confidence Calibration**: Confidence scores should reflect position consistency:

- Both passes agree: confidence = average of individual confidences
- Passes disagree: confidence = 0.5, verdict = TIE

### Rubric Generation

Well-defined rubrics reduce evaluation variance by 40-60% compared to open-ended scoring.

**Rubric Components**:

1. **Level descriptions**: Clear boundaries for each score level
2. **Characteristics**: Observable features that define each level
3. **Examples**: Representative text for each level (optional but valuable)
4. **Edge cases**: Guidance for ambiguous situations
5. **Scoring guidelines**: General principles for consistent application

**Strictness Calibration**:

- **Lenient**: Lower bar for passing scores, appropriate for encouraging iteration
- **Balanced**: Fair, typical expectations for production use
- **Strict**: High standards, appropriate for safety-critical or high-stakes evaluation

**Domain Adaptation**: Rubrics should use domain-specific terminology. A "code readability" rubric mentions variables, functions, and comments. A "medical accuracy" rubric references clinical terminology and evidence standards.

## Evaluation Pipeline Design

Production evaluation systems require multiple layers:

```
┌─────────────────────────────────────────────────┐
│                 Evaluation Pipeline              │
├─────────────────────────────────────────────────┤
│                                                   │
│  Input: Response + Prompt + Context               │
│           │                                       │
│           ▼                                       │
│  ┌─────────────────────┐                         │
│  │   Criteria Loader   │ ◄── Rubrics, weights    │
│  └──────────┬──────────┘                         │
│             │                                     │
│             ▼                                     │
│  ┌─────────────────────┐                         │
│  │   Primary Scorer    │ ◄── Direct or Pairwise  │
│  └──────────┬──────────┘                         │
│             │                                     │
│             ▼                                     │
│  ┌─────────────────────┐                         │
│  │   Bias Mitigation   │ ◄── Position swap, etc. │
│  └──────────┬──────────┘                         │
│             │                                     │
│             ▼                                     │
│  ┌─────────────────────┐                         │
│  │ Confidence Scoring  │ ◄── Calibration         │
│  └──────────┬──────────┘                         │
│             │                                     │
│             ▼                                     │
│  Output: Scores + Justifications + Confidence     │
│                                                   │
└─────────────────────────────────────────────────┘
```

## Common Anti-Patterns

**Anti-pattern: Scoring without justification**

- Problem: Scores lack grounding, difficult to debug or improve
- Solution: Always require evidence-based justification before score

**Anti-pattern: Single-pass pairwise comparison**

- Problem: Position bias corrupts results
- Solution: Always swap positions and check consistency

**Anti-pattern: Overloaded criteria**

- Problem: Criteria measuring multiple things are unreliable
- Solution: One criterion = one measurable aspect

**Anti-pattern: Missing edge case guidance**

- Problem: Evaluators handle ambiguous cases inconsistently
- Solution: Include edge cases in rubrics with explicit guidance

**Anti-pattern: Ignoring confidence calibration**

- Problem: High-confidence wrong judgments are worse than low-confidence
- Solution: Calibrate confidence to position consistency and evidence strength

## Scaling Evaluation

For high-volume evaluation:

1. **Panel of LLMs (PoLL)**: Use multiple models as judges, aggregate votes
   - Reduces individual model bias
   - More expensive but more reliable for high-stakes decisions

2. **Hierarchical evaluation**: Fast cheap model for screening, expensive model for edge cases
   - Cost-effective for large volumes
   - Requires calibration of screening threshold

3. **Human-in-the-loop**: Automated evaluation for clear cases, human review for low-confidence
   - Best reliability for critical applications
   - Design feedback loop to improve automated evaluation

## Examples

### Example 1: Direct Scoring for Accuracy

**Input**:

```
Prompt: "What causes seasons on Earth?"
Response: "Seasons are caused by Earth's tilted axis. As Earth orbits the Sun,
different hemispheres receive more direct sunlight at different times of year."
Criterion: Factual Accuracy (weight: 1.0)
Scale: 1-5
```

**Output**:

```json
{
  "criterion": "Factual Accuracy",
  "score": 5,
  "evidence": [
    "Correctly identifies axial tilt as primary cause",
    "Correctly explains differential sunlight by hemisphere",
    "No factual errors present"
  ],
  "justification": "Response accurately explains the cause of seasons with correct
scientific reasoning. Both the axial tilt and its effect on sunlight distribution
are correctly described.",
  "improvement": "Could add the specific tilt angle (23.5°) for completeness."
}
```

### Example 2: Pairwise Comparison with Position Swap

**Input**:

```
Prompt: "Explain machine learning to a beginner"
Response A: [Technical explanation with jargon]
Response B: [Simple analogy-based explanation]
Criteria: ["clarity", "accessibility"]
```

**First Pass (A first)**:

```json
{ "winner": "B", "confidence": 0.8 }
```

**Second Pass (B first)**:

```json
{ "winner": "A", "confidence": 0.6 }
```

(Note: Winner is A because B was in first position)

**Mapped Second Pass**:

```json
{ "winner": "B", "confidence": 0.6 }
```

**Final Result**:

```json
{
  "winner": "B",
  "confidence": 0.7,
  "positionConsistency": {
    "consistent": true,
    "firstPassWinner": "B",
    "secondPassWinner": "B"
  }
}
```

### Example 3: Rubric Generation

**Input**:

```
criterionName: "Code Readability"
criterionDescription: "How easy the code is to understand and maintain"
domain: "software engineering"
scale: "1-5"
strictness: "balanced"
```

**Output** (abbreviated):

```json
{
  "levels": [
    {
      "score": 1,
      "label": "Poor",
      "description": "Code is difficult to understand without significant effort",
      "characteristics": [
        "No meaningful variable or function names",
        "No comments or documentation",
        "Deeply nested or convoluted logic"
      ]
    },
    {
      "score": 3,
      "label": "Adequate",
      "description": "Code is understandable with some effort",
      "characteristics": [
        "Most variables have meaningful names",
        "Basic comments present for complex sections",
        "Logic is followable but could be cleaner"
      ]
    },
    {
      "score": 5,
      "label": "Excellent",
      "description": "Code is immediately clear and maintainable",
      "characteristics": [
        "All names are descriptive and consistent",
        "Comprehensive documentation",
        "Clean, modular structure"
      ]
    }
  ],
  "edgeCases": [
    {
      "situation": "Code is well-structured but uses domain-specific abbreviations",
      "guidance": "Score based on readability for domain experts, not general audience"
    }
  ]
}
```

## Guidelines

1. **Always require justification before scores** - Chain-of-thought prompting improves reliability by 15-25%

2. **Always swap positions in pairwise comparison** - Single-pass comparison is corrupted by position bias

3. **Match scale granularity to rubric specificity** - Don't use 1-10 without detailed level descriptions

4. **Separate objective and subjective criteria** - Use direct scoring for objective, pairwise for subjective

5. **Include confidence scores** - Calibrate to position consistency and evidence strength

6. **Define edge cases explicitly** - Ambiguous situations cause the most evaluation variance

7. **Use domain-specific rubrics** - Generic rubrics produce generic (less useful) evaluations

8. **Validate against human judgments** - Automated evaluation is only valuable if it correlates with human assessment

9. **Monitor for systematic bias** - Track disagreement patterns by criterion, response type, model

10. **Design for iteration** - Evaluation systems improve with feedback loops

## References

External research:

- [Eugene Yan: Evaluating the Effectiveness of LLM-Evaluators](https://eugeneyan.com/writing/llm-evaluators/)
- [Judging LLM-as-a-Judge (Zheng et al., 2023)](https://arxiv.org/abs/2306.05685)
- [G-Eval: NLG Evaluation using GPT-4 (Liu et al., 2023)](https://arxiv.org/abs/2303.16634)
- [Large Language Models are not Fair Evaluators (Wang et al., 2023)](https://arxiv.org/abs/2305.17926)

---

**Created**: 2024-12-24
**Last Updated**: 2024-12-24
**Author**: Muratcan Koylan
