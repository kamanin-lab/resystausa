<!-- GSD:project-start source:PROJECT.md -->
## Project

**resystausa.com Website Backup**

A complete local archival copy of resystausa.com — a WordPress site the client is losing access to. The backup captures all HTML pages, images, CSS, JS, fonts, and PDFs using multiple fallback strategies (direct IP bypass, browser-emulated wget, Python scraper, Wayback Machine) and organizes results for future SEO URL mapping.

**Core Value:** Preserve every accessible page and asset from resystausa.com before access is permanently lost.

### Constraints

- **Rate limiting**: Wait 1-2s between requests — do not hammer the server
- **User-Agent**: Always use browser UA (Chrome 124), never default wget/curl
- **Cloudflare**: JS challenge pages are not processable — use IP bypass or Wayback
- **Platform**: Windows 10, bash shell via Claude Code
<!-- GSD:project-end -->

<!-- GSD:stack-start source:research/STACK.md -->
## Technology Stack

## Recommended Stack
### Tier 1 — Primary: wget (GNU Wget 1.25.x)
| Property | Value |
|----------|-------|
| Tool | GNU Wget |
| Version | 1.25.x (latest as of 2026) |
| Purpose | Full recursive site mirror — HTML, CSS, JS, images, fonts, PDFs |
| Windows | Available via Git Bash (MSYS2/MINGW), Chocolatey, or standalone .exe |
| Why | Battle-tested, single binary, no Python deps, handles `--mirror` semantics natively, accepts arbitrary `--header` for Host override and User-Agent spoofing |
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
### Tier 2 — Fallback: Python requests + BeautifulSoup4
| Property | Value |
|----------|-------|
| Language | Python 3.11+ |
| Libraries | `requests>=2.31`, `beautifulsoup4>=4.12`, `lxml>=5.0` |
| Purpose | Page-by-page scraper when wget is rate-limited or blocked |
| Windows | Native Python — no issues |
| Why | Full control over every header, cookies, session state, retry logic, and delay. Can emulate browser fingerprint more completely than wget. |
### Tier 3 — Last Resort: waybackpack (Wayback Machine)
| Property | Value |
|----------|-------|
| Tool | waybackpack |
| Version | latest via pip |
| Purpose | Download Internet Archive snapshots if live site is fully inaccessible |
| Windows | Pure Python — works everywhere |
| Why | Only reliable source of site content if both live-site methods fail |
| Flag | Rationale |
|------|-----------|
| `--from-date 20250101` | Capture recent snapshots only — avoids downloading years of stale versions |
| `--to-date 20260407` | Upper bound = today |
| `--delay 3` | Respect archive.org rate limits |
| `--no-clobber` | Resume interrupted downloads safely |
| `--uniques-only` | Skip duplicate snapshots — usually only the first unique version matters |
| `-d resysta-backup/wayback/` | Separate output dir from live-site downloads |
# Query CDX API to find all archived URLs for the domain
### Supporting Tools
| Tool | Purpose | Install |
|------|---------|---------|
| `curl` | Connectivity test, sitemap download, CDX API query | Pre-installed in Git Bash |
| `python -m http.server` | Verify archive renders correctly offline | Built-in Python |
| `lxml` | Faster HTML parsing for BeautifulSoup fallback | `pip install lxml` |
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
## Windows 10 Installation Notes
# Should show: GNU Wget 1.21.x or later
# Via Chocolatey
# Or download standalone from: https://eternallybored.org/misc/wget/
## Decision Tree for Access Methods
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
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

Conventions not yet established. Will populate as patterns emerge during development.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, or `.github/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
