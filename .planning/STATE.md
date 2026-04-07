# Project State: resystausa.com Website Backup

**Last updated:** 2026-04-07
**Last activity:** 2026-04-07 - Completed quick task 260407-uol: Injected CSS to hide CF7 forms and Flodesk newsletter across 607 static HTML pages

---

## Project Reference

**Core Value:** Preserve every accessible page and asset from resystausa.com before access is permanently lost.

**Target site:** resystausa.com (WordPress, IONOS hosting, Cloudflare WAF)
**Origin IP:** 74.208.236.71 (IONOS) — use HTTP port 80, not HTTPS
**Output path:** G:\01_OPUS\Projects\resystausa\resysta-backup\

---

## Current Position

**Current Phase:** Phase 1 (not started)
**Current Plan:** None
**Status:** Roadmap created — ready to begin Phase 1

**Progress:**
```
[..........] 0% complete
Phase 1: [ ] Phase 2: [ ] Phase 3: [ ] Phase 4: [ ]
```

---

## Phase Status

| Phase | Status | Notes |
|-------|--------|-------|
| 1. Availability Probe + Sitemap Extraction | Not started | Must run first; determines ACCESS_METHOD |
| 2. wget Mirror + Uploads Sweep | Not started | Blocked on Phase 1 |
| 3. Fallback Strategies | Conditional | Only runs if Phase 2 post-mirror validation FAILS |
| 4. URL Consolidation + Output Structure | Not started | Blocked on Phase 2 (or 3) |

---

## Key Technical Decisions

| Decision | Value | Rationale |
|----------|-------|-----------|
| Primary access method | HTTP to 74.208.236.71 with Host header | Bypasses Cloudflare edge entirely |
| HTTPS to bare IP | FORBIDDEN | TLS cert hostname mismatch — use port 80 only |
| Windows prep | LongPathsEnabled must be enabled before any wget run | Silent file drops on paths >260 chars |
| Post-mirror validation | grep for _cf_chl_opt + "Just a moment" | wget exits 0 even when saving challenge pages |
| waybackpack limitation | HTML snapshots only — no CSS/JS/images | Must document if Phase 3 Wayback fallback runs |
| Query string guard | --reject-regex on ?s=, ?replytocom=, /wp-json/ | Prevents infinite crawl bloat |
| Rate limiting | --wait=1 --random-wait (wget); 1.5-3.0s (Python) | Avoids rate limiting and bot detection |

---

## Accumulated Context

### Decisions Made
- Use direct IP HTTP bypass as the primary crawl strategy (not domain HTTPS)
- Python scraper fallback must also target direct IP to avoid TLS JA3 fingerprint detection
- Wayback Machine fallback is last resort (HTML-only limitation acceptable at that point)
- Phase 3 is conditional — skip it entirely if Phase 2 validation passes
- Blog posts are at ROOT URL level (resystausa.com/SLUG/), NOT at /blog/SLUG/
- All blog posts deleted from live site by April 2026 — Wayback Machine is sole source
- admin-ajax.php (WP Bakery AJAX) is blocked at IONOS server level for /wp-admin/ path
- WP REST API public posts endpoint returns 0 (posts are private/deleted)
- Blog enumeration: use Wayback CDX domain scan (url=resystausa.com/*) to find post slugs

### Active TODOs
- [ ] Confirm 74.208.236.71 is the current live IONOS origin IP (validate in Phase 1 probe)
- [ ] Verify wget is available in Git Bash (wget --version)
- [ ] Verify Python deps: pip install requests beautifulsoup4 lxml waybackpack

### Blockers
- None yet — Phase 1 not started

### Quick Tasks Completed

| # | Description | Date | Commit | Status | Directory |
|---|-------------|------|--------|--------|-----------|
| 260407-fou | Make complete local backup of resystausa.com website | 2026-04-07 | 8fffc7c | Verified | [260407-fou-make-complete-local-backup-of-resystausa](./quick/260407-fou-make-complete-local-backup-of-resystausa/) |
| 260407-gjb | Install wget and run resystausa.com backup | 2026-04-07 | — | In Progress | [260407-gjb-install-wget-and-run-resystausa-com-back](./quick/260407-gjb-install-wget-and-run-resystausa-com-back/) |
| 260407-jrr | Install and run SiteOne Crawler for full SEO analysis of resystausa.com | 2026-04-07 | — | Complete | [260407-jrr-install-and-run-siteone-crawler-for-full](./quick/260407-jrr-install-and-run-siteone-crawler-for-full/) |
| 260407-q3u | Спарсить список дистрибьюторов и заменить карту SSF на статические карточки | 2026-04-07 | 11e4bec | Complete | [260407-q3u-resystausa-com-find-a-distributor-super-](./quick/260407-q3u-resystausa-com-find-a-distributor-super-/) |
| 260407-qhd | Comprehensive backup audit — 107 missing files, CF7 forms, blog gaps | 2026-04-07 | e837674 | Complete | [260407-qhd-resystausa-com](./quick/260407-qhd-resystausa-com/) |
| 260407-rhk | Download 107 missing PDF/DWG-ZIP/DOCX from wp-content/uploads | 2026-04-07 | 22da640 | Complete | [260407-rhk-107-missing-pdf-dwg-docx-wp-content-uplo](./quick/260407-rhk-107-missing-pdf-dwg-docx-wp-content-uplo/) |
| 260407-rhm | Спарсить 55 постов блога (с Wayback Machine — с живого сайта удалены) | 2026-04-07 | d7dadf5 | Complete | [260407-rhm-resystausa-com](./quick/260407-rhm-resystausa-com/) |
| 260407-rhm | Scrape all ~55 blog posts from resystausa.com | 2026-04-07 | d7dadf5 | Complete | [260407-rhm-resystausa-com](./quick/260407-rhm-resystausa-com/) |
| 260407-uol | Hide all CF7 contact forms and Flodesk newsletter across 607 static pages | 2026-04-07 | 116406b | Complete | [260407-uol-hide-all-contact-forms-and-newsletter-su](./quick/260407-uol-hide-all-contact-forms-and-newsletter-su/) |

### Known Risks
- If 74.208.236.71 is no longer the current origin IP, the entire primary path fails and Phase 3 becomes mandatory
- Cloudflare may have CDN-offloaded media on a different domain — inspect live HTML source before running wget to check for external CDN URL patterns

---

## Performance Metrics

- Plans completed: 0
- Phases completed: 0/4
- Requirements satisfied: 0/23

---

*State initialized: 2026-04-07*
