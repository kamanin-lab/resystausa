# Requirements: resystausa.com Website Backup

**Defined:** 2026-04-07
**Core Value:** Preserve every accessible page and asset from resystausa.com before access is permanently lost.

## v1 Requirements

### Probe

- [ ] **PRB-01**: Script checks server availability via direct HTTP to 74.208.236.61 with Host header and Chrome UA
- [ ] **PRB-02**: Script checks server availability via HTTPS to resystausa.com domain with Chrome UA
- [ ] **PRB-03**: Script validates response is real content (not a Cloudflare challenge page) by checking for `wp-content` in body
- [ ] **PRB-04**: Script enables Windows LongPathsEnabled registry key before any wget runs

### Sitemap

- [ ] **SMP-01**: Script downloads sitemap.xml, sitemap_index.xml, and wp-sitemap.xml (tries all three)
- [ ] **SMP-02**: Script parses sitemap to extract all page URLs into seed url-list
- [ ] **SMP-03**: Script saves sitemap files to resysta-backup/ root

### Mirror

- [ ] **MIR-01**: Script runs wget mirror via direct IP (HTTP port 80, Host header, Chrome UA, --restrict-file-names=windows)
- [ ] **MIR-02**: Script runs wget mirror via domain HTTPS (Chrome UA, --restrict-file-names=windows) in parallel with MIR-01
- [ ] **MIR-03**: Post-mirror validation scans downloaded HTML for Cloudflare challenge markers (cf-browser-verification, Just a moment, _cf_chl_opt)
- [ ] **MIR-04**: wget flags include --convert-links --adjust-extension --page-requisites --no-parent --wait=1 --random-wait --reject-regex ".*\?.*"

### Uploads

- [ ] **UPL-01**: Script performs dedicated wget pass on /wp-content/uploads/ for years 2022-2025 to capture orphaned media
- [ ] **UPL-02**: Downloaded media saved under resysta-backup/site/ directory tree

### Fallback

- [ ] **FAL-01**: If wget mirror produces challenge pages or fails, Python requests scraper runs against direct IP with full browser header set (Host, User-Agent, Accept, Accept-Language, Referer, Sec-Fetch-* headers)
- [ ] **FAL-02**: Python scraper uses requests.Session() to persist WordPress cookies across requests
- [ ] **FAL-03**: Python scraper implements 1-2s random delay between requests
- [ ] **FAL-04**: If live site is fully inaccessible, waybackpack runs against resystausa.com from 2025-01-01 (with CDX API pre-check for coverage)
- [ ] **FAL-05**: Wayback output saves to resysta-backup/wayback/ (not mixed with live mirror)

### URL Consolidation

- [ ] **URL-01**: url-list.txt assembled from sitemap URLs + wget crawl log URLs, deduplicated and sorted
- [ ] **URL-02**: Wayback wrapper URLs (archive.org/web/...) stripped — only original resystausa.com URLs in url-list.txt
- [ ] **URL-03**: url-list.txt saved to resysta-backup/url-list.txt

### Output Structure

- [ ] **OUT-01**: Final output follows structure: resysta-backup/site/, resysta-backup/wayback/, resysta-backup/sitemap.xml, resysta-backup/url-list.txt
- [ ] **OUT-02**: All output saved to G:\01_OPUS\Projects\resystausa\resysta-backup\

## v2 Requirements

### Enhanced Coverage

- **ENH-01**: Playwright-based scraper for JS-rendered pages if requests-based scraper misses dynamic content
- **ENH-02**: CDX API enumeration for Wayback to get full URL list before download (not just domain root)
- **ENH-03**: Automated WARC format archive for long-term preservation

## Out of Scope

| Feature | Reason |
|---------|--------|
| WordPress admin access | No credentials — rescue is read-only |
| Database export | No server access |
| Theme/plugin source files | Focus is rendered HTML and public assets |
| Cloudflare JS challenge solving via Playwright | Direct IP bypass makes this unnecessary |
| HTTPS to bare IP (74.208.236.61) | TLS cert mismatch — use HTTP port 80 only |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| PRB-01 | Phase 1 | Pending |
| PRB-02 | Phase 1 | Pending |
| PRB-03 | Phase 1 | Pending |
| PRB-04 | Phase 1 | Pending |
| SMP-01 | Phase 1 | Pending |
| SMP-02 | Phase 1 | Pending |
| SMP-03 | Phase 1 | Pending |
| MIR-01 | Phase 2 | Pending |
| MIR-02 | Phase 2 | Pending |
| MIR-03 | Phase 2 | Pending |
| MIR-04 | Phase 2 | Pending |
| UPL-01 | Phase 2 | Pending |
| UPL-02 | Phase 2 | Pending |
| FAL-01 | Phase 3 | Pending |
| FAL-02 | Phase 3 | Pending |
| FAL-03 | Phase 3 | Pending |
| FAL-04 | Phase 3 | Pending |
| FAL-05 | Phase 3 | Pending |
| URL-01 | Phase 4 | Pending |
| URL-02 | Phase 4 | Pending |
| URL-03 | Phase 4 | Pending |
| OUT-01 | Phase 4 | Pending |
| OUT-02 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 23 total
- Mapped to phases: 23
- Unmapped: 0 ✓

---
*Requirements defined: 2026-04-07*
*Last updated: 2026-04-07 after initial definition*
