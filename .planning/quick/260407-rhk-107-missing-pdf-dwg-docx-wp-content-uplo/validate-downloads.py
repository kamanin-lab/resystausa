#!/usr/bin/env python3
"""
Task 2: Validate downloaded files and produce download-report.txt.

Checks:
- File size > 1 KB
- PDF header = %PDF
- ZIP/DOCX header = PK (0x504B)
- No Cloudflare challenge HTML saved as binary file
"""

import re
import os
from pathlib import Path

SITE_ROOT = Path("G:/01_OPUS/Projects/resystausa/resysta-backup/site")
UPLOADS_ROOT = SITE_ROOT / "wp-content/uploads"
PLAN_DIR = Path("G:/01_OPUS/Projects/resystausa/.planning/quick/260407-rhk-107-missing-pdf-dwg-docx-wp-content-uplo")
MISSING_TXT = PLAN_DIR / "missing-files.txt"

URL_PATTERN = re.compile(
    r'https?://(?:www\.)?resystausa\.com(/wp-content/uploads/\d{4}/\d{2}/[^"\'>\s]+)',
    re.IGNORECASE
)
TARGET_EXTS = {".pdf", ".zip", ".docx"}


def local_path_for(url_path):
    return SITE_ROOT / url_path.lstrip("/")


def scan_html_files():
    found = set()
    for html_file in SITE_ROOT.rglob("*.html"):
        try:
            content = html_file.read_text(encoding="utf-8", errors="replace")
            for match in URL_PATTERN.finditer(content):
                path = match.group(1)
                if Path(path).suffix.lower() in TARGET_EXTS:
                    found.add(path)
        except Exception:
            pass
    return sorted(found)


def validate_file(local_path, ext):
    """Returns (ok: bool, reason: str)."""
    if not local_path.exists():
        return False, "File missing"
    size = local_path.stat().st_size
    if size < 1024:
        return False, f"Too small ({size} bytes)"
    try:
        with open(local_path, "rb") as f:
            header = f.read(16)
        # Check for HTML content (Cloudflare challenge)
        if header[:9].upper() in (b"<!DOCTYPE", b"<HTML LAN") or header[:6].upper() == b"<HTML>":
            return False, "Cloudflare challenge HTML saved as file"
        if ext == ".pdf":
            if header[:4] != b"%PDF":
                return False, f"Not a PDF (header: {header[:4]})"
        elif ext in (".zip", ".docx"):
            if header[:2] != b"PK":
                return False, f"Not a ZIP/DOCX (header: {header[:2]})"
        return True, f"OK ({size // 1024} KB)"
    except Exception as e:
        return False, f"Read error: {e}"


def main():
    print("=" * 60)
    print("Validation Report — resystausa.com Missing Files")
    print("=" * 60)
    print()

    all_paths = scan_html_files()
    print(f"Total upload URLs in HTML: {len(all_paths)}")

    still_missing = [p for p in all_paths if not local_path_for(p).exists()]
    print(f"Still missing locally: {len(still_missing)}")
    print()

    # Validate each file referenced in HTML
    valid = []
    invalid = []
    cf_challenges = []

    for url_path in all_paths:
        local = local_path_for(url_path)
        ext = Path(url_path).suffix.lower()
        ok, reason = validate_file(local, ext)
        if ok:
            valid.append((url_path, reason))
        elif "Cloudflare" in reason:
            cf_challenges.append((url_path, reason))
            invalid.append((url_path, reason))
        else:
            invalid.append((url_path, reason))

    # By type
    pdf_valid = sum(1 for p, _ in valid if Path(p).suffix.lower() == ".pdf")
    zip_valid = sum(1 for p, _ in valid if Path(p).suffix.lower() == ".zip")
    docx_valid = sum(1 for p, _ in valid if Path(p).suffix.lower() == ".docx")

    # Write report
    report_path = PLAN_DIR / "download-report.txt"
    lines = []
    lines.append("=" * 60)
    lines.append("download-report.txt — resystausa.com 107-file download")
    lines.append(f"Generated: 2026-04-07")
    lines.append("=" * 60)
    lines.append("")
    lines.append("COUNTS")
    lines.append(f"  Total URLs in HTML:      {len(all_paths)}")
    lines.append(f"  Valid files (passed):    {len(valid)}")
    lines.append(f"    PDFs:                  {pdf_valid}")
    lines.append(f"    ZIPs:                  {zip_valid}")
    lines.append(f"    DOCXs:                 {docx_valid}")
    lines.append(f"  Invalid/missing files:   {len(invalid)}")
    lines.append(f"  Cloudflare challenges:   {len(cf_challenges)}")
    lines.append("")

    if invalid:
        lines.append("INVALID/FAILED FILES")
        for url_path, reason in invalid:
            lines.append(f"  FAIL: https://resystausa.com{url_path}")
            lines.append(f"        Reason: {reason}")
        lines.append("")
    else:
        lines.append("INVALID/FAILED FILES: None")
        lines.append("")

    if cf_challenges:
        lines.append("CLOUDFLARE CHALLENGE PAGES DETECTED")
        for url_path, _ in cf_challenges:
            lines.append(f"  CF: https://resystausa.com{url_path}")
        lines.append("")
    else:
        lines.append("CLOUDFLARE CHALLENGE PAGES: None detected")
        lines.append("")

    lines.append("VALIDATION RESULT")
    if len(invalid) == 0 and len(still_missing) == 0:
        lines.append("  STATUS: PASS — All 107 files present and valid")
    else:
        lines.append(f"  STATUS: PARTIAL — {len(valid)}/107 valid, {len(invalid)} failed")
        lines.append("  Next steps for failed files:")
        lines.append("  1. Retry via Wayback Machine: waybackpack <URL>")
        lines.append("  2. Try HTTPS domain (if TLS cert is valid): https://resystausa.com/<path>")
    lines.append("")

    report_text = "\n".join(lines)
    with open(report_path, "w") as f:
        f.write(report_text)

    print(report_text)
    print(f"Report written to: {report_path}")


if __name__ == "__main__":
    main()
