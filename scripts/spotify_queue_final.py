#!/usr/bin/env python3
"""
Spotify Queue Enhancer - Based on Your Top Artists
"""

import json
import requests
import base64
from datetime import datetime

# Load config
with open('/root/.openclaw/workspace/.spotify_config.json', 'r') as f:
    config = json.load(f)['spotify']

ACCESS_TOKEN = config['access_token']
REFRESH_TOKEN = config['refresh_token']
CLIENT_ID = config['client_id']
CLIENT_SECRET = config['client_secret']

def make_request(url):
    """Make authenticated request with auto-refresh"""
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    resp = requests.get(url, headers=headers)
    
    if resp.status_code == 401:
        # Refresh token
        auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
        auth_b64 = base64.b64encode(auth_str.encode()).decode()
        
        refresh = requests.post(
            'https://accounts.spotify.com/api/token',
            headers={
                'Authorization': f'Basic {auth_b64}',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={'grant_type': 'refresh_token', 'refresh_token': REFRESH_TOKEN}
        )
        
        if refresh.status_code == 200:
            new_token = refresh.json()['access_token']
            config['access_token'] = new_token
            with open('/root/.openclaw/workspace/.spotify_config.json', 'w') as f:
                json.dump({'spotify': config}, f, indent=2)
            
            headers = {'Authorization': f'Bearer {new_token}'}
            resp = requests.get(url, headers=headers)
    
    return resp

def get_top_artists(limit=10):
    """Get user's top artists"""
    resp = make_request(f'https://api.spotify.com/v1/me/top/artists?limit={limit}&time_range=medium_term')
    if resp.status_code == 200:
        return resp.json().get('items', [])
    return []

def get_related_artists(artist_id):
    """Get related artists"""
    resp = make_request(f'https://api.spotify.com/v1/artists/{artist_id}/related-artists')
    if resp.status_code == 200:
        return resp.json().get('artists', [])
    return []

def get_artist_top_tracks(artist_id, market='US'):
    """Get artist's top tracks"""
    resp = make_request(f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market={market}')
    if resp.status_code == 200:
        return resp.json().get('tracks', [])
    return []

def add_to_queue(uri):
    """Add track to queue"""
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    resp = requests.post(
        f'https://api.spotify.com/v1/me/player/queue?uri={uri}',
        headers=headers
    )
    return resp.status_code == 204

def main():
    print("=" * 70)
    print("🎵 SPOTIFY QUEUE ENHANCER")
    print("   Based on your listening history")
    print("=" * 70)
    print()
    
    # Get top artists
    print("📊 Analyzing your top artists...")
    top_artists = get_top_artists(limit=10)
    
    if not top_artists:
        print("❌ Could not retrieve top artists")
        return
    
    print(f"✅ Found {len(top_artists)} top artists\n")
    
    # Display top artists
    print("🎤 YOUR TOP ARTISTS:")
    print("-" * 70)
    for i, artist in enumerate(top_artists, 1):
        name = artist.get('name')
        genres = ', '.join(artist.get('genres', [])[:2])
        print(f"{i:2d}. {name:<25} {genres}")
    print()
    
    # Find similar music
    print("🔍 FINDING SIMILAR ARTISTS & TRACKS:")
    print("=" * 70)
    
    all_suggestions = []
    
    # For top 3 artists, get related artists and their top tracks
    for artist in top_artists[:3]:
        artist_name = artist.get('name')
        artist_id = artist.get('id')
        
        print(f"\n🎧 Based on: {artist_name}")
        print("-" * 50)
        
        # Get related artists
        related = get_related_artists(artist_id)
        if related:
            print(f"   Found {len(related)} similar artists")
            
            # Get top tracks from first 3 related artists
            for rel in related[:3]:
                rel_name = rel.get('name')
                rel_id = rel.get('id')
                
                tracks = get_artist_top_tracks(rel_id)
                if tracks:
                    for track in tracks[:2]:  # Top 2 from each
                        suggestion = {
                            'name': track.get('name'),
                            'artist': rel_name,
                            'album': track.get('album', {}).get('name'),
                            'uri': track.get('uri'),
                            'preview_url': track.get('preview_url'),
                            'based_on': artist_name
                        }
                        all_suggestions.append(suggestion)
                        print(f"   • {track.get('name')} - {rel_name}")
    
    # Show summary
    print("\n" + "=" * 70)
    print(f"🎯 TOTAL SUGGESTIONS: {len(all_suggestions)} tracks")
    print("=" * 70)
    
    if all_suggestions:
        # Save to file
        with open('/root/.openclaw/workspace/.spotify_queue_suggestions.json', 'w') as f:
            json.dump({
                'generated_at': datetime.now().isoformat(),
                'based_on': [a.get('name') for a in top_artists[:5]],
                'suggestions': all_suggestions[:20]
            }, f, indent=2)
        
        print("\n✅ Suggestions saved!")
        print()
        print("🎧 SAMPLE OF RECOMMENDATIONS:")
        print("-" * 70)
        for i, track in enumerate(all_suggestions[:10], 1):
            print(f"{i:2d}. {track['name']}")
            print(f"    Artist: {track['artist']}")
            print(f"    Similar to: {track['based_on']}")
            print()
        
        print("=" * 70)
        print("\n💡 OPTIONS:")
        print("   1. Add all to queue (Spotify must be playing)")
        print("      Run: python3 /root/.openclaw/workspace/scripts/spotify_add_all.py")
        print()
        print("   2. Create a playlist from these suggestions")
        print("      Say: 'Create a playlist from my suggestions'")
        print()
        print("   3. Add specific tracks")
        print("      Say: 'Add track #1, #3, and #5 to my queue'")
        print()
        
        # Ask user what they want to do
        print("What would you like to do?")
        
    else:
        print("❌ Could not generate suggestions")
        print("   This might be due to API rate limits")

if __name__ == '__main__':
    main()
