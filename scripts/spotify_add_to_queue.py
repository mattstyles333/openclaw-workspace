#!/usr/bin/env python3
"""
Add tracks to Spotify playback queue
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
        
    print("🎵 Adding tracks to your playback queue...")
    print(f"   {len(track_ids)} tracks ready to add")
    print()
    
    # Check if there's an active device
    req = urllib.request.Request(
        'https://api.spotify.com/v1/me/player/devices',
        headers={'Authorization': f'Bearer {ACCESS_TOKEN}'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            devices = json.loads(response.read().decode())
            active_devices = [d for d in devices.get('devices', []) if d.get('is_active')]
            
            if not active_devices:
                print("⚠️  No active Spotify device found!")
                print()
                print("To add to queue, you need to:")
                print("1. Open Spotify on your phone, computer, or smart speaker")
                print("2. Start playing any song (or just have Spotify open)")
                print("3. Then run this script again")
                print()
                print("Available devices:")
                for device in devices.get('devices', []):
                    status = "🟢 Active" if device.get('is_active') else "⚪ Inactive"
                    print(f"  • {device.get('name')} ({device.get('type')}) - {status}")
                exit(0)
            
            device_id = active_devices[0].get('id')
            device_name = active_devices[0].get('name')
            print(f"✅ Found active device: {device_name}")
            print()
            
    except urllib.error.HTTPError as e:
        print(f"⚠️  Could not check devices: {e}")
        device_id = None
    
    # Add tracks to queue (one by one since that's how queue works)
    print("Adding tracks to queue...")
    print()
    
    added_count = 0
    for i, track_id in enumerate(track_ids[:10], 1):  # Add first 10
        track_uri = f"spotify:track:{track_id}"
        track_name = tracks_info[i-1].get('name', 'Unknown')
        track_artists = ', '.join(tracks_info[i-1].get('artists', ['Unknown']))
        
        # Build URL with device_id if available
        url = f'https://api.spotify.com/v1/me/player/queue?uri={track_uri}'
        if device_id:
            url += f'&device_id={device_id}'
        
        req = urllib.request.Request(
            url,
            headers={'Authorization': f'Bearer {ACCESS_TOKEN}'},
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                if response.status == 204:
                    print(f"  ✅ {i}. {track_name} - {track_artists}")
                    added_count += 1
                else:
                    print(f"  ⚠️  {i}. {track_name} - Unexpected status: {response.status}")
                    
        except urllib.error.HTTPError as e:
            if e.code == 403:
                print(f"  ❌ {i}. {track_name} - Permission denied (403)")
                print(f"     This usually means queue modification isn't allowed")
            elif e.code == 404:
                print(f"  ❌ {i}. {track_name} - No active device (404)")
            else:
                print(f"  ❌ {i}. {track_name} - Error: {e.code}")
    
    print()
    print("=" * 70)
    if added_count > 0:
        print(f"✅ Added {added_count} tracks to your queue!")
        print()
        print("🎧 Open Spotify and check your queue to see the added songs")
    else:
        print("❌ Could not add tracks to queue")
        print()
        print("This might be because:")
        print("  1. No active Spotify device (open Spotify on your phone/PC)")
        print("  2. Your Spotify app is in development mode")
        print("  3. The API token doesn't have queue modification permissions")
    print("=" * 70)
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
