# resystausa.com Backup Audit Report

**Generated:** 2026-04-07
**Audit scope:** 554 HTML files in `G:/01_OPUS/Projects/resystausa/resysta-backup/site/`
**Purpose:** Identify dynamic content, AJAX dependencies, external embeds, and missing assets before WordPress access is permanently lost

---

## Executive Summary

The backup captures the **HTML structure and most visual content** of resystausa.com, but has significant gaps in downloadable technical files. Dynamic WordPress features (contact forms, AJAX, wishlist) will not function in static hosting, but the content itself is readable.

**Priority 1 action: Download 107 missing technical files** (50 PDFs + 54 DWG ZIPs + 3 DOCX) before losing WP access. These are the client's technical documentation — irreplaceable once the site goes offline.

**Known-fixed (skip):** reCAPTCHA removed from all pages. Super Store Finder replaced with static distributor cards.

---

## Table of Contents

1. [AJAX Endpoints and WordPress Backend Dependencies](#1-ajax-endpoints)
2. [External Embeds and CDN Dependencies](#2-external-embeds)
3. [WordPress Plugin Inventory](#3-wordpress-plugins)
4. [Missing Downloadable Files](#4-missing-downloadable-files)
5. [Form Inventory](#5-form-inventory)
6. [WooCommerce Product Data Assessment](#6-woocommerce-product-data)
7. [Blog Post Inventory](#7-blog-inventory)
8. [Portfolio Inventory](#8-portfolio-inventory)
9. [Priority Action List](#9-priority-action-list)

---

## 1. AJAX Endpoints

**Summary:** WordPress AJAX infrastructure is present in all 552 content pages via injected JavaScript configuration. All AJAX calls point to `https://resystausa.com/wp-admin/admin-ajax.php`. These will silently fail in a static backup, but do not cause page errors — they degrade gracefully since form submissions are handled via CF7 AJAX and wishlist via WooCommerce AJAX.

### Findings

| Pattern | Files Affected | Notes |
|---------|----------------|-------|
| `admin-ajax.php` | 552 | AJAX handler URL injected on every page |
| `wp-json/` | 552 | WP REST API URL injected on every page |
| `ajaxurl` variable | 552 | JS variable: `https://resystausa.com/wp-admin/admin-ajax.php` |
| `XMLHttpRequest / $.ajax()` | 552 | jQuery AJAX calls in plugin scripts |
| `fetch()` | 552 | Fetch API calls in plugin scripts |

### AJAX-dependent Features

| Feature | Plugin | Status in Backup | Priority |
|---------|--------|-----------------|----------|
| Contact Form 7 submission | `wpcf7` | BROKEN — form renders but POST to admin-ajax.php will fail | HIGH |
| Warranty Registration form | CF7 form ID 1005 | BROKEN — same AJAX POST issue | HIGH |
| Add to Wishlist | YITH WooCommerce Wishlist | BROKEN — AJAX call to add/remove wishlist items | LOW (cosmetic) |
| Add to Cart | WooCommerce | BROKEN — no real cart in static backup | LOW (ecom not live) |
| Cost Calculator | ql-cost-calculator | BROKEN — JS config loads but back-end calculation via AJAX fails | MEDIUM |
| Spam blocker (CF7 add-on) | `wp-contact-form-7-spam-blocker` | Not functional | LOW |

**Assessment:** Contact Form 7 forms are the primary user-facing AJAX dependency. They need a static replacement (Formspree, Netlify Forms, or similar) for the staging site to remain functional.

---

## 2. External Embeds and CDN Dependencies

### 2a. YouTube Video Embeds — WORKING (no action needed)

All 13 YouTube videos are embedded via `<iframe src="https://www.youtube.com/embed/...">` and will continue working as long as the visitor has internet access. All 13 are on the **Installation Guides & Videos** page (`installation-guides-videos-pdf-downloads/index.html`).

| Video ID | URL |
|----------|-----|
| CJBl2J4qr1g | https://www.youtube.com/watch?v=CJBl2J4qr1g |
| M0O3iGGqfPM | https://www.youtube.com/watch?v=M0O3iGGqfPM |
| MciIQpRGMMU | https://www.youtube.com/watch?v=MciIQpRGMMU |
| P_k2HhBAYs0 | https://www.youtube.com/watch?v=P_k2HhBAYs0 |
| SQwy1yUct1A | https://www.youtube.com/watch?v=SQwy1yUct1A |
| VSU7g3ZQbaU | https://www.youtube.com/watch?v=VSU7g3ZQbaU |
| eyPRIQBxFrQ | https://www.youtube.com/watch?v=eyPRIQBxFrQ |
| je5EfvHpJ5Y | https://www.youtube.com/watch?v=je5EfvHpJ5Y |
| nHn0gV99CXY | https://www.youtube.com/watch?v=nHn0gV99CXY |
| pLVOyqgUVAc | https://www.youtube.com/watch?v=pLVOyqgUVAc |
| qA1dTAqV-Ek | https://www.youtube.com/watch?v=qA1dTAqV-Ek |
| vnWwwnuwHqA | https://www.youtube.com/watch?v=vnWwwnuwHqA |
| z1NlaanO6bM | https://www.youtube.com/watch?v=z1NlaanO6bM |

### 2b. Google Maps Embeds — WORKING (no action needed)

| URL | Page |
|-----|------|
| `google.com/maps/embed?pb=...` (Rancho Cucamonga, CA) | `index.html` (homepage) |
| `google.com/maps/embed?pb=...` (Rancho Cucamonga, CA) | `contact-resysta-usa/index.html` |
| `google.com/maps/embed?pb=...` (same) | `what-is-resysta/warranty-registration/index.html` |

All 3 iframe Google Maps embeds will work indefinitely as long as the embed key is valid.

### 2c. Google Fonts — WORKING (no action needed)

`fonts.googleapis.com` and `fonts.gstatic.com` are loaded on all 552 pages. Will continue working as long as Google Fonts CDN is available.

### 2d. Social Platform Scripts — LOW RISK (cosmetic functionality broken)

| Service | Pages | Notes |
|---------|-------|-------|
| Facebook SDK | 552 | Facebook social sharing, like buttons — cosmetic |
| Twitter/X | 252 | Tweet buttons — cosmetic |
| Instagram | 552 | Instagram follow widgets — cosmetic |
| Google Analytics/GTM | 552 | Analytics tracking — no user-visible impact |
| Cloudflare Analytics (`cf-beacon`) | 23 | Cloudflare web analytics — not needed in backup |

### 2e. Public CDN Assets — ACTION NEEDED

| CDN | Files | Pages | Notes |
|-----|-------|-------|-------|
| `stackpath.bootstrapcdn.com` or similar | Present | 68 | Bootstrap CSS — should verify locally cached |
| `cdn.jsdelivr.net` / `cdnjs` | Present | 68 | JS libraries |

**Note:** If any of these CDN assets are NOT locally cached in `wp-content/`, they may fail to load offline. The backup uses `--convert-links` so most assets should be local. Verify by checking the offline rendering at `python -m http.server`.

### 2f. Resysta Course Page — No YouTube Embed

The `resysta-course/index.html` page only links to the YouTube channel (`youtube.com/@Rswdist-RESYSTA-North_America`) — it does not embed video content. The page has a CF7 contact form (form ID 30013) which will be broken.

---

## 3. WordPress Plugin Inventory

### Plugins Confirmed Active (via wp-content/plugins/ references)

| Plugin Slug | Pages | Status in Backup | Replacement Needed |
|-------------|-------|-----------------|-------------------|
| `contact-form-7` | 552 | BROKEN — AJAX POST fails | Yes — Formspree/Netlify Forms |
| `contact-form-7-image-captcha` | 552 | Broken (part of CF7) | No |
| `ql-cost-calculator` | 552 | BROKEN — JS loads, calculation backend fails | Possibly (see below) |
| `revslider` | 552 | Working — slider HTML is static | No |
| `woocommerce` | 552 | BROKEN — cart/checkout AJAX fails | No (client not doing ecom) |
| `yith-woocommerce-ajax-navigation` | 552 | BROKEN — filter AJAX fails | No |
| `yith-woocommerce-wishlist` | 552 | BROKEN — wishlist AJAX fails | No |
| `js_composer` (WP Bakery) | 552 | Working — layout rendered to static HTML | No |
| `easy-side-tab-pro` | 552 | Working — static HTML | No |
| `startup-framework` | 552 | Working — static HTML | No |
| `superstorefinder-wp` | 277 | REPLACED — static distributor cards | Done |
| `ulc` (custom ULC product plugin) | 552 | Partially working — see below | See notes |
| `wp-contact-form-7-spam-blocker` | 552 | Broken (CF7 addon) | No |
| `wp-rocket` | 110 | Not relevant in static backup | No |
| `grid-plus` | 6 | Working — grid rendered to static HTML | No |

### CF7 Form IDs Found

| Form ID | Page | Purpose |
|---------|------|---------|
| 1004 | `contact-resysta-usa/index.html` | Main contact form |
| 1005 | `what-is-resysta/warranty-registration/index.html` | Warranty registration (20+ fields) |
| 19875 | Most pages (sidebar/footer) | Newsletter / general inquiry |
| 22816 | `index.html` (homepage) | Homepage CTA form |
| 30013 | `resysta-course/index.html`, `aia-course-2.../index.html` | AIA Course registration |

### ULC Custom Plugin Assessment

The `ulc` plugin appears to be a custom plugin for ULC (Underwriters Laboratories Canada) certification data on product pages. It loads CSS from `wp-content/plugins/ulc/assets/css/font-awesome.min.css`. A prior task (`260407-q3u`) involved scraping ULC document links. The plugin data appears to be embedded statically in the HTML.

### Cost Calculator Assessment

The `ql-cost-calculator` plugin loads its CSS but the calculation engine runs server-side. The calculator form renders in HTML but submitting it will fail silently. The calculator is **sitewide** (all 552 pages include the plugin JS/CSS), meaning it's likely in the header/footer template, not a dedicated page widget.

**Action:** Check if the cost calculator has a dedicated page. If calculation logic is needed, it may need to be re-implemented as a client-side JS calculator.

---

## 4. Missing Downloadable Files

### Summary

| Type | Present | Missing | Total Referenced |
|------|---------|---------|-----------------|
| PDF (technical specs/drawings) | 44 | **50** | 94 |
| ZIP (DWG AutoCAD drawings) | 1 | **54** | 55 |
| ZIP (BIM Revit files) | 0 | **4** | 4 |
| DOCX (CSI specification docs) | 0 | **3** | 3 |
| **TOTAL** | **45** | **107** | **152** |

**CRITICAL: 107 files must be downloaded from the live site before access is lost.**

### Missing PDFs (50 files) — CRITICAL

These are product technical specification sheets and typical drawing detail PDFs. All are in `wp-content/uploads/`.

**Product spec sheets (per-product PDFs):**

| URL | Source Page |
|-----|------------|
| `.../2022/05/RESCPH120412.pdf` | `products/siding-4-profile-h/` |
| `.../2022/07/ButtJoint_Hor_Clad_BJHCD-210722.pdf` | `typical-drawing-details/` |
| `.../2022/08/AlumTrim_Hor_Sid_ATHSD-080822.pdf` | `typical-drawing-details/` |
| `.../2023/03/2CH_AL_Ver_Clad_UBrackket_2AL-VCUB-270223.pdf` | `typical-drawing-details/` |
| `.../2023/03/2CH_Ver_Clad_UBracket_2VCUB-270223.pdf` | `typical-drawing-details/` |
| `.../2023/03/2Ch_AL_Hor_Clad_UBracket_2AL-HCUB-270223.pdf` | `typical-drawing-details/` |
| `.../2023/03/2Ch_Hor_Clad_UBracket_2HCUB-270223.pdf` | `typical-drawing-details/` |
| `.../2023/03/4Ch_AL_Ver_Clad_UBracket_4AL-VCUB-280223.pdf` | `typical-drawing-details/` |
| `.../2023/03/4Ch_Hor_Clad_UBracket_4HCUB-270223.pdf` | `typical-drawing-details/` |
| `.../2023/03/4Ch_Ver_Clad_UBracket_4VCUB-270223.pdf` | `typical-drawing-details/` |
| `.../2023/03/AlumTrim_Hor_Clad_Det_ATHCD-030123.pdf` | `typical-drawing-details/` |
| `.../2023/03/AlumTrim_Ver_Clad_ATVCD-14022023.pdf` | `typical-drawing-details/` |
| `.../2023/03/AlumTrim_Ver_Sid_Det_ATVSD-030123.pdf` | `typical-drawing-details/` |
| `.../2023/03/ButtJoint_HorClad_HFLongClip_Det_BJHCD-LC-030123.pdf` | `typical-drawing-details/` |
| `.../2023/03/DeckingBoard_Det_DBD-030123.pdf` | `typical-drawing-details/` |
| `.../2023/03/RESCLIPHF100.pdf` | `products/facade-clip/` |
| `.../2023/03/RESCLIPS200.pdf` | `products/decking-clip/` |
| `.../2023/03/RESCLIPSS125.pdf` | `products/start-end-clip-ss1-2/` |
| `.../2023/03/RESCPH120612.pdf` | `products/siding-6-profile-h/` |
| `.../2023/03/RESCPSS25.pdf` | `products/siding-screw/` |
| `.../2023/03/RESDCH343412.pdf` | `products/deco-corner/` |
| `.../2023/03/RESDOWEL3.pdf` | `products/dowel/` |
| `.../2023/03/RESDP340612-1.pdf` | `products/6-deko-profile/` |
| `.../2023/03/RESGC11223412.pdf` | `products/cladding-2-channels-thick/` |
| `.../2023/03/RESGCI020612-1.pdf` | `products/cladding-4-channels-thick-al/` |
| `.../2023/03/RESGCI11223412.pdf` | `products/cladding-2-channels-thick-al/` |
| `.../2023/03/RESP1223412.pdf` | `products/cladding-2-channels-thin/` |
| `.../2023/03/RESP1231212.pdf` | `products/cladding-3-channels/` |
| `.../2023/03/RESP340612.pdf` | `products/cladding-4-channels/` |
| `.../2023/03/RESP340812.pdf` | `products/cladding-7-channels/` |
| `.../2023/03/RESP3423412.pdf` | `products/cladding-2-channels/` |
| `.../2023/03/RESRPH340312.pdf` | `products/rhombus-siding-profile/` |
| `.../2023/03/RESUB112234.pdf` | `products/aluminium-u-bracket/` |
| `.../2023/09/RESGC11211212.pdf` | `products/cladding-1-channel-thick/` |
| `.../2023/09/RESGCI11211212.pdf` | `products/cladding-1-channel-thick-al/` |
| `.../2024/08/ButtJoint_Ver_Clad_Det_BJVCD-310724.pdf` | `typical-drawing-details/` |
| `.../2024/08/RES010612-BE_Rev.1_150624.pdf` | `products/decking-board/` |
| `.../2024/08/RESF12812-1.pdf` | `products/fascia-board/` |
| `.../2024/08/RESLP340612.pdf` | `products/6-lusso-profile/` |
| `.../2024/08/RESSB010612.pdf` | `products/starter-board/` |
| `.../2024/09/1Ch_Hor_Clad_UBracket_1HCUB-200924_FN-1.pdf` | `typical-drawing-details/` |
| `.../2024/10/RESCLIPHFL100-pdf.pdf` | `typical-drawing-details/`, `products/facade-long-clip/` |
| `.../2025/10/RESGC020612.pdf` | `products/cladding-4-channels-thick/` |
| `.../2025/11/RESFB3411208-Fence-Bottom-Rail.pdf` | `products/fence-bottom-rail-resfb3411208/` |
| `.../2025/11/RESFI123408-Profile-Insert.pdf` | `products/fence-profile-insert-resfi123408/` |
| `.../2025/11/RESFP010608-Fence-Profile.pdf` | `products/composite-fence-profile-resfp010608/` |
| `.../2025/11/RESFP04040-fence-Post-with-Insert.pdf` | `products/fence-post-insert-profile-resfp04040/` |
| `.../2025/11/RESFPB11416-Fence-Post-Base.pdf` | `products/fence-post-base-resfpb11416/` |
| `.../2025/11/RESFT3411208-Fence-Top-Rail.pdf` | `products/fence-top-rail-resft3411208/` |
| `.../2025/12/RESCHP011208.pdf` | `products/siding-12-profile/` |

### Missing DWG ZIPs (54 files) — CRITICAL

Every product PDF has a corresponding `.dwg_.zip` (AutoCAD drawing files). Plus several typical drawing detail DWGs. All follow the same naming pattern as the PDFs with `.dwg_.zip` suffix.

| URL | Source Page |
|-----|------------|
| `.../2018/12/HybridDecking_Resysta-2016.rvt_.zip` | `cad-bim-and-csi/` |
| `.../2018/12/HybridDecking_Resysta-2017.rvt_.zip` | `cad-bim-and-csi/` |
| `.../2018/12/HybridDecking_Resysta-2018.rvt_.zip` | `cad-bim-and-csi/` |
| `.../2018/12/Materials_Resysta.zip` | `cad-bim-and-csi/` |
| `.../2022/05/RESCPH120412.dwg_.zip` | `products/siding-4-profile-h/` |
| `.../2022/07/ButtJoint_Hor_Clad_BJHCD-210722.dwg_.zip` | `typical-drawing-details/` |
| `.../2022/09/AlumTrim_Hor_Sid_ATHS-080822.dwg_.zip` | `typical-drawing-details/` |
| *(+ 47 more DWG ZIPs with same pattern as PDF list)* | Various product pages |
| `.../2025/11/RESFB3411208.zip` | `products/fence-bottom-rail-resfb3411208/` |
| `.../2025/11/RESFI123408.zip` | `products/fence-profile-insert-resfi123408/` |
| `.../2025/11/RESFP010608.zip` | `products/composite-fence-profile-resfp010608/` |
| `.../2025/11/RESFP04040.zip` | `products/fence-post-insert-profile-resfp04040/` |
| `.../2025/11/RESFPB11416.zip` | `products/fence-post-base-resfpb11416/` |
| `.../2025/11/RESFT3411208.zip` | `products/fence-top-rail-resft3411208/` |
| `.../2025/12/RESCHP011208.zip` | `products/siding-12-profile/` |

### Missing DOCX (3 files) — CRITICAL

CSI specification documents for Resysta products. Referenced from `cad-bim-and-csi/index.html`.

| URL |
|-----|
| `https://resystausa.com/wp-content/uploads/2023/05/07460resR10.docx` |
| `https://resystausa.com/wp-content/uploads/2025/03/06603truR18-1-1.docx` |
| `https://resystausa.com/wp-content/uploads/2025/03/06730truR18.docx` |

### Download Script

To download all 107 missing files, use the following wget command pattern (bypass Cloudflare via direct IP):

```bash
# Create a list of all 107 missing file URLs and batch-download them
wget --no-check-certificate \
  --header="Host: resystausa.com" \
  --header="User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36" \
  --wait=1 --random-wait \
  -P "resysta-backup/site/wp-content/uploads/" \
  --cut-dirs=3 \
  -i missing-files.txt \
  --base=http://74.208.236.61/
```

---

## 5. Form Inventory

### Active CF7 Forms

| Form | Page | Fields | AJAX Action | Status |
|------|------|--------|-------------|--------|
| General inquiry (ID: 19875) | ~107 pages (footer/sidebar) | Email, message | `wpcf7_submit` | BROKEN |
| Homepage CTA (ID: 22816) | `index.html` | Name, email, message | `wpcf7_submit` | BROKEN |
| Contact us (ID: 1004) | `contact-resysta-usa/index.html` | Full contact fields | `wpcf7_submit` | BROKEN |
| Warranty registration (ID: 1005) | `what-is-resysta/warranty-registration/` | 20+ fields (name, address, product, date, warranty type) | `wpcf7_submit` | BROKEN |
| Course registration (ID: 30013) | `resysta-course/`, `aia-course-2-beyond-straight-level-facades/` | Name, phone, email, company, address | `wpcf7_submit` | BROKEN |

### WooCommerce Search Forms

All `<form action="../../index.html">` patterns are WooCommerce product search/filter forms. These resolve to the site root, which means they work as regular navigation, but the AJAX filtering won't function.

### Wishlist "Forms"

Many forms have actions like `index.html@add_to_wishlist=XXXX&_wpnonce=YYYYYY.html` — these are YITH Wishlist URL-encoded actions captured as separate HTML files by wget. They are non-functional artifacts of the scrape. Total count: ~570 wishlist variant files.

---

## 6. WooCommerce Product Data

### Product Page Assessment

**36 individual product pages** are captured in `products/[slug]/index.html`. Each page contains:
- Product images (static — present in backup)
- Product name and description (static HTML)
- Technical specifications table (static HTML)
- PDF and DWG download links (pointing to wp-content/uploads — **107 files missing**)
- Price display (HTML rendered at scrape time — preserved)
- SKU/product code (static HTML)
- "Add to Cart" button (BROKEN — AJAX call to WooCommerce cart)
- "Add to Wishlist" button (BROKEN — AJAX call to YITH wishlist)

### Product Category Pages

7 product category pages in `product/[category]/`:

| Category | HTML Files |
|----------|-----------|
| `product/decking/` | 7 |
| `product/fencing-boards/` | 8 |
| `product/screen-walls/` | 9 |
| `product/siding/` | 9 |
| `product/soffit-and-ceilings/` | 6 |
| `product/trellis/` | 9 |
| `product/wall-cladding/` | 32 |

The extra HTML files per category are wishlist URL variants (non-functional artifacts).

### WooCommerce Features Status

| Feature | Status | Notes |
|---------|--------|-------|
| Product page content | WORKING | All text, images, specs captured |
| Product pricing | WORKING | Prices rendered in HTML at scrape time |
| Product images | WORKING | Present in backup |
| Add to cart | BROKEN | WooCommerce AJAX — not relevant (client not running ecom) |
| Product variations | BROKEN | AJAX-driven — variation data may be incomplete |
| Cart/Checkout | BROKEN | Dynamic — not functional in static backup |
| My Account | BROKEN | Dynamic — only login form renders |
| Stock status | Present in HTML | Values shown in backup but not real-time |

---

## 7. Blog Inventory

### Status

**Blog posts: 0 individual post pages in backup.**

The blog is severely under-captured:
- `blog/index.html` exists (232KB file — indicates the blog was scraped)
- The index page contains **1 article element** (`post-30348`) — only 1 post visible on the index page
- Blog post subdirectory pages: **0** (no `blog/[post-slug]/index.html` files)
- Wayback archive: **empty** (wayback directory is empty, 0 files)

### Why Posts Are Missing

The wget crawl likely did not follow the `?page_id=` or individual post URLs from the blog index. The blog index page at `blog/index.html` shows posts via JavaScript-enhanced pagination or the posts were fetched via AJAX after page load (common in WordPress themes with lazy-loading post grids).

Additionally, the blog index `href` links all point to `resystausa.com` domain (not relative paths), which wget may have treated as external if the base URL differed slightly.

### Blog Post Count on Live Site

From the blog index, 61 elements with `class` containing `type-post` suggest **~61 blog posts** on the live site, none of which are captured individually.

### Recommendation

**MEDIUM priority:** Scrape blog posts before access is lost. Use `curl` on the CDX API to enumerate all blog post URLs, then use wget or Python scraper to download each.

```bash
# Get all archived blog post URLs from Wayback CDX
curl "http://web.archive.org/cdx/search/cdx?url=resystausa.com/blog/*/&output=text&fl=original&collapse=urlkey&limit=200" | sort -u
```

---

## 8. Portfolio Inventory

### Status: COMPLETE (29 portfolio items captured)

All portfolio project pages are present in the backup.

| Slug | Page |
|------|------|
| 5-star-er-pfugerville | ER facility, Pflugerville TX |
| avoin-complex | Commercial complex |
| chick-fil-a | Chick-fil-A restaurant |
| chick-fil-a-florida | Chick-fil-A Florida |
| cowlitz-tribal-casino-ridgefield | Casino, Ridgefield WA |
| decking-in-san-diego | Residential decking |
| exclusive-private-residence-in-los-angeles | Private residence, LA |
| fire-station-3-pleasanton-ca | Fire station, Pleasanton CA |
| fire-stone-grill | Restaurant |
| five-on-black-south-24th-street-west-billings-mt | Billings MT |
| gallery-row-tucson-az | Tucson AZ |
| hotel-palace-station-las-vegas | Hotel, Las Vegas |
| metlife-symphony-tower-llc | Office tower |
| new-cinema-sacramento | Cinema, Sacramento |
| nursery-building | Nursery |
| office-building | Office building |
| panda-express-restaurant-in-los-angeles | Restaurant, LA |
| parkgarage-in-fremont-ca | Parking garage |
| private-apartements-menlo-park-california | Menlo Park CA |
| private-house | Private house |
| private-lusso-puerto_rico | Puerto Rico |
| private-residence-california | California |
| residential-san-francisco | San Francisco |
| resysta-decking-carlsbad | Carlsbad |
| shack-shake | Shake Shack variant |
| starbucks-tigard-or | Starbucks, Tigard OR |
| timbers-kiawah-resort | Resort |
| twinstar-credit-union-aberdeen | Credit union |
| wall-cladding-raleys-supermarket | Supermarket |

**Portfolio categories captured (5):** decking, lusso, novano-resysta, siding, wall-cladding

---

## 9. Priority Action List

### CRITICAL — Do immediately before WP access is lost

| # | Action | Files | Pages | Effort |
|---|--------|-------|-------|--------|
| C1 | Download 50 missing PDF product spec sheets and typical drawing PDFs | 50 PDFs | `products/`, `typical-drawing-details/` | 1-2 hours |
| C2 | Download 54 missing DWG AutoCAD drawing ZIPs | 54 ZIPs | Same pages | 1-2 hours |
| C3 | Download 3 missing CSI DOCX specification documents | 3 DOCXs | `cad-bim-and-csi/` | 15 min |
| C4 | Download 4 missing Revit BIM ZIPs (HybridDecking 2016/2017/2018, Materials) | 4 ZIPs | `cad-bim-and-csi/` | 15 min |

**Fastest approach for C1-C4:** Extract all 107 missing URLs into a file and use wget batch download via IP bypass.

### HIGH — Fixes needed for staging site to be useful

| # | Action | Impact | Effort |
|---|--------|--------|--------|
| H1 | Replace Contact Form 7 with static form service (Formspree, Netlify Forms) | Contact form `contact-resysta-usa/` stops working | 2-4 hours |
| H2 | Replace Warranty Registration form (20+ fields, ID 1005) with static equivalent | Warranty signups broken | 2-4 hours |
| H3 | Replace AIA Course registration form (ID 30013) | Course signups broken | 1-2 hours |
| H4 | Replace general inquiry form (ID 19875, sitewide in footer) | General contact broken sitewide | 2 hours |

### MEDIUM — Content recovery before access loss

| # | Action | Details | Effort |
|---|--------|---------|--------|
| M1 | Scrape all ~61 blog posts individually | No blog posts in backup; CDX API can enumerate them | 2-4 hours |
| M2 | Audit cost calculator functionality | Determine if server-side calculation is needed or can be replaced with client-side JS | 2 hours |
| M3 | Verify CDN assets load offline | Test `python -m http.server` on backup and check for 404 CDN assets | 1 hour |
| M4 | Remove broken wishlist/cart buttons from product pages | 570+ wishlist URL-variant HTML files, broken "Add to Wishlist" / "Add to Cart" buttons | 3-4 hours |

### LOW — Cosmetic / non-critical

| # | Action | Details |
|---|--------|---------|
| L1 | Remove social tracking scripts (GA, GTM, Cloudflare analytics) | Reduce page weight, privacy — all 552 pages |
| L2 | Remove Facebook/Twitter/Instagram share widget scripts | Non-functional in static — cosmetic clutter |
| L3 | Clean up 570+ wishlist URL-variant HTML files from backup | Artifact files like `index.html@add_to_wishlist=1508&_wpnonce=30d39e5412.html` |
| L4 | Verify Google Maps embeds still work | 3 maps on contact/homepage/warranty pages — should be fine |
| L5 | Test offline rendering | Run `python -m http.server 8080` in backup dir and verify pages render correctly |

---

## Appendix: Site Structure Summary

| Section | HTML Files | Notes |
|---------|-----------|-------|
| `products/` | 357 | Includes 36 individual products + 7 category pages + wishlist variants |
| `product/` | 80 | Alternate product category URLs (7 categories) |
| `portfolio/` | 30 | 29 project pages + index |
| `portfolio-category/` | 5 | Category indexes |
| `wall-cladding-profiles/` | 16 | Includes wishlist variants |
| `screen-wall-dividers/` | 9 | Includes wishlist variants |
| `trellis-canopy/` | 9 | Includes wishlist variants |
| `siding-profiles/` | 9 | Includes wishlist variants |
| `soffits-ceilings/` | 6 | Includes wishlist variants |
| `decking-profiles-and-boards/` | 7 | Includes wishlist variants |
| `what-is-resysta/` | 3 | Index + care-and-cleaning + warranty-registration |
| `why-resysta/` | 2 | Index + FAQ |
| `blog/` | 1 | Index only — 0 individual posts |
| Other pages | ~25 | Homepage, contact, find-a-distributor, AIA course, installation guides, etc. |

**Total: 554 HTML files** (many are wishlist URL variant duplicates — not actual unique pages)

---

*Audit completed: 2026-04-07*
*Scripts used: Python stdlib (pathlib, re, collections) — no external dependencies*
