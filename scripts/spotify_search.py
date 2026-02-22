#!/usr/bin/env python3
"""
Search Spotify
Usage: python3 spotify_search.py "your search query"
"""

import json
import urllib.request
import urllib.parse
import sys

if len(sys.argv) < 2:
    print("Usage: python3 spotify_search.py 'artist or song name'")
    sys.exit(1)

query = sys.argv[1]

# Load credentials
try:
    with open('/root/.openclaw/workspace/.spotify_config.json', 'r') as f:
        config = json.load(f)['spotify']
    
    ACCESS_TOKEN = config.get('access_token')
    
    if not ACCESS_TOKEN:
        print("❌ Not authenticated yet!")
        print("Run: python3 /root/.openclaw/workspace/scripts/spotify_auth.py")
        exit(1)
    
    # Search
    search_url = f"https://api.spotify.com/v1/search?q={urllib.parse.quote(query)}&type=track,artist,album&limit=5"
    
    req = urllib.request.Request(
        search_url,
        headers={'Authorization': f'Bearer {ACCESS_TOKEN}'}
    )
    
    with urllib.request.urlopen(req) as response:
        results = json.loads(response.read().decode())
        
        print("="*70)
        print(f"🔍 SEARCH RESULTS FOR: '{query}'")
        print("="*70)
        print()
        
        # Tracks
        if results.get('tracks', {}).get('items'):
            print("🎵 TRACKS:")
            for track in results['tracks']['items'][:3]:
                artists = ', '.join([a['name'] for a in track['artists']])
                print(f"  • {track['name']} - {artists}")
            print()
        
        # Artists
        if results.get('artists', {}).get('items'):
            print("🎤 ARTISTS:")
            for artist in results['artists']['items'][:3]:
                print(f"  • {artist['name']}")
            print()
        
        # Albums
        if results.get('albums', {}).get('items'):
            print("💿 ALBUMS:")
            for album in results['albums']['items'][:3]:
                print(f"  • {album['name']} - {album['artists'][0]['name']}")
            print()
        
        print("="*70)
        
except Exception as e:
    print(f"❌ Error: {e}")
