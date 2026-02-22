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
        
        # Wait for and fill login form
        print("⏳ Waiting for login form...")
        await page.wait_for_selector("input[type='text'], input[name='username']", timeout=15000)
        
        print("🔑 Logging in...")
        await page.fill("input[type='text']", USERNAME)
        await page.fill("input[type='password']", PASSWORD)
        
        # Try multiple login button selectors
        login_selectors = [
            "input[type='submit']",
            "button[type='submit']", 
            "button:has-text('Login')",
            "button:has-text('Sign in')",
            "input[value='Login']",
            "input[value='Sign in']",
            ".btn-primary",
            "button.btn"
        ]
        
        for selector in login_selectors:
            try:
                await page.click(selector, timeout=3000)
                print(f"✅ Clicked login: {selector}")
                break
            except:
                continue
        
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(3)
        await page.screenshot(path="01_logged_in.png")
        print("📸 Screenshot: 01_logged_in.png")
        
        # Click on Bookings tile (the calendar icon)
        print("📅 Clicking Bookings tile...")
        try:
            await page.click("a:has-text('Book'), text='Bookings', a[href*='booking']")
        except:
            try:
                await page.click(".fa-book, .fa-calendar, [class*='booking']")
            except:
                # Try clicking by coordinate if all else fails
                await page.mouse.click(200, 600)  # Approximate Bookings tile location
        
        await asyncio.sleep(2)
        await page.screenshot(path="02_bookings.png")
        print("📸 Screenshot: 02_bookings.png")
        
        # Click Book Now button
        print("📅 Clicking Book Now...")
        try:
            await page.click("button:has-text('Book Now'), a:has-text('Book Now'), .btn:has-text('Book Now')")
        except:
            await page.click("text='Book Now'")
        
        await asyncio.sleep(3)
        await page.screenshot(path="03_calendar.png")
        print("📸 Screenshot: 03_calendar.png")
        
        # Select Squash from dropdown
        print("🏸 Changing to Squash...")
        try:
            await page.select_option("select", "Squash")
            await asyncio.sleep(2)
        except Exception as e:
            print(f"  ⚠️ Could not select Squash: {e}")
        
        await page.screenshot(path="04_squash.png")
        print("📸 Screenshot: 04_squash.png")
        
        # Click Refresh Calendar
        print("🔄 Refreshing calendar...")
        try:
            await page.click("button:has-text('Refresh'), button:has-text('Refresh Calendar')")
            await asyncio.sleep(3)
        except:
            print("  ℹ️ No refresh button")
        
        await page.screenshot(path="05_calendar_ready.png")
        print("📸 Screenshot: 05_calendar_ready.png")
        
        # Click on Court 1, 17:30-18:00 slot (5:30-6:00)
        print("🎯 Clicking Court 1, 17:30-18:00 (5:30-6:00pm)...")
        
        # Get page content and find the cell
        cells = await page.locator("td").all()
        clicked = False
        for i, cell in enumerate(cells):
            text = await cell.text_content()
            if text and "17:30" in text and "18:00" in text:
                try:
                    # Check if this is Court 1 (should be early in the list)
                    await cell.click()
                    print(f"✅ Clicked cell {i}: {text.strip()}")
                    clicked = True
                    break
                except:
                    pass
        
        if not clicked:
            print("  ⚠️ Could not find/click the 5:30 slot")
        
        await asyncio.sleep(2)
        await page.screenshot(path="06_slot_selected.png")
        print("📸 Screenshot: 06_slot_selected.png")
        
        # Look for booking dialog or extend option
        print("➕ Checking for extend/book options...")
        content = await page.content()
        
        # Try to extend or book
        try:
            await page.click("button:has-text('Extend'), a:has-text('Extend')", timeout=3000)
            print("✅ Extended booking")
        except:
            print("  ℹ️ No extend option")
        
        try:
            await page.click("button:has-text('Book'), button:has-text('Confirm'), input[value='Book']", timeout=5000)
            print("🎉 BOOKING SUBMITTED!")
        except Exception as e:
            print(f"  ⚠️ Could not complete booking: {e}")
        
        await asyncio.sleep(3)
        await page.screenshot(path="07_final.png")
        print("📸 Screenshot: 07_final.png")
        
        # Check result
        final_content = await page.content()
        if "success" in final_content.lower() or "confirmed" in final_content.lower() or "booked" in final_content.lower():
            print("\n✅ BOOKING APPEARS SUCCESSFUL!")
        else:
            print("\n⚠️ BOOKING STATUS UNCLEAR - check screenshot")
        
        await browser.close()
        print("\n✅ Done!")

asyncio.run(book_court())
