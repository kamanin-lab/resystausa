---
phase: quick
plan: 260407-q3u
subsystem: site-html
tags: [scraping, static-html, distributor, ssf-plugin, wordpress]
dependency_graph:
  requires: []
  provides: [find-a-distributor/index.html, find-a-distributor/distributors.json]
  affects: [find-a-distributor page on Vercel staging]
tech_stack:
  added: []
  patterns: [Python requests + direct IP bypass, CSS Grid responsive cards]
key_files:
  created:
    - resysta-backup/site/find-a-distributor/distributors.json
  modified:
    - resysta-backup/site/find-a-distributor/index.html
decisions:
  - Scraped SSF XML from PHP endpoint (ssf-wp-xml.php) via direct IP bypass — returns all store data without JS execution
  - Used CSS Grid (not Bootstrap) for cards since page already had Bootstrap but CSS Grid is self-contained and simpler
  - Left original SSF CSS style block in <head> (harmless inert CSS with no matching DOM elements)
  - Font Awesome icons retained from existing FA load (SSF CSS still links it)
metrics:
  duration: "~15 minutes"
  completed: "2026-04-07"
  tasks_completed: 2
  files_modified: 2
---

# Quick Task 260407-q3u: Find a Distributor — Replace SSF Widget with Static Cards

**One-liner:** Scraped 9 distributors from SSF plugin's XML endpoint via direct IP bypass and replaced the broken WordPress map widget with a responsive 3-column CSS Grid card layout using the site's green #7baa20 accent color.

## What Was Done

**Task 1 — Scrape distributor data (commit: 1cc7c66)**

- Attempted AJAX actions against `/wp-admin/admin-ajax.php` — all returned `0` (not found)
- Discovered SSF plugin stores data in `ssf-wp-xml.php` (a PHP endpoint generating XML), loaded via jQuery AJAX GET in `mega-superstorefinder.js`
- Fetched `http://74.208.236.71/wp-content/plugins/superstorefinder-wp/ssf-wp-xml.php?wpml_lang=&t=1` via direct IP bypass with Host header
- Parsed 9 distributor entries from XML (`<item>` elements inside `<locator>`)
- Normalized addresses (whitespace), decoded HTML entities (`&#44;` → comma)
- Saved to `find-a-distributor/distributors.json`

**Distributors captured:**
1. all green - Building products distribution (Chino, CA)
2. HDG Building Materials, LLC (Camas, WA)
3. Los Portales de Madeco, Inc. (San Juan, PR)
4. North Country Distributors (Osseo, MN)
5. Pacific American Lumber (Honolulu, HI)
6. RE-PLAST ECO (Notre-Dame-du Bon-Conseil, QC, Canada)
7. RSW Colombia (Bogota, Colombia)
8. Sustain Built Supply, Inc. (Marysville, WA)
9. VAMO Building Products Corp. (Surrey, BC, Canada)

**Task 2 — Replace SSF widget with static cards (commit: 11e4bec)**

- Replaced the entire SSF block (12,578 chars) from `<div id='ssf-dummy-blck'` through the two contact form popup divs (`modernBrowserPopup`, `modernBrowserConatct`)
- Inserted self-contained `<style>` block + distributor cards HTML
- All 9 distributors rendered as cards with: company name (green heading), address, phone (tel: link), website (external link), email (mailto: link), service categories
- Responsive CSS Grid: 3 columns desktop (992px+), 2 columns tablet (768-991px), 1 column mobile

## Verification Results

| Check | Result |
|-------|--------|
| ssf-dummy-blck removed | PASS |
| ssf-preloader removed | PASS |
| ssf-overlay removed | PASS |
| modernBrowserPopup removed | PASS |
| modernBrowserConatct removed | PASS |
| distributor-cards container present | PASS |
| distributor-grid container present | PASS |
| 9 distributor cards in HTML | PASS |
| #7baa20 green accent in CSS | PASS |
| Footer structure intact | PASS |
| Header structure intact | PASS |
| article/entry-content intact | PASS |
| Font Awesome icons (fa-map-marker, fa-phone, etc.) | PASS |
| tel: links present | PASS |
| mailto: links present | PASS |
| target="_blank" website links | PASS |

## Deviations from Plan

### Auto-fixed Issues

None — plan executed as written.

### Notes

**ssf-contact-form in CSS:** The original page had an inline SSF `<style>` block in the `<head>` containing CSS rules targeting `#ssf-contact-form`. This block was left in place per plan guidance ("harmless if left"). No actual `<form id="ssf-contact-form">` DOM element exists in the updated page — the CSS selector is inert. Verification check for `ssf-contact-form` not present in HTML is technically a false alarm (it's in a CSS rule, not HTML markup).

**AJAX approach:** Plan's primary approach tried AJAX actions — these returned `0` because SSF's data is served via a direct XML PHP endpoint, not a WP AJAX action. The fallback "Direct HTTP to origin IP" approach succeeded immediately on the first try.

## Known Stubs

None — all 9 distributor cards contain real scraped data from the live site.

## Threat Flags

None — static HTML modification only, no new endpoints or trust boundaries introduced.

## Self-Check: PASSED

- `resysta-backup/site/find-a-distributor/distributors.json` — exists, 9 entries
- `resysta-backup/site/find-a-distributor/index.html` — updated, 9 cards, SSF removed
- Commit 1cc7c66 — verified in git log
- Commit 11e4bec — verified in git log
