## API Keys & Secrets

**OpenAI API Key**: Configured as environment variable `OPENAI_API_KEY`
- Provided: 2026-02-20
- Store in: Environment variable (not in files for security)
- To set permanently, add to your shell profile (~/.bashrc, ~/.zshrc, etc.)

**SigNoz API Key**: `FS3pXDYQsAbBUAvJeOMxiPbXcVJSRafe8rpKjb12cx8=`
- URL: https://logs.s4l.link
- Provided: 2026-02-20
- Store in: Environment variable `SIGNOZ_API_KEY` (add to shell profile)

**Context7 API Key**: `ctx7sk-86bac2d2-6c75-4b71-804d-42e149515427`
- Provided: 2026-02-22 (Matt)
- Usage: Context7 docs fetching (direct API or MCP auth)

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


## PostgreSQL Database (External)

**Host:** 81.150.36.20  
**Port:** 5432  
**Database:** mydatabase  
**User:** readonly  
**Password:** `rD9mK2pL7vX4nQ8wE5cJ3hA6bF1gY9zT`  

*Provided: 2026-02-22*

---

## ElevenLabs API Key

**Key:** `sk_8f67aa6f7a037d91fef135299aaf90957258d4f27b865695`  
**Provider:** ElevenLabs (TTS + Scribe STT)  
**Use:** Voice synthesis & speech-to-text  
**Store:** Environment variable `ELEVENLABS_API_KEY` (add to shell profile)

*Provided: 2026-02-22*

---

## GitLab Token (Self-Hosted)

**Host:** gitlab.s4l.link  
**Token:** `glpat-g1Bi2NWiNqbrWYALuvu-7W86MQp1OjIH.01.0w1jvn6ay`  
**CLI:** `glab`  
**Use:** GitLab API operations, repo management, CI/CD  
**Store:** Environment variable `GITLAB_TOKEN` or `glab auth login`

*Provided: 2026-02-22*

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