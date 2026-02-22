# Order Lookup Workflow

## Step-by-Step

1. **Navigate to Orders**
   ```
   https://sadmx.spex4less.com/monadminx472/sales/order/
   ```

2. **Login if needed**
   - Credentials from 1Password (op CLI)
   - Use tmux session for 1Password access

3. **Search for Order**
   - Order ID (e.g., "100012345")
   - Customer email
   - Customer name
   - Date range (if known)

4. **Click Order to View**
   - Order summary (top)
   - Items ordered (middle)
   - **Journal** (bottom — CRITICAL)

5. **Extract Key Info**
   - Order status
   - Payment status
   - Shipping status
   - Any notes/comments
   - Refund/adjustment history

6. **Screenshot**
   - Full order page
   - Journal section (expanded)

## Journal Section Explained

The Journal at the bottom of the order page shows:

```
Date/Time          | User     | Action/Comment
-------------------|----------|------------------
2024-01-15 10:23   | System   | Order created
2024-01-15 10:24   | Payment  | Payment authorized (£150.00)
2024-01-15 14:30   | John     | Order status: Processing
2024-01-16 09:15   | System   | Invoice created
2024-01-17 11:00   | Jane     | Shipped via Royal Mail (Track: AB123456789GB)
2024-01-18 16:45   | System   | Order Complete
```

## Common Order Statuses

| Status | Meaning |
|--------|---------|
| Pending | Order received, not processed |
| Processing | Being prepared/manufactured |
| Complete | Shipped and delivered |
| Cancelled | Order cancelled |
| On Hold | Awaiting payment or verification |

## Common Issues to Watch For

- **Pending for >24h** — Stuck order
- **Processing >5 days** — Manufacturing delay
- **No tracking number** — Not yet shipped
- **Payment failed** — Authorization issue
- **Multiple refunds** — Customer service issue
