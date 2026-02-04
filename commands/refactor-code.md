# Code Refactoring Workflow

**Purpose:** Systematic approach to refactoring code safely

## When to Use

- Code is complex/hard to understand
- Duplicate code found
- Performance issues
- Need to improve maintainability
- Technical debt reduction

## Refactoring Steps

### Step 1: Identify the Problem

**Common Refactoring Triggers:**

```
- [ ] Function > 50 lines
- [ ] File > 300 lines
- [ ] Duplicate code (3+ instances)
- [ ] Complex conditionals (> 3 levels deep)
- [ ] Hard to test
- [ ] Hard to understand
- [ ] Performance bottleneck
- [ ] `any` types
```

### Step 2: Write Tests First

**CRITICAL: Test before refactoring!**

```typescript
// Write comprehensive tests for current behavior
describe('FeatureService', () => {
  it('should handle case 1', () => {
    // Test current behavior
  });

  it('should handle case 2', () => {
    // Test current behavior
  });

  it('should handle edge cases', () => {
    // Test current behavior
  });
});

// Run tests - they should all pass
npm test
```

### Step 3: Check Examples

```bash
# Find the right pattern
cat .agents/EXAMPLES/API/endpoint-crud.md
cat .agents/EXAMPLES/FRONTEND/component-pattern.md
cat .agents/EXAMPLES/API/service-factory.md
```

### Step 4: Make Small Changes

**Refactor incrementally:**

1. **Extract Function**

   ```typescript
   // Before
   async processVideo(data: VideoDto) {
     // 50 lines of processing logic
     // Complex validation
     // Multiple database calls
     // Error handling
   }

   // After
   async processVideo(data: VideoDto) {
     this.validateVideoData(data);
     const processed = await this.transformVideo(data);
     await this.saveVideo(processed);
     await this.notifyCompletion(processed);
   }

   private validateVideoData(data: VideoDto) {
     // Validation logic
   }

   private async transformVideo(data: VideoDto) {
     // Transformation logic
   }
   ```

2. **Extract Constants**

   ```typescript
   // Before
   if (size > 10485760) throw new Error("Too large");

   // After
   const MAX_VIDEO_SIZE = 10 * 1024 * 1024; // 10MB
   if (size > MAX_VIDEO_SIZE) throw new Error("Video too large");
   ```

3. **Replace `any` with Types**

   ```typescript
   // Before
   function process(data: any) {
     return data.items.map((item: any) => item.name);
   }

   // After
   interface ProcessData {
     items: Array<{ name: string; id: string }>;
   }

   function process(data: ProcessData): string[] {
     return data.items.map((item) => item.name);
   }
   ```

### Step 5: Run Tests After Each Change

```bash
# After EVERY change
npm test

# Verify behavior unchanged
npm test -- [specific-test-file]
```

### Step 6: Common Refactoring Patterns

#### Extract Service

```typescript
// Before: Controller with business logic
@Controller("videos")
export class VideosController {
  @Post()
  async create(@Body() data: CreateVideoDto) {
    // Lots of business logic here
    // Database operations
    // External API calls
    // Queue jobs
  }
}

// After: Thin controller, fat service
@Controller("videos")
export class VideosController {
  constructor(private readonly videosService: VideosService) {}

  @Post()
  async create(@Body() data: CreateVideoDto) {
    return this.videosService.create(data); // Delegate to service
  }
}
```

#### Extract Component

```typescript
// Before: Large component
export const Dashboard = () => {
  return (
    <div>
      {/* 200 lines of JSX */}
      {/* User profile section */}
      {/* Stats section */}
      {/* Recent activity section */}
    </div>
  );
};

// After: Extracted components
export const Dashboard = () => {
  return (
    <div>
      <UserProfile />
      <Stats />
      <RecentActivity />
    </div>
  );
};
```

#### Replace Conditionals with Polymorphism

```typescript
// Before: Complex conditionals
function getPrice(item: Item) {
  if (item.type === "video") {
    return item.duration * 0.1;
  } else if (item.type === "image") {
    return item.pixels * 0.001;
  } else if (item.type === "audio") {
    return item.duration * 0.05;
  }
}

// After: Strategy pattern
interface PricingStrategy {
  calculate(item: Item): number;
}

class VideoPricing implements PricingStrategy {
  calculate(item: Item) {
    return item.duration * 0.1;
  }
}

const strategies = {
  video: new VideoPricing(),
  image: new ImagePricing(),
  audio: new AudioPricing(),
};

function getPrice(item: Item) {
  return strategies[item.type].calculate(item);
}
```

### Step 7: Performance Refactoring

#### Database Queries

```typescript
// Before: N+1 queries
for (const video of videos) {
  video.user = await this.usersModel.findById(video.userId);
}

// After: Batch query
const userIds = videos.map((v) => v.userId);
const users = await this.usersModel.find({ _id: { $in: userIds } });
const userMap = new Map(users.map((u) => [u._id, u]));
videos.forEach((v) => (v.user = userMap.get(v.userId)));
```

#### React Re-renders

```typescript
// Before: Re-renders on every parent update
export const ExpensiveComponent = ({ data }) => {
  const processed = processData(data); // Expensive!
  return <div>{processed}</div>;
};

// After: Memoized
export const ExpensiveComponent = React.memo(({ data }) => {
  const processed = useMemo(() => processData(data), [data]);
  return <div>{processed}</div>;
});
```

### Step 8: Refactoring Checklist

```
Before starting:
- [ ] All tests passing
- [ ] Understanding what the code does
- [ ] Have example pattern to follow
- [ ] Committed current working code

During refactoring:
- [ ] Make one change at a time
- [ ] Run tests after each change
- [ ] Keep same public API
- [ ] Document why (not just what)

After refactoring:
- [ ] All tests still passing
- [ ] No behavior changes
- [ ] Code is more readable
- [ ] Performance same or better
- [ ] Documentation updated
```

### Step 9: Review Improvements

**Measure improvements:**

```
Before:
- Lines of code: 500
- Cyclomatic complexity: 25
- Test coverage: 45%
- `any` types: 12

After:
- Lines of code: 350 (-30%)
- Cyclomatic complexity: 8 (-68%)
- Test coverage: 75% (+30%)
- `any` types: 0 (✅)
```

### Step 10: Document

```bash
# Create session entry
cat >> .agents/SESSIONS/$(date +%Y-%m-%d).md << EOF

## Refactoring: [Component/Service Name]

**Reason:** [Why refactoring was needed]

**Changes:**
- Extracted X functions
- Replaced Y conditionals
- Removed Z duplicate code
- Eliminated all \`any\` types

**Results:**
- Reduced complexity by X%
- Improved test coverage to Y%
- Performance improved by Z%

**Files Changed:**
- [list of files]

**Tests:** All passing ✅
EOF
```

## Red Flags (Stop and Reconsider)

```
- Behavior changes during refactoring
- Tests start failing
- Need to change public API
- Unclear what code does
- No test coverage to verify
- Affects multiple projects
```

## Safe Refactoring Rules

1. **Always have tests first**
2. **One change at a time**
3. **Run tests after each change**
4. **Keep same behavior**
5. **Don't change public API**
6. **Commit working states**
7. **Document why, not just what**

## Quick Wins

**Low-risk, high-value refactorings:**

1. Replace `any` with proper types
2. Extract magic numbers to constants
3. Extract duplicate code to functions
4. Add missing error handling
5. Add organization/isDeleted filters
6. Rename unclear variables
7. Add TypeScript return types

---

**Remember:** Refactoring = Behavior stays same, structure improves. If behavior changes, it's not refactoring!
