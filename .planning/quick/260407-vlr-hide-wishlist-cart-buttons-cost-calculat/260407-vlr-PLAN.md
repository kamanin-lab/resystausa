---
phase: quick-260407-vlr
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - resysta-backup/cleanup-site.py
autonomous: true
requirements:
  - hide-wishlist-buttons
  - hide-cart-buttons
  - hide-cost-calculator
  - remove-social-tracking-scripts
must_haves:
  truths:
    - "No wishlist heart-icon buttons visible on any page"
    - "No Add to Cart buttons visible on product listing or single-product pages"
    - "Cost calculator widget is hidden sitewide"
    - "Facebook Pixel, Google Analytics/GTM, and Cloudflare beacon scripts are absent from all HTML files"
    - "DNS prefetch hints for tracking domains are removed"
    - "Script is idempotent — safe to re-run without double-injecting CSS or corrupting HTML"
  artifacts:
    - path: "resysta-backup/cleanup-site.py"
      provides: "Python script that injects CSS hide rules and strips social tracking scripts from all 607 HTML files"
  key_links:
    - from: "resysta-backup/cleanup-site.py"
      to: "resysta-backup/site/**/*.html"
      via: "os.walk recursive file pass"
      pattern: "os.walk.*site"
---

<objective>
Extend the static-site cleanup tooling to hide WooCommerce wishlist/cart buttons and
the cost calculator widget, and completely remove Facebook Pixel, Google Analytics/GTM,
Cloudflare beacon, and related DNS prefetch tags from all 607 archived HTML files.

Purpose: The static backup must not show broken e-commerce UI or fire live tracking
pixels when viewed offline or hosted on a staging server.

Output: `resysta-backup/cleanup-site.py` — an idempotent Python script that processes
all `.html` files under `resysta-backup/site/` in a single pass.
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/execute-plan.md
@$HOME/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@resysta-backup/hide-forms.py

<!-- Existing pattern reference (from CLAUDE.md CONVENTIONS):
  - Marker: <!-- gsd:hide-forms -->
  - Strategy: inject <style> block before </head>, skip if marker present (idempotent)
  - SITE_DIR = os.path.join(os.path.dirname(__file__), "site")
  - Skip dirs: wp-admin, cdn-cgi
  - New script uses marker <!-- gsd:cleanup-site --> for CSS; regex presence checks for script removal
-->
</context>

<tasks>

<task type="auto">
  <name>Task 1: Write resysta-backup/cleanup-site.py</name>
  <files>resysta-backup/cleanup-site.py</files>
  <action>
Create `G:/01_OPUS/Projects/resystausa/resysta-backup/cleanup-site.py` following the
exact structure of hide-forms.py. The script performs two independent passes over each
HTML file in a single read:

**Pass A — CSS injection (idempotent via marker `<!-- gsd:cleanup-site -->`):**

Inject the following `<style>` block immediately before `</head>` on files that do NOT
already contain the marker `<!-- gsd:cleanup-site -->`. Only process files that contain
at least one of: `yith-wcwl`, `ajax_add_to_cart`, `single_add_to_cart_button`,
`costCalculator`, `ql-cost-calculator`.

CSS block to inject:
```html
<!-- gsd:cleanup-site -->
<style>
/* Hide WooCommerce wishlist buttons */
.yith-wcwl-add-button { display: none !important; }
.yith-wcwl-add-to-wishlist { display: none !important; }
/* Hide WooCommerce cart buttons */
.ajax_add_to_cart { display: none !important; }
.single_add_to_cart_button { display: none !important; }
/* Hide cost calculator widget */
#costCalculator { display: none !important; }
.ql-cost-calculator { display: none !important; }
</style>
```

**Pass B — Social tracking script removal (idempotent via absence check):**

For each file, check if it still contains tracking signatures. If the signatures are
absent (already removed on a previous run), skip the regex passes. Apply ALL four
removals in sequence on the file content before writing:

1. **Facebook Pixel inline script** — remove the entire `<script>` tag whose content
   matches the pattern `!function\(f,b,e,v,n,t,s\)` through its closing `</script>`.
   Use `re.DOTALL` flag. Pattern (multiline):
   `r'<script[^>]*>\s*!function\(f,b,e,v,n,t,s\)[\s\S]*?fbq\(\'track\',\s*\'PageView\'\)[\s\S]*?</script>'`

2. **Facebook noscript pixel** — remove the `<noscript>` tag containing
   `facebook.com/tr?id=`. Pattern:
   `r'<noscript>\s*<img[^>]*facebook\.com/tr\?id=[^>]*>\s*</noscript>'`

3. **Google Tag Manager / GA4** — remove both the external GTM script tag AND the
   inline `dataLayer` script block. Two regex passes:
   - External: `r'<script[^>]*src=["\'][^"\']*googletagmanager\.com/gtag/js[^"\']*["\'][^>]*></script>'`
   - Inline dataLayer: `r'<script[^>]*>\s*window\.dataLayer\s*=\s*window\.dataLayer[\s\S]*?</script>'`

4. **Cloudflare beacon** — remove the `<script>` tag containing `beacon.min.js` with
   `data-cf-beacon` attribute. Pattern:
   `r'<script[^>]*data-cf-beacon[^>]*></script>'`

5. **DNS prefetch hints** — remove `<link>` tags where `href` contains
   `connect.facebook.net` or `www.googletagmanager.com`. Pattern:
   `r'<link[^>]*href=["\']https?://(connect\.facebook\.net|www\.googletagmanager\.com)[^"\']*["\'][^>]*/?>'`

Idempotency for Pass B: at the top of the file processing function, set a flag
`needs_script_removal = ("fbq(" in content or "googletagmanager" in content or
"data-cf-beacon" in content)`. Only run the regex passes if this flag is True.

**Output counts to print:**
- Files scanned (total .html)
- Files CSS-patched (Pass A applied)
- Files already CSS-patched (marker present, skipped Pass A)
- Files script-cleaned (Pass B applied)
- Files already script-clean (no tracking signatures found)
- Files skipped entirely (no relevant content for either pass)
- Files with no `</head>` tag (warn, skip CSS injection)

**File encoding:** `utf-8`, `errors="replace"` (same as hide-forms.py).
**Skip dirs:** `wp-admin`, `cdn-cgi` (same exclusions as hide-forms.py).
**SITE_DIR:** `os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")`
  — use `os.path.abspath` so the script runs correctly regardless of cwd.
  </action>
  <verify>
    <automated>cd "G:/01_OPUS/Projects/resystausa" && python resysta-backup/cleanup-site.py</automated>
  </verify>
  <done>
Script runs without errors and prints a summary showing: scanned count ~607, CSS-patched
+ already-CSS-patched = scanned, script-cleaned + already-script-clean = scanned.
Spot-check: open `resysta-backup/site/index.html` in a text editor and confirm
`<!-- gsd:cleanup-site -->` marker is present, `fbq(` is absent, and GTM script tags
are absent.
  </done>
</task>

<task type="auto">
  <name>Task 2: Commit cleanup script and processed site files</name>
  <files>resysta-backup/cleanup-site.py</files>
  <action>
Stage and commit in the site sub-repo at `G:/01_OPUS/Projects/resystausa/resysta-backup/site/`:

```bash
cd "G:/01_OPUS/Projects/resystausa/resysta-backup/site"
git add -A
git commit -m "feat(quick-260407-vlr): hide wishlist/cart/calculator, remove social tracking scripts"
```

Then in the parent repo at `G:/01_OPUS/Projects/resystausa/`:

```bash
cd "G:/01_OPUS/Projects/resystausa"
git add resysta-backup/cleanup-site.py
git commit -m "feat(quick-260407-vlr): add cleanup-site.py script"
```

If either repo is not initialised (no `.git`), skip that commit and note it in the
summary.
  </action>
  <verify>
    <automated>cd "G:/01_OPUS/Projects/resystausa/resysta-backup/site" && git log --oneline -3 2>/dev/null || echo "no git repo"</automated>
  </verify>
  <done>
Commit visible in `git log --oneline` with message matching
`feat(quick-260407-vlr): hide wishlist/cart/calculator, remove social tracking scripts`,
OR a note that the repo is not yet initialised.
  </done>
</task>

</tasks>

<verification>
Run the script and grep for residual tracking signatures in the site directory:

```bash
# Should return 0 matches
grep -rl "fbq(" "G:/01_OPUS/Projects/resystausa/resysta-backup/site/" | wc -l
grep -rl "googletagmanager" "G:/01_OPUS/Projects/resystausa/resysta-backup/site/" | wc -l
grep -rl "data-cf-beacon" "G:/01_OPUS/Projects/resystausa/resysta-backup/site/" | wc -l

# Should return >0 matches (CSS marker present)
grep -rl "gsd:cleanup-site" "G:/01_OPUS/Projects/resystausa/resysta-backup/site/" | wc -l
```
</verification>

<success_criteria>
- `cleanup-site.py` exists at `resysta-backup/cleanup-site.py` and runs without errors
- All 607 HTML files have been processed in a single pass
- Zero HTML files contain `fbq(`, `googletagmanager`, or `data-cf-beacon` after the run
- Files that contained WooCommerce wishlist/cart/calculator classes have the
  `<!-- gsd:cleanup-site -->` CSS marker injected before `</head>`
- Script is idempotent: a second run produces identical output files and reports
  "already patched" / "already clean" for all files
</success_criteria>

<output>
After completion, create `.planning/quick/260407-vlr-hide-wishlist-cart-buttons-cost-calculat/260407-vlr-SUMMARY.md`
</output>
