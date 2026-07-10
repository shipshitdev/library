# shadcn/ui Setup — Additional Examples

## Dependency Versions Example

```json
{
  "dependencies": {
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0",
    "lucide-react": "^0.400.0"
  },
  "devDependencies": {
    "tailwindcss": "^4.0.0",
    "@tailwindcss/postcss": "^4.0.0"
  }
}
```

## Generated File Structure

```
project/
├── src/
│   ├── app/
│   │   └── globals.css           # Tailwind v4 + shadcn theme
│   ├── components/
│   │   └── ui/                   # shadcn components
│   │       ├── button.tsx
│   │       ├── card.tsx
│   │       └── ...
│   └── lib/
│       └── utils.ts              # cn() utility
├── components.json               # shadcn config
└── postcss.config.mjs            # PostCSS with @tailwindcss/postcss
```

## components.json Full Example

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "default",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "",
    "css": "src/app/globals.css",
    "baseColor": "zinc",
    "cssVariables": true,
    "prefix": ""
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  },
  "iconLibrary": "lucide"
}
```

**Note**: The `tailwind.config` is empty because we use CSS-first configuration in v4.

## Using Components Example

```tsx
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export function MyComponent() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Welcome</CardTitle>
      </CardHeader>
      <CardContent>
        <Button>Click me</Button>
      </CardContent>
    </Card>
  );
}
```

## Dark Mode — Manual Toggle Provider

```tsx
// Add to layout.tsx or a theme provider
'use client';

import { useEffect, useState } from 'react';

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark');
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}
```

Update CSS to use class-based dark mode:

```css
/* Replace @media (prefers-color-scheme: dark) with: */
.dark {
  --color-background: hsl(222.2 84% 4.9%);
  /* ... rest of dark theme variables */
}
```
