#!/usr/bin/env python3
"""Navigate to Google and click I'm Feeling Lucky - SIMPLIFIED"""
import asyncio
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
    # Try to find the button
    lucky = page.locator('input[name="btnI"]').first
    
    if lucky.is_visible():
        print("✅ Found 'I'm Feeling Lucky' button!")
        print("🖱️  Clicking it...")
        lucky.click()
        
        print("⏳ Waiting for navigation...")
        page.wait_for_load_state("networkidle")
        
        new_url = page.url
        new_title = page.title()
        
        print(f"\n🎉 RESULT:")
        print(f"   URL: {new_url}")
        print(f"   Title: {new_title}")
        
        page.screenshot(path="/root/.openclaw/workspace/lucky_result.png")
        print("📸 Screenshot saved!")
    else:
        print("⚠️  Button not found, taking screenshot...")
        page.screenshot(path="/root/.openclaw/workspace/google_home.png")
        
        # List all buttons
        buttons = page.locator("input[type='submit']").all()
        print(f"\nFound {len(buttons)} buttons:")
        for i, btn in enumerate(buttons[:5]):
            val = btn.get_attribute("value")
            name = btn.get_attribute("name")
            print(f"  {i}: value='{val}', name='{name}'")
    
    browser.close()
    print("\n✅ Done!")
