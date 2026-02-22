#!/usr/bin/env python3
"""Navigate to Google and click I'm Feeling Lucky"""
from playwright.sync_api import sync_playwright

print("🚀 Starting browser...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    print("🌐 Navigating to Google...")
    page.goto("https://google.com", wait_until="networkidle")
    
    title = page.title()
    print(f"📄 Page title: {title}")
    
    print("\n🔍 Looking for 'I'm Feeling Lucky' button...")
    # Find the button by name attribute
    lucky_buttons = page.locator("input[name='btnI']").all()
    
    if lucky_buttons:
        print(f"✅ Found {len(lucky_buttons)} 'I'm Feeling Lucky' button(s)!")
        lucky = lucky_buttons[0]  # Use the first one
        
        print("🖱️  Clicking it...")
        lucky.click()
        
        print("⏳ Waiting for navigation...")
        page.wait_for_load_state("networkidle")
        
        new_url = page.url
        new_title = page.title()
        
        print(f"\n🎉 RESULT - I landed on:")
        print(f"   URL: {new_url}")
        print(f"   Title: {new_title}")
        
        page.screenshot(path="/root/.openclaw/workspace/lucky_result.png")
        print("\n📸 Screenshot saved to lucky_result.png")
    else:
        print("⚠️  Button not found")
        page.screenshot(path="/root/.openclaw/workspace/google_home.png")
    
    browser.close()
    print("\n✅ Done!")
