#!/usr/bin/env python3
"""
Spotify Authentication Helper for OpenClaw
Run this to get your access token
"""

import json
import base64
import urllib.parse
import urllib.request
import sys

# Load credentials
with open('/root/.openclaw/workspace/.spotify_config.json', 'r') as f:
    config = json.load(f)['spotify']

CLIENT_ID = config['client_id']
CLIENT_SECRET = config['client_secret']
REDIRECT_URI = config['redirect_uri']

# Scopes - what we want access to
SCOPES = [
    'user-read-private',
    'user-read-email',
    'user-read-playback-state',
    'user-modify-playback-state',
    'user-read-currently-playing',
    'user-read-recently-played',
    'user-top-read',
    'playlist-read-private',
    'playlist-read-collaborative',
    'user-library-read',
    'user-read-playback-position'
]

# Step 1: Generate authorization URL
auth_url = f"https://accounts.spotify.com/authorize"
params = {
    'client_id': CLIENT_ID,
    'response_type': 'code',
    'redirect_uri': REDIRECT_URI,
    'scope': ' '.join(SCOPES)
}

auth_full_url = f"{auth_url}?{urllib.parse.urlencode(params)}"

print("="*70)
print("🎵 SPOTIFY AUTHENTICATION")
print("="*70)
print()
print("Step 1: Open this URL in your browser:")
print()
print(auth_full_url)
print()
print("Step 2: Log in to Spotify and authorize the app")
print()
print("Step 3: You'll be redirected to localhost (it will fail - that's OK)")
print()
print("Step 4: Copy the 'code' parameter from the URL")
print("   Example: http://localhost:8888/callback?code=AQD...")
print("                              ^^^^^^^^^^^^^^^^^^^^^^^")
print()
print("Step 5: Run: python3 /root/.openclaw/workspace/scripts/spotify_get_token.py <code>")
print("="*70)
