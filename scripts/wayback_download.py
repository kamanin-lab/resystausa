#!/usr/bin/env python3
"""
resystausa.com Wayback Machine downloader.

Performs a CDX API pre-check before invoking waybackpack.
If no snapshots are found in the CDX index, exits cleanly without downloading.

Usage:
    python wayback_download.py [--from-date YYYYMMDD] [--to-date YYYYMMDD] [--output-dir DIR]
"""

import argparse
import subprocess
import sys
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DOMAIN = "resystausa.com"
CDX_API = "https://web.archive.org/cdx/search/cdx"

# Query string patterns to filter out from CDX results (search/compare junk)
SKIP_PATTERNS = ["?s=", "?replytocom=", "wc-ajax", "yith-woocompare"]


# ---------------------------------------------------------------------------
# CDX pre-check
# ---------------------------------------------------------------------------

def query_cdx(from_date: str, to_date: str, output_dir: Path) -> list[str]:
    """
    Query the CDX API for all archived resystausa.com URLs.

    Returns a list of clean (filtered) URLs, or an empty list if none found.
    Saves full CDX output to output_dir/../wayback-cdx-urls.txt.
    Saves filtered output to output_dir/../wayback-url-list-clean.txt.
    """
    backup_dir = output_dir.parent

    params = {
        "url": f"{DOMAIN}/*",
        "output": "text",
        "fl": "original",
        "collapse": "urlkey",
        "filter": "statuscode:200",
        "from": from_date,
        "to": to_date,
    }

    print(f"[CDX] Querying Wayback Machine CDX API for {DOMAIN} snapshots "
          f"({from_date}–{to_date})...")

    try:
        resp = requests.get(CDX_API, params=params, timeout=60)
        resp.raise_for_status()
    except requests.RequestException as exc:
        print(f"[ERROR] CDX API query failed: {exc}", file=sys.stderr)
        return []

    raw_urls = [line.strip() for line in resp.text.splitlines() if line.strip()]

    if not raw_urls:
        print(f"[SKIP] No Wayback snapshots found for {DOMAIN}")
        return []

    # Save full CDX URL list
    cdx_file = backup_dir / "wayback-cdx-urls.txt"
    cdx_file.parent.mkdir(parents=True, exist_ok=True)
    cdx_file.write_text("\n".join(raw_urls) + "\n", encoding="utf-8")
    print(f"[CDX] {len(raw_urls)} total archived URLs saved to {cdx_file}")

    # Filter out query-string junk
    clean_urls = []
    for url in raw_urls:
        if not any(pat in url for pat in SKIP_PATTERNS):
            clean_urls.append(url)

    # Save clean list
    clean_file = backup_dir / "wayback-url-list-clean.txt"
    clean_file.write_text("\n".join(clean_urls) + "\n", encoding="utf-8")
    print(f"[CDX] {len(clean_urls)} clean URLs saved to {clean_file}")

    # Append clean URLs to url-list-raw.txt for consolidation
    url_list_raw = backup_dir / "url-list-raw.txt"
    with url_list_raw.open("a", encoding="utf-8") as fh:
        for url in clean_urls:
            fh.write(url + "\n")
    print(f"[CDX] Appended {len(clean_urls)} URLs to {url_list_raw}")

    return clean_urls


# ---------------------------------------------------------------------------
# waybackpack download
# ---------------------------------------------------------------------------

def run_waybackpack(from_date: str, to_date: str, output_dir: Path) -> int:
    """
    Run waybackpack to download HTML snapshots of the site.

    Returns the subprocess exit code.
    """
    print(
        "\n[NOTE] waybackpack downloads HTML snapshots only — "
        "no CSS, JS, images, or fonts."
    )
    print(f"[INFO] Downloading Wayback snapshots to {output_dir} ...")

    output_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "waybackpack",
        f"https://{DOMAIN}",
        "--from-date", from_date,
        "--to-date", to_date,
        "--delay", "3",
        "--delay-retry", "30",
        "--no-clobber",
        "--uniques-only",
        "--ignore-errors",
        "--max-retries", "3",
        "-d", str(output_dir),
    ]

    print(f"[CMD] {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=False)
        exit_code = result.returncode
    except FileNotFoundError:
        print(
            "[ERROR] waybackpack not found. Install with: pip install waybackpack",
            file=sys.stderr,
        )
        return 1

    if exit_code != 0:
        print(
            f"[WARN] waybackpack exited with code {exit_code} "
            "(partial failures expected — using --ignore-errors)"
        )
    else:
        print("[OK] waybackpack completed successfully.")

    return 0  # treat partial failures as success due to --ignore-errors


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "resystausa.com Wayback Machine downloader — "
            "CDX pre-check + waybackpack"
        )
    )
    parser.add_argument(
        "--from-date",
        default="20250101",
        metavar="YYYYMMDD",
        help="Start date for Wayback snapshots (default: 20250101)",
    )
    parser.add_argument(
        "--to-date",
        default="20260407",
        metavar="YYYYMMDD",
        help="End date for Wayback snapshots (default: 20260407)",
    )
    parser.add_argument(
        "--output-dir",
        default="resysta-backup/wayback",
        metavar="DIR",
        help="Output directory for Wayback downloads (default: resysta-backup/wayback)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)

    # Step 1: CDX pre-check
    clean_urls = query_cdx(
        from_date=args.from_date,
        to_date=args.to_date,
        output_dir=output_dir,
    )

    if not clean_urls:
        print(f"[SKIP] No Wayback snapshots found for {DOMAIN} — skipping download.")
        return 0

    # Step 2: Run waybackpack
    exit_code = run_waybackpack(
        from_date=args.from_date,
        to_date=args.to_date,
        output_dir=output_dir,
    )

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
