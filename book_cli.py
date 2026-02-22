#!/usr/bin/env python3
"""Use browser-use CLI to book the court"""
import subprocess
import time

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(f"$ {cmd}")
    print(result.stdout)
    if result.stderr:
        print(f"stderr: {result.stderr}")
    return result

print("🌐 Opening SmartClubCloud...")
run_cmd('browser-use open "https://www.smartclubcloud.com/"')
time.sleep(3)

print("\n📋 Getting page state...")
run_cmd('browser-use state')

print("\n🔑 Typing username...")
run_cmd('browser-use type "matthew.styles.1963"')
time.sleep(1)

print("\n🔑 Typing password...")
run_cmd('browser-use keys "Tab"')
time.sleep(0.5)
run_cmd('browser-use type "James333"')
time.sleep(1)

print("\n🔑 Submitting login...")
run_cmd('browser-use keys "Enter"')
time.sleep(5)

print("\n📸 After login...")
run_cmd('browser-use screenshot 01_cli_login.png')

print("\n📅 Clicking Bookings...")
run_cmd('browser-use click 8')  # Assuming 8 is Bookings tile
time.sleep(3)
run_cmd('browser-use screenshot 02_cli_bookings.png')

print("\n✅ Done with CLI approach")
