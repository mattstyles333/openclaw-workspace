#!/usr/bin/env python3
"""Proper navigation through Spex4Less"""
import os
os.environ['DISPLAY'] = ':99'

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--no-sandbox', '--disable-setuid-sandbox']
    )
    page = browser.new_page(viewport={'width': 1280, 'height': 900})
    
    # 1. HOMEPAGE
    print("Loading homepage...")
    page.goto("https://spex4less.com", wait_until="networkidle")
    
    # Accept cookies first
    try:
        accept_btn = page.locator("button:has-text('Accept Cookies')").first
        if accept_btn.is_visible():
            accept_btn.click()
            page.wait_for_timeout(1000)
            print("✓ Cookies accepted")
    except:
        pass
    
    page.screenshot(path="/root/.openclaw/workspace/spex_home.png")
    
    # 2. CLICK MEN'S GLASSES FROM NAVIGATION
    print("\nClicking Men's Glasses...")
    glasses_menu = page.locator("a:has-text('Glasses')").first
    if glasses_menu.is_visible():
        glasses_menu.hover()
        page.wait_for_timeout(500)
        
        # Look for Men's in dropdown
        mens_link = page.locator("a:has-text('Men')").first
        if mens_link.is_visible():
            mens_link.click()
            page.wait_for_load_state("networkidle")
            page.screenshot(path="/root/.openclaw/workspace/spex_mens.png", full_page=True)
            print(f"✓ Men's page loaded: {page.url}")
    
    # 3. CLICK A PRODUCT
    print("\nClicking a product...")
    product = page.locator(".product a, [data-product] a, .product-item a").first
    if product:
        product.click()
        page.wait_for_load_state("networkidle")
        page.screenshot(path="/root/.openclaw/workspace/spex_product.png", full_page=True)
        print(f"✓ Product page: {page.title()[:50]}")
        
        # Get price
        price_elem = page.locator(".price, .product-price, [data-price]").first
        if price_elem.is_visible():
            print(f"  Price: {price_elem.text_content().strip()}")
    
    browser.close()

print("\n✅ Screenshots saved:")
print("  - spex_home.png")
print("  - spex_mens.png")
print("  - spex_product.png")
