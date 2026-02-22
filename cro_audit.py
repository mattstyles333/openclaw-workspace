#!/usr/bin/env python3
import asyncio
import time
from browser_use import Agent, Browser, BrowserConfig, ActionResult
from browser_use.browser.browser import BrowserContext
from browser_use.browser.context import BrowserContextConfig
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    # Configure browser with headless=False to see what's happening
    config = BrowserConfig(
        headless=False,
        disable_security=False,
        extra_args=[],
    )
    browser = Browser(config=config)
    context = await browser.new_context(
        BrowserContextConfig(
            viewport={'width': 1280, 'height': 720},
        )
    )
    
    # Navigate to homepage with basic auth
    start = time.time()
    page = await context.new_page()
    # Basic auth via URL
    response = await page.goto('https://test:test@test.s4l.link')
    if response and response.status != 200:
        print(f"Failed to load homepage: {response.status}")
    else:
        load_time = time.time() - start
        print(f"Homepage load time: {load_time:.2f}s")
        if load_time > 3:
            print("WARNING: Homepage load time >3s")
    
    # Take screenshot of homepage
    await page.screenshot(path='homepage.png', full_page=True)
    
    # Evaluate trust signals on homepage (look for reviews, security badges)
    # We'll check for common selectors
    trust_selectors = [
        '.reviews', '.testimonials', '.trustpilot', '.badge', '.security-badge',
        'img[alt*="secure"]', 'img[alt*="ssl"]', 'img[alt*="trust"]'
    ]
    trust_found = []
    for selector in trust_selectors:
        elements = await page.query_selector_all(selector)
        if elements:
            trust_found.append(selector)
    print(f"Trust signals found: {trust_found}")
    
    # Navigate to a product page (assume there's a product link)
    # Find first product link
    product_link = await page.query_selector('a[href*="/product"], a[href*="/shop"], .product a')
    if product_link:
        product_href = await product_link.get_attribute('href')
        print(f"Found product link: {product_href}")
        start = time.time()
        await page.goto(product_href)
        load_time = time.time() - start
        print(f"Product page load time: {load_time:.2f}s")
        await page.screenshot(path='product_page.png', full_page=True)
        
        # Check for reviews, security badges on product page
        trust_found_product = []
        for selector in trust_selectors:
            elements = await page.query_selector_all(selector)
            if elements:
                trust_found_product.append(selector)
        print(f"Trust signals on product page: {trust_found_product}")
        
        # Add to cart (assuming there's an add to cart button)
        add_to_cart = await page.query_selector('button[class*="add-to-cart"], #add-to-cart, .add-to-cart')
        if add_to_cart:
            await add_to_cart.click()
            await page.wait_for_timeout(1000)
            # Go to cart page
            cart_link = await page.query_selector('a[href*="/cart"], .cart')
            if cart_link:
                await cart_link.click()
                await page.wait_for_timeout(2000)
                await page.screenshot(path='cart_page.png', full_page=True)
                # Check security indicators on cart page
                security_indicators = await page.query_selector_all('.secure, .lock, img[alt*="secure"], .security')
                print(f"Security indicators on cart page: {len(security_indicators)}")
                
                # Checkout button
                checkout = await page.query_selector('button[class*="checkout"], #checkout, .checkout')
                if checkout:
                    await checkout.click()
                    await page.wait_for_timeout(2000)
                    await page.screenshot(path='checkout_page.png', full_page=True)
                    
                    # Count checkout form fields
                    form_fields = await page.query_selector_all('input, select, textarea')
                    print(f"Checkout form field count: {len(form_fields)}")
                    
                    # Look for progress indicator
                    progress = await page.query_selector('.progress, .step, .progress-bar, .checkout-progress')
                    if progress:
                        print("Progress indicator present")
                    else:
                        print("Progress indicator NOT present")
                    
                    # Look for error messages (try to submit empty form to see errors)
                    # We'll just check for existing error messages
                    errors = await page.query_selector_all('.error, .alert, .warning, .validation')
                    print(f"Error message elements present: {len(errors)}")
                    if errors:
                        for err in errors[:2]:
                            text = await err.text_content()
                            print(f"Error text: {text[:100]}")
                    
                    # Look for exit opportunities (links away from checkout)
                    exit_links = await page.query_selector_all('a[href*="/"], a[href*="http"]')
                    exit_count = len(exit_links)
                    print(f"Exit opportunities (links) on checkout page: {exit_count}")
                    
                    # Price clarity: look for hidden fees elements
                    hidden_fee_selectors = ['.fee', '.surcharge', '.tax', '.shipping', '.additional']
                    hidden_fees = []
                    for sel in hidden_fee_selectors:
                        els = await page.query_selector_all(sel)
                        if els:
                            hidden_fees.append(sel)
                    print(f"Potential hidden fee elements: {hidden_fees}")
                else:
                    print("Checkout button not found")
            else:
                print("Cart link not found")
        else:
            print("Add to cart button not found")
    else:
        print("No product link found")
    
    await browser.close()

if __name__ == '__main__':
    asyncio.run(main())