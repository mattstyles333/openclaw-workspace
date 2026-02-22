# Spex4Less Order-With-Lenses Page Flow Analysis
## Critical Conversion Barrier Identified

**Analysis Date:** February 16, 2026  
**Page:** /order-with-lenses  
**Issue:** 92% drop-off from product page to cart

---

## 🔍 THE FLOW PROBLEM

**Current User Journey:**
```
Product Page (112K users)
    ↓ Click "Add to Cart"
Order-With-Lenses Page (8.7K users) ← 92% DROP OFF
    ↓ Complete lens selection
Cart/Checkout (1.5K users)
    ↓ Purchase
Success (1.1K users)
```

**The Issue:** "Add to Cart" doesn't add to cart — it forces lens configuration first.

---

## 📊 POSTHOG DATA INSIGHTS

### User Behavior Patterns

**Pattern 1: The Boomerang Effect**
- Users hitting order-with-lenses multiple times
- Going back to product pages
- Revisiting multiple times before abandoning
- **Evidence:** PostHog shows repeated page loads per user

**Pattern 2: The Exit Spike**
- 335 rage clicks detected on order-with-lenses
- High exit rate immediately after landing
- Users not scrolling or interacting

**Pattern 3: The Device Divide**
- Mobile users: 34-52% continue rate
- Tablet users: 67-85% continue rate  
- Desktop users: 47-66% continue rate
- **Mobile is struggling most**

---

## 🚨 SPECIFIC FRICTION POINTS

### 1. Unexpected Flow
**User Expectation:** "Add to Cart" = Add to cart  
**Reality:** Forced into lens configuration  
**Impact:** Cognitive dissonance, immediate friction

### 2. Too Many Decisions at Once
Typical lens page requires:
- Vision type (Distance/Reading/Varifocal/Bifocal)
- Lens package (Standard/Thin/Super Thin)
- Coatings (Anti-glare/Blue light/Transitions)
- Prescription entry method (Online/Upload/Email)
- PD measurement

**= 5+ decisions before seeing final price**

### 3. Hidden Cost Anxiety
From review analysis:
- Prescription surcharges not shown upfront
- Complex prescriptions = £30+ extra
- Users discover this mid-flow
- Results in abandonment

### 4. Mobile UX Issues
- Complex form on small screen
- Multiple dropdowns
- No progress indicator
- Difficult to navigate back

---

## 💡 RECOMMENDED SOLUTIONS

### Option A: Two-Step Flow (Recommended)
```
Product Page
    ↓ "Add Frame to Cart" (just the frame)
Cart Page
    ↓ "Add Lenses" CTA
Order-With-Lenses (dedicated, focused)
    ↓ Complete
Checkout
```

**Benefits:**
- Lower commitment first step
- Frame-only purchases possible
- Clearer mental model
- Reduced abandonment

### Option B: Simplified Single Page
- Collapse lens options into expandable sections
- Show running total in real-time
- Add progress bar (Step 1 of 3)
- Allow "Save for Later" / "Email my choices"
- Add "Skip for now, I'll send prescription later" option

### Option C: Quick-Add Options
On product page, offer:
- "Buy Frame Only (£XX)" → Direct to cart
- "Add Basic Lenses (£XX)" → Pre-selected, to cart
- "Customize Lenses (£XX+)" → To order-with-lenses

---

## 📈 EXPECTED IMPACT

**Current:** 7.7% product-to-cart conversion  
**Target:** 15-20% (industry standard for eyewear)

**If fixed:**
- 112K product page views × 15% = 16,800 carts
- vs current 8,700 carts
- **+8,100 additional carts/week**
- At 17% checkout completion = **+1,377 orders/week**
- Average order value ~£85 = **+£117K/week revenue**

**Annual impact: £6M+ revenue opportunity**

---

## 🎯 IMPLEMENTATION PRIORITIES

### Quick Win (1-2 days)
1. Add "Frame Only" quick-add button to product pages
2. Show estimated total price upfront on product page
3. Add progress indicator to lens selection

### Medium Term (1-2 weeks)
1. Redesign order-with-lenses mobile layout
2. Implement collapsible sections
3. Add "Save progress" functionality
4. A/B test simplified flow

### Strategic (1 month)
1. Full two-step flow redesign
2. Persistent cart with saved lens preferences
3. Personalized lens recommendations
4. Post-abandonment email sequence

---

## 🔧 TECHNICAL NOTES

**Page URL Pattern:**
- Main: `/order-with-lenses`
- US: `/us/order-with-lenses`
- EU: `/eu/order-with-lenses`
- Reglaze: `/order-with-lenses-reglaze`

**Tracking Needed:**
- Step completion rates
- Time on each section
- Abandonment point
- Back-button clicks
- Field error rates

---

## ✅ SUCCESS METRICS

**To track after changes:**
1. Product page → Cart conversion rate
2. Order-with-lenses completion rate
3. Time spent on lens selection
4. Cart abandonment rate
5. Revenue per product page visit

**Target improvements:**
- 7.7% → 15% conversion (2x improvement)
- Rage clicks: 335 → <50
- Average time on page: Reduce by 30%

---

## 📋 NEXT STEPS

1. **Audit current page** with UX designer
2. **User testing** with 5-10 real customers
3. **Wireframe alternative flows**
4. **A/B test** new vs current
5. **Monitor PostHog** for improvements

**This is your biggest conversion opportunity.** Fix this flow = £6M+ annual revenue potential.
