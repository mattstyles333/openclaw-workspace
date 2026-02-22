#!/bin/bash
# Spotify OAuth automation using browser-use

# Load credentials
CLIENT_ID=$(cat /root/.openclaw/workspace/.spotify_config.json | python3 -c "import json,sys; print(json.load(sys.stdin)['spotify']['client_id'])")
REDIRECT_URI="http://localhost:8888/callback"
SCOPES="user-read-private user-read-email user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-recently-played user-top-read playlist-read-private playlist-read-collaborative user-library-read user-read-playback-position"

# Build auth URL
AUTH_URL="https://accounts.spotify.com/authorize?client_id=${CLIENT_ID}&response_type=code&redirect_uri=${REDIRECT_URI}&scope=${SCOPES// /%20}"

echo "🎵 Starting Spotify OAuth Flow..."
echo ""
echo "Opening authorization URL in cloud browser..."
echo ""

# Start a cloud browser session and open the auth URL
browser-use open "$AUTH_URL" --keep-alive 2>&1 | tee /tmp/browser_session.txt &

sleep 3

# Get the session ID and live URL
SESSION_ID=$(cat /tmp/browser_session.txt | grep -o 'session_id: [a-z0-9-]*' | cut -d' ' -f2)
LIVE_URL=$(cat /tmp/browser_session.txt | grep -o 'live_url: https://[^ ]*' | cut -d' ' -f2)

echo ""
echo "═══════════════════════════════════════════════════════"
echo "📱 VIEW THE BROWSER LIVE:"
echo "$LIVE_URL"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "Step 1: Click the live URL above to watch/assist"
echo "Step 2: Log in to Spotify in the browser"
echo "Step 3: Click 'Agree' to authorize"
echo "Step 4: After redirect, copy the URL from the address bar"
echo "Step 5: Run: ./complete_auth.sh '<paste_url_here>'"
echo ""
echo "Session ID: $SESSION_ID"
