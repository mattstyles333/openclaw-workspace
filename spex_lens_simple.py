#!/usr/bin/env python3
"""Direct navigation to lens selection"""
import os
os.environ['DISPLAY'] = ':99'

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    page = browser.new_page(viewport={'width': 1280, 'height': 900})
    
    # Navigate to a specific product (Ray-Ban as example)
    print("Loading product page...")
    page.goto("https://spex4less.com/products/ray-ban-rb5169", wait_until="networkidle")
    
    print(f"Page title: {page.title()}")
    print(f"URL: {page.url}")
    
    # Take screenshot of product page
    page.screenshot(path="/root/.openclaw/workspace/spex_product.png", full_page=True)
    print("✓ Product page screenshot saved")
    
    # Look for lens/prescription buttons
    buttons = page.locator("button, a.btn").all()
    print(f"\nFound {len(buttons)} buttons:")
    for i, btn in enumerate(buttons[:15]):
        text = btn.text_content().strip()
        if text:
            print(f"  {i}: {text[:50]}")
    
    # Look for select dropdowns
    selects = page.locator("select").all()
    print(f"\nFound {len(selects)} select dropdowns")
    for i, sel in enumerate(selects[:5]):
        label = sel.get_attribute("name") or sel.get_attribute("id") or f"select_{i}"
        print(f"  - {label}")
    
    browser.close()
    print("\n✓ Done")
