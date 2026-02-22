#!/usr/bin/env python3
"""
Book a squash court at SmartClubCloud for Friday 6-7pm
Run on laptop (not VPS) since VPS IP may be blocked.
"""
import asyncio
from playwright.async_api import async_playwright
from datetime import datetime, timedelta

# Credentials
USERNAME = "matthew.styles.1963"
PASSWORD = "James333"

# Target: This Friday, 6-7pm
today = datetime.now()
days_until_friday = (4 - today.weekday()) % 7
if days_until_friday == 0:
    days_until_friday = 7
friday = today + timedelta(days=days_until_friday)
TARGET_DATE = friday.strftime("%Y-%m-%d")
TARGET_DAY_NAME = friday.strftime("%A %d %B")
TARGET_DATE_DISPLAY = friday.strftime("%d %b %Y")

async def book_court():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        print(f"🌐 Opening smartclubcloud.com...")
        await page.goto("https://www.smartclubcloud.com/")
        
        print("⏳ Waiting for login form...")
        await page.wait_for_selector("input[type='text']", timeout=15000)
        
        print(f"🔑 Logging in as {USERNAME}...")
        await page.fill("input[type='text']", USERNAME)
        await page.fill("input[type='password']", PASSWORD)
        await page.click("button[type='submit']")
        
        print("⏳ Waiting for login...")
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(3)
        await page.screenshot(path="01_after_login.png", full_page=True)
        print("📸 Screenshot: 01_after_login.png")
        
        # Click Bookings tile
        print("📅 Clicking Bookings...")
        await page.click("a:has-text('Bookings'), [href*='booking']")
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(2)
        await page.screenshot(path="02_bookings_page.png", full_page=True)
        print("📸 Screenshot: 02_bookings_page.png")
        
        # Click "Book Now" button
        print("📅 Clicking 'Book Now' button...")
        await page.click("button:has-text('Book Now'), a:has-text('Book Now')")
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(3)
        await page.screenshot(path="03_calendar_page.png", full_page=True)
        print("📸 Screenshot: 03_calendar_page.png")
        
        # Select Squash from dropdown
        print("🏸 Selecting Squash...")
        await page.select_option("select", label="Squash")
        await asyncio.sleep(3)
        await page.screenshot(path="04_squash_selected.png", full_page=True)
        print("📸 Screenshot: 04_squash_selected.png")
        
        # Navigate to Friday by clicking next arrow on date
        print(f"📆 Navigating to Friday ({TARGET_DAY_NAME})...")
        for i in range(days_until_friday):
            try:
                # Look for next date arrow
                await page.click("[class*='next'], .next-arrow, button:has-text('>'), a:has-text('>'), img[alt*='next'], img[title*='next']", timeout=2000)
                await asyncio.sleep(1)
            except:
                # Try clicking on the date input and typing
                try:
                    await page.click("input[name*='date']")
                    await asyncio.sleep(1)
                    await page.fill("input[name*='date']", TARGET_DATE_DISPLAY)
                    await page.press("input[name*='date']", "Enter")
                    await asyncio.sleep(2)
                    break
                except:
                    pass
        
        await asyncio.sleep(2)
        await page.screenshot(path="05_friday_selected.png", full_page=True)
        print("📸 Screenshot: 05_friday_selected.png")
        
        # Refresh calendar
        print("🔄 Refreshing calendar...")
        try:
            await page.click("button:has-text('Refresh')")
            await asyncio.sleep(3)
        except:
            pass
        
        await page.screenshot(path="06_calendar_refreshed.png", full_page=True)
        print("📸 Screenshot: 06_calendar_refreshed.png")
        
        # Click on an available slot at 6pm
        # Looking at the table, we need to click a specific court column in the 18:00-19:00 row
        # Court 1 is the 2nd column, Court 2 is 3rd, Court 3 is 4th, Court 4 is 5th
        print("🕐 Looking for available 6:00pm slot...")
        
        # Try to click on available slots in the 18:00 row
        # We need to target the specific td cells that are empty (white)
        slot_booked = False
        courts = ["Court 1", "Court 2", "Court 3", "Court 4"]
        
        for court_num in range(1, 5):
            try:
                # Try to find the row with 18:00-19:00 and click the court column
                # The table structure: row has th for time, then td for each court
                # We want 18:00-19:00 row which should be the row containing "18:00"
                
                # Try clicking based on the table structure
                # Look for the cell that contains just the time text (available slot)
                cell_selectors = [
                    f"table tbody tr:has(th:has-text('18:00')) td:nth-child({court_num + 1})",
                    f"td:has-text('18:00 - 18:30'):nth-child({court_num + 1})",
                    f"//table//tr[contains(., '18:00')]//td[{court_num}]",
                ]
                
                for selector in cell_selectors:
                    try:
                        if selector.startswith("//"):
                            await page.click(f"xpath={selector}", timeout=3000)
                        else:
                            await page.click(selector, timeout=3000)
                        print(f"✅ Clicked on {courts[court_num-1]} at 6:00pm")
                        slot_booked = True
                        await asyncio.sleep(3)
                        break
                    except:
                        continue
                
                if slot_booked:
                    break
                    
            except Exception as e:
                print(f"  ❌ Could not click Court {court_num}: {e}")
        
        if not slot_booked:
            print("  ⚠️ Could not find available slot - may be fully booked")
        
        await page.screenshot(path="07_slot_clicked.png", full_page=True)
        print("📸 Screenshot: 07_slot_clicked.png")
        
        # Check if a booking dialog/form appeared
        print("🔍 Checking for booking dialog...")
        await asyncio.sleep(2)
        
        # Look for extend option
        print("➕ Looking for EXTEND button...")
        try:
            await page.click("button:has-text('Extend'), a:has-text('Extend'), input[value*='Extend']", timeout=3000)
            print("✅ Clicked EXTEND")
            await asyncio.sleep(2)
        except:
            print("  ℹ️ No extend button found")
        
        await page.screenshot(path="08_extended.png", full_page=True)
        print("📸 Screenshot: 08_extended.png")
        
        # Try to complete booking
        print("✅ Looking for BOOK/CONFIRM button...")
        try:
            await page.click("button:has-text('Book'), button:has-text('Confirm'), button:has-text('Complete'), input[type='submit']", timeout=5000)
            print("✅ Clicked BOOK/CONFIRM")
            await asyncio.sleep(3)
        except:
            print("  ⚠️ No book button found")
        
        await page.screenshot(path="09_final.png", full_page=True)
        print("📸 Screenshot: 09_final.png")
        
        # Check page content for success
        page_content = await page.content()
        success = any(word in page_content.lower() for word in ['success', 'confirmed', 'booked', 'thank you', 'completed'])
        
        print("\n" + "=" * 60)
        print("BOOKING ATTEMPT COMPLETE")
        print("=" * 60)
        print(f"Target: Squash court, {TARGET_DAY_NAME} at 18:00-19:00")
        print(f"Result: {'✅ Likely SUCCESSFUL' if success else '⚠️ Check screenshots'}")
        print("=" * 60)
        
        await browser.close()
        return success

if __name__ == "__main__":
    print("=" * 60)
    print("SmartClubCloud Squash Court Booker")
    print("=" * 60)
    print(f"Target: Friday {TARGET_DAY_NAME} at 18:00")
    print("=" * 60)
    asyncio.run(book_court())
