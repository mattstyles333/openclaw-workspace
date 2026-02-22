#!/bin/bash
# Book Court 1, 5:30-6:30pm using browser-use CLI

echo "🌐 Opening SmartClubCloud..."
browser-use open "https://www.smartclubcloud.com/"
sleep 3

echo "📋 Getting login page state..."
browser-use state

echo "🔑 Logging in..."
browser-use type "matthew.styles.1963"
browser-use keys "Tab"
browser-use type "James333"
browser-use keys "Enter"
sleep 5

echo "📸 After login..."
browser-use screenshot after_login.png

echo "📅 Clicking Bookings..."
browser-use click 6  # Assuming 6 is Bookings based on typical layout
sleep 2
browser-use screenshot bookings_page.png

echo "📅 Clicking Book Now..."
browser-use state
# Find and click Book Now button

echo "Done - check screenshots"
