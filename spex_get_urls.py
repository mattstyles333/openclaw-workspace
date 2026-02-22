#!/usr/bin/env python3
"""Get actual product URLs from collection page"""
import os
os.environ['DISPLAY'] = ':99'

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    page = browser.new_page(viewport={'width': 1280, 'height': 900})
    
    # Go to rimless glasses collection
    page.goto("https://spex4less.com/collections/rimless-glasses", wait_until="networkidle")
    page.wait_for_timeout(2000)
    
    print(f"On page: {page.url}")
    print(f"Title: {page.title()}")
    
    # Get all links
    links = page.locator("a[href]").all()
    print(f"\nFound {len(links)} links")
    
    # Find product links (exclude navigation, footer, etc)
    product_urls = []
    for link in links:
        href = link.get_attribute("href")
        if href and href.startswith("/") and "/collections/" not in href:
            # Check if it looks like a product
            text = link.text_content().strip()
            # Product links usually have prices or names
            if text and ("£" in text or len(text) > 10):
                full_url = f"https://spex4less.com{href}"
                if full_url not in [u for u, t in product_urls]:
                    product_urls.append((full_url, text[:40]))
    
    print(f"\nFound {len(product_urls)} potential products:")
    for i, (url, text) in enumerate(product_urls[:5]):
        print(f"  {i}: {url}")
        print(f"     Text: {text}")
    
    # Try first product
    if product_urls:
        url, text = product_urls[0]
        print(f"\nNavigating to: {url}")
        page.goto(url, wait_until="networkidle")
        
        print(f"Page title: {page.title()}")
        print(f"Final URL: {page.url}")
        
        page.screenshot(path="/root/.openclaw/workspace/spex_actual_product.png", full_page=True)
        print("✓ Screenshot saved: spex_actual_product.png")
    
    browser.close()
