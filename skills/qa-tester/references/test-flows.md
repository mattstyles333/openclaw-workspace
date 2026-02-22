# Pre-Built Test Flows

Ready-to-use browser-use test scripts for common scenarios.

## E-Commerce Happy Path (Desktop)

```bash
browser-use run "Test complete e-commerce purchase flow:

1. NAVIGATE to homepage
   - Screenshot: homepage.png
   - Check: Load time < 3s
   - Check: Hero CTA visible and clickable

2. CATEGORY BROWSING
   - Click main category menu
   - Screenshot: category-menu.png
   - Select 'Glasses' category
   - Screenshot: plp-glasses.png
   - Check: Products load, prices visible
   - Check: Filter options work

3. PRODUCT DETAIL PAGE
   - Click first product
   - Screenshot: pdp.png
   - Check: Images load, zoom works
   - Check: Price clear, stock status visible
   - Check: Add to cart button prominent
   - Check: Product description readable

4. ADD TO CART
   - Click Add to Cart
   - Screenshot: add-to-cart.png
   - Check: Cart updates immediately
   - Check: Mini-cart shows correct item
   - Check: Price accurate

5. CART PAGE
   - Go to cart
   - Screenshot: cart.png
   - Check: All items listed correctly
   - Check: Quantity can be changed
   - Check: Remove item works
   - Check: Promo code field present
   - Check: Checkout button prominent

6. CHECKOUT FLOW
   - Click checkout
   - Screenshot: checkout-step1.png
   - Check: Guest checkout available
   - Fill shipping info (use test data)
   - Screenshot: checkout-shipping.png
   - Check: Shipping options clear
   - Continue to payment
   - Screenshot: checkout-payment.png
   - Check: Payment methods visible
   - Check: Security badges present
   - Check: Order summary visible

7. ORDER CONFIRMATION
   - Complete test purchase
   - Screenshot: order-confirmation.png
   - Check: Confirmation message clear
   - Check: Order number displayed
   - Check: Email confirmation mentioned
   - Check: What happens next explained

8. REPORT
   - List any errors encountered
   - Note any confusing UI
   - Flag anything that would make you abandon
   - Rate overall experience 1-10"
```

## Mobile Responsive Test

```bash
browser-use run "Test mobile experience:

1. HOMEPAGE (Mobile)
   - Viewport: 375x812 (iPhone X)
   - Screenshot: mobile-homepage.png
   - Check: No horizontal scroll
   - Check: Text readable without zoom
   - Check: Hamburger menu works

2. NAVIGATION (Mobile)
   - Tap hamburger menu
   - Screenshot: mobile-menu.png
   - Check: Menu opens smoothly
   - Check: Links tappable (not too small)
   - Check: Can close menu

3. PRODUCT LISTING (Mobile)
   - Navigate to category
   - Screenshot: mobile-plp.png
   - Check: Filters accessible
   - Check: Product cards tappable
   - Check: Images load

4. PRODUCT DETAIL (Mobile)
   - Tap product
   - Screenshot: mobile-pdp.png
   - Check: Image gallery swipeable
   - Check: Zoom/pinch works
   - Check: Add to cart button tappable
   - Check: Size/option selectors usable

5. CART (Mobile)
   - Add item
   - Screenshot: mobile-cart.png
   - Check: Quantity controls work
   - Check: Remove button tappable

6. CHECKOUT (Mobile)
   - Proceed to checkout
   - Screenshot: mobile-checkout.png
   - Check: Form fields large enough
   - Check: Keyboard doesn't block inputs
   - Check: Date pickers work
   - Check: Dropdowns usable

7. REPORT
   - List mobile-specific issues
   - Rate mobile experience 1-10"
   --screen-size 375x812
```

## CRO Audit Flow

```bash
browser-use run "CRO Audit - Find conversion killers:

1. HOMEPAGE
   - Load time: [measure]
   - Is value prop clear in 5 seconds?
   - Is primary CTA obvious?
   - Trust signals visible? (reviews, guarantees)
   - Screenshot: cro-homepage.png

2. PRODUCT PAGES
   - Price visible above fold?
   - Stock urgency (if applicable)?
   - Reviews/testimonials visible?
   - Return policy linked?
   - Multiple payment options shown?
   - Screenshot: cro-pdp.png

3. CART PAGE
   - Security badges present?
   - Guest checkout option?
   - Clear progress indicator?
   - No unexpected fees?
   - Screenshot: cro-cart.png

4. CHECKOUT
   - How many form fields? (count)
   - Progress bar showing steps?
   - Can edit cart from checkout?
   - No exit links to other pages?
   - Error messages helpful?
   - Screenshot: cro-checkout.png

5. POST-PURCHASE
   - Clear confirmation?
   - Next steps explained?
   - Create account option (not forced)?
   - Screenshot: cro-confirmation.png

6. REPORT
   - List each friction point found
   - Estimate conversion impact (High/Medium/Low)
   - Recommend specific fixes"
```

## Edge Cases & Error Testing

```bash
browser-use run "Edge case testing:

1. FORM VALIDATION
   - Submit empty checkout form
   - Screenshot: error-empty-form.png
   - Enter invalid email
   - Screenshot: error-invalid-email.png
   - Enter invalid phone
   - Screenshot: error-invalid-phone.png
   - Enter invalid postcode
   - Screenshot: error-invalid-postcode.png

2. CART EDGE CASES
   - Add 999 quantity of item
   - Screenshot: cart-massive-qty.png
   - Add 0 quantity
   - Screenshot: cart-zero-qty.png
   - Refresh page after adding item
   - Screenshot: cart-refresh.png
   - Navigate back then forward
   - Screenshot: cart-back-forward.png

3. PRODUCT EDGE CASEES
   - Try to add out-of-stock item
   - Screenshot: oos-error.png
   - Manually edit URL to invalid product
   - Screenshot: 404-product.png
   - Rapid click add to cart 10 times
   - Screenshot: rapid-click.png

4. CHECKOUT EDGE CASES
   - Navigate to checkout with empty cart
   - Screenshot: empty-cart-checkout.png
   - Apply invalid promo code
   - Screenshot: invalid-promo.png
   - Apply expired promo code
   - Screenshot: expired-promo.png
   - Browser back during checkout
   - Screenshot: checkout-back.png

5. REPORT
   - List all errors found
   - Note if error messages are helpful
   - Flag any crashes or data loss"
```

## Accessibility Test

```bash
browser-use run "Accessibility audit:

1. IMAGES
   - Check product images have alt text
   - Screenshot: img-alt-check.png

2. FORMS
   - Check all inputs have labels
   - Check error messages are clear
   - Screenshot: form-labels.png

3. CONTRAST
   - Check text is readable
   - Check button text contrasts with background
   - Screenshot: contrast-check.png

4. KEYBOARD NAVIGATION
   - Navigate using Tab key
   - Can reach all interactive elements?
   - Focus indicators visible?
   - Screenshot: keyboard-nav.png

5. REPORT
   - List accessibility issues
   - Reference WCAG guidelines"
```

## Performance Test

```bash
browser-use run "Performance testing:

1. HOMEPAGE LOAD
   - Navigate to homepage
   - Measure load time
   - Screenshot: perf-homepage.png
   - Check Core Web Vitals indicators if available

2. PRODUCT PAGE LOAD
   - Navigate to product page
   - Measure load time
   - Screenshot: perf-pdp.png
   - Check image loading speed

3. CART PERFORMANCE
   - Add item, measure response time
   - Screenshot: perf-add-cart.png
   - Update quantity, measure response
   - Screenshot: perf-update-qty.png

4. CHECKOUT PERFORMANCE
   - Navigate checkout steps
   - Measure each step load time
   - Screenshot: perf-checkout.png

5. REPORT
   - Load times for each page
   - Flag anything > 3 seconds
   - Note layout shifts"
```

## Search & Filter Test

```bash
browser-use run "Test search and filtering:

1. SEARCH FUNCTIONALITY
   - Search for common term (e.g., 'black glasses')
   - Screenshot: search-results.png
   - Check: Relevant results
   - Check: No results message if applicable
   - Search with typo
   - Screenshot: search-typo.png
   - Check: Did you mean suggestions?

2. FILTERING
   - Apply price filter
   - Screenshot: filter-price.png
   - Check: Results update correctly
   - Apply multiple filters
   - Screenshot: filter-multiple.png
   - Check: Filter combination works
   - Clear filters
   - Screenshot: filter-clear.png
   - Check: Returns to full results

3. SORTING
   - Sort by price low-high
   - Screenshot: sort-price-asc.png
   - Check: Correct order
   - Sort by price high-low
   - Screenshot: sort-price-desc.png
   - Sort by newest
   - Screenshot: sort-newest.png

4. REPORT
   - List any search/filter bugs
   - Note UX improvements"
```

## User Account Flow

```bash
browser-use run "Test user account features:

1. REGISTRATION
   - Navigate to register page
   - Screenshot: register-page.png
   - Fill registration form
   - Test password requirements
   - Submit registration
   - Screenshot: register-success.png
   - Check: Welcome email mentioned

2. LOGIN
   - Log out
   - Navigate to login
   - Screenshot: login-page.png
   - Enter wrong password
   - Screenshot: login-error.png
   - Check: Error message (not too specific)
   - Enter correct credentials
   - Screenshot: login-success.png

3. ACCOUNT DASHBOARD
   - View account dashboard
   - Screenshot: account-dashboard.png
   - Check: Orders visible
   - Check: Address book accessible
   - Check: Password change option

4. ORDER HISTORY
   - View order history
   - Screenshot: order-history.png
   - Click on order
   - Screenshot: order-detail.png
   - Check: Tracking info if available

5. ADDRESS MANAGEMENT
   - Add new address
   - Screenshot: add-address.png
   - Edit existing address
   - Screenshot: edit-address.png
   - Delete address
   - Screenshot: delete-address.png

6. REPORT
   - List account feature issues
   - Note UX friction points"
```
