# resystausa.com Website Backup

## What This Is

A complete local archival copy of resystausa.com — a WordPress site the client is losing access to. The backup captures all HTML pages, images, CSS, JS, fonts, and PDFs using multiple fallback strategies (direct IP bypass, browser-emulated wget, Python scraper, Wayback Machine) and organizes results for future SEO URL mapping.

## Core Value

Preserve every accessible page and asset from resystausa.com before access is permanently lost.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Check server availability via direct IP (74.208.236.61) and via domain with browser User-Agent
- [ ] Download sitemap (sitemap.xml, sitemap_index.xml, wp-sitemap.xml)
- [ ] Mirror full site via wget (direct IP method and domain+UA method in parallel)
- [ ] Download WordPress media uploads (/wp-content/uploads/ by year/month)
- [ ] Fall back to Python requests/BeautifulSoup scraper if wget is blocked
- [ ] Fall back to Wayback Machine (waybackpack, from 2025-01-01) if live site inaccessible
- [ ] Generate url-list.txt with all discovered URLs for SEO mapping
- [ ] Save all output to structured resysta-backup/ folder

### Out of Scope

- WordPress admin/dashboard access — not possible without credentials
- Database export — no server access
- Theme/plugin source files — focus is on rendered HTML and assets

## Context

- Site: resystausa.com (WordPress)
- Hosting: IONOS, real server IP: 74.208.236.61
- CDN/WAF: Cloudflare — blocks default wget/curl user-agents with 403
- Access method: Direct IP with `Host: resystausa.com` header bypasses Cloudflare
- Fallback: domain with browser User-Agent if IP method fails
- Last resort: Python scraper with full header emulation, then Wayback Machine
- Output path: G:\01_OPUS\Projects\resystausa\resysta-backup\
- Required delays: 1-2s between requests to avoid rate limiting

## Constraints

- **Rate limiting**: Wait 1-2s between requests — do not hammer the server
- **User-Agent**: Always use browser UA (Chrome 124), never default wget/curl
- **Cloudflare**: JS challenge pages are not processable — use IP bypass or Wayback
- **Platform**: Windows 10, bash shell via Claude Code

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Test both access methods in parallel | Saves time, reveals fastest working path | — Pending |
| Wayback Machine as final fallback | Ensures some copy even if live site blocks all access | — Pending |
| Python scraper as wget fallback | Full header emulation handles aggressive Cloudflare blocks | — Pending |

---
*Last updated: 2026-04-07 after initial project creation*
