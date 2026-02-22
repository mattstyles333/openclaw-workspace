#!/usr/bin/env python3
"""
Heartbeat Email Checker for matt@spex4less.com
Checks for new important emails and sends alerts
"""

import json
import os
import sys
import subprocess
from datetime import datetime, timedelta

# Important keywords/patterns
IMPORTANT_KEYWORDS = [
    'order', 'payment', 'invoice', 'refund', 'urgent', 'asap',
    'support', 'complaint', 'dispute', 'legal', 'lawyer',
    'bank', 'wise', 'stripe', 'paypal', 'failed', 'declined',
    'kering', 'supplier', 'shipment', 'delivery', 'return'
]

SENDER_PATTERNS = [
    'kering', 'wise', 'stripe', 'paypal', 'bank', 'santander',
    'customer', 'support', 'noreply', 'no-reply'
]

def load_tokens():
    """Load tokens from gog storage"""
    tokens_path = os.path.expanduser('~/.config/gogcli/tokens.json')
    if os.path.exists(tokens_path):
        with open(tokens_path, 'r') as f:
            return json.load(f)
    return {}

def check_new_emails(email='matt@spex4less.com', hours=1):
    """Check for new emails in the last X hours"""
    tokens = load_tokens()
    
    if email not in tokens:
        return None, f"No token found for {email}"
    
    token = tokens[email].get('access_token')
    if not token:
        return None, f"No access token for {email}"
    
    # Search for emails newer than X hours
    import time
    from datetime import datetime, timedelta
    
    # Gmail API uses seconds for internalDate
    hours_ago = datetime.utcnow() - timedelta(hours=hours)
    timestamp = int(hours_ago.timestamp())
    
    # Use Gmail API to search
    url = f'https://gmail.googleapis.com/gmail/v1/users/me/messages?q=newer_than:{hours}h'
    
    cmd = [
        'curl', '-s', '-H', f'Authorization: Bearer {token}',
        url
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        data = json.loads(result.stdout)
        
        messages = data.get('messages', [])
        return messages, None
    except Exception as e:
        return None, str(e)

def analyze_email_importance(email_id, token):
    """Analyze if an email is important"""
    cmd = [
        'curl', '-s', '-H', f'Authorization: Bearer {token}',
        f'https://gmail.googleapis.com/gmail/v1/users/me/messages/{email_id}?format=metadata&metadataHeaders=Subject&metadataHeaders=From&metadataHeaders=Date'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        msg_data = json.loads(result.stdout)
        
        headers = {h['name']: h['value'] for h in msg_data.get('payload', {}).get('headers', [])}
        subject = headers.get('Subject', '').lower()
        from_addr = headers.get('From', '').lower()
        
        # Check importance
        importance_score = 0
        reasons = []
        
        # Check subject keywords
        for keyword in IMPORTANT_KEYWORDS:
            if keyword in subject:
                importance_score += 2
                reasons.append(f"Keyword: '{keyword}' in subject")
        
        # Check sender patterns
        for pattern in SENDER_PATTERNS:
            if pattern in from_addr:
                importance_score += 1
                reasons.append(f"Sender: '{pattern}'")
        
        return {
            'id': email_id,
            'subject': headers.get('Subject', 'No Subject'),
            'from': headers.get('From', 'Unknown'),
            'date': headers.get('Date', 'Unknown'),
            'importance_score': importance_score,
            'is_important': importance_score >= 3,
            'reasons': reasons
        }
    except Exception as e:
        return None

def main():
    print("🔍 Checking for new important emails...")
    print()
    
    # Check last 1 hour for heartbeat
    messages, error = check_new_emails('matt@spex4less.com', hours=1)
    
    if error:
        print(f"❌ Error: {error}")
        return
    
    if not messages:
        print("📭 No new emails in the last hour")
        return
    
    print(f"📧 Found {len(messages)} new email(s) in the last hour")
    print()
    
    # Load token for analysis
    tokens = load_tokens()
    token = tokens.get('matt@spex4less.com', {}).get('access_token')
    
    important_emails = []
    
    for msg in messages[:10]:  # Check first 10
        analysis = analyze_email_importance(msg['id'], token)
        if analysis and analysis['is_important']:
            important_emails.append(analysis)
    
    if important_emails:
        print("⚠️  IMPORTANT EMAILS DETECTED:")
        print("=" * 60)
        for email in important_emails:
            print(f"\n🔴 Importance Score: {email['importance_score']}/10")
            print(f"   Subject: {email['subject']}")
            print(f"   From: {email['from']}")
            print(f"   Date: {email['date']}")
            print(f"   Why important: {', '.join(email['reasons'])}")
        print("\n" + "=" * 60)
    else:
        print("✅ No important emails detected in the last hour")
        print()
        print("Recent emails (not flagged as important):")
        for msg in messages[:3]:
            analysis = analyze_email_importance(msg['id'], token)
            if analysis:
                print(f"  - {analysis['subject'][:60]}...")
                print(f"    From: {analysis['from'][:40]}")

if __name__ == '__main__':
    main()
