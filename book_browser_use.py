#!/usr/bin/env python3
"""Use browser-use Python API to book the court"""
import asyncio
from browser_use import Agent, Browser

async def book_court():
    browser = Browser()
    
    try:
        page = await browser.new_page()
        
        print("🌐 Opening SmartClubCloud...")
        await page.goto("https://www.smartclubcloud.com/")
        await asyncio.sleep(2)
        
        print("🔑 Logging in...")
        await page.fill("input[type='text']", "matthew.styles.1963")
        await page.fill("input[type='password']", "James333")
        await page.click("input[type='submit']")
        await asyncio.sleep(3)
        
        print("📅 Navigating to Bookings...")
        await page.click("text='Bookings'")
        await asyncio.sleep(2)
        
        # Get all buttons
        buttons = await page.locator("button").all()
        print(f"Found {len(buttons)} buttons")
        
        for i, btn in enumerate(buttons):
            text = await btn.text_content()
            if text and "Book Now" in text:
                print(f"  Clicking button {i}: {text}")
                await btn.click()
                break
        
        await asyncio.sleep(5)
        await page.screenshot(path="browser_use_test.png")
        print(f"URL: {page.url}")
        
    finally:
        await browser.close()
    
    print("✅ Done")

if __name__ == "__main__":
    asyncio.run(book_court())
