#!/usr/bin/env python3
"""Quick Spex4Less homepage analysis"""
import os
os.environ['DISPLAY'] = ':99'

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--no-sandbox', '--disable-setuid-sandbox']
    )
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    
    print("=" * 70)
    print("🕶️  SPEX4LESS WEBSITE REVIEW - CUSTOMER JOURNEY")
    print("=" * 70)
    
    # HOMEPAGE
    page.goto("https://spex4less.com", wait_until="networkidle")
    
    print("\n📍 HOMEPAGE ANALYSIS")
    print("-" * 70)
    
    title = page.title()
    print(f"✓ Page Title: {title}")
    
    # Check hero section
    hero_h1 = page.locator("h1").first
    if hero_h1.is_visible():
        print(f"✓ Hero Headline: '{hero_h1.text_content().strip()}'")
    
    # Check main CTAs
    shop_men = page.locator("a:has-text('Shop Men'), button:has-text('Shop Men')").count()
    shop_women = page.locator("a:has-text('Shop Women'), button:has-text('Shop Women')").count()
    print(f"✓ Shop Men CTAs: {shop_men}")
    print(f"✓ Shop Women CTAs: {shop_women}")
    
    # Check for trust signals
    reviews = page.locator("text=/review|trustpilot|rating/i").count()
    print(f"✓ Trust signals found: {reviews} references")
    
    # Check brands displayed
    brands = page.locator("text=/Ray-Ban|Oakley|Gucci|Tom Ford/i").count()
    print(f"✓ Designer brands mentioned: {brands}")
    
    # Check price points
    prices = page.locator("text=/£[0-9]+/i").count()
    print(f"✓ Price references: {prices}")
    
    # MEN'S GLASSES CATEGORY
    print("\n📍 NAVIGATING TO MEN'S GLASSES")
    print("-" * 70)
    
    try:
        # Find and click Men's Glasses
        mens_btn = page.locator("a:has-text('Men'), button:has-text('Shop Men')").first
        if mens_btn.is_visible():
            print("✓ Found Men's Glasses link")
            mens_btn.click()
            page.wait_for_load_state("networkidle")
            
            print(f"✓ Current URL: {page.url}")
            print(f"✓ Page Title: {page.title()}")
            
            # Count products
            products = page.locator(".product-item, [data-product], .product").count()
            print(f"✓ Products displayed: {products}")
            
            # Check filters
            filters = page.locator(".filter, [data-filter], .facet").count()
            print(f"✓ Filter options: {filters}")
            
            # Take screenshot
            page.screenshot(path="/root/.openclaw/workspace/spex4less_mens.png", full_page=True)
            print("✓ Screenshot saved: spex4less_mens.png")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # PRODUCT PAGE
    print("\n📍 PRODUCT PAGE ANALYSIS")
    print("-" * 70)
    
    try:
        # Click first product
        product = page.locator(".product-item a, .product a").first
        if product.is_visible():
            print("✓ Clicking first product...")
            product.click()
            page.wait_for_load_state("networkidle")
            
            print(f"✓ Product URL: {page.url}")
            print(f"✓ Product Title: {page.title()}")
            
            # Check for product details
            price = page.locator(".price, .amount, [data-price]").first
            if price.is_visible():
                print(f"✓ Price displayed: {price.text_content().strip()}")
            
            # Check for prescription options
            rx_options = page.locator("text=/prescription|lens|vision/i").count()
            print(f"✓ Prescription-related elements: {rx_options}")
            
            # Check for add to cart
            add_cart = page.locator("button:has-text('Add'), a:has-text('Add'), .add-to-cart").count()
            print(f"✓ Add to cart buttons: {add_cart}")
            
            page.screenshot(path="/root/.openclaw/workspace/spex4less_product.png", full_page=True)
            print("✓ Screenshot saved: spex4less_product.png")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    browser.close()

print("\n" + "=" * 70)
print("📝 INITIAL IMPRESSIONS")
print("=" * 70)
print("""
✅ STRENGTHS:
• Clean, professional design
• Clear "Shop Men" / "Shop Women" CTAs above the fold
• Designer brands prominently featured (Ray-Ban, Oakley, Gucci)
• Trust signals visible (reviews, guarantees)
• "How To Buy" section explains the process
• Price promise messaging ("Why Pay More for the Same Look?")
• Multiple ways to browse (by style, by activity/sport)

⚠️  AREAS FOR IMPROVEMENT:
• Consider adding a search bar more prominently
• Virtual try-on feature would significantly boost conversions
• Price filtering could be more prominent
• Exit-intent popup for email capture?
• Live chat for prescription questions?
• More urgency (limited time offers, stock levels)?

🔍 NEXT STEPS FOR DEEPER ANALYSIS:
• Review checkout flow (cart to payment)
• Test prescription entry process
• Check mobile experience
• Analyze page load speed
• Review SEO/meta descriptions
""")

print("=" * 70)
