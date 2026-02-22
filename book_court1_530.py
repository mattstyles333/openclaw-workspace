#!/usr/bin/env python3
"""Book Court 1, 5:30-6:30pm on Friday"""
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
        await page.click("button[type='submit']")
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(3)
        
        # Navigate to Bookings
        print("📅 Going to Bookings...")
        await page.click("a:has-text('Book')")
        await asyncio.sleep(2)
        
        # Click Book Now
        print("📅 Clicking Book Now...")
        await page.click("button:has-text('Book Now')")
        await asyncio.sleep(3)
        
        # Select Squash from dropdown
        print("🏸 Selecting Squash...")
        await page.select_option("select", "Squash")
        await asyncio.sleep(2)
        
        # Click Refresh Calendar
        print("🔄 Refreshing calendar...")
        await page.click("button:has-text('Refresh Calendar')")
        await asyncio.sleep(3)
        
        # Take screenshot before booking
        await page.screenshot(path="before_booking.png")
        print("📸 Screenshot: before_booking.png")
        
        # Try to click on Court 1, 17:30-18:00 slot
        print("🎯 Clicking Court 1, 17:30-18:00 slot...")
        try:
            # Try clicking the cell with the time text
            await page.click("td:has-text('17:30 - 18:00'):nth-of-type(2)", timeout=5000)
            print("✅ Clicked 17:30-18:00 slot")
        except:
            try:
                # Try xpath
                await page.click("xpath=//td[contains(text(), '17:30 - 18:00')][1]")
                print("✅ Clicked 17:30-18:00 slot (xpath)")
            except Exception as e:
                print(f"  ❌ Could not click: {e}")
        
        await asyncio.sleep(2)
        await page.screenshot(path="after_first_click.png")
        
        # Look for extend button or second slot selection
        print("➕ Looking for extend/book options...")
        content = await page.content()
        
        # Check if we got a booking dialog
        if "book" in content.lower() or "confirm" in content.lower():
            print("🎉 Booking dialog appeared!")
            await page.screenshot(path="booking_dialog.png")
        
        # Try clicking extend if available
        try:
            await page.click("button:has-text('Extend'), a:has-text('Extend'), input[value*='Extend']", timeout=3000)
            print("✅ Extended to 1 hour")
        except:
            print("  ℹ️ No extend button found")
        
        # Try to complete booking
        print("✅ Looking for Confirm/Book button...")
        try:
            await page.click("button:has-text('Confirm'), button:has-text('Book'), input[value='Book']", timeout=5000)
            print("🎉 BOOKING SUBMITTED!")
        except:
            print("  ⚠️ Could not find book button")
        
        await asyncio.sleep(3)
        await page.screenshot(path="final_result.png")
        print("📸 Screenshot: final_result.png")
        
        await browser.close()
        print("✅ Done")

asyncio.run(book_court())
