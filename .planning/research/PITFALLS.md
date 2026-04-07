# Domain Pitfalls: Website Archival / Mirroring (WordPress + Cloudflare)

**Domain:** Website archival — WordPress site behind Cloudflare WAF, direct IP bypass, multi-tool fallback strategy
**Researched:** 2026-04-07
**Applies to:** resystausa.com (74.208.236.61, IONOS, Cloudflare)

---

## Critical Pitfalls

Mistakes that silently corrupt the archive or cause it to be unrecoverable later.

---

### Pitfall 1: Silently Saving Cloudflare Challenge Pages as Content

**What goes wrong:** wget or Python requests receives a Cloudflare browser-integrity-check HTML page (the "Checking your browser..." interstitial) and saves it to disk as if it were real content. The download succeeds with HTTP 200, the file looks like a normal .html file, and no error is reported. The archive appears complete but contains challenge page garbage instead of real pages.

**Why it happens:** Cloudflare's JS challenge returns HTTP 200 with HTML that embeds JavaScript the client must execute. wget cannot execute JavaScript. The direct-IP bypass method sidesteps this entirely, but if the domain-based fallback is used without the correct User-Agent, Cloudflare re-challenges. When the browser UA is accepted but a Turnstile CAPTCHA is active on specific pages, those pages still return challenge HTML.

**Consequences:** Entire sections of the archive are corrupted with boilerplate challenge text. This is invisible unless you manually inspect files. url-list.txt will include those URLs as "captured" when they were not.

**Warning signs:**
- Downloaded HTML files are very small (< 5 KB) and uniform in size
- Files contain the string "Checking your browser" or "cf-ray" in their body
- HTTP response headers include `cf-ray:` or `server: cloudflare`
- Files contain `<title>Just a moment...</title>` or `window._cf_chl_opt`

**Prevention:**
1. After the wget pass, run a spot-check: `grep -rl "Checking your browser\|cf-ray\|_cf_chl_opt" resysta-backup/ | head -20`
2. Use the direct-IP method (74.208.236.61 + `Host: resystausa.com` header) as the primary path — it bypasses Cloudflare's edge entirely
3. Verify the first response before launching the full mirror: `wget -S --spider --header="Host: resystausa.com" http://74.208.236.61/ 2>&1 | grep "HTTP/"`
4. For any page returning a challenge, fall back to waybackpack for that specific URL

**Phase:** Step 1 (connectivity check) must validate real content is returned before Step 3 (full mirror) begins.

---

### Pitfall 2: SSL Certificate Hostname Mismatch on Direct IP Connections

**What goes wrong:** When connecting to `https://74.208.236.61` with a `Host: resystausa.com` header, wget's SSL layer sees the certificate is issued for `resystausa.com` but the connection target is an IP address. The TLS SNI field sends the IP, not the hostname. wget aborts with "ERROR: certificate common name `resystausa.com` doesn't match requested host name `74.208.236.61`."

**Why it happens:** SNI is used by the server to select the correct certificate. When you connect to a bare IP address, SNI is either absent or set to the IP, causing a certificate name mismatch even though the cert is perfectly valid for the domain.

**Consequences:** HTTPS connections to the direct IP fail entirely, forcing a fallback to HTTP (unencrypted) or requiring `--no-check-certificate` which silently opens the possibility of getting a wrong server's content.

**Warning signs:**
- `wget: ERROR: certificate common name doesn't match requested host name`
- `SSL: certificate subject name does not match target host name`

**Prevention:**
1. Use HTTP (not HTTPS) for direct-IP connections: `http://74.208.236.61/` — IONOS origin servers typically serve unencrypted HTTP on port 80; Cloudflare handles the HTTPS termination
2. If HTTPS is required, pass `--no-check-certificate` AND verify the server identity by checking the response contains expected WordPress content (look for `wp-content` in the HTML)
3. For Python requests: `requests.get("http://74.208.236.61/", headers={"Host": "resystausa.com"}, verify=False)` with a content sanity check

**Phase:** Step 1 (connectivity check) — test HTTP vs HTTPS before committing to a method.

---

### Pitfall 3: Windows MAX_PATH (260-character) Truncation Silently Drops Files

**What goes wrong:** WordPress sites generate deeply nested URLs: `/wp-content/uploads/2023/08/some-long-descriptive-product-image-filename-hero-banner.jpg`. When wget mirrors to `G:\01_OPUS\Projects\resystausa\resysta-backup\`, the full filesystem path can exceed Windows' legacy MAX_PATH limit of 260 characters. wget either silently skips the file, creates a truncated filename that overwrites unrelated files, or exits with a cryptic error.

**Why it happens:** Windows Win32 API has a 260-character path limit by default. The base path alone (`G:\01_OPUS\Projects\resystausa\resysta-backup\`) is 47 characters, leaving 213 characters for the mirrored URL path. WordPress media filenames with date subdirectories consume this budget quickly.

**Consequences:** Media files (images, PDFs) are missing from the archive with no warning. The url-list.txt will show them as present when they are not.

**Warning signs:**
- Image files missing in `wp-content/uploads/` subdirectories
- wget log shows errors containing "File name too long" or silent skips with no error at all
- Spot-checking a specific upload URL returns 200 but the file is absent locally

**Prevention:**
1. Enable Windows Long Path support before running wget: open Group Policy (`gpedit.msc`) > Computer Configuration > Administrative Templates > System > Filesystem > "Enable Win32 long paths" > Enabled. Alternatively: `reg add "HKLM\SYSTEM\CurrentControlSet\Control\FileSystem" /v LongPathsEnabled /t REG_DWORD /d 1 /f`
2. Keep the output directory path as short as possible — consider `C:\r\` or `G:\r\` instead of deep nesting
3. After mirroring, compare the count of URLs referencing images against the count of files in `wp-content/uploads/`

**Phase:** Step 3 (wget mirror) — enable long paths before the first wget run.

---

### Pitfall 4: wget Query String Infinite Crawl / Duplicate Bloat

**What goes wrong:** WordPress generates multiple URL shapes for the same content: `/?p=123`, `/post-slug/`, `/?page=2`, `/?s=searchterm`, `/?replytocom=456`, and calendar archive URLs (`/2023/08/`, `/2023/`). Without filtering, wget treats each query-string variant as a unique URL and downloads them all — potentially crawling infinite search result pages or paginated archives indefinitely, creating thousands of near-duplicate files.

**Why it happens:** wget's `--mirror` flag (`-r -N -l inf --no-remove-listing`) follows every discovered link. WordPress REST API endpoints at `/wp-json/` expose hundreds of sub-paths. Comment reply links (`?replytocom=`) generate one URL per comment. Search boxes (`?s=`) create unbounded search result pages if any crawled page has a search widget.

**Consequences:** Archive ballooned with junk files, hours of extra crawl time, rate-limit triggers, and a url-list.txt filled with thousands of useless query-string URLs that pollute SEO mapping.

**Warning signs:**
- Download count growing far beyond expected page count
- Presence of `/?s=` or `/?replytocom=` or `/wp-json/` paths in the output directory
- Download has been running for many hours with no sign of completion

**Prevention:**
Always include these reject patterns in the wget command:
```
--reject-regex="(\?s=|\?replytocom=|/wp-json/|/feed/|/trackback/|\?share=|\?like=|\?like_actor=|\?like_comment=|\?ver=|/embed/)"
--exclude-directories="/wp-json,/feed,/trackback,/comments/feed"
```
Additionally use `--no-host-directories` and `--restrict-file-names=windows` to sanitize filenames.

**Phase:** Step 3 (wget mirror) — include reject-regex in the initial wget command, not as an afterthought.

---

## Moderate Pitfalls

---

### Pitfall 5: --convert-links Appears Broken During Long Downloads

**What goes wrong:** After running wget --mirror for hours, inspecting downloaded HTML files shows all URLs still pointing to `https://resystausa.com/...` — absolute links that break local browsing. The conclusion that `--convert-links` is not working leads to premature abort or adding unnecessary post-processing.

**Why it happens:** `--convert-links` is intentionally deferred — wget only performs link rewriting in a single pass at the very end of the entire download, immediately before the process exits. During the download, files contain unconverted absolute links. This is by design and documented in wget source code: link conversion requires knowing the full set of downloaded files first.

**Prevention:**
- Do not inspect HTML files for link conversion while wget is still running
- If wget is killed mid-run (power loss, timeout), links will NOT be converted — rerun with `-nc` (no-clobber) to resume and let it complete normally
- Alternatively run a post-processing pass with `wget --convert-links --input-file=url-list.txt` after the initial crawl

**Phase:** Step 3 (wget mirror) — understanding this prevents false-alarm aborts.

---

### Pitfall 6: Media Offloaded to External CDN / S3 is Invisible to wget

**What goes wrong:** If the WordPress site uses a media offload plugin (WP Offload Media, Jetpack CDN, etc.), all images and files served from `wp-content/uploads/` are actually delivered from an S3 bucket, CloudFront, or StackPath CDN URL. wget following links from `resystausa.com` will not follow those external domains and the media will be missing from the archive.

**Why it happens:** Media offload plugins rewrite `<img src>` tags to point at `https://cdn.resystausa.com/...` or `https://s3.amazonaws.com/resystausa/...`. wget's `--no-parent` and domain-scoping flags prevent it from following these external URLs.

**Warning signs:**
- `wp-content/uploads/` directory in the archive is empty or sparse despite the live site having images
- HTML files reference `cdn.`, `s3.amazonaws.com`, `cloudfront.net`, or `stackpathcdn.com` for image sources
- wget log shows many "external link" skips for image URLs

**Prevention:**
1. First, inspect the live site's HTML source for image URL patterns before running the mirror
2. If offloaded CDN is detected, add the CDN domain to wget's `--domains` list: `--domains=resystausa.com,cdn.resystausa.com`
3. As a catch-all, run a separate download pass targeting only `<img>`, `<source>`, and `<video>` tags via the Python BS4 scraper with external domain following enabled

**Phase:** Step 3 (wget mirror) — check HTML source before the wget run. Step 4 (BS4 scraper) handles external CDN media.

---

### Pitfall 7: TLS Fingerprinting Blocks Python requests Despite Correct User-Agent

**What goes wrong:** The Python requests library sends a distinctive TLS ClientHello fingerprint (JA3 hash) that Cloudflare recognizes as non-browser traffic regardless of the User-Agent header. Even with `User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124...`, the requests library is blocked with 403 when going through the Cloudflare edge (domain-based access).

**Why it happens:** Cloudflare's Bot Management analyzes the TLS handshake's cipher suite order, extensions, and elliptic curves — the "JA3 fingerprint." Python's `ssl` module produces a consistently different fingerprint than Chrome's TLS stack. This detection is passive and invisible — no challenge page, just a clean 403.

**Consequences:** The Python BS4 fallback scraper fails even before it starts processing pages, wasting time on a dead code path.

**Prevention:**
1. The Python scraper fallback should always target the direct IP (`http://74.208.236.61/`), not the domain, to avoid Cloudflare TLS inspection entirely
2. If domain access is required (e.g., to follow redirects), use `curl_cffi` instead of `requests`: `pip install curl-cffi` and use `curl_cffi.requests.get(url, impersonate="chrome124")`
3. Do not spend time debugging requests User-Agent headers if 403 persists — switch to curl_cffi or the direct IP method

**Phase:** Step 5 (Python BS4 scraper) — choose the right HTTP client before writing scraper code.

---

### Pitfall 8: waybackpack Downloads Only HTML Snapshots, Not Assets

**What goes wrong:** waybackpack downloads each captured HTML snapshot from the Wayback Machine but does NOT download the CSS, JS, images, or fonts referenced in those pages. The result is raw HTML that renders as unstyled text — unusable for visual reference.

**Why it happens:** waybackpack is designed to download the HTML content of each URL snapshot. It does not recursively fetch page requisites. Additionally, many assets from WordPress sites were never captured by the Wayback Machine at all — bots typically only crawl HTML pages.

**Warning signs:**
- Downloaded pages display without styling when opened in a browser
- No `wp-content/` subdirectory exists in waybackpack output
- Very fast download time (assets are skipped, not downloaded)

**Prevention:**
1. Use waybackpack only as a last-resort source for HTML content (text, structure, URLs)
2. After waybackpack completes, run a targeted wget pass using `--input-file` with the discovered URLs to attempt asset recovery from the live server
3. If the live server is also inaccessible, accept that waybackpack output is HTML-only and document that limitation explicitly in the url-list.txt header

**Phase:** Step 6 (waybackpack fallback) — set correct expectations and add a post-processing step.

---

### Pitfall 9: Duplicate Files from www vs non-www and HTTP vs HTTPS Variants

**What goes wrong:** WordPress sites frequently have both `http://` and `https://` versions, and `www.resystausa.com` alongside `resystausa.com`. wget following redirects can end up downloading the same page twice under different directory names, or creating broken local links when the canonical URL redirects.

**Why it happens:** WordPress adds `<link rel="canonical">` tags and 301 redirects. wget's `--trust-server-names` flag follows the final URL after redirects, which can cause the file to be saved under the canonical path. Without this flag, wget saves under the original URL, but `--convert-links` rewrites to the canonical. The two interact unpredictably.

**Prevention:**
1. Explicitly set wget to follow the canonical domain with `--domains=resystausa.com` (no www)
2. Use `--trust-server-names` to save files based on final redirected URL — this reduces duplicates
3. Do not use both `http://` and `https://` start URLs in the same wget invocation

**Phase:** Step 3 (wget mirror) — configure domain scope before running.

---

## Minor Pitfalls

---

### Pitfall 10: wget Default User-Agent Triggers Immediate 403

**What goes wrong:** The first wget request returns 403 Forbidden. The default wget User-Agent is `Wget/1.21.x (linux-gnu)` — explicitly blocked by Cloudflare's Browser Integrity Check in default configurations.

**Prevention:** Always include `-U "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"` in every wget invocation. Never use the default UA.

**Phase:** Step 3 (wget mirror) — this should be in every wget command template.

---

### Pitfall 11: Query String Filenames Break on Windows (? and = characters)

**What goes wrong:** wget on Windows creates files with `?` and `=` in their names to represent query strings (e.g., `index.html?ver=6.4.3`). Windows NTFS does not allow `?` in filenames. This causes file creation to silently fail or wget to crash.

**Prevention:** Always include `--restrict-file-names=windows` in wget commands. This flag replaces illegal Windows filename characters with URL-encoded equivalents.

**Phase:** Step 3 (wget mirror) — mandatory flag for Windows operation.

---

### Pitfall 12: sitemap.xml May Not List All Pages

**What goes wrong:** WordPress sitemaps are split across multiple files (`sitemap_index.xml`, `post-sitemap.xml`, `page-sitemap.xml`, `product-sitemap.xml`). Downloading only `sitemap.xml` misses everything in sub-sitemaps. Some WordPress configurations only have `wp-sitemap.xml` (the native WordPress sitemap), not the Yoast/Rank Math sitemap format.

**Prevention:** Check all three sitemap entry points: `sitemap.xml`, `sitemap_index.xml`, and `wp-sitemap.xml`. Parse sitemap index files to extract and download all child sitemaps. Use sitemap URLs to seed the url-list.txt before the wget run.

**Phase:** Step 2 (sitemap download) — check all three URLs, parse index files.

---

### Pitfall 13: wp-content/uploads/ Gaps from Year/Month Directories Not Crawled

**What goes wrong:** wget's recursive crawl discovers uploaded media only if those files are referenced on crawled pages. Orphaned media (uploaded but not embedded in posts) and media from deleted or draft posts will be absent. Manually brute-forcing `/wp-content/uploads/YYYY/MM/` is necessary to catch everything.

**Prevention:** After the main wget mirror completes, run a separate wget pass targeting the uploads directory: `wget -r -np --no-check-certificate -U "[browser-UA]" --header="Host: resystausa.com" http://74.208.236.61/wp-content/uploads/`. This only works if directory listing is enabled on the server. If not, the sitemap and crawled page references are the only source.

**Phase:** Step 4 (uploads harvesting) — separate dedicated pass for media uploads.

---

### Pitfall 14: Rate Limiting from IONOS Origin Server (Not Cloudflare)

**What goes wrong:** Even with Cloudflare bypassed via direct IP, the IONOS origin server itself may have rate limiting or fail2ban rules. Rapid requests trigger a temporary IP block, returning 429 or 503, or silently dropping connections. This is distinct from Cloudflare's protection.

**Prevention:** Honor the 1-2 second delay between requests (`--wait=2 --random-wait` in wget). Monitor the download log for sudden bursts of 503 or connection timeouts. If blocking occurs, increase wait to 3-5 seconds and reduce `--tries` to avoid hammering a blocked endpoint repeatedly.

**Phase:** Step 3 and Step 5 — apply delays consistently across all tools.

---

## Phase-Specific Warnings

| Phase / Step | Likely Pitfall | Mitigation |
|---|---|---|
| Step 1: Connectivity check | Cloudflare challenge page returned as 200 | Verify response contains `wp-content` text, not `Checking your browser` |
| Step 1: Connectivity check | HTTPS to direct IP fails with cert mismatch | Use HTTP (port 80) for direct IP; HTTPS for domain-based access |
| Step 2: Sitemap download | Only `sitemap.xml` checked; sub-sitemaps missed | Check `sitemap.xml`, `sitemap_index.xml`, `wp-sitemap.xml` — parse all |
| Step 3: wget mirror | Default User-Agent blocked immediately | Hardcode Chrome UA in every wget command |
| Step 3: wget mirror | Query string infinite crawl bloat | Include `--reject-regex` covering `?s=`, `?replytocom=`, `/wp-json/` |
| Step 3: wget mirror | Windows 260-char path truncation | Enable LongPathsEnabled registry key before running |
| Step 3: wget mirror | `?` in filenames crash on Windows | Use `--restrict-file-names=windows` always |
| Step 3: wget mirror | `--convert-links` looks broken mid-run | Normal — conversion happens at job completion only |
| Step 3: wget mirror | www vs non-www duplicates | `--domains=resystausa.com` (no www) + `--trust-server-names` |
| Step 4: uploads harvest | Media offloaded to CDN, not on origin | Check HTML source for external CDN domains before wget |
| Step 5: Python BS4 scraper | TLS fingerprint 403 from Cloudflare edge | Target direct IP, or use `curl_cffi` with `impersonate="chrome124"` |
| Step 5: Python BS4 scraper | IONOS rate limit from rapid requests | Always `time.sleep(random.uniform(1.5, 3))` between requests |
| Step 6: waybackpack | HTML-only download, no assets | Document limitation; run separate wget pass for assets afterward |
| Step 6: waybackpack | Empty/single-line index.html files | Verify downloaded files exceed 1 KB; re-fetch failures individually |
| All steps | Cloudflare challenge saved as real HTML | Post-run grep for `_cf_chl_opt` and `Just a moment` across all .html files |

---

## Sources

- Kevin Cox — Mirroring a Website with Wget: https://kevincox.ca/2022/12/21/wget-mirror/
- A.J. Fleming — Archive a WordPress site using wget: https://ajfleming.info/2023/06/12/archive-a-wordpress-site-using-wget/
- Daniel Malmer — Why wget --convert-links isn't converting your links: https://danielmalmer.medium.com/heres-why-wget-s-convert-links-option-isn-t-converting-your-links-cec832ee934c
- ZenRows — Cloudflare 403 Forbidden Bypass: https://www.zenrows.com/blog/cloudflare-403-forbidden-bypass
- ZenRows — How to Bypass Cloudflare: https://www.zenrows.com/blog/bypass-cloudflare
- Cloudflare Community — wget certificate error: https://community.cloudflare.com/t/certificate-error-when-running-a-wget-command/38883
- GNU wget manual — HTTPS/TLS Options: https://www.gnu.org/software/wget/manual/html_node/HTTPS-_0028SSL_002fTLS_0029-Options.html
- Microsoft Learn — Maximum Path Length Limitation: https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation
- waybackpack GitHub Issues — empty files and asset gaps: https://github.com/jsvine/waybackpack/issues
- Cloudflare Challenges docs — Turnstile / JS challenge: https://developers.cloudflare.com/cloudflare-challenges/challenge-types/turnstile/
- ScrapingAnt — wget SSL certificate ignore: https://scrapingant.com/blog/wget-ignore-ssl
- ScrapingAnt — wget cheatsheet: https://scrapingant.com/blog/wget-cheatsheet
- DEV Community — Why Python requests scraper is already blocked: https://dev.to/deepak_mishra_35863517037/beyond-requests-why-your-python-scraper-is-already-blocked-id8
- ScrapeHero — Rate limiting in web scraping: https://www.scrapehero.com/rate-limiting-in-web-scraping/
- WordPress Trac — Disallow wp-json crawling ticket: https://core.trac.wordpress.org/ticket/36390
