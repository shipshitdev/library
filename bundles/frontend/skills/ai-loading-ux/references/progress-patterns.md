# Progress Step Patterns

For AI interfaces that complete multi-step tasks.

## Table of Contents

- [When to Use](#when-to-use)
- [Anatomy of Progress Steps](#anatomy-of-progress-steps)
- [Step States](#step-states)
- [Layout Patterns](#layout-patterns)
- [Implementation Patterns](#implementation-patterns)
- [Edge Cases](#edge-cases)

## When to Use

Use progress steps when:

- Task has 3+ discrete steps
- Steps complete sequentially
- Users need to know what's happening at each stage
- Total time exceeds 10 seconds

Examples:

- "Analyzing document → Extracting data → Formatting report"
- "Searching → Filtering → Ranking → Generating response"
- "Uploading → Processing → Saving"

## Anatomy of Progress Steps

```
┌─────────────────────────────────────────────────────┐
│  Processing your request                            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━░░░░░░░░  75%     │
├─────────────────────────────────────────────────────┤
│  ✓ Analyzing document              2.3s            │
│  ✓ Extracting key information      4.1s            │
│  ● Generating summary...           1.2s            │
│  ○ Formatting output                               │
└─────────────────────────────────────────────────────┘
```

**Components:**

1. **Header** - Overall task description
2. **Progress bar** - Visual completion indicator
3. **Step list** - Individual steps with status
4. **Timing** - Per-step or total elapsed time

## Step States

| State | Visual | Behavior |
|-------|--------|----------|
| Pending | ○ (empty circle) | Grayed out, waiting |
| Active | ● (filled, pulsing) | Highlighted, animated |
| Complete | ✓ (checkmark) | Green, shows duration |
| Error | ✗ (x mark) | Red, shows error message |
| Skipped | — (dash) | Gray, strikethrough |

## Layout Patterns

### Vertical List (Default)

```
✓ Step 1: Completed
● Step 2: In progress...
○ Step 3: Pending
○ Step 4: Pending
```

Best for: 3-7 steps, detailed descriptions

### Horizontal Stepper

```
[1]───[2]───[3]───[4]
 ✓     ●     ○     ○
```

Best for: 3-5 steps, compact UI, wizards

### Compact Badge

```
Step 2 of 4: Processing...
```

Best for: Minimal UI, mobile, inline display

### Timeline

```
2:00 PM ─● Started analysis
2:01 PM ─✓ Extracted 234 records
2:02 PM ─● Generating report...
         ○ Finalizing
```

Best for: Audit trails, long-running tasks

## Implementation Patterns

### Pattern A: Linear Steps with Substeps

```
// Pseudocode

ProgressSteps:
  steps: Step[]
  currentStep: number

  Step:
    label: string
    status: pending | active | complete | error
    substeps?: string[]
    duration?: number

  render:
    <Container>
      <ProgressBar percent={currentStep / steps.length * 100} />
      <StepList>
        {steps.map((step, i) =>
          <StepRow status={step.status}>
            <StatusIcon status={step.status} />
            <Label>{step.label}</Label>
            {step.duration && <Duration>{step.duration}s</Duration>}
            {step.status === "active" && step.substeps && (
              <Substeps>
                {step.substeps.map(sub => <SubstepRow>{sub}</SubstepRow>)}
              </Substeps>
            )}
          </StepRow>
        )}
      </StepList>
    </Container>
```

### Pattern B: Streaming Steps

```
// Steps appear as they're discovered (not predetermined)

StreamingProgress:
  steps: Step[] = []

  onNewStep(step):
    steps.push(step)

  onStepComplete(stepId):
    steps.find(s => s.id === stepId).status = "complete"

  render:
    <Container>
      {steps.map(step => <StepRow {...step} />)}
      {isProcessing && <PendingIndicator />}
    </Container>
```

### Pattern C: Action Plan Preview

```
// Show planned steps before execution (builds trust)

ActionPlan:
  plannedSteps: string[]
  executedSteps: Step[]

  render:
    <Container>
      <Header>I'll do the following:</Header>
      {plannedSteps.map((step, i) => {
        const executed = executedSteps[i]
        return (
          <StepRow
            status={executed?.status || "pending"}
            label={step}
            actual={executed?.label} // May differ from planned
          />
        )
      })}
    </Container>
```

## Edge Cases

### Unknown Step Count

When you don't know how many steps upfront:

```
Processing... (Step 3)
✓ Analyzed structure
✓ Extracted entities
● Resolving references...
```

- Show completed count, not percentage
- Add "..." to indicate more may come

### Step Failure with Recovery

```
✓ Step 1: Complete
✗ Step 2: Failed - Retrying (attempt 2/3)
○ Step 3: Waiting
```

- Show retry status
- Don't reset the whole progress
- Offer skip option for non-critical steps

### Parallel Steps

```
● Processing (3 tasks running)
  ├─ ● Analyzing images (12/50)
  ├─ ● Extracting text (34/50)
  └─ ● Classifying content (8/50)
```

- Show each parallel task's progress
- Complete parent when all children complete

### Long-Running Steps

```
● Generating report... (2m 34s)
  Last update: Processing section 4 of 12

  [Show Details] [Cancel]
```

- Provide sub-progress or last action
- Always offer cancel for long steps
- Consider timeout warnings

## Accessibility

- Use `aria-live="polite"` for step announcements
- Progress bar needs `role="progressbar"` with `aria-valuenow`
- Ensure color isn't only indicator (icons matter)
- Support keyboard navigation between steps
