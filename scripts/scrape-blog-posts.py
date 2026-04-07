#!/usr/bin/env python3
"""
Scrape all blog posts from resystausa.com and save to resysta-backup/site/blog/[slug]/index.html

KEY FINDINGS:
- Blog posts are NOT at /blog/SLUG/ but at ROOT level: /SLUG/
- All posts were deleted from live site (404), MUST use Wayback Machine
- Posts organized under blog/ in backup for archival clarity
- Wayback CDX has 55 posts identified, ~55+ total
- admin-ajax.php is blocked; WP REST API returns 0 posts (all deleted/private)
- Wayback Machine is the ONLY viable source

Strategy:
1. Build URL list from embedded knowledge + CDX API query
2. Try live site first (might still have recent posts)
3. Fall back to Wayback Machine for each post
4. Save to resysta-backup/site/blog/[slug]/index.html
5. Download inline images from wp-content/uploads
"""

import requests
import time
import random
import os
import re
import json
import sys
import argparse
from pathlib import Path
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings('ignore')

# =====================
# CONFIGURATION
# =====================
BACKUP_ROOT = Path("G:/01_OPUS/Projects/resystausa/resysta-backup/site")
BLOG_DIR = BACKUP_ROOT / "blog"

LIVE_BASE_URL = "http://74.208.236.71"
LIVE_DOMAIN = "resystausa.com"
WAYBACK_BASE = "https://web.archive.org"

HEADERS = {
    "Host": "resystausa.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",
}

WAYBACK_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Known blog post slugs (at root URL, not under /blog/)
# Discovered via Wayback CDX API - these are NOT live (deleted from site)
KNOWN_BLOG_SLUGS = [
    "11-popular-decking-types",
    "choosing-the-right-composite-decking-color-for-your-outdoor-space",
    "composite-fencing-california",
    "composite-fencing-florida",
    "composite-fencing-illinois",
    "composite-fencing-in-architecture",
    "composite-fencing-minnesota",
    "composite-fencing-new-jersey",
    "composite-fencing-vs-wood-fencing-longevity",
    "composite-fencing-washington-state",
    "composite-siding-allergy-season-benefits",
    "corporate-branding-through-modern-building-facades",
    "creating-the-perfect-multi-functional-deck-for-outdoor-living",
    "decking-california",
    "decking-florida",
    "decking-illinois",
    "decking-minnesota",
    "decking-new-jersey",
    "decking-washington-state",
    "early-spring-deck-installation-guide",
    "earth-month-sustainable-composite-siding",
    "green-building-codes-architects-builders-guide",
    "how-acoustic-wall-panels-enhance-guest-experience",
    "innovative-spaces-curved-wall-siding",
    "maintenance-tips-composite-siding",
    "new-resysta-decking-color-weathered-koa",
    "outdoor-living-deck-enhancements",
    "project-spotlight-avoin-complex-burbank-ca",
    "project-spotlight-contemporary-la-residence-lusso-siding",
    "project-spotlight-contemporary-private-residence-puerto-rico",
    "property-managers-prefer-composite-fencing-over-wood",
    "resysta-ibs-2025-sustainable-building",
    "role-composite-materials-in-architecture",
    "siding-california",
    "siding-illinois",
    "siding-minnesota",
    "siding-new-jersey",
    "siding-summer-checklist-inspection-tips",
    "siding-washington-state",
    "spring-deck-cleaning-maintenance-guide",
    "spring-siding-color-trends-2025",
    "top-7-design-trends-decking-2025",
    "trellis-canopy-ideas-backyard-transformations",
    "understanding-composite-siding-homeowners-guide",
    "understanding-rainscreen-systems-ventilation-in-siding",
    "wall-cladding-california",
    "wall-cladding-florida",
    "wall-cladding-illinois",
    "wall-cladding-minnesota",
    "wall-cladding-new-jersey",
    "wall-cladding-vs-siding",
    "wall-cladding-washington-state",
    "what-is-composite-decking-material",
    "why-architects-choose-resysta-composite-fencing-sustainability",
    "why-may-best-time-install-composite-siding",
]


def get_session():
    """Create a requests session with browser-like headers."""
    session = requests.Session()
    session.headers.update(WAYBACK_HEADERS)
    return session


def enumerate_urls_from_cdx(session):
    """Method A: Wayback CDX API to enumerate blog post URLs."""
    print("\n[Method A] Querying Wayback CDX API...")
    found_slugs = set()

    try:
        resp = session.get(
            "https://web.archive.org/cdx/search/cdx",
            params={
                "url": "resystausa.com/*",
                "output": "json",
                "fl": "original",
                "limit": 2000,
                "matchType": "domain",
                "filter": "statuscode:200",
                "collapse": "original",
            },
            timeout=60
        )

        if resp.status_code == 200:
            data = resp.json()
            print(f"  CDX total results: {len(data)}")

            # Known non-blog URL patterns to skip
            non_blog_indicators = [
                'wp-content', 'wp-admin', 'wp-json', 'wp-includes', 'wp-login',
                'category/', 'tag/', 'author/', 'feed', '?', '.xml', '.svg', '.png',
                '.jpg', '.ico', '.pdf', '.zip', '.dwg', 'blog/', 'blogs/',
                'what-is-resysta/', 'why-resysta/', 'contact-resysta-usa/',
                'find-a-distributor', 'cad-bim', 'technical-center/',
                'installation-guides', 'testing-certification',
                'sustainability-leed', 'sustainable-award-for-resysta/',
                'resysta-material-in-comparison/', 'typical-drawing-details/',
                'screen-wall-dividers/', 'trellis-canopy/',
                'soffits-ceilings/', 'siding-profiles/', 'wall-cladding-profiles/',
                'decking-profiles-and-boards/', 'composite-fencing-boards/',
                'resysta-products/', 'resysta-course/', 'aia-course',
                'sample-order-thank-you/', 'form-contact-thank-you/',
                'exit-intent', 'resysta-owner/', 'trucolor-decking/',
                'interior-facing/', 'get-samples-thank-you', 'order-confirmation',
                'our-best-projects/', 'resysta-decking-installation-video',
                'facade/', 'warranty-registration/', 'care-and-cleaning/', 'faq/',
                'decking-siding', 'homepage', 'resysta-florida/', 'resysta-california/',
                'resysta-washington-state/', 'automation-testing/',
                'find-a-distributor-2/', 'decking-facade-profiles/',
                'products/', '/product/', 'portfolio/', 'portfolio-category/',
                'ulc-link-type/', 'color-selector/', 'soffit-ceilings/',
                'resysta-florida', 'resysta-california', 'resysta-washington',
            ]

            for row in data[1:]:
                url = row[0]
                # Extract slug
                path_match = re.match(r'https?://resystausa\.com/([^/?#]+)/?$', url)
                if not path_match:
                    continue
                slug = path_match.group(1).rstrip('/')

                # Skip non-blog patterns
                is_blog = True
                for nb in non_blog_indicators:
                    if nb in url or nb.rstrip('/') == slug:
                        is_blog = False
                        break

                # Blog posts have substantial hyphenated slugs
                if is_blog and len(slug) >= 15 and slug.count('-') >= 2:
                    found_slugs.add(slug)

            print(f"  CDX found {len(found_slugs)} potential blog posts")
        else:
            print(f"  CDX API error: {resp.status_code}")
    except Exception as e:
        print(f"  CDX API exception: {e}")

    return found_slugs


def enumerate_urls_live_rest(session):
    """Method B: WP REST API via IP bypass (known to return 0, kept for completeness)."""
    print("\n[Method B] Checking WP REST API (expected empty)...")
    slugs = set()

    try:
        resp = session.get(
            f"https://resystausa.com/wp-json/wp/v2/posts",
            params={"per_page": 100, "page": 1, "_fields": "id,slug,link,title"},
            timeout=15,
            verify=False
        )
        if resp.status_code == 200:
            data = resp.json()
            print(f"  REST API posts: {len(data)}")
            for post in data:
                slug = post.get("slug", "")
                if slug:
                    slugs.add(slug)
        else:
            print(f"  REST API status: {resp.status_code}")
    except Exception as e:
        print(f"  REST API exception: {e}")

    return slugs


def get_wayback_timestamp(slug, session):
    """Get the best available Wayback timestamp for a URL."""
    try:
        resp = session.get(
            "https://web.archive.org/cdx/search/cdx",
            params={
                "url": f"resystausa.com/{slug}/",
                "output": "json",
                "fl": "timestamp,statuscode",
                "limit": 10,
                "filter": "statuscode:200",
            },
            timeout=20
        )
        if resp.status_code == 200:
            data = resp.json()
            rows = data[1:]  # Skip header
            if rows:
                # Return most recent timestamp
                return rows[0][0]
    except Exception as e:
        pass
    return None


def download_from_live(slug, session):
    """Try to download blog post from live site via IP bypass."""
    url = f"{LIVE_BASE_URL}/{slug}/"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=20, allow_redirects=True)
        if resp.status_code == 200:
            content = resp.text
            # Check for CF challenge
            if "_cf_chl_opt" in content or "Just a moment" in content:
                print(f"    CF challenge on live site")
                return None
            # Check it's actual content (not a redirect to homepage)
            if len(content) > 10000 and "resystausa.com" in content:
                return content
    except Exception as e:
        pass
    return None


def download_from_wayback(slug, timestamp, session):
    """Download blog post from Wayback Machine."""
    if not timestamp:
        # Try without specific timestamp (Wayback will use latest)
        wayback_url = f"https://web.archive.org/web/2025/{LIVE_DOMAIN}/{slug}/"
    else:
        wayback_url = f"https://web.archive.org/web/{timestamp}/{LIVE_DOMAIN}/{slug}/"

    try:
        resp = session.get(wayback_url, timeout=30, verify=False, allow_redirects=True)
        if resp.status_code == 200:
            content = resp.text
            # Check for Wayback toolbar noise but actual content
            if "web.archive.org" in wayback_url and len(content) > 5000:
                # Check for CF challenge
                if "_cf_chl_opt" in content or "Just a moment" in content:
                    print(f"    CF challenge in Wayback snapshot")
                    return None
                # Check for Wayback "Page not found" or "not available"
                if "This URL has been excluded" in content or "Hrm, Wayback Machine doesn" in content:
                    return None
                return content
    except Exception as e:
        pass
    return None


def rewrite_wayback_urls(html_content, slug):
    """Remove Wayback Machine URL wrappers from links."""
    if "web.archive.org" not in html_content:
        return html_content

    # Remove Wayback banners and toolbars
    soup = BeautifulSoup(html_content, 'lxml')

    # Remove Wayback toolbar elements
    for el in soup.find_all(id=['wm-ipp-base', 'wm-ipp', 'donato-loading-bar']):
        el.decompose()
    for el in soup.find_all(class_=['wb-autocomplete-suggestion']):
        el.decompose()

    # Rewrite Wayback URLs back to original
    # Pattern: /web/TIMESTAMP/https://resystausa.com/... -> https://resystausa.com/...
    content = str(soup)

    # Fix href and src attributes
    content = re.sub(
        r'(href|src|action)=["\']https?://web\.archive\.org/web/\d+/(https?://resystausa\.com[^"\']*)["\']',
        r'\1="\2"',
        content
    )
    content = re.sub(
        r'(href|src|action)=["\']https?://web\.archive\.org/web/\d+/(https?://[^"\']*)["\']',
        r'\1="\2"',
        content
    )

    # Fix remaining /web/TIMESTAMP/ patterns
    content = re.sub(r'/web/\d+/https://resystausa\.com/', '/', content)
    content = re.sub(r'/web/\d+/', '/', content)

    return content


def download_image(img_url, session, base_save_path):
    """Download a wp-content/uploads image if not already saved."""
    if not img_url or 'wp-content/uploads' not in img_url:
        return False

    # Normalize URL
    if img_url.startswith('//'):
        img_url = 'https:' + img_url
    elif img_url.startswith('/'):
        img_url = 'https://resystausa.com' + img_url

    # Extract path after domain
    path_match = re.search(r'wp-content/uploads/(.+)$', img_url)
    if not path_match:
        return False

    rel_path = path_match.group(1).split('?')[0]  # Remove query params
    save_path = base_save_path / "wp-content" / "uploads" / rel_path

    if save_path.exists():
        return True  # Already downloaded

    save_path.parent.mkdir(parents=True, exist_ok=True)

    # Try live site first
    for attempt_url in [
        f"http://{LIVE_BASE_URL}/wp-content/uploads/{rel_path}",
        f"https://resystausa.com/wp-content/uploads/{rel_path}",
    ]:
        try:
            headers = HEADERS.copy() if '74.208' in attempt_url else WAYBACK_HEADERS.copy()
            resp = requests.get(attempt_url, headers=headers, timeout=30, stream=True, verify=False)
            if resp.status_code == 200:
                with open(save_path, 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True
        except Exception:
            continue

    return False


def save_post(slug, html_content):
    """Save blog post HTML to the backup directory."""
    # Create directory: blog/SLUG/
    post_dir = BLOG_DIR / slug
    post_dir.mkdir(parents=True, exist_ok=True)

    index_path = post_dir / "index.html"
    with open(index_path, 'w', encoding='utf-8', errors='replace') as f:
        f.write(html_content)

    return index_path


def download_post_images(slug, html_content, session):
    """Download all inline images referenced in the blog post."""
    downloaded = 0
    soup = BeautifulSoup(html_content, 'lxml')

    img_urls = set()
    for img in soup.find_all('img', src=True):
        src = img.get('src', '')
        if src:
            img_urls.add(src)
        # Check srcset
        srcset = img.get('srcset', '')
        for part in srcset.split(','):
            url = part.strip().split()[0] if part.strip() else ''
            if url:
                img_urls.add(url)

    for img_url in img_urls:
        if 'wp-content/uploads' in img_url:
            success = download_image(img_url, session, BACKUP_ROOT)
            if success:
                downloaded += 1

    return downloaded


def scrape_blog_posts(enumerate_only=False, skip_existing=True):
    """Main function to enumerate and download all blog posts."""
    session = get_session()

    print("=" * 60)
    print("resystausa.com Blog Post Scraper")
    print("=" * 60)

    # Step 1: Enumerate all URLs
    print("\n--- Phase 1: URL Enumeration ---")

    # Start with known slugs
    all_slugs = set(KNOWN_BLOG_SLUGS)
    print(f"Known slugs from CDX analysis: {len(KNOWN_BLOG_SLUGS)}")

    # Method A: CDX API (may find additional slugs)
    cdx_slugs = enumerate_urls_from_cdx(session)
    new_from_cdx = cdx_slugs - all_slugs
    if new_from_cdx:
        print(f"  Additional slugs from CDX: {new_from_cdx}")
    all_slugs.update(cdx_slugs)

    # Method B: REST API
    time.sleep(1)
    rest_slugs = enumerate_urls_live_rest(session)
    if rest_slugs:
        new_from_rest = rest_slugs - all_slugs
        print(f"  Additional slugs from REST API: {new_from_rest}")
    all_slugs.update(rest_slugs)

    # Sort and display final list
    sorted_slugs = sorted(all_slugs)
    print(f"\n--- Enumeration Complete ---")
    print(f"Total unique blog post URLs: {len(sorted_slugs)}")
    print()
    for i, slug in enumerate(sorted_slugs, 1):
        print(f"  {i:3d}. https://resystausa.com/{slug}/")

    if enumerate_only:
        print(f"\n[--enumerate-only mode] Stopping after enumeration.")
        return sorted_slugs

    # Step 2: Download each post
    print("\n--- Phase 2: Downloading Posts ---")

    stats = {
        "downloaded_live": 0,
        "downloaded_wayback": 0,
        "skipped_exists": 0,
        "skipped_cf": 0,
        "failed": 0,
        "images_downloaded": 0,
    }
    failed_urls = []

    BLOG_DIR.mkdir(parents=True, exist_ok=True)

    for i, slug in enumerate(sorted_slugs, 1):
        post_dir = BLOG_DIR / slug
        index_path = post_dir / "index.html"

        # Skip if already downloaded
        if skip_existing and index_path.exists() and index_path.stat().st_size > 5000:
            print(f"[{i:3d}/{len(sorted_slugs)}] SKIP (exists): {slug}")
            stats["skipped_exists"] += 1
            continue

        print(f"[{i:3d}/{len(sorted_slugs)}] Downloading: {slug}", end="")

        html_content = None
        source = None

        # Try live site first (direct IP bypass)
        html_content = download_from_live(slug, session)
        if html_content:
            source = "live"
            print(f" -> LIVE ({len(html_content)} bytes)", end="")

        # Fall back to Wayback Machine
        if not html_content:
            # Get best timestamp
            timestamp = get_wayback_timestamp(slug, session)
            if timestamp:
                html_content = download_from_wayback(slug, timestamp, session)
                if html_content:
                    source = f"wayback:{timestamp}"
                    print(f" -> WAYBACK/{timestamp[:8]} ({len(html_content)} bytes)", end="")

        # Try Wayback without specific timestamp
        if not html_content:
            # Try most recent wayback archive
            for year in ["2025", "2026", "2024"]:
                try:
                    wayback_url = f"https://web.archive.org/web/{year}/https://resystausa.com/{slug}/"
                    resp = session.get(wayback_url, timeout=30, verify=False, allow_redirects=True)
                    if resp.status_code == 200 and len(resp.text) > 5000:
                        content = resp.text
                        if "_cf_chl_opt" not in content and "Just a moment" not in content:
                            if "Hrm, Wayback Machine" not in content and "URL has been excluded" not in content:
                                html_content = content
                                source = f"wayback:{year}"
                                print(f" -> WAYBACK/{year} ({len(html_content)} bytes)", end="")
                                break
                except Exception:
                    continue

        if not html_content:
            print(f" -> FAILED (not found on live or Wayback)")
            stats["failed"] += 1
            failed_urls.append(f"https://resystausa.com/{slug}/")
            time.sleep(random.uniform(1.5, 2.5))
            continue

        # Rewrite Wayback URLs if from archive
        if source and "wayback" in source:
            html_content = rewrite_wayback_urls(html_content, slug)

        # Save the post
        try:
            save_post(slug, html_content)

            if source and "wayback" in source:
                stats["downloaded_wayback"] += 1
            else:
                stats["downloaded_live"] += 1

            # Download inline images
            img_count = download_post_images(slug, html_content, session)
            stats["images_downloaded"] += img_count
            if img_count > 0:
                print(f" [{img_count} imgs]", end="")

            print()  # newline after status

        except Exception as e:
            print(f" -> SAVE ERROR: {e}")
            stats["failed"] += 1
            failed_urls.append(f"https://resystausa.com/{slug}/")

        # Rate limiting
        time.sleep(random.uniform(2.0, 3.5))

    # Step 3: Summary
    print("\n" + "=" * 60)
    print("DOWNLOAD SUMMARY")
    print("=" * 60)
    print(f"Total posts enumerated: {len(sorted_slugs)}")
    print(f"Downloaded from live site: {stats['downloaded_live']}")
    print(f"Downloaded from Wayback:   {stats['downloaded_wayback']}")
    print(f"Skipped (already exists):  {stats['skipped_exists']}")
    print(f"Failed / Not found:        {stats['failed']}")
    print(f"Images downloaded:          {stats['images_downloaded']}")

    if failed_urls:
        print("\nFailed URLs (not on live site or Wayback):")
        for url in failed_urls:
            print(f"  {url}")

    # Verify no CF challenge pages
    print("\n--- Validation ---")
    blog_posts = list(BLOG_DIR.glob("*/index.html"))
    print(f"Blog post files: {len(blog_posts)}")

    cf_pages = []
    small_pages = []
    for html_file in blog_posts:
        if html_file.stat().st_size < 1024:
            small_pages.append(html_file)
        else:
            content = html_file.read_text(encoding='utf-8', errors='ignore')
            if "_cf_chl_opt" in content or "Just a moment" in content:
                cf_pages.append(html_file)

    if cf_pages:
        print(f"WARNING: {len(cf_pages)} CF challenge pages found!")
        for f in cf_pages:
            print(f"  {f}")
    else:
        print("No CF challenge pages detected.")

    if small_pages:
        print(f"WARNING: {len(small_pages)} files < 1KB:")
        for f in small_pages:
            print(f"  {f} ({f.stat().st_size} bytes)")

    # Check for real blog content
    content_check = list(BLOG_DIR.glob("*/index.html"))[:5]
    has_content = [f for f in content_check
                   if any(term in f.read_text(encoding='utf-8', errors='ignore')
                          for term in ['entry-content', 'post-content', 'article', 'resystausa'])]
    print(f"Files with real blog content (sample): {len(has_content)}/{min(5, len(content_check))}")

    return sorted_slugs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape resystausa.com blog posts")
    parser.add_argument("--enumerate-only", action="store_true",
                        help="Only enumerate URLs, don't download")
    parser.add_argument("--no-skip-existing", action="store_true",
                        help="Re-download even if file exists")
    args = parser.parse_args()

    scrape_blog_posts(
        enumerate_only=args.enumerate_only,
        skip_existing=not args.no_skip_existing
    )
