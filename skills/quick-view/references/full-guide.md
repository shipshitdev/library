# Quick View — Full Examples

## File Naming Lifecycle Example

```
# First iteration
drafts-temp.html  ← created

# User: "keep this"
drafts.html       ← promoted (temp deleted)

# Later iteration
drafts-temp.html  ← new temp created
drafts.html       ← keeper untouched

# User: "this is better, keep it"
drafts.2025-01-01.html  ← old keeper archived
drafts.html             ← new keeper promoted
```

## Editable Drafts Markup

```html
<details>
  <summary><strong>@username</strong> — action <span class="status"></span></summary>
  <pre contenteditable="true"
       data-username="username"
       data-original="Original draft text here"
       onblur="saveDraft(this)">Original draft text here</pre>
  <div class="actions">
    <a href="tg://resolve?domain=username">Open Telegram</a>
    <button onclick="copyDraft(this)">Copy</button>
  </div>
</details>
```

## Editable Drafts Script

Include this script block at end of `<body>` (before closing `</body>` tag):

```javascript
function saveDraft(el) {
  const key = 'draft_' + el.dataset.username;
  const edited = el.textContent.trim();
  const original = el.dataset.original;
  if (edited !== original) {
    localStorage.setItem(key, edited);
    el.closest('details').querySelector('.status').textContent = '(edited)';
  }
}

function copyDraft(btn) {
  const pre = btn.closest('details').querySelector('pre');
  navigator.clipboard.writeText(pre.textContent.trim());
  btn.textContent = 'Copied!';
  setTimeout(() => btn.textContent = 'Copy', 1500);
}

function restoreEdits() {
  document.querySelectorAll('pre[data-username]').forEach(el => {
    const saved = localStorage.getItem('draft_' + el.dataset.username);
    if (saved) {
      el.textContent = saved;
      el.closest('details').querySelector('.status').textContent = '(edited)';
    }
  });
}

function exportEdits() {
  const edits = [];
  document.querySelectorAll('pre[data-username]').forEach(el => {
    const original = el.dataset.original;
    const current = el.textContent.trim();
    if (original !== current) {
      edits.push({ username: el.dataset.username, original, edited: current });
    }
  });
  if (edits.length === 0) { alert('No edits to export'); return; }
  const blob = new Blob([JSON.stringify({exported_at: new Date().toISOString(), edits}, null, 2)], {type: 'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'draft_edits.json';
  a.click();
}

restoreEdits();
```
