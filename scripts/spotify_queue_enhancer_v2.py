#!/usr/bin/env python3
"""
Spotify Queue Enhancer - Improved Version
Analyzes liked songs and suggests queue improvements
"""

import json
import requests
import base64

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
        config['access_token'] = new_token['access_token']
        with open('/root/.openclaw/workspace/.spotify_config.json', 'w') as f:
            json.dump({'spotify': config}, f, indent=2)
        return new_token['access_token']
    return None

def get_liked_songs(limit=50):
    """Get user's liked/saved songs"""
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    
    response = requests.get(
        f'https://api.spotify.com/v1/me/tracks?limit={limit}',
        headers=headers
    )
    
    if response.status_code == 401:
        new_token = refresh_access_token()
        if new_token:
            headers = {'Authorization': f'Bearer {new_token}'}
            response = requests.get(
                f'https://api.spotify.com/v1/me/tracks?limit={limit}',
                headers=headers
            )
    
    if response.status_code == 200:
        return response.json().get('items', [])
    return []

def get_audio_features(track_ids):
    """Get audio features for tracks (danceability, energy, etc.)"""
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    
    ids_str = ','.join(track_ids[:100])  # Max 100 per request
    response = requests.get(
        f'https://api.spotify.com/v1/audio-features?ids={ids_str}',
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json().get('audio_features', [])
    return []

def get_recommendations_by_artists(seed_artists, limit=20):
    """Get recommendations based on seed artists"""
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    
    seed_string = ','.join(seed_artists[:5])  # Max 5 seeds
    
    response = requests.get(
        f'https://api.spotify.com/v1/recommendations?seed_artists={seed_string}&limit={limit}',
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json().get('tracks', [])
    return []

def search_similar_tracks(artist_name, track_name):
    """Search for similar tracks"""
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    
    query = f"artist:{artist_name}"
    response = requests.get(
        f'https://api.spotify.com/v1/search?q={query}&type=track&limit=5',
        headers=headers
    )
    
    if response.status_code == 200:
        tracks = response.json().get('tracks', {}).get('items', [])
        return [t for t in tracks if t.get('name') != track_name][:3]
    return []

def main():
    print("=" * 70)
    print("🎵 SPOTIFY QUEUE ENHANCER")
    print("=" * 70)
    print()
    
    # Get liked songs
    print("📥 Loading your liked songs...")
    liked_songs = get_liked_songs(limit=50)
    
    if not liked_songs:
        print("❌ Could not retrieve liked songs")
        return
    
    print(f"✅ Loaded {len(liked_songs)} liked songs")
    print()
    
    # Analyze
    artists = {}
    track_info = []
    
    for item in liked_songs:
        track = item.get('track', {})
        if not track:
            continue
            
        artist = track.get('artists', [{}])[0]
        artist_name = artist.get('name', 'Unknown')
        artist_id = artist.get('id', '')
        track_name = track.get('name', 'Unknown')
        track_id = track.get('id', '')
        
        if artist_name in artists:
            artists[artist_name]['count'] += 1
            artists[artist_name]['ids'].add(artist_id)
        else:
            artists[artist_name] = {'count': 1, 'ids': {artist_id}}
        
        track_info.append({
            'name': track_name,
            'artist': artist_name,
            'id': track_id
        })
    
    # Show top artists
    print("🎤 YOUR TOP ARTISTS:")
    print("-" * 70)
    sorted_artists = sorted(artists.items(), key=lambda x: x[1]['count'], reverse=True)[:10]
    for i, (artist, data) in enumerate(sorted_artists, 1):
        print(f"{i:2d}. {artist:<30} ({data['count']} songs)")
    print()
    
    # Get audio features for mood analysis
    print("🎚️ Analyzing music characteristics...")
    track_ids = [t['id'] for t in track_info if t['id']][:20]
    
    if track_ids:
        features = get_audio_features(track_ids)
        
        if features:
            # Calculate averages
            avg_energy = sum(f.get('energy', 0) for f in features if f) / len([f for f in features if f])
            avg_danceability = sum(f.get('danceability', 0) for f in features if f) / len([f for f in features if f])
            avg_valence = sum(f.get('valence', 0) for f in features if f) / len([f for f in features if f])
            avg_tempo = sum(f.get('tempo', 0) for f in features if f) / len([f for f in features if f])
            
            print(f"   Energy:        {avg_energy:.0%} {'(High energy)' if avg_energy > 0.6 else '(Chill)'}")
            print(f"   Danceability:  {avg_danceability:.0%}")
            print(f"   Positivity:    {avg_valence:.0%} {'(Upbeat)' if avg_valence > 0.5 else '(Melancholic)'}")
            print(f"   Average Tempo: {avg_tempo:.0f} BPM")
            print()
            
            # Mood detection
            if avg_energy > 0.7 and avg_valence > 0.6:
                mood = "🎉 PARTY / HIGH ENERGY"
            elif avg_energy > 0.6:
                mood = "💪 PRODUCTIVE / FOCUSED"
            elif avg_valence > 0.6:
                mood = "😊 HAPPY / UPBEAT"
            elif avg_energy < 0.4:
                mood = "😌 CHILL / RELAXED"
            else:
                mood = "🎵 BALANCED / MIXED"
            
            print(f"🎭 DETECTED MOOD: {mood}")
            print()
    
    # Get recommendations using top artists as seeds
    print("🎯 GETTING RECOMMENDATIONS:")
    print("-" * 70)
    
    # Get top 3 artist IDs
    top_artist_ids = []
    for artist, data in sorted_artists[:3]:
        ids = list(data['ids'])
        if ids and ids[0]:
            top_artist_ids.append(ids[0])
    
    if top_artist_ids:
        recommendations = get_recommendations_by_artists(top_artist_ids, limit=15)
        
        if recommendations:
            print(f"Found {len(recommendations)} recommended tracks:\n")
            
            for i, track in enumerate(recommendations[:10], 1):
                name = track.get('name', 'Unknown')
                artist = track.get('artists', [{}])[0].get('name', 'Unknown')
                album = track.get('album', {}).get('name', '')
                uri = track.get('uri', '')
                
                print(f"{i:2d}. {name}")
                print(f"    Artist: {artist}")
                if album:
                    print(f"    Album:  {album}")
                print()
            
            # Save recommendations to file for queueing
            rec_data = {
                'timestamp': datetime.now().isoformat(),
                'mood': mood if 'mood' in locals() else 'unknown',
                'top_artists': [a[0] for a in sorted_artists[:5]],
                'recommendations': [
                    {
                        'name': t.get('name'),
                        'artist': t.get('artists', [{}])[0].get('name'),
                        'uri': t.get('uri'),
                        'id': t.get('id')
                    }
                    for t in recommendations[:10]
                ]
            }
            
            with open('/root/.openclaw/workspace/.spotify_recommendations.json', 'w') as f:
                json.dump(rec_data, f, indent=2)
            
            print("✅ Recommendations saved to .spotify_recommendations.json")
            print()
            print("🎧 TO ADD TO YOUR QUEUE:")
            print("   1. Make sure Spotify is open and playing")
            print("   2. Run: python3 /root/.openclaw/workspace/scripts/spotify_add_to_queue.py")
            print()
            print("💡 TIP: You can also create a playlist from these recommendations")
            print("        Ask me to 'create a playlist from my recommendations'")
        else:
            print("❌ Could not get recommendations from Spotify API")
            print("   This might be due to API limitations or authentication")
    
    print("=" * 70)

if __name__ == '__main__':
    from datetime import datetime
    main()
