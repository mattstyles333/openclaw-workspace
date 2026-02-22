#!/usr/bin/env python3
"""
Generate playlist by finding similar artists and their top tracks
"""

import json
import urllib.request
import urllib.parse

# Load credentials
with open('/root/.openclaw/workspace/.spotify_config.json', 'r') as f:
    config = json.load(f)['spotify']

ACCESS_TOKEN = config.get('access_token')

if not ACCESS_TOKEN:
    print("❌ Not authenticated!")
    exit(1)

print("🎵 Analyzing your music taste...")

# Get liked songs
try:
    req = urllib.request.Request(
        'https://api.spotify.com/v1/me/tracks?limit=30',
        headers={'Authorization': f'Bearer {ACCESS_TOKEN}'}
    )
    
    with urllib.request.urlopen(req) as response:
        liked = json.loads(response.read().decode())
        liked_items = liked.get('items', [])
        
        print(f"✅ Found {len(liked_items)} liked songs")
        print()
        
        # Extract unique artists
        artists = {}
        for item in liked_items:
            track = item.get('track', {})
            for artist in track.get('artists', []):
                artist_id = artist.get('id')
                name = artist.get('name')
                if artist_id and name and artist_id not in artists:
                    artists[artist_id] = name
        
        print("🎤 Your Artists:")
        artist_list = list(artists.items())[:10]
        for aid, name in artist_list:
            print(f"  • {name}")
        print()
        
        # Get similar artists by searching
        print("🔮 Finding similar artists and songs...")
        print()
        
        recommendations = []
        
        # For each artist, search for similar ones
        for artist_id, artist_name in artist_list[:5]:
            try:
                # Search for the artist to get their top tracks
                search_url = f"https://api.spotify.com/v1/search?q={urllib.parse.quote(artist_name)}&type=artist&limit=1"
                req = urllib.request.Request(
                    search_url,
                    headers={'Authorization': f'Bearer {ACCESS_TOKEN}'}
                )
                
                with urllib.request.urlopen(req) as response:
                    search_data = json.loads(response.read().decode())
                    artists_found = search_data.get('artists', {}).get('items', [])
                    
                    if artists_found:
                        found_artist = artists_found[0]
                        # Get artist's top tracks
                        top_tracks_url = f"https://api.spotify.com/v1/artists/{found_artist['id']}/top-tracks?market=GB"
                        
                        req = urllib.request.Request(
                            top_tracks_url,
                            headers={'Authorization': f'Bearer {ACCESS_TOKEN}'}
                        )
                        
                        with urllib.request.urlopen(req) as response:
                            tracks_data = json.loads(response.read().decode())
                            top_tracks = tracks_data.get('tracks', [])
                            
                            # Add top 2 tracks from each artist
                            for track in top_tracks[:2]:
                                if track.get('id') not in [r.get('id') for r in recommendations]:
                                    recommendations.append(track)
                                    
            except Exception as e:
                print(f"  ⚠️ Could not get tracks for {artist_name}: {e}")
                continue
        
        # Also search for "similar to" each artist
        print("🔍 Searching for similar artists...")
        for artist_id, artist_name in artist_list[:3]:
            try:
                # Search for similar artists
                search_query = f"artists similar to {artist_name}"
                search_url = f"https://api.spotify.com/v1/search?q={urllib.parse.quote(search_query)}&type=track&limit=5"
                
                req = urllib.request.Request(
                    search_url,
                    headers={'Authorization': f'Bearer {ACCESS_TOKEN}'}
                )
                
                with urllib.request.urlopen(req) as response:
                    search_data = json.loads(response.read().decode())
                    tracks = search_data.get('tracks', {}).get('items', [])
                    
                    for track in tracks:
                        if track.get('id') not in [r.get('id') for r in recommendations]:
                            recommendations.append(track)
                            if len(recommendations) >= 20:
                                break
                                
                if len(recommendations) >= 20:
                    break
                    
            except Exception as e:
                continue
        
        # Display recommendations
        if recommendations:
            print()
            print("=" * 70)
            print("🎵 RECOMMENDED PLAYLIST - Based on Your Liked Songs")
            print("=" * 70)
            print()
            print(f"Generated {len(recommendations)} song recommendations")
            print()
            print("-" * 70)
            
            for i, track in enumerate(recommendations[:20], 1):
                name = track.get('name', 'Unknown')
                track_artists = ', '.join([a.get('name', 'Unknown') for a in track.get('artists', [])])
                album = track.get('album', {}).get('name', 'Unknown')
                track_id = track.get('id')
                
                print(f"{i:2}. {name}")
                print(f"    🎤 {track_artists}")
                print(f"    💿 {album}")
                print(f"    🔗 https://open.spotify.com/track/{track_id}")
                print()
            
            print("=" * 70)
            print()
            
            # Save for playlist creation
            with open('/tmp/spotify_recommendations.json', 'w') as f:
                json.dump({
                    'track_ids': [t.get('id') for t in recommendations[:20]],
                    'tracks': [{'name': t.get('name'), 'artists': [a.get('name') for a in t.get('artists', [])], 'id': t.get('id')} for t in recommendations[:20]]
                }, f, indent=2)
            
            print("✅ Recommendations saved to /tmp/spotify_recommendations.json")
            print()
            print("💡 Want me to create this as an actual Spotify playlist?")
            print("   I can create it and add all these tracks!")
            
        else:
            print("⚠️ Could not generate recommendations. Please try again later.")
                
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
