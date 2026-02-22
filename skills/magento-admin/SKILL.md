---
name: magento-admin
description: "Access and navigate Spex4Less Magento 2 admin panel in read-only mode using OpenClaw browser. Use when user mentions 'magento', 'm2', 'check order', 'look up product', 'find customer', or needs information from the admin backend. Retrieves order details, product configurations, customer info, and reports. READ-ONLY — never modify data without explicit permission."
---

# Magento Admin (Spex4Less)

Read-only access to the Spex4Less Magento 2 admin panel using OpenClaw browser tool.

## Base URL

```
https://sadmx.spex4less.com/monadminx472/
```

## Key Pages

| Section | URL | Purpose |
|---------|-----|---------|
| **Orders** | `/sales/order/` | Search and view order details, journal entries |
| **Products** | `/catalog/product/` | Product catalog, attributes, configurations |
| **Customers** | `/customer/index/` | Customer search and profiles |
| **Reports** | `/reports/` | Sales, products, customers reports |
| **Dashboard** | `/admin/dashboard/` | Admin home |

## Authentication

Uses 1Password credentials for Magento admin login.

### Method 1: 1Password Browser Extension (Preferred)
- Use Chrome profile with 1Password extension attached
- Browser extension will auto-fill or suggest credentials

### Method 2: 1Password CLI (When Extension Unavailable)

**Prerequisites:**
- 1Password CLI installed: `op --version` → 2.x
- Account signed in (check: `op account list`)
- Account: `my.1password.com` (mattstyles333@gmail.com)

**Get Credentials via tmux:**

```bash
# Create tmux session for op auth
SOCKET_DIR="${TMPDIR:-/tmp}/tmux-sockets"
mkdir -p "$SOCKET_DIR"
SOCKET="$SOCKET_DIR/op-session.sock"
SESSION="op-magento"

# Start session
tmux -S "$SOCKET" new -d -s "$SESSION"

# Run op command (may need biometric approval)
tmux -S "$SOCKET" send-keys -t "$SESSION" 'op item get "Spex4Less Magento" --fields username,password' Enter

# Wait for user approval (10-15 seconds), then capture
tmux -S "$SOCKET" send-keys -t "$SESSION" 'echo "Done"' Enter

# Capture output
OUTPUT=$(tmux -S "$SOCKET" capture-pane -t "$SESSION" -p)
echo "$OUTPUT"

# Cleanup
tmux -S "$SOCKET" kill-session -t "$SESSION"
```

**Extract credentials from output:**
- Username: field after `username:`
- Password: field after `password:`

### Method 3: Browser Fill with Credentials

```python
# Navigate to login page
browser: {
  "action": "open",
  "targetUrl": "https://sadmx.spex4less.com/monadminx472/admin/auth/login/"
}

# Fill credentials (obtained from 1Password)
browser: {
  "action": "act",
  "request": {
    "kind": "fill",
    "fields": [
      {"name": "login[username]", "value": "$USERNAME_FROM_OP"},
      {"name": "login[password]", "value": "$PASSWORD_FROM_OP"}
    ]
  }
}

# Click Sign In
browser: {
  "action": "act",
  "request": {"kind": "click", "ref": "Sign in"}
}
```

**Note:** Never hardcode credentials. Always retrieve from 1Password in real-time.

## READ-ONLY Policy

- ✅ **Allowed:** View, search, read, screenshot
- ❌ **Never:** Edit, delete, save changes, place test orders
- ⚠️ **Exception:** Only modify if user explicitly says "update", "change", "edit" + confirms

## Browser Workflow (Primary Method)

### 1. Navigate to Admin

```python
browser: {
  "action": "open",
  "targetUrl": "https://sadmx.spex4less.com/monadminx472/admin/auth/login/"
}
```

### 2. Login

```python
browser: {
  "action": "act",
  "request": {
    "kind": "fill",
    "fields": [{"name": "login[username]", "value": "USERNAME"}, {"name": "login[password]", "value": "PASSWORD"}]
  }
}
browser: {
  "action": "act", 
  "request": {"kind": "click", "ref": "Sign in"}
}
```

**Note:** Credentials from 1Password. If 1Password extension is attached, use it. Otherwise manually extract via 1Password app.

### 3. Navigate to Section

```python
# For Orders
browser: {
  "action": "navigate",
  "targetUrl": "https://sadmx.spex4less.com/monadminx472/sales/order/"
}

# For Products
browser: {
  "action": "navigate",
  "targetUrl": "https://sadmx.spex4less.com/monadminx472/catalog/product/"
}

# For Customers
browser: {
  "action": "navigate", 
  "targetUrl": "https://sadmx.spex4less.com/monadminx472/customer/index/"
}
```

### 4. Search & Find

```python
browser: {
  "action": "act",
  "request": {"kind": "type", "selector": "input[name='increment_id']", "text": "ORDER_ID"}
}
browser: {
  "action": "act",
  "request": {"kind": "click", "ref": "Search"}
}
```

### 5. Screenshot Results

```python
browser: {
  "action": "screenshot",
  "fullPage": true
}
```

## Common Tasks

### Task 1: Look Up Latest Order

```python
# Navigate to orders
browser: {
  "action": "open",
  "targetUrl": "https://sadmx.spex4less.com/monadminx472/sales/order/"
}

# Login if needed
# ... (see Login section above)

# Orders are sorted by date descending by default
# The first row is the latest order - click it
browser: {
  "action": "act",
  "request": {"kind": "click", "selector": "table.data-grid tbody tr:first-child td:first-child a"}
}

# Screenshot order details
browser: {
  "action": "screenshot",
  "fullPage": true
}

# Scroll down to Journal section
browser: {
  "action": "act",
  "request": {"kind": "scroll", "direction": "down"}
}

# Screenshot Journal
browser: {
  "action": "screenshot",
  "fullPage": true
}
```

### Task 2: Look Up Specific Order

```python
browser: {
  "action": "navigate",
  "targetUrl": "https://sadmx.spex4less.com/monadminx472/sales/order/"
}

# Search by order ID
browser: {
  "action": "act",
  "request": {"kind": "type", "selector": "#order_grid_filter_increment_id", "text": "100012345"}
}
browser: {
  "action": "act",
  "request": {"kind": "click", "ref": "Filters"}
}
browser: {
  "action": "act", 
  "request": {"kind": "click", "ref": "Apply"}
}

# Click order in results
browser: {
  "action": "act",
  "request": {"kind": "click", "selector": "table tbody tr:first-child a"}
}

# Screenshot full order
browser: {
  "action": "screenshot",
  "fullPage": true
}
```

### Task 3: Check Product

```python
browser: {
  "action": "navigate",
  "targetUrl": "https://sadmx.spex4less.com/monadminx472/catalog/product/"
}

# Search by SKU or name
browser: {
  "action": "act",
  "request": {"kind": "type", "selector": "#product_grid_filter_name", "text": "Ray-Ban"}
}
browser: {
  "action": "act",
  "request": {"kind": "click", "ref": "Filters"}
}
browser: {
  "action": "act",
  "request": {"kind": "click", "ref": "Apply"}
}

# Click product
browser: {
  "action": "act",
  "request": {"kind": "click", "selector": "table tbody tr:first-child a"}
}

# Screenshot product details
browser: {
  "action": "screenshot",
  "fullPage": true
}

# Scroll to attributes/configurations  
browser: {
  "action": "act",
  "request": {"kind": "scroll", "direction": "down"}
}
```

### Task 4: Find Customer

```python
browser: {
  "action": "navigate",
  "targetUrl": "https://sadmx.spex4less.com/monadminx472/customer/index/"
}

# Search by email
browser: {
  "action": "act",
  "request": {"kind": "type", "selector": "#customerGrid_filter_email", "text": "customer@example.com"}
}
browser: {
  "action": "act",
  "request": {"kind": "click", "ref": "Search"}
}

# Click customer
browser: {
  "action": "act",
  "request": {"kind": "click", "selector": "table tbody tr:first-child a"}
}
```

## Key Order Fields

| Field | Where to Find |
|-------|---------------|
| Order ID | Top of page |
| Status | Order & Account Information box |
| Payment Status | Payment section |
| Shipping Status | Shipping section |
| Customer Info | Order & Account Information |
| Items Ordered | Items Ordered section |
| Totals | Totals section on right |
| **Journal** | **Bottom of page - CRITICAL** |

## Journal Section

The Journal shows order history:
- Status changes
- Payment updates
- Shipping/tracking info
- Comments/notes

**Always screenshot the Journal** — it contains critical order status history.

## Response Format

```markdown
## Order #XXXXX Lookup

**Status:** [Complete/Processing/Pending/Cancelled]
**Customer:** [Name] ([Email])
**Total:** £XX.XX
**Date:** [Date]
**Payment:** [Status]

### Items
| SKU | Product | Qty | Price |
|-----|---------|-----|-------|
| XXX | [Name] | X | £XX.XX |

### Shipping
- Method: [Royal Mail/etc]
- Tracking: [If available]

### Journal (Latest 5 entries)
- [Time] — [Action/User]
- [Time] — [Action/User]
- ...

### Screenshots
- Order details: [attached]
- Journal section: [attached]

### Notes
[Any issues or observations]
```

## Safety

- **Read-only** — Never save changes
- **Screenshot everything** — Evidence for records
- **Log out** when done
- **Don't share customer PII** unnecessarily

## Troubleshooting

**Login page not loading?**
- Check URL: `/admin/auth/login/`
- Try refreshing

**Session expired?**
- Re-login via browser

**Can't find order?**
- Check date range filters
- Try searching by email instead of ID
- Check if order is recent enough to be in first page

**Product not showing?**
- Check "Status" filter (Active/Inactive)
- Try SKU search
- Check pagination

**Customer not found?**
- Try partial email match
- Check different email formats

## 1Password (When Browser Extension Unavailable)

If browser 1Password extension isn't working:

```python
# Get credentials via tmux + op CLI
exec: {
  "command": "export SOCKET_DIR=\"${TMPDIR:-/tmp}/tmux-sockets\" && mkdir -p \"$SOCKET_DIR\" && SOCKET=\"$SOCKET_DIR/op-$(date +%s).sock\" && SESSION=\"op-$(date +%Y%m%d-%H%M%S)\" && tmux -S \"$SOCKET\" new -d -s \"$SESSION\" && tmux -S \"$SOCKET\" send-keys -t \"$SESSION\" 'op signin --raw' Enter && sleep 5 && tmux -S \"$SOCKET\" capture-pane -t \"$SESSION\" -p && tmux -S \"$SOCKET\" kill-session -t \"$SESSION\" 2>/dev/null"
}
```

But prefer browser extension when available.
