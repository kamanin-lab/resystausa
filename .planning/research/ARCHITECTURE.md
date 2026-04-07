# Architecture Patterns

**Domain:** Multi-fallback website archival pipeline
**Project:** resystausa.com mirror
**Researched:** 2026-04-07

---

## Recommended Architecture

A sequential pipeline with parallel sub-tasks. Availability probing runs in parallel at the start; the rest of the stages gate on the result. Each stage writes its output to the shared `resysta-backup/` tree and appends discovered URLs to `url-list.txt`. If a stage succeeds, later fallback stages are skipped via early-exit logic.

```
[1] Availability Probe (parallel)
      ├── curl → IP:80  (Host: resystausa.com)
      └── curl → domain (User-Agent: Chrome 124)
             ↓ sets ACCESS_METHOD variable

[2] Sitemap Extraction
      ├── Try /sitemap.xml
      ├── Try /sitemap_index.xml
      └── Try /wp-sitemap.xml
            → resysta-backup/sitemap.xml
            → urls appended to url-list.txt

[3] Primary Mirror: wget via IP bypass
      wget --mirror + --header="Host: resystausa.com" against 74.208.236.61
            → resysta-backup/site/
      EXIT CODE 0 → skip stages 4a and 4b
      EXIT CODE non-0 or incomplete → continue to fallback

[3b] Secondary Mirror: wget via domain + browser UA  (runs in parallel with 3)
      wget --mirror against https://resystausa.com with Chrome UA
            → resysta-backup/site/
      Merge into site/ (--no-clobber prevents duplicate downloads)

[4a] Fallback: Python requests + BeautifulSoup scraper
      Triggered when wget exits non-zero OR zero pages downloaded
      BFS crawl starting from homepage + sitemap URLs
      Saves full HTML, discovers linked assets
            → resysta-backup/site/
            → urls appended to url-list.txt

[4b] Fallback: Wayback Machine (waybackpack)
      Triggered when live site returns only 403/JS-challenge pages
      waybackpack --from-date 20250101 --ignore-errors --delay 2
            → resysta-backup/wayback/

[5] Media Download  (runs after stage 3/4a, uses url-list.txt)
      Filter urls containing /wp-content/uploads/
      wget with --input-file, preserving year/month directory structure
            → resysta-backup/site/wp-content/uploads/

[6] URL List Consolidation
      Deduplicate url-list.txt
      Sort and write final file
            → resysta-backup/url-list.txt
```

---

## Component Boundaries

| Component | Responsibility | Input | Output |
|-----------|---------------|-------|--------|
| Availability Probe | Determine which access method works | IP + domain | `ACCESS_METHOD` env var (`ip`, `domain`, `dead`) |
| Sitemap Extractor | Fetch and parse XML sitemaps; extract all `<loc>` URLs | ACCESS_METHOD, domain | `resysta-backup/sitemap.xml`, lines in url-list.txt |
| wget Mirror (IP) | Full recursive mirror via direct IP with Host header | IP, target dir | `resysta-backup/site/` tree |
| wget Mirror (domain) | Full recursive mirror via domain with browser UA | domain, UA string, target dir | `resysta-backup/site/` tree (merged) |
| Python Scraper | BFS crawl, saves HTML + assets, handles JS-challenge detection | Seed URL list, headers dict | `resysta-backup/site/` tree, url-list.txt entries |
| Wayback Fallback | Download archived snapshots from archive.org | Domain, date range | `resysta-backup/wayback/` |
| Media Downloader | Download all /wp-content/uploads/ assets by year/month | Filtered URL list | `resysta-backup/site/wp-content/uploads/YYYY/MM/` |
| URL Consolidator | Deduplicate and sort all discovered URLs | Partial url-list.txt files | `resysta-backup/url-list.txt` |

---

## Fallback Chain: When to Trigger Each Stage

### Stage 3 (wget IP bypass) — always attempt first
The direct IP method (`--header="Host: resystausa.com"` to `74.208.236.61`) bypasses Cloudflare entirely. This is the highest-fidelity path.

**Trigger next stage when:**
- wget exits with non-zero and the log contains `403 Forbidden` or `ERROR 403`
- Downloaded file count is below a threshold (e.g., fewer than 10 HTML files)
- wget downloads only a Cloudflare challenge page (detectable: file contains `cf-browser-verification` in body)

### Stage 3b (wget domain + browser UA) — runs in parallel with Stage 3
Run both wget strategies concurrently using `&` and `wait`. Merge results. This costs nothing extra in time and catches cases where IP is blocked but domain UA is accepted.

**Superseded by Stage 4a when:**
- Both wget attempts return 0 files or only challenge pages

### Stage 4a (Python scraper) — fallback to wget failure
The Python scraper handles aggressive Cloudflare configurations where wget's TLS fingerprint or static headers trigger a JS challenge, but the server still serves content with highly realistic HTTP headers (full `Accept`, `Accept-Language`, `Accept-Encoding`, `Sec-Fetch-*` headers plus `requests.Session` cookie persistence).

**Trigger next stage when:**
- Scraper consistently receives `<title>Just a moment...</title>` (Cloudflare JS challenge)
- Zero pages downloaded after 3 attempts

### Stage 4b (Wayback Machine) — last resort for live site access failure
waybackpack is not a replacement for a live mirror — it retrieves frozen snapshots and may be incomplete. Use it only when the live site is definitively inaccessible.

**Trigger when:**
- `ACCESS_METHOD=dead` (both availability probes failed)
- OR all live-site strategies returned only challenge pages

**Do not** run waybackpack in parallel with live-site attempts — Wayback snapshots are supplementary, not equivalent.

---

## Data Flow

```
resysta-backup/
├── site/                     ← wget + Python scraper output (live site HTML/assets)
│   └── wp-content/
│       └── uploads/
│           └── YYYY/MM/      ← media files by date
├── wayback/                  ← waybackpack output (archive.org snapshots)
│   └── 20250101000000/
│       └── resystausa.com/
├── sitemap.xml               ← canonical sitemap copy
└── url-list.txt              ← all URLs discovered across all stages (deduplicated)
```

URL list is built incrementally:
- Sitemap extraction appends `<loc>` URLs
- wget mirror appends URLs from server log (`--server-response` flag captures redirects)
- Python scraper appends every URL it visits
- Wayback download appends snapshot URLs (original URLs, not `web.archive.org` URLs)
- Final consolidation step deduplicates and sorts

---

## Patterns to Follow

### Pattern 1: Probe-then-Branch
Always run a lightweight availability check before committing to a full download. Use `curl -s -o /dev/null -w "%{http_code}" --connect-timeout 10` against both targets. Capture the HTTP status. Branch the entire pipeline on this result, not on wget's error output (which is verbose and harder to parse reliably).

```bash
IP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  --connect-timeout 10 \
  -H "Host: resystausa.com" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36" \
  "http://74.208.236.61/")

DOMAIN_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  --connect-timeout 10 \
  -A "Mozilla/5.0 ..." \
  "https://resystausa.com/")
```

### Pattern 2: wget with Full Header Emulation
wget's default headers are immediately identifiable. Always pass the full browser header set:

```bash
wget \
  --mirror \
  --page-requisites \
  --convert-links \
  --adjust-extension \
  --no-parent \
  --wait=1 \
  --random-wait \
  --limit-rate=500k \
  -e robots=off \
  --header="Host: resystausa.com" \
  --header="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
  --header="Accept-Language: en-US,en;q=0.9" \
  --header="Accept-Encoding: gzip, deflate" \
  --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36" \
  --directory-prefix=resysta-backup/site \
  "http://74.208.236.61/"
```

Key flags: `--wait=1 --random-wait` prevents rate limiting (1-2s delay range). `--limit-rate=500k` avoids bandwidth-triggered blocks. `-e robots=off` prevents robots.txt from blocking media subdirectories.

### Pattern 3: Python Scraper with requests.Session
The scraper must maintain a persistent `requests.Session()` to carry cookies across requests (WordPress sets `wordpress_test_cookie`; session persistence signals human-like behavior).

Headers must include all `Sec-Fetch-*` headers that Chrome 124 sends, not just User-Agent. Cloudflare inspects the full header fingerprint.

BFS queue: start from homepage + all sitemap URLs. Track visited URLs in a set. Normalize URLs (strip fragments, lowercase scheme/host) before inserting into the queue.

### Pattern 4: Sitemap-Driven URL Seeding
Parse the sitemap before launching any download. WordPress sitemaps (`wp-sitemap.xml`) are sitemap indexes containing child sitemaps for posts, pages, categories, tags, and authors. Follow all `<sitemap><loc>` entries recursively. Extract all `<url><loc>` entries as the canonical URL seed list.

This seed list should be passed to every subsequent stage. It ensures the Python scraper and wget's `--input-file` option start with a known-good URL set rather than relying purely on link-following from the homepage.

### Pattern 5: Media Download via Filtered URL List
After the main mirror completes, filter `url-list.txt` for `/wp-content/uploads/` URLs and download them separately using `wget --input-file`. This catches media that the mirror may have missed (e.g., media referenced only in JS or CSS, not in HTML anchor tags).

WordPress organizes uploads as `/wp-content/uploads/YYYY/MM/filename.ext`. The wget `--force-directories --no-host-directories` flags preserve this structure in the output tree.

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Running All Fallbacks Unconditionally
Running wget + Python scraper + waybackpack in sequence regardless of success wastes time and may create duplicate/conflicting output trees. Gate each fallback on explicit failure detection.

**Instead:** Check exit codes, file counts, and HTTP status codes before triggering the next stage.

### Anti-Pattern 2: Storing wget Output at Domain Root (no -nH flag)
Without `--no-host-directories` (`-nH`), wget creates `resysta-backup/site/resystausa.com/index.html` when targeting the IP, and `resysta-backup/site/74.208.236.61/index.html` when targeting the IP — resulting in split directory trees.

**Instead:** Always use `-nH` (no host directories) so files land directly under `resysta-backup/site/`.

### Anti-Pattern 3: Mixing Wayback URLs into url-list.txt
Wayback Machine URLs (`web.archive.org/web/20250101.../resystausa.com/page`) are not real site URLs. Including them in url-list.txt corrupts the SEO URL mapping the file is intended to support.

**Instead:** Extract the original URL from the Wayback URL (the portion after the timestamp) when appending to url-list.txt.

### Anti-Pattern 4: Hammering Without Delays
No `--wait` flag on wget, no `time.sleep()` in the scraper. IONOS hosting will rate-limit or temporarily block the requester IP, causing gaps in the archive.

**Instead:** Enforce 1-2s between requests at every layer. Use `--wait=1 --random-wait` for wget; `time.sleep(1 + random.random())` in the Python scraper.

### Anti-Pattern 5: Ignoring Cloudflare Challenge Pages
wget exits 0 even when it downloads a Cloudflare JS challenge page (HTTP 200 for the challenge). The file count looks fine, but the archive is full of `<title>Just a moment...</title>` pages.

**Instead:** After wget completes, scan a sample of HTML files for `cf-browser-verification` or `Just a moment` strings. If found in more than a threshold percentage, treat the stage as failed and escalate to the Python scraper.

---

## Suggested Build and Execution Order

The pipeline maps directly to implementation phases:

1. **Availability probe + sitemap extraction** — These are fast (seconds), have no dependencies, and their outputs (ACCESS_METHOD, url-list.txt seed, sitemap.xml) feed every later stage. Build and validate this first.

2. **wget IP bypass mirror** — The highest-fidelity path. Build and test against a small subdirectory (`/wp-content/uploads/2025/`) before running full-site mirror to verify header configuration works and files are landing in the right tree structure.

3. **wget domain + browser UA mirror** — Near-identical command to the IP bypass mirror but targeting the domain. Can be layered on top of Step 2 with minimal new code.

4. **Python scraper** — Most complex component. Build as a standalone script with its own URL queue management. Input: list of seed URLs. Output: downloaded files + appended url-list.txt. Test against a few known pages before running site-wide.

5. **Wayback fallback** — Simplest to implement (single waybackpack CLI call). Build last since it only runs when the live site is fully inaccessible.

6. **Media downloader** — Depends on url-list.txt being populated. Run after Stage 3/4a. A simple wget `--input-file` call against the filtered URL list.

7. **URL consolidation** — Final step. Sort + deduplicate url-list.txt. One-liner with `sort -u`.

---

## Scalability Considerations

This is a one-time archival run, not an ongoing service. Scalability concerns are therefore about completeness and reliability rather than throughput.

| Concern | Mitigation |
|---------|------------|
| Large media library (hundreds of GB) | Run media download stage separately; add `--quota` to wget to avoid disk fill |
| Rate limiting mid-run | `--wait --random-wait` on wget; sleep in scraper; waybackpack `--delay 2` |
| Partial wget run (interrupted) | `--no-clobber` and wget's built-in timestamping (`-N` via `--mirror`) allow safe resume |
| Wayback API throttling | waybackpack `--delay-retry 30`; run during off-peak hours |
| Cloudflare challenge detection gaps | Post-run HTML scan for challenge page markers as a validation step |

---

## Sources

- GNU Wget Manual — Recursive Retrieval Options: https://www.gnu.org/software/wget/manual/html_node/Recursive-Retrieval-Options.html
- waybackpack README (jsvine/waybackpack): https://github.com/jsvine/waybackpack/blob/master/README.md
- AskApache — Wget Header Tricks: https://www.askapache.com/linux/wget-header-trick/
- Advanced wget Website Mirroring: https://handyman.dulare.com/advanced-wget-website-mirroring/
- Scraping WordPress Step by Step (Nik Rahmel, Medium): https://medium.com/@nik.rahmel/scraping-wordpress-step-by-step-dbb605fc2101
- ZenRows — How to Bypass Cloudflare: https://www.zenrows.com/blog/bypass-cloudflare
- Baeldung — Verify URL Validity from Shell: https://www.baeldung.com/linux/shell-check-url-validity
