#!/usr/bin/env python3
"""Click into a specific product"""
import os
os.environ['DISPLAY'] = ':99'

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    page = browser.new_page(viewport={'width': 1280, 'height': 900})
    
    # Go to rimless glasses page
    page.goto("https://spex4less.com/collections/rimless-glasses", wait_until="networkidle")
    
    # Accept cookies
    try:
        accept = page.locator("button:has-text('Accept Cookies')").first
        if accept.is_visible():
            accept.click()
            page.wait_for_timeout(500)
    except:
        pass
    
    print("On category page, clicking first product...")
    
    # Click first product
    first_product = page.locator(".product-item a, .product-card a, .product a").first
    if first_product.is_visible():
        first_product.click()
        page.wait_for_load_state("networkidle")
        
        print(f"Product page loaded")
        print(f"Title: {page.title()}")
        print(f"URL: {page.url}")
        
        # Take screenshot
        page.screenshot(path="/root/.openclaw/workspace/spex_individual_product.png", full_page=True)
        print("✓ Screenshot saved: spex_individual_product.png")
        
        # Look for lens selection
        print("\nLooking for lens/prescription options...")
        buttons = page.locator("button, a").all()
        for btn in buttons:
            text = btn.text_content().strip().lower()
            if any(word in text for word in ['lens', 'prescription', 'select', 'buy', 'add']):
                print(f"  Found: '{btn.text_content().strip()}'")
    else:
        print("No product found to click")
    
    browser.close()
