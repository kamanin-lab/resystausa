---
phase: quick-260407-rhm
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - scripts/scrape-blog-posts.py
  - resysta-backup/site/blog/*/index.html
autonomous: true
must_haves:
  truths:
    - "All ~61 blog post URLs are enumerated from CDX API and/or live site"
    - "Each blog post HTML is saved to resysta-backup/site/blog/[slug]/index.html"
    - "Blog post images referenced in posts are downloaded alongside the HTML"
    - "No Cloudflare challenge pages saved (validated by grep for cf_chl)"
  artifacts:
    - path: "scripts/scrape-blog-posts.py"
      provides: "Blog post enumeration and download script"
    - path: "resysta-backup/site/blog/*/index.html"
      provides: "Individual blog post HTML files"
  key_links:
    - from: "scripts/scrape-blog-posts.py"
      to: "http://74.208.236.71/blog/*"
      via: "HTTP requests with Host header bypass"
      pattern: "Host.*resystausa.com"
---

<objective>
Scrape all ~61 blog posts from resystausa.com and save them into the existing backup at
`resysta-backup/site/blog/[post-slug]/index.html`.

Purpose: The blog index page uses WP Bakery's vc_basic_grid which loads posts entirely via
AJAX (admin-ajax.php). The wget mirror captured only the empty blog shell page. All ~61 blog
posts are missing from the backup and must be recovered before site access is lost.

Output: ~61 blog post HTML files + inline images, organized as `blog/[slug]/index.html`
</objective>

<execution_context>
@.planning/STATE.md
@CLAUDE.md
@.planning/quick/260407-qhd-resystausa-com/AUDIT-REPORT.md
</execution_context>

<context>
**Origin IP:** 74.208.236.71 (from STATE.md — use HTTP port 80 only, NOT HTTPS)
**Blog index:** Uses `vc_basic_grid` AJAX loader — no post links in static HTML
**Blog post count:** ~61 (from class="type-post" count in audit)
**Access method:** Direct IP bypass with Host header (per CLAUDE.md decision tree)

Key parameters for all HTTP requests:
- Base URL: `http://74.208.236.71`
- Header: `Host: resystausa.com`
- Header: `User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36`
- Delay: 1.5-3.0 seconds between requests (Python tier)
- NO HTTPS — TLS cert mismatch on bare IP

**Existing backup structure:**
- `resysta-backup/site/blog/index.html` — blog shell (no post content)
- `resysta-backup/site/blog/` — target directory for post subdirectories
</context>

<tasks>

<task type="auto">
  <name>Task 1: Enumerate all blog post URLs via CDX API + live site WP REST API</name>
  <files>scripts/scrape-blog-posts.py</files>
  <action>
Create a Python script `scripts/scrape-blog-posts.py` that enumerates and downloads all blog posts.

**Step 1 — Enumerate URLs using TWO methods and merge:**

Method A — Wayback CDX API (no rate limit concern, public API):
```
GET http://web.archive.org/cdx/search/cdx?url=resystausa.com/blog/*/&output=json&fl=original&collapse=urlkey&limit=500
```
Parse response, extract unique blog post URLs matching pattern `resystausa.com/blog/[slug]/`.
Filter OUT pagination URLs (page/2/, page/3/), feed URLs (/feed/), and the bare /blog/ index.

Method B — WordPress REST API via IP bypass (the WP REST API is typically accessible even when the front-end blog grid is AJAX-only):
```
GET http://74.208.236.71/wp-json/wp/v2/posts?per_page=100&page=1&_fields=id,slug,link,title
Headers: Host: resystausa.com, User-Agent: Chrome 124
```
Paginate through all pages (increment page= until empty response or 400).
Extract slug from each post to build URL: `https://resystausa.com/blog/{slug}/`

Method C — If REST API is blocked, fall back to parsing the sitemap:
```
GET http://74.208.236.71/sitemap.xml  (or /sitemap_index.xml, /post-sitemap.xml)
Headers: Host: resystausa.com
```
Parse XML for URLs matching `/blog/`.

**Merge and deduplicate** all URLs from methods A+B (or A+C). Normalize: strip trailing slashes, lowercase, remove query strings.

Print the full enumerated URL list with count before proceeding to download.

**IMPORTANT:**
- Use `requests` library with a `Session` object
- Set all headers on the session: Host, User-Agent, Accept
- For Method B (REST API), the base URL is `http://74.208.236.71/wp-json/wp/v2/posts`
- Wait 1.5s between REST API pagination requests
- If REST API returns 403 or 404, skip to Method C (sitemap), log the failure
  </action>
  <verify>
    <automated>python scripts/scrape-blog-posts.py --enumerate-only 2>&1 | tail -5</automated>
  </verify>
  <done>Script prints a list of 50+ unique blog post URLs. The enumeration count is printed to stdout.</done>
</task>

<task type="auto">
  <name>Task 2: Download all blog posts via IP bypass and save to backup</name>
  <files>resysta-backup/site/blog/*/index.html</files>
  <action>
The same script `scripts/scrape-blog-posts.py` (from Task 1) handles downloading when run without `--enumerate-only`.

**Download logic (already in the script from Task 1, this task is about running it):**

For each enumerated blog post URL:
1. Convert `https://resystausa.com/blog/{slug}/` to `http://74.208.236.71/blog/{slug}/`
2. GET the page with full headers (Host: resystausa.com, Chrome UA, Accept: text/html)
3. Check response: if status != 200, log error and skip
4. Check for Cloudflare challenge: if response body contains `_cf_chl_opt` or `Just a moment`, log as CF-blocked and skip
5. Save HTML to `resysta-backup/site/blog/{slug}/index.html` (create subdirectory if needed)
6. Parse saved HTML with BeautifulSoup to find inline images:
   - Find all `<img>` tags with `src` containing `wp-content/uploads/`
   - For each image URL, convert to IP-bypass URL and download
   - Save images preserving the wp-content/uploads/YYYY/MM/filename.ext path structure under `resysta-backup/site/`
   - Skip images that already exist in the backup (check file existence first)
7. Wait random 1.5-3.0 seconds before next post
8. Print progress: `[N/total] Downloaded: {slug}` or `[N/total] SKIPPED (CF block): {slug}`

**After all downloads complete:**
- Print summary: total downloaded, total skipped, total images downloaded
- Print list of any CF-blocked or failed URLs for manual review

**Run the full download:**
```bash
cd G:/01_OPUS/Projects/resystausa
python scripts/scrape-blog-posts.py
```

The script should take ~3-5 minutes for ~61 posts at 2s average delay.
  </action>
  <verify>
    <automated>ls -d G:/01_OPUS/Projects/resystausa/resysta-backup/site/blog/*/index.html 2>/dev/null | wc -l</automated>
  </verify>
  <done>At least 50 blog post directories exist under resysta-backup/site/blog/, each containing an index.html. No Cloudflare challenge pages present (verified by: grep -rl "_cf_chl_opt" resysta-backup/site/blog/*/index.html returns empty).</done>
</task>

<task type="auto">
  <name>Task 3: Validate downloaded posts and commit to backup</name>
  <files>resysta-backup/site/blog/*/index.html</files>
  <action>
**Validation checks:**

1. Count total blog post directories created:
   ```bash
   ls -d resysta-backup/site/blog/*/index.html | wc -l
   ```
   Expected: ~61 (or close to it)

2. Check for Cloudflare challenge contamination:
   ```bash
   grep -rl "_cf_chl_opt\|Just a moment" resysta-backup/site/blog/*/index.html
   ```
   Expected: no results. If any found, delete those files and re-download via Wayback Machine fallback:
   ```bash
   # For each CF-blocked slug, try Wayback:
   # wget "https://web.archive.org/web/2025/https://resystausa.com/blog/{slug}/" -O resysta-backup/site/blog/{slug}/index.html
   ```

3. Check for empty or tiny files (< 1KB = likely error pages):
   ```bash
   find resysta-backup/site/blog -name "index.html" -size -1k
   ```
   If any found, investigate and re-download or remove.

4. Spot-check 3 random posts to verify they contain actual blog content (look for `<article` tag, `entry-content` class, etc.):
   ```bash
   grep -l "entry-content\|article\|post-content" resysta-backup/site/blog/*/index.html | head -3
   ```

**After validation passes, stage and commit:**
```bash
cd G:/01_OPUS/Projects/resystausa
git add resysta-backup/site/blog/
git add scripts/scrape-blog-posts.py
git commit -m "feat: scrape ~61 blog posts from resystausa.com via IP bypass

Enumerated blog post URLs via Wayback CDX API + WP REST API.
Downloaded each post HTML + inline images via direct IP (74.208.236.71).
Blog index used WP Bakery AJAX grid — posts were not captured by wget mirror.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```
  </action>
  <verify>
    <automated>cd "G:/01_OPUS/Projects/resystausa" && git log --oneline -1 && ls -d resysta-backup/site/blog/*/index.html | wc -l</automated>
  </verify>
  <done>Git commit exists containing all blog post HTML files. At least 50 blog post directories present under blog/. Zero Cloudflare challenge pages in the downloaded files. Script committed alongside the backup files.</done>
</task>

</tasks>

<verification>
1. `ls -d resysta-backup/site/blog/*/index.html | wc -l` returns 50+
2. `grep -rl "_cf_chl_opt" resysta-backup/site/blog/*/index.html` returns empty
3. `find resysta-backup/site/blog -name "index.html" -size -1k` returns empty (no tiny error pages)
4. `git log --oneline -1` shows the blog post commit
5. `python scripts/scrape-blog-posts.py --enumerate-only` can re-enumerate for verification
</verification>

<success_criteria>
- All ~61 blog posts downloaded as individual HTML files in blog/[slug]/index.html
- Inline images from blog posts saved to wp-content/uploads/ structure
- No Cloudflare challenge pages in the backup
- All files committed to git repository
- Script is rerunnable (idempotent — skips existing files)
</success_criteria>
