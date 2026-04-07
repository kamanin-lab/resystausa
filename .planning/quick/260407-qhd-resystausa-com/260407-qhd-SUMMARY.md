---
phase: quick
plan: 260407-qhd
subsystem: backup-audit
tags: [audit, backup, wordpress, missing-assets]
key-files:
  created:
    - .planning/quick/260407-qhd-resystausa-com/AUDIT-REPORT.md
decisions:
  - Audit is read-only — no HTML files modified
  - Python stdlib only (no external deps) for maximum portability
metrics:
  duration: ~45 minutes
  completed: 2026-04-07
  tasks: 1
  files: 1
---

# Phase quick Plan 260407-qhd: Backup Audit Summary

**One-liner:** Comprehensive scan of 554 HTML files revealed 107 missing technical files (50 PDFs + 54 DWG ZIPs + 3 DOCX), 5 broken CF7 forms needing replacement, and 0 of ~61 blog posts captured.

## What Was Done

Ran Python scripts against all 554 HTML files in the backup to systematically audit:

1. **AJAX endpoints** — All 552 content pages inject `admin-ajax.php` URL; 5 CF7 forms and WooCommerce AJAX will fail in static hosting
2. **External embeds** — 13 YouTube embeds + 3 Google Maps iframes working; social tracking scripts cosmetic
3. **Plugin inventory** — 15 plugins identified; 8 broken in static (CF7, WooCommerce, YITH Wishlist, Cost Calculator), 7 working (RevSlider, Elementor, WP Bakery)
4. **Missing downloads** — 107 files missing: 50 PDFs, 54 DWG ZIPs, 3 DOCX (irreplaceable technical documentation)
5. **Forms** — 5 CF7 forms (IDs: 1004, 1005, 19875, 22816, 30013) all broken; need static form service replacement
6. **WooCommerce** — 36 product pages captured with prices/specs; cart/checkout AJAX broken (acceptable)
7. **Blog** — 0 individual posts captured; site has ~61 posts; blog index exists but post pages were not scraped
8. **Portfolio** — 29 items fully captured across 5 categories

## Key Findings

- **CRITICAL:** 107 technical files (PDFs + DWG CAD drawings + DOCX specs) are missing from backup and must be downloaded before WP access is lost
- **HIGH:** All 5 Contact Form 7 forms are broken — contact form, warranty registration, course registration, and sitewide inquiry form
- **MEDIUM:** ~61 blog posts were never scraped — only the blog index page is present
- Blog posts are missing likely because wget didn't follow individual post URLs from the dynamically-rendered blog index

## Deviations from Plan

None — plan executed exactly as written.

## Deliverable

AUDIT-REPORT.md at `.planning/quick/260407-qhd-resystausa-com/AUDIT-REPORT.md`
- 499 lines, 26KB
- Covers all 8 audit categories from the plan
- Every finding has a priority level (CRITICAL/HIGH/MEDIUM/LOW)
- Includes wget command pattern for batch-downloading 107 missing files
- Includes CDX API command for enumerating missing blog post URLs
