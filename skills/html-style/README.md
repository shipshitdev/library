# html-style

Apply opinionated styling to barebones HTML.

## When to Use

- User has plain/unstyled HTML
- "style this", "make this look good"
- After using `quick-view` or `table-filters`

## What It Does

1. Reads the HTML
2. Injects `base.css` styles
3. Adds appropriate classes
4. Handles dark mode

## Key Classes

| Class | Effect |
|-------|--------|
| `.stale` `.warm` `.pending` | Status text colors |
| `.trend-up` `.trend-down` | Green/red with arrows |
| `.status-success` `.status-error` | Colored pills |
| `.section-header` | Dark bar divider |

## Resources

- `assets/base.css` - Full stylesheet
- `references/style-guide.md` - Detailed patterns
