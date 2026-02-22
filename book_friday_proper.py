#!/usr/bin/env python3
"""Book Court 1, 5:30-6:30pm on FRIDAY - Proper navigation"""
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
        await page.screenshot(path="01_dashboard.png")
        
        # Click on Bookings tile (calendar icon)
        print("📅 Clicking Bookings tile...")
        # The Bookings tile has text "Bookings" and is in the bottom row
        await page.click("text='Bookings'")
        await asyncio.sleep(3)
        await page.screenshot(path="02_bookings_page.png")
        print("📸 Bookings page")
        
        # Click the green "Book Now" button
        print("📅 Clicking Book Now...")
        await page.click("button:has-text('Book Now'), .btn:has-text('Book Now')")
        await asyncio.sleep(3)
        await page.screenshot(path="03_calendar.png")
        print("📸 Calendar loaded")
        
        # Select Squash from dropdown
        print("🏸 Selecting Squash...")
        try:
            # The dropdown should be visible now
            await page.select_option("select", "Squash")
            await asyncio.sleep(2)
            print("✅ Selected Squash")
        except Exception as e:
            print(f"  ⚠️ Could not select Squash: {e}")
        
        await page.screenshot(path="04_squash.png")
        
        # Navigate to FRIDAY 20 Feb using the date navigation
        print("📆 Navigating to Friday 20 Feb...")
        
        # Click on the date field to open date picker
        try:
            await page.click("input[name='dateStart']")
            await asyncio.sleep(1)
            print("  Opened date picker")
            
            # Try clicking on 20
            await page.click("text='20'", timeout=3000)
            await asyncio.sleep(1)
            print("  Selected day 20")
            
            # Click Done
            await page.click("button:has-text('Done')")
            await asyncio.sleep(2)
            print("✅ Date set to Friday 20 Feb")
        except Exception as e:
            print(f"  ⚠️ Date picker issue: {e}")
        
        await page.screenshot(path="05_friday.png")
        
        # Refresh calendar
        print("🔄 Refreshing calendar...")
        try:
            await page.click("button:has-text('Refresh')")
            await asyncio.sleep(3)
            print("✅ Calendar refreshed")
        except:
            print("  ℹ️ No refresh needed")
        
        await page.screenshot(path="06_friday_calendar.png")
        
        # Click on Court 1, 17:30-18:00 slot
        print("🎯 Clicking Court 1, 17:30-18:00...")
        
        # Get all cells and find the right one
        cells = await page.locator("table td").all()
        print(f"  Found {len(cells)} cells")
        
        clicked = False
        for i, cell in enumerate(cells):
            text = await cell.text_content()
            if text and "17:30" in text and "18:00" in text:
                print(f"  Found: {text.strip()}")
                try:
                    await cell.click()
                    print(f"  ✅ Clicked!")
                    clicked = True
                    break
                except Exception as e:
                    print(f"  Click failed: {e}")
        
        await asyncio.sleep(3)
        await page.screenshot(path="07_slot_clicked.png")
        
        # Look for extend and book options
        print("➕ Looking for extend option...")
        try:
            await page.click("button:has-text('Extend')", timeout=3000)
            print("✅ Extended to 1 hour")
        except:
            print("  ℹ️ No extend option")
        
        print("✅ Looking for Book button...")
        try:
            await page.click("button:has-text('Book'):visible", timeout=5000)
            print("🎉 BOOKED!")
        except Exception as e:
            print(f"  ⚠️ Could not complete: {e}")
        
        await asyncio.sleep(3)
        await page.screenshot(path="08_final.png")
        
        await browser.close()
        print("\n✅ Done - check screenshots!")

asyncio.run(book_court())
