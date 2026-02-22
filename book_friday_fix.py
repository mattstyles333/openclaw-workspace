#!/usr/bin/env python3
"""Book Court 1, 5:30-6:30pm on FRIDAY - Fixed selectors"""
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
        await page.screenshot(path="01_logged_in.png")
        
        # Navigate to Bookings - click the Bookings tile
        print("📅 Going to Bookings...")
        await page.goto("https://www.smartclubcloud.com/Courts")
        await asyncio.sleep(3)
        await page.screenshot(path="02_bookings.png")
        print("📸 Screenshot saved")
        
        # Click Book Now - use text-based selector
        print("📅 Clicking Book Now...")
        try:
            await page.click("text='Book Now'")
            print("✅ Clicked Book Now (text)")
        except:
            try:
                await page.click(".btn-success, .btn-primary, button.btn")
                print("✅ Clicked Book Now (class)")
            except Exception as e:
                print(f"  ❌ Could not click Book Now: {e}")
        
        await asyncio.sleep(3)
        await page.screenshot(path="03_calendar.png")
        print("📸 Screenshot saved")
        
        # Select Squash
        print("🏸 Selecting Squash...")
        try:
            await page.select_option("select", "Squash")
            await asyncio.sleep(2)
            print("✅ Selected Squash")
        except Exception as e:
            print(f"  ⚠️ Could not select Squash: {e}")
        
        # Navigate to FRIDAY 20 Feb
        print("📆 Changing date to Friday 20 Feb...")
        try:
            # Click date field to open picker
            await page.click("input[name='dateStart']")
            await asyncio.sleep(1)
            
            # Click on the 20th
            await page.click("text='20'", timeout=5000)
            await asyncio.sleep(1)
            
            # Click Done
            await page.click("button:has-text('Done')")
            await asyncio.sleep(2)
            print("✅ Selected Friday 20 Feb")
        except Exception as e:
            print(f"  ⚠️ Date selection issue: {e}")
        
        await page.screenshot(path="04_friday.png")
        print("📸 Screenshot saved")
        
        # Click Refresh Calendar
        print("🔄 Refreshing calendar...")
        try:
            await page.click("button:has-text('Refresh')")
            await asyncio.sleep(3)
            print("✅ Refreshed")
        except:
            print("  ℹ️ No refresh needed")
        
        await page.screenshot(path="05_calendar_ready.png")
        
        # Get all table cells and find the Court 1, 17:30-18:00 slot
        print("🎯 Looking for Court 1, 17:30-18:00 slot...")
        
        # Find all clickable cells (td elements)
        cells = await page.locator("table td").all()
        print(f"Found {len(cells)} table cells")
        
        clicked = False
        for i, cell in enumerate(cells):
            text = await cell.text_content()
            if text and "17:30" in text and "18:00" in text:
                print(f"  Found cell {i}: {text.strip()}")
                try:
                    # Check if this is likely Court 1 (not Court 2 or 3)
                    # Court 1 cells should appear before Court 2 and 3 cells
                    await cell.click()
                    print(f"  ✅ Clicked cell {i}")
                    clicked = True
                    break
                except Exception as e:
                    print(f"  Could not click: {e}")
        
        if not clicked:
            print("  ⚠️ Could not click any time slot")
        
        await asyncio.sleep(3)
        await page.screenshot(path="06_after_click.png")
        print("📸 Screenshot saved")
        
        # Check for booking dialog
        content = await page.content()
        if "book" in content.lower() or "confirm" in content.lower():
            print("🎉 Booking interface detected!")
        
        # Try to complete booking
        print("➕ Looking for extend option...")
        try:
            await page.click("button:has-text('Extend')", timeout=3000)
            print("✅ Extended to 1 hour")
        except:
            print("  ℹ️ No extend option")
        
        print("✅ Looking for Book/Confirm...")
        try:
            await page.click("button:has-text('Book'):visible, button:has-text('Confirm'):visible", timeout=5000)
            print("🎉 BOOKED!")
        except Exception as e:
            print(f"  ⚠️ Could not complete booking: {e}")
        
        await asyncio.sleep(3)
        await page.screenshot(path="07_final.png")
        print("📸 Final screenshot saved")
        
        await browser.close()
        print("\n✅ Done!")

asyncio.run(book_court())
