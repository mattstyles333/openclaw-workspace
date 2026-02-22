#!/usr/bin/env python3
"""Simple test - just navigate and screenshot"""
import os
os.environ['DISPLAY'] = ':99'  # For headless environments

from playwright.sync_api import sync_playwright

print("🚀 Starting browser...")
with sync_playwright() as p:
    # Launch with explicit args for headless
    browser = p.chromium.launch(
        headless=True,
        args=['--no-sandbox', '--disable-setuid-sandbox']
    )
    page = browser.new_page()
    
    print("🌐 Navigating to example.com...")
    page.goto("https://example.com")
    
    print("📸 Taking screenshot...")
    page.screenshot(path="/root/.openclaw/workspace/test.png")
    
    print(f"📄 Title: {page.title()}")
    print("✅ Done!")
    
    browser.close()
