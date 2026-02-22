#!/usr/bin/env python3
"""Simple Playwright script to navigate Wikipedia and click I'm Feeling Lucky"""
import asyncio
from playwright.async_api import async_playwright

async def main():
    print("🚀 Starting browser...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("🌐 Navigating to Wikipedia...")
        await page.goto("https://wikipedia.org")
        
        print("📄 Getting page title...")
        title = await page.title()
        print(f"Page title: {title}")
        
        print("\n🔍 Looking for 'I'm Feeling Lucky' button...")
        # Try to find the button by text
        lucky_button = await page.query_selector('text="I\'m Feeling Lucky"')
        
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
            await page.screenshot(path="/root/.openclaw/workspace/wikipedia_home.png")
            print("📸 Screenshot saved to wikipedia_home.png")
            
            # Print all buttons on the page
            buttons = await page.query_selector_all("button")
            print(f"\nFound {len(buttons)} buttons:")
            for i, btn in enumerate(buttons[:10]):
                text = await btn.text_content()
                print(f"  {i}: {text}")
        
        await browser.close()
        print("\n✅ Browser closed")

if __name__ == "__main__":
    asyncio.run(main())
