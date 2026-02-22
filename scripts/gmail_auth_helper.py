#!/usr/bin/env python3
"""
Gmail OAuth Helper for Remote Servers
This script helps authenticate Gmail when running on a remote server via SSH
"""

import json
import urllib.parse
import urllib.request
import sys

def get_auth_url():
    """Generate the Google OAuth URL"""
    params = {
        'access_type': 'offline',
        'client_id': '958285278898-9nhigplt7pkcpabin43trm7f3qkqhdda.apps.googleusercontent.com',
        'redirect_uri': 'http://localhost',
        'response_type': 'code',
        'scope': 'https://www.googleapis.com/auth/gmail.readonly',
        'prompt': 'consent'
    }
    
    base_url = 'https://accounts.google.com/o/oauth2/auth'
    query = urllib.parse.urlencode(params)
    return f"{base_url}?{query}"

def exchange_code_for_token(auth_code):
    """Exchange the authorization code for tokens"""
    
    # Load credentials
    with open('/root/.openclaw/workspace/.gmail_matt_client_secret.json', 'r') as f:
        creds = json.load(f)['installed']
    
    # Token endpoint
    token_url = 'https://oauth2.googleapis.com/token'
    
    # Prepare the request
    data = {
        'code': auth_code,
        'client_id': creds['client_id'],
        'client_secret': creds['client_secret'],
        'redirect_uri': 'http://localhost',
        'grant_type': 'authorization_code'
    }
    
    encoded_data = urllib.parse.urlencode(data).encode('utf-8')
    
    try:
        req = urllib.request.Request(token_url, data=encoded_data, method='POST')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        
        with urllib.request.urlopen(req) as response:
            token_data = json.loads(response.read().decode('utf-8'))
            return token_data
    except Exception as e:
        print(f"Error exchanging code: {e}")
        return None

def save_token(token_data):
    """Save token in gog format"""
    import os
    
    # gog stores tokens in ~/.config/gogcli/tokens.json
    config_dir = os.path.expanduser('~/.config/gogcli')
    os.makedirs(config_dir, exist_ok=True)
    
    tokens_file = os.path.join(config_dir, 'tokens.json')
    
    # Load existing tokens if any
    tokens = {}
    if os.path.exists(tokens_file):
        with open(tokens_file, 'r') as f:
            tokens = json.load(f)
    
    # Add new token
    tokens['matt@spex4less.com'] = {
        'access_token': token_data.get('access_token'),
        'refresh_token': token_data.get('refresh_token'),
        'token_type': token_data.get('token_type', 'Bearer'),
        'expiry': token_data.get('expires_in'),
        'services': ['gmail']
    }
    
    # Save
    with open(tokens_file, 'w') as f:
        json.dump(tokens, f, indent=2)
    
    print(f"✅ Token saved to {tokens_file}")

def main():
    print("=" * 60)
    print("Gmail OAuth Helper for matt@spex4less.com")
    print("=" * 60)
    print()
    
    # Step 1: Show the auth URL
    auth_url = get_auth_url()
    print("Step 1: Open this URL in your browser:")
    print()
    print(auth_url)
    print()
    print("Step 2: Login with matt@spex4less.com and grant permission")
    print()
    print("Step 3: You'll be redirected to a localhost error page.")
    print("         COPY the code from the URL bar")
    print("         (it's after 'code=' and before '&scope=')")
    print()
    
    # Step 2: Get the code from user
    auth_code = input("Step 4: Paste the authorization code here: ").strip()
    
    if not auth_code:
        print("❌ No code provided. Exiting.")
        sys.exit(1)
    
    print()
    print("Exchanging code for token...")
    
    # Step 3: Exchange code for token
    token_data = exchange_code_for_token(auth_code)
    
    if token_data:
        print("✅ Authentication successful!")
        print()
        print("Token details:")
        print(f"  Access Token: {token_data.get('access_token', 'N/A')[:20]}...")
        print(f"  Refresh Token: {'Yes' if token_data.get('refresh_token') else 'No'}")
        print(f"  Expires in: {token_data.get('expires_in', 'N/A')} seconds")
        print()
        
        # Step 4: Save token
        save_token(token_data)
        
        print()
        print("🎉 Setup complete!")
        print()
        print("Test with:")
        print("  export GOG_ACCOUNT=matt@spex4less.com")
        print("  gog gmail search 'is:unread' --max 5")
    else:
        print("❌ Failed to exchange code for token")
        sys.exit(1)

if __name__ == '__main__':
    main()
