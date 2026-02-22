#!/usr/bin/env python3
"""
Exchange authorization code for access token
"""

import json
import base64
import urllib.parse
import urllib.request
import sys

if len(sys.argv) < 2:
    print("Usage: python3 spotify_get_token.py <authorization_code>")
    sys.exit(1)

auth_code = sys.argv[1]

# Load credentials
with open('/root/.openclaw/workspace/.spotify_config.json', 'r') as f:
    config = json.load(f)['spotify']

CLIENT_ID = config['client_id']
CLIENT_SECRET = config['client_secret']
REDIRECT_URI = config['redirect_uri']

# Prepare token request
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

# Make request
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
        
        print("="*70)
        print("✅ AUTHENTICATION SUCCESSFUL!")
        print("="*70)
        print()
        print(f"Access Token: {token_data['access_token'][:20]}...")
        print(f"Refresh Token: {token_data['refresh_token'][:20]}...")
        print(f"Expires in: {token_data['expires_in']} seconds")
        print()
        print("Your Spotify integration is now ready to use!")
        print("="*70)
        
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
