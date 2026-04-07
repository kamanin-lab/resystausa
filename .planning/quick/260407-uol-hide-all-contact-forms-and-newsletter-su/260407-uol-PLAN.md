---
phase: quick
plan: 260407-uol
type: execute
wave: 1
depends_on: []
files_modified:
  - resysta-backup/site/**/*.html  # 607 files patched in-place by script
  - resysta-backup/hide-forms.py
autonomous: true
requirements: []

must_haves:
  truths:
    - "All CF7 contact forms are invisible on every page of the static site"
    - "The Flodesk newsletter widget on the homepage is invisible"
    - "Form HTML is preserved in source — not deleted, only hidden"
    - "The site renders without errors (no broken layout from the change)"
  artifacts:
    - path: "resysta-backup/hide-forms.py"
      provides: "Script that injects hide CSS into all affected HTML files"
    - path: "resysta-backup/site/index.html"
      provides: "Homepage with both CF7 form and newsletter hidden"
  key_links:
    - from: "hide-forms.py"
      to: "resysta-backup/site/**/*.html"
      via: "in-place string replacement — inserts <style> block before </head>"
      pattern: "</head>"
---

<objective>
Hide all broken CF7 contact forms and the Flodesk newsletter widget across 607+ pages of the static HTML backup by injecting a CSS `display:none` rule before `</head>` in every affected file.

Purpose: The static site is deployed to Vercel. CF7 AJAX POST submissions will fail on static hosting. The client wants forms invisible (not deleted) until a replacement solution is in place.
Output: 607+ patched HTML files + 1 Python script.
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/execute-plan.md
@$HOME/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/STATE.md

Site backup root: G:/01_OPUS/Projects/resystausa/resysta-backup/site/

Key facts discovered during planning:
- 607 HTML files contain class="wpcf7" (CF7 form wrapper)
- Newsletter is a Flodesk embed (class="resnewsletter", div id="fd-form-*") — appears ONLY on index.html
- CF7 forms render as: `<div class="wpcf7 ...">` wrappers
- A single CSS rule hides all CF7 forms sitewide: `.wpcf7 { display: none !important; }`
- Newsletter hide rule: `.resnewsletter { display: none !important; }`
- Injection point: insert `<style>` block immediately before `</head>` in each file
- Files NOT containing "wpcf7" or "resnewsletter" must NOT be modified
</context>

<tasks>

<task type="auto">
  <name>Task 1: Write and run hide-forms.py to inject CSS into all affected HTML files</name>
  <files>resysta-backup/hide-forms.py</files>
  <action>
Create G:/01_OPUS/Projects/resystausa/resysta-backup/hide-forms.py with the following logic:

```python
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
```

After writing the file, run it:
```bash
cd G:/01_OPUS/Projects/resystausa
python resysta-backup/hide-forms.py
```

Expected output: ~607 patched, rest skipped.
  </action>
  <verify>
    <automated>python resysta-backup/hide-forms.py 2>&1 | grep -E "Patched|Done"</automated>
  </verify>
  <done>Script runs without error and reports 600+ files patched. Running it a second time reports 0 patched (idempotent / "already-patched" count matches first run's patched count).</done>
</task>

<task type="auto">
  <name>Task 2: Spot-check patched files to confirm CSS injection is correct</name>
  <files>(read-only verification — no files modified)</files>
  <action>
Run these three verification checks:

1. Confirm the style block appears in a high-traffic page (index.html):
```bash
grep -A 5 "gsd:hide-forms" "G:/01_OPUS/Projects/resystausa/resysta-backup/site/index.html"
```
Expected: Shows the `<style>` block with both `.wpcf7` and `.resnewsletter` rules.

2. Confirm a known CF7 page is patched (contact page):
```bash
grep "gsd:hide-forms" "G:/01_OPUS/Projects/resystausa/resysta-backup/site/contact-resysta-usa/index.html"
```
Expected: Outputs the hide marker line (non-empty).

3. Confirm a page WITHOUT wpcf7 was NOT modified (pick any blog post):
```bash
BLOG_FILE=$(ls "G:/01_OPUS/Projects/resystausa/resysta-backup/site/blog/"*/index.html 2>/dev/null | head -1)
grep -c "gsd:hide-forms" "$BLOG_FILE" && echo "UNEXPECTED PATCH" || echo "Correctly skipped"
```
Expected: "Correctly skipped" (blog posts have no CF7 forms).

4. Count total patched files as a sanity check:
```bash
grep -rl "gsd:hide-forms" "G:/01_OPUS/Projects/resystausa/resysta-backup/site/" --include="*.html" | wc -l
```
Expected: 600-620 files (matches script's patched count).

If any check fails, re-run hide-forms.py and re-verify. The script is idempotent — safe to run multiple times.
  </action>
  <verify>
    <automated>grep -c "gsd:hide-forms" "G:/01_OPUS/Projects/resystausa/resysta-backup/site/index.html"</automated>
  </verify>
  <done>All four checks pass: index.html contains the style block, contact page is patched, blog post is NOT patched, total patched count is 600+.</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| Script → local filesystem | Python script writes to local HTML files — no network, no untrusted input |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-uol-01 | Tampering | hide-forms.py file walk | accept | Script is local-only, no network calls, no user input. Worst case: wrong files patched — idempotent run + git diff catches any issue. |
| T-uol-02 | Denial of Service | Encoding errors on binary-named .html | mitigate | `errors="replace"` in open() prevents crash on malformed bytes. |
</threat_model>

<verification>
Full verification sequence after both tasks complete:

1. Script exit code is 0
2. `grep -rl "gsd:hide-forms" resysta-backup/site/ --include="*.html" | wc -l` returns 600+
3. `grep "gsd:hide-forms" resysta-backup/site/index.html` returns the marker (homepage patched)
4. `grep "gsd:hide-forms" resysta-backup/site/contact-resysta-usa/index.html` returns the marker
5. No blog post files contain the marker (they have no CF7 forms)
6. Running the script a second time shows 0 new patches (idempotent)
</verification>

<success_criteria>
- All 600+ HTML files containing CF7 wpcf7 wrappers have `.wpcf7 { display: none !important; }` injected into a `<style>` block before `</head>`
- The Flodesk newsletter section on index.html is hidden via `.resnewsletter { display: none !important; }`
- Form HTML is untouched — only a `<style>` tag was added, nothing deleted
- Pages without forms are unmodified
- Script is re-runnable safely (idempotent via `gsd:hide-forms` marker check)
</success_criteria>

<output>
After completion, create `.planning/quick/260407-uol-hide-all-contact-forms-and-newsletter-su/260407-uol-SUMMARY.md` with:
- Files patched count
- Verification results
- Any anomalies found (pages with no `</head>` tag, etc.)
</output>
