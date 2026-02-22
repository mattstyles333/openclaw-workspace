#!/usr/bin/env python3
"""Navigate Spex4Less and capture key pages"""
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
    print("Capturing homepage...")
    page.goto("https://spex4less.com", wait_until="networkidle")
    page.screenshot(path="/root/.openclaw/workspace/spex4less_homepage.png")
    
    # 2. MEN'S GLASSES - Try direct URL
    print("Capturing Men's glasses...")
    page.goto("https://spex4less.com/mens-glasses", wait_until="networkidle")
    page.screenshot(path="/root/.openclaw/workspace/spex4less_mens.png", full_page=True)
    
    # Count products on page
    products = page.locator(".product-item").count()
    print(f"  Products found: {products}")
    
    # 3. CLICK FIRST PRODUCT
    print("Capturing product page...")
    first_product = page.locator(".product-item a").first
    if first_product.is_visible():
        first_product.click()
        page.wait_for_load_state("networkidle")
        page.screenshot(path="/root/.openclaw/workspace/spex4less_product.png", full_page=True)
        
        # Get product info
        name = page.locator("h1").text_content()
        price = page.locator(".price").first.text_content() if page.locator(".price").first.is_visible() else "N/A"
        print(f"  Product: {name[:50]}...")
        print(f"  Price: {price}")
    
    # 4. PRESCRIPTION OPTIONS
    print("Looking for prescription options...")
    rx_section = page.locator("text=/Select Lens Type|Prescription|Lens Options/i").first
    if rx_section.is_visible():
        page.screenshot(path="/root/.openclaw/workspace/spex4less_prescription.png")
        print("  ✓ Prescription section found")
    
    # 5. CHECKOUT/CART
    print("Checking cart...")
    cart_btn = page.locator("a[href*='cart'], .cart-icon").first
    if cart_btn.is_visible():
        cart_btn.click()
        page.wait_for_load_state("networkidle")
        page.screenshot(path="/root/.openclaw/workspace/spex4less_cart.png")
        print("  ✓ Cart page captured")
    
    browser.close()

print("\n✅ Screenshots captured:")
print("  - spex4less_homepage.png")
print("  - spex4less_mens.png")
print("  - spex4less_product.png")
print("  - spex4less_prescription.png")
print("  - spex4less_cart.png")
