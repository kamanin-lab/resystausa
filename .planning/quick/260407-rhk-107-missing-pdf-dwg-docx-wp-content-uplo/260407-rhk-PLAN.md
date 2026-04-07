---
phase: quick
plan: 260407-rhk
type: execute
wave: 1
depends_on: []
files_modified:
  - .planning/quick/260407-rhk-107-missing-pdf-dwg-docx-wp-content-uplo/missing-files.txt
  - resysta-backup/site/wp-content/uploads/ (107 new files across YYYY/MM subdirs)
autonomous: true
must_haves:
  truths:
    - "All 107 missing files (50 PDFs, 54 ZIPs, 3 DOCXs) are downloaded to the correct local paths"
    - "Directory structure wp-content/uploads/YYYY/MM/ is preserved exactly"
    - "Downloaded files are non-zero size and not Cloudflare challenge pages"
  artifacts:
    - path: "resysta-backup/site/wp-content/uploads/"
      provides: "107 newly downloaded technical files"
  key_links:
    - from: "HTML pages referencing wp-content/uploads/*.pdf|*.zip|*.docx"
      to: "resysta-backup/site/wp-content/uploads/YYYY/MM/*"
      via: "relative href paths"
      pattern: "wp-content/uploads/\\d{4}/\\d{2}/"
---

<objective>
Download all 107 missing technical files (50 PDFs, 54 DWG/RVT/materials ZIPs, 3 DOCXs) from resystausa.com via direct IP bypass before WordPress access is permanently lost.

Purpose: These are the client's irreplaceable product specification sheets, AutoCAD drawings, Revit BIM files, and CSI specifications. Without them, the backup is incomplete for technical/engineering use.
Output: 107 files saved into resysta-backup/site/wp-content/uploads/ with correct YYYY/MM/ directory structure.
</objective>

<execution_context>
@.claude/get-shit-done/workflows/execute-plan.md
@.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/STATE.md
@.planning/quick/260407-qhd-resystausa-com/AUDIT-REPORT.md
@CLAUDE.md

CRITICAL connection details from STATE.md:
- Origin IP: 74.208.236.71 (IONOS hosting)
- Protocol: HTTP only (port 80) -- HTTPS will fail due to TLS cert hostname mismatch
- Host header: resystausa.com
- User-Agent: Chrome 124 browser UA
- Rate limit: wait 1-2s between requests
</context>

<tasks>

<task type="auto">
  <name>Task 1: Generate missing file URL list and batch download all 107 files</name>
  <files>
    .planning/quick/260407-rhk-107-missing-pdf-dwg-docx-wp-content-uplo/missing-files.txt
    .planning/quick/260407-rhk-107-missing-pdf-dwg-docx-wp-content-uplo/download-missing.py
    resysta-backup/site/wp-content/uploads/ (107 new files)
  </files>
  <action>
Step 1: Create a Python script `download-missing.py` that:

a) Scans all HTML files in `G:/01_OPUS/Projects/resystausa/resysta-backup/site/` for href attributes pointing to `https://resystausa.com/wp-content/uploads/` with extensions `.pdf`, `.zip`, `.docx` (and `.dwg_.zip`, `.rvt_.zip` variants).

b) For each found URL, checks if the corresponding local file exists at `G:/01_OPUS/Projects/resystausa/resysta-backup/site/wp-content/uploads/YYYY/MM/filename`. If the file does NOT exist locally, adds it to the download queue.

c) Writes the full list of missing URLs to `missing-files.txt` (one URL per line) for audit trail.

d) Downloads each missing file using Python `requests` library with these EXACT headers:
   - Direct IP: `http://74.208.236.71/wp-content/uploads/YYYY/MM/filename`
   - `Host: resystausa.com`
   - `User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36`
   - `Accept: */*`
   - `Accept-Language: en-US,en;q=0.9`

e) For each download:
   - Create the target directory (e.g., `uploads/2023/03/`) if it doesn't exist using `os.makedirs(exist_ok=True)`
   - Save the file to the correct local path preserving the YYYY/MM/ structure
   - Verify the response is HTTP 200 and Content-Type is NOT text/html (Cloudflare challenge detection)
   - Check file size > 0
   - Wait random 1.5-2.5 seconds between requests (use `time.sleep(random.uniform(1.5, 2.5))`)
   - Print progress: `[N/107] OK filename (size KB)` or `[N/107] FAILED filename (status_code)`

f) At the end, print summary: total downloaded, total failed, list of any failures.

IMPORTANT: Use HTTP (port 80), NOT HTTPS. The origin IP 74.208.236.71 does not have a valid TLS cert for direct access. The URL pattern is:
  `http://74.208.236.71/wp-content/uploads/2023/03/RESCLIPHF100.pdf`
with Host header `resystausa.com`.

IMPORTANT: The URL path extraction must handle the full URL like `https://resystausa.com/wp-content/uploads/2023/03/file.pdf` and convert it to the download URL `http://74.208.236.71/wp-content/uploads/2023/03/file.pdf`.

Step 2: Run the script. It will take approximately 3-5 minutes for 107 files with 1.5-2.5s delays.

Step 3: If any files fail, retry them once with a longer delay (3-5 seconds).
  </action>
  <verify>
    <automated>cd "G:/01_OPUS/Projects/resystausa/resysta-backup/site" && echo "PDFs:" && find wp-content/uploads -name "*.pdf" | wc -l && echo "ZIPs:" && find wp-content/uploads -name "*.zip" | wc -l && echo "DOCXs:" && find wp-content/uploads -name "*.docx" | wc -l && echo "---" && echo "Expected: ~93 PDFs, ~55 ZIPs, ~3 DOCXs"</automated>
  </verify>
  <done>All 107 files downloaded successfully (non-zero size, not CF challenge pages). File counts: ~93 PDFs (43 existing + 50 new), ~55 ZIPs (1 existing + 54 new), 3 DOCXs (0 existing + 3 new).</done>
</task>

<task type="auto">
  <name>Task 2: Validate downloads and report results</name>
  <files>
    .planning/quick/260407-rhk-107-missing-pdf-dwg-docx-wp-content-uplo/download-report.txt
  </files>
  <action>
After Task 1 completes, run validation:

1. Re-run the missing file scan from Task 1 (scan HTML hrefs, check local existence). Any URLs still missing = failed downloads.

2. For each newly downloaded file, verify:
   - File size > 1 KB (catch empty/error pages)
   - First bytes are NOT `<!DOCTYPE` or `<html` (catch Cloudflare challenge HTML saved as .pdf/.zip)
   - PDFs start with `%PDF` header
   - ZIPs start with `PK` header (0x504B)
   - DOCXs start with `PK` header (DOCX is ZIP-based)

3. Write `download-report.txt` with:
   - Count of successfully downloaded files by type
   - Count of still-missing files (if any)
   - List of any files that failed validation (wrong content type, zero size, etc.)
   - List of any files that are actually Cloudflare challenge pages

4. If any files failed, print their URLs clearly so they can be retried manually or via Wayback Machine.
  </action>
  <verify>
    <automated>cat "G:/01_OPUS/Projects/resystausa/.planning/quick/260407-rhk-107-missing-pdf-dwg-docx-wp-content-uplo/download-report.txt" | head -20</automated>
  </verify>
  <done>Download report confirms all 107 files present and valid, or clearly documents which files failed with actionable next steps.</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| Script to origin server | HTTP requests to 74.208.236.71 with Host header spoofing |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-rhk-01 | Tampering | Downloaded files | mitigate | Validate file headers (PDF=%PDF, ZIP=PK) to ensure Cloudflare did not serve challenge HTML in place of real files |
| T-rhk-02 | Denial of Service | Origin server rate limiting | mitigate | Random 1.5-2.5s delay between requests, single-threaded download |
| T-rhk-03 | Information Disclosure | IP bypass detection | accept | Low risk -- archival download of own client's public files |
</threat_model>

<verification>
1. File count check: `find wp-content/uploads -name "*.pdf" | wc -l` shows ~93 (was 43)
2. File count check: `find wp-content/uploads -name "*.zip" | wc -l` shows ~55 (was 1)
3. File count check: `find wp-content/uploads -name "*.docx" | wc -l` shows 3 (was 0)
4. No Cloudflare challenge pages: `grep -rl "Just a moment" wp-content/uploads/ 2>/dev/null` returns empty
5. All files non-zero: `find wp-content/uploads -size 0 -name "*.pdf" -o -size 0 -name "*.zip" -o -size 0 -name "*.docx"` returns empty
</verification>

<success_criteria>
- 107 missing files downloaded to correct wp-content/uploads/YYYY/MM/ paths
- Zero Cloudflare challenge pages saved as downloads
- All files pass header validation (PDF=%PDF, ZIP/DOCX=PK)
- download-report.txt confirms success or documents failures
</success_criteria>

<output>
After completion, create `.planning/quick/260407-rhk-107-missing-pdf-dwg-docx-wp-content-uplo/260407-rhk-SUMMARY.md`
</output>
