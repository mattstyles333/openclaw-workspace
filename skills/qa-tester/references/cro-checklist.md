# CRO (Conversion Rate Optimization) Checklist

Systematic checks to identify conversion killers on e-commerce sites.

## Page Load Speed

| Check | Target | Impact |
|-------|--------|--------|
| Homepage load | < 2s | High |
| Product page load | < 2s | High |
| Cart page load | < 1.5s | High |
| Checkout load | < 1.5s | Critical |
| Image optimization | WebP format | Medium |
| Lazy loading | Images below fold | Medium |

**Red flags:**
- Blank white screen > 1s
- Layout shifts after load
- Fonts loading slowly (FOUT/FOIT)
- Unoptimized images

## Trust Signals

| Element | Location | Priority |
|---------|----------|----------|
| Reviews/ratings | PDP, near price | Critical |
| Trust badges | Checkout, footer | Critical |
| Secure payment icons | Checkout | Critical |
| Return policy | PDP, cart, checkout | High |
| Money-back guarantee | Homepage, PDP | High |
| Contact info | Header/footer | High |
| About us/story | Footer | Medium |
| SSL certificate | Browser lock | Critical |

**Red flags:**
- No reviews on product pages
- Missing security badges at checkout
- Hidden return policy
- No phone/email visible

## Product Page (PDP)

| Element | Check | Impact |
|---------|-------|--------|
| Price | Above fold, clear | Critical |
| Stock status | Visible (in/out) | High |
| Images | Multiple angles, zoom | Critical |
| Description | Scannable, benefits | High |
| Reviews | Visible, authentic | High |
| Add to Cart | Prominent, contrasting | Critical |
| Size/options | Clear selection | Critical |
| Shipping info | Estimated delivery | High |
| Returns | Policy link | High |
| Related products | Cross-sell | Medium |

**Red flags:**
- Price hidden below fold
- Single product image
- No zoom functionality
- Unclear product options
- Reviews buried
- Weak CTA button

## Cart Page

| Element | Check | Impact |
|---------|-------|--------|
| Item images | Visible | High |
| Prices | Clear, subtotal | Critical |
| Quantity | Easy to change | High |
| Remove | Clear option | Medium |
| Promo code | Field present | Medium |
| Shipping estimate | Calculator | High |
| Trust badges | Security icons | Critical |
| Checkout CTA | Prominent | Critical |
| Continue shopping | Available | Low |
| Save for later | Available | Low |

**Red flags:**
- Hidden shipping costs
- Can't edit quantity easily
- No images of items
- Weak checkout button
- Unexpected fees appear

## Checkout Flow

| Element | Check | Impact |
|---------|-------|--------|
| Progress indicator | Steps shown | High |
| Form fields | Minimal required | Critical |
| Guest checkout | Available | Critical |
| Auto-fill | Address lookup | High |
| Error messages | Clear, helpful | Critical |
| Payment options | Multiple methods | High |
| Security | HTTPS, badges | Critical |
| Order summary | Visible throughout | High |
| Edit cart | Can modify | Medium |
| Save info | For return visits | Low |

**Red flags:**
- Forced account creation
- Too many form fields (>10)
- No progress indicator
- Vague error messages
- Can't see order total
- Hidden fees at final step
- No security indicators

## Mobile-Specific

| Element | Check | Impact |
|---------|-------|--------|
| Tap targets | > 44px | Critical |
| Text size | > 16px (no zoom) | Critical |
| Viewport | No horizontal scroll | Critical |
| Forms | Keyboard friendly | High |
| Buttons | Thumb-reachable | High |
| Images | Optimized size | Medium |
| Menu | Hamburger works | High |
| Sticky CTA | Add to cart visible | High |

**Red flags:**
- Horizontal scrolling
- Tiny tap targets
- Zoom required to read
- Keyboard covers inputs
- Sticky header too large
- Popup covers content

## Navigation

| Element | Check | Impact |
|---------|-------|--------|
| Search | Prominent, works | High |
| Categories | Clear hierarchy | High |
| Filters | Available on PLP | High |
| Breadcrumbs | Present on PDP | Medium |
| Cart icon | Always visible | High |
| Account | Easy access | Medium |

**Red flags:**
- Hidden search
- Confusing category names
- No filters on listing pages
- Deep navigation (3+ clicks to product)

## Psychological Triggers

| Element | Check | Impact |
|---------|-------|--------|
| Scarcity | Stock levels | Medium |
| Urgency | Time-limited offers | Medium |
| Social proof | "X people bought" | Medium |
| Authority | Expert endorsements | Low |
| Reciprocity | Free gift | Low |

**Red flags:**
- Fake scarcity (always "only 2 left")
- Excessive urgency (pressure tactics)
- No social proof at all

## Error Handling

| Scenario | Good UX | Bad UX |
|----------|---------|--------|
| Empty search | Suggestions, categories | "No results" only |
| Out of stock | Notify me, alternatives | Dead end |
| Cart empty | Continue shopping CTA | Error message |
| Form errors | Inline, specific | Page reload, lost data |
| Payment failed | Retry, save cart | Cart cleared |
| 404 page | Search, categories | Generic error |

## Form Optimization

| Best Practice | Implementation |
|---------------|----------------|
| Field count | Minimum required only |
| Auto-fill | Enable browser auto-fill |
| Validation | Real-time, inline |
| Error messages | Specific, helpful |
| Progress saving | Save as user goes |
| Mobile | Appropriate keyboards |
| Labels | Clear, above field |
| Placeholders | Examples, not labels |

## A/B Test Ideas

High-impact tests to consider:

1. **Checkout CTA color** — Red vs green vs brand color
2. **Guest checkout prominence** — Default vs option
3. **Free shipping threshold** — Display vs hide
4. **Product page layout** — Image left vs right
5. **Review placement** — Above fold vs below
6. **Urgency messaging** — With/without countdown
7. **Trust badge placement** — Footer vs checkout
8. **Search bar prominence** — Header center vs right

## CRO Killers (Blockers)

These kill conversions immediately:

- [ ] Page load > 5s
- [ ] Forced account creation
- [ ] Hidden fees at checkout
- [ ] Broken payment flow
- [ ] No mobile optimization
- [ ] No SSL/security
- [ ] Broken search
- [ ] Cart clears on error
- [ ] Can't contact support
- [ ] No return policy

## Scoring

Rate each page 1-10 on:
- Clarity (user knows what to do)
- Friction (ease of completion)
- Trust (would you buy?)
- Speed (technical performance)

**Overall score:**
- 9-10: Ship it
- 7-8: Minor tweaks
- 5-6: Fix before ship
- <5: Major issues, block release
