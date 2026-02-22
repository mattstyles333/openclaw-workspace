#!/usr/bin/env python3
"""Navigate to Google, accept cookies, click I'm Feeling Lucky"""
from playwright.sync_api import sync_playwright

print("🚀 Starting browser...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    print("🌐 Navigating to Google...")
    page.goto("https://google.com", wait_until="networkidle")
    
    title = page.title()
    print(f"📄 Page title: {title}")
    
    # Handle cookie consent popup
    print("\n🍪 Checking for cookie popup...")
    try:
        # Look for "Accept all" button (UK/EU version)
        accept_btn = page.locator("button:has-text('Accept all')").first
        if accept_btn.is_visible(timeout=5000):
            print("✅ Found cookie popup, clicking 'Accept all'...")
            accept_btn.click()
            page.wait_for_timeout(1000)  # Wait for popup to close
            print("✅ Cookies accepted!")
        else:
            print("ℹ️  No cookie popup found")
    except Exception as e:
        print(f"ℹ️  No cookie popup or error: {e}")
    
    print("\n🔍 Looking for 'I'm Feeling Lucky' button...")
    # Find the button by name attribute
    lucky_buttons = page.locator("input[name='btnI']").all()
    
    if lucky_buttons:
        print(f"✅ Found {len(lucky_buttons)} 'I'm Feeling Lucky' button(s)!")
        lucky = lucky_buttons[0]  # Use the first one
        
        print("🖱️  Clicking 'I'm Feeling Lucky'...")
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
