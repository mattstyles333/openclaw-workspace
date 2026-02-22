#!/usr/bin/env python3
"""Navigate from homepage to find product"""
import os
os.environ['DISPLAY'] = ':99'

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    page = browser.new_page(viewport={'width': 1280, 'height': 900})
    
    # Go to homepage
    page.goto("https://spex4less.com", wait_until="networkidle")
    
    # Accept cookies
    try:
        accept = page.locator("button:has-text('Accept Cookies')").first
        if accept.is_visible():
            accept.click()
            page.wait_for_timeout(500)
    except:
        pass
    
    # Scroll down to see products
    page.evaluate("window.scrollTo(0, 800)")
    page.wait_for_timeout(1000)
    
    # Find product links
    links = page.locator("a[href]").all()
    product_links = []
    for link in links:
        href = link.get_attribute("href")
        if href and ("/products/" in href or "/p/" in href or "-glasses" in href):
            text = link.text_content().strip()[:30]
            product_links.append((href, text))
    
    print(f"Found {len(product_links)} potential product links:")
    for i, (href, text) in enumerate(product_links[:10]):
        print(f"  {i}: {href} - {text}")
    
    # Click first product
    if product_links:
        print(f"\nClicking: {product_links[0][0]}")
        page.goto(product_links[0][0], wait_until="networkidle")
        
        print(f"Page title: {page.title()}")
        print(f"URL: {page.url}")
        
        page.screenshot(path="/root/.openclaw/workspace/spex_real_product.png", full_page=True)
        print("✓ Screenshot saved: spex_real_product.png")
    
    browser.close()
