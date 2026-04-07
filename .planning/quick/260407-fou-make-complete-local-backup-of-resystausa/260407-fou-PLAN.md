---
phase: 260407-fou
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - scraper.py
  - wayback_download.py
  - backup.sh
autonomous: true
requirements:
  - PRB-01
  - PRB-02
  - PRB-03
  - PRB-04
  - SMP-01
  - SMP-02
  - SMP-03
  - MIR-01
  - MIR-02
  - MIR-03
  - MIR-04
  - UPL-01
  - UPL-02
  - FAL-01
  - FAL-02
  - FAL-03
  - FAL-04
  - FAL-05
  - URL-01
  - URL-02
  - URL-03
  - OUT-01
  - OUT-02

must_haves:
  truths:
    - "backup.sh runs end-to-end without manual intervention, producing output in resysta-backup/"
    - "Script probes BOTH IPs (74.208.236.61 and 74.208.236.71) and uses whichever responds"
    - "wget stages are skipped gracefully if wget is not installed, falling through to Python scraper"
    - "scraper.py recursively downloads HTML pages via direct IP with browser headers and 1.5-3s delay"
    - "wayback_download.py performs CDX pre-check before invoking waybackpack"
    - "resysta-backup/url-list.txt contains deduplicated resystausa.com URLs from all sources"
    - "Challenge page detection runs after every download stage and triggers fallback if >20% contaminated"
  artifacts:
    - path: "scraper.py"
      provides: "Python requests+BeautifulSoup recursive site scraper"
      min_lines: 120
    - path: "wayback_download.py"
      provides: "Wayback Machine CDX check + waybackpack download wrapper"
      min_lines: 60
    - path: "backup.sh"
      provides: "Main orchestrator script — full backup pipeline"
      min_lines: 200
  key_links:
    - from: "backup.sh"
      to: "scraper.py"
      via: "python scraper.py invocation when wget absent or challenge pages detected"
      pattern: "python.*scraper\\.py"
    - from: "backup.sh"
      to: "wayback_download.py"
      via: "python wayback_download.py invocation as last resort fallback"
      pattern: "python.*wayback_download\\.py"
    - from: "scraper.py"
      to: "http://DIRECT_IP/"
      via: "requests.Session().get() with Host: resystausa.com header"
      pattern: "session\\.get.*DIRECT_IP"
    - from: "wayback_download.py"
      to: "web.archive.org/cdx"
      via: "CDX API query before waybackpack invocation"
      pattern: "cdx/search/cdx"
---

<objective>
Create the complete resystausa.com backup toolkit: a bash orchestrator (backup.sh) that calls
two Python scripts (scraper.py, wayback_download.py) to download the full site with automatic
fallback from wget -> Python scraper -> Wayback Machine.

Purpose: The client is losing access to this WordPress site behind Cloudflare. This toolkit
preserves every accessible page and asset via direct IP bypass before access is permanently lost.

Output: Three executable scripts in project root + resysta-backup/ output directory with
site/, wayback/, sitemap.xml, and url-list.txt.
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/execute-plan.md
@$HOME/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/quick/260407-fou-make-complete-local-backup-of-resystausa/260407-fou-CONTEXT.md
@.planning/quick/260407-fou-make-complete-local-backup-of-resystausa/260407-fou-RESEARCH.md
@input.txt
</context>

<tasks>

<task type="auto">
  <name>Task 1: Create Python scraper and Wayback download scripts</name>
  <files>scraper.py, wayback_download.py</files>
  <action>
Create two Python scripts in the project root (G:\01_OPUS\Projects\resystausa\).

**scraper.py** — Recursive site scraper using requests + BeautifulSoup. Requirements:

- Target direct IP via HTTP (not domain) to bypass Cloudflare TLS fingerprinting.
- IP selection: accept a `--ip` argument. Default to `74.208.236.71`. backup.sh will pass the correct IP after probing both candidates (74.208.236.71 and 74.208.236.61).
- Use `requests.Session()` for cookie persistence across pages.
- Full browser header set including:
  - `Host: resystausa.com`
  - `User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36`
  - `Accept`, `Accept-Language`, `Accept-Encoding`, `Connection`, `Upgrade-Insecure-Requests`
  - `Sec-Fetch-Dest: document`, `Sec-Fetch-Mode: navigate`, `Sec-Fetch-Site: none`, `Sec-Fetch-User: ?1`
- Skip URL patterns: `?s=`, `?replytocom=`, `/wp-json/`, `/feed/`, `/trackback/`, `?share=`, `?like=`, `?wc-ajax=`, `mailto:`, `tel:`, `#`
- Challenge page detection: check response body for `_cf_chl_opt`, `cf-browser-verification`, `Just a moment` — log and skip if found.
- Normalize URLs: rewrite domain-based URLs to IP-based, ignore external domains, handle relative URLs via urljoin.
- Save HTML files to `resysta-backup/site/` preserving URL path structure (e.g., `/about/` saves to `resysta-backup/site/about/index.html`).
- Also download page requisites (CSS, JS, images, fonts, PDFs) found in HTML: parse `<link href>`, `<script src>`, `<img src>`, `<img srcset>`, `<source>`, `<a href>` pointing to asset files (.css, .js, .png, .jpg, .jpeg, .gif, .svg, .webp, .woff, .woff2, .ttf, .eot, .pdf, .ico).
- Append discovered URLs (converted to domain form `https://resystausa.com/...`) to `resysta-backup/url-list-raw.txt`.
- Throttle: `time.sleep(random.uniform(1.5, 3.0))` between page requests, `time.sleep(random.uniform(0.3, 0.8))` between asset downloads.
- Accept optional `--seed-file` argument to load initial URLs from a file (one URL per line).
- Accept `--max-pages` argument (default 2000).
- Accept `--output-dir` argument (default `resysta-backup/site`).
- Print progress: `[N] Fetching: URL` for each page.
- Exit with code 0 on success, 1 on fatal error. Print summary line: `Scraper complete: N pages visited, M saved.`

**wayback_download.py** — Wayback Machine CDX pre-check + waybackpack wrapper. Requirements:

- Step 1: Query CDX API: `https://web.archive.org/cdx/search/cdx?url=resystausa.com/*&output=text&fl=original&collapse=urlkey&filter=statuscode:200`
- If CDX returns 0 results, print `[SKIP] No Wayback snapshots found for resystausa.com` and exit 0.
- Save full CDX URL list to `resysta-backup/wayback-cdx-urls.txt`.
- Filter out query-string junk (`?s=`, `?replytocom=`, `wc-ajax`, `yith-woocompare`), save clean list to `resysta-backup/wayback-url-list-clean.txt`.
- Append clean URLs to `resysta-backup/url-list-raw.txt`.
- Step 2: Run waybackpack via `subprocess.run()`:
  ```
  waybackpack "https://resystausa.com" \
    --from-date 20250101 --to-date 20260407 \
    --delay 3 --delay-retry 30 \
    --no-clobber --uniques-only --ignore-errors --max-retries 3 \
    -d "resysta-backup/wayback"
  ```
- Print limitation warning: `[NOTE] waybackpack downloads HTML snapshots only — no CSS, JS, images, or fonts.`
- Accept `--from-date` and `--to-date` arguments (defaults: 20250101, 20260407).
- Accept `--output-dir` argument (default `resysta-backup/wayback`).
- Exit with code 0 on success (even if waybackpack has partial failures — it uses --ignore-errors), 1 on fatal error.
  </action>
  <verify>
    <automated>python scraper.py --help 2>&1 || python scraper.py --max-pages 0 2>&1; python wayback_download.py --help 2>&1 || echo "scripts created"</automated>
  </verify>
  <done>
    - scraper.py exists in project root, is syntactically valid Python, accepts --ip/--seed-file/--max-pages/--output-dir args
    - wayback_download.py exists in project root, is syntactically valid Python, accepts --from-date/--to-date/--output-dir args
    - Both scripts use argparse for CLI arguments
    - scraper.py uses requests.Session() with full browser headers including Sec-Fetch-* headers
    - wayback_download.py queries CDX API before invoking waybackpack
  </done>
</task>

<task type="auto">
  <name>Task 2: Create backup.sh orchestrator script</name>
  <files>backup.sh</files>
  <action>
Create backup.sh in project root (G:\01_OPUS\Projects\resystausa\). This is the single entry point that orchestrates the entire backup pipeline.

**Script structure** (use `set -euo pipefail`, with explicit error handling where fallback logic runs):

```
#!/usr/bin/env bash
set -euo pipefail
```

**Constants:**
```bash
IP_CANDIDATE_1="74.208.236.71"
IP_CANDIDATE_2="74.208.236.61"
DOMAIN="resystausa.com"
BACKUP_DIR="resysta-backup"
CHROME_UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
```

**Functions to implement (in this order):**

1. `log()` — Timestamped echo: `[HH:MM:SS] message`

2. `check_tools()` — Verify curl, python are available. Check if wget is available, set `WGET_AVAILABLE=true/false`. If wget not found: print install instructions (Chocolatey: `choco install wget`, or standalone from eternallybored.org), then log `[INFO] wget not found — will use Python scraper as primary download method`. Do NOT auto-download wget.

3. `check_longpaths()` — Run PowerShell query for LongPathsEnabled registry key. If value is 1, log `[OK]`. If not 1 or query fails, log `[WARN]` with instructions but do NOT abort (it is already enabled on this machine per research, this is a safety check).

4. `probe_connectivity()` — Probe both IP candidates and the domain. For each IP: `curl -s -o /tmp/probe_IP.html -w "%{http_code}" --connect-timeout 10 -H "Host: resystausa.com" -A "$CHROME_UA" "http://${IP}/"`. Check response body for `wp-content` (real page) vs `Just a moment` (challenge). For domain: `curl -s -o /tmp/probe_domain.html -w "%{http_code}" --connect-timeout 10 -A "$CHROME_UA" "https://resystausa.com/"`. Set `DIRECT_IP` to whichever IP returned 200 with real content (prefer IP_CANDIDATE_1 if both work). Set `ACCESS_METHOD` to `ip`, `domain`, or `dead`. If `dead`: log error, skip wget and scraper, jump directly to wayback fallback.

5. `download_sitemaps()` — Try all three WordPress sitemap URLs (sitemap.xml, sitemap_index.xml, wp-sitemap.xml) via curl to `http://${DIRECT_IP}/` with Host header. Save successful downloads to `$BACKUP_DIR/`. Extract `<loc>` URLs from sitemaps (and follow sitemap index child sitemaps). Append extracted URLs to `$BACKUP_DIR/url-list-raw.txt`. Copy the first successfully downloaded sitemap to `$BACKUP_DIR/sitemap.xml` if not already named that.

6. `run_wget_mirror()` — Only runs if `WGET_AVAILABLE=true`. Launch two wget processes in background:
   - wget IP pass: target `http://${DIRECT_IP}/` with Host header, all flags from RESEARCH.md section 1 (--mirror, --page-requisites, --convert-links, --adjust-extension, --no-parent, -nH, --trust-server-names, --restrict-file-names=windows, --wait=1, --random-wait, --limit-rate=500k, -e robots=off, full browser headers, --exclude-directories, --reject-regex for query strings, --reject="php", -P "$BACKUP_DIR/site", -o "$BACKUP_DIR/logs/wget-ip.log").
   - wget domain pass: target `https://resystausa.com/` with --no-clobber, --no-check-certificate, --wait=2, same exclusions, -o "$BACKUP_DIR/logs/wget-domain.log".
   - Wait for both with `wait $PID; EXIT=$?`. Log exit codes.
   If `WGET_AVAILABLE=false`: log `[SKIP] wget not available — proceeding to Python scraper` and set `WGET_SUCCESS=false`.

7. `scan_challenge_pages()` — grep -rl for challenge markers (_cf_chl_opt, cf-browser-verification, "Just a moment") across `$BACKUP_DIR/site/*.html`. Count total HTML files. Calculate contamination ratio. If 0 HTML files: `WGET_SUCCESS=false`. If >20% challenge pages: `WGET_SUCCESS=false`. Otherwise: `WGET_SUCCESS=true`. Save list of challenge files to `$BACKUP_DIR/logs/challenge-pages.txt`.

8. `run_python_scraper()` — Call: `python "$SCRIPT_DIR/scraper.py" --ip "$DIRECT_IP" --seed-file "$BACKUP_DIR/url-list-raw.txt" --output-dir "$BACKUP_DIR/site" --max-pages 2000`. Log exit code.

9. `run_wayback_fallback()` — Call: `python "$SCRIPT_DIR/wayback_download.py" --output-dir "$BACKUP_DIR/wayback"`. Log exit code.

10. `download_uploads()` — Targeted sweep of `/wp-content/uploads/` for years 2018-2026. If wget available, use wget -r -np targeting `http://${DIRECT_IP}/wp-content/uploads/`. If not, add `/wp-content/uploads/` as a seed URL to a second scraper.py run focused on asset downloading.

11. `consolidate_url_list()` — Assemble url-list.txt from all sources:
    - Extract URLs from wget log files (grep for HTTP 200 URLs, rewrite IP to domain form).
    - Extract URLs from downloaded HTML file tree (reconstruct URLs from file paths).
    - Extract `<loc>` URLs from any saved sitemap XML files.
    - Read url-list-raw.txt (already populated by scraper.py and wayback_download.py).
    - Deduplicate: `sort -u`, filter to resystausa.com URLs only, exclude query-string junk.
    - Write final `$BACKUP_DIR/url-list.txt`.
    - Log count.

12. `print_summary()` — Print final report: total HTML files, total assets, url-list.txt count, which methods succeeded (wget/scraper/wayback), any warnings.

**Main pipeline:**
```bash
mkdir -p "$BACKUP_DIR/site" "$BACKUP_DIR/logs" "$BACKUP_DIR/wayback"

check_tools
check_longpaths
probe_connectivity

if [[ "$ACCESS_METHOD" == "dead" ]]; then
  log "[WARN] Live site inaccessible — skipping to Wayback fallback"
  run_wayback_fallback
  consolidate_url_list
  print_summary
  exit 0
fi

download_sitemaps
run_wget_mirror
scan_challenge_pages

if [[ "$WGET_SUCCESS" == "false" ]]; then
  log "[INFO] wget mirror incomplete — running Python scraper fallback"
  run_python_scraper
  scan_challenge_pages  # re-check after scraper
fi

if [[ "$WGET_SUCCESS" == "false" ]]; then
  log "[INFO] Live site still incomplete — running Wayback Machine fallback"
  run_wayback_fallback
fi

download_uploads
consolidate_url_list
print_summary
```

Make the script executable: ensure it has a proper shebang and is created with LF line endings (not CRLF, which would break bash execution).
  </action>
  <verify>
    <automated>bash -n backup.sh && echo "backup.sh syntax OK" || echo "backup.sh syntax ERROR"</automated>
  </verify>
  <done>
    - backup.sh exists in project root with proper shebang (#!/usr/bin/env bash)
    - Script passes bash -n syntax check
    - Contains all 12 functions: log, check_tools, check_longpaths, probe_connectivity, download_sitemaps, run_wget_mirror, scan_challenge_pages, run_python_scraper, run_wayback_fallback, download_uploads, consolidate_url_list, print_summary
    - Probes BOTH IPs (74.208.236.71 and 74.208.236.61) in probe_connectivity
    - Gracefully handles wget absence (WGET_AVAILABLE=false path)
    - Calls scraper.py and wayback_download.py via python invocation
    - Auto-fallback chain: wget -> scraper -> wayback with no manual intervention
    - Challenge page detection with >20% threshold triggers fallback
    - consolidate_url_list produces deduplicated url-list.txt
  </done>
</task>

<task type="auto">
  <name>Task 3: Validate scripts and run connectivity probe</name>
  <files>backup.sh, scraper.py, wayback_download.py</files>
  <action>
Run validation checks on all three scripts without executing the full backup:

1. **Syntax validation:**
   - `bash -n backup.sh` — must pass
   - `python -c "import ast; ast.parse(open('scraper.py').read()); print('scraper.py OK')"` — must pass
   - `python -c "import ast; ast.parse(open('wayback_download.py').read()); print('wayback_download.py OK')"` — must pass

2. **Dependency check:**
   - `python -c "import requests, bs4, lxml; print('Python deps OK')"` — must pass
   - `python -c "import waybackpack; print('waybackpack OK')"` — must pass

3. **Quick connectivity probe** (runs the actual probe logic from backup.sh, but standalone):
   - Probe IP 74.208.236.71: `curl -s -o /dev/null -w "%{http_code}" --connect-timeout 10 -H "Host: resystausa.com" -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36" "http://74.208.236.71/"`
   - Probe IP 74.208.236.61: `curl -s -o /dev/null -w "%{http_code}" --connect-timeout 10 -H "Host: resystausa.com" -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36" "http://74.208.236.61/"`
   - Probe domain: `curl -s -o /dev/null -w "%{http_code}" --connect-timeout 10 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36" "https://resystausa.com/"`
   - Log which methods returned 200 vs non-200.

4. **Quick CDX check:**
   - `curl -s "https://web.archive.org/cdx/search/cdx?url=resystausa.com/*&output=text&fl=original&collapse=urlkey&filter=statuscode:200&limit=5" | head -5`
   - Log whether Wayback Machine has snapshots available.

5. **Fix any issues found:** If syntax checks fail, fix the offending script. If a dependency is missing, run `pip install` to install it. If both IPs are unreachable and domain is also unreachable, log this as a critical finding — the script's wayback-only path will be the only option.

6. **Line ending check:** Verify backup.sh does not have CRLF line endings: `file backup.sh` should show "ASCII text" not "ASCII text, with CRLF line terminators". If CRLF detected, convert with `sed -i 's/\r$//' backup.sh`.
  </action>
  <verify>
    <automated>bash -n backup.sh && python -c "import ast; ast.parse(open('scraper.py').read())" && python -c "import ast; ast.parse(open('wayback_download.py').read())" && echo "ALL SCRIPTS VALID"</automated>
  </verify>
  <done>
    - All three scripts pass syntax validation
    - Python dependencies (requests, bs4, lxml, waybackpack) are importable
    - Connectivity probe results are logged — we know which access method(s) work
    - CDX API availability confirmed
    - backup.sh has LF line endings (not CRLF)
    - If any script had syntax errors, they were fixed
  </done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| Script -> Origin server | HTTP requests to direct IP bypass Cloudflare; server may return unexpected content |
| Script -> archive.org | CDX API and waybackpack downloads from third-party archive service |
| Downloaded HTML -> Local filesystem | Untrusted HTML content saved to disk; filenames derived from URLs |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-fou-01 | T (Tampering) | Downloaded HTML files | accept | Read-only archival — files are not executed, only stored. No server-side rendering. |
| T-fou-02 | I (Information Disclosure) | curl/wget logs | mitigate | Logs saved to resysta-backup/logs/ only — no credentials in headers. User-Agent is a generic Chrome string. |
| T-fou-03 | D (Denial of Service) | Rate limiting on origin server | mitigate | 1-2s delay between requests (wget --wait=1 --random-wait, scraper.py random.uniform(1.5, 3.0)), --limit-rate=500k |
| T-fou-04 | S (Spoofing) | IP address may not be current origin | mitigate | Probe BOTH candidate IPs and validate response body contains wp-content before proceeding |
| T-fou-05 | T (Tampering) | Path traversal in URL-to-filepath mapping | mitigate | url_to_local_path strips leading slashes, uses Path resolution within OUTPUT_DIR only |
</threat_model>

<verification>
1. `bash -n backup.sh` passes (valid bash syntax)
2. `python -c "import ast; ast.parse(open('scraper.py').read())"` passes
3. `python -c "import ast; ast.parse(open('wayback_download.py').read())"` passes
4. `grep -c "def " backup.sh` returns 12 (all functions defined)
5. `grep "74.208.236.71" backup.sh` and `grep "74.208.236.61" backup.sh` both match (dual IP probe)
6. `grep "scraper.py" backup.sh` matches (calls Python scraper)
7. `grep "wayback_download.py" backup.sh` matches (calls Wayback downloader)
8. `grep "WGET_AVAILABLE" backup.sh` matches (handles wget absence)
9. `grep "Sec-Fetch" scraper.py` matches (full browser headers)
10. `grep "cdx/search/cdx" wayback_download.py` matches (CDX pre-check)
</verification>

<success_criteria>
- Three scripts exist in project root: backup.sh, scraper.py, wayback_download.py
- All three pass syntax validation
- backup.sh orchestrates the full pipeline: probe -> sitemap -> wget (if available) -> challenge check -> scraper fallback -> wayback fallback -> url consolidation
- Running `bash backup.sh` from project root produces resysta-backup/ with site/, wayback/, sitemap.xml, url-list.txt
- No manual intervention required — fallbacks trigger automatically based on challenge page detection
- Both IP candidates (74.208.236.71 and 74.208.236.61) are probed before any download begins
</success_criteria>

<output>
After completion, create `.planning/quick/260407-fou-make-complete-local-backup-of-resystausa/260407-fou-SUMMARY.md`
</output>
