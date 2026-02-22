#!/usr/bin/env python3
"""Click on a product and analyze lens selection"""
import os
os.environ['DISPLAY'] = ':99'

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    page = browser.new_page(viewport={'width': 1280, 'height': 900})
    
    # Start at homepage
    page.goto("https://spex4less.com", wait_until="networkidle")
    page.wait_for_timeout(2000)
    
    # Accept cookies
    try:
        accept = page.locator("text='Accept Cookies'").first
        if accept.is_visible():
            accept.click()
            page.wait_for_timeout(500)
    except:
        pass
    
    # Scroll to products
    page.evaluate("window.scrollTo(0, 800)")
    page.wait_for_timeout(1500)
    
    # Close popup if present
    try:
        close_btn = page.locator("button.close, .modal-close, [aria-label='Close']").first
        if close_btn.is_visible():
            close_btn.click()
            page.wait_for_timeout(500)
    except:
        pass
    
    # Click on Ray-Ban product
    print("Clicking Ray-Ban product...")
    rayban = page.locator("text='Ray-Ban RX7047'").first
    if rayban.is_visible():
        rayban.click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        print(f"Product page loaded: {page.url}")
        print(f"Title: {page.title()}")
        
        page.screenshot(path="/root/.openclaw/workspace/spex_product_final.png", full_page=True)
        print("✓ Screenshot saved")
        
        # Look for lens selection elements
        print("\n🔍 Analyzing page for lens selection...")
        
        # Common selectors for lens/prescription options
        selectors = [
            "button:has-text('Select')",
            "button:has-text('Lenses')",
            "button:has-text('Prescription')",
            "button:has-text('Buy')",
            "button:has-text('Add')",
            "a:has-text('Select')",
            "select",
            "[data-lens]",
            "[data-prescription]",
            ".lens-option",
            ".prescription"
        ]
        
        found = False
        for selector in selectors:
            elems = page.locator(selector).all()
            if elems:
                print(f"\n✓ Found with '{selector}':")
                for elem in elems[:3]:
                    text = elem.text_content().strip()[:50]
                    visible = elem.is_visible()
                    print(f"   - '{text}' (visible: {visible})")
                    if not found and visible:
                        found = True
                        print("   🖱️  Clicking this element...")
                        elem.click()
                        page.wait_for_timeout(2000)
                        page.screenshot(path="/root/.openclaw/workspace/spex_lens_options.png", full_page=True)
                        print("   ✓ Lens options screenshot saved")
                        break
        
        if not found:
            print("\n⚠️  No lens selection elements found with standard selectors")
            print("\nAll buttons on page:")
            buttons = page.locator("button").all()
            for btn in buttons[:10]:
                text = btn.text_content().strip()
                if text:
                    print(f"   - '{text}'")
    else:
        print("Ray-Ban product not found")
    
    browser.close()
    print("\n✅ Done")
