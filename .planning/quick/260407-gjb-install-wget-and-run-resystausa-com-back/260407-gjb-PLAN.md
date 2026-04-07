---
phase: 260407-gjb
plan: 01
type: execute
wave: 1
depends_on: []
files_modified: []
autonomous: true
must_haves:
  truths:
    - "wget --version returns a valid GNU Wget version string"
    - "resysta-backup/ directory contains downloaded HTML pages and assets"
    - "No Cloudflare challenge pages contaminate the backup (or fallback chain handles them)"
  artifacts:
    - path: "resysta-backup/site/"
      provides: "Downloaded HTML pages, CSS, JS, images, fonts, PDFs"
    - path: "resysta-backup/logs/"
      provides: "wget execution logs for both IP and domain passes"
  key_links:
    - from: "wget binary"
      to: "backup.sh check_tools()"
      via: "command -v wget sets WGET_AVAILABLE=true"
---

<objective>
Install GNU Wget on Windows 10 and run the resystausa.com full site backup.

Purpose: wget is the Tier 1 download tool for this project but is not currently installed. The existing backup.sh orchestrator (from prior quick task 260407-fou) already contains the full wget mirror command with all correct flags (IP bypass, Host header, Chrome UA, rate limiting, etc.). Once wget is installed, backup.sh can use it as primary instead of falling back to the Python scraper.

Output: wget installed and accessible in bash PATH; resysta-backup/ populated with site mirror.
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/execute-plan.md
@$HOME/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/STATE.md
@CLAUDE.md
@backup.sh

Prior task 260407-fou created backup.sh, scraper.py, and wayback_download.py. The backup.sh
orchestrator already has full wget mirror logic with IP bypass, dual-pass (IP + domain),
challenge page detection, and automatic fallback to Python scraper if wget fails. It currently
detects wget as absent and skips to the Python scraper path. Installing wget unlocks the
primary Tier 1 download path.

Key facts from STATE.md and prior task:
- Origin IP 74.208.236.71 confirmed alive (301 -> 200, wp-content verified)
- Origin IP 74.208.236.61 also alive (same behavior)
- backup.sh probes both IPs and selects the first that responds
- HTTP to bare IP (port 80), NOT HTTPS — TLS cert hostname mismatch
- backup.sh uses --wait=1 --random-wait for IP pass, --wait=2 --random-wait for domain pass
- backup.sh already has --no-check-certificate, Host header, Chrome 124 UA, -e robots=off,
  --mirror, --page-requisites, --convert-links, --adjust-extension, --restrict-file-names=windows,
  --reject-regex for query string junk, --exclude-directories for wp-json/feed/trackback
</context>

<tasks>

<task type="auto">
  <name>Task 1: Install GNU Wget on Windows 10</name>
  <files></files>
  <action>
Install wget so it is available in the current bash (Git Bash / MSYS2) PATH.

**Strategy — try in order, stop at first success:**

1. **Check if Chocolatey is available:**
   ```
   command -v choco
   ```
   If choco exists, run:
   ```
   choco install wget -y
   ```
   Then verify with `wget --version`.

2. **If choco is NOT available, download standalone wget.exe:**
   Download the latest wget.exe for Windows from a reliable source. Use curl (already available in Git Bash) to download:
   ```
   curl -L -o /usr/bin/wget.exe "https://eternallybored.org/misc/wget/1.21.4/64/wget.exe"
   ```
   If that URL fails (404, timeout), try the GitHub mirror or alternative:
   ```
   curl -L -o /usr/bin/wget.exe "https://github.com/webfolderio/wget-windows/releases/download/v1.21.4/wget.exe"
   ```
   Set executable permission: `chmod +x /usr/bin/wget.exe`

3. **Verify installation:**
   ```
   wget --version
   ```
   Must print a GNU Wget version string. If it does not, the task has failed — do NOT proceed to Task 2.

**Important:**
- Do NOT skip wget installation and fall back to Python scraper. The user explicitly requires wget to be installed.
- The wget binary must be accessible from the same bash session that will run backup.sh.
- If /usr/bin/ is not writable, try /usr/local/bin/ or $HOME/bin/ (ensure it is on PATH).
  </action>
  <verify>
    <automated>wget --version 2>&1 | head -1</automated>
  </verify>
  <done>wget --version prints a GNU Wget version line (e.g., "GNU Wget 1.21.4 built on mingw32"). The binary is in PATH and callable from bash.</done>
</task>

<task type="auto">
  <name>Task 2: Run resystausa.com backup via backup.sh</name>
  <files></files>
  <action>
Run the existing backup.sh orchestrator which already contains the full wget mirror logic with all CLAUDE.md-specified flags.

**Pre-flight checks before running:**

1. Verify wget is available (Task 1 must have succeeded):
   ```
   wget --version | head -1
   ```

2. Verify the backup script exists and is syntactically valid:
   ```
   bash -n backup.sh
   ```

3. Create the output directory structure if it does not exist:
   ```
   mkdir -p resysta-backup/site resysta-backup/wayback resysta-backup/logs
   ```

**Run the backup:**
```
cd "G:/01_OPUS/Projects/resystausa" && bash backup.sh
```

The script will:
- check_tools() — detect wget as available this time
- check_longpaths() — warn if Windows LongPathsEnabled is not set
- probe_connectivity() — probe both IP candidates, select the first responding one
- download_sitemaps() — fetch sitemap.xml for URL discovery
- run_wget_mirror() — launch dual wget passes (IP + domain) in parallel with all required flags
- scan_challenge_pages() — verify no Cloudflare challenge contamination (>20% = fail)
- If challenge pages detected: automatic fallback to Python scraper, then Wayback
- download_uploads() — targeted sweep of /wp-content/uploads/
- consolidate_url_list() — assemble deduplicated URL list
- print_summary() — final report

**Monitoring:**
This is a long-running command (potentially 30-60+ minutes depending on site size). Run it with a generous timeout or in background. The script logs to resysta-backup/logs/wget-ip.log and resysta-backup/logs/wget-domain.log.

**If backup.sh encounters issues:**
- If wget exits with errors but downloaded some files, the script continues (|| true on wget calls)
- If challenge page contamination >20%, script auto-falls back to Python scraper
- If both live methods fail, script auto-falls back to Wayback Machine
- All three tiers are built into backup.sh — no manual intervention needed

**Post-run validation:**
After backup.sh completes, verify:
1. Count HTML files: `find resysta-backup/site -name "*.html" 2>/dev/null | wc -l`
2. Count total files: `find resysta-backup/site -type f 2>/dev/null | wc -l`
3. Check for challenge pages: `grep -rl "_cf_chl_opt\|Just a moment" resysta-backup/site/*.html 2>/dev/null | wc -l`
4. Check wget logs exist: `ls -la resysta-backup/logs/`
5. Check URL list: `wc -l resysta-backup/url-list.txt 2>/dev/null`
  </action>
  <verify>
    <automated>test -d "G:/01_OPUS/Projects/resystausa/resysta-backup/site" && find "G:/01_OPUS/Projects/resystausa/resysta-backup/site" -name "*.html" 2>/dev/null | head -5</automated>
  </verify>
  <done>resysta-backup/site/ contains downloaded HTML pages. wget log files exist in resysta-backup/logs/. The backup.sh print_summary() output confirms files were downloaded. At least 1 HTML file exists in the backup (ideally dozens+ for a full WordPress site).</done>
</task>

</tasks>

<verification>
1. `wget --version` returns a valid GNU Wget version
2. `resysta-backup/site/` directory exists and contains HTML files
3. `resysta-backup/logs/wget-ip.log` or `resysta-backup/logs/wget-domain.log` exist (proves wget was used, not just the Python fallback)
4. Challenge page count is 0 or below 20% of total HTML files
</verification>

<success_criteria>
- wget is installed and callable from bash
- backup.sh ran to completion using wget as the primary download method
- resysta-backup/site/ contains HTML pages and assets from resystausa.com
- No significant Cloudflare challenge page contamination in the backup
</success_criteria>

<output>
After completion, create `.planning/quick/260407-gjb-install-wget-and-run-resystausa-com-back/260407-gjb-SUMMARY.md`
</output>
