## API Keys & Secrets (1Password)

All secrets are now stored in **1Password** (vault: `claw`). Use `op` CLI to retrieve them securely.

### Service Account Token
Stored at: `/root/.openclaw/.op_service_account_token`

### Available Secrets

| Secret | 1Password Item | Access Command |
|--------|---------------|----------------|
| **OpenAI API** | `OpenAI API` | `op item get "OpenAI API" --vault=claw --field="API Key"` |
| **SigNoz API** | `SigNoz API` | `op item get "SigNoz API" --vault=claw --field="API Key"` |
| **Context7 API** | `Context7 API` | `op item get "Context7 API" --vault=claw --field="API Key"` |
| **ElevenLabs API** | `ElevenLabs API` | `op item get "ElevenLabs API" --vault=claw --field="API Key"` |
| **PostgreSQL** | `PostgreSQL (External)` | `op item get "PostgreSQL (External)" --vault=claw --field="password"` |
| **GitLab Token** | `GitLab (Self-Hosted)` | `op item get "GitLab (Self-Hosted)" --vault=claw --field="Token"` |
| **Wiki.js API** | `Wiki.js API` | `op item get "Wiki.js API" --vault=claw --field="API Key"` |
| **Gmail API** | `Gmail API (matt@spex4less.com)` | `op item get "Gmail API (matt@spex4less.com)" --vault=claw --field="Access Token"` |
| **OpenRouter API** | `OpenRouter API` | `op item get "OpenRouter API" --vault=claw --field="API Key"` |
| **Magento API** | `Magento API` | `op item get "Magento API" --vault=claw --field="API Key"` |
| **AWS Credentials** | `AWS Credentials` | `op item get "AWS Credentials" --vault=claw --field="Secret Access Key"` |

### Usage Examples

```bash
# Export service account token
export OP_SERVICE_ACCOUNT_TOKEN=$(cat /root/.openclaw/.op_service_account_token)

# Get OpenAI API key
export OPENAI_API_KEY=$(op item get "OpenAI API" --vault=claw --field="API Key")

# Get PostgreSQL password
export PGPASSWORD=$(op item get "PostgreSQL (External)" --vault=claw --field="password")

# Run command with injected secrets
op run --env-file=/dev/stdin -- python3 script.py <<EOF
OPENAI_API_KEY=op://claw/OpenAI API/API Key
SIGNOZ_API_KEY=op://claw/SigNoz API/API Key
EOF
```

## Tailscale Network

**This Server:** `claw` (100.99.165.92)
**OpenClaw Web UI:** http://100.99.165.92:18789/
**Access:** All Tailscale devices can now reach OpenClaw dashboard

**Other Devices:**
- `omarchy` — 100.81.76.42 (Linux)
- `portainer` — 100.94.67.6 (Linux)
- `postgres` — 100.121.255.51 (Linux)
- `nothing-a065` — 100.77.85.94 (Android, offline 7d)

---


## Domain Finder CLI

**Location:** `/root/domain-finder/`  
**Source:** `gitlab.s4l.link/matt/domain-finder`  
**Use:** AI-powered domain name search with availability checking  
**Run:** `domain-finder <keyword> [--rounds N] [--desc "description"]`  
**Alias:** `domain-finder` (added to ~/.bashrc)

**Example:**
```bash
domain-finder spex4less --rounds 3 --desc "online glasses retailer"
```

**Installed:** 2026-02-22

---

## Spex4Less Product Pipeline

**Location:** `/root/supplier_scraper/` & `/root/product_upload/`  
**Source:** `gitlab.s4l.link/internal/supplier_scraper` & `gitlab.s4l.link/internal/product_upload`  
**Use:** Scrape eyewear suppliers → upload to Magento 2  
**Agent:** `spex-pipeline` (specialized agent available)

**Workflow:**
```bash
# 1. Scrape supplier data
scrape --supplier marcolin --output ./data/

# 2. Prepare & upload to M2
m2upload supplier marcolin
m2upload reconcile compare marcolin
m2upload m2 upload marcolin
```

**Supported Suppliers:** Inspecs, Kering, Marcolin, Maui Jim  
**Aliases:** `scrape`, `m2upload` (added to ~/.bashrc)

**Installed:** 2026-02-22

---

## Wiki.js Knowledge Base

**URL:** https://wiki.s4l.link  
**API Key:** Configured in `.wiki_js_config.json`  
**CLI:** `wiki` (custom Python tool)  
**Use:** Manage Spex4Less documentation, SOPs, process docs

**Commands:**
```bash
wiki pages list                    # List all pages
wiki pages get <id>                # Get page content
wiki pages search <query>          # Search wiki
```

**Examples:**
```bash
wiki pages list                    # 35 pages currently
wiki pages search "stock"          # Find inventory docs
wiki pages get 26                  # Read C.R.I.S.P.Y doc
```

**Location:** `/root/.openclaw/workspace/skills/wiki-js/`  
**Installed:** 2026-02-22

---

Add whatever helps you do your job. This is your cheat sheet.