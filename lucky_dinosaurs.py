#!/usr/bin/env python3
"""Google I'm Feeling Lucky with redirect following"""
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
    
    # Use I'm Feeling Lucky with a random interesting term
    search_term = "dinosaurs"  # Change this to any topic!
    
    print(f"🎲 Searching for: '{search_term}'")
    print("🍀 Using 'I'm Feeling Lucky'...")
    
    lucky_url = f"https://www.google.com/search?q={search_term}&btnI=I'm+Feeling+Lucky"
    page.goto(lucky_url, wait_until="networkidle")
    
    # Check if we hit a redirect notice
    if "Redirect Notice" in page.title():
        print("📍 Hit redirect notice, clicking through...")
        link = page.locator("a[href*='wikipedia.org']").first
        if link.is_visible():
            link.click()
            page.wait_for_load_state("networkidle")
    
    print(f"\n🎉 LANDED ON:")
    print(f"   URL: {page.url}")
    print(f"   Title: {page.title()}")
    
    page.screenshot(path="/root/.openclaw/workspace/lucky_result.png")
    print("📸 Screenshot saved!")
    
    browser.close()
    print("\n✅ Done!")
