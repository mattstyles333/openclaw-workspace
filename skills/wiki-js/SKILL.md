---
name: wiki-js
description: "Manage Wiki.js knowledge base via GraphQL API. Create, read, update pages. Search and list all documentation. Use for: SOPs, process docs, team knowledge base."
metadata:
  { "openclaw": { "emoji": "📚", "requires": { "bins": ["curl", "python3"] } } }
---

# Wiki.js Skill

Interact with your Wiki.js instance at https://wiki.s4l.link

## Config
File: `/root/.openclaw/workspace/.wiki_js_config.json`

## Commands

### List All Pages
```bash
curl -s -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $(jq -r .WIKI_JS_API_KEY /root/.openclaw/workspace/.wiki_js_config.json)" -d '{"query": "{ pages { list(orderBy: TITLE) { id path title description isPublished createdAt updatedAt } } }" }' "$(jq -r .WIKI_JS_URL /root/.openclaw/workspace/.wiki_js_config.json)/graphql" | python3 -m json.tool
```

### Get Page by ID
```bash
ID=13; curl -s -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $(jq -r .WIKI_JS_API_KEY /root/.openclaw/workspace/.wiki_js_config.json)" -d "{\"query\": \"{ pages { single(id: $ID) { id path title content description createdAt updatedAt } } }\"}" "$(jq -r .WIKI_JS_URL /root/.openclaw/workspace/.wiki_js_config.json)/graphql" | python3 -m json.tool
```

### Search Pages
```bash
QUERY="stock"; curl -s -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $(jq -r .WIKI_JS_API_KEY /root/.openclaw/workspace/.wiki_js_config.json)" -d "{\"query\": \"{ pages { search(query: \\\"$QUERY\\\") { id path title } } }\"}" "$(jq -r .WIKI_JS_URL /root/.openclaw/workspace/.wiki_js_config.json)/graphql" | python3 -m json.tool
```

### Create Page
```bash
curl -s -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $(jq -r .WIKI_JS_API_KEY /root/.openclaw/workspace/.wiki_js_config.json)" -d '{"query": "mutation { pages { create(path: \"/new-page\", title: \"New Page\", content: \"# Heading\\n\\nContent here\", editor: \"markdown\", description: \"Brief description\") { responseResult { succeeded message } page { id path title } } } }" }' "$(jq -r .WIKI_JS_URL /root/.openclaw/workspace/.wiki_js_config.json)/graphql" | python3 -m json.tool
```

### Update Page
```bash
ID=13; curl -s -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $(jq -r .WIKI_JS_API_KEY /root/.openclaw/workspace/.wiki_js_config.json)" -d "{\"query\": \"mutation { pages { update(id: $ID, content: \\\"# Updated content\\\") { responseResult { succeeded message } page { id updatedAt } } } }\"}" "$(jq -r .WIKI_JS_URL /root/.openclaw/workspace/.wiki_js_config.json)/graphql" | python3 -m json.tool
```

## Usage Examples

**List all pages:**
```bash
wiki pages list
```

**Get specific page:**
```bash
wiki pages get 13
```

**Search wiki:**
```bash
wiki pages search "inventory"
```

**Create SOP:**
```bash
wiki pages create --path "sops/new-process" --title "New Process" --content-file ./process.md
```

## Notes

- Uses GraphQL API at `/graphql` endpoint
- Requires API token with `read:pages` and `write:pages` scopes
- Content supports Markdown, HTML, or WikiText depending on editor setting
- Path format: "folder/subfolder/page-name" (no leading slash in some versions)
