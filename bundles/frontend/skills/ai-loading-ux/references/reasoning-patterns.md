# Reasoning Display Patterns

For AI interfaces that show chain-of-thought or "thinking" processes.

## Table of Contents

- [When to Use](#when-to-use)
- [Anatomy of a Thinking Indicator](#anatomy-of-a-thinking-indicator)
- [Visibility Levels](#visibility-levels)
- [State Machine](#state-machine)
- [Implementation Patterns](#implementation-patterns)
- [Accessibility](#accessibility)

## When to Use

Use reasoning display when:

- AI is solving complex problems (math, logic, planning)
- Users benefit from understanding *how* the answer was reached
- Trust-building is important (financial, medical, legal domains)
- The process takes >3 seconds

Skip reasoning display when:

- Simple Q&A or lookups
- Speed is more important than transparency
- Content speaks for itself (creative writing, summaries)

## Anatomy of a Thinking Indicator

```
┌─────────────────────────────────────────┐
│ 🧠 Thinking...                    12s   │  ← Header: icon + label + timer
├─────────────────────────────────────────┤
│ ▸ Analyzing the problem                 │  ← Expandable reasoning steps
│ ▸ Considering edge cases                │
│ • Checking mathematical constraints     │  ← Current step (animated)
└─────────────────────────────────────────┘
```

**Components:**

1. **Icon** - Animated to show activity (brain, sparkles, dots)
2. **Label** - Changes based on phase ("Thinking...", "Analyzing...", "Finalizing...")
3. **Timer** - Elapsed time (reduces anxiety about stuck states)
4. **Reasoning list** - Structured bullets, progressive reveal
5. **Expand/collapse** - User control over detail level

## Visibility Levels

### Level 1: Minimal (ChatGPT-style)

```
Thinking...
```

- Just a label + animation
- Collapses when done
- Best for: Fast responses, simple queries

### Level 2: Summary (Claude-style)

```
▼ Thinking (8s)
  • Analyzing request
  • Searching knowledge
  • Formulating response
```

- Collapsed by default, expandable
- Shows high-level steps
- Best for: Balance of transparency and simplicity

### Level 3: Verbose (DeepSeek-style)

```
Thinking...
First, I need to understand what the user is asking.
They want to know about X, which involves Y and Z.
Let me consider the implications...
[continues streaming]
```

- Full reasoning visible
- Streams in real-time
- Best for: Power users, debugging, research contexts

## State Machine

```
┌─────────┐    start    ┌──────────┐   complete   ┌──────────┐
│  Idle   │ ─────────→  │ Thinking │  ─────────→  │   Done   │
└─────────┘             └──────────┘              └──────────┘
                              │                        │
                              │ error                  │ dismiss
                              ▼                        ▼
                        ┌──────────┐              ┌──────────┐
                        │  Error   │              │  Hidden  │
                        └──────────┘              └──────────┘
```

**State behaviors:**

- **Idle**: No indicator visible
- **Thinking**: Animated indicator, timer counting, steps appearing
- **Done**: Animation stops, checkmark or fade, then transition to answer
- **Error**: Red state, error message, retry option
- **Hidden**: Collapsed but accessible via "Show thinking"

## Implementation Patterns

### Pattern A: Collapsible Accordion

```
// Pseudocode - adapt to your framework

ThinkingIndicator:
  state: collapsed | expanded
  steps: string[]
  currentStep: number
  elapsedTime: number

  render:
    if collapsed:
      <Row onClick={expand}>
        <AnimatedIcon />
        <Label>"Thinking..."</Label>
        <Timer>{elapsedTime}s</Timer>
        <ChevronDown />
      </Row>

    if expanded:
      <Column>
        <Header onClick={collapse}>
          <AnimatedIcon />
          <Label>"Thinking..."</Label>
          <Timer>{elapsedTime}s</Timer>
          <ChevronUp />
        </Header>
        <StepList>
          {steps.map((step, i) =>
            <Step
              complete={i < currentStep}
              active={i === currentStep}
            >
              {step}
            </Step>
          )}
        </StepList>
      </Column>
```

### Pattern B: Inline Badge

```
// For chat interfaces where thinking appears inline

<Message>
  <ThinkingBadge status={thinking ? "active" : "complete"}>
    {thinking ? "Thinking..." : `Thought for ${time}s`}
  </ThinkingBadge>
  {!thinking && <Content>{response}</Content>}
</Message>
```

### Pattern C: Side Panel

```
// For complex reasoning that shouldn't interrupt main flow

<Layout>
  <MainContent>
    {response}
  </MainContent>
  <SidePanel visible={showReasoning}>
    <ReasoningTrace steps={steps} />
  </SidePanel>
</Layout>
```

## Accessibility

- **Screen readers**: Announce state changes ("Now thinking", "Response ready")
- **Reduced motion**: Replace animations with static indicators
- **Keyboard**: Expand/collapse with Enter/Space
- **Color**: Don't rely on color alone for state (use icons too)

## Common Mistakes

1. **No end state** - Users don't know thinking finished
2. **Too verbose** - Reasoning overwhelms the answer
3. **No escape** - Can't stop or skip long thinking
4. **Frozen UI** - Blocking interaction during thinking
5. **Lost on error** - No recovery path when thinking fails
