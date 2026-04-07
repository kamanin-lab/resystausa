#!/usr/bin/env python3
"""
hide-forms.py — Inject CSS to hide CF7 contact forms and Flodesk newsletter
across all HTML files in the static site backup.

Targets:
  - .wpcf7 { display: none !important; }  — hides all CF7 form wrappers
  - .resnewsletter { display: none !important; }  — hides Flodesk newsletter widget

Strategy:
  - Walk resysta-backup/site/ recursively, process *.html files
  - Only patch files that contain "wpcf7" or "resnewsletter"
  - Insert <style> block immediately before </head>
  - Skip files that already contain the hide marker (idempotent)
  - Print a summary: files scanned / patched / skipped
"""

import os
import sys

SITE_DIR = os.path.join(os.path.dirname(__file__), "site")

HIDE_MARKER = "<!-- gsd:hide-forms -->"

STYLE_BLOCK = """\
<!-- gsd:hide-forms -->
<style>
/* Hide broken CF7 contact forms (static hosting — AJAX POST will fail) */
.wpcf7 { display: none !important; }
/* Hide Flodesk newsletter widget */
.resnewsletter { display: none !important; }
</style>"""

def patch_file(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Skip if neither target class is present
    if "wpcf7" not in content and "resnewsletter" not in content:
        return "skipped"

    # Skip if already patched (idempotent)
    if HIDE_MARKER in content:
        return "already-patched"

    # Insert before </head>
    if "</head>" not in content:
        return "no-head-tag"

    patched = content.replace("</head>", STYLE_BLOCK + "\n</head>", 1)

    with open(path, "w", encoding="utf-8", errors="replace") as f:
        f.write(patched)

    return "patched"

def main():
    counts = {"patched": 0, "skipped": 0, "already-patched": 0, "no-head-tag": 0}
    total = 0

    for root, dirs, files in os.walk(SITE_DIR):
        # Skip wp-admin, cdn-cgi — not public pages
        dirs[:] = [d for d in dirs if d not in ("wp-admin", "cdn-cgi")]
        for fname in files:
            if not fname.endswith(".html"):
                continue
            total += 1
            result = patch_file(os.path.join(root, fname))
            counts[result] += 1

    print(f"Done. Scanned {total} HTML files.")
    print(f"  Patched:        {counts['patched']}")
    print(f"  Already patched:{counts['already-patched']}")
    print(f"  Skipped:        {counts['skipped']}")
    print(f"  No </head> tag: {counts['no-head-tag']}")

if __name__ == "__main__":
    main()
