#!/usr/bin/env python3
"""
Download all missing PDF, ZIP, DOCX files from resystausa.com
via direct IP bypass (74.208.236.71, HTTP port 80).

Task 260407-rhk: Download 107 missing technical files.
"""

import os
import re
import time
import random
import requests
from pathlib import Path

# ---- Config ----------------------------------------------------------------
SITE_ROOT = Path("G:/01_OPUS/Projects/resystausa/resysta-backup/site")
UPLOADS_ROOT = SITE_ROOT / "wp-content/uploads"
PLAN_DIR = Path("G:/01_OPUS/Projects/resystausa/.planning/quick/260407-rhk-107-missing-pdf-dwg-docx-wp-content-uplo")
ORIGIN_IP = "74.208.236.71"
ORIGIN_BASE = f"http://{ORIGIN_IP}"

HEADERS = {
    "Host": "resystausa.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
}

TARGET_EXTS = {".pdf", ".zip", ".docx"}
# Regex to match resystausa.com uploads URLs
URL_PATTERN = re.compile(
    r'https?://(?:www\.)?resystausa\.com(/wp-content/uploads/\d{4}/\d{2}/[^"\'>\s]+)',
    re.IGNORECASE
)

# ---- Step 1: Scan HTML files for upload URLs --------------------------------

def scan_html_files():
    """Scan all HTML files and collect wp-content/uploads URLs with target extensions."""
    found_urls = set()
    html_files = list(SITE_ROOT.rglob("*.html"))
    print(f"Scanning {len(html_files)} HTML files...")

    for html_file in html_files:
        try:
            content = html_file.read_text(encoding="utf-8", errors="replace")
            for match in URL_PATTERN.finditer(content):
                path = match.group(1)
                ext = Path(path).suffix.lower()
                if ext in TARGET_EXTS:
                    # Normalize: decode %20 etc
                    found_urls.add(path)
        except Exception as e:
            print(f"  WARN: Could not read {html_file}: {e}")

    return sorted(found_urls)


def local_path_for(url_path):
    """Convert /wp-content/uploads/YYYY/MM/file.ext to local Path."""
    # url_path starts with /wp-content/uploads/
    relative = url_path.lstrip("/")
    return SITE_ROOT / relative


def find_missing(all_paths):
    """Return subset of paths that do not exist locally."""
    missing = []
    for path in all_paths:
        local = local_path_for(path)
        if not local.exists():
            missing.append(path)
    return missing


# ---- Step 2: Download files -----------------------------------------------

def is_cloudflare_challenge(response):
    """Detect if the response is a Cloudflare challenge page instead of real content."""
    ct = response.headers.get("Content-Type", "")
    if "text/html" in ct:
        snippet = response.content[:500].decode("utf-8", errors="replace")
        if any(marker in snippet for marker in [
            "Just a moment", "_cf_chl_opt", "Cloudflare", "cf-spinner",
            "<!DOCTYPE", "<html"
        ]):
            return True
    return False


def validate_file_header(local_path, ext):
    """Validate file header bytes match expected format."""
    try:
        with open(local_path, "rb") as f:
            header = f.read(8)
        if ext == ".pdf":
            return header[:4] == b"%PDF"
        elif ext in (".zip", ".docx"):
            return header[:2] == b"PK"
        return True
    except Exception:
        return False


def download_file(url_path, idx, total, retry=False):
    """Download a single file. Returns (success, size_bytes, error_msg)."""
    local = local_path_for(url_path)
    download_url = f"{ORIGIN_BASE}{url_path}"
    ext = Path(url_path).suffix.lower()

    try:
        resp = requests.get(download_url, headers=HEADERS, timeout=30, stream=True)

        if resp.status_code != 200:
            return False, 0, f"HTTP {resp.status_code}"

        if is_cloudflare_challenge(resp):
            return False, 0, "Cloudflare challenge page"

        # Create directories
        local.parent.mkdir(parents=True, exist_ok=True)

        # Write file
        content = resp.content
        if len(content) == 0:
            return False, 0, "Empty response"

        local.write_bytes(content)

        # Validate header
        if not validate_file_header(local, ext):
            local.unlink(missing_ok=True)
            return False, 0, f"Invalid file header (not {ext[1:].upper()})"

        size_kb = len(content) / 1024
        label = "RETRY OK" if retry else "OK"
        print(f"  [{idx}/{total}] {label} {local.name} ({size_kb:.1f} KB)")
        return True, len(content), None

    except requests.exceptions.RequestException as e:
        return False, 0, str(e)


# ---- Main ------------------------------------------------------------------

def main():
    print("=" * 60)
    print("resystausa.com Missing Files Downloader")
    print("=" * 60)
    print()

    # Step 1: Scan
    all_upload_paths = scan_html_files()
    print(f"Found {len(all_upload_paths)} total upload URLs in HTML files")

    # Step 2: Find missing
    missing = find_missing(all_upload_paths)
    print(f"Missing locally: {len(missing)} files")
    print()

    # Write missing-files.txt audit log
    missing_txt = PLAN_DIR / "missing-files.txt"
    with open(missing_txt, "w") as f:
        for path in missing:
            f.write(f"https://resystausa.com{path}\n")
    print(f"Wrote {missing_txt}")
    print()

    if not missing:
        print("All files already present locally. Nothing to download.")
        return

    # Step 3: Download
    print(f"Starting download of {len(missing)} files...")
    print(f"Using: {ORIGIN_BASE} with Host: resystausa.com")
    print("-" * 60)

    results = []
    failed = []
    total = len(missing)

    for idx, url_path in enumerate(missing, 1):
        success, size, err = download_file(url_path, idx, total)
        if success:
            results.append((url_path, size, None))
        else:
            print(f"  [{idx}/{total}] FAILED {Path(url_path).name}: {err}")
            failed.append((url_path, err))

        # Rate limit: 1.5-2.5s between requests
        if idx < total:
            delay = random.uniform(1.5, 2.5)
            time.sleep(delay)

    print()
    print("-" * 60)

    # Step 4: Retry failures with longer delay
    if failed:
        print(f"Retrying {len(failed)} failed files (3-5s delay)...")
        still_failed = []
        for url_path, prev_err in failed:
            time.sleep(random.uniform(3.0, 5.0))
            success, size, err = download_file(url_path, "R", len(failed), retry=True)
            if success:
                results.append((url_path, size, None))
            else:
                print(f"  [R] STILL FAILED {Path(url_path).name}: {err}")
                still_failed.append((url_path, err))
        failed = still_failed

    # Step 5: Summary
    print()
    print("=" * 60)
    print(f"SUMMARY: {len(results)} downloaded, {len(failed)} failed")
    print("=" * 60)

    if failed:
        print("\nFailed files (manual retry or Wayback Machine needed):")
        for url_path, err in failed:
            print(f"  FAILED: https://resystausa.com{url_path}")
            print(f"          Reason: {err}")

    # Final counts
    pdf_count = sum(1 for p, _, _ in results if Path(p).suffix.lower() == ".pdf")
    zip_count = sum(1 for p, _, _ in results if Path(p).suffix.lower() == ".zip")
    docx_count = sum(1 for p, _, _ in results if Path(p).suffix.lower() == ".docx")
    print(f"\nDownloaded by type: {pdf_count} PDFs, {zip_count} ZIPs, {docx_count} DOCXs")

    return results, failed


if __name__ == "__main__":
    main()
