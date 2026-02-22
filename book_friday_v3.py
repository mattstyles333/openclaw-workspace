#!/usr/bin/env python3
"""Book Court 1, 6-7pm on FRIDAY"""
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
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(3)
        print("✅ Logged in")
        
        # Click Bookings
        await page.click("text='Bookings'")
        await asyncio.sleep(3)
        await page.screenshot(path="01_bookings.png")
        
        # Click Book Now
        await page.click("button:has-text('Book Now')")
        await asyncio.sleep(3)
        await page.screenshot(path="02_calendar.png")
        print("📸 Calendar loaded (Tennis)")
        
        # Select Squash from dropdown
        print("🏸 Changing to Squash...")
        await page.select_option("select", "Squash")
        await asyncio.sleep(2)
        print("✅ Squash selected")
        
        # Navigate to Friday by clicking the next arrow 3 times
        print("📆 Navigating to Friday...")
        for i in range(3):
            try:
                # Click the right arrow next to the date
                await page.click("button[class*='next'], .next-date, button:has-text('>')")
                await asyncio.sleep(1)
            except:
                pass
        
        await asyncio.sleep(2)
        await page.screenshot(path="03_friday.png")
        print("📸 Date should be Friday now")
        
        # Refresh calendar
        print("🔄 Refreshing...")
        await page.click("button:has-text('Refresh Calendar')")
        await asyncio.sleep(3)
        await page.screenshot(path="04_calendar_ready.png")
        print("📸 Friday Squash calendar")
        
        # Click Court 1, 18:00-19:00
        print("🎯 Clicking Court 1, 18:00-19:00...")
        cells = await page.locator("table td").all()
        for cell in cells:
            text = await cell.text_content()
            if text and ("18:00" in text and "19:00" in text):
                print(f"  Found: {text.strip()}")
                try:
                    await cell.click()
                    print("  ✅ Clicked!")
                    break
                except Exception as e:
                    print(f"  Failed: {e}")
        
        await asyncio.sleep(3)
        await page.screenshot(path="05_popup.png")
        
        # Click EXTEND
        print("➕ Extending...")
        try:
            await page.click("button:has-text('Extend')", timeout=5000)
            print("✅ Extended")
        except:
            print("  ℹ️ No extend")
        
        await page.screenshot(path="06_extended.png")
        
        # Click BOOK
        print("✅ Booking...")
        try:
            await page.click("button:has-text('Book')", timeout=5000)
            print("🎉 BOOKED!")
        except Exception as e:
            print(f"  ⚠️ {e}")
        
        await asyncio.sleep(3)
        await page.screenshot(path="07_final.png")
        
        await browser.close()
        print("\n✅ Done!")

asyncio.run(book_court())
