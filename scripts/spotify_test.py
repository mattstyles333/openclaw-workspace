#!/usr/bin/env python3
"""
Spotify API Test - Show what you can do!
"""

import json
import urllib.request

# Load credentials
try:
    with open('/root/.openclaw/workspace/.spotify_config.json', 'r') as f:
        config = json.load(f)['spotify']
    
    ACCESS_TOKEN = config.get('access_token')
    
    if not ACCESS_TOKEN:
        print("❌ Not authenticated yet!")
        print("Run: python3 /root/.openclaw/workspace/scripts/spotify_auth.py")
        exit(1)
    
    # Test API - Get user profile
    req = urllib.request.Request(
        'https://api.spotify.com/v1/me',
        headers={'Authorization': f'Bearer {ACCESS_TOKEN}'}
    )
    
    with urllib.request.urlopen(req) as response:
        profile = json.loads(response.read().decode())
        
        print("="*70)
        print("🎵 SPOTIFY INTEGRATION READY!")
        print("="*70)
        print()
        print(f"Connected as: {profile.get('display_name', 'Unknown')}")
        print(f"Email: {profile.get('email', 'N/A')}")
        print(f"Country: {profile.get('country', 'N/A')}")
        print(f"Account: {'Premium' if profile.get('product') == 'premium' else 'Free'}")
        print()
        print("="*70)
        print()
        print("You can now:")
        print("  • Search for tracks, albums, artists")
        print("  • View your playlists")
        print("  • Get recommendations")
        print("  • View currently playing (if active device)")
        if profile.get('product') == 'premium':
            print("  • Control playback (play/pause/skip) ✅")
        else:
            print("  • ⚠️ Playback control requires Premium")
        print()
        print("Try: python3 /root/.openclaw/workspace/scripts/spotify_search.py 'daft punk'")
        print("="*70)
        
except Exception as e:
    print(f"❌ Error: {e}")
