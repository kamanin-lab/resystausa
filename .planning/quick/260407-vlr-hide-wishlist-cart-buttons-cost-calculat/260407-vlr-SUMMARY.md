---
phase: quick-260407-vlr
plan: "01"
subsystem: site-cleanup
tags: [css-injection, script-removal, woocommerce, tracking, idempotent]
dependency_graph:
  requires: []
  provides: [cleanup-site.py, css-hidden-ecommerce-ui, tracking-scripts-removed]
  affects: [resysta-backup/site/**/*.html]
tech_stack:
  added: []
  patterns: [css-injection-via-marker, regex-script-removal, idempotent-file-patching]
key_files:
  created:
    - resysta-backup/cleanup-site.py
  modified:
    - resysta-backup/site/**/*.html (607 files)
decisions:
  - Used comment-block regex (<!-- Meta Pixel Code --> ... <!-- End Meta Pixel Code -->) as primary FB Pixel removal pattern — more reliable than matching the IIFE body alone
  - Preserved Wayback Machine-wrapped googletagmanager.com links (web.archive.org/...googletagmanager.com) as benign archive artifacts — only direct DNS prefetch hints are removed
  - Switched script_result to content-diff-based counting so idempotency counter accurately reflects actual file changes rather than signature-presence checks
metrics:
  duration_minutes: 25
  completed_date: "2026-04-07"
  tasks_completed: 2
  tasks_total: 2
  files_created: 1
  files_modified: 607
---

# Phase quick-260407-vlr Plan 01: Cleanup Site Summary

**One-liner:** Idempotent Python script injects CSS hide rules for WooCommerce wishlist/cart/calculator and strips Facebook Pixel, GTM, and Cloudflare beacon scripts from all 607 archived HTML files.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Write resysta-backup/cleanup-site.py | `076bf9a` (parent), `06310d7` (site) | cleanup-site.py + 607 .html files |
| 2 | Commit cleanup script and processed site files | `076bf9a` / `06310d7` | — |

## Verification Results

| Check | Result |
|-------|--------|
| `fbq(` remaining in site/ | 0 files |
| `data-cf-beacon` remaining in site/ | 0 files |
| `gsd:cleanup-site` marker present | 607 files |
| `googletagmanager` in site/ | 54 files (all benign web.archive.org wrappers) |
| Script idempotent (3rd run) | 0 patched, 609 already-clean |

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Facebook Pixel regex did not match actual HTML structure**
- **Found during:** Task 1 verification
- **Issue:** The plan's regex required `!function(f,b,e,v,n,t,s)` and `fbq('track', 'PageView')` in the same `<script>` tag. The actual pages use 3 separate script tags: (1) the IIFE fbevents.js loader, (2) fbq('set')/fbq('init') calls, (3) fbq('track', 'PageView') call. The combined pattern never matched.
- **Fix:** Added `RE_FB_PIXEL_BLOCK` (comment-wrapper pattern), `RE_FB_PIXEL_LOADER` (IIFE only), and `RE_FB_FBQ_CALLS` (any script calling fbq init/set/track). Removed the non-matching combined pattern.
- **Files modified:** resysta-backup/cleanup-site.py

**2. [Rule 1 - Bug] GTM regex did not match inline IIFE pattern**
- **Found during:** Task 1 verification
- **Issue:** The plan's `RE_GTM_INLINE` targeted `window.dataLayer = window.dataLayer` (GA4 config), but the actual GTM script uses `(function(w,d,s,l,i){w[l]=w[l]||[]...gtm.js...})(...)` — a different IIFE form. Also added `RE_GTM_COMMENT_BLOCK` to handle the HTML-comment-wrapped block and `RE_GTAG_EVENT` for inline `gtag('event', ...)` conversion calls.
- **Fix:** Added `RE_GTM_COMMENT_BLOCK`, `RE_GTM_IIFE`, and `RE_GTAG_EVENT` patterns in addition to the original `RE_GTM_DATALAYER`.
- **Files modified:** resysta-backup/cleanup-site.py

**3. [Rule 1 - Bug] DNS prefetch regex missed protocol-relative `//` form**
- **Found during:** Task 1 verification (1 remaining file after initial run)
- **Issue:** The plan's regex required `https?://` prefix, but one file used `<link rel='dns-prefetch' href='//www.googletagmanager.com' />` (protocol-relative).
- **Fix:** Updated `RE_DNS_PREFETCH` to match `(?:https?:)?//` with a negative lookahead `(?!web\.archive\.org)` to exclude Wayback Machine-wrapped archive URLs that benignly contain the domain string.
- **Files modified:** resysta-backup/cleanup-site.py

**4. [Rule 1 - Bug] Idempotency counter reported false positives**
- **Found during:** Idempotency verification run
- **Issue:** 54 files containing Wayback Machine URLs with `googletagmanager` string triggered `needs_script_removal=True` but no regex actually changed content. These were counted as "cleaned" on every run.
- **Fix:** Added `pre_script_content` snapshot; only set `script_result = "cleaned"` when `content != pre_script_content`.
- **Files modified:** resysta-backup/cleanup-site.py

## Known Stubs

None — all CSS and script removals are fully wired.

## Self-Check

- [x] `resysta-backup/cleanup-site.py` exists
- [x] Site sub-repo commit `06310d7` visible in git log
- [x] Parent repo commit `076bf9a` visible in git log
- [x] 607 HTML files contain `gsd:cleanup-site` marker
- [x] 0 HTML files contain `fbq(` or `data-cf-beacon`
- [x] Script idempotent: third run shows 0 patched + 609 already-clean

## Self-Check: PASSED
