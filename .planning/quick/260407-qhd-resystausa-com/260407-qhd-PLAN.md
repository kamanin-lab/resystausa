---
phase: quick
plan: 260407-qhd
type: execute
wave: 1
depends_on: []
files_modified:
  - .planning/quick/260407-qhd-resystausa-com/AUDIT-REPORT.md
autonomous: true
must_haves:
  truths:
    - "Every AJAX/admin-ajax.php call in backup HTML is catalogued"
    - "All external embeds (YouTube, maps, CDN) are identified"
    - "All WordPress plugin dependencies are listed with broken/working status"
    - "All downloadable files (PDF, CAD, DWG) are verified present or missing"
    - "A prioritized action list exists for what to scrape before access is lost"
  artifacts:
    - path: ".planning/quick/260407-qhd-resystausa-com/AUDIT-REPORT.md"
      provides: "Complete audit of dynamic content and missing assets"
      contains: "Priority"
---

<objective>
Comprehensive audit of the resystausa.com backup to identify all dynamic content, AJAX dependencies, external embeds, and missing assets that need scraping before the client loses access to the WordPress site.

Purpose: The static HTML backup may reference WordPress backend endpoints (admin-ajax.php, wp-json, CF7 forms, WooCommerce AJAX, cost calculator), external services (YouTube, Google Maps, CDNs), and downloadable files (PDFs, CAD/BIM) that are either broken or not yet captured. This audit produces a prioritized list of what still needs to be scraped/fixed.

Output: AUDIT-REPORT.md with categorized findings and priority actions.
</objective>

<execution_context>
@.planning/STATE.md
</execution_context>

<context>
Backup location: G:/01_OPUS/Projects/resystausa/resysta-backup/site/
Staging URL: https://site-nine-kappa-33.vercel.app/

Already fixed:
- reCAPTCHA scripts removed (no real functionality lost)
- Super Store Finder map replaced with static distributor cards (9 distributors from live SSF XML)

Known WordPress plugins to investigate: Contact Form 7 (CF7), ql-cost-calculator, WooCommerce, YITH Wishlist, Revolution Slider, Elementor.

The backup has 554 HTML files, 820 JPG, 218 PNG, 43 PDF, 5 JS files, plus CSS/fonts.
</context>

<tasks>

<task type="auto">
  <name>Task 1: Scan all backup HTML for AJAX calls, external dependencies, and plugin signatures</name>
  <files>.planning/quick/260407-qhd-resystausa-com/AUDIT-REPORT.md</files>
  <action>
Write and run a Python script that scans ALL 554 HTML files in G:/01_OPUS/Projects/resystausa/resysta-backup/site/ and extracts:

1. **AJAX endpoints**: grep for `admin-ajax.php`, `wp-json`, `wp-admin`, `action=` patterns in scripts and HTML. For each occurrence, record the file path, the full URL/action, and the context (which plugin/feature uses it).

2. **External embeds and dependencies**: grep for `iframe`, `youtube.com`, `youtu.be`, `google.com/maps`, `maps.googleapis.com`, `gstatic.com`, `cloudflare`, `cdn.`, `gravatar`, `facebook`, `twitter`, `instagram`, `vimeo`, external `src=` and `href=` pointing outside resystausa.com domain. Categorize as: video embeds, map embeds, social embeds, CDN assets, analytics/tracking, other.

3. **WordPress plugin signatures**: grep for known plugin patterns:
   - `wpcf7` or `contact-form-7` (Contact Form 7)
   - `ql-cost-calculator` or `qc-cost-calculator` (Cost Calculator)
   - `woocommerce` or `wc-` or `add-to-cart` (WooCommerce)
   - `yith` or `wishlist` (YITH Wishlist)
   - `revslider` or `revolution` (Revolution Slider)
   - `elementor` (Elementor)
   - `wpml` (WPML multilingual)
   - `super-store-finder` or `ssf` (already fixed)
   - `recaptcha` or `grecaptcha` (already removed)
   - Any other `wp-content/plugins/` references

4. **Downloadable file references**: grep for links to `.pdf`, `.dwg`, `.dxf`, `.zip`, `.doc`, `.xls`, `.csv`, `.bim`, `.rvt`, `.skp` files. For each referenced file, check if it actually exists in the backup directory. Report missing files.

5. **Form actions**: grep for `<form` elements and their `action=` attributes. Identify which forms POST to WordPress endpoints that will not work in static backup.

6. **WooCommerce product data**: check product pages for pricing data, add-to-cart buttons, variation selectors, stock status — anything that comes from WP database and may not be in static HTML.

7. **Blog post inventory**: count blog posts in backup, list all blog post URLs found.

8. **Portfolio inventory**: count portfolio items, list all portfolio URLs found.

For each finding, assess:
- CRITICAL: Data will be permanently lost if not scraped (e.g., calculator pricing data, product DB-only fields)
- HIGH: Feature is broken and needs replacement (e.g., contact form needs static alternative)
- MEDIUM: Content is missing from backup and should be fetched (e.g., missing PDFs)
- LOW: Cosmetic issue or acceptable loss (e.g., analytics scripts, login page)

Use Python with os.walk + regex (no external deps beyond stdlib). Process files in bulk. Output structured findings to stdout, then assemble into the final report.
  </action>
  <verify>
    <automated>python -c "import os; assert os.path.exists('G:/01_OPUS/Projects/resystausa/.planning/quick/260407-qhd-resystausa-com/AUDIT-REPORT.md'), 'Report not created'; content=open('G:/01_OPUS/Projects/resystausa/.planning/quick/260407-qhd-resystausa-com/AUDIT-REPORT.md').read(); assert 'Priority' in content, 'No priority section'; assert 'AJAX' in content or 'ajax' in content, 'No AJAX analysis'; assert len(content) > 2000, f'Report too short: {len(content)} chars'"</automated>
  </verify>
  <done>
AUDIT-REPORT.md exists with:
- Complete inventory of AJAX/backend dependencies found in backup HTML
- List of all external embeds (YouTube, maps, CDN) with URLs and hosting pages
- WordPress plugin dependency map with broken/working assessment
- Missing downloadable files (PDFs, CAD) with source pages
- Form inventory with action endpoints
- Blog and portfolio page counts
- Prioritized action list (CRITICAL / HIGH / MEDIUM / LOW) of what to scrape/fix before access is lost
  </done>
</task>

</tasks>

<verification>
- AUDIT-REPORT.md is comprehensive (covers all 8 audit categories)
- Every finding has a priority level assigned
- Missing files are identified with specific paths
- The report is actionable — a developer can use it to plan next scraping tasks
</verification>

<success_criteria>
- Single markdown report file produced at .planning/quick/260407-qhd-resystausa-com/AUDIT-REPORT.md
- Report covers: AJAX calls, external embeds, plugin dependencies, missing downloads, forms, WooCommerce data, blog inventory, portfolio inventory
- Each finding categorized by priority (CRITICAL/HIGH/MEDIUM/LOW)
- Report includes a summary section with top-priority action items
</success_criteria>

<output>
After completion, the AUDIT-REPORT.md serves as the deliverable. No SUMMARY needed for quick tasks.
</output>
