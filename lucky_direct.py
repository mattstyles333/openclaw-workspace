#!/usr/bin/env python3
"""Google search + I'm Feeling Lucky"""
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
    
    # Method 1: Direct URL with btnI parameter (I'm Feeling Lucky)
    print("🌐 Using direct 'I'm Feeling Lucky' URL...")
    search_term = "wikipedia"  # You can change this
    
    # This URL format triggers I'm Feeling Lucky
    lucky_url = f"https://www.google.com/search?q={search_term}&btnI=I'm+Feeling+Lucky"
    
    print(f"   Search term: {search_term}")
    page.goto(lucky_url, wait_until="networkidle")
    
    print(f"\n🎉 LANDED ON:")
    print(f"   URL: {page.url}")
    print(f"   Title: {page.title()}")
    
    page.screenshot(path="/root/.openclaw/workspace/lucky_result.png")
    print("📸 Screenshot saved to lucky_result.png")
    
    browser.close()
    print("\n✅ Done!")
