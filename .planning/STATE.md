# Project State: resystausa.com Website Backup

**Last updated:** 2026-04-07
**Last activity:** 2026-04-07 - Completed quick task 260407-gjb: Install wget and run resystausa.com backup

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
