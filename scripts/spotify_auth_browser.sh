#!/bin/bash
# Spotify OAuth using browser-use (simpler approach)

export PATH="$HOME/.local/bin:$PATH"

# Load credentials
CLIENT_ID=$(cat /root/.openclaw/workspace/.spotify_config.json | python3 -c "import json,sys; print(json.load(sys.stdin)['spotify']['client_id'])")
REDIRECT_URI="http://localhost:8888/callback"
SCOPES="user-read-private user-read-email user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-recently-played user-top-read playlist-read-private playlist-read-collaborative user-library-read user-read-playback-position"

# Build auth URL (URL encoded)
AUTH_URL="https://accounts.spotify.com/authorize?client_id=${CLIENT_ID}&response_type=code&redirect_uri=${REDIRECT_URI}&scope=${SCOPES// /%20}"

echo "🎵 Spotify OAuth Setup"
echo "======================"
echo ""
echo "Starting cloud browser session..."
echo ""

# Start browser session and capture output
browser-use open "$AUTH_URL" 2>&1 &
BROWSER_PID=$!

sleep 5

echo ""
echo "═══════════════════════════════════════════════════════"
echo "📱 BROWSER IS OPEN"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "The Spotify authorization page is now open in a cloud browser."
echo ""
echo "To complete authentication:"
echo ""
echo "1. I can try to automate it (requires your Spotify email/password)"
echo "2. OR you can view the browser and complete it manually"
echo ""
echo "═══════════════════════════════════════════════════════"
echo ""

# Show current browser state
sleep 2
browser-use state 2>&1 | head -30

echo ""
echo "Would you like me to:"
echo "  [1] Try to automate login (need your credentials)"
echo "  [2] Show you the browser URL to complete manually"
echo ""

# Keep browser open
wait $BROWSER_PID
