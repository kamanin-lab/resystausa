---
phase: quick
plan: 260407-uol
subsystem: static-site-patching
tags: [css-injection, cf7, flodesk, forms, static-site]
dependency_graph:
  requires: []
  provides: [hidden-cf7-forms, hidden-newsletter-widget]
  affects: [resysta-backup/site/**/*.html]
tech_stack:
  added: []
  patterns: [idempotent-css-injection, in-place-html-patching]
key_files:
  created:
    - resysta-backup/hide-forms.py
  modified:
    - resysta-backup/site/**/*.html  # 607 files patched
decisions:
  - Used CSS display:none injection (not HTML deletion) to preserve form structure for future replacement
  - Idempotency via gsd:hide-forms comment marker — safe to re-run
  - Skipped wp-admin and cdn-cgi directories (non-public pages)
metrics:
  duration: ~10 minutes
  completed: 2026-04-07
  tasks_completed: 2
  files_modified: 608
---

# Phase quick Plan 260407-uol: Hide All Contact Forms and Newsletter Summary

**One-liner:** Injected `.wpcf7 { display: none }` and `.resnewsletter { display: none }` into 607 static HTML files before `</head>` using an idempotent Python script.

## What Was Built

A Python script (`hide-forms.py`) that walks all HTML files in `resysta-backup/site/`, detects files containing CF7 form wrappers (`wpcf7`) or Flodesk newsletter embeds (`resnewsletter`), and injects a `<style>` block immediately before `</head>`. The script uses a comment marker (`<!-- gsd:hide-forms -->`) to ensure idempotency.

## Results

| Metric | Value |
|--------|-------|
| HTML files scanned | 609 |
| Files patched | 607 |
| Files skipped (no targets) | 2 |
| Files with no `</head>` | 0 |
| Second-run new patches | 0 (idempotent confirmed) |

## Verification Results

1. **Script exit code:** 0 (success)
2. **Total patched files:** 607 (confirmed via grep count)
3. **index.html patched:** Confirmed — `gsd:hide-forms` marker + style block present before `</head>`
4. **contact-resysta-usa/index.html patched:** Confirmed — marker present
5. **Idempotency:** Second run shows 607 already-patched, 0 new patches

## Deviations from Plan

### Plan Assumption Corrected

**Found during:** Task 2 (verification)
**Issue:** The plan stated "blog posts have no CF7 forms" and expected verification check 5 to confirm blog posts were NOT patched. In reality, blog post HTML files contain 58+ `wpcf7` references each (the CF7 script is loaded sitewide in WordPress).
**Fix:** No fix needed — the script's behavior is correct. Blog posts were patched, which is the desired outcome (CF7 forms should be hidden everywhere). The plan's verification assumption was inaccurate, not the implementation.
**Impact:** 0 — all 607 patched files correctly have CF7 forms hidden.

## Known Stubs

None — the CSS injection directly hides the form elements on every patched page.

## Threat Flags

None — script is local filesystem only, no network calls, no user input.

## Self-Check: PASSED

- `resysta-backup/hide-forms.py` — EXISTS
- `resysta-backup/site/index.html` — EXISTS with gsd:hide-forms marker (confirmed)
- `resysta-backup/site/contact-resysta-usa/index.html` — EXISTS with gsd:hide-forms marker (confirmed)
- Site sub-repo commit `046c6f5` — 607 files changed (confirmed)
- Parent repo commit `116406b` — hide-forms.py added (confirmed)
