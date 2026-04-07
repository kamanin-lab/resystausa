# Technology Stack: resystausa.com Archival

**Project:** resystausa.com website mirror/backup
**Researched:** 2026-04-07
**Overall confidence:** HIGH (tools are well-documented, battle-tested, and Windows-compatible)

---

## Recommended Stack

### Tier 1 — Primary: wget (GNU Wget 1.25.x)

| Property | Value |
|----------|-------|
| Tool | GNU Wget |
| Version | 1.25.x (latest as of 2026) |
| Purpose | Full recursive site mirror — HTML, CSS, JS, images, fonts, PDFs |
| Windows | Available via Git Bash (MSYS2/MINGW), Chocolatey, or standalone .exe |
| Why | Battle-tested, single binary, no Python deps, handles `--mirror` semantics natively, accepts arbitrary `--header` for Host override and User-Agent spoofing |

**Why wget over everything else for Tier 1:**
wget's `--mirror` mode is the gold standard for static-site archival. It handles infinite recursion depth, timestamps, no-clobber, and redirect following out of the box. The `--header` flag accepts arbitrary HTTP headers, which is exactly what's needed to pass both `Host: resystausa.com` for Cloudflare bypass and a real browser User-Agent. No other single binary does this without significant setup overhead.

**Canonical command for this project (direct-IP Cloudflare bypass):**

```bash
wget \
  --mirror \
  --page-requisites \
  --convert-links \
  --adjust-extension \
  --no-parent \
  --trust-server-names \
  --restrict-file-names=windows \
  --no-check-certificate \
  --wait=2 \
  --random-wait \
  --header="Host: resystausa.com" \
  --header="User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36" \
  --header="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8" \
  --header="Accept-Language: en-US,en;q=0.5" \
  --exclude-directories="feed,*/feed/,wp-json,search,wp-login.php" \
  --reject-regex="\?(s|replytocom)=" \
  --reject=php,xml \
  -e robots=off \
  -P resysta-backup/ \
  https://74.208.236.61/
```

**Flag rationale:**

| Flag | Rationale |
|------|-----------|
| `--mirror` | Enables `-r -N -l inf --no-remove-listing` — ideal for archival |
| `--page-requisites` | Fetches all assets referenced by downloaded HTML (CSS, JS, images) |
| `--convert-links` | Rewrites absolute URLs to relative so archive works offline |
| `--adjust-extension` | Appends `.html` where missing, correct MIME handling |
| `--no-parent` | Stays within scope, won't crawl parent directories |
| `--trust-server-names` | Uses final redirect URL for filename, avoids mangled paths |
| `--restrict-file-names=windows` | Sanitizes colons/special chars for Windows filesystem |
| `--no-check-certificate` | Required when hitting 74.208.236.61 directly — cert is issued for resystausa.com, not bare IP |
| `--wait=2 --random-wait` | 1-2s randomized delay between requests — avoids rate limiting |
| `--header="Host: resystausa.com"` | **The Cloudflare bypass** — tells origin server which vhost to serve without going through Cloudflare |
| `--header="User-Agent: ..."` | Chrome 124 UA — required, default wget UA gets 403 from Cloudflare |
| `--header="Accept: ..."` | Completes browser fingerprint — reduces detection probability |
| `-e robots=off` | Archive task — do not honor robots.txt exclusions |
| `-P resysta-backup/` | Output directory |
| `--exclude-directories=...` | Skip RSS feeds, REST API, login — non-archivable dynamic endpoints |
| `--reject=php,xml` | Skip server-side files that return dynamic content |

**Fallback Tier 1b — domain-based wget (if direct IP is refused):**
Replace the IP with the domain and remove `--header="Host: ..."`. Keep the Chrome UA. This hits Cloudflare directly but may work if the site is not under active "Under Attack Mode."

---

### Tier 2 — Fallback: Python requests + BeautifulSoup4

| Property | Value |
|----------|-------|
| Language | Python 3.11+ |
| Libraries | `requests>=2.31`, `beautifulsoup4>=4.12`, `lxml>=5.0` |
| Purpose | Page-by-page scraper when wget is rate-limited or blocked |
| Windows | Native Python — no issues |
| Why | Full control over every header, cookies, session state, retry logic, and delay. Can emulate browser fingerprint more completely than wget. |

**Use this when:** wget returns consistent 403/429 despite correct headers, or Cloudflare returns JS challenge pages that wget cannot process.

**Architecture:**
1. Seed URLs from sitemap.xml (downloaded separately first)
2. `requests.Session` with browser-identical headers (see below)
3. BeautifulSoup parses each page for `<a>`, `<img>`, `<link>`, `<script>` hrefs
4. Asset URLs queued and downloaded with correct relative paths
5. Throttle: `time.sleep(random.uniform(1.5, 3.0))` between requests

**Required headers for requests Session:**
```python
headers = {
    "Host": "resystausa.com",   # For direct-IP requests
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}
```

**Install:**
```bash
pip install requests beautifulsoup4 lxml
```

**Do NOT use cloudscraper** — it is no longer actively maintained (as of 2025-2026), does not keep up with current Cloudflare challenge versions, and is overkill here because this project uses direct IP access to bypass Cloudflare entirely, not challenge solving.

---

### Tier 3 — Last Resort: waybackpack (Wayback Machine)

| Property | Value |
|----------|-------|
| Tool | waybackpack |
| Version | latest via pip |
| Purpose | Download Internet Archive snapshots if live site is fully inaccessible |
| Windows | Pure Python — works everywhere |
| Why | Only reliable source of site content if both live-site methods fail |

**Install:**
```bash
pip install waybackpack
```

**Command for this project:**
```bash
waybackpack https://resystausa.com \
  --from-date 20250101 \
  --to-date 20260407 \
  --delay 3 \
  --no-clobber \
  --uniques-only \
  -d resysta-backup/wayback/
```

**Flag rationale:**

| Flag | Rationale |
|------|-----------|
| `--from-date 20250101` | Capture recent snapshots only — avoids downloading years of stale versions |
| `--to-date 20260407` | Upper bound = today |
| `--delay 3` | Respect archive.org rate limits |
| `--no-clobber` | Resume interrupted downloads safely |
| `--uniques-only` | Skip duplicate snapshots — usually only the first unique version matters |
| `-d resysta-backup/wayback/` | Separate output dir from live-site downloads |

**Limitation:** waybackpack downloads snapshots URL-by-URL. It does not recursively crawl. Feed it the URL list from sitemap.xml plus a recursive CDX API query to enumerate all archived URLs:

```bash
# Query CDX API to find all archived URLs for the domain
curl "http://web.archive.org/cdx/search/cdx?url=resystausa.com/*&output=text&fl=original&collapse=urlkey&filter=statuscode:200" \
  > resysta-backup/wayback-url-list.txt
```

---

### Supporting Tools

| Tool | Purpose | Install |
|------|---------|---------|
| `curl` | Connectivity test, sitemap download, CDX API query | Pre-installed in Git Bash |
| `python -m http.server` | Verify archive renders correctly offline | Built-in Python |
| `lxml` | Faster HTML parsing for BeautifulSoup fallback | `pip install lxml` |

---

## What NOT to Use

| Tool | Reason to Avoid |
|------|-----------------|
| **HTTrack** | GUI-first, limited header customization, poor control over Host header injection for IP bypass. Version 3.49.2 (Nov 2025) still maintained but not suited to this specific bypass pattern. |
| **Scrapy** | Heavy framework with spider abstractions, async pipelines, and project scaffolding — serious overkill for a single-site one-time archive. requests+BS4 is faster to write and reason about. |
| **Playwright / Selenium / FlareSolverr** | Required only for JS-challenge Cloudflare pages. This project bypasses Cloudflare entirely via direct IP — no JS solving needed. Adds significant complexity for zero benefit. |
| **wget default UA** | Gets 403 from Cloudflare. Always override with `--header="User-Agent: ..."`. |
| **cloudscraper** | Not maintained as of 2025-2026. Does not handle current Cloudflare versions. Unnecessary given IP bypass strategy. |
| **wget without `--no-check-certificate`** | TLS certificate is bound to resystausa.com hostname — direct IP requests will fail certificate verification. Always include `--no-check-certificate` for IP-based access. |
| **Python `urllib`** | Default `User-Agent: Python-urllib/3.x` is immediately flagged. requests library is preferred and provides session management. |

---

## Windows 10 Installation Notes

**wget via Git Bash (recommended — already available):**
Git Bash on Windows ships with wget in MINGW/MSYS2 toolchain. Verify:
```bash
wget --version
# Should show: GNU Wget 1.21.x or later
```
If missing:
```bash
# Via Chocolatey
choco install wget

# Or download standalone from: https://eternallybored.org/misc/wget/
```

**Python:**
```bash
python --version   # Verify Python 3.11+ is in PATH
pip install requests beautifulsoup4 lxml waybackpack
```

**Path quoting note:** When using bash on Windows, output paths with spaces must be quoted. `resysta-backup/` (no spaces) avoids this entirely.

---

## Decision Tree for Access Methods

```
1. Try: wget --mirror with direct IP (74.208.236.61) + Host header
   -> Success (200 responses, HTML returned)?  YES => use as primary
                                                NO  => go to 2

2. Try: wget --mirror with domain + Chrome UA (Cloudflare pass-through)
   -> Success?  YES => use as secondary
                NO  => go to 3

3. Try: Python requests scraper with full header set + direct IP
   -> Success?  YES => use as fallback
                NO  => go to 4

4. Use: waybackpack with CDX enumeration
   -> Always has some snapshots unless site was never crawled
```

---

## Sources

- GNU Wget 1.25.0 Manual: https://www.gnu.org/software/wget/manual/wget.html
- Archiving a WordPress site with wget: https://ajfleming.info/2023/06/12/archive-a-wordpress-site-using-wget/
- Wget mirror best practices: https://kevincox.ca/2022/12/21/wget-mirror/
- Waybackpack README: https://github.com/jsvine/waybackpack
- Wayback CDX Server API: https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server
- cloudscraper maintenance status (2026): https://roundproxies.com/blog/cloudscraper/
- Cloudflare bypass via direct IP: https://cornerpirate.com/2023/11/11/bypassing-cloudflare/
- Python requests headers for scraping: https://oxylabs.io/blog/5-key-http-headers-for-web-scraping
- Scrapy vs requests comparison: https://scrapeops.io/python-web-scraping-playbook/python-scrapy-vs-requests-beautiful-soup/
