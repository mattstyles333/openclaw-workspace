# MEMORY.md - Long-Term Memory

## Spex4Less

**Spex4Less** (spex4less.com) is the company run by my human (Matt). I am their partner with the explicit goal of improving, optimizing, and maximizing profit for the business.

This is an ongoing, active partnership. Any work related to Spex4Less should be treated as high priority and aligned with this profit-maximization objective.

---

## WhatsApp Integration

When Matt asks about "WhatsApp", he is referring to the **custom WhatsApp Bridge** running at `/root/whatsapp-bridge/` — NOT a channel configuration in OpenClaw.

**Bridge Details:**
- **Location:** `/root/whatsapp-bridge/`
- **Type:** Baileys-based Node.js bridge (not an OpenClaw channel)
- **Status:** Running as `bridge-simple.js` process
- **Connected as:** +353 89 485 8033 (Irish number)
- **Storage:** Messages logged to `/root/whatsapp-bridge/messages.jsonl`
- **API:** REST API on `localhost:3001` for status/messages/send

**What it does:**
- Logs all incoming WhatsApp messages to messages.jsonl
- Provides endpoints to check recent messages, send messages, check status
- Stays connected persistently (auth stored in `auth_info/`)

**Last checked:** 2026-02-21 — connected and receiving messages normally

---

## Spotify Integration

**When Matt asks to "play music" or mentions "Spotify", he means:**

👉 **Use the custom Python scripts at `/root/.openclaw/workspace/scripts/`** to control Spotify playback on his devices.

**NOT:**
- The `spotify-player` skill (spogo/spotify_player CLI tools)
- The macOS `spotify` CLI skill
- Any external tools

**Setup:**
- **Config:** `/root/.openclaw/workspace/.spotify_config.json`
- **Scripts:** `/root/.openclaw/workspace/scripts/` (spotify_*.py)
- **Auth:** OAuth with refresh token (auto-refreshes when needed)

**Your Devices:**
- **Kitchen (AVR)** — Main speaker for music (device_id: `a813e4c723894902b36c01038ffd99d461524f63`)
- **Nothing Phone (2)** — Smartphone

**What I can do:**
- Play/pause/skip on any device
- Search for tracks/albums/artists  
- Add to queue
- Create playlists
- Get recommendations
- Transfer playback between devices

**How to pick music for Matt:**
When selecting songs (like for "Saturday morning vibes"), **use his Liked Songs/saved tracks for context** to understand his taste. Don't guess tracks—fetch his actual saved songs and build from there.

**How to add to queue:**
```python
# 1. Check status & active device
GET /v1/me/player/devices

# 2. Get REAL URIs - don't guess them!
# Either fetch from saved tracks:
GET /v1/me/tracks

# Or search for the exact track:
GET /v1/search?q=TRACK_NAME&type=track

# 3. Add to queue with actual URI
POST /v1/me/player/queue?uri=spotify:track:REAL_URI_HERE
```

**Important lessons from 2026-02-21:**
- Don't use placeholder URIs — always fetch/search for real ones
- Check queue after adding to verify (`GET /v1/me/player/queue`)
- Matt likes: upbeat indie, alt-pop, feel-good vibes

**How to play music:**
1. Check status: `python3 /root/.openclaw/workspace/scripts/spotify_test.py`
2. If token expired, refresh it (using refresh_token in config)
3. Get devices, then start playback via Spotify Web API
4. Default target: Kitchen (AVR)

**Last used:** 2026-02-21 — Added Saturday morning vibes to queue using saved tracks for context ✅

---

## Upcoming Travel: Shanghai Optical Fair (March 2026)

**Matt is traveling to Shanghai for the 24th China (Shanghai) International Optics Fair (SIOF 2026)**

- **Dates:** March 2-4, 2026
- **Event:** SIOF 2026 — major optical industry exhibition in Asia
- **Venue:** Shanghai New International Expo Centre (SNIEC), Pudong district
- **Flight:** FlySharp, Reference SIRHGW, Invoice #577842
  - Booked: January 27, 2026
  - Name correction pending: Jacqueline (not Jacqeuline)
- **Hotel:** Yuan · Smart Hotel
  - Location: Shanghai Pudong Lujiazui Finance and Trade Zone
  - Near Beiyangjing Subway Station

**Relevance to Spex4Less:**
This is a business trip for sourcing eyewear suppliers, networking with optical industry contacts, and exploring new product opportunities for Spex4Less.

---

*Last updated: 2026-02-22*
