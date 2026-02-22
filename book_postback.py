#!/usr/bin/env python3
"""Book Court 1 Friday 6-7pm - ASP.NET postback approach"""
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
        
        # Click Bookings tile using JavaScript
        print("📅 Clicking Bookings...")
        await page.evaluate('''() => {
            const links = document.querySelectorAll('a');
            for (let link of links) {
                if (link.textContent.includes('Bookings')) {
                    link.click();
                    return 'clicked';
                }
            }
            return 'not found';
        }''')
        await asyncio.sleep(3)
        await page.screenshot(path="01_bookings.png")
        
        # Click Book Now using JavaScript to trigger the ASP.NET postback
        print("📅 Clicking Book Now (JS)...")
        result = await page.evaluate('''() => {
            const buttons = document.querySelectorAll('button');
            for (let btn of buttons) {
                if (btn.textContent.includes('Book Now')) {
                    // Trigger click event
                    const clickEvent = new MouseEvent('click', {
                        bubbles: true,
                        cancelable: true,
                        view: window
                    });
                    btn.dispatchEvent(clickEvent);
                    return 'dispatched';
                }
            }
            return 'button not found';
        }''')
        print(f"  Result: {result}")
        
        await asyncio.sleep(5)
        await page.screenshot(path="02_after_booknow.png")
        
        # Check URL
        url = page.url
        print(f"  URL: {url}")
        
        if "Courts" in url or "courts" in url.lower():
            print("  ✅ Calendar page loaded!")
            
            # Select Squash
            print("🏸 Selecting Squash...")
            await page.select_option("select", "Squash")
            await asyncio.sleep(2)
            
            # Navigate to Friday
            print("📆 Navigating to Friday...")
            await page.evaluate('''() => {
                // Try to find and click the Fri 20 Feb button
                const buttons = document.querySelectorAll('button');
                for (let btn of buttons) {
                    if (btn.textContent.includes('Fri 20 Feb')) {
                        btn.click();
                        return 'clicked Fri 20 Feb';
                    }
                }
                return 'Fri button not found';
            }''')
            await asyncio.sleep(2)
            
            # Refresh calendar
            print("🔄 Refreshing...")
            await page.click("button:has-text('Refresh')")
            await asyncio.sleep(3)
            await page.screenshot(path="03_friday_calendar.png")
            
            # Click Court 1, 18:00 slot
            print("🎯 Clicking Court 1, 18:00...")
            await page.evaluate('''() => {
                const cells = document.querySelectorAll('td');
                for (let cell of cells) {
                    const text = cell.textContent;
                    if (text && text.includes('18:00') && text.includes('19:00')) {
                        cell.click();
                        return 'clicked slot: ' + text;
                    }
                }
                return 'slot not found';
            }''')
            await asyncio.sleep(3)
            await page.screenshot(path="04_slot_clicked.png")
            
            # Extend and book
            print("➕ Extending...")
            await page.evaluate('''() => {
                const buttons = document.querySelectorAll('button');
                for (let btn of buttons) {
                    if (btn.textContent.includes('Extend')) {
                        btn.click();
                        return 'extended';
                    }
                }
                return 'no extend';
            }''')
            await asyncio.sleep(2)
            
            print("✅ Booking...")
            await page.evaluate('''() => {
                const buttons = document.querySelectorAll('button');
                for (let btn of buttons) {
                    if (btn.textContent.includes('Book') && !btn.textContent.includes('Book Now')) {
                        btn.click();
                        return 'booked';
                    }
                }
                return 'no book button';
            }''')
            await asyncio.sleep(3)
            await page.screenshot(path="05_final.png")
            
        else:
            print("  ⚠️ Still on Bookings page")
        
        await browser.close()
        print("\n✅ Done!")

asyncio.run(book_court())
