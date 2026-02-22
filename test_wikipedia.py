#!/usr/bin/env python3
"""Test browser-use to navigate to Wikipedia and click I'm Feeling Lucky"""
import asyncio
import os
from browser_use import Agent, Browser, ChatOpenAI

async def main():
    print("🚀 Starting browser...")
    browser = Browser()
    
    print("🌐 Navigating to Wikipedia...")
    # Navigate to Wikipedia
    await browser.goto("https://wikipedia.org")
    
    print("📄 Getting page state...")
    # Get the current state
    state = await browser.get_state()
    print(f"Current URL: {state.url}")
    print(f"Page title: {state.title}")
    
    # Find all clickable elements
    print("\n🎯 Clickable elements found:")
    for i, elem in enumerate(state.interactive_elements, 1):
        text = elem.get('text', '')[:50] if hasattr(elem, 'get') else str(elem)[:50]
        print(f"  {i}. {text}")
    
    # Look for "I'm Feeling Lucky" button
    lucky_found = False
    for i, elem in enumerate(state.interactive_elements, 1):
        text = elem.get('text', '').lower() if hasattr(elem, 'get') else str(elem).lower()
        if 'lucky' in text or 'feeling' in text:
            print(f"\n✅ Found 'I'm Feeling Lucky' at index {i}")
            print(f"Clicking element {i}...")
            await browser.click_element(elem)
            lucky_found = True
            break
    
    if not lucky_found:
        print("\n⚠️ 'I'm Feeling Lucky' not found in interactive elements")
        print("Taking screenshot to see what's on the page...")
        await browser.take_screenshot("wikipedia_page.png")
        print("Screenshot saved to wikipedia_page.png")
    else:
        # Wait a moment for navigation
        await asyncio.sleep(3)
        
        # Get new state
        new_state = await browser.get_state()
        print(f"\n🎉 Landed on: {new_state.url}")
        print(f"Page title: {new_state.title}")
        
        # Take screenshot
        await browser.take_screenshot("lucky_result.png")
        print("Screenshot saved to lucky_result.png")
    
    await browser.close()
    print("\n✅ Browser closed")

if __name__ == "__main__":
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set")
        print("Set it with: export OPENAI_API_KEY='your-key'")
    
    asyncio.run(main())
