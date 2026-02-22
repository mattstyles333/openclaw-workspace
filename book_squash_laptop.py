#!/usr/bin/env python3
"""
Book a squash court at 12:30 today on smartclubcloud.com
Run this on your laptop (not the VPS) since the VPS IP is blocked.
"""
import asyncio
from playwright.async_api import async_playwright
from datetime import datetime

# Your credentials (from 1Password)
USERNAME = "matthew.styles.1963"
PASSWORD = "James333"

# Target time
TARGET_TIME = "12:30"
SPORT = "Squash"  # Change from default Tennis

async def book_court():
    async with async_playwright() as p:
        # Launch browser (visible so you can see what's happening)
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        print("🌐 Opening smartclubcloud.com...")
        await page.goto("https://www.smartclubcloud.com/")
        
        # Wait for login form
        await page.wait_for_selector("input[type='text'], input[name='username'], #username", timeout=10000)
        
        print("🔑 Logging in...")
        # Fill username
        await page.fill("input[type='text'], input[name='username'], #username", USERNAME)
        
        # Fill password
        await page.fill("input[type='password'], input[name='password'], #password", PASSWORD)
        
        # Click login
        await page.click("button[type='submit'], input[type='submit'], .login-button, button:has-text('Login'), button:has-text('Sign in')")
        
        # Wait for page to load after login
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(2)
        
        print("📅 Looking for booking section...")
        
        # Look for court booking link/button
        booking_selectors = [
            "a:has-text('Book')",
            "a:has-text('Courts')",
            "a:has-text('Facilities')",
            "a:has-text('Book a Court')",
            "button:has-text('Book')",
            "[href*='book']",
            "[href*='court']",
        ]
        
        for selector in booking_selectors:
            try:
                await page.click(selector, timeout=3000)
                print(f"✅ Clicked: {selector}")
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(2)
                break
            except:
                continue
        
        print("🏸 Looking for sport selection...")
        # Look for sport dropdown or squash option
        sport_selectors = [
            "select",
            "[name*='sport']",
            "[name*='activity']",
            "button:has-text('Tennis')",  # If tennis is default
            "a:has-text('Squash')",
            "label:has-text('Squash')",
            "text='Squash'",
        ]
        
        for selector in sport_selectors:
            try:
                if "select" in selector:
                    await page.select_option(selector, label="Squash")
                else:
                    await page.click(selector, timeout=3000)
                print(f"✅ Selected sport using: {selector}")
                await asyncio.sleep(1)
                break
            except:
                continue
        
        print("🕐 Looking for time selection (12:30)...")
        # Look for 12:30 time slot
        time_selectors = [
            f"text='12:30'",
            f"text='12.30'",
            "[value*='12:30']",
            "[data-time*='12:30']",
        ]
        
        for selector in time_selectors:
            try:
                await page.click(f"[{selector}], *:has-text('12:30')", timeout=3000)
                print(f"✅ Selected 12:30 using: {selector}")
                await asyncio.sleep(1)
                break
            except:
                continue
        
        print("\n📸 Taking screenshot of current state...")
        await page.screenshot(path="squash_booking_state.png", full_page=True)
        print("Screenshot saved to: squash_booking_state.png")
        
        print("\n⚠️  Browser will stay open for 60 seconds so you can complete the booking...")
        print("   - Check if Squash is selected (not Tennis)")
        print("   - Check if 12:30 time slot is selected")
        print("   - Click the Book/Confirm button to complete")
        await asyncio.sleep(60)
        
        await browser.close()
        print("✅ Done!")

if __name__ == "__main__":
    print("=" * 60)
    print("SmartClubCloud Squash Court Booker")
    print("=" * 60)
    print(f"Target: Squash court at {TARGET_TIME} today")
    print(f"User: {USERNAME}")
    print("=" * 60)
    asyncio.run(book_court())
