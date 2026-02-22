---
name: website-builder
description: "Build, test, and deploy websites via GitHub Pages. Orchestrates: (1) project scoping questions, (2) coding agent for development, (3) QA agent for testing, (4) GitHub Pages deployment. Uses HTML/CSS/JS + Tailwind CSS by default. NOT for: complex SPAs, e-commerce backends, or apps requiring server-side logic."
metadata:
  {
    "openclaw":
      {
        "emoji": "🌐",
        "requires": { "bins": ["gh", "git"] },
        "skills": ["coding-agent", "qa-tester", "github"]
      },
  }
---

# Website Builder

A complete website development pipeline: scope → build → test → deploy.

## Workflow

```
1. SCOPE  → Ask questions, define requirements
2. BUILD  → Spawn coding-agent to create site
3. TEST   → Run qa-tester for validation  
4. DEPLOY → GitHub commit + Pages deploy
```

## Phase 1: Scoping Questions

Ask the user:

| Question | Why |
|----------|-----|
| **Purpose?** | Landing page, portfolio, docs, blog, etc. |
| **Content?** | What sections/pages needed? |
| **Design vibe?** | Minimal, bold, professional, playful? |
| **Colors?** | Brand colors or pick a palette? |
| **Assets?** | Logo, images, copy provided? |
| **Domain?** | GitHub Pages URL or custom? |
| **Timeline?** | Quick MVP vs polished? |

## Phase 2: Build (Coding Agent)

Spawn `coding-agent` with:

```
Tech stack: HTML5 + Tailwind CSS (CDN) + vanilla JS
No frameworks unless specifically requested
Responsive by default (mobile-first)
Clean semantic HTML, accessible (ARIA where needed)
```

**Output structure:**
```
site/
├── index.html
├── css/ (if custom styles beyond Tailwind)
├── js/ (if needed)
├── assets/ (images, fonts)
└── README.md (deployment notes)
```

## Phase 3: QA (QA Tester)

Run `qa-tester` skill:
- Desktop & mobile viewport testing
- Click-through validation
- CRO best practices check
- Performance sanity check

## Phase 4: Deploy (GitHub Pages)

```bash
# Create repo (public for Pages)
gh repo create <name> --public --source=site --push

# Enable GitHub Pages (branch: main, folder: root)
gh api repos/<user>/<name>/pages --method POST \
  -f source.branch=main -f source.path=/

# Get Pages URL
gh api repos/<user>/<name>/pages | jq .html_url
```

## Usage

```
User: "Build me a landing page for my photography portfolio"
→ Ask scoping questions
→ Spawn coding-agent with brief
→ Run qa-tester when build complete
→ Deploy to GitHub Pages
→ Return live URL
```

## Example Prompts for Coding Agent

```
"Create a minimal landing page for a freelance photographer. 
Dark theme (#1a1a1a background, white text). 
Sections: hero with name/tagline, 3-image gallery grid, contact form, footer.
Use Tailwind via CDN. Single HTML file. Responsive."
```

```
"Build a docs site for an API. Clean, readable, sidebar navigation.
Light theme with blue accents (#3b82f6). 
Markdown-style content sections. Mobile hamburger menu.
Use Tailwind. Single-page with anchor links."
```

## Notes

- Always use **Tailwind CSS via CDN** for simplicity
- Keep to **single-page sites** unless multi-page explicitly needed
- **Images**: Use placeholders (placehold.co, unsplash source) unless user provides
- **Forms**: Use formspree.io or similar for static hosting
- **Analytics**: Optional Plausible/GoatCounter script if requested

## Post-Deploy

```
✅ Live at: https://<user>.github.io/<repo>
📱 Test on your phone
🔄 Changes: Edit files → git push → auto-deploy (1-2 min)
```
