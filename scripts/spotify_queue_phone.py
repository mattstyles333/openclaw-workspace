#!/usr/bin/env python3
"""
Add tracks to Spotify playback queue on phone
"""

import json
import urllib.request
import urllib.error

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
        tracks_info = data.get('tracks', [])
        
    if not track_ids:
        print("❌ No tracks found!")
        exit(1)
        
    print("🎵 Adding tracks to your phone's queue...")
    print()
    
    # Get active device
    req = urllib.request.Request(
        'https://api.spotify.com/v1/me/player/devices',
        headers={'Authorization': f'Bearer {ACCESS_TOKEN}'}
    )
    
    with urllib.request.urlopen(req) as response:
        devices = json.loads(response.read().decode())
        active_devices = [d for d in devices.get('devices', []) if d.get('is_active')]
        
        if not active_devices:
            print("❌ No active device found!")
            exit(1)
        
        device_id = active_devices[0].get('id')
        device_name = active_devices[0].get('name')
        print(f"📱 Target device: {device_name}")
        print()
    
    # Add tracks to queue (one by one)
    print("Adding tracks...")
    print()
    
    added_count = 0
    failed_tracks = []
    
    for i, track_id in enumerate(track_ids[:15], 1):  # Add all 15
        track_uri = f"spotify:track:{track_id}"
        track_name = tracks_info[i-1].get('name', 'Unknown')
        track_artists = ', '.join(tracks_info[i-1].get('artists', ['Unknown']))
        
        # Build URL with device_id
        url = f'https://api.spotify.com/v1/me/player/queue?uri={track_uri}&device_id={device_id}'
        
        req = urllib.request.Request(
            url,
            headers={'Authorization': f'Bearer {ACCESS_TOKEN}'},
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                if response.status == 204:
                    print(f"  ✅ {i:2}. {track_name} - {track_artists}")
                    added_count += 1
                else:
                    print(f"  ⚠️  {i:2}. {track_name} - Status: {response.status}")
                    failed_tracks.append((track_name, response.status))
                    
        except urllib.error.HTTPError as e:
            error_msg = f"HTTP {e.code}"
            if e.code == 403:
                error_msg = "Permission denied (app in dev mode)"
            elif e.code == 404:
                error_msg = "Device not found"
            
            print(f"  ❌ {i:2}. {track_name} - {error_msg}")
            failed_tracks.append((track_name, e.code))
    
    print()
    print("=" * 70)
    if added_count > 0:
        print(f"✅ Successfully added {added_count} of {len(track_ids)} tracks to your phone!")
        print()
        print(f"📱 Device: {device_name}")
        print()
        print("🎧 Check your Spotify app - the songs should be in your queue!")
        print("   (Tap the queue icon in the bottom right)")
        
        if failed_tracks:
            print()
            print(f"⚠️  {len(failed_tracks)} tracks failed to add")
    else:
        print("❌ Could not add any tracks to queue")
        print()
        print("This is likely because:")
        print("  • Your Spotify app is in 'Development Mode'")
        print("  • The API needs additional permissions")
        print("  • Spotify restricts queue modification for security")
        print()
        print("💡 Workaround: Use the track URLs below to manually add to queue")
    print("=" * 70)
    
    if failed_tracks:
        print()
        print("Failed tracks (for manual adding):")
        for name, code in failed_tracks:
            print(f"  • {name} (Error {code})")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
