# Status Indicator Patterns

For AI interfaces with background processing or polling states.

## Table of Contents

- [When to Use](#when-to-use)
- [Indicator Types](#indicator-types)
- [Placement Strategies](#placement-strategies)
- [Implementation Patterns](#implementation-patterns)
- [Notification Patterns](#notification-patterns)
- [Edge Cases](#edge-cases)

## When to Use

Use status indicators when:

- Work happens in the background
- User can continue other tasks while waiting
- Process duration is unpredictable
- User needs awareness without blocking interaction

Examples:

- "Syncing your data..."
- "Indexing files in background"
- "Waiting for API response"
- "Training model (this may take a while)"

## Indicator Types

### Spinner / Loader

```
⟳ Processing...
```

- Simple, universally understood
- No progress information
- Best for: Unknown duration, quick tasks

### Pulsing Dot

```
● Syncing
```

- Subtle, non-intrusive
- Shows activity without demanding attention
- Best for: Ambient background status

### Progress Ring / Bar

```
◐ 45% complete
━━━━━━━━░░░░░░░░
```

- Shows measurable progress
- Best for: Known duration/size, file uploads

### Status Badge

```
[Processing] Document.pdf
```

- Inline with content
- Best for: Per-item status in lists

### Toast / Banner

```
┌──────────────────────────────────┐
│ ● Background sync in progress... │
└──────────────────────────────────┘
```

- Temporary, dismissible
- Best for: Temporary states, notifications

## Placement Strategies

### Global Status Bar

```
┌────────────────────────────────────────┐
│  App Header                    ● Sync  │ ← Top-right badge
├────────────────────────────────────────┤
│                                        │
│  Main Content                          │
│                                        │
└────────────────────────────────────────┘
```

- Always visible
- Doesn't interrupt flow
- Click to expand details

### Contextual Inline

```
┌─ Files ────────────────────────────────┐
│  📄 Report.pdf           ✓ Ready       │
│  📄 Analysis.xlsx        ⟳ Processing  │ ← Per-item status
│  📄 Summary.doc          ✓ Ready       │
└────────────────────────────────────────┘
```

- Status next to affected item
- Clear relationship
- Good for lists/tables

### Floating Indicator

```
                    ┌───────────────────┐
                    │ ● 3 tasks running │
                    │   View details →  │
                    └───────────────────┘
Main Content
```

- Doesn't take layout space
- Can be minimized
- Good for non-blocking background tasks

### Full-Screen Overlay (Use Sparingly)

```
┌────────────────────────────────────────┐
│                                        │
│         ⟳ Preparing workspace...       │
│                                        │
│         This may take a minute         │
│                                        │
└────────────────────────────────────────┘
```

- Blocks interaction
- Only for critical initialization
- Must have timeout/escape

## Implementation Patterns

### Pattern A: Background Task Manager

```
// Pseudocode

TaskManager:
  tasks: Task[] = []

  Task:
    id: string
    label: string
    status: pending | running | complete | error
    progress?: number

  addTask(task):
    tasks.push(task)

  updateTask(id, updates):
    tasks.find(t => t.id === id).merge(updates)

  render:
    <FloatingPanel>
      <Header>
        {runningCount} task(s) running
        <CollapseButton />
      </Header>
      {expanded && (
        <TaskList>
          {tasks.map(task => (
            <TaskRow status={task.status}>
              <Label>{task.label}</Label>
              {task.progress && <ProgressBar value={task.progress} />}
              {task.status === "error" && <RetryButton />}
            </TaskRow>
          ))}
        </TaskList>
      )}
    </FloatingPanel>
```

### Pattern B: Polling Status

```
// For async operations that require polling

PollingStatus:
  status: idle | polling | success | error
  lastCheck: timestamp

  startPolling(interval = 2000):
    status = "polling"
    poll()

  poll():
    result = await checkStatus()
    lastCheck = now()

    if result.complete:
      status = "success"
      onComplete(result)
    else if result.error:
      status = "error"
    else:
      setTimeout(poll, interval)

  render:
    switch status:
      case "polling":
        <Badge>
          <Spinner />
          Checking... (last: {timeAgo(lastCheck)})
        </Badge>
      case "success":
        <Badge success>Complete</Badge>
      case "error":
        <Badge error>
          Failed <RetryButton onClick={startPolling} />
        </Badge>
```

### Pattern C: Optimistic UI with Background Sync

```
// Show immediate feedback, sync in background

OptimisticAction:
  localState: any
  syncStatus: synced | syncing | error

  performAction(action):
    // Update UI immediately
    localState = applyAction(localState, action)
    syncStatus = "syncing"

    // Sync in background
    try:
      await syncToServer(action)
      syncStatus = "synced"
    catch:
      syncStatus = "error"
      // Optionally revert localState

  render:
    <Container>
      <Content data={localState} />
      <SyncIndicator status={syncStatus} />
    </Container>
```

## Notification Patterns

### Completion Notifications

```
// When background task completes

onTaskComplete(task):
  if document.hidden:
    // User not looking - use system notification
    showSystemNotification(`${task.label} complete`)
  else if !taskPanelVisible:
    // User in app but not watching - use toast
    showToast(`${task.label} complete`, { action: "View" })
  else:
    // User watching - just update status
    updateTaskStatus(task.id, "complete")
```

### Error Notifications

```
// Errors need more attention than success

onTaskError(task, error):
  // Always show prominent error
  showToast({
    type: "error",
    title: `${task.label} failed`,
    message: error.message,
    actions: [
      { label: "Retry", onClick: () => retryTask(task) },
      { label: "Dismiss", onClick: () => dismissTask(task) }
    ],
    persistent: true  // Don't auto-dismiss errors
  })
```

## Edge Cases

### Multiple Concurrent Tasks

```
<StatusBar>
  {tasks.length === 1 ? (
    <SingleTaskView task={tasks[0]} />
  ) : (
    <MultiTaskSummary count={tasks.length} onClick={showDetails} />
  )}
</StatusBar>
```

### Stale Status

```
// Detect stuck states

if (task.status === "running" && now() - task.lastUpdate > STALE_THRESHOLD):
  <TaskRow>
    <Label>{task.label}</Label>
    <Warning>
      No updates for {timeAgo(task.lastUpdate)}
      <Button onClick={checkStatus}>Check</Button>
      <Button onClick={cancel}>Cancel</Button>
    </Warning>
  </TaskRow>
```

### Reconnection

```
// After connection loss

<ConnectionStatus>
  {isReconnecting && (
    <Banner>
      <Spinner /> Reconnecting...
    </Banner>
  )}
  {justReconnected && (
    <Banner success>
      ✓ Reconnected. Syncing {pendingChanges} changes...
    </Banner>
  )}
</ConnectionStatus>
```

### Long-Running Background Tasks

```
// Tasks that take minutes/hours

<LongTaskStatus task={task}>
  <Title>{task.label}</Title>
  <Progress value={task.progress} />
  <Estimate>~{task.estimatedRemaining} remaining</Estimate>

  <Options>
    <Checkbox checked={notifyOnComplete}>
      Notify me when complete
    </Checkbox>
    <Button onClick={runInBackground}>
      Continue in background
    </Button>
  </Options>
</LongTaskStatus>
```

## Accessibility

- Use `aria-live="polite"` for status updates
- `aria-busy="true"` on elements being processed
- Don't use only color to indicate status
- Ensure spinners have accessible labels
- Provide text alternatives for all indicators
- Allow users to pause/hide animations
