# Universal Coding Standards

Standards that apply across all projects regardless of tech stack.

---

## Code Quality

### Never Use `any` Types

**WRONG:**

```typescript
function processData(data: any) {
  return data.map((item: any) => item.name);
}
```

**CORRECT:**

```typescript
interface DataItem {
  name: string;
  id: string;
}

function processData(data: DataItem[]): string[] {
  return data.map((item) => item.name);
}
```

---

### Use Path Aliases, Not Relative Paths

**WRONG:**

```typescript
import { Button } from "../../../components/ui/Button";
import { utils } from "../../lib/utils";
```

**CORRECT:**

```typescript
import { Button } from "@components/ui/Button";
import { utils } from "@lib/utils";
```

**WHY:** Path aliases:

- Make imports consistent and readable
- Prevent breakage when files are moved
- Enable better IDE autocomplete

---

### Never Use console.log in Production Code

**WRONG:**

```typescript
console.log("User created:", user);
console.error("Error:", error);
```

**CORRECT:**

```typescript
// Use project's logging service
logger.info("User created", { userId: user.id });
logger.error("Operation failed", { error });
```

---

### Never Create Inline Interfaces

**WRONG:**

```typescript
function Component({ title }: { title: string }) {}

interface LocalState { count: number; }
```

**CORRECT:**

```typescript
// In a dedicated types/interfaces file
export interface ComponentProps {
  title: string;
}

// In component file
import { ComponentProps } from "@types/component.types";

function Component({ title }: ComponentProps) {}
```

**WHY:** Centralized interfaces enable reuse and easier refactoring.

---

## Error Handling

### Always Handle Async Errors

**WRONG:**

```typescript
const result = await operation();
return result;
```

**CORRECT:**

```typescript
try {
  const result = await operation();
  return result;
} catch (error) {
  logger.error("Operation failed", { error });
  throw new Error("Operation failed");
}
```

---

### Use AbortController for Async React Effects

**WRONG:**

```typescript
useEffect(() => {
  const fetchData = async () => {
    const data = await service.getData();
    setData(data);
  };
  fetchData();
}, []);
```

**CORRECT:**

```typescript
useEffect(() => {
  const controller = new AbortController();

  const fetchData = async () => {
    try {
      const data = await service.getData({ signal: controller.signal });
      setData(data);
    } catch (error) {
      if (error.name === "AbortError") return;
      handleError(error);
    }
  };

  fetchData();

  return () => controller.abort();
}, []);
```

**WHY:** Prevents memory leaks and race conditions when components unmount.

---

## File Organization

### Edit Existing Files, Don't Create New Ones

**WRONG:** Creating `feature-service-new.ts` instead of editing `feature.service.ts`

**CORRECT:**

1. Search for existing implementations first
2. Edit existing files
3. Only create new files when explicitly needed

---

### Use Consistent Import Styles

Follow the project's established import order:

1. External packages (react, next, etc.)
2. Internal packages (@company/*)
3. Path aliases (@components/*, @lib/*)
4. Relative imports (same directory only)

---

## Documentation

### Never Create Root-Level Markdown Files

**ALLOWED at project root:**

- `README.md`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `LICENSE.md`

**Everything else:** Goes in a docs/ or .agents/ folder

---

### Don't Add Comments for Obvious Code

**WRONG:**

```typescript
// Increment the counter
counter++;

// Return the result
return result;
```

**CORRECT:**

```typescript
// Calculate compound interest using the formula A = P(1 + r/n)^(nt)
// This handles edge cases where rate or time could be zero
const compoundInterest = principal * Math.pow(1 + rate/n, n * time);
```

Only add comments for non-obvious logic or business rules.

---

## Git Practices

### Never Force Push to Main/Master

**FORBIDDEN:**

```bash
git push --force origin main
git push -f origin master
```

---

### Never Skip Pre-commit Hooks

**FORBIDDEN:**

```bash
git commit --no-verify
git commit -n
```

---

### Use Descriptive Commit Messages

**WRONG:**

```
fix
update
wip
```

**CORRECT:**

```
fix: resolve null pointer in user authentication flow
feat: add dark mode toggle to settings page
refactor: extract validation logic into shared utility
```

---

## Security

### Never Commit Secrets

**FORBIDDEN in git:**

- `.env` files with real values
- API keys
- Database credentials
- Private keys
- Tokens

**USE:** Environment variables, secret managers, or encrypted config.

---

### Validate All External Input

Always validate:

- User input from forms
- Query parameters
- Request bodies
- URL parameters
- File uploads

Never trust data from external sources.

---

## Performance

### Don't Premature Optimize

Focus on:

1. Correctness first
2. Readability second
3. Performance when measured

Only optimize when you have evidence of a bottleneck.

---

### Avoid N+1 Queries

**WRONG:**

```typescript
const users = await getUsers();
for (const user of users) {
  const posts = await getPostsForUser(user.id); // N queries!
}
```

**CORRECT:**

```typescript
const users = await getUsers();
const userIds = users.map(u => u.id);
const posts = await getPostsForUsers(userIds); // 1 query
```
