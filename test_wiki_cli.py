#!/usr/bin/env python3
"""Test browser-use CLI approach"""
import subprocess
import time

BROWSER_USE = "/root/.local/bin/browser-use"

def run_cmd(cmd, wait=5):
    """Run a browser-use CLI command"""
    full_cmd = f"{BROWSER_USE} {cmd}"
    print(f"\n$ browser-use {cmd}")
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=60)
    print(f"stdout: {result.stdout[:2000] if result.stdout else '(empty)'}")
    if result.stderr:
        print(f"stderr: {result.stderr[:500]}")
    print(f"return code: {result.returncode}")
    return result

# Open Wikipedia
print("🌐 Opening Wikipedia...")
run_cmd("open https://wikipedia.org --session wiki_lucky", wait=5)

# Get state to see elements
print("\n📄 Getting page state...")
result = run_cmd("--session wiki_lucky state", wait=10)

# Store output for analysis
output = result.stdout + result.stderr

# Take a screenshot to see what we're working with
print("\n📸 Taking screenshot of Wikipedia homepage...")
run_cmd("--session wiki_lucky screenshot wikipedia_home.png", wait=3)

# Try to find "I'm Feeling Lucky" button
# Wikipedia's "I'm Feeling Lucky" is usually near the search box
# Let's try clicking on elements that might be it
# Common positions: element 5-8 range typically contains search-related buttons

print("\n🎯 Looking for 'I'm Feeling Lucky' button...")
print("Output preview:", output[:1000] if output else "(no output)")

# Try clicking elements 5, 6, 7, 8 (likely locations for the lucky button)
for elem_num in [5, 6, 7, 8, 9]:
    print(f"\n🖱️  Trying to click element {elem_num}...")
    run_cmd(f"--session wiki_lucky click {elem_num}", wait=3)
    
    # Check state after click
    result = run_cmd("--session wiki_lucky state", wait=5)
    new_output = result.stdout + result.stderr
    
    # If URL changed, we found it
    if "wikipedia.org" not in new_output.lower() or "/wiki/" in new_output.lower():
        print(f"\n🎉 SUCCESS! Clicked element {elem_num} and navigated to a new page!")
        break

# Get final state
print("\n📍 Getting final page state...")
result = run_cmd("--session wiki_lucky state", wait=5)

# Extract URL from output
final_output = result.stdout + result.stderr
print("\n" + "="*60)
print("FINAL RESULT:")
print("="*60)
print(final_output[:2000] if final_output else "(no output)")

# Take final screenshot
print("\n📸 Taking final screenshot...")
run_cmd("--session wiki_lucky screenshot lucky_final.png", wait=3)

print("\n✅ Done! Check wikipedia_home.png and lucky_final.png")
