#!/usr/bin/env python3
"""Book Court 1, 6-7pm Friday - Force click approach"""
import asyncio
from playwright.async_api import async_playwright

USERNAME = "matthew.styles.1963"
PASSWORD = "James333"

async def book_court():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("🌐 Opening SmartClubCloud...")
        await page.goto("https://www.smartclubcloud.com/")
        await page.wait_for_selector("input[type='text']", timeout=15000)
        
        print("🔑 Logging in...")
        await page.fill("input[type='text']", USERNAME)
        await page.fill("input[type='password']", PASSWORD)
        await page.click("input[type='submit']")
        await asyncio.sleep(3)
        print("✅ Logged in")
        
        # Click Bookings
        print("📅 Clicking Bookings...")
        await page.click("text='Bookings'")
        await asyncio.sleep(2)
        await page.screenshot(path="01_bookings.png")
        
        # Click Book Now with force
        print("📅 Clicking Book Now (force)...")
        try:
            btn = page.locator("button:has-text('Book Now')")
            count = await btn.count()
            print(f"  Found {count} Book Now buttons")
            if count > 0:
                await btn.first.click(force=True)
                print("  ✅ Clicked!")
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        await asyncio.sleep(5)
        await page.screenshot(path="02_after_click.png")
        
        # Check if we're on the calendar page
        url = page.url
        print(f"  URL: {url}")
        
        content = await page.content()
        if "Calendar" in content or "courts" in content.lower():
            print("  ✅ Calendar page loaded!")
        else:
            print("  ⚠️ Still on Bookings page")
        
        await browser.close()
        print("\n✅ Done")

asyncio.run(book_court())
