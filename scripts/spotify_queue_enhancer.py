#!/usr/bin/env python3
"""
Spotify Queue Enhancer
Analyzes liked songs and improves queue with smart recommendations
"""

import json
import requests
import base64
import sys
from datetime import datetime, timedelta

# Load Spotify config
with open('/root/.openclaw/workspace/.spotify_config.json', 'r') as f:
    config = json.load(f)['spotify']

ACCESS_TOKEN = config['access_token']
REFRESH_TOKEN = config['refresh_token']
CLIENT_ID = config['client_id']
CLIENT_SECRET = config['client_secret']

def refresh_access_token():
    """Refresh the access token using refresh token"""
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_bytes = auth_str.encode('ascii')
    auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
    
    headers = {
        'Authorization': f'Basic {auth_b64}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN
    }
    
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    
    if response.status_code == 200:
        new_token = response.json()
        # Update config
        config['access_token'] = new_token['access_token']
        config['token_type'] = new_token.get('token_type', 'Bearer')
        config['expires_in'] = new_token.get('expires_in', 3600)
        
        with open('/root/.openclaw/workspace/.spotify_config.json', 'w') as f:
            json.dump({'spotify': config}, f, indent=2)
        
        print("✅ Token refreshed successfully!")
        return new_token['access_token']
    else:
        print(f"❌ Failed to refresh token: {response.text}")
        return None

def get_liked_songs(limit=50):
    """Get user's liked/saved songs"""
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    
    response = requests.get(
        f'https://api.spotify.com/v1/me/tracks?limit={limit}',
        headers=headers
    )
    
    if response.status_code == 401:
        # Token expired, refresh it
        print("🔄 Token expired, refreshing...")
        new_token = refresh_access_token()
        if new_token:
            headers = {'Authorization': f'Bearer {new_token}'}
            response = requests.get(
                f'https://api.spotify.com/v1/me/tracks?limit={limit}',
                headers=headers
            )
    
    if response.status_code == 200:
        data = response.json()
        tracks = data.get('items', [])
        
        print(f"🎵 Found {len(tracks)} liked songs")
        print()
        
        # Analyze tracks
        artists = {}
        genres = set()
        
        for item in tracks:
            track = item.get('track', {})
            artist = track.get('artists', [{}])[0].get('name', 'Unknown')
            track_name = track.get('name', 'Unknown')
            
            if artist in artists:
                artists[artist] += 1
            else:
                artists[artist] = 1
        
        # Show top artists
        print("🎤 Your Top Artists:")
        sorted_artists = sorted(artists.items(), key=lambda x: x[1], reverse=True)[:10]
        for i, (artist, count) in enumerate(sorted_artists, 1):
            print(f"  {i}. {artist} ({count} songs)")
        
        return tracks, sorted_artists
    else:
        print(f"❌ Failed to get liked songs: {response.status_code}")
        print(response.text)
        return [], []

def get_recommendations(seed_tracks, limit=20):
    """Get recommendations based on liked songs"""
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    
    # Get track IDs for seed
    seed_ids = [track.get('track', {}).get('id') for track in seed_tracks[:5] if track.get('track', {}).get('id')]
    seed_string = ','.join(seed_ids)
    
    response = requests.get(
        f'https://api.spotify.com/v1/recommendations?seed_tracks={seed_string}&limit={limit}',
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        tracks = data.get('tracks', [])
        
        print(f"\n🎯 Recommendations based on your liked songs:")
        print("=" * 60)
        for i, track in enumerate(tracks[:10], 1):
            name = track.get('name', 'Unknown')
            artist = track.get('artists', [{}])[0].get('name', 'Unknown')
            album = track.get('album', {}).get('name', 'Unknown')
            print(f"{i}. {name}")
            print(f"   by {artist} | Album: {album}")
            print()
        
        return tracks
    else:
        print(f"❌ Failed to get recommendations: {response.status_code}")
        return []

def add_to_queue(track_uris):
    """Add tracks to playback queue"""
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    
    added = []
    for uri in track_uris[:10]:  # Add up to 10 songs
        response = requests.post(
            f'https://api.spotify.com/v1/me/player/queue?uri={uri}',
            headers=headers
        )
        if response.status_code == 204:
            added.append(uri)
    
    return added

def main():
    print("=" * 60)
    print("🎵 Spotify Queue Enhancer")
    print("=" * 60)
    print()
    
    # Step 1: Get liked songs
    print("📥 Analyzing your liked songs...")
    liked_songs, top_artists = get_liked_songs(limit=50)
    
    if not liked_songs:
        print("❌ Could not retrieve liked songs. Please check authentication.")
        return
    
    print()
    
    # Step 2: Get recommendations
    print("🎯 Getting personalized recommendations...")
    recommendations = get_recommendations(liked_songs, limit=20)
    
    if not recommendations:
        print("❌ Could not get recommendations.")
        return
    
    print()
    
    # Step 3: Ask if user wants to add to queue
    print("=" * 60)
    print("✅ Analysis complete!")
    print(f"   • Analyzed {len(liked_songs)} liked songs")
    print(f"   • Top artist: {top_artists[0][0] if top_artists else 'N/A'}")
    print(f"   • Generated {len(recommendations)} recommendations")
    print()
    print("To add these recommendations to your queue:")
    print("  1. Open Spotify on your device")
    print("  2. Start playing any song")
    print("  3. Run: python3 /root/.openclaw/workspace/scripts/spotify_add_to_queue.py")
    print()
    print("Note: Spotify Premium required for queue management")
    print("=" * 60)

if __name__ == '__main__':
    main()
