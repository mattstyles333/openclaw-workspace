#!/usr/bin/env python3
"""
Add tracks to existing Spotify playlist
"""

import json
import urllib.request

# Load credentials
with open('/root/.openclaw/workspace/.spotify_config.json', 'r') as f:
    config = json.load(f)['spotify']

ACCESS_TOKEN = config.get('access_token')

if not ACCESS_TOKEN:
    print("❌ Not authenticated!")
    exit(1)

# Load recommendations
try:
    with open('/tmp/spotify_recommendations.json', 'r') as f:
        data = json.load(f)
        track_ids = data.get('track_ids', [])
        
    if not track_ids:
        print("❌ No recommendations found!")
        exit(1)
        
    # The playlist ID from the successful creation
    playlist_id = "6mEJkBNgdfX5lhh8rKk2OY"  # From previous output
    
    print(f"🎵 Adding {len(track_ids)} tracks to playlist...")
    print()
    
    # Add tracks in smaller batches (Spotify recommends max 100 per request)
    # We'll do all at once since we only have 15
    batch_size = 15
    
    for i in range(0, len(track_ids), batch_size):
        batch = track_ids[i:i+batch_size]
        tracks_uris = [f"spotify:track:{tid}" for tid in batch]
        
        add_data = json.dumps({
            'uris': tracks_uris
        }).encode()
        
        req = urllib.request.Request(
            f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks',
            data=add_data,
            headers={
                'Authorization': f'Bearer {ACCESS_TOKEN}',
                'Content-Type': 'application/json'
            },
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode())
                print(f"✅ Added batch of {len(batch)} tracks")
                
        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            print(f"❌ Error adding tracks: {e.code}")
            print(f"Response: {error_body}")
            
    print()
    print("=" * 70)
    print("🎵 PLAYLIST COMPLETE!")
    print("=" * 70)
    print()
    print("📀 Playlist: OpenClaw Recommendations - 2026-02-18")
    print("🔗 URL: https://open.spotify.com/playlist/6mEJkBNgdfX5lhh8rKk2OY")
    print()
    print("Tracks:")
    for i, track in enumerate(data.get('tracks', [])[:20], 1):
        print(f"  {i:2}. {track['name']} - {', '.join(track['artists'])}")
    print()
    print("=" * 70)
    print()
    print("🎧 Open Spotify to listen to your new playlist!")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
