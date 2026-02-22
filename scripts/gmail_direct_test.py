#!/usr/bin/env python3
"""
Gmail OAuth Direct Access
Uses the tokens directly without gog CLI issues
"""

import json
import os
import sys

def load_tokens():
    """Load tokens from gog storage"""
    tokens_path = os.path.expanduser('~/.config/gogcli/tokens.json')
    if os.path.exists(tokens_path):
        with open(tokens_path, 'r') as f:
            return json.load(f)
    return {}

def test_gmail_access(email):
    """Test Gmail API access with curl"""
    tokens = load_tokens()
    
    if email not in tokens:
        print(f"❌ No token found for {email}")
        return False
    
    token = tokens[email].get('access_token')
    if not token:
        print(f"❌ No access token for {email}")
        return False
    
    # Test with Gmail API
    import subprocess
    cmd = [
        'curl', '-s', '-H', f'Authorization: Bearer {token}',
        'https://gmail.googleapis.com/gmail/v1/users/me/profile'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        data = json.loads(result.stdout)
        
        if 'emailAddress' in data:
            print(f"✅ SUCCESS! Connected to: {data['emailAddress']}")
            print(f"   Messages: {data.get('messagesTotal', 'N/A')}")
            print(f"   Threads: {data.get('threadsTotal', 'N/A')}")
            return True
        else:
            print(f"❌ Error: {data.get('error', {}).get('message', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

def search_gmail(email, query='is:unread', max_results=5):
    """Search Gmail using direct API"""
    tokens = load_tokens()
    
    if email not in tokens:
        print(f"❌ No token found for {email}")
        return
    
    token = tokens[email].get('access_token')
    
    import subprocess
    import urllib.parse
    
    encoded_query = urllib.parse.quote(query)
    url = f'https://gmail.googleapis.com/gmail/v1/users/me/messages?q={encoded_query}&maxResults={max_results}'
    
    cmd = [
        'curl', '-s', '-H', f'Authorization: Bearer {token}',
        url
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        data = json.loads(result.stdout)
        
        messages = data.get('messages', [])
        print(f"\n📧 Search: '{query}'")
        print(f"   Found: {len(messages)} messages\n")
        
        for i, msg in enumerate(messages[:max_results], 1):
            # Get message details
            msg_cmd = [
                'curl', '-s', '-H', f'Authorization: Bearer {token}',
                f'https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg["id"]}?format=metadata&metadataHeaders=Subject&metadataHeaders=From&metadataHeaders=Date'
            ]
            msg_result = subprocess.run(msg_cmd, capture_output=True, text=True, timeout=5)
            msg_data = json.loads(msg_result.stdout)
            
            headers = {h['name']: h['value'] for h in msg_data.get('payload', {}).get('headers', [])}
            subject = headers.get('Subject', 'No Subject')[:50]
            from_addr = headers.get('From', 'Unknown')[:40]
            
            print(f"{i}. {subject}")
            print(f"   From: {from_addr}")
            print()
            
    except Exception as e:
        print(f"❌ Search failed: {e}")

if __name__ == '__main__':
    print("=" * 60)
    print("Gmail Direct API Test")
    print("=" * 60)
    print()
    
    # Test both accounts
    print("Testing info@spex4less.com:")
    test_gmail_access('info@spex4less.com')
    
    print()
    print("Testing matt@spex4less.com:")
    test_gmail_access('matt@spex4less.com')
    
    print()
    print("=" * 60)
    
    # Sample searches
    if len(sys.argv) > 1:
        email = sys.argv[1]
        query = sys.argv[2] if len(sys.argv) > 2 else 'is:unread'
        search_gmail(email, query)
