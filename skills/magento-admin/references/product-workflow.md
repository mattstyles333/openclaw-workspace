# Product Check Workflow

## Step-by-Step

1. **Navigate to Products**
   ```
   https://sadmx.spex4less.com/monadminx472/catalog/product/
   ```

2. **Search for Product**
   - By SKU (e.g., "RAY-BAN-RB2132-52")
   - By name (e.g., "Ray-Ban New Wayfarer")
   - By ID (if known)

3. **Review Product Details**

### General Tab
- Name: [Product name]
- SKU: [Stock keeping unit]
- Price: £XX.XX
- Status: Enabled/Disabled
- Visibility: Catalog, Search

### Images
- Main image present?
- Gallery images (multiple angles)?
- Image quality acceptable?

### Attributes (Key for Eyewear)
- Frame Width
- Bridge Width
- Temple Length
- Frame Color
- Lens Color
- Frame Material
- Gender
- Age Group

### Configurations (If configurable product)
- Size options (S, M, L)
- Color options
- Each variant has own SKU and stock

### Inventory
- Stock quantity
- Stock status (In/Out of stock)
- Backorders allowed?

### SEO
- URL key
- Meta title/description
- Properly configured?

## Common Product Issues

| Issue | Check |
|-------|-------|
| Missing images | Are photos uploaded? |
| Wrong price | Compare to website |
| Out of stock | Inventory = 0? |
| Disabled | Status field |
| Missing attributes | Size/color not set? |
| No variants | Configurations missing? |
| SEO issues | URL key blank? |

## QA Checklist for Products

- [ ] Enabled and visible
- [ ] Images present and clear
- [ ] Price correct
- [ ] All attributes filled
- [ ] Stock > 0 (if expecting sales)
- [ ] Variants configured (if applicable)
- [ ] Description complete
- [ ] SEO fields filled
