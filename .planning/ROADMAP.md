# Roadmap: resystausa.com Website Backup

**Project:** resystausa.com Website Backup
**Core Value:** Preserve every accessible page and asset from resystausa.com before access is permanently lost.
**Created:** 2026-04-07
**Granularity:** Coarse (4 phases)

---

## Phases

- [ ] **Phase 1: Availability Probe + Sitemap Extraction** - Confirm server is reachable and harvest all known URLs before downloading anything
- [ ] **Phase 2: wget Mirror + Uploads Sweep** - Download the full site via direct IP bypass and sweep orphaned media from /wp-content/uploads/
- [ ] **Phase 3: Fallback Strategies** - Run Python scraper and/or Wayback Machine if Phase 2 mirror is blocked or produces challenge pages (conditional — skip if Phase 2 passes validation)
- [ ] **Phase 4: URL Consolidation + Output Structure** - Assemble clean url-list.txt, strip Wayback wrapper URLs, and verify final output tree

---

## Phase Details

### Phase 1: Availability Probe + Sitemap Extraction
**Goal**: Confirm the origin server is reachable via at least one access method and harvest all known page URLs into a seed list before any bulk download begins
**Depends on**: Nothing (first phase)
**Requirements**: PRB-01, PRB-02, PRB-03, PRB-04, SMP-01, SMP-02, SMP-03
**Success Criteria** (what must be TRUE):
  1. A curl probe to http://74.208.236.71 with Host: resystausa.com and Chrome UA returns a response body containing `wp-content` (not a Cloudflare challenge page)
  2. ACCESS_METHOD variable is set to `ip`, `domain`, or `dead` — determining which path downstream phases use
  3. At least one of sitemap.xml, sitemap_index.xml, or wp-sitemap.xml is saved to resysta-backup/
  4. url-list.txt seed file exists with at least one resystausa.com URL extracted from the sitemap
  5. Windows LongPathsEnabled registry key is confirmed enabled before any wget invocation
**Plans**: TBD

**Notes**:
- Use HTTP (not HTTPS) when probing the direct IP — HTTPS will fail with a TLS cert hostname mismatch because the cert is issued for the domain, not the bare IP
- PRB-03 must confirm `wp-content` in response body; "Just a moment" or "Checking your browser" indicates Cloudflare challenge — treat as failure

---

### Phase 2: wget Mirror + Uploads Sweep
**Goal**: Download a complete local mirror of the live site using wget's IP-bypass method, then sweep /wp-content/uploads/ for orphaned media not linked from any crawled page
**Depends on**: Phase 1 (ACCESS_METHOD must not be `dead`; LongPathsEnabled must be confirmed)
**Requirements**: MIR-01, MIR-02, MIR-03, MIR-04, UPL-01, UPL-02
**Success Criteria** (what must be TRUE):
  1. resysta-backup/site/ contains more than 10 HTML files after wget completes
  2. A post-mirror grep scan across all .html files finds zero occurrences of `_cf_chl_opt`, `cf-browser-verification`, or `Just a moment` — confirming no Cloudflare challenge pages were saved as real content
  3. resysta-backup/site/wp-content/uploads/ contains image and media files spanning at least two year subdirectories (e.g., 2023/, 2024/)
  4. wget ran with --restrict-file-names=windows, --wait=1, --random-wait, and --reject-regex covering query strings — no illegal filename characters or infinite-crawl bloat
**Plans**: TBD

**Notes**:
- MIR-01 targets http://74.208.236.71 (HTTP, port 80) — do NOT use HTTPS to a bare IP
- MIR-02 runs in parallel against https://resystausa.com/ using --no-clobber to merge into the same site/ tree
- If post-mirror validation (MIR-03) detects challenge pages, treat Phase 2 as FAILED and trigger Phase 3
- Waybackpack captures HTML only (no CSS, JS, or images) — this limitation is irrelevant in Phase 2 but is documented here for Phase 3 context

---

### Phase 3: Fallback Strategies
**Goal**: Recover site content when the wget mirror (Phase 2) is blocked or produces invalid output — using a Python scraper against the direct IP as primary fallback, and Wayback Machine as last resort if the live site is entirely inaccessible
**Depends on**: Phase 2 (only runs if Phase 2 validation FAILS — skip this phase entirely if Phase 2 passes)
**Requirements**: FAL-01, FAL-02, FAL-03, FAL-04, FAL-05
**Success Criteria** (what must be TRUE):
  1. If Python scraper is triggered: resysta-backup/site/ gains HTML files with real page content (body contains site-specific text, not Cloudflare boilerplate) — scraper pointed at http://74.208.236.71 to bypass Cloudflare TLS fingerprinting
  2. If Python scraper is triggered: requests.Session() is used so WordPress session cookies persist across page requests
  3. If Wayback fallback is triggered: a CDX API pre-check confirms at least some coverage exists for resystausa.com from 2025-01-01 before waybackpack is invoked
  4. If Wayback fallback is triggered: downloaded snapshots are saved to resysta-backup/wayback/ (kept separate from live mirror in resysta-backup/site/)
  5. Phase 3 is skipped entirely and marked as not applicable when Phase 2 post-mirror validation passes
**Plans**: TBD

**Notes**:
- waybackpack downloads HTML snapshots only — CSS, JS, images, and fonts are NOT captured by this fallback; document this limitation in the run log
- Python scraper must target the direct IP (http://74.208.236.71), not the domain, to avoid Cloudflare TLS JA3 fingerprint detection
- Per-request delay of 1.5–3.0 seconds random sleep required (FAL-03)

---

### Phase 4: URL Consolidation + Output Structure
**Goal**: Produce a clean, deduplicated url-list.txt of every discovered resystausa.com URL and verify the final output directory tree matches the required structure
**Depends on**: Phase 2 (or Phase 3 if triggered)
**Requirements**: URL-01, URL-02, URL-03, OUT-01, OUT-02
**Success Criteria** (what must be TRUE):
  1. resysta-backup/url-list.txt exists and contains only resystausa.com URLs — no archive.org/web/ wrapper URLs are present
  2. url-list.txt is deduplicated and sorted (sort -u output), assembled from both sitemap seed URLs and wget crawl log URLs
  3. Final output tree at G:\01_OPUS\Projects\resystausa\resysta-backup\ contains: site/ subdirectory, url-list.txt, and sitemap.xml at the root; wayback/ subdirectory present only if Phase 3 ran
**Plans**: TBD

---

## Progress Table

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Availability Probe + Sitemap Extraction | 0/? | Not started | - |
| 2. wget Mirror + Uploads Sweep | 0/? | Not started | - |
| 3. Fallback Strategies | 0/? | Not started | - |
| 4. URL Consolidation + Output Structure | 0/? | Not started | - |

---

## Coverage

**v1 requirements:** 23 total
**Mapped:** 23/23 ✓
**Unmapped:** 0

| Phase | Requirements |
|-------|-------------|
| Phase 1 | PRB-01, PRB-02, PRB-03, PRB-04, SMP-01, SMP-02, SMP-03 |
| Phase 2 | MIR-01, MIR-02, MIR-03, MIR-04, UPL-01, UPL-02 |
| Phase 3 | FAL-01, FAL-02, FAL-03, FAL-04, FAL-05 |
| Phase 4 | URL-01, URL-02, URL-03, OUT-01, OUT-02 |

---

*Roadmap created: 2026-04-07*
