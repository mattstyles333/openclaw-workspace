# Mobile Testing Guide

Comprehensive mobile testing patterns for responsive e-commerce sites.

## Device Viewports to Test

| Device | Viewport | Priority |
|--------|----------|----------|
| iPhone SE | 375x667 | High |
| iPhone 12/13/14 | 390x844 | Critical |
| iPhone 14 Pro Max | 430x932 | High |
| Samsung Galaxy S21 | 384x854 | High |
| iPad Mini | 768x1024 | Medium |
| iPad Pro | 1024x1366 | Medium |

**browser-use command:**
```bash
browser-use run "Test..." --screen-size 390x844 --no-wait  # iPhone 12
```

## Touch Interaction Testing

### Tap Target Size

**Minimum:** 44x44px (Apple HIG)
**Recommended:** 48x48px (Material Design)

**Test:**
```bash
browser-use run "Check tap targets:
1. Navigate to page
2. Screenshot
3. List all interactive elements
4. Flag any that look too small (<44px)
5. Try to tap each one - any missed taps?"
```

### Touch States

| Element | Check |
|---------|-------|
| Buttons | Visual feedback on tap |
| Links | Underline or color change |
| Cards | Lift/shadow on tap |
| Images | No accidental zoom |

### Gesture Support

| Gesture | Test |
|---------|------|
| Swipe | Image galleries, carousels |
| Pinch | Product image zoom |
| Pull | Refresh content |
| Scroll | Smooth, no stickiness |

## Responsive Layout Tests

### Breakpoint Testing

```bash
# Test common breakpoints
browser-use run "Test..." --screen-size 320x568 --no-wait   # Small phone
browser-use run "Test..." --screen-size 390x844 --no-wait   # Modern phone
browser-use run "Test..." --screen-size 768x1024 --no-wait  # Tablet
browser-use run "Test..." --screen-size 1440x900 --no-wait  # Desktop
```

### Layout Issues to Check

| Issue | Test |
|-------|------|
| Horizontal scroll | Check for overflow-x |
| Text overflow | Ellipsis vs wrapping |
| Image distortion | Aspect ratio maintained |
| Overlapping elements | Z-index issues |
| Cut-off content | Viewport clipping |
| Sticky elements | Header/footer behavior |

## Mobile-Specific UX

### Navigation Patterns

**Hamburger Menu:**
- Tap to open
- Tap outside to close
- Swipe to close
- Animation smoothness
- Menu items tappable

**Tab Bar (if applicable):**
- Persistent on scroll
- Icons + labels
- Active state clear
- Thumb-reachable

### Form Interactions

**Keyboard Behavior:**
```bash
browser-use run "Test mobile forms:
1. Tap first input
2. Screenshot: keyboard-open.png
3. Check: Keyboard doesn't cover input
4. Check: Next/Prev buttons work
5. Check: Return key submits
6. Tap date field - native picker?
7. Check numeric keyboard for phone/zip"
```

**Input Types:**
| Field | Keyboard Type |
|-------|---------------|
| Email | email |
| Phone | tel |
| Number | number |
| Date | date picker |
| Text | text |

### Scroll Behavior

**Test:**
- Momentum scrolling smooth
- No scroll jank
- Sticky headers don't flicker
- Parallax (if used) doesn't lag
- Infinite scroll works
- Pull-to-refresh (if applicable)

## Mobile Performance

### Touch Response Time

| Interaction | Target |
|-------------|--------|
| Tap feedback | < 100ms |
| Scroll start | < 50ms |
| Page transition | < 300ms |
| Image load | Progressive |

### Network Conditions

Test on simulated slow connections:
```bash
browser-use run "Test on slow 3G..." --proxy-country gb --no-wait
```

## Mobile CRO Checks

### Thumb Zone

**Primary actions must be in thumb-reachable zone:**
- Bottom center: Best
- Bottom corners: Good
- Top corners: Avoid for primary actions
- Center screen: Okay

### Sticky Elements

| Element | Behavior |
|---------|----------|
| Header | Sticky but not too tall |
| Add to Cart | Sticky at bottom |
| Chat widget | Collapsible |
| Promo banner | Dismissible |

### Mobile Checkout

**Critical checks:**
- [ ] Single-column layout
- [ ] Minimal form fields
- [ ] Address lookup (Google/Apple)
- [ ] Digital wallets (Apple Pay, GPay)
- [ ] Progress indicator
- [ ] Summary always visible
- [ ] No pinch-zoom needed

## Common Mobile Bugs

### Layout Bugs

| Bug | Cause | Fix |
|-----|-------|-----|
| Horizontal scroll | Fixed width elements | Use max-width: 100% |
| Text too small | Fixed font sizes | Use viewport units |
| Images overflow | No max-width | max-width: 100% |
| Buttons too small | Desktop sizing | min-height: 44px |
| Overlap | Absolute positioning | Use flex/grid |

### Interaction Bugs

| Bug | Cause | Fix |
|-----|-------|-----|
| Double-tap zoom | Click delay | touch-action: manipulation |
| 300ms delay | Touch delay | FastClick or CSS |
| Sticky hover | :hover on touch | Use @media (hover) |
| Scroll blocking | Touch events | passive: true |
| Focus stuck | Input focus | Blur on background tap |

### Performance Bugs

| Bug | Cause | Fix |
|-----|-------|-----|
| Scroll jank | Heavy JS | Debounce, requestAnimationFrame |
| Image lag | Unoptimized | Lazy loading, WebP |
| Font flash | Web fonts | font-display: swap |
| Layout shift | Async content | Reserve space |

## Mobile Testing Checklist

### Navigation
- [ ] Hamburger menu works
- [ ] Menu closes properly
- [ ] Search accessible
- [ ] Cart icon visible
- [ ] Account accessible
- [ ] Back button works

### Product Listing
- [ ] Filters accessible
- [ ] Sort works
- [ ] Product cards tappable
- [ ] Images load
- [ ] Infinite scroll works

### Product Detail
- [ ] Image gallery swipeable
- [ ] Zoom works
- [ ] Options selectable
- [ ] Add to cart prominent
- [ ] Reviews readable
- [ ] Related products visible

### Cart
- [ ] Items visible
- [ ] Quantity adjustable
- [ ] Remove works
- [ ] Promo code field
- [ ] Checkout prominent

### Checkout
- [ ] Form fields large enough
- [ ] Keyboard doesn't block
- [ ] Progress indicator
- [ ] Digital wallets available
- [ ] Order summary visible
- [ ] Error messages clear

### General
- [ ] No horizontal scroll
- [ ] Text readable (no zoom)
- [ ] Tap targets large enough
- [ ] Page loads fast (<3s)
- [ ] Sticky elements not annoying
- [ ] Popups dismissible

## Test Script: Mobile Full Suite

```bash
browser-use run "Full mobile test suite:

1. SETUP
   - Viewport: 390x844 (iPhone 12)
   - Clear cache/cookies

2. HOMEPAGE
   - Load homepage
   - Screenshot: m-homepage.png
   - Check: Load time < 3s
   - Check: No horizontal scroll
   - Check: Hamburger menu visible
   - Tap hamburger menu
   - Screenshot: m-menu-open.png
   - Check: Menu items tappable
   - Close menu
   - Check: Menu closes smoothly

3. SEARCH
   - Tap search icon
   - Screenshot: m-search.png
   - Type 'black glasses'
   - Check: Keyboard works
   - Submit search
   - Screenshot: m-search-results.png
   - Check: Results relevant

4. PRODUCT LISTING
   - Scroll results
   - Screenshot: m-plp-scroll.png
   - Check: Smooth scroll
   - Apply filter
   - Screenshot: m-filter.png
   - Check: Filters work

5. PRODUCT DETAIL
   - Tap first product
   - Screenshot: m-pdp.png
   - Check: Images swipeable
   - Swipe images
   - Screenshot: m-pdp-gallery.png
   - Check: Zoom works (pinch)
   - Select options
   - Screenshot: m-options.png
   - Check: Options tappable

6. ADD TO CART
   - Tap Add to Cart
   - Screenshot: m-add-cart.png
   - Check: Feedback (mini cart opens)
   - Check: Correct item added

7. CART
   - Go to cart
   - Screenshot: m-cart.png
   - Check: Item visible
   - Change quantity
   - Screenshot: m-qty-change.png
   - Check: Updates correctly

8. CHECKOUT
   - Tap checkout
   - Screenshot: m-checkout-1.png
   - Check: Form fields large
   - Fill shipping info
   - Screenshot: m-checkout-form.png
   - Check: Keyboard doesn't block
   - Check: Next button works
   - Continue to payment
   - Screenshot: m-checkout-payment.png
   - Check: Digital wallets shown
   - Check: Security badges

9. ISSUES
   - List all bugs found
   - Rate severity (Critical/Major/Minor)
   - Screenshot evidence for each

10. SUMMARY
    - Overall mobile experience: 1-10
    - Ship/Fix/Block recommendation"
    --screen-size 390x844
```

## Reporting Mobile Issues

**Format:**
```markdown
## Mobile Issue #[#]

**Device:** iPhone 12 (390x844)
**Page:** [URL]
**Severity:** [Critical/Major/Minor]

**Description:**
[What happens]

**Expected:**
[What should happen]

**Evidence:**
[Screenshot link]

**Reproduction:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Impact:**
[How this hurts conversion]
```
