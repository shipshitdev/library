# Streaming Content Patterns

For AI interfaces that display content as it generates token-by-token.

## Table of Contents

- [When to Use](#when-to-use)
- [Streaming Behaviors](#streaming-behaviors)
- [Visual Indicators](#visual-indicators)
- [Implementation Patterns](#implementation-patterns)
- [Performance Considerations](#performance-considerations)
- [Edge Cases](#edge-cases)

## When to Use

Use streaming display when:

- Content generates incrementally (LLM token streaming)
- Showing progress reduces perceived wait time
- Users can start reading before generation completes
- Response length is unpredictable

Skip streaming when:

- Response is very short (<50 tokens)
- Content needs validation before display
- Structured output must be complete to render (JSON, tables)

## Streaming Behaviors

### Text Streaming

```
The quick brown fox jum|
The quick brown fox jumps over|
The quick brown fox jumps over the lazy dog.|
```

- Append tokens as received
- Cursor indicates active generation

### Block Streaming

```
┌──────────────────────────┐
│ Generating...            │
│ ████████░░░░░░░░ 50%     │
└──────────────────────────┘
         ↓
┌──────────────────────────┐
│ Here is your summary:    │
│                          │
│ The document discusses...│
└──────────────────────────┘
```

- Show placeholder until enough content
- Reveal in chunks for smoother reading

### Skeleton → Content

```
┌──────────────────────────┐     ┌──────────────────────────┐
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │     │ Introduction             │
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓       │  →  │ This report covers...    │
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    │     │ Key findings include:    │
└──────────────────────────┘     └──────────────────────────┘
```

- Pre-render expected shape
- Replace skeleton with real content
- Reduces layout shift

## Visual Indicators

### Cursor Styles

```
█  Block cursor (classic terminal)
|  Line cursor (text editor)
●  Dot cursor (minimal)
▋  Half-block cursor (modern)
```

### Animation States

- **Typing**: Cursor visible, blinking or solid
- **Paused**: Cursor visible, no blink, "paused" indicator
- **Complete**: Cursor hidden, content stable
- **Error**: Red indicator, error message appended

### Container Indicators

```
┌─ Generating ─────────────────┐
│ Content streams here...      │
│                          ... │ ← Activity dots
└──────────────────────────────┘
```

## Implementation Patterns

### Pattern A: Simple Token Append

```
// Pseudocode

StreamingText:
  content: string = ""
  isGenerating: boolean = false

  onToken(token):
    content += token

  render:
    <Container>
      <Text>{content}</Text>
      {isGenerating && <Cursor />}
    </Container>
```

### Pattern B: Smooth Token Rendering

```
// Batch tokens to reduce render frequency

StreamingText:
  displayContent: string = ""
  buffer: string = ""

  onToken(token):
    buffer += token

  // Flush buffer on interval (e.g., 50ms) or buffer size
  flushBuffer():
    displayContent += buffer
    buffer = ""

  render:
    <Container>
      <Text>{displayContent}</Text>
      {isGenerating && <Cursor />}
    </Container>
```

### Pattern C: Markdown Streaming

```
// Handle markdown as it streams

MarkdownStream:
  rawContent: string = ""

  onToken(token):
    rawContent += token

  render:
    // Parse complete markdown blocks, hold incomplete ones
    const { complete, partial } = parseMarkdown(rawContent)

    <Container>
      <Markdown>{complete}</Markdown>
      <RawText>{partial}</RawText>
      {isGenerating && <Cursor />}
    </Container>
```

### Pattern D: Code Block Streaming

```
// Special handling for code blocks

CodeStream:
  content: string = ""
  inCodeBlock: boolean = false

  onToken(token):
    content += token
    inCodeBlock = detectCodeBlock(content)

  render:
    if inCodeBlock:
      <CodeEditor
        value={content}
        language={detectLanguage(content)}
        streaming={true}
      />
    else:
      <Text>{content}</Text>
```

## Performance Considerations

### Token Batching

Don't render on every single token—batch updates:

```
// Bad: renders 100 times for 100 tokens
tokens.forEach(token => setContent(c => c + token))

// Good: batches into ~20 renders
const BATCH_INTERVAL = 50 // ms
let batch = ""
tokens.forEach(token => batch += token)
setInterval(() => {
  if (batch) {
    setContent(c => c + batch)
    batch = ""
  }
}, BATCH_INTERVAL)
```

### Virtual Scrolling

For very long outputs:

```
// Only render visible portion
<VirtualList
  items={contentLines}
  renderItem={(line) => <Line>{line}</Line>}
  autoScroll={isGenerating}
/>
```

### Debounced Parsing

For rich content (markdown, code highlighting):

```
// Don't re-parse on every token
const parsedContent = useDebouncedMemo(
  () => parseMarkdown(rawContent),
  [rawContent],
  100 // ms
)
```

## Edge Cases

### Stop Generation

```
<Container>
  <StreamingContent content={content} />
  {isGenerating && (
    <StopButton onClick={stop}>
      ■ Stop generating
    </StopButton>
  )}
</Container>
```

- Always provide escape hatch
- Clearly indicate what will happen (content preserved)

### Connection Loss

```
<Container>
  <Text>{content}</Text>
  {connectionLost && (
    <Warning>
      Connection lost.
      <Button onClick={resume}>Resume</Button>
      <Button onClick={retry}>Retry from start</Button>
    </Warning>
  )}
</Container>
```

- Preserve partial content
- Offer resume if possible

### Rate Limiting

```
<Container>
  <Text>{content}</Text>
  {rateLimited && (
    <Notice>
      Slowing down... will continue in {countdown}s
    </Notice>
  )}
</Container>
```

- Don't lose content on rate limit
- Show clear status and countdown

### Empty Response

```
if (isComplete && !content) {
  <EmptyState>
    No response generated. This might mean:
    • The query was too vague
    • Content was filtered
    <Button onClick={retry}>Try again</Button>
  </EmptyState>
}
```

## Accessibility

- Announce streaming start: "Generating response"
- Announce completion: "Response complete"
- Don't auto-scroll aggressively (disorienting for screen readers)
- Provide "skip to end" option for long streams
- Ensure stop button is keyboard accessible
