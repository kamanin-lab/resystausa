# Research Summary: resystausa.com Archival
**Synthesized:** 2026-04-07
**Sources:** STACK.md, FEATURES.md, ARCHITECTURE.md, PITFALLS.md

---

## Executive Summary

This project is a one-time rescue archive of a WordPress site (resystausa.com) hosted on IONOS and fronted by Cloudflare WAF. The key technical challenge is not crawling itself but reliably bypassing Cloudflare without triggering bot detection. The proven solution is hitting the origin server at its IONOS IP (74.208.236.61) over HTTP with a spoofed Host: resystausa.com header and a full Chrome 124 User-Agent fingerprint. This sidesteps Cloudflare edge entirely: no JS challenge solving, no headless browser, no added complexity.

The pipeline is a sequential waterfall with early-exit gates: availability probe -> sitemap harvest -> wget IP-bypass mirror -> uploads sweep -> URL list consolidation. Python requests and waybackpack exist as clearly-gated fallbacks triggered only on verified failure of the stage above them. The critical invisible failure mode is wget silently saving Cloudflare challenge pages as real content (HTTP 200, body is just a moment) so a post-run grep check is mandatory. On Windows 10, MAX_PATH truncation and illegal filename characters are also silent killers that must be pre-empted before any wget run.

The primary deliverable is a locally-browsable HTML/asset mirror plus a clean url-list.txt of all discovered URLs for downstream SEO redirect mapping. WARC format, database export, headless screenshots, and incremental re-crawl are explicitly out of scope.

---

## 1. Recommended Stack

| Priority | Tool | Version | Why |
|----------|------|---------|-----|
| Primary | GNU wget | 1.25.x | Single binary, --mirror semantics, --header flag for IP bypass, handles all asset types, Windows-compatible via Git Bash |
| Fallback 1 | Python requests + BeautifulSoup4 | requests>=2.31, bs4>=4.12 | Full header control, session/cookie persistence, per-URL retry logic |
| Fallback 2 | waybackpack | latest via pip | Last-resort HTML snapshots when live site is fully inaccessible |
| Supporting | curl | pre-installed | Availability probes and sitemap preflight checks |
| Supporting | Python http.server | built-in | Offline verification that archive renders correctly |

Do NOT use: HTTrack (poor Host header support), Scrapy (overkill), Playwright/Selenium/FlareSolverr (unnecessary given IP bypass strategy), cloudscraper (unmaintained 2025-2026), Python urllib (flagged UA).

Windows 10 pre-flight:
- Enable long paths: reg add "HKLM\SYSTEM\CurrentControlSet\Control\FileSystem" /v LongPathsEnabled /t REG_DWORD /d 1 /f
- Verify wget in Git Bash: wget --version
- Install Python deps: pip install requests beautifulsoup4 lxml waybackpack

---

## 2. Table Stakes Features

Every item below is required for a usable archive. Missing any = incomplete backup.

| Feature | How Covered |
|---------|------------|
| All HTML pages (crawlable) | wget --mirror --recursive |
| CSS, JS, images, fonts | wget --page-requisites |
| PDF documents | wget crawl + explicit /wp-content/uploads/ sweep |
| Offline-browsable links | wget --convert-links |
| Correct file extensions | wget --adjust-extension |
| Chrome User-Agent on every request | --header="User-Agent: Mozilla/5.0 Chrome/124..." |
| Rate-limit politeness delay | --wait=2 --random-wait (wget); time.sleep(1.5-3.0) (Python) |
| Sitemap harvest (all variants) | Fetch sitemap.xml, sitemap_index.xml, wp-sitemap.xml + parse child sitemaps |
| WordPress uploads sweep | Separate wget pass on /wp-content/uploads/ after main mirror |
| Cloudflare bypass | Direct IP 74.208.236.61 + Host: resystausa.com header |
| url-list.txt of all discovered URLs | Assembled from sitemap + crawl log; deduplicated with sort -u |
| Post-run challenge-page detection | grep -rl on _cf_chl_opt and "Just a moment" across all .html files |
| Windows MAX_PATH mitigation | LongPathsEnabled registry key + short output path |
| Windows-safe filenames | --restrict-file-names=windows on every wget command |

Defer / out of scope: WARC format, database export, WordPress theme/plugin source, headless screenshots, search indexing, incremental re-crawl.

---

## 3. Architecture / Pipeline Order

Execute stages in order. Gate each stage on verified failure of the prior one.

**Stage 1: Availability Probe** (~30 seconds)
- curl to http://74.208.236.61/ with Host: resystausa.com + Chrome UA
- curl to https://resystausa.com/ with Chrome UA
- Verify: response body contains "wp-content", NOT "Checking your browser"
- Sets ACCESS_METHOD = ip | domain | dead

**Stage 2: Sitemap Extraction** (~1 minute)
- Fetch: sitemap.xml, sitemap_index.xml, wp-sitemap.xml
- Parse: follow all child sitemaps from index files
- Output: resysta-backup/sitemap.xml, seed lines in url-list.txt

**Stage 3: wget IP-Bypass Mirror** (primary -- may take hours)
- wget --mirror --page-requisites --convert-links --adjust-extension
- --no-parent --trust-server-names --restrict-file-names=windows
- --no-check-certificate --wait=2 --random-wait
- --header="Host: resystausa.com" + Chrome UA header
- --reject-regex covering ?s=, ?replytocom=, /wp-json/, /feed/
- -e robots=off -P resysta-backup/site/ http://74.208.236.61/
- Validate: file count > 10 HTML; grep for challenge page markers
- Skip Stage 4a if validation passes

**Stage 3b: wget Domain Mirror** (runs in parallel with Stage 3)
- Same flags targeting https://resystausa.com/ (no Host override)
- --no-clobber merges into same resysta-backup/site/ tree

**Stage 4a: Python Scraper Fallback** (only if Stage 3 failed)
- Target: http://74.208.236.61/ -- direct IP avoids TLS fingerprint block
- BFS from homepage + sitemap URLs; requests.Session with full Chrome header set
- Skip Stage 4b if any pages successfully downloaded

**Stage 4b: Wayback Machine Fallback** (only if live site is dead)
- waybackpack https://resystausa.com --from-date 20250101 --delay 3 --uniques-only
- CDX API enumeration for complete URL list
- HTML-only capture; document this limitation explicitly

**Stage 5: Uploads Sweep** (after Stage 3 or 4a completes)
- wget -r -np targeting http://74.208.236.61/wp-content/uploads/
- Catches orphaned media not linked from any crawled page

**Stage 6: URL List Consolidation** (final step)
- sort -u url-list.txt > url-list-final.txt
- Verify: Wayback wrapper archive.org URLs not included (extract original URLs only)

Output tree:

    resysta-backup/
    +-- site/                        (live site mirror)
    |   +-- wp-content/uploads/YYYY/MM/
    +-- wayback/                     (archive.org snapshots if needed)
    +-- sitemap.xml                  (canonical copy)
    +-- url-list.txt                 (all discovered URLs, deduplicated)

---

## 4. Top Pitfalls to Avoid

**1. CRITICAL (silent): Cloudflare challenge pages saved as real content**
wget exits 0 and file count looks normal, but pages contain "Just a moment..." boilerplate instead of real HTML.
Fix: use direct IP as primary; run post-crawl grep for _cf_chl_opt and "Just a moment" across all .html files before declaring success.

**2. CRITICAL (silent): Windows MAX_PATH (260 chars) silently drops deep-path files**
WordPress media paths under a deep project directory exceed 260 chars; files are silently skipped with no error or warning.
Fix: enable LongPathsEnabled registry key before any wget run; keep output path as short as possible (e.g., G:/r/).

**3. CRITICAL (wastes hours): Query string infinite crawl bloat**
Without --reject-regex, wget follows ?s=, ?replytocom=, and /wp-json/ indefinitely, producing thousands of junk files.
Fix: include --reject-regex from the initial command, not as an afterthought.

**4. CRITICAL (blocks start): SSL cert hostname mismatch on direct IP HTTPS**
https://74.208.236.61 fails cert validation because the cert is issued for the hostname, not the bare IP.
Fix: use http:// (port 80) for direct IP connections. If HTTPS is forced, add --no-check-certificate and verify response contains wp-content.

**5. MODERATE: TLS fingerprint blocks Python requests despite correct User-Agent**
Cloudflare JA3 analysis identifies the Python ssl module at the handshake layer regardless of what headers are set.
Fix: always point the Python scraper at the direct IP to bypass Cloudflare TLS inspection, or use curl_cffi with impersonate="chrome124".

**6. MODERATE: Media offloaded to external CDN is invisible to wget**
CDN-hosted images live on a different domain; wget domain-scoping prevents following them.
Fix: inspect live HTML source for external CDN URL patterns before running; add CDN domain to --domains if detected.

**7. MINOR (false alarm): --convert-links looks broken during long downloads**
Link rewriting is intentionally deferred to wget final pass; all links appear absolute while the download is running.
Fix: do not abort mid-run; verify only after wget exits cleanly.

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|-----------|-------|
| Stack | HIGH | wget + requests + waybackpack are battle-tested; IP bypass method is well-documented |
| Features | HIGH (core) / MEDIUM (Cloudflare bypass reliability) | wget mechanics are certain; whether 74.208.236.61 is still the live origin requires live validation |
| Architecture | HIGH | Pipeline has a clear dependency chain; fallback gates are logically sound |
| Pitfalls | HIGH | All pitfalls are specific to this stack/OS/host combination with concrete prevention steps |

**Key gap requiring live validation before work begins:** Whether 74.208.236.61 is the current IONOS origin IP must be confirmed in Stage 1. If the IP has changed or direct access is blocked at the firewall level, the entire primary path collapses to the Python scraper / Wayback fallback chain. Run the Stage 1 probe before building anything else.

---

## Sources

- GNU Wget Manual: https://www.gnu.org/software/wget/manual/wget.html
- waybackpack README: https://github.com/jsvine/waybackpack
- Wayback CDX API: https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server
- Cloudflare bypass via direct IP: https://cornerpirate.com/2023/11/11/bypassing-cloudflare/
- ZenRows Bypass Cloudflare: https://www.zenrows.com/blog/bypass-cloudflare
- Kevin Cox Mirroring with Wget: https://kevincox.ca/2022/12/21/wget-mirror/
- A.J. Fleming Archive WordPress with wget: https://ajfleming.info/2023/06/12/archive-a-wordpress-site-using-wget/
- Microsoft Learn MAX_PATH Limitation: https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation
- Daniel Malmer wget --convert-links deferred: https://danielmalmer.medium.com/heres-why-wget-s-convert-links-option-isn-t-converting-your-links-cec832ee934c
- ScrapeOps Bypass Cloudflare 2026: https://scrapeops.io/web-scraping-playbook/how-to-bypass-cloudflare/
