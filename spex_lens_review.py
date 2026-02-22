#!/usr/bin/env python3
"""Navigate to product and analyze lens selection process"""
import os
os.environ['DISPLAY'] = ':99'

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--no-sandbox', '--disable-setuid-sandbox']
    )
    page = browser.new_page(viewport={'width': 1280, 'height': 900})
    
    print("=" * 70)
    print("🔍 SPEX4LESS LENS SELECTION PROCESS REVIEW")
    print("=" * 70)
    
    # 1. Go to homepage
    print("\n📍 Loading Spex4Less...")
    page.goto("https://spex4less.com", wait_until="networkidle")
    
    # Accept cookies
    try:
        accept_btn = page.locator("button:has-text('Accept Cookies')").first
        if accept_btn.is_visible(timeout=3000):
            accept_btn.click()
            page.wait_for_timeout(500)
    except:
        pass
    
    # 2. Click Men's Glasses
    print("\n📍 Clicking Men's Glasses...")
    mens_btn = page.locator("a:has-text('Men')").filter(has=page.locator("text='Glasses'")).first
    if not mens_btn.is_visible():
        # Try simpler selector
        mens_btn = page.locator("text='Men' >> visible=true").first
    
    if mens_btn.is_visible():
        mens_btn.click()
        page.wait_for_load_state("networkidle")
        print(f"   Navigated to: {page.url}")
    else:
        print("   Trying direct URL...")
        page.goto("https://spex4less.com/glasses/men", wait_until="networkidle")
    
    # 3. Click first product
    print("\n📍 Selecting a product...")
    products = page.locator("a[href*='/products/'], .product a, [data-product] a").all()
    if products:
        print(f"   Found {len(products)} products")
        products[0].click()
        page.wait_for_load_state("networkidle")
        
        product_name = page.locator("h1").text_content()
        print(f"   Product: {product_name[:50]}")
        print(f"   URL: {page.url}")
        
        page.screenshot(path="/root/.openclaw/workspace/spex_product_page.png")
        print("   ✓ Screenshot saved: spex_product_page.png")
    else:
        print("   No products found")
        browser.close()
        exit()
    
    # 4. Look for lens/prescription options
    print("\n📍 Looking for 'Select Lenses' or prescription options...")
    
    # Try various selectors
    lens_buttons = [
        "button:has-text('Select')",
        "button:has-text('Lenses')",
        "button:has-text('Prescription')",
        "a:has-text('Select')",
        "[data-lenses]",
        ".select-lenses"
    ]
    
    lens_btn = None
    for selector in lens_buttons:
        elem = page.locator(selector).first
        if elem.is_visible():
            lens_btn = elem
            print(f"   ✓ Found: {selector}")
            break
    
    if lens_btn:
        print("\n📸 Taking screenshot before clicking...")
        page.screenshot(path="/root/.openclaw/workspace/spex_before_lenses.png")
        
        print("   🖱️  Clicking lens selection...")
        lens_btn.click()
        page.wait_for_timeout(2000)
        page.wait_for_load_state("networkidle")
        
        print(f"   New URL: {page.url}")
        print(f"   Title: {page.title()}")
        
        page.screenshot(path="/root/.openclaw/workspace/spex_lens_selection.png", full_page=True)
        print("   ✓ Screenshot saved: spex_lens_selection.png")
        
        # Analyze the lens options
        print("\n📍 Analyzing lens options...")
        
        # Look for lens types
        lens_types = page.locator("text=/Single Vision|Bifocal|Varifocal/i").all()
        print(f"   Lens types found: {len(lens_types)}")
        for i, lt in enumerate(lens_types[:3]):
            print(f"     - {lt.text_content().strip()}")
        
        # Look for prescription entry
        prescription_form = page.locator("input[name*='sphere'], input[name*='cyl'], select[name*='axis']").count()
        print(f"   Prescription input fields: {prescription_form}")
        
        if prescription_form > 0:
            print("   ✓ Prescription entry form detected")
        
        # Look for PD (pupillary distance)
        pd_field = page.locator("text=/PD|Pupillary/i").count()
        print(f"   PD references: {pd_field}")
        
        # Check for coatings/options
        coatings = page.locator("text=/Anti-reflective|Scratch|UV|Blue Light/i").count()
        print(f"   Coating options: {coatings}")
        
        # Check for pricing
        prices = page.locator("text=/£[0-9]+/").all()
        print(f"   Price points found: {len(prices)}")
        for i, price in enumerate(prices[:5]):
            print(f"     - {price.text_content().strip()}")
    else:
        print("   ⚠️  No lens selection button found")
        print("   Available buttons on page:")
        buttons = page.locator("button, a").all()
        for i, btn in enumerate(buttons[:10]):
            text = btn.text_content().strip()[:40]
            if text:
                print(f"     {i}: {text}")
    
    browser.close()

print("\n" + "=" * 70)
print("✅ LENS SELECTION REVIEW COMPLETE")
print("=" * 70)
