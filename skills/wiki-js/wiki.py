#!/usr/bin/env python3
"""
Wiki.js CLI - Simple wrapper for Wiki.js GraphQL API
"""

import json
import sys
import subprocess
import os

CONFIG_FILE = "/root/.openclaw/workspace/.wiki_js_config.json"

def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def graphql_query(query):
    config = load_config()
    token = config['WIKI_JS_API_KEY']
    url = config['WIKI_JS_URL'] + '/graphql'
    
    cmd = [
        'curl', '-s', '-X', 'POST',
        '-H', 'Content-Type: application/json',
        '-H', f'Authorization: Bearer {token}',
        '-d', json.dumps({"query": query}),
        url
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)

def list_pages():
    query = '''{ pages { list(orderBy: TITLE) { id path title description isPublished updatedAt } } }'''
    result = graphql_query(query)
    pages = result['data']['pages']['list']
    
    print(f"{'ID':<6} {'Path':<35} {'Title':<40} {'Published':<10}")
    print("-" * 95)
    for page in pages:
        pub = "✓" if page['isPublished'] else "✗"
        path = page['path'][:33] + ".." if len(page['path']) > 35 else page['path']
        title = page['title'][:38] + ".." if len(page['title']) > 40 else page['title']
        print(f"{page['id']:<6} {path:<35} {title:<40} {pub:<10}")
    print(f"\nTotal: {len(pages)} pages")

def get_page(page_id):
    query = f'''{{ pages {{ single(id: {page_id}) {{ id path title content description createdAt updatedAt }} }} }}'''
    result = graphql_query(query)
    page = result['data']['pages']['single']
    
    print(f"\n=== {page['title']} ===")
    print(f"ID: {page['id']}")
    print(f"Path: {page['path']}")
    print(f"Created: {page['createdAt']}")
    print(f"Updated: {page['updatedAt']}")
    if page['description']:
        print(f"Description: {page['description']}")
    print(f"\n--- Content ---\n")
    print(page['content'])

def search_pages(query_term):
    query = f'''{{ pages {{ search(query: "{query_term}") {{ results {{ id path title }} }} }} }}'''
    result = graphql_query(query)
    
    if 'errors' in result:
        # Try alternative search query structure
        query = f'''{{ pages {{ list {{ id path title description }} }} }}'''
        result = graphql_query(query)
        pages = [p for p in result['data']['pages']['list'] if query_term.lower() in p['title'].lower() or query_term.lower() in p['path'].lower() or (p['description'] and query_term.lower() in p['description'].lower())]
    else:
        pages = result['data']['pages']['search'].get('results', [])
    
    if not pages:
        print(f"No results for '{query_term}'")
        return
    
    print(f"\nFound {len(pages)} results for '{query_term}':")
    print(f"{'ID':<6} {'Path':<35} {'Title'}")
    print("-" * 70)
    for page in pages:
        print(f"{page['id']:<6} {page['path']:<35} {page['title']}")

def main():
    if len(sys.argv) < 2:
        print("Usage: wiki <command> [args]")
        print("\nCommands:")
        print("  pages list              List all pages")
        print("  pages get <id>          Get page content")
        print("  pages search <query>    Search pages")
        print("  pages create            Create new page (interactive)")
        sys.exit(1)
    
    cmd = sys.argv[1:]
    
    if cmd == ['pages', 'list']:
        list_pages()
    elif len(cmd) >= 3 and cmd[0] == 'pages' and cmd[1] == 'get':
        get_page(int(cmd[2]))
    elif len(cmd) >= 3 and cmd[0] == 'pages' and cmd[1] == 'search':
        search_pages(cmd[2])
    else:
        print(f"Unknown command: {' '.join(cmd)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
