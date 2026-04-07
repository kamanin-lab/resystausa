# Feature Landscape: Website Mirror / Backup

**Domain:** Static website archival — capturing a live WordPress site before access is lost
**Researched:** 2026-04-07
**Confidence:** HIGH for core wget mechanics; MEDIUM for Cloudflare bypass reliability; LOW for JS-rendered content completeness

---

## Table Stakes

Features that make the backup actually usable. Missing any of these = incomplete archive.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Full HTML page download — all crawlable pages | Primary deliverable; without pages, there is no archive | Low | wget `--mirror --recursive` covers this |
| CSS stylesheet download | Pages render as unstyled text without it | Low | Included in `--page-requisites` |
| JavaScript download | JS files needed for page rendering context even if not executed | Low | Included in `--page-requisites` |
| Image download (jpg, png, gif, svg, webp) | Visual content; loses site identity if missing | Low | wget resolves `<img src>` automatically |
| Font download (woff, woff2, ttf, eot) | Often CDN-hosted; breaks typography offline | Low | Fonts embedded in CSS `@font-face` are fetched by `--page-requisites` only if wget follows them |
| PDF download | WordPress sites commonly link PDFs as documents/spec sheets — critical for content recovery | Medium | wget only downloads linked PDFs it encounters via crawl; must verify `/wp-content/uploads/` walk separately |
| Link rewriting for offline browsing | Turns downloaded files from server-relative paths to local relative paths | Low | wget `--convert-links` handles this |
| Correct file extensions on responses | Some WordPress URLs have no extension (e.g., `/about/` → must save as `about/index.html`) | Low | wget `--adjust-extension` handles this |
| Browser User-Agent on all requests | Cloudflare returns 403 to wget/curl default UA; Chrome UA passes | Low | `--user-agent="Mozilla/5.0 ..."` flag |
| Rate limiting / politeness delay | Server bans IP on rapid requests; IONOS shared hosting is especially sensitive | Low | `--wait=1 --random-wait` flags |
| Sitemap retrieval (all variants) | Sitemaps are the most reliable URL inventory for a WordPress site | Low | Fetch sitemap.xml, sitemap_index.xml, wp-sitemap.xml directly |
| WordPress uploads directory walk | `/wp-content/uploads/YYYY/MM/` tree holds media not always linked from pages | Medium | Requires direct directory traversal or deduction from sitemap |
| url-list.txt generation | Required downstream for SEO redirect mapping during site migration | Low | Assemble from crawl log + sitemap URLs |
| Structured output folder | Reproducible layout so files are findable after the job | Low | Mirror to `resysta-backup/` with clear subdirectory naming |
| Cloudflare bypass via direct IP + Host header | resystausa.com sits behind Cloudflare; domain requests hit JS challenge pages | Medium | Use `74.208.236.61` with `--header "Host: resystausa.com"` |
| Fallback strategy: Python requests scraper | wget may still get blocked by advanced bot detection; full header emulation is more controllable | Medium | Implement as second-pass for pages that return 403/429 to wget |
| Fallback strategy: Wayback Machine (waybackpack) | If live site is completely inaccessible, historical snapshots preserve content | Medium | `waybackpack resystausa.com --from-date 20250101` |

---

## Nice to Have

Features that improve completeness or usability but are not blockers for a working backup.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| HTTP status code log per URL | Reveals 404s, redirects, and blocked resources in the crawl | Low | wget `--server-response` or parse wget log |
| Deduplication of url-list.txt | Prevents duplicate redirect rules downstream; cleaner SEO mapping | Low | `sort -u` post-process on the URL list |
| Crawl resume support | If job is interrupted, resume without re-downloading existing files | Low | wget `--continue` handles partial files; `--mirror` skips already-fetched files by default |
| Timestamp preservation | Keeps original file modification dates for audit trail | Low | wget `--timestamping` |
| Manifest of downloaded files | Inventory of everything captured; useful for gap analysis | Low | Post-process: find all files in backup dir, emit as manifest.txt |
| Separate archive per access method | One folder per method (IP-bypass, domain+UA, wayback) makes comparison easy | Low | Name subdirs `wget-ip/`, `wget-domain/`, `wayback/` |
| Robots.txt check (then ignore) | Knowing what robots.txt says is useful; ignoring it is legitimate for archival | Low | wget `--execute robots=off` |
| Identify JS-rendered content gaps | Some pages may be SPA or AJAX-heavy; flag them as potentially incomplete | High | Out-of-scope for this toolset; note in output README |
| WARC format output | Industry-standard archival format; usable in archive viewers | High | wget `--warc-file` flag supports this; adds complexity, not needed for SEO recovery use case |

---

## Anti-Features

Things NOT to build. Each wastes time or creates problems without adding value for this specific use case.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| WordPress admin/dashboard access | Requires credentials we do not have; no path forward | Scope out entirely |
| Database export (wp-config, MySQL) | No server shell access; not achievable via HTTP crawl | Scope out entirely |
| Theme/plugin source file reconstruction | `/wp-content/themes/` and `/wp-content/plugins/` are typically blocked from directory listing | Note the gap; do not burn time attempting |
| Screenshot capture of every page | Adds heavy tooling (headless Chrome) for marginal value; this is a content backup, not visual QA | Scope out; Wayback Machine has screenshots if needed |
| CAPTCHA/JS challenge solving | Cloudflare's JS challenges require a real browser runtime; adding Playwright/Selenium creates a large dependency chain | Use IP bypass method instead — it sidesteps the challenge entirely |
| Crawler politeness negotiation (robots.txt obedience) | This is a legitimate archival of a site the client owns; robots.txt is irrelevant | Pass `robots=off`; move on |
| Incremental / scheduled re-crawl | One-time archival task; scheduling is operational overhead with no benefit | Run once, done |
| Deep external link following | Following links off-domain bloats the archive with unrelated sites | `--no-parent --domains=resystausa.com` strictly |
| Content deduplication across Wayback snapshots | Wayback Machine has many historical snapshots; comparing them is research, not archival | Use `--from-date` to pin to a recent, clean snapshot |
| Search index over archived content | Full-text search (e.g., ArchiveBox) is useful for ongoing archives, not a one-time rescue job | Scope out entirely |

---

## Feature Dependencies

```
Sitemap retrieval
    → url-list.txt (seed URLs feed the list)
    → wget crawl (sitemap URLs fed via --input-file to seed crawl)

Direct IP bypass (working)
    → wget mirror (primary path)
    → url-list.txt (from wget crawl log)

Direct IP bypass (blocked)
    → Python scraper fallback
        → url-list.txt (from scraper output)

Python scraper (blocked)
    → waybackpack fallback
        → url-list.txt (from Wayback CDX API)

WordPress uploads walk
    → PDF/image completeness (supplements linked assets)
    → url-list.txt (adds media URLs not found by page crawl alone)
```

---

## MVP for This Project

Given the goal (rescue archive before access is lost), build in this order:

1. **Server reachability check** — verify direct IP and domain+UA both respond before committing to a full crawl
2. **Sitemap download** — fastest way to get the complete URL inventory; drives everything else
3. **wget IP-bypass mirror** — primary content capture; covers ~90% of pages and assets in one command
4. **WordPress uploads walk** — catches PDFs and media not reachable via page crawl
5. **url-list.txt assembly** — merge sitemap URLs + crawl-discovered URLs, deduplicate, sort
6. **Python scraper fallback** — run only if wget produces significant 403 gaps
7. **Wayback Machine fallback** — run only if live site is completely inaccessible

Defer: WARC format, screenshot capture, search indexing, incremental re-crawl.

---

## Sources

- [wget offline mirroring options — DEV Community](https://dev.to/rijultp/how-to-use-wget-to-mirror-websites-for-offline-browsing-48l4)
- [Advanced wget website mirroring — IT Handyman](https://handyman.dulare.com/advanced-wget-website-mirroring/)
- [wget mirror gist — GitHub](https://gist.github.com/crittermike/fe02c59fed1aeebd0a9697cf7e9f5c0c)
- [HTTrack vs Wget comparison — WebAsha Technologies](https://www.webasha.com/blog/httrack-vs-wget-a-comprehensive-comparison-of-the-best-website-mirroring-tools-for-osint-and-cybersecurity)
- [Best tools to archive webpages 2025 — oscoo](https://www.oscooshop.com/blogs/blogs/tools-to-archive-webpages-and-websites)
- [How to bypass Cloudflare 2026 — ScrapeOps](https://scrapeops.io/web-scraping-playbook/how-to-bypass-cloudflare/)
- [Wayback Machine URL extraction for SEO — Exposure Ninja](https://exposureninja.com/blog/extract-urls-archive-org/)
- [waybackpack on PyPI](https://pypi.org/project/waybackpack/)
- [Scraping Wayback Machine historical data — The Web Scraping Club](https://substack.thewebscraping.club/p/scraping-wayback-machine)
- [Website archival guide — Kinsta](https://kinsta.com/blog/archive-a-website/)
