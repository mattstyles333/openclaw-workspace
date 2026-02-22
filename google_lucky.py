#!/usr/bin/env python3
"""Navigate to Google and click I'm Feeling Lucky"""
import asyncio
from playwright.async_api import async_playwright

async def main():
    print("🚀 Starting browser...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("🌐 Navigating to Google...")
        await page.goto("https://google.com")
        
        print("📄 Getting page title...")
        title = await page.title()
        print(f"Page title: {title}")
        
        # Accept cookies if prompted (EU/UK users)
        try:
            accept_button = await page.query_selector('text="Accept all"')
            if accept_button:
                print("🍪 Accepting cookies...")
                await accept_button.click()
                await asyncio.sleep(1)
        except:
            pass
        
        print("\n🔍 Looking for 'I'm Feeling Lucky' button...")
        # Try multiple selectors
        lucky_button = None
        
        # Try by text content
        lucky_button = await page.query_selector('text=/I\'m Feeling Lucky/i')
        
        if not lucky_button:
            # Try by input value
            lucky_button = await page.query_selector('input[value*="Lucky" i]')
        
        if not lucky_button:
            # Try by name attribute
            lucky_button = await page.query_selector('[name="btnI"]')
        
        if lucky_button:
            print("✅ Found 'I'm Feeling Lucky' button!")
            print("🖱️  Clicking it...")
            await lucky_button.click()
            
            # Wait for navigation
            print("⏳ Waiting for navigation...")
            await page.wait_for_load_state("networkidle")
            
            # Get the new page info
            new_url = page.url
            new_title = await page.title()
            
            print(f"\n🎉 Landed on: {new_url}")
            print(f"Page title: {new_title}")
            
            # Take screenshot
            await page.screenshot(path="/root/.openclaw/workspace/lucky_result.png")
            print("📸 Screenshot saved to lucky_result.png")
        else:
            print("⚠️  'I'm Feeling Lucky' button not found")
            # Take screenshot to see what's on the page
            await page.screenshot(path="/root/.openclaw/workspace/google_home.png")
            print("📸 Screenshot saved to google_home.png")
            
            # Print all buttons/inputs on the page
            inputs = await page.query_selector_all("input[type='submit']")
            print(f"\nFound {len(inputs)} submit buttons:")
            for i, inp in enumerate(inputs[:5]):
                value = await inp.get_attribute("value")
                name = await inp.get_attribute("name")
                print(f"  {i}: value='{value}', name='{name}'")
        
        await browser.close()
        print("\n✅ Browser closed")

if __name__ == "__main__":
    asyncio.run(main())
