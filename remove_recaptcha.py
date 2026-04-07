#!/usr/bin/env python3
"""Remove reCAPTCHA scripts from all HTML files in resysta-backup/site."""

import os
import re
from pathlib import Path

BACKUP_DIR = Path("resysta-backup/site")

# Patterns to remove (full script tags)
PATTERNS = [
    # <script src="https://www.google.com/recaptcha/api.js..."></script>
    re.compile(
        r'<script[^>]+src="https://www\.google\.com/recaptcha/api\.js[^"]*"[^>]*>\s*</script>',
        re.IGNORECASE,
    ),
    # <script id="wpcf7-recaptcha-js-before">...var wpcf7_recaptcha = {...}...</script>
    re.compile(
        r'<script[^>]+id="wpcf7-recaptcha-js-before"[^>]*>.*?</script>',
        re.IGNORECASE | re.DOTALL,
    ),
    # <script src=".../contact-form-7/modules/recaptcha/index.js..."></script>
    re.compile(
        r'<script[^>]+src="[^"]*contact-form-7/modules/recaptcha/index\.js[^"]*"[^>]*>\s*</script>',
        re.IGNORECASE,
    ),
]

def process_file(path: Path) -> bool:
    """Remove reCAPTCHA tags from a single file. Returns True if modified."""
    original = path.read_text(encoding="utf-8", errors="ignore")
    content = original
    for pattern in PATTERNS:
        content = pattern.sub("", content)
    if content != original:
        path.write_text(content, encoding="utf-8")
        return True
    return False

def main():
    html_files = list(BACKUP_DIR.rglob("*.html"))
    print(f"Found {len(html_files)} HTML files")
    modified = 0
    for f in html_files:
        if process_file(f):
            modified += 1
            print(f"  cleaned: {f.relative_to(BACKUP_DIR)}")
    print(f"\nDone. Modified {modified}/{len(html_files)} files.")

if __name__ == "__main__":
    main()
