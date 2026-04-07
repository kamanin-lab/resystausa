#!/usr/bin/env python3
"""
cleanup-site.py — Hide WooCommerce wishlist/cart/calculator buttons and remove
social tracking scripts from all HTML files in the static site backup.

Pass A — CSS injection (idempotent via marker <!-- gsd:cleanup-site -->):
  Injects a <style> block before </head> on files that contain WooCommerce or
  cost-calculator class names. Skips files already containing the marker.

Pass B — Social tracking script removal (idempotent via absence check):
  Removes Facebook Pixel, Google Tag Manager / GA4, Cloudflare beacon, and
  related DNS prefetch tags. Skips files that contain none of the signatures.

Targets:
  .yith-wcwl-add-button       — WooCommerce wishlist heart-icon button
  .yith-wcwl-add-to-wishlist  — WooCommerce wishlist container
  .ajax_add_to_cart           — WooCommerce add-to-cart button (listings)
  .single_add_to_cart_button  — WooCommerce add-to-cart button (single product)
  #costCalculator             — Cost calculator widget (ID)
  .ql-cost-calculator         — Cost calculator widget (class)
  Facebook Pixel inline script and noscript
  Google Tag Manager / GA4 scripts
  Cloudflare beacon script
  DNS prefetch links for facebook.net and googletagmanager.com
"""

import os
import re
import sys

SITE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")

# ── Pass A ──────────────────────────────────────────────────────────────────
CSS_MARKER = "<!-- gsd:cleanup-site -->"

CSS_TARGETS = (
    "yith-wcwl",
    "ajax_add_to_cart",
    "single_add_to_cart_button",
    "costCalculator",
    "ql-cost-calculator",
)

STYLE_BLOCK = """\
<!-- gsd:cleanup-site -->
<style>
/* Hide WooCommerce wishlist buttons */
.yith-wcwl-add-button { display: none !important; }
.yith-wcwl-add-to-wishlist { display: none !important; }
/* Hide WooCommerce cart buttons */
.ajax_add_to_cart { display: none !important; }
.single_add_to_cart_button { display: none !important; }
/* Hide cost calculator widget */
#costCalculator { display: none !important; }
.ql-cost-calculator { display: none !important; }
</style>"""

# ── Pass B ──────────────────────────────────────────────────────────────────
# Idempotency signatures — if none present, skip all regex passes
SCRIPT_SIGNATURES = ("fbq(", "googletagmanager", "data-cf-beacon")

# 1. Facebook Pixel block: the HTML comment wrapper captures everything
#    between <!-- Meta Pixel Code --> and <!-- End Meta Pixel Code -->
RE_FB_PIXEL_BLOCK = re.compile(
    r"<!-- Meta Pixel Code -->[\s\S]*?<!-- End Meta Pixel Code -->",
    re.DOTALL,
)

# 1b. Facebook Pixel loader IIFE (when not wrapped in comment)
#     Matches: <script>!function(f,b,e,v,n,t,s){...}(window,...fbevents.js...);</script>
RE_FB_PIXEL_LOADER = re.compile(
    r"<script[^>]*>\s*!function\(f,b,e,v,n,t,s\)[\s\S]*?fbevents\.js[^\)]*\);\s*</script>",
    re.DOTALL,
)

# 1c. Any remaining <script> that calls fbq('init',...), fbq('set',...),
#     fbq('track',...), or fbq('trackSingle',...)
RE_FB_FBQ_CALLS = re.compile(
    r"<script[^>]*>(?:[^<]|<(?!/script))*?fbq\(['\"](?:init|set|track|trackSingle)['\"][\s\S]*?</script>",
    re.DOTALL,
)

# 2. Facebook noscript pixel image
RE_FB_NOSCRIPT = re.compile(
    r"<noscript>\s*<img[^>]*facebook\.com/tr\?id=[^>]*>\s*</noscript>",
    re.DOTALL,
)

# 3. Google Tag Manager block: the HTML comment wrapper
RE_GTM_COMMENT_BLOCK = re.compile(
    r"<!-- Google Tag Manager -->[\s\S]*?<!-- End Google Tag Manager -->",
    re.DOTALL,
)

# 3b. GTM inline IIFE (when not wrapped in comment):
#     (function(w,d,s,l,i){w[l]=w[l]||[]...gtm.js...})(...)
RE_GTM_IIFE = re.compile(
    r"<script[^>]*>\s*\(function\(w,d,s,l,i\)\{w\[l\]=w\[l\]\|\|[\s\S]*?googletagmanager\.com/gtm\.js[\s\S]*?\}\)\([^)]*\);\s*</script>",
    re.DOTALL,
)

# 3c. External GTM/GA4 script tag with src attribute
RE_GTM_EXTERNAL = re.compile(
    r"<script[^>]*src=[\"'][^\"']*googletagmanager\.com/gtag/js[^\"']*[\"'][^>]*></script>",
    re.DOTALL,
)

# 3d. Inline window.dataLayer = ... / gtag() config block (GA4 pattern)
RE_GTM_DATALAYER = re.compile(
    r"<script[^>]*>\s*window\.dataLayer\s*=\s*window\.dataLayer[\s\S]*?</script>",
    re.DOTALL,
)

# 3e. Inline gtag('event', ...) conversion call
RE_GTAG_EVENT = re.compile(
    r"<script[^>]*>\s*gtag\('event'[\s\S]*?</script>",
    re.DOTALL,
)

# 4. Cloudflare beacon script
RE_CF_BEACON = re.compile(
    r"<script[^>]*data-cf-beacon[^>]*></script>",
    re.DOTALL,
)

# 5. DNS prefetch links for tracking domains
#    Matches both https?:// and protocol-relative // forms.
#    Negative lookahead excludes Wayback Machine wrappers (web.archive.org/...)
#    which contain googletagmanager.com as part of an archived URL, not a live hint.
RE_DNS_PREFETCH = re.compile(
    r"<link[^>]*href=[\"'](?:https?:)?//(?!web\.archive\.org)(?:connect\.facebook\.net|www\.googletagmanager\.com)[^\"']*[\"'][^>]*/?>",
    re.DOTALL,
)


def process_file(path):
    """
    Returns a dict with keys:
      css_result    : "patched" | "already-patched" | "skipped" | "no-head-tag"
      script_result : "cleaned" | "already-clean" | "skipped"
    """
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    original = content
    css_result = "skipped"
    script_result = "skipped"

    # ── Pass A ──────────────────────────────────────────────────────────────
    has_woo = any(t in content for t in CSS_TARGETS)
    if has_woo:
        if CSS_MARKER in content:
            css_result = "already-patched"
        elif "</head>" not in content:
            css_result = "no-head-tag"
        else:
            content = content.replace("</head>", STYLE_BLOCK + "\n</head>", 1)
            css_result = "patched"

    # ── Pass B ──────────────────────────────────────────────────────────────
    # Snapshot content before Pass A changes for accurate Pass B comparison
    pre_script_content = content
    needs_script_removal = any(sig in content for sig in SCRIPT_SIGNATURES)
    if needs_script_removal:
        # Facebook Pixel — comment block first, then individual patterns
        content = RE_FB_PIXEL_BLOCK.sub("", content)
        content = RE_FB_PIXEL_LOADER.sub("", content)
        content = RE_FB_FBQ_CALLS.sub("", content)
        content = RE_FB_NOSCRIPT.sub("", content)
        # Google Tag Manager / GA4
        content = RE_GTM_COMMENT_BLOCK.sub("", content)
        content = RE_GTM_IIFE.sub("", content)
        content = RE_GTM_EXTERNAL.sub("", content)
        content = RE_GTM_DATALAYER.sub("", content)
        content = RE_GTAG_EVENT.sub("", content)
        # Cloudflare beacon
        content = RE_CF_BEACON.sub("", content)
        # DNS prefetch hints
        content = RE_DNS_PREFETCH.sub("", content)
        # Only count as "cleaned" if content actually changed
        if content != pre_script_content:
            script_result = "cleaned"
        else:
            script_result = "already-clean"
    else:
        script_result = "already-clean"

    # Write only if content changed from original (covers both passes)
    if content != original:
        with open(path, "w", encoding="utf-8", errors="replace") as f:
            f.write(content)

    return {"css_result": css_result, "script_result": script_result}


def main():
    css_counts = {"patched": 0, "already-patched": 0, "skipped": 0, "no-head-tag": 0}
    script_counts = {"cleaned": 0, "already-clean": 0, "skipped": 0}
    total = 0

    for root, dirs, files in os.walk(SITE_DIR):
        # Skip wp-admin, cdn-cgi — not public pages
        dirs[:] = [d for d in dirs if d not in ("wp-admin", "cdn-cgi")]
        for fname in files:
            if not fname.endswith(".html"):
                continue
            total += 1
            result = process_file(os.path.join(root, fname))
            css_counts[result["css_result"]] += 1
            script_counts[result["script_result"]] += 1

    print(f"Done. Scanned {total} HTML files.")
    print()
    print("Pass A -- CSS injection:")
    print(f"  CSS-patched:         {css_counts['patched']}")
    print(f"  Already CSS-patched: {css_counts['already-patched']}")
    print(f"  Skipped (no WooCommerce/calculator content): {css_counts['skipped']}")
    print(f"  No </head> tag (warned, skipped): {css_counts['no-head-tag']}")
    print()
    print("Pass B -- Script removal:")
    print(f"  Script-cleaned:      {script_counts['cleaned']}")
    print(f"  Already script-clean:{script_counts['already-clean']}")
    print(f"  Skipped (no tracking signatures): {script_counts['skipped']}")

    if css_counts["no-head-tag"]:
        print()
        print(f"  WARNING: {css_counts['no-head-tag']} file(s) had no </head> tag -- CSS NOT injected.")

    # Sanity check: all counts sum to total
    css_total = sum(css_counts.values())
    script_total = sum(script_counts.values())
    if css_total != total or script_total != total:
        print(f"\n  WARN: count mismatch -- total={total}, css_sum={css_total}, script_sum={script_total}")

    sys.exit(0)


if __name__ == "__main__":
    main()
