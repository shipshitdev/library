# shadcn/ui Tailwind v4 Theme Token Reference

Full CSS token block for `src/app/globals.css` using Tailwind v4 CSS-first configuration.

```css
/* src/app/globals.css */
@import "tailwindcss";

@theme {
  /* Base colors */
  --color-background: hsl(0 0% 100%);
  --color-foreground: hsl(222.2 84% 4.9%);

  /* Card */
  --color-card: hsl(0 0% 100%);
  --color-card-foreground: hsl(222.2 84% 4.9%);

  /* Popover */
  --color-popover: hsl(0 0% 100%);
  --color-popover-foreground: hsl(222.2 84% 4.9%);

  /* Primary */
  --color-primary: hsl(222.2 47.4% 11.2%);
  --color-primary-foreground: hsl(210 40% 98%);

  /* Secondary */
  --color-secondary: hsl(210 40% 96.1%);
  --color-secondary-foreground: hsl(222.2 47.4% 11.2%);

  /* Muted */
  --color-muted: hsl(210 40% 96.1%);
  --color-muted-foreground: hsl(215.4 16.3% 46.9%);

  /* Accent */
  --color-accent: hsl(210 40% 96.1%);
  --color-accent-foreground: hsl(222.2 47.4% 11.2%);

  /* Destructive */
  --color-destructive: hsl(0 84.2% 60.2%);
  --color-destructive-foreground: hsl(210 40% 98%);

  /* Border & Input */
  --color-border: hsl(214.3 31.8% 91.4%);
  --color-input: hsl(214.3 31.8% 91.4%);
  --color-ring: hsl(222.2 84% 4.9%);

  /* Chart colors */
  --color-chart-1: hsl(12 76% 61%);
  --color-chart-2: hsl(173 58% 39%);
  --color-chart-3: hsl(197 37% 24%);
  --color-chart-4: hsl(43 74% 66%);
  --color-chart-5: hsl(27 87% 67%);

  /* Border radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;
  --radius-2xl: 1rem;
  --radius-full: 9999px;

  /* Sidebar (if using sidebar component) */
  --color-sidebar: hsl(0 0% 98%);
  --color-sidebar-foreground: hsl(240 5.3% 26.1%);
  --color-sidebar-primary: hsl(240 5.9% 10%);
  --color-sidebar-primary-foreground: hsl(0 0% 98%);
  --color-sidebar-accent: hsl(240 4.8% 95.9%);
  --color-sidebar-accent-foreground: hsl(240 5.9% 10%);
  --color-sidebar-border: hsl(220 13% 91%);
  --color-sidebar-ring: hsl(217.2 91.2% 59.8%);
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  @theme {
    --color-background: hsl(222.2 84% 4.9%);
    --color-foreground: hsl(210 40% 98%);
    --color-card: hsl(222.2 84% 4.9%);
    --color-card-foreground: hsl(210 40% 98%);
    --color-popover: hsl(222.2 84% 4.9%);
    --color-popover-foreground: hsl(210 40% 98%);
    --color-primary: hsl(210 40% 98%);
    --color-primary-foreground: hsl(222.2 47.4% 11.2%);
    --color-secondary: hsl(217.2 32.6% 17.5%);
    --color-secondary-foreground: hsl(210 40% 98%);
    --color-muted: hsl(217.2 32.6% 17.5%);
    --color-muted-foreground: hsl(215 20.2% 65.1%);
    --color-accent: hsl(217.2 32.6% 17.5%);
    --color-accent-foreground: hsl(210 40% 98%);
    --color-destructive: hsl(0 62.8% 30.6%);
    --color-destructive-foreground: hsl(210 40% 98%);
    --color-border: hsl(217.2 32.6% 17.5%);
    --color-input: hsl(217.2 32.6% 17.5%);
    --color-ring: hsl(212.7 26.8% 83.9%);
    --color-sidebar: hsl(240 5.9% 10%);
    --color-sidebar-foreground: hsl(240 4.8% 95.9%);
    --color-sidebar-primary: hsl(224.3 76.3% 48%);
    --color-sidebar-primary-foreground: hsl(0 0% 100%);
    --color-sidebar-accent: hsl(240 3.7% 15.9%);
    --color-sidebar-accent-foreground: hsl(240 4.8% 95.9%);
    --color-sidebar-border: hsl(240 3.7% 15.9%);
  }
}

/* Base styles */
* {
  border-color: var(--color-border);
}

body {
  background-color: var(--color-background);
  color: var(--color-foreground);
}
```
