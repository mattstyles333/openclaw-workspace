#!/usr/bin/env python3
"""Book Court 1, 5:30-6:30pm on FRIDAY"""
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
        
        # Navigate to Bookings
        print("📅 Going to Bookings...")
        await page.click("a:has-text('Book')")
        await asyncio.sleep(2)
        
        # Click Book Now
        print("📅 Clicking Book Now...")
        await page.click("button:has-text('Book Now')")
        await asyncio.sleep(3)
        
        # Select Squash
        print("🏸 Selecting Squash...")
        await page.select_option("select", "Squash")
        await asyncio.sleep(2)
        
        # Navigate to FRIDAY by clicking the date picker
        print("📆 Changing date to Friday 20 Feb...")
        await page.click("input[name='dateStart'], .date-picker, input[placeholder*='Date']")
        await asyncio.sleep(1)
        
        # Try to click on the 20th in the calendar
        try:
            await page.click("text='20'", timeout=3000)
            print("✅ Selected day 20")
        except:
            try:
                await page.click("td:has-text('20'):not(:has(*))", timeout=3000)
                print("✅ Selected day 20 (td)")
            except:
                print("  ⚠️ Could not click day 20, trying next button...")
                # Click next arrow 3 times to get to Friday
                for i in range(3):
                    try:
                        await page.click("[class*='next'], .ui-datepicker-next")
                        await asyncio.sleep(0.5)
                    except:
                        pass
        
        await asyncio.sleep(2)
        
        # Click Done or close date picker
        try:
            await page.click("button:has-text('Done'), .ui-datepicker-close")
        except:
            pass
        
        await asyncio.sleep(2)
        await page.screenshot(path="05_friday_selected.png")
        print("📸 Screenshot: 05_friday_selected.png")
        
        # Refresh calendar
        print("🔄 Refreshing calendar...")
        await page.click("button:has-text('Refresh')")
        await asyncio.sleep(3)
        await page.screenshot(path="06_calendar_friday.png")
        print("📸 Screenshot: 06_calendar_friday.png")
        
        # Click on Court 1, 17:30-18:00 slot
        print("🎯 Clicking Court 1, 17:30-18:00...")
        
        # Look for the cell with "17:30 - 18:00" text in Court 1 column
        # Based on the HTML structure, each cell should be clickable
        cells = await page.locator("td").all()
        for cell in cells:
            text = await cell.text_content()
            if text and "17:30" in text and "18:00" in text:
                # Check if this cell is in Court 1 column
                # Court 1 should be the second column (index 1 after Time column)
                html = await cell.evaluate("el => el.outerHTML")
                print(f"Found cell: {text.strip()}")
                try:
                    await cell.click()
                    print("✅ Clicked the time slot!")
                    break
                except Exception as e:
                    print(f"  Could not click: {e}")
        
        await asyncio.sleep(3)
        await page.screenshot(path="07_slot_clicked.png")
        print("📸 Screenshot: 07_slot_clicked.png")
        
        # Check if a booking dialog appeared
        content = await page.content()
        if "booking" in content.lower() or "confirm" in content.lower():
            print("🎉 Booking dialog appeared!")
        
        # Try to extend and book
        print("➕ Looking for extend option...")
        try:
            await page.click("button:has-text('Extend'), a:has-text('Extend')", timeout=3000)
            print("✅ Extended")
        except:
            print("  ℹ️ No extend option")
        
        print("✅ Looking for Book/Confirm button...")
        try:
            await page.click("button:has-text('Book'), button:has-text('Confirm'):visible", timeout=5000)
            print("🎉 BOOKED!")
        except Exception as e:
            print(f"  ⚠️ Could not book: {e}")
        
        await asyncio.sleep(3)
        await page.screenshot(path="08_final.png")
        print("📸 Screenshot: 08_final.png")
        
        await browser.close()
        print("\n✅ Done - check screenshots!")

asyncio.run(book_court())
