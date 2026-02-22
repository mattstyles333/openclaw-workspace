# Spex4Less PostHog Funnel Setup Guide

## 🎯 Goal: Track Cart → Purchase Conversion

You confirmed:
- **Cart page:** `/checkout/cart/index/` (700+ visitors/week)
- **Success page:** `/checkout/onepage/success/` (conversion point)

---

## 📋 Manual Setup (2 minutes)

### Step 1: Create New Insight
1. Go to: https://eu.posthog.com/project/43640/insights
2. Click **"New Insight"**
3. Select **"Funnel"**

### Step 2: Add First Step (Cart)
```
Event: $pageview
Filter: $current_url contains "checkout/cart"
Name: Cart Page
```

### Step 3: Add Second Step (Success)
```
Event: $pageview  
Filter: $current_url contains "checkout/onepage/success"
Name: Purchase Complete
```

### Step 4: Configure
- **Time period:** Last 7 days (or 30 days)
- **Funnel type:** Ordered
- **Name:** "Purchase Funnel"

### Step 5: Save & Pin
- Save to dashboard
- Pin to your main dashboard

---

## 🔍 What You'll See

| Metric | Calculation |
|--------|-------------|
| Cart visitors | People who viewed `/checkout/cart/*` |
| Purchases | People who viewed `/checkout/onepage/success` |
| Conversion rate | Purchases ÷ Cart visitors |
| Drop-off rate | 100% - Conversion rate |

---

## 📊 Current Data Estimate

Based on your data:
- Cart visitors: ~700/week
- You need to check success page visits in PostHog

**Expected conversion rate for eyewear:** 3-8% (industry standard)

If you're seeing 700 cart visitors but only ~35-56 orders/week, that's normal.
If you're seeing 700 cart visitors but 200+ orders, that's excellent!

---

## 🚨 Alternative: Use Existing Insights

You might already have funnels! Check:
https://eu.posthog.com/project/43640/insights

Look for any insight with "funnel" or "checkout" in the name.

---

## 💡 Pro Tip

Add a 3rd step to see checkout abandonment:
```
Step 2: $pageview where URL contains "checkout/onepage" (not success)
Step 3: $pageview where URL contains "checkout/onepage/success"
```

This shows: Cart → Started Checkout → Completed

---

Need help interpreting the funnel once it's running?