#!/usr/bin/env python3
"""
Mobile QA test for https://test.s4l.link with viewport 390x844
"""
import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Add workspace .venv to path
sys.path.insert(0, '/root/.openclaw/workspace/.venv/lib/python3.13/site-packages')
try:
    from browser_use import Browser
except ImportError as e:
    print(f"ERROR: Failed to import browser_use: {e}")
    print("Make sure browser-use is installed. Try: pip install browser-use")
    sys.exit(1)

SCREENSHOT_DIR = Path("/root/.openclaw/workspace/screenshots_mobile")
SCREENSHOT_DIR.mkdir(exist_ok=True)

VIEWPORT = {'width': 390, 'height': 844}
BASE_URL = "https://test.s4l.link"
AUTH_URL = f"https://test:test@{BASE_URL.split('://')[1]}"

async def take_screenshot(page, step_name: str) -> str:
    """Take screenshot and return filename"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = SCREENSHOT_DIR / f"{step_name}_{timestamp}.png"
    await page.screenshot(path=str(filename))
    print(f"  Screenshot: {filename.name}")
    return str(filename)

async def step_navigate(page):
    """Step 1: Navigate with mobile viewport"""
    print("Step 1: Navigating to site with mobile viewport")
    await page.goto(AUTH_URL)
    await page.wait_for_load_state('networkidle')
    # Set viewport
    await page.set_viewport_size(VIEWPORT)
    # Wait a bit for page to adjust
    await asyncio.sleep(2)
    screenshot = await take_screenshot(page, "1_navigation")
    return {'step': 1, 'screenshot': screenshot, 'url': page.url}

async def step_hamburger_menu(page):
    """Step 2: Test hamburger menu opens/closes"""
    print("Step 2: Testing hamburger menu")
    # Try to find hamburger button (common selectors)
    selectors = [
        'button[aria-label*="menu"]',
        'button[aria-label*="Menu"]',
        'button[aria-label*="navigation"]',
        'button[aria-label*="Navigation"]',
        '[data-testid*="menu"]',
        '[class*="hamburger"]',
        '[class*="menu-button"]',
        'button:has(svg)',
        'button:has(>svg)',
        'button:has(>span)',
    ]
    button = None
    for selector in selectors:
        elements = await page.locator(selector).all()
        if elements:
            button = elements[0]
            break
    if not button:
        # Fallback: first button on page
        buttons = await page.locator('button').all()
        if buttons:
            button = buttons[0]
    
    if not button:
        return {'step': 2, 'error': 'No button found for hamburger menu'}
    
    # Click to open
    await button.click()
    await asyncio.sleep(1)
    open_screenshot = await take_screenshot(page, "2_menu_open")
    
    # Click again to close (or click outside)
    # Try clicking same button
    await button.click()
    await asyncio.sleep(1)
    closed_screenshot = await take_screenshot(page, "2_menu_closed")
    
    return {'step': 2, 'screenshot_open': open_screenshot, 'screenshot_closed': closed_screenshot}

async def step_touch_interactions(page):
    """Step 3: Test touch interactions on buttons (are they tappable?)"""
    print("Step 3: Testing touch interactions on buttons")
    # Find all interactive elements: buttons, links, inputs
    buttons = await page.locator('button').all()
    links = await page.locator('a').all()
    interactive = buttons + links
    
    results = []
    for i, element in enumerate(interactive[:10]):  # limit to 10
        # Get bounding box to check size
        bbox = await element.bounding_box()
        if bbox:
            width, height = bbox['width'], bbox['height']
            # Check minimum tap target size (44x44)
            tap_target_ok = width >= 44 and height >= 44
            # Try to click (should work if visible/enabled)
            try:
                await element.click(timeout=2000)
                clickable = True
                await asyncio.sleep(0.5)
                # Go back? Might navigate away
                # Instead, we'll just note if click succeeded
            except Exception as e:
                clickable = False
                print(f"    Element {i} not clickable: {e}")
            results.append({
                'index': i,
                'type': 'button' if element in buttons else 'link',
                'size': f"{width}x{height}",
                'tap_target_ok': tap_target_ok,
                'clickable': clickable
            })
    
    screenshot = await take_screenshot(page, "3_touch_interactions")
    return {'step': 3, 'screenshot': screenshot, 'results': results}

async def step_product_gallery_swipe(page):
    """Step 4: Test product image gallery swipe"""
    print("Step 4: Testing product image gallery swipe")
    # Need to navigate to a product page first
    # Search for product links
    product_links = await page.locator('a[href*="product"], a[href*="item"]').all()
    if product_links:
        await product_links[0].click()
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)
        screenshot1 = await take_screenshot(page, "4_product_page")
        # Look for image gallery
        gallery_selectors = [
            '[class*="gallery"]',
            '[class*="carousel"]',
            '[class*="slider"]',
            '.slick-slider',
            '.swiper',
        ]
        gallery = None
        for selector in gallery_selectors:
            if await page.locator(selector).count() > 0:
                gallery = selector
                break
        if gallery:
            # Try to simulate swipe (drag)
            gallery_element = page.locator(gallery).first
            bbox = await gallery_element.bounding_box()
            if bbox:
                start_x = bbox['x'] + bbox['width'] * 0.8
                start_y = bbox['y'] + bbox['height'] * 0.5
                end_x = bbox['x'] + bbox['width'] * 0.2
                await page.mouse.move(start_x, start_y)
                await page.mouse.down()
                await page.mouse.move(end_x, start_y, steps=10)
                await page.mouse.up()
                await asyncio.sleep(1)
                screenshot2 = await take_screenshot(page, "4_gallery_swipe")
                return {'step': 4, 'screenshots': [screenshot1, screenshot2], 'gallery_found': True}
        return {'step': 4, 'screenshots': [screenshot1], 'gallery_found': False}
    else:
        screenshot = await take_screenshot(page, "4_no_products")
        return {'step': 4, 'error': 'No product links found'}

async def step_add_to_cart(page):
    """Step 5: Add to cart on mobile"""
    print("Step 5: Adding to cart")
    # Assume we are on product page from previous step
    # Look for add to cart button
    add_buttons = await page.locator('button:has-text("Add to Cart"), button:has-text("Add to Bag"), button:has-text("Buy")').all()
    if not add_buttons:
        add_buttons = await page.locator('button').all()
    
    if add_buttons:
        await add_buttons[0].click()
        await asyncio.sleep(2)
        screenshot = await take_screenshot(page, "5_add_to_cart")
        # Check if cart updated (look for cart count)
        cart_count = await page.locator('[class*="cart-count"], [class*="bag-count"]').first.inner_text() if await page.locator('[class*="cart-count"]').count() > 0 else None
        return {'step': 5, 'screenshot': screenshot, 'cart_count': cart_count}
    else:
        screenshot = await take_screenshot(page, "5_no_add_button")
        return {'step': 5, 'error': 'No add to cart button found'}

async def step_checkout_form_keyboard(page):
    """Step 6: Test checkout form with keyboard open (does keyboard block inputs?)"""
    print("Step 6: Testing checkout form keyboard")
    # Navigate to cart/checkout
    cart_links = await page.locator('a[href*="cart"], a[href*="checkout"], a:has-text("Cart"), a:has-text("Checkout")').all()
    if cart_links:
        await cart_links[0].click()
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)
        screenshot1 = await take_screenshot(page, "6_checkout_page")
        # Find first input field
        input_fields = await page.locator('input[type="text"], input[type="email"], input[type="tel"]').all()
        if input_fields:
            await input_fields[0].click()
            await asyncio.sleep(1)
            screenshot2 = await take_screenshot(page, "6_keyboard_open")
            # Check if input is visible (keyboard may cover)
            bbox = await input_fields[0].bounding_box()
            viewport = page.viewport_size
            # Rough check: if input's bottom is near viewport bottom, keyboard may cover
            input_bottom = bbox['y'] + bbox['height']
            viewport_height = viewport['height']
            keyboard_may_block = input_bottom > viewport_height * 0.6
            # Press escape to close keyboard (if possible)
            await page.keyboard.press('Escape')
            return {'step': 6, 'screenshots': [screenshot1, screenshot2], 'keyboard_may_block': keyboard_may_block}
        else:
            return {'step': 6, 'screenshots': [screenshot1], 'error': 'No input fields found'}
    else:
        screenshot = await take_screenshot(page, "6_no_checkout")
        return {'step': 6, 'error': 'No cart/checkout link found'}

async def step_date_pickers_dropdowns(page):
    """Step 7: Test date pickers and dropdowns"""
    print("Step 7: Testing date pickers and dropdowns")
    # Look for date inputs
    date_inputs = await page.locator('input[type="date"], input[type="datetime-local"]').all()
    dropdowns = await page.locator('select').all()
    
    date_results = []
    for inp in date_inputs[:2]:
        try:
            await inp.click()
            await asyncio.sleep(1)
            screenshot = await take_screenshot(page, "7_date_picker_open")
            # Close picker
            await page.keyboard.press('Escape')
            date_results.append({'type': 'date', 'screenshot': screenshot})
        except Exception as e:
            date_results.append({'type': 'date', 'error': str(e)})
    
    dropdown_results = []
    for sel in dropdowns[:2]:
        try:
            options = await sel.locator('option').all()
            if options:
                await sel.select_option(value=await options[0].get_attribute('value'))
                await asyncio.sleep(0.5)
                screenshot = await take_screenshot(page, "7_dropdown_selected")
                dropdown_results.append({'type': 'dropdown', 'screenshot': screenshot})
        except Exception as e:
            dropdown_results.append({'type': 'dropdown', 'error': str(e)})
    
    return {'step': 7, 'date_pickers': date_results, 'dropdowns': dropdown_results}

async def main():
    print(f"Starting mobile QA test with viewport {VIEWPORT['width']}x{VIEWPORT['height']}")
    print(f"Screenshots will be saved in {SCREENSHOT_DIR}")
    
    browser = Browser(headless=False)  # Show browser for debugging
    page = None
    try:
        page = await browser.new_page()
        await page.set_viewport_size(VIEWPORT)
        
        results = []
        
        # Step 1
        result1 = await step_navigate(page)
        results.append(result1)
        
        # Step 2
        result2 = await step_hamburger_menu(page)
        results.append(result2)
        
        # Step 3
        result3 = await step_touch_interactions(page)
        results.append(result3)
        
        # Step 4
        result4 = await step_product_gallery_swipe(page)
        results.append(result4)
        
        # Step 5
        result5 = await step_add_to_cart(page)
        results.append(result5)
        
        # Step 6
        result6 = await step_checkout_form_keyboard(page)
        results.append(result6)
        
        # Step 7
        result7 = await step_date_pickers_dropdowns(page)
        results.append(result7)
        
        print("\n" + "="*50)
        print("TEST COMPLETE")
        print("="*50)
        
        # Summary
        mobile_experience_rating = 0
        issues = []
        for r in results:
            if 'error' in r:
                issues.append(f"Step {r['step']}: {r['error']}")
            if 'tap_target_ok' in r and not r['tap_target_ok']:
                issues.append(f"Step {r['step']}: tap target too small")
            if 'keyboard_may_block' in r and r['keyboard_may_block']:
                issues.append(f"Step {r['step']}: keyboard may block input")
        
        # Rate experience 1-10 based on issues
        if len(issues) == 0:
            mobile_experience_rating = 9
        elif len(issues) <= 2:
            mobile_experience_rating = 7
        elif len(issues) <= 5:
            mobile_experience_rating = 5
        else:
            mobile_experience_rating = 3
        
        # Output structured findings
        findings = {
            'viewport': VIEWPORT,
            'steps': results,
            'issues': issues,
            'mobile_experience_rating': mobile_experience_rating,
            'screenshot_directory': str(SCREENSHOT_DIR)
        }
        
        print("\nSTRUCTURED FINDINGS:")
        print(f"Mobile Experience Rating: {mobile_experience_rating}/10")
        print(f"Issues found: {len(issues)}")
        for issue in issues:
            print(f"  - {issue}")
        print(f"Screenshots saved in {SCREENSHOT_DIR}")
        
        # Return findings for subagent
        return findings
        
    except Exception as e:
        print(f"ERROR during test: {e}")
        import traceback
        traceback.print_exc()
        return {'error': str(e)}
    finally:
        if page:
            await page.close()
        await browser.close()

if __name__ == "__main__":
    findings = asyncio.run(main())
    # Print JSON for subagent to parse
    import json
    print("\n=== FINDINGS JSON ===")
    print(json.dumps(findings, indent=2))