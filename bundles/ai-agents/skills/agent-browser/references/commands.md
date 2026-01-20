# agent-browser Command Reference

Complete reference for all agent-browser CLI commands.

## Installation

```bash
npm install -g agent-browser
```

## Global Options

| Option | Description |
|--------|-------------|
| `--session <name>` | Use named session for parallel testing |
| `--json` | Output results as JSON |
| `--headed` | Show browser window (for debugging) |
| `--cdp <port>` | Connect via Chrome DevTools Protocol |

---

## Navigation Commands

### open

Navigate to a URL.

```bash
agent-browser open <url>
agent-browser open https://example.com
agent-browser open https://example.com --headed  # Show browser
```

### back

Navigate back in history.

```bash
agent-browser back
```

### forward

Navigate forward in history.

```bash
agent-browser forward
```

### reload

Reload the current page.

```bash
agent-browser reload
agent-browser reload --hard  # Clear cache
```

### close

Close the browser.

```bash
agent-browser close
```

---

## Snapshot Commands

Snapshots analyze the page and return element references (`@e1`, `@e2`, etc.) for interactions.

### snapshot

Get page accessibility tree.

```bash
agent-browser snapshot            # Full tree
agent-browser snapshot -i         # Interactive elements only (recommended)
agent-browser snapshot -c         # Compact output
agent-browser snapshot -d 3       # Limit depth to 3 levels
agent-browser snapshot -s "#main" # Scope to CSS selector
agent-browser snapshot -a         # Include ARIA attributes
agent-browser snapshot -f         # Full page (scroll through all)
```

**Options:**

| Flag | Description |
|------|-------------|
| `-i` | Interactive elements only |
| `-c` | Compact output |
| `-d <n>` | Limit depth |
| `-s <selector>` | Scope to CSS selector |
| `-a` | Include ARIA attributes |
| `-f` | Full page snapshot |

---

## Interaction Commands

All interaction commands use `@refs` from snapshot output.

### click

Click an element.

```bash
agent-browser click @e1
agent-browser click @e1 --force   # Force click (bypass visibility checks)
agent-browser click @e1 --button right  # Right-click
```

### dblclick

Double-click an element.

```bash
agent-browser dblclick @e1
```

### focus

Focus an element.

```bash
agent-browser focus @e1
```

### fill

Clear and type into an input.

```bash
agent-browser fill @e1 "text to type"
agent-browser fill @e1 ""  # Clear field
```

### type

Type without clearing (append).

```bash
agent-browser type @e1 "additional text"
```

### press

Press a key or key combination.

```bash
agent-browser press Enter
agent-browser press Tab
agent-browser press Escape
agent-browser press Control+a       # Select all
agent-browser press Control+c       # Copy
agent-browser press Control+v       # Paste
agent-browser press Shift+Tab       # Shift+Tab
agent-browser press Alt+F4          # Close window
```

### keydown / keyup

Hold or release a key.

```bash
agent-browser keydown Shift
agent-browser click @e1
agent-browser keyup Shift
```

### hover

Hover over an element.

```bash
agent-browser hover @e1
```

### check / uncheck

Toggle checkboxes.

```bash
agent-browser check @e1
agent-browser uncheck @e1
```

### select

Select dropdown option.

```bash
agent-browser select @e1 "Option Text"
agent-browser select @e1 --value "option_value"
agent-browser select @e1 --index 2
```

### scroll

Scroll the page or element.

```bash
agent-browser scroll down 500     # Scroll down 500px
agent-browser scroll up 300       # Scroll up 300px
agent-browser scroll left 200     # Scroll left
agent-browser scroll right 200    # Scroll right
agent-browser scroll top          # Scroll to top
agent-browser scroll bottom       # Scroll to bottom
```

### scrollintoview

Scroll element into viewport.

```bash
agent-browser scrollintoview @e1
```

### drag

Drag and drop.

```bash
agent-browser drag @e1 @e2        # Drag e1 to e2
agent-browser drag @e1 100 200    # Drag e1 to coordinates
```

### upload

Upload files to file input.

```bash
agent-browser upload @e1 file.pdf
agent-browser upload @e1 file1.pdf file2.pdf  # Multiple files
```

---

## Information Commands

### get text

Get element text content.

```bash
agent-browser get text @e1
agent-browser get text @e1 --json
```

### get html

Get element innerHTML.

```bash
agent-browser get html @e1
```

### get value

Get input value.

```bash
agent-browser get value @e1
```

### get attr

Get element attribute.

```bash
agent-browser get attr @e1 href
agent-browser get attr @e1 data-id
agent-browser get attr @e1 class
```

### get title

Get page title.

```bash
agent-browser get title
```

### get url

Get current URL.

```bash
agent-browser get url
```

### get count

Count elements matching selector.

```bash
agent-browser get count ".item"
agent-browser get count "button"
agent-browser get count "[data-testid='row']"
```

### get box

Get element bounding box.

```bash
agent-browser get box @e1
# Returns: { x, y, width, height }
```

---

## State Check Commands

### is visible

Check if element is visible.

```bash
agent-browser is visible @e1
# Returns: true/false
```

### is enabled

Check if element is enabled.

```bash
agent-browser is enabled @e1
```

### is checked

Check if checkbox/radio is checked.

```bash
agent-browser is checked @e1
```

---

## Screenshot & Media Commands

### screenshot

Capture screenshot.

```bash
agent-browser screenshot                    # Output to stdout
agent-browser screenshot page.png           # Save to file
agent-browser screenshot --full page.png    # Full page scroll
agent-browser screenshot @e1 element.png    # Element only
```

### pdf

Export page as PDF.

```bash
agent-browser pdf output.pdf
agent-browser pdf output.pdf --format A4
agent-browser pdf output.pdf --landscape
```

### record

Record video.

```bash
agent-browser record start ./video.webm     # Start recording
agent-browser record stop                   # Stop and save
agent-browser record restart ./new.webm     # Stop current, start new
```

---

## Wait Commands

### wait (element)

Wait for element to appear.

```bash
agent-browser wait @e1
agent-browser wait @e1 --timeout 10000
```

### wait (time)

Wait for milliseconds.

```bash
agent-browser wait 2000
```

### wait --text

Wait for text to appear.

```bash
agent-browser wait --text "Success"
agent-browser wait --text "Loading" --gone  # Wait for text to disappear
```

### wait --url

Wait for URL pattern.

```bash
agent-browser wait --url "**/dashboard"
agent-browser wait --url "https://example.com/success"
```

### wait --load

Wait for page load state.

```bash
agent-browser wait --load domcontentloaded
agent-browser wait --load load
agent-browser wait --load networkidle
```

### wait --fn

Wait for JavaScript condition.

```bash
agent-browser wait --fn "window.loaded === true"
agent-browser wait --fn "document.querySelectorAll('.item').length > 5"
```

---

## Mouse Commands

### mouse move

Move mouse to coordinates.

```bash
agent-browser mouse move 100 200
```

### mouse down / up

Press/release mouse button.

```bash
agent-browser mouse down left
agent-browser mouse up left
agent-browser mouse down right
```

### mouse wheel

Scroll with mouse wheel.

```bash
agent-browser mouse wheel 100       # Scroll down
agent-browser mouse wheel -100      # Scroll up
```

---

## Semantic Locators

Alternative to @refs - find elements by semantic properties.

### find role

Find by ARIA role.

```bash
agent-browser find role button click --name "Submit"
agent-browser find role textbox fill "text" --name "Email"
agent-browser find role link click --name "Home"
```

### find text

Find by text content.

```bash
agent-browser find text "Sign In" click
agent-browser find text "Continue" click
```

### find label

Find input by label.

```bash
agent-browser find label "Email" fill "user@test.com"
agent-browser find label "Password" fill "secret123"
```

### find first / nth

Find by CSS selector.

```bash
agent-browser find first ".item" click
agent-browser find nth 2 ".item" click     # 0-indexed
agent-browser find last ".item" click
```

---

## Browser Settings

### set viewport

Set browser viewport size.

```bash
agent-browser set viewport 1920 1080
agent-browser set viewport 375 812  # Mobile
```

### set device

Emulate device.

```bash
agent-browser set device "iPhone 14"
agent-browser set device "iPad Pro"
agent-browser set device "Pixel 7"
```

### set geo

Set geolocation.

```bash
agent-browser set geo 37.7749 -122.4194  # San Francisco
```

### set offline

Toggle offline mode.

```bash
agent-browser set offline on
agent-browser set offline off
```

### set headers

Set extra HTTP headers.

```bash
agent-browser set headers '{"X-Custom-Header": "value"}'
```

### set credentials

Set HTTP basic auth credentials.

```bash
agent-browser set credentials username password
```

### set media

Set media features (dark mode, etc.).

```bash
agent-browser set media dark
agent-browser set media light
agent-browser set media reduced-motion
```

---

## Cookies & Storage

### cookies

Manage cookies.

```bash
agent-browser cookies                     # Get all
agent-browser cookies set name value      # Set cookie
agent-browser cookies get name            # Get specific
agent-browser cookies clear               # Clear all
agent-browser cookies clear --name foo    # Clear specific
```

### storage

Manage localStorage/sessionStorage.

```bash
agent-browser storage local               # Get all localStorage
agent-browser storage local key           # Get specific key
agent-browser storage local set key value # Set value
agent-browser storage local clear         # Clear all

agent-browser storage session             # sessionStorage
agent-browser storage session key
agent-browser storage session set key value
agent-browser storage session clear
```

### state

Save/load browser state (cookies + storage).

```bash
agent-browser state save auth.json        # Save state
agent-browser state load auth.json        # Load state
```

---

## Network Commands

### network route

Intercept and mock network requests.

```bash
agent-browser network route "**/api/data"              # Log requests
agent-browser network route "**/api/data" --abort      # Block requests
agent-browser network route "**/api/data" --body '{}' # Mock response
agent-browser network route "**/api/data" --status 500 # Mock status
agent-browser network route "**/*.png" --abort         # Block images
```

### network unroute

Remove network interception.

```bash
agent-browser network unroute              # Remove all
agent-browser network unroute "**/api/*"   # Remove specific
```

### network requests

View intercepted requests.

```bash
agent-browser network requests
agent-browser network requests --filter api
agent-browser network requests --method POST
```

---

## Tab & Window Commands

### tab

Manage browser tabs.

```bash
agent-browser tab                 # List all tabs
agent-browser tab new             # New blank tab
agent-browser tab new <url>       # New tab with URL
agent-browser tab 2               # Switch to tab index
agent-browser tab close           # Close current tab
agent-browser tab close 2         # Close tab by index
```

### window

Manage browser windows.

```bash
agent-browser window new          # New window
agent-browser window close        # Close window
```

---

## Frame Commands

### frame

Switch between frames.

```bash
agent-browser frame "#iframe-id"  # Switch to iframe
agent-browser frame "[name=foo]"  # By name attribute
agent-browser frame main          # Back to main frame
```

---

## Dialog Commands

### dialog

Handle JavaScript dialogs (alert, confirm, prompt).

```bash
agent-browser dialog accept       # Accept dialog
agent-browser dialog accept "text" # Accept with input (for prompt)
agent-browser dialog dismiss      # Dismiss dialog
```

---

## JavaScript Commands

### eval

Execute JavaScript in page context.

```bash
agent-browser eval "document.title"
agent-browser eval "window.scrollY"
agent-browser eval "localStorage.getItem('token')"
agent-browser eval "document.querySelectorAll('.item').length"
```

---

## Session Commands

Run parallel browser instances.

```bash
agent-browser --session test1 open site-a.com
agent-browser --session test2 open site-b.com
agent-browser --session test1 snapshot -i
agent-browser --session test2 snapshot -i
agent-browser session list
agent-browser session close test1
```

---

## Debugging Commands

### console

View browser console output.

```bash
agent-browser console             # View messages
agent-browser console --clear     # Clear console
agent-browser console --filter error  # Filter by type
```

### errors

View page errors.

```bash
agent-browser errors
agent-browser errors --clear
```

### highlight

Highlight element on page (headed mode).

```bash
agent-browser highlight @e1
```

### trace

Record performance trace.

```bash
agent-browser trace start
# ... perform actions ...
agent-browser trace stop trace.zip
```

---

## Common Patterns

### Login Flow

```bash
agent-browser open https://app.com/login
agent-browser snapshot -i
agent-browser fill @e1 "username"
agent-browser fill @e2 "password"
agent-browser click @e3
agent-browser wait --url "**/dashboard"
agent-browser state save auth.json
```

### Form Testing

```bash
agent-browser open https://app.com/form
agent-browser snapshot -i
agent-browser fill @e1 "invalid"
agent-browser click @e5
agent-browser snapshot -i  # Check for errors
agent-browser get text @e1  # Get error message
```

### Visual Regression

```bash
agent-browser open https://app.com
agent-browser set viewport 1920 1080
agent-browser screenshot desktop.png --full
agent-browser set device "iPhone 14"
agent-browser reload
agent-browser screenshot mobile.png --full
```

### API Mocking

```bash
agent-browser network route "**/api/users" --body '[{"id":1,"name":"Test"}]'
agent-browser open https://app.com/users
agent-browser snapshot -i
```
