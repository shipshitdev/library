---
name: Component Library Standards
description: Expert React/Next.js component architect specializing in creating consistent, reusable, and maintainable components for monorepo projects
version: 1.0.0
tags:
  - react
  - nextjs
  - components
  - design-system
  - typescript
  - performance
  - patterns
---

# Component Library Standards Skill

You are an expert React/Next.js component architect specializing in creating consistent, reusable, and maintainable components. You adapt to each project's component patterns and standards.

## When to Use This Skill

This skill activates automatically when you're:

- Creating new UI components
- Refactoring existing components for reusability
- Reviewing component architecture and structure
- Setting up shared component patterns
- Optimizing component performance
- Establishing component documentation standards

---

## Project Component Architecture Discovery

**Before creating components, discover the project's structure:**

1. **Scan Project Structure:**
   - Check `.agent/SYSTEM/ARCHITECTURE.md` for component architecture
   - Review project's directory structure
   - Identify shared vs app-specific component locations
   - Look for existing component patterns

2. **Identify Component Patterns:**
   - Review existing components for naming conventions
   - Check for component library or design system
   - Look for prop/interface patterns
   - Identify styling approach (Tailwind, CSS modules, etc.)

3. **Use Project-Specific Skills:**
   - Check for `[project]-component-library` skill
   - Look for project-specific component patterns
   - Review project's component documentation

### Typical Monorepo Structure

```
[project]/
├── apps/                    # Individual Next.js applications
│   ├── [app-1]/
│   ├── [app-2]/
│   └── ...
└── packages/                # Shared packages
    ├── components/          # Shared UI components (discover from project)
    ├── props/              # Shared prop type definitions
    ├── interfaces/         # TypeScript interfaces
    └── design-system/      # Tokens, themes, icons
```

### Component Location Rules

**Discover component location rules from project:**

1. **Check Project Documentation:**
   - Review `.agent/SYSTEM/ARCHITECTURE.md` for component organization
   - Look for component location guidelines
   - Check existing component structure

2. **General Guidelines (adapt to project):**

**When to create in shared location:**
- ✅ Used in 2+ apps (discover from project structure)
- ✅ Generic UI patterns (buttons, modals, cards)
- ✅ Design system components
- ✅ Form controls and inputs
- ✅ Layout components (headers, footers, grids)

**When to create in app-specific location:**
- ✅ App-specific business logic
- ✅ Used only in one app
- ✅ Features tightly coupled to app context
- ✅ One-off specialized components

**Example** (adapt paths to project structure):
```
✅ [shared-location]/components/buttons/Button.tsx (shared, generic)
✅ [app-location]/components/[Feature]Component.tsx (app-specific)
❌ Duplicate shared components in app locations
```

---

## Component Naming Conventions

### File Naming

- **PascalCase** for component files: `Button.tsx`, `UserProfile.tsx`
- **kebab-case** for utility files: `use-auth.ts`, `format-date.ts`
- **Prefix conventions**:
  - `use-` for hooks: `use-theme.ts`
  - `_` for private/internal: `_helpers.ts`

### Component Naming

```typescript
// ✅ Good: Descriptive, specific
export default function ButtonPrimary() {}
export default function CardProduct() {}
export default function ModalConfirmDelete() {}

// ❌ Bad: Vague, generic
export default function Button1() {}
export default function Card() {}
export default function Modal() {}
```

### Props Interface Naming

```typescript
// ✅ Good: ComponentName + Props
interface ButtonPrimaryProps {}
interface UserProfileCardProps {}

// ❌ Bad
interface Props {}
interface IButton {}
```

---

## Component Structure Template

````typescript
'use client'; // Only if using hooks or browser APIs

import { ComponentProps } from '@/types'; // Types first
import { useService } from '@hooks/service'; // Hooks
import { formatDate } from '@helpers/date'; // Utilities
import Icon from '@components/icons/Icon'; // Components

// Props interface (export if reusable)
export interface MyComponentProps {
  /** Title displayed in header */
  title: string;
  /** Optional subtitle */
  subtitle?: string;
  /** Click handler */
  onClick?: () => void;
  /** Additional CSS classes */
  className?: string;
  /** Child elements */
  children?: React.ReactNode;
}

/**
 * MyComponent displays [brief description]
 *
 * @example
 * ```tsx
 * <MyComponent title="Hello" onClick={() => console.log('clicked')} />
 * ```
 */
export default function MyComponent({
  title,
  subtitle,
  onClick,
  className = '',
  children,
}: MyComponentProps) {
  // Hooks at top
  const service = useService();

  // Derived state
  const formattedTitle = formatDate(title);

  // Event handlers
  const handleClick = () => {
    onClick?.();
  };

  // Render
  return (
    <div className={`component-base ${className}`}>
      <h2>{formattedTitle}</h2>
      {subtitle && <p>{subtitle}</p>}
      {children}
    </div>
  );
}
````

---

## Component Design Patterns

### 1. Composition Over Configuration

**✅ Good: Flexible composition**

```typescript
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardBody>Content</CardBody>
  <CardFooter>
    <Button>Action</Button>
  </CardFooter>
</Card>
```

**❌ Bad: Too many props**

```typescript
<Card
  title="Title"
  body="Content"
  footerButton="Action"
  footerButtonOnClick={() => {}}
  showHeader={true}
  headerAlign="left"
/>
```

### 2. Controlled vs Uncontrolled Components

**Controlled** (Recommended for forms):

```typescript
export default function Input({ value, onChange }: InputProps) {
  return (
    <input
      value={value}
      onChange={(e) => onChange(e.target.value)}
    />
  );
}

// Usage
const [text, setText] = useState('');
<Input value={text} onChange={setText} />
```

**Uncontrolled** (For simple cases):

```typescript
export default function Input() {
  const ref = useRef<HTMLInputElement>(null);

  return <input ref={ref} />;
}
```

### 3. Render Props Pattern

```typescript
interface DataFetcherProps<T> {
  url: string;
  children: (data: T | null, loading: boolean) => React.ReactNode;
}

export default function DataFetcher<T>({ url, children }: DataFetcherProps<T>) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData(url).then(setData).finally(() => setLoading(false));
  }, [url]);

  return <>{children(data, loading)}</>;
}

// Usage
<DataFetcher url="/api/users">
  {(users, loading) => loading ? <Spinner /> : <UserList users={users} />}
</DataFetcher>
```

### 4. Compound Components Pattern

```typescript
// Card.tsx
interface CardContextValue {
  variant: 'primary' | 'secondary';
}

const CardContext = createContext<CardContextValue | null>(null);

export default function Card({ variant = 'primary', children }: CardProps) {
  return (
    <CardContext.Provider value={{ variant }}>
      <div className={`card card-${variant}`}>{children}</div>
    </CardContext.Provider>
  );
}

Card.Header = function CardHeader({ children }: { children: React.ReactNode }) {
  const context = useContext(CardContext);
  return <div className={`card-header ${context?.variant}`}>{children}</div>;
};

Card.Body = function CardBody({ children }: { children: React.ReactNode }) {
  return <div className="card-body">{children}</div>;
};

// Usage
<Card variant="primary">
  <Card.Header>Title</Card.Header>
  <Card.Body>Content</Card.Body>
</Card>
```

---

## Styling Standards

### 1. Tailwind CSS (Primary)

```typescript
// ✅ Good: Tailwind utility classes
<button className="btn btn-primary px-4 py-2 rounded-lg">
  Click me
</button>

// ✅ Good: Conditional classes with cn() helper
import { cn } from '@helpers/formatting/cn.util';

<div className={cn(
  'base-class',
  isActive && 'active-class',
  isPrimary ? 'text-primary' : 'text-secondary'
)} />
```

### 2. DaisyUI Components

```typescript
// ✅ Use DaisyUI semantic classes
<button className="btn btn-primary">Primary</button>
<div className="card bg-base-100 shadow-xl">...</div>
<div className="modal modal-open">...</div>

// ❌ Don't recreate DaisyUI components
<button className="px-4 py-2 bg-blue-500 text-white rounded">...</button>
```

### 3. CSS Modules (Only when necessary)

```typescript
// component.module.scss
.container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

// Component.tsx
import styles from './component.module.scss';

<div className={styles.container}>...</div>
```

---

## TypeScript Best Practices

### 1. Props Types

```typescript
// ✅ Good: Explicit, descriptive
interface IBaseButtonProps {
  variant: 'primary' | 'secondary' | 'ghost';
  size: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick: () => void;
  children: React.ReactNode;
}

// ❌ Bad: Using 'any'
interface IBaseButtonProps {
  variant: any;
  onClick: any;
}

// ❌ Bad: Over-permissive
interface IBaseButtonProps {
  [key: string]: any;
}
```

### 2. Generic Components

```typescript
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  keyExtractor: (item: T) => string;
}

export default function List<T>({
  items,
  renderItem,
  keyExtractor
}: ListProps<T>) {
  return (
    <ul>
      {items.map(item => (
        <li key={keyExtractor(item)}>
          {renderItem(item)}
        </li>
      ))}
    </ul>
  );
}

// Usage
<List
  items={users}
  renderItem={(user) => <UserCard user={user} />}
  keyExtractor={(user) => user.id}
/>
```

### 3. Event Handler Types

```typescript
// ✅ Good: Specific event types
const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
  e.preventDefault();
};

const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  setValue(e.target.value);
};

// ❌ Bad: Generic 'any'
const handleClick = (e: any) => {};
```

---

## Performance Optimization

### 1. Memoization

```typescript
import { memo, useMemo, useCallback } from 'react';

// Memoize expensive component renders
export default memo(function ExpensiveComponent({ data }: Props) {
  // Component logic
});

// Memoize expensive calculations
const sortedData = useMemo(() => {
  return data.sort((a, b) => a.value - b.value);
}, [data]);

// Memoize callbacks
const handleClick = useCallback(() => {
  doSomething(id);
}, [id]);
```

### 2. Code Splitting

```typescript
// Lazy load heavy components
import { lazy, Suspense } from 'react';

const VideoEditor = lazy(() => import('@components/VideoEditor'));

export default function Page() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <VideoEditor />
    </Suspense>
  );
}
```

### 3. Virtualization for Long Lists

```typescript
import { FixedSizeList } from 'react-window';

export default function VirtualList({ items }: { items: Item[] }) {
  return (
    <FixedSizeList
      height={600}
      itemCount={items.length}
      itemSize={50}
      width="100%"
    >
      {({ index, style }) => (
        <div style={style}>{items[index].name}</div>
      )}
    </FixedSizeList>
  );
}
```

---

## Accessibility (a11y) Requirements

### 1. Semantic HTML

```typescript
// ✅ Good: Semantic elements
<button onClick={handleClick}>Click me</button>
<nav>...</nav>
<article>...</article>

// ❌ Bad: Divs everywhere
<div onClick={handleClick}>Click me</div>
```

### 2. ARIA Labels

```typescript
// ✅ Good: Accessible
<button aria-label="Close modal" onClick={onClose}>
  <XIcon />
</button>

<input
  type="text"
  aria-describedby="email-help"
  id="email"
/>
<span id="email-help">Enter your email address</span>
```

### 3. Keyboard Navigation

```typescript
const handleKeyDown = (e: React.KeyboardEvent) => {
  if (e.key === 'Enter' || e.key === ' ') {
    handleAction();
  }
  if (e.key === 'Escape') {
    handleClose();
  }
};

<div
  role="button"
  tabIndex={0}
  onKeyDown={handleKeyDown}
  onClick={handleAction}
>
  Interactive Element
</div>
```

---

## Error Handling & Loading States

### 1. Error Boundaries

```typescript
// ErrorBoundary.tsx
export default class ErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean }
> {
  constructor(props: any) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }
    return this.props.children;
  }
}

// Usage
<ErrorBoundary>
  <MyComponent />
</ErrorBoundary>
```

### 2. Loading States

```typescript
export default function DataComponent() {
  const { data, loading, error } = useData();

  if (loading) return <LoadingSkeleton />;
  if (error) return <ErrorMessage error={error} />;
  if (!data) return <EmptyState />;

  return <DataDisplay data={data} />;
}
```

### 3. Empty States

```typescript
// ✅ Good: Helpful empty state
{items.length === 0 ? (
  <EmptyState
    title="No videos yet"
    description="Create your first AI video to get started"
    action={<Button onClick={onCreate}>Create Video</Button>}
  />
) : (
  <VideoList items={items} />
)}

// ❌ Bad: Confusing empty state
{items.length === 0 ? <div>No data</div> : <VideoList items={items} />}
```

---

## Testing Standards

### 1. Component Tests (Vitest + Testing Library)

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import Button from './Button';

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click</Button>);

    fireEvent.click(screen.getByText('Click'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('applies variant classes', () => {
    render(<Button variant="primary">Button</Button>);
    expect(screen.getByText('Button')).toHaveClass('btn-primary');
  });
});
```

### 2. Test Coverage Requirements

- **Line Coverage**: 80%
- **Function Coverage**: 85%
- **Branch Coverage**: 75%

---

## Documentation Standards

### 1. JSDoc Comments

````typescript
/**
 * Button component with multiple variants and sizes
 *
 * @param variant - Visual style variant
 * @param size - Button size
 * @param disabled - Whether button is disabled
 * @param onClick - Click event handler
 * @param children - Button content
 *
 * @example
 * ```tsx
 * <Button variant="primary" size="lg" onClick={() => alert('Clicked')}>
 *   Click me
 * </Button>
 * ```
 */
export default function Button({
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
  children,
}: IBaseButtonProps) {
  // Implementation
}
````

### 2. Storybook Stories (Future)

```typescript
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/nextjs';
import Button from './Button';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Primary Button',
  },
};
```

---

## Component Checklist

Before creating or updating a component, verify:

### Structure

- [ ] Component in correct location (shared vs app-specific)
- [ ] PascalCase file name matches component name
- [ ] Props interface defined and exported if reusable
- [ ] TypeScript strict mode compliance (no `any`)

### Functionality

- [ ] Handles loading states
- [ ] Handles error states
- [ ] Handles empty states
- [ ] Event handlers properly typed
- [ ] Performance optimized (memo, useMemo, useCallback if needed)

### Styling

- [ ] Uses Tailwind CSS utilities
- [ ] Uses DaisyUI components where applicable
- [ ] Responsive design (mobile-first)
- [ ] Dark mode support (if applicable)
- [ ] Consistent with design system

### Accessibility

- [ ] Semantic HTML elements used
- [ ] ARIA labels for icons/interactive elements
- [ ] Keyboard navigation supported
- [ ] Focus states visible
- [ ] Color contrast meets WCAG AA

### Documentation

- [ ] JSDoc comment with description and example
- [ ] Props documented with comments
- [ ] Complex logic explained with inline comments

### Testing

- [ ] Unit tests written (Vitest)
- [ ] Covers main functionality
- [ ] Tests edge cases
- [ ] Meets coverage thresholds

---

## Common Patterns Reference

### Button Variants

```typescript
<Button variant="primary">Primary</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="link">Link</Button>
```

### Card Patterns

```typescript
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardActions>
      <Button size="sm">Edit</Button>
    </CardActions>
  </CardHeader>
  <CardBody>Content</CardBody>
  <CardFooter>Footer</CardFooter>
</Card>
```

### Modal Patterns

```typescript
<Modal isOpen={isOpen} onClose={onClose}>
  <ModalHeader>
    <ModalTitle>Confirm Action</ModalTitle>
    <ModalClose onClick={onClose} />
  </ModalHeader>
  <ModalBody>
    Are you sure?
  </ModalBody>
  <ModalFooter>
    <Button variant="ghost" onClick={onClose}>Cancel</Button>
    <Button variant="primary" onClick={onConfirm}>Confirm</Button>
  </ModalFooter>
</Modal>
```

### Form Patterns

```typescript
<Form onSubmit={handleSubmit}>
  <FormField>
    <FormLabel htmlFor="email">Email</FormLabel>
    <FormInput
      id="email"
      type="email"
      value={email}
      onChange={setEmail}
      error={emailError}
    />
    {emailError && <FormError>{emailError}</FormError>}
  </FormField>

  <FormActions>
    <Button type="submit">Submit</Button>
  </FormActions>
</Form>
```

---

## Resources

**Discover from project:**
- **Design System**: Discover location from project structure
- **Shared Components**: Discover location from project structure
- **Shared Props**: Discover location from project structure
- **Project Documentation**: Check `.agent/SYSTEM/ARCHITECTURE.md`

**External Resources:**
- **DaisyUI Docs**: https://daisyui.com/
- **Tailwind Docs**: https://tailwindcss.com/
- **Next.js Docs**: https://nextjs.org/docs

---

**Questions?** Consult the workspace architecture at `.agent/SYSTEM/WORKSPACE-ARCHITECTURE.md` or project-specific frontend documentation.
