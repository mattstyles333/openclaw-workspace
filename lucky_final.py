#!/usr/bin/env python3
"""Navigate to Google, accept cookies, click I'm Feeling Lucky"""
import os
os.environ['DISPLAY'] = ':99'

from playwright.sync_api import sync_playwright

print("🚀 Starting browser...")
with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--no-sandbox', '--disable-setuid-sandbox']
    )
    page = browser.new_page()
    
    print("🌐 Navigating to Google...")
    page.goto("https://google.com", wait_until="networkidle")
    
    print(f"📄 Page title: {page.title()}")
    
    # Handle cookie consent
    print("\n🍪 Checking for cookie popup...")
    try:
        accept_btn = page.locator("button:has-text('Accept all')").first
        if accept_btn.is_visible(timeout=3000):
            print("✅ Found cookie popup, clicking 'Accept all'...")
            accept_btn.click()
            page.wait_for_timeout(1000)
            print("✅ Cookies accepted!")
    except:
        print("ℹ️  No cookie popup")
    
    print("\n🔍 Looking for 'I'm Feeling Lucky' button...")
    lucky_buttons = page.locator("input[name='btnI']").all()
    
    if lucky_buttons:
        print(f"✅ Found 'I'm Feeling Lucky' button!")
        lucky_buttons[0].click()
        
        print("⏳ Waiting for navigation...")
        page.wait_for_load_state("networkidle")
        
        print(f"\n🎉 RESULT:")
        print(f"   URL: {page.url}")
        print(f"   Title: {page.title()}")
        
        page.screenshot(path="/root/.openclaw/workspace/lucky_result.png")
        print("📸 Screenshot saved!")
    else:
        print("⚠️  Button not found")
        page.screenshot(path="/root/.openclaw/workspace/google_page.png")
    
    browser.close()
    print("\n✅ Done!")
