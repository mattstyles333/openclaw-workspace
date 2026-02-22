#!/usr/bin/env python3
"""Book Court 1, 6-7pm on FRIDAY - Click the handy date shortcut"""
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
        
        # Click on Bookings tile
        print("📅 Clicking Bookings...")
        await page.click("text='Bookings'")
        await asyncio.sleep(3)
        await page.screenshot(path="01_bookings.png")
        
        # Click Book Now
        print("📅 Clicking Book Now...")
        await page.click("button:has-text('Book Now'), .btn:has-text('Book Now')")
        await asyncio.sleep(3)
        await page.screenshot(path="02_calendar.png")
        print("📸 Calendar loaded")
        
        # Select Squash
        print("🏸 Selecting Squash...")
        await page.select_option("select", "Squash")
        await asyncio.sleep(2)
        print("✅ Squash selected")
        
        # Click the "Fri 20 Feb" handy shortcut button
        print("📆 Clicking 'Fri 20 Feb' shortcut...")
        try:
            await page.click("button:has-text('Fri 20 Feb'), .btn:has-text('Fri 20 Feb'), text='Fri 20 Feb'")
            print("✅ Clicked Fri 20 Feb")
            await asyncio.sleep(2)
        except Exception as e:
            print(f"  ⚠️ Could not click shortcut: {e}")
        
        await page.screenshot(path="03_friday.png")
        
        # Refresh calendar
        print("🔄 Refreshing calendar...")
        await page.click("button:has-text('Refresh')")
        await asyncio.sleep(3)
        await page.screenshot(path="04_friday_calendar.png")
        print("📸 Friday calendar loaded")
        
        # Click on Court 1, 18:00-19:00 (6-7pm) slot
        print("🎯 Clicking Court 1, 18:00-19:00 (6-7pm)...")
        
        cells = await page.locator("table td").all()
        for i, cell in enumerate(cells):
            text = await cell.text_content()
            # Look for 18:00-19:00 or similar
            if text and ("18:00 - 19:00" in text or "18:00-19:00" in text):
                print(f"  Found Court slot: {text.strip()}")
                try:
                    await cell.click()
                    print("  ✅ Clicked!")
                    break
                except Exception as e:
                    print(f"  Click failed: {e}")
        
        await asyncio.sleep(3)
        await page.screenshot(path="05_popup.png")
        print("📸 Popup should be visible")
        
        # Look for EXTEND button in popup
        print("➕ Looking for EXTEND button...")
        try:
            await page.click("button:has-text('Extend'):visible, .btn:has-text('Extend'):visible", timeout=5000)
            print("✅ Extended to 1 hour")
            await asyncio.sleep(2)
        except Exception as e:
            print(f"  ℹ️ No extend button: {e}")
        
        await page.screenshot(path="06_extended.png")
        
        # Click BOOK button
        print("✅ Clicking BOOK button...")
        try:
            await page.click("button:has-text('Book'):visible, .btn:has-text('Book'):visible", timeout=5000)
            print("🎉 BOOKED!")
        except Exception as e:
            print(f"  ⚠️ Could not click Book: {e}")
        
        await asyncio.sleep(3)
        await page.screenshot(path="07_final.png")
        print("📸 Final screenshot")
        
        await browser.close()
        print("\n✅ Done!")

asyncio.run(book_court())
