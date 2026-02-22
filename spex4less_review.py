#!/usr/bin/env python3
"""Navigate Spex4Less as a consumer and provide feedback"""
import os
os.environ['DISPLAY'] = ':99'

from playwright.sync_api import sync_playwright

feedback = []
screenshots = []

def take_screenshot(page, name):
    path = f"/root/.openclaw/workspace/spex4less_{name}.png"
    page.screenshot(path=path, full_page=True)
    screenshots.append(name)
    return path

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--no-sandbox', '--disable-setuid-sandbox']
    )
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    
    print("=" * 60)
    print("🕶️  SPEX4LESS CUSTOMER JOURNEY REVIEW")
    print("=" * 60)
    
    # === HOMEPAGE ===
    print("\n📍 STEP 1: Homepage (First Impressions)")
    page.goto("https://spex4less.com", wait_until="networkidle")
    take_screenshot(page, "01_homepage")
    
    title = page.title()
    print(f"   Page Title: {title}")
    feedback.append(f"**Homepage:** Title is '{title}' - {'✅ Clear' if 'glasses' in title.lower() or 'spex' in title.lower() else '⚠️ Could be more descriptive about glasses/eyewear'}")
    
    # Check main headline/hero
    hero = page.locator("h1").first
    if hero.is_visible():
        hero_text = hero.text_content()
        print(f"   Hero Text: {hero_text[:80]}...")
        feedback.append(f"**Hero Section:** H1 says '{hero_text[:50]}...' - captures attention")
    
    # Check for CTA buttons
    ctas = page.locator("a, button").filter(has_text="Shop").count()
    ctas += page.locator("a, button").filter(has_text="Browse").count()
    print(f"   Shop/Browse CTAs found: {ctas}")
    feedback.append(f"**CTAs:** Found {ctas} shop/browse buttons - {'✅ Good' if ctas > 0 else '⚠️ Add clear call-to-action buttons'}")
    
    # === PRODUCT CATEGORY PAGE ===
    print("\n📍 STEP 2: Finding Glasses (Category Navigation)")
    
    # Try to find and click on "Men's Glasses" or similar
    try:
        mens_link = page.locator("a:has-text('Men')").first
        if mens_link.is_visible():
            print("   Found Men's category, clicking...")
            mens_link.click()
            page.wait_for_load_state("networkidle")
            take_screenshot(page, "02_mens_glasses")
            feedback.append("**Navigation:** Men's glasses category accessible ✅")
        else:
            # Try any glasses link
            glasses_link = page.locator("a:has-text('Glasses')").first
            if glasses_link.is_visible():
                glasses_link.click()
                page.wait_for_load_state("networkidle")
                take_screenshot(page, "02_glasses_category")
                feedback.append("**Navigation:** Glasses category found ✅")
    except Exception as e:
        feedback.append(f"**Navigation:** ⚠️ Could not easily find glasses category - {e}")
    
    # === PRODUCT PAGE ===
    print("\n📍 STEP 3: Product Selection")
    
    try:
        # Look for product listings
        products = page.locator(".product, [data-product], .item").all()
        if not products:
            # Try alternative selectors
            products = page.locator("a[href*='/product'], a[href*='/glasses']").all()[:6]
        
        print(f"   Products found: {len(products)}")
        
        if len(products) > 0:
            feedback.append(f"**Product Grid:** Found {len(products)} products displayed ✅")
            
            # Click first product
            print("   Clicking first product...")
            products[0].click()
            page.wait_for_load_state("networkidle")
            take_screenshot(page, "03_product_page")
            
            # Check for product details
            price = page.locator(".price, [data-price], .amount").first
            if price.is_visible():
                price_text = price.text_content()
                print(f"   Price displayed: {price_text}")
                feedback.append(f"**Product Page:** Price clearly shown ({price_text}) ✅")
            else:
                feedback.append("**Product Page:** ⚠️ Price not immediately visible")
            
            # Check for "Add to Cart" or similar
            add_cart = page.locator("button:has-text('Add'), button:has-text('Buy'), a:has-text('Add')").first
            if add_cart.is_visible():
                feedback.append("**Product Page:** Add to cart button present ✅")
            else:
                feedback.append("**Product Page:** ⚠️ No clear 'Add to Cart' button found")
                
        else:
            feedback.append("**Product Grid:** ⚠️ No products found on category page")
    except Exception as e:
        feedback.append(f"**Product Selection:** ⚠️ Error browsing products - {e}")
    
    # === PRESCRIPTION/LENS OPTIONS ===
    print("\n📍 STEP 4: Prescription/Lens Options")
    
    try:
        # Look for prescription-related elements
        prescription_elements = page.locator("text=/prescription|lens|RX/i").count()
        print(f"   Prescription-related elements: {prescription_elements}")
        
        if prescription_elements > 0:
            feedback.append(f"**Prescription:** Found {prescription_elements} prescription/lens related elements ✅")
        else:
            feedback.append("**Prescription:** ⚠️ Prescription options not immediately visible")
    except:
        feedback.append("**Prescription:** Could not evaluate prescription flow")
    
    # === CHECKOUT/CART ===
    print("\n📍 STEP 5: Cart/Checkout Process")
    
    try:
        # Look for cart icon/link
        cart = page.locator("a[href*='cart'], .cart, [data-cart]").first
        if cart.is_visible():
            print("   Cart icon found")
            feedback.append("**Cart:** Shopping cart accessible ✅")
        else:
            feedback.append("**Cart:** ⚠️ Shopping cart not prominently displayed")
    except:
        feedback.append("**Cart:** Could not evaluate cart accessibility")
    
    # === MOBILE RESPONSIVENESS CHECK ===
    print("\n📍 STEP 6: Mobile Responsiveness")
    
    page.set_viewport_size({'width': 375, 'height': 667})  # iPhone size
    page.goto("https://spex4less.com", wait_until="networkidle")
    take_screenshot(page, "06_mobile_homepage")
    
    # Check for mobile menu
    mobile_menu = page.locator(".menu-toggle, .hamburger, [data-toggle='menu']").first
    if mobile_menu.is_visible():
        feedback.append("**Mobile:** Hamburger menu present for mobile navigation ✅")
    else:
        feedback.append("**Mobile:** ⚠️ No obvious mobile menu button")
    
    browser.close()

# === PRINT FEEDBACK REPORT ===
print("\n" + "=" * 60)
print("📋 WEBSITE FEEDBACK REPORT")
print("=" * 60)

for item in feedback:
    print(f"\n• {item}")

print("\n" + "=" * 60)
print("🎯 KEY RECOMMENDATIONS")
print("=" * 60)
print("""
1. **First Impressions:**
   - Hero section should clearly communicate value prop
   - Make sure primary CTA stands out (contrasting color)

2. **Navigation:**
   - Ensure "Shop Glasses" is prominently displayed
   - Consider filtering by face shape, style, or price

3. **Product Pages:**
   - High-quality images are crucial (multiple angles)
   - Clear pricing with lens options explained
   - "Virtual try-on" feature would be a game-changer

4. **Prescription Flow:**
   - Make the prescription entry process intuitive
   - Explain PD (pupillary distance) clearly
   - Offer prescription upload/photo option

5. **Trust Signals:**
   - Add customer reviews/testimonials
   - Show "As seen on" or media mentions
   - Clear return policy and warranty info

6. **Mobile Experience:**
   - Ensure touch targets are large enough
   - Simplify mobile checkout流程
""")

print(f"\n📸 Screenshots captured: {', '.join(screenshots)}")
print("=" * 60)
