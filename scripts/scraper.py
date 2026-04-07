#!/usr/bin/env python3
"""
resystausa.com Python fallback scraper.

Targets direct IP (HTTP, not HTTPS) to bypass Cloudflare TLS fingerprinting.
Run ONLY when wget passes have failed challenge-page detection or wget is absent.

Usage:
    python scraper.py [--ip IP] [--seed-file FILE] [--max-pages N] [--output-dir DIR]
"""

import argparse
import os
import random
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urldefrag, urlparse

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DOMAIN = "resystausa.com"
CHALLENGE_MARKERS = ["_cf_chl_opt", "cf-browser-verification", "Just a moment"]

# Asset file extensions to download as page requisites
ASSET_EXTENSIONS = {
    ".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp",
    ".woff", ".woff2", ".ttf", ".eot", ".pdf", ".ico",
}

# Full browser header set — Host is set dynamically based on DIRECT_IP
BASE_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}

# URL patterns to skip — mirrors wget --reject-regex
SKIP_PATTERN = re.compile(
    r"(\?s=|\?replytocom=|/wp-json/|/feed/?$|/trackback/"
    r"|\?share=|\?like=|\?wc-ajax=|#|mailto:|tel:)"
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def build_base_url(ip: str) -> str:
    """Return http://IP (no trailing slash)."""
    return f"http://{ip}"


def is_challenge_page(html: str) -> bool:
    """Return True if response body contains Cloudflare challenge markers."""
    return any(marker in html for marker in CHALLENGE_MARKERS)


def normalize_url(url: str, base_url: str, direct_ip_base: str) -> str | None:
    """
    Normalize a URL to the direct-IP form.

    - Rewrites domain-based URLs to use direct IP.
    - Ignores external domains.
    - Resolves relative URLs against base_url.
    - Returns None if the URL should be skipped.
    """
    url, _ = urldefrag(url)
    if not url or url.startswith("data:"):
        return None

    parsed = urlparse(url)

    # Rewrite domain-based absolute URLs to use direct IP
    if parsed.netloc in (DOMAIN, f"www.{DOMAIN}"):
        url = direct_ip_base + (parsed.path or "/")
        if parsed.query:
            url += "?" + parsed.query
        parsed = urlparse(url)
    elif parsed.netloc and parsed.netloc != urlparse(direct_ip_base).netloc:
        return None  # external domain — skip

    # Resolve relative URLs
    if not parsed.netloc:
        url = urljoin(base_url, url)

    return url


def url_to_local_path(url: str, output_dir: Path) -> Path:
    """
    Convert an IP-based URL to a local file path inside output_dir.

    Security: strips leading slashes and resolves within output_dir only.
    Path traversal is prevented by ensuring the resolved path is a descendant
    of output_dir.
    """
    parsed = urlparse(url)
    path = parsed.path.lstrip("/") or "index.html"

    # Sanitize query string into filename suffix
    if parsed.query:
        safe_query = parsed.query.replace("/", "%2F").replace("\\", "%5C")
        path += "_" + safe_query

    # If path ends with / or has no extension, treat as directory index
    if not Path(path).suffix or path.endswith("/"):
        path = path.rstrip("/") + "/index.html"

    # Resolve and validate — must stay within output_dir
    resolved = (output_dir / path).resolve()
    try:
        resolved.relative_to(output_dir.resolve())
    except ValueError:
        # Path traversal attempt — fall back to safe name
        safe_name = re.sub(r"[^a-zA-Z0-9._-]", "_", path)
        resolved = output_dir / safe_name

    return resolved


def download_asset(session: requests.Session, url: str, output_dir: Path,
                   direct_ip_base: str) -> None:
    """Download a single asset (CSS/JS/image/font/PDF) to output_dir."""
    try:
        resp = session.get(url, timeout=30, allow_redirects=True)
        if resp.status_code != 200:
            return
        local_path = url_to_local_path(url, output_dir)
        local_path.parent.mkdir(parents=True, exist_ok=True)
        if local_path.exists():
            return  # no-clobber
        local_path.write_bytes(resp.content)
    except requests.RequestException:
        pass
    time.sleep(random.uniform(0.3, 0.8))


def extract_assets(soup: BeautifulSoup, base_url: str,
                   direct_ip_base: str) -> list[str]:
    """Extract asset URLs (CSS, JS, images, fonts, PDFs) from parsed HTML."""
    assets = []
    selectors = [
        ("link", "href"),
        ("script", "src"),
        ("img", "src"),
        ("source", "src"),
        ("a", "href"),
    ]
    for tag_name, attr in selectors:
        for tag in soup.find_all(tag_name, **{attr: True}):
            raw = tag.get(attr, "").strip()
            if not raw:
                continue
            # Handle srcset attributes
            normalized = normalize_url(raw, base_url, direct_ip_base)
            if normalized:
                ext = Path(urlparse(normalized).path).suffix.lower()
                if ext in ASSET_EXTENSIONS:
                    assets.append(normalized)

    # Also handle img srcset
    for img in soup.find_all("img", srcset=True):
        for part in img["srcset"].split(","):
            src = part.strip().split()[0]
            normalized = normalize_url(src, base_url, direct_ip_base)
            if normalized:
                ext = Path(urlparse(normalized).path).suffix.lower()
                if ext in ASSET_EXTENSIONS:
                    assets.append(normalized)

    return list(dict.fromkeys(assets))  # deduplicate, preserve order


# ---------------------------------------------------------------------------
# Main scraper
# ---------------------------------------------------------------------------

def scrape(
    ip: str,
    seed_urls: list[str],
    max_pages: int,
    output_dir: Path,
    url_list_raw: Path,
) -> int:
    """
    Recursively scrape the site via direct IP.

    Returns number of pages saved.
    """
    direct_ip_base = build_base_url(ip)

    headers = dict(BASE_HEADERS)
    headers["Host"] = DOMAIN

    session = requests.Session()
    session.headers.update(headers)

    visited: set[str] = set()
    queue: list[str] = list(seed_urls)
    url_log: list[str] = []

    output_dir.mkdir(parents=True, exist_ok=True)

    while queue and len(visited) < max_pages:
        url = queue.pop(0)
        if url in visited:
            continue
        if SKIP_PATTERN.search(url):
            continue

        visited.add(url)
        print(f"[{len(visited)}] Fetching: {url}")

        try:
            resp = session.get(url, timeout=30, allow_redirects=True)
        except requests.RequestException as exc:
            print(f"  ERROR: {exc}")
            time.sleep(2)
            continue

        if resp.status_code != 200:
            print(f"  HTTP {resp.status_code} — skipping")
            time.sleep(1)
            continue

        html = resp.text
        if is_challenge_page(html):
            print(f"  CHALLENGE PAGE DETECTED at {url} — skipping")
            continue

        # Save HTML to disk
        local_path = url_to_local_path(url, output_dir)
        local_path.parent.mkdir(parents=True, exist_ok=True)
        local_path.write_text(html, encoding="utf-8", errors="replace")

        # Record URL in canonical domain form
        canonical = url.replace(direct_ip_base, f"https://{DOMAIN}")
        url_log.append(canonical)

        # Parse and enqueue links
        soup = BeautifulSoup(html, "lxml")
        for tag in soup.find_all(["a", "link"], href=True):
            href = tag.get("href", "").strip()
            normalized = normalize_url(href, url, direct_ip_base)
            if normalized and normalized not in visited:
                # Only enqueue HTML pages (no file extension = page)
                ext = Path(urlparse(normalized).path).suffix.lower()
                if ext not in ASSET_EXTENSIONS and not SKIP_PATTERN.search(normalized):
                    queue.append(normalized)

        # Download page requisites (assets)
        assets = extract_assets(soup, url, direct_ip_base)
        for asset_url in assets:
            if asset_url not in visited:
                visited.add(asset_url)
                download_asset(session, asset_url, output_dir, direct_ip_base)

        # Throttle between page requests
        time.sleep(random.uniform(1.5, 3.0))

    # Append discovered URLs to url-list-raw.txt
    url_list_raw.parent.mkdir(parents=True, exist_ok=True)
    with url_list_raw.open("a", encoding="utf-8") as fh:
        for u in url_log:
            fh.write(u + "\n")

    saved = len(url_log)
    print(f"\nScraper complete: {len(visited)} pages visited, {saved} saved.")
    return saved


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="resystausa.com recursive scraper — direct IP bypass"
    )
    parser.add_argument(
        "--ip",
        default="74.208.236.71",
        help="Direct server IP address (default: 74.208.236.71)",
    )
    parser.add_argument(
        "--seed-file",
        default=None,
        metavar="FILE",
        help="File containing seed URLs to crawl (one per line)",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=2000,
        metavar="N",
        help="Maximum number of pages to visit (default: 2000)",
    )
    parser.add_argument(
        "--output-dir",
        default="resysta-backup/site",
        metavar="DIR",
        help="Output directory for downloaded pages (default: resysta-backup/site)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    direct_ip_base = build_base_url(args.ip)
    output_dir = Path(args.output_dir)
    url_list_raw = output_dir.parent / "url-list-raw.txt"

    # Build seed URL list
    seeds: list[str] = [f"{direct_ip_base}/"]
    if args.seed_file and os.path.exists(args.seed_file):
        with open(args.seed_file, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                normalized = normalize_url(line, f"{direct_ip_base}/", direct_ip_base)
                if normalized:
                    seeds.append(normalized)
        print(f"[INFO] Loaded {len(seeds) - 1} seed URLs from {args.seed_file}")
    else:
        if args.seed_file:
            print(f"[WARN] Seed file not found: {args.seed_file} — using root URL only")

    print(f"[INFO] Starting scraper: IP={args.ip}, max_pages={args.max_pages}, "
          f"output={output_dir}")

    try:
        scrape(
            ip=args.ip,
            seed_urls=seeds,
            max_pages=args.max_pages,
            output_dir=output_dir,
            url_list_raw=url_list_raw,
        )
    except KeyboardInterrupt:
        print("\n[INFO] Scraper interrupted by user.")
        return 0
    except Exception as exc:  # pylint: disable=broad-except
        print(f"[FATAL] Scraper failed: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
