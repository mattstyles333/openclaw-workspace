#!/usr/bin/env python3
"""
Complete Spotify OAuth by extracting code from redirect URL
"""

import sys
import json
import base64
import urllib.parse
import urllib.request

if len(sys.argv) < 2:
    print("Usage: python3 complete_spotify_auth.py '<redirect_url>'")
    print("Example: python3 complete_spotify_auth.py 'http://localhost:8888/callback?code=AQDxyz...'")
    sys.exit(1)

redirect_url = sys.argv[1]

# Extract code from URL
parsed = urllib.parse.urlparse(redirect_url)
params = urllib.parse.parse_qs(parsed.query)

if 'code' not in params:
    print("❌ No code found in URL!")
    print(f"URL: {redirect_url}")
    sys.exit(1)

auth_code = params['code'][0]
print(f"✅ Extracted code: {auth_code[:20]}...")

# Load credentials
with open('/root/.openclaw/workspace/.spotify_config.json', 'r') as f:
    config = json.load(f)['spotify']

CLIENT_ID = config['client_id']
CLIENT_SECRET = config['client_secret']
REDIRECT_URI = config['redirect_uri']

# Exchange code for token
token_url = "https://accounts.spotify.com/api/token"
credentials = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

headers = {
    'Authorization': f'Basic {credentials}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

data = urllib.parse.urlencode({
    'grant_type': 'authorization_code',
    'code': auth_code,
    'redirect_uri': REDIRECT_URI
}).encode()

try:
    req = urllib.request.Request(token_url, data=data, headers=headers, method='POST')
    with urllib.request.urlopen(req) as response:
        token_data = json.loads(response.read().decode())
        
        # Save tokens
        config['access_token'] = token_data['access_token']
        config['refresh_token'] = token_data['refresh_token']
        config['token_type'] = token_data['token_type']
        config['expires_in'] = token_data['expires_in']
        
        with open('/root/.openclaw/workspace/.spotify_config.json', 'w') as f:
            json.dump({'spotify': config}, f, indent=2)
        
        print("")
        print("="*70)
        print("✅ SPOTIFY AUTHENTICATION SUCCESSFUL!")
        print("="*70)
        print("")
        print(f"Access Token: {token_data['access_token'][:30]}...")
        print(f"Refresh Token: {token_data['refresh_token'][:30]}...")
        print(f"Expires in: {token_data['expires_in']} seconds")
        print("")
        print("🎵 Your Spotify integration is now ready!")
        print("")
        print("Test it with:")
        print("  python3 /root/.openclaw/workspace/scripts/spotify_test.py")
        print("")
        print("="*70)
        
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
