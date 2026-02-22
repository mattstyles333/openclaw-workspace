#!/usr/bin/env python3
"""Navigate to a specific product"""
import os
os.environ['DISPLAY'] = ':99'

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    page = browser.new_page(viewport={'width': 1280, 'height': 900})
    
    # Try common product URL patterns
    urls_to_try = [
        "https://spex4less.com/products/x-rimless",
        "https://spex4less.com/products/aviator-sunglasses",
        "https://spex4less.com/products/ray-ban-chris",
        "https://spex4less.com/x-rimless-glasses",
    ]
    
    for url in urls_to_try:
        print(f"Trying: {url}")
        page.goto(url, wait_until="networkidle")
        
        if "404" not in page.title() and "Not Found" not in page.title():
            print(f"✓ Success! Title: {page.title()}")
            page.screenshot(path="/root/.openclaw/workspace/spex_working_product.png", full_page=True)
            print("✓ Screenshot saved")
            
            # Look for lens options
            print("\nLooking for lens/prescription buttons...")
            buttons = page.locator("button, a.btn, input[type='submit']").all()
            for btn in buttons[:10]:
                text = btn.text_content().strip()
                if text and len(text) < 50:
                    print(f"  - '{text}'")
            
            break
        else:
            print(f"  ✗ 404 - {page.title()}")
    
    browser.close()
