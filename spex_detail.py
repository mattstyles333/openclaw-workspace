#!/usr/bin/env python3
"""Click product with better selectors"""
import os
os.environ['DISPLAY'] = ':99'

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    page = browser.new_page(viewport={'width': 1280, 'height': 900})
    
    # Go to a glasses collection
    page.goto("https://spex4less.com/collections/all-glasses", wait_until="networkidle")
    page.wait_for_timeout(2000)
    
    # Accept cookies
    try:
        accept = page.locator("text='Accept Cookies'").first
        if accept.is_visible():
            accept.click()
            page.wait_for_timeout(500)
    except:
        pass
    
    print(f"Page title: {page.title()}")
    print(f"URL: {page.url}")
    
    # Find all links
    links = page.locator("a").all()
    print(f"\nTotal links: {len(links)}")
    
    # Look for product links
    product_links = []
    for link in links[:30]:
        href = link.get_attribute("href")
        if href and ("/products/" in href or "/collections/" not in href and "-" in href):
            text = link.text_content().strip()[:40]
            if text and len(text) > 5:
                product_links.append((href, text))
                print(f"  Link: {href[:60]} - {text}")
    
    # Click first interesting link
    if product_links:
        print(f"\nClicking: {product_links[0][0]}")
        page.goto(product_links[0][0], wait_until="networkidle")
        page.screenshot(path="/root/.openclaw/workspace/spex_detail.png", full_page=True)
        print("✓ Screenshot: spex_detail.png")
        print(f"New URL: {page.url}")
        print(f"New title: {page.title()}")
    
    browser.close()
