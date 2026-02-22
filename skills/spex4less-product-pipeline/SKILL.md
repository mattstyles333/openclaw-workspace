---
name: spex4less-product-pipeline
description: "Orchestrate Spex4Less product data pipeline: scrape supplier data → validate → upload to Magento 2. Uses supplier_scraper and product_upload CLI tools from GitLab. NOT for: general web scraping, non-eyewear products, or suppliers not in the supported list."
metadata:
  {
    "openclaw":
      {
        "emoji": "👓",
        "requires": { "bins": ["python3"], "skills": ["glab"] },
        "tools": ["bash", "read", "write"]
      },
  }
---

# Spex4Less Product Pipeline

Orchestrate the complete supplier-to-Magento workflow for eyewear products.

## Supported Suppliers

| Supplier | Method | Auth Required |
|----------|--------|---------------|
| **Inspecs** | Scraping + POST API | Username/Password |
| **Kering** | Excel + Scraping | Username/Password |
| **Marcolin** | API (2-stage) | Username/Password |
| **Maui Jim** | Scraping + PDF/AI | None (Public) |

## Workflow

```
1. SCRAPE   → Run supplier_scraper for target supplier
2. VALIDATE → Check extracted data quality
3. PREPARE  → Run product_upload supplier command
4. RECONCILE→ Compare with existing M2 products (optional)
5. UPLOAD   → Upload to Magento 2
```

## Phase 1: Scrape Supplier Data

```bash
cd /root/supplier_scraper

# Scrape specific supplier
python -m src.main --supplier <name> --output /root/product_upload/data/supplier/

# Supported: inspecs, kering, marcolin, mauijim
```

**Output:** JSON files with standardized product data

## Phase 2: Validate Data

```bash
cd /root/product_upload

# Validate supplier data
python -m product_upload.cli supplier validate <supplier_name>

# Check for missing required fields
# Required: sku, brand, product_url, base_image_url, size, color, price, ean/upc/gtin
```

## Phase 3: Prepare for Magento

```bash
cd /root/product_upload

# Prepare supplier data (transform to M2 format)
python -m product_upload.cli supplier <supplier_name>

# Output: data/processed/<supplier>/magento_ready.json
```

## Phase 4: Reconcile (Optional but Recommended)

```bash
cd /root/product_upload

# Compare with existing M2 products
python -m product_upload.cli reconcile compare <supplier_name>

# Plan: CREATE, UPDATE, DELETE, NO_CHANGE
# Review the reconciliation report before upload
```

## Phase 5: Upload to Magento

```bash
cd /root/product_upload

# Upload products (respects reconcile plan if exists)
python -m product_upload.cli m2 upload <supplier_name>

# Or upload with reconciliation filter
python -m product_upload.cli m2 upload <supplier_name> --reconciled

# Upload images separately (if needed)
python -m product_upload.cli m2 upload-images <supplier_name>
```

## Usage

```
User: "Get latest products from Marcolin and upload to M2"
→ Scrape Marcolin
→ Validate data
→ Prepare for Magento
→ Reconcile (show plan)
→ Upload to M2
→ Report: X created, Y updated, Z unchanged
```

```
User: "Update stock for Kering products"
→ Scrape Kering (quick mode if available)
→ Validate
→ Prepare
→ Reconcile (focus on stock changes)
→ Upload with --reconciled flag
```

## Safety Checks

**Always do before upload:**
1. ✅ Validate data quality (no missing required fields)
2. ✅ Run reconcile to see planned changes
3. ✅ Get user approval for CREATE/UPDATE/DELETE counts
4. ⚠️  Never auto-approve DELETE operations without review

## Common Issues

| Issue | Fix |
|-------|-----|
| Missing required fields | Check scraper output, re-scrape with `--full` |
| Auth errors | Verify .env credentials for supplier |
| M2 upload fails | Check MAGENTO_API_URL and MAGENTO_API_KEY in .env |
| Image upload fails | Verify image URLs are accessible |
| Reconcile shows unexpected DELETE | Review orphaned products carefully |

## Post-Upload

```bash
# Verify in Magento Admin
check products by SKU
verify images loaded
confirm stock quantities

# Report to user
Summary: Created X, Updated Y, Unchanged Z, Errors W
```

## Environment Requirements

Both tools need their .env files configured:

**supplier_scraper/.env:**
```
INSPECS_USERNAME=
INSPECS_PASSWORD=
KERING_USERNAME=
KERING_PASSWORD=
MARCOLIN_USERNAME=
MARCOLIN_PASSWORD=
# Maui Jim needs no auth
```

**product_upload/.env:**
```
MAGENTO_API_URL=https://magento.s4l.link/rest/V1
MAGENTO_API_KEY=
```

## Aliases

Add to shell profile:
```bash
alias scrape='cd /root/supplier_scraper && python -m src.main'
alias m2upload='cd /root/product_upload && python -m product_upload.cli'
```
