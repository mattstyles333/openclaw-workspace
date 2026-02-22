#!/usr/bin/env python3
"""Try to navigate to products via homepage"""
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
    
    # Get current URL state
    print(f"Homepage: {page.url}")
    print(f"Title: {page.title()}")
    
    # Look for any clickable products on homepage
    page.evaluate("window.scrollTo(0, 600)")
    page.wait_for_timeout(1000)
    
    # Take screenshot to see what's available
    page.screenshot(path="/root/.openclaw/workspace/spex_home_scroll.png")
    print("Screenshot saved: spex_home_scroll.png")
    
    # Look for images that might be products
    images = page.locator("img").all()
    print(f"Found {len(images)} images")
    
    # Look for product containers
    products = page.locator("[data-product], .product, .product-item, [data-item]").all()
    print(f"Found {len(products)} product elements")
    
    browser.close()
