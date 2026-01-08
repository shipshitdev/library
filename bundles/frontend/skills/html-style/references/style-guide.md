# Style Guide Reference

## Table of Contents

1. [Base Layout](#base-layout)
2. [Colors](#colors)
3. [Typography](#typography)
4. [Tables](#tables)
5. [Tags & Pills](#tags--pills)
6. [Status Indicators](#status-indicators)
7. [Stat Boxes](#stat-boxes)
8. [Interactive Elements](#interactive-elements)
9. [Section Headers](#section-headers)
10. [Dark Mode](#dark-mode)

---

## Base Layout

```css
* { box-sizing: border-box; }
body {
    max-width: 900px;
    margin: 40px auto;
    padding: 0 20px;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #fff;
    color: #1a1a1a;
    line-height: 1.5;
}
```

**Width tiers:**

- `900px` - content pages (outreach, drafts)
- `1000px` - table-heavy pages
- `1400px` - two-panel dashboards

---

## Colors

### CSS Variables

```css
:root {
    /* Semantic backgrounds */
    --success-bg: #dcfce7;
    --success-text: #166534;
    --success-accent: #22c55e;

    --info-bg: #dbeafe;
    --info-text: #1e40af;
    --info-accent: #3b82f6;

    --warning-bg: #fef3c7;
    --warning-text: #854d0e;
    --warning-accent: #f97316;

    --error-bg: #fee2e2;
    --error-text: #991b1b;
    --error-accent: #ef4444;

    /* Border radius */
    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 12px;
    --radius-pill: 20px;
}
```

### Status Text (inline)

```css
.stale { color: #c00; font-weight: bold; }
.warm { color: #080; }
.pending { color: #f90; font-weight: bold; }
```

### Trend Colors

```css
.trend-up { color: #22c55e; }
.trend-up::after { content: ' ↑'; }
.trend-down { color: #ef4444; }
.trend-down::after { content: ' ↓'; }
```

---

## Typography

```css
h1 { border-bottom: 2px solid #333; padding-bottom: 10px; }
h2 { color: #333; margin-top: 32px; border-bottom: 1px solid #ccc; padding-bottom: 8px; }
h3 { color: #333; margin-top: 24px; }

/* Monospace for code/data */
code, pre, .mono {
    font-family: 'SF Mono', Monaco, monospace;
}

pre {
    white-space: pre-wrap;
    background: #f5f5f5;
    padding: 12px;
    margin: 8px 0;
    border-left: 3px solid #333;
    border-radius: var(--radius-md);
}
```

---

## Tables

### Default (minimal)

```css
table { border-collapse: collapse; width: 100%; margin: 16px 0; }
th, td { padding: 8px; text-align: left; border-bottom: 1px solid #e5e5e5; }
th { font-weight: 600; color: #666; font-size: 14px; }
```

### Sortable Headers

```css
th.sortable a {
    cursor: pointer;
    text-decoration: none;
    color: inherit;
}
th.sorted { font-weight: bold; }
/* Append ▼ to sorted column text */
```

### Styled Table (opt-in)

```css
.table-styled td.positive { color: var(--success-accent); }
.table-styled td.negative { color: var(--error-accent); }
.table-styled tr:hover { background: #f9f9f9; }
.table-styled .highlight { background: var(--warning-bg); }
```

---

## Tags & Pills

### Category Tags

For categorizing items (group, DM, money, etc.)

```css
.tag {
    display: inline-block;
    padding: 2px 8px;
    border-radius: var(--radius-sm);
    font-size: 0.8em;
    margin-left: 8px;
}
.tag-group { background: #e3f2fd; color: #1565c0; }
.tag-dm { background: #f3e5f5; color: #7b1fa2; }
.tag-money { background: #fff3e0; color: #e65100; }
```

### Status Pills

For state indicators (Paid, Failed, Pending)

```css
.status {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 12px;
    border-radius: var(--radius-pill);
    font-size: 0.85em;
    color: white;
}
.status-success { background: var(--success-accent); }
.status-error { background: var(--error-accent); }
.status-pending { background: var(--warning-accent); }
.status-info { background: var(--info-accent); }
```

### Filter Pills

For toggleable filters

```css
.filter {
    display: inline-block;
    padding: 6px 12px;
    border-radius: var(--radius-pill);
    border: 1px solid #e5e5e5;
    background: white;
    cursor: pointer;
    text-decoration: none;
    color: #1a1a1a;
}
.filter.active {
    background: #1a1a1a;
    color: white;
    border-color: #1a1a1a;
}
```

### Time Filter Pills

```css
.pill {
    padding: 6px 12px;
    border-radius: var(--radius-sm);
    text-decoration: none;
    color: #666;
}
.pill.active {
    background: #333;
    color: white;
}
```

---

## Status Indicators

### Inline Status Text

```html
<span class="stale">STALE: needs response</span>
<span class="warm">Active conversation</span>
<span class="pending">Waiting for reply</span>
```

### Status Cards (full-width)

```css
.card-success {
    background: var(--success-bg);
    border-radius: var(--radius-lg);
    padding: 16px;
}
.card-success .title { color: var(--success-text); }

.card-error {
    background: var(--error-bg);
    border-radius: var(--radius-lg);
    padding: 16px;
}
.card-error .title { color: var(--error-text); }
```

---

## Stat Boxes

```css
.stat {
    display: inline-block;
    margin: 8px 24px 8px 0;
}
.stat-value {
    font-size: 28px;
    font-weight: bold;
}
.stat-label {
    font-size: 12px;
    color: #666;
}
```

**Usage:**

```html
<div class="stat">
    <div class="stat-value">8,017</div>
    <div class="stat-label">Total Items</div>
</div>
```

---

## Interactive Elements

### Collapsible Sections

```css
details {
    margin: 20px 0;
    padding-bottom: 20px;
    border-bottom: 1px solid #eee;
}
summary {
    cursor: pointer;
    font-size: 1.1em;
    font-weight: 500;
}
```

### Contenteditable Drafts

```html
<pre contenteditable="true"
     data-thread-id="tg:dm:username"
     data-original="original text"
     onblur="saveDraft(this)">editable draft</pre>
```

```javascript
function saveDraft(el) {
    localStorage.setItem('draft:' + el.dataset.threadId, el.textContent);
}
function restoreDrafts() {
    document.querySelectorAll('[data-thread-id]').forEach(el => {
        const saved = localStorage.getItem('draft:' + el.dataset.threadId);
        if (saved) el.textContent = saved;
    });
}
document.addEventListener('DOMContentLoaded', restoreDrafts);
```

### Copy Button

```javascript
function copyToClipboard(text, btn) {
    navigator.clipboard.writeText(text).then(() => {
        btn.textContent = 'Copied!';
        setTimeout(() => btn.textContent = 'Copy', 1500);
    });
}
```

```css
button, .btn {
    cursor: pointer;
    padding: 4px 12px;
    border-radius: var(--radius-md);
    border: 1px solid #e5e5e5;
    background: white;
}
button:hover, .btn:hover {
    background: #f5f5f5;
}
```

### Deep Links

```html
<a href="tg://resolve?domain=username">Open Telegram</a>
<a href="sms:+14155551234">Send SMS</a>
```

---

## Section Headers

```css
.section-header {
    background: #333;
    color: white;
    padding: 10px 15px;
    margin: 30px 0 20px 0;
    border-radius: var(--radius-md);
}
```

**Usage with emoji prefix:**

```html
<div class="section-header">🔴 URGENT - Needs Action</div>
<div class="section-header">🟠 PENDING - Follow Up</div>
<div class="section-header">🟡 OPPORTUNITY - Proactive</div>
```

---

## Dark Mode

Apply when user requests dark/trading/real-time context.

```css
body.dark {
    background: #0a0a0a;
    color: #e5e5e5;
}
body.dark pre {
    background: #1a1a1a;
    border-left-color: #444;
}
body.dark table {
    border-color: #333;
}
body.dark th, body.dark td {
    border-color: #333;
}
body.dark .section-header {
    background: #1f1f1f;
}
body.dark button, body.dark .btn {
    background: #1a1a1a;
    border-color: #333;
    color: #e5e5e5;
}
```

---

## Insight/Context Callouts

```css
.insight {
    font-style: italic;
    color: #555;
    margin: 8px 0;
    background: #fffde7;
    padding: 8px;
    border-radius: var(--radius-sm);
}
.fallback {
    font-size: 0.9em;
    color: #666;
    margin: 8px 0;
}
```

---

## Tier Coloring (Leaderboards)

```css
.tier-gold { background: #fff8e1; }
.tier-silver { background: #f5f5f5; }
.tier-bronze { background: #fff3e0; }
```
