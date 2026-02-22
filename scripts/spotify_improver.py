#!/usr/bin/env python3
"""
Spotify Queue Helper - Simple version
Gets your liked songs and suggests similar tracks
"""

import json
import requests
import base64

# Load config
with open('/root/.openclaw/workspace/.spotify_config.json', 'r') as f:
    config = json.load(f)['spotify']

ACCESS_TOKEN = config['access_token']
REFRESH_TOKEN = config['refresh_token']
CLIENT_ID = config['client_id']
CLIENT_SECRET = config['client_secret']

def make_request(url, method='GET', data=None):
    """Make authenticated request with auto-refresh"""
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    
    if method == 'GET':
        response = requests.get(url, headers=headers)
    else:
        headers['Content-Type'] = 'application/json'
        response = requests.post(url, headers=headers, json=data)
    
    # If token expired, refresh and retry
    if response.status_code == 401:
        auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
        auth_b64 = base64.b64encode(auth_str.encode()).decode()
        
        refresh_resp = requests.post(
            'https://accounts.spotify.com/api/token',
            headers={
                'Authorization': f'Basic {auth_b64}',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={'grant_type': 'refresh_token', 'refresh_token': REFRESH_TOKEN}
        )
        
        if refresh_resp.status_code == 200:
            new_token = refresh_resp.json()['access_token']
            config['access_token'] = new_token
            with open('/root/.openclaw/workspace/.spotify_config.json', 'w') as f:
                json.dump({'spotify': config}, f, indent=2)
            
            # Retry with new token
            headers = {'Authorization': f'Bearer {new_token}'}
            if method == 'GET':
                response = requests.get(url, headers=headers)
            else:
                response = requests.post(url, headers=headers, json=data)
    
    return response

def get_liked_songs():
    """Get your saved tracks"""
    resp = make_request('https://api.spotify.com/v1/me/tracks?limit=50')
    if resp.status_code == 200:
        return resp.json().get('items', [])
    return []

def get_artist_top_tracks(artist_id):
    """Get artist's top tracks"""
    resp = make_request(f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US')
    if resp.status_code == 200:
        return resp.json().get('tracks', [])
    return []

def get_related_artists(artist_id):
    """Get related artists"""
    resp = make_request(f'https://api.spotify.com/v1/artists/{artist_id}/related-artists')
    if resp.status_code == 200:
        return resp.json().get('artists', [])
    return []

def search_tracks(query, limit=10):
    """Search for tracks"""
    resp = make_request(f'https://api.spotify.com/v1/search?q={query}&type=track&limit={limit}')
    if resp.status_code == 200:
        return resp.json().get('tracks', {}).get('items', [])
    return []

def add_to_queue(uri):
    """Add track to queue"""
    resp = make_request(f'https://api.spotify.com/v1/me/player/queue?uri={uri}', method='POST')
    return resp.status_code == 204

def main():
    print("=" * 70)
    print("🎵 SPOTIFY QUEUE IMPROVER")
    print("=" * 70)
    print()
    
    # Get liked songs
    print("Loading your liked songs...")
    liked = get_liked_songs()
    
    if not liked:
        print("❌ Could not load liked songs")
        return
    
    print(f"✅ Found {len(liked)} liked songs\n")
    
    # Extract unique artists
    artists = {}
    for item in liked:
        track = item.get('track', {})
        for artist in track.get('artists', []):
            name = artist.get('name')
            aid = artist.get('id')
            if name and aid:
                artists[name] = aid
    
    # Show liked songs
    print("❤️ YOUR LIKED SONGS:")
    print("-" * 70)
    for i, item in enumerate(liked[:10], 1):
        track = item.get('track', {})
        print(f"{i}. {track.get('name')} - {track.get('artists', [{}])[0].get('name')}")
    print()
    
    # Get recommendations from related artists
    print("🎧 FINDING SIMILAR MUSIC:")
    print("-" * 70)
    
    suggestions = []
    
    # Try top 3 artists
    for artist_name, artist_id in list(artists.items())[:3]:
        print(f"\nLooking for music similar to: {artist_name}")
        
        # Get related artists
        related = get_related_artists(artist_id)
        if related:
            print(f"  Found {len(related)} related artists")
            
            # Get top tracks from first 2 related artists
            for rel_artist in related[:2]:
                rel_name = rel_artist.get('name')
                rel_id = rel_artist.get('id')
                
                top_tracks = get_artist_top_tracks(rel_id)
                if top_tracks:
                    for track in top_tracks[:2]:  # Top 2 tracks
                        suggestions.append({
                            'name': track.get('name'),
                            'artist': rel_name,
                            'uri': track.get('uri'),
                            'id': track.get('id'),
                            'based_on': artist_name
                        })
    
    # Show suggestions
    if suggestions:
        print(f"\n🎯 FOUND {len(suggestions)} SUGGESTIONS:")
        print("=" * 70)
        
        for i, track in enumerate(suggestions[:15], 1):
            print(f"\n{i}. {track['name']}")
            print(f"   Artist: {track['artist']}")
            print(f"   Similar to: {track['based_on']}")
        
        # Save suggestions
        with open('/root/.openclaw/workspace/.spotify_suggestions.json', 'w') as f:
            json.dump(suggestions, f, indent=2)
        
        print("\n" + "=" * 70)
        print("✅ Suggestions saved to .spotify_suggestions.json")
        
        # Ask if they want to add to queue
        print("\n💡 TO ADD TO QUEUE:")
        print("   1. Open Spotify and start playing music")
        print("   2. Run: python3 /root/.openclaw/workspace/scripts/spotify_add_suggestions.py")
        
    else:
        print("❌ Could not find suggestions")
        print("   This might be due to API limits or artist availability")
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()
