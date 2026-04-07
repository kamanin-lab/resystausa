#!/usr/bin/env bash
# ==============================================================================
# backup.sh — resystausa.com complete local backup
#
# Usage:  bash backup.sh
# Output: resysta-backup/
#   site/        — HTML pages + assets (wget / Python scraper)
#   wayback/     — Wayback Machine HTML snapshots (last resort)
#   sitemap.xml  — Primary sitemap (copy of first successful download)
#   url-list.txt — Deduplicated, filtered list of all discovered URLs
#   logs/        — wget logs, challenge page report
#
# Fallback chain (auto, no manual intervention):
#   1. wget IP mirror + wget domain mirror (parallel)
#   2. Python scraper (if wget yields >20% challenge pages or 0 HTML files)
#   3. Wayback Machine (if scraper still incomplete / site dead)
# ==============================================================================

set -euo pipefail

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------
IP_CANDIDATE_1="74.208.236.71"
IP_CANDIDATE_2="74.208.236.61"
DOMAIN="resystausa.com"
BACKUP_DIR="resysta-backup"
CHROME_UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# State variables (mutated by functions)
DIRECT_IP=""
ACCESS_METHOD=""
WGET_AVAILABLE=false
WGET_SUCCESS=false

# ------------------------------------------------------------------------------
# 1. log() — timestamped echo
# ------------------------------------------------------------------------------
log() {
  echo "[$(date +%H:%M:%S)] $*"
}

# ------------------------------------------------------------------------------
# 2. check_tools() — verify required tools, detect wget
# ------------------------------------------------------------------------------
check_tools() {
  log "=== Checking tools ==="

  # curl is required for connectivity probes, sitemaps, CDX
  if ! command -v curl &>/dev/null; then
    log "[ERROR] curl is not installed. Please install curl and retry."
    exit 1
  fi
  log "[OK] curl found: $(curl --version | head -1)"

  # python is required for scraper and wayback fallback
  if ! command -v python &>/dev/null; then
    log "[ERROR] python is not installed. Please install Python 3 and retry."
    exit 1
  fi
  log "[OK] python found: $(python --version 2>&1)"

  # wget is optional — gracefully degrade to Python scraper if absent
  if command -v wget &>/dev/null; then
    WGET_AVAILABLE=true
    log "[OK] wget found: $(wget --version 2>&1 | head -1)"
  else
    WGET_AVAILABLE=false
    log "[WARN] wget not found — will use Python scraper as primary download method"
    log "  To install wget (optional):"
    log "    1. Download from https://eternallybored.org/misc/wget/ (standalone .exe)"
    log "    2. Or install via Chocolatey: choco install wget"
    log "    3. Or install via scoop: scoop install wget"
    log "  Python scraper will run instead."
  fi
}

# ------------------------------------------------------------------------------
# 3. check_longpaths() — verify Windows LongPathsEnabled registry key
# ------------------------------------------------------------------------------
check_longpaths() {
  log "=== Checking Windows LongPathsEnabled ==="

  if ! command -v powershell &>/dev/null; then
    log "[SKIP] PowerShell not found — skipping LongPath check"
    return 0
  fi

  LONGPATH=$(powershell -Command \
    "(Get-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem' \
    -Name LongPathsEnabled -ErrorAction SilentlyContinue).LongPathsEnabled" \
    2>/dev/null || echo "")

  if [[ "$LONGPATH" == "1" ]]; then
    log "[OK] LongPathsEnabled = 1 — paths longer than 260 chars are supported"
  else
    log "[WARN] LongPathsEnabled is not set to 1 (value: '${LONGPATH:-not found}')"
    log "  To enable: Run PowerShell as Administrator and execute:"
    log "    Set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem' -Name LongPathsEnabled -Value 1"
    log "  Or enable via Group Policy: gpedit.msc > Computer Configuration >"
    log "    Administrative Templates > System > Filesystem > Enable Win32 long paths"
    log "  Note: Current output path is short (~48 chars); most URLs will fit within 260 chars."
    log "  Continuing without LongPathsEnabled — some deep URL paths may be truncated."
  fi
}

# ------------------------------------------------------------------------------
# 4. probe_connectivity() — probe both IP candidates and the domain
# ------------------------------------------------------------------------------
probe_connectivity() {
  log "=== Probing connectivity ==="

  local probe_file_1="/tmp/probe_${IP_CANDIDATE_1}.html"
  local probe_file_2="/tmp/probe_${IP_CANDIDATE_2}.html"
  local probe_file_domain="/tmp/probe_domain.html"

  # Probe IP_CANDIDATE_1 (74.208.236.71)
  log "Probing $IP_CANDIDATE_1 ..."
  local status_1
  status_1=$(curl -s \
    -o "$probe_file_1" \
    -w "%{http_code}" \
    --connect-timeout 10 \
    -H "Host: $DOMAIN" \
    -A "$CHROME_UA" \
    "http://${IP_CANDIDATE_1}/" 2>/dev/null || echo "000")

  # Probe IP_CANDIDATE_2 (74.208.236.61)
  log "Probing $IP_CANDIDATE_2 ..."
  local status_2
  status_2=$(curl -s \
    -o "$probe_file_2" \
    -w "%{http_code}" \
    --connect-timeout 10 \
    -H "Host: $DOMAIN" \
    -A "$CHROME_UA" \
    "http://${IP_CANDIDATE_2}/" 2>/dev/null || echo "000")

  # Probe domain (via Cloudflare)
  log "Probing https://$DOMAIN ..."
  local status_domain
  status_domain=$(curl -s \
    -o "$probe_file_domain" \
    -w "%{http_code}" \
    --connect-timeout 10 \
    -A "$CHROME_UA" \
    "https://${DOMAIN}/" 2>/dev/null || echo "000")

  log "Results: IP1=$status_1  IP2=$status_2  domain=$status_domain"

  # Evaluate which IP has real WordPress content (not a challenge page)
  local ip1_real=false
  local ip2_real=false

  if [[ "$status_1" == "200" ]] && [[ -f "$probe_file_1" ]]; then
    if grep -q "wp-content" "$probe_file_1" 2>/dev/null && \
       ! grep -q "Just a moment" "$probe_file_1" 2>/dev/null; then
      ip1_real=true
    fi
  fi

  if [[ "$status_2" == "200" ]] && [[ -f "$probe_file_2" ]]; then
    if grep -q "wp-content" "$probe_file_2" 2>/dev/null && \
       ! grep -q "Just a moment" "$probe_file_2" 2>/dev/null; then
      ip2_real=true
    fi
  fi

  # Prefer IP_CANDIDATE_1 if both work; fall back to IP_CANDIDATE_2; then domain
  if [[ "$ip1_real" == "true" ]]; then
    DIRECT_IP="$IP_CANDIDATE_1"
    ACCESS_METHOD="ip"
    log "[OK] Direct IP access via $DIRECT_IP (WordPress confirmed)"
  elif [[ "$ip2_real" == "true" ]]; then
    DIRECT_IP="$IP_CANDIDATE_2"
    ACCESS_METHOD="ip"
    log "[OK] Direct IP access via $DIRECT_IP (WordPress confirmed)"
  elif [[ "$status_1" == "200" ]] || [[ "$status_2" == "200" ]]; then
    # Got 200 but no wp-content — likely challenge page — still try IP
    if [[ "$status_1" == "200" ]]; then
      DIRECT_IP="$IP_CANDIDATE_1"
    else
      DIRECT_IP="$IP_CANDIDATE_2"
    fi
    ACCESS_METHOD="ip"
    log "[WARN] IP returned 200 but no wp-content detected — may be challenge page"
    log "  Will proceed with IP access; challenge-page scanner will catch issues."
  elif [[ "$status_domain" == "200" ]]; then
    DIRECT_IP=""
    ACCESS_METHOD="domain"
    log "[WARN] Direct IP unreachable — only domain access is available (behind Cloudflare)"
    log "  wget/scraper will target domain; challenge pages are more likely"
  else
    DIRECT_IP=""
    ACCESS_METHOD="dead"
    log "[ERROR] Neither IP candidates nor domain responded — site appears unreachable"
    log "  Will attempt Wayback Machine fallback only."
  fi
}

# ------------------------------------------------------------------------------
# 5. download_sitemaps() — try all three WordPress sitemap entry points
# ------------------------------------------------------------------------------
download_sitemaps() {
  log "=== Downloading sitemaps ==="

  local target_base
  if [[ -n "$DIRECT_IP" ]]; then
    target_base="http://${DIRECT_IP}"
  else
    target_base="https://${DOMAIN}"
  fi

  local first_sitemap=""

  for sitemap_name in sitemap.xml sitemap_index.xml wp-sitemap.xml; do
    local target_url="${target_base}/${sitemap_name}"
    local local_file="${BACKUP_DIR}/${sitemap_name}"

    local status
    if [[ -n "$DIRECT_IP" ]]; then
      status=$(curl -s \
        -o "$local_file" \
        -w "%{http_code}" \
        --connect-timeout 15 \
        -H "Host: $DOMAIN" \
        -A "$CHROME_UA" \
        "$target_url" 2>/dev/null || echo "000")
    else
      status=$(curl -s \
        -o "$local_file" \
        -w "%{http_code}" \
        --connect-timeout 15 \
        -A "$CHROME_UA" \
        "$target_url" 2>/dev/null || echo "000")
    fi

    if [[ "$status" == "200" ]] && [[ -s "$local_file" ]]; then
      log "[OK] Downloaded $sitemap_name (HTTP $status)"

      # Extract <loc> URLs
      grep -oP '(?<=<loc>)[^<]+' "$local_file" \
        >> "${BACKUP_DIR}/url-list-raw.txt" 2>/dev/null || true

      # Track first successful sitemap for canonical copy
      [[ -z "$first_sitemap" ]] && first_sitemap="$sitemap_name"

      # Follow child sitemaps if this is a sitemap index
      if grep -q "<sitemap>" "$local_file" 2>/dev/null; then
        log "  -> Sitemap index detected — following child sitemaps..."
        while IFS= read -r child_url; do
          [[ -z "$child_url" ]] && continue
          local child_file="${BACKUP_DIR}/$(basename "$child_url")"

          # Rewrite domain URL to IP for direct access
          local child_target="$child_url"
          if [[ -n "$DIRECT_IP" ]]; then
            child_target="${child_url/https:\/\/$DOMAIN/http:\/\/$DIRECT_IP}"
            child_target="${child_target/http:\/\/$DOMAIN/http:\/\/$DIRECT_IP}"
          fi

          local child_status
          if [[ -n "$DIRECT_IP" ]]; then
            child_status=$(curl -s \
              -o "$child_file" \
              -w "%{http_code}" \
              --connect-timeout 15 \
              -H "Host: $DOMAIN" \
              -A "$CHROME_UA" \
              "$child_target" 2>/dev/null || echo "000")
          else
            child_status=$(curl -s \
              -o "$child_file" \
              -w "%{http_code}" \
              --connect-timeout 15 \
              -A "$CHROME_UA" \
              "$child_target" 2>/dev/null || echo "000")
          fi

          if [[ "$child_status" == "200" ]] && [[ -s "$child_file" ]]; then
            log "    [OK] Child sitemap: $(basename "$child_url")"
            grep -oP '(?<=<loc>)[^<]+' "$child_file" \
              >> "${BACKUP_DIR}/url-list-raw.txt" 2>/dev/null || true
          fi
        done < <(grep -oP '(?<=<loc>)[^<]+' "$local_file" 2>/dev/null || true)
      fi
    else
      log "[SKIP] $sitemap_name returned HTTP $status"
      rm -f "$local_file"
    fi
  done

  # Create canonical sitemap.xml if not already present
  if [[ -n "$first_sitemap" ]] && [[ "$first_sitemap" != "sitemap.xml" ]]; then
    if [[ -f "${BACKUP_DIR}/${first_sitemap}" ]]; then
      cp "${BACKUP_DIR}/${first_sitemap}" "${BACKUP_DIR}/sitemap.xml"
      log "[INFO] Copied $first_sitemap -> sitemap.xml"
    fi
  fi

  local url_count=0
  [[ -f "${BACKUP_DIR}/url-list-raw.txt" ]] && \
    url_count=$(wc -l < "${BACKUP_DIR}/url-list-raw.txt")
  log "[INFO] url-list-raw.txt now has $url_count entries after sitemaps"
}

# ------------------------------------------------------------------------------
# 6. run_wget_mirror() — dual wget passes (IP + domain) in parallel
# ------------------------------------------------------------------------------
run_wget_mirror() {
  if [[ "$WGET_AVAILABLE" == "false" ]]; then
    log "[SKIP] wget not available — proceeding to Python scraper"
    WGET_SUCCESS=false
    return 0
  fi

  log "=== Running wget mirror (IP + domain, parallel) ==="

  local target_ip
  if [[ -n "$DIRECT_IP" ]]; then
    target_ip="$DIRECT_IP"
  else
    # No direct IP — only run domain pass
    log "[INFO] No direct IP available — running domain-only wget pass"
    wget \
      --mirror \
      --page-requisites \
      --convert-links \
      --adjust-extension \
      --no-parent \
      -nH \
      --trust-server-names \
      --restrict-file-names=windows \
      --wait=2 \
      --random-wait \
      --limit-rate=500k \
      -e robots=off \
      --no-check-certificate \
      --header="User-Agent: $CHROME_UA" \
      --header="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8" \
      --header="Accept-Language: en-US,en;q=0.5" \
      --exclude-directories="/feed,/wp-json,/search,/trackback,/comments/feed" \
      --reject-regex="(\?s=|\?replytocom=|/wp-json/|/feed/?$|/trackback/|\?share=|\?like=|\?wc-ajax=)" \
      --reject="php" \
      -P "${BACKUP_DIR}/site" \
      -o "${BACKUP_DIR}/logs/wget-domain.log" \
      "https://${DOMAIN}/" || true
    log "[INFO] Domain wget pass completed"
    return 0
  fi

  # Launch IP-based wget in background
  log "[INFO] Starting wget IP pass (http://${target_ip}/) ..."
  wget \
    --mirror \
    --page-requisites \
    --convert-links \
    --adjust-extension \
    --no-parent \
    -nH \
    --trust-server-names \
    --restrict-file-names=windows \
    --wait=1 \
    --random-wait \
    --limit-rate=500k \
    -e robots=off \
    --header="Host: $DOMAIN" \
    --header="User-Agent: $CHROME_UA" \
    --header="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8" \
    --header="Accept-Language: en-US,en;q=0.5" \
    --exclude-directories="/feed,/wp-json,/search,/trackback,/comments/feed" \
    --reject-regex="(\?s=|\?replytocom=|/wp-json/|/feed/?$|/trackback/|\?share=|\?like=|\?wc-ajax=)" \
    --reject="php" \
    -P "${BACKUP_DIR}/site" \
    -o "${BACKUP_DIR}/logs/wget-ip.log" \
    "http://${target_ip}/" &
  WGET_IP_PID=$!
  log "[INFO] wget IP pass running (PID $WGET_IP_PID)"

  # Launch domain-based wget in background
  log "[INFO] Starting wget domain pass (https://$DOMAIN/) ..."
  wget \
    --mirror \
    --page-requisites \
    --convert-links \
    --adjust-extension \
    --no-parent \
    -nH \
    --trust-server-names \
    --restrict-file-names=windows \
    --wait=2 \
    --random-wait \
    --limit-rate=500k \
    -e robots=off \
    --no-check-certificate \
    --header="User-Agent: $CHROME_UA" \
    --header="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8" \
    --header="Accept-Language: en-US,en;q=0.5" \
    --exclude-directories="/feed,/wp-json,/search,/trackback,/comments/feed" \
    --reject-regex="(\?s=|\?replytocom=|/wp-json/|/feed/?$|/trackback/|\?share=|\?like=|\?wc-ajax=)" \
    --reject="php" \
    --no-clobber \
    -P "${BACKUP_DIR}/site" \
    -o "${BACKUP_DIR}/logs/wget-domain.log" \
    "https://${DOMAIN}/" &
  WGET_DOMAIN_PID=$!
  log "[INFO] wget domain pass running (PID $WGET_DOMAIN_PID)"

  # Wait for both
  log "[INFO] Waiting for both wget passes to complete..."
  wait "$WGET_IP_PID"; WGET_IP_EXIT=$?
  wait "$WGET_DOMAIN_PID"; WGET_DOMAIN_EXIT=$?

  log "[INFO] wget IP pass exit code: $WGET_IP_EXIT"
  log "[INFO] wget domain pass exit code: $WGET_DOMAIN_EXIT"
}

# ------------------------------------------------------------------------------
# 7. scan_challenge_pages() — detect Cloudflare challenge page contamination
# ------------------------------------------------------------------------------
scan_challenge_pages() {
  log "=== Scanning for Cloudflare challenge pages ==="

  local site_dir="${BACKUP_DIR}/site"

  # Count total HTML files
  local total_html=0
  if [[ -d "$site_dir" ]]; then
    total_html=$(find "$site_dir" -name "*.html" 2>/dev/null | wc -l)
  fi

  log "[INFO] Total HTML files in site/: $total_html"

  if [[ $total_html -eq 0 ]]; then
    log "[FAIL] wget downloaded 0 HTML files — triggering fallback"
    WGET_SUCCESS=false
    return 0
  fi

  # Find challenge pages
  local challenge_file="${BACKUP_DIR}/logs/challenge-pages.txt"
  grep -rl \
    "_cf_chl_opt\|cf-browser-verification\|Just a moment\|Checking your browser" \
    "$site_dir" 2>/dev/null \
    | grep "\.html$" \
    | head -100 \
    > "$challenge_file" || true

  local challenge_count=0
  [[ -f "$challenge_file" ]] && challenge_count=$(wc -l < "$challenge_file")

  if [[ $challenge_count -eq 0 ]]; then
    log "[OK] No challenge pages detected — wget succeeded"
    WGET_SUCCESS=true
  else
    local ratio=$(( challenge_count * 100 / total_html ))
    log "[WARN] Challenge pages: $challenge_count / $total_html HTML files ($ratio%)"
    if [[ $ratio -gt 20 ]]; then
      log "[FAIL] >20% challenge pages — wget blocked by Cloudflare. Triggering fallback."
      WGET_SUCCESS=false
    else
      log "[OK] <20% challenge pages ($ratio%) — wget mostly succeeded. Proceeding."
      WGET_SUCCESS=true
    fi
  fi
}

# ------------------------------------------------------------------------------
# 8. run_python_scraper() — Python requests+BeautifulSoup fallback
# ------------------------------------------------------------------------------
run_python_scraper() {
  log "=== Running Python scraper fallback ==="

  if [[ -z "$DIRECT_IP" ]]; then
    log "[WARN] No direct IP available — Python scraper cannot bypass Cloudflare TLS"
    log "  Scraper will target https://$DOMAIN — challenge pages likely"
    python "$SCRIPT_DIR/scraper.py" \
      --ip "$IP_CANDIDATE_1" \
      --seed-file "${BACKUP_DIR}/url-list-raw.txt" \
      --output-dir "${BACKUP_DIR}/site" \
      --max-pages 2000 || true
    return 0
  fi

  log "[INFO] Running scraper.py targeting http://$DIRECT_IP/"
  python "$SCRIPT_DIR/scraper.py" \
    --ip "$DIRECT_IP" \
    --seed-file "${BACKUP_DIR}/url-list-raw.txt" \
    --output-dir "${BACKUP_DIR}/site" \
    --max-pages 2000 || true

  local scraper_exit=$?
  log "[INFO] Python scraper exit code: $scraper_exit"
}

# ------------------------------------------------------------------------------
# 9. run_wayback_fallback() — Wayback Machine last resort
# ------------------------------------------------------------------------------
run_wayback_fallback() {
  log "=== Running Wayback Machine fallback ==="
  python "$SCRIPT_DIR/wayback_download.py" \
    --output-dir "${BACKUP_DIR}/wayback" || true

  local wb_exit=$?
  log "[INFO] wayback_download.py exit code: $wb_exit"
}

# ------------------------------------------------------------------------------
# 10. download_uploads() — targeted sweep of wp-content/uploads/
# ------------------------------------------------------------------------------
download_uploads() {
  log "=== Downloading wp-content/uploads/ ==="

  if [[ "$ACCESS_METHOD" == "dead" ]]; then
    log "[SKIP] Site unreachable — skipping uploads sweep"
    return 0
  fi

  if [[ "$WGET_AVAILABLE" == "true" ]] && [[ -n "$DIRECT_IP" ]]; then
    log "[INFO] Running wget uploads sweep (http://${DIRECT_IP}/wp-content/uploads/)"
    wget \
      -r -np -nH \
      --restrict-file-names=windows \
      --cut-dirs=0 \
      --wait=1 --random-wait \
      --limit-rate=500k \
      -e robots=off \
      --header="Host: $DOMAIN" \
      --header="User-Agent: $CHROME_UA" \
      -P "${BACKUP_DIR}/site" \
      -o "${BACKUP_DIR}/logs/wget-uploads.log" \
      "http://${DIRECT_IP}/wp-content/uploads/" || true
    log "[INFO] Uploads wget sweep completed"
  else
    # Python scraper pass targeting uploads directory specifically
    log "[INFO] Running Python scraper uploads pass..."
    local uploads_base
    if [[ -n "$DIRECT_IP" ]]; then
      uploads_base="http://${DIRECT_IP}/wp-content/uploads/"
    else
      uploads_base="https://${DOMAIN}/wp-content/uploads/"
    fi

    # Add uploads URL as seed and run limited scrape
    echo "$uploads_base" >> "${BACKUP_DIR}/url-list-raw.txt"

    local uploads_ip="${DIRECT_IP:-$IP_CANDIDATE_1}"
    python "$SCRIPT_DIR/scraper.py" \
      --ip "$uploads_ip" \
      --seed-file "${BACKUP_DIR}/url-list-raw.txt" \
      --output-dir "${BACKUP_DIR}/site" \
      --max-pages 500 || true
    log "[INFO] Python uploads pass completed"
  fi
}

# ------------------------------------------------------------------------------
# 11. consolidate_url_list() — assemble deduplicated url-list.txt
# ------------------------------------------------------------------------------
consolidate_url_list() {
  log "=== Consolidating URL list ==="

  local raw_file="${BACKUP_DIR}/url-list-raw.txt"
  local final_file="${BACKUP_DIR}/url-list.txt"

  # Source 1: Extract URLs from wget log files (HTTP 200 lines)
  for log_file in "${BACKUP_DIR}/logs/wget-ip.log" "${BACKUP_DIR}/logs/wget-domain.log"; do
    if [[ -f "$log_file" ]]; then
      # wget log format: grep lines starting with -- that contain 200 OK
      grep -oP 'https?://[^ ]+' "$log_file" 2>/dev/null \
        | grep -i "$DOMAIN" \
        | sed "s|http://${IP_CANDIDATE_1}|https://$DOMAIN|g" \
        | sed "s|http://${IP_CANDIDATE_2}|https://$DOMAIN|g" \
        >> "$raw_file" || true
    fi
  done

  # Source 2: Reconstruct URLs from downloaded HTML file tree
  if [[ -d "${BACKUP_DIR}/site" ]]; then
    find "${BACKUP_DIR}/site" -type f -name "*.html" 2>/dev/null \
      | sed "s|${BACKUP_DIR}/site/||" \
      | sed "s|/index\.html$|/|" \
      | sed "s|\.html$||" \
      | sed "s|^|https://$DOMAIN/|" \
      >> "$raw_file" || true
  fi

  # Source 3: Extract <loc> URLs from all saved sitemap XML files
  find "${BACKUP_DIR}" -maxdepth 2 \( -name "*.xml" -o -name "sitemap*" \) \
    -not -path "*/wayback/*" 2>/dev/null \
    | while IFS= read -r xml_file; do
        grep -oP '(?<=<loc>)[^<]+' "$xml_file" 2>/dev/null | \
          grep "^https\?://.*$DOMAIN" || true
      done \
    >> "$raw_file" || true

  # Source 4: CDX clean URLs (already appended by wayback_download.py if it ran)

  # Final deduplication, filtering, sort
  if [[ -f "$raw_file" ]]; then
    sort -u "$raw_file" \
      | grep "^https\?://.*${DOMAIN}" \
      | grep -v "\?s=" \
      | grep -v "\?replytocom=" \
      | grep -v "wc-ajax" \
      | grep -v "yith-woocompare" \
      | grep -v "^#" \
      > "$final_file" || true

    local count=0
    [[ -f "$final_file" ]] && count=$(wc -l < "$final_file")
    log "[OK] url-list.txt: $count unique URLs"
  else
    log "[WARN] url-list-raw.txt not found — url-list.txt will be empty"
    touch "$final_file"
  fi
}

# ------------------------------------------------------------------------------
# 12. print_summary() — final report
# ------------------------------------------------------------------------------
print_summary() {
  log "=== Backup Summary ==="

  local html_count=0
  local asset_count=0
  local url_count=0
  local wayback_count=0

  [[ -d "${BACKUP_DIR}/site" ]] && \
    html_count=$(find "${BACKUP_DIR}/site" -name "*.html" 2>/dev/null | wc -l)
  [[ -d "${BACKUP_DIR}/site" ]] && \
    asset_count=$(find "${BACKUP_DIR}/site" -type f \
      \( -name "*.css" -o -name "*.js" -o -name "*.png" -o -name "*.jpg" \
         -o -name "*.jpeg" -o -name "*.gif" -o -name "*.svg" -o -name "*.webp" \
         -o -name "*.woff" -o -name "*.woff2" -o -name "*.pdf" \) \
      2>/dev/null | wc -l)
  [[ -f "${BACKUP_DIR}/url-list.txt" ]] && \
    url_count=$(wc -l < "${BACKUP_DIR}/url-list.txt")
  [[ -d "${BACKUP_DIR}/wayback" ]] && \
    wayback_count=$(find "${BACKUP_DIR}/wayback" -type f 2>/dev/null | wc -l)

  echo ""
  echo "=============================================="
  echo "  resystausa.com Backup Complete"
  echo "=============================================="
  echo "  Output directory : ${BACKUP_DIR}/"
  echo "  HTML pages       : ${html_count}"
  echo "  Asset files      : ${asset_count}"
  echo "  Wayback files    : ${wayback_count}"
  echo "  Unique URLs      : ${url_count} (url-list.txt)"
  echo ""
  echo "  Access method    : ${ACCESS_METHOD}"
  echo "  Direct IP used   : ${DIRECT_IP:-none}"
  echo "  wget available   : ${WGET_AVAILABLE}"
  echo "  wget success     : ${WGET_SUCCESS}"
  echo "=============================================="

  if [[ -f "${BACKUP_DIR}/logs/challenge-pages.txt" ]]; then
    local challenge_count
    challenge_count=$(wc -l < "${BACKUP_DIR}/logs/challenge-pages.txt")
    if [[ $challenge_count -gt 0 ]]; then
      echo ""
      echo "  [WARN] $challenge_count challenge pages detected — see:"
      echo "    ${BACKUP_DIR}/logs/challenge-pages.txt"
    fi
  fi

  if [[ "${ACCESS_METHOD}" == "dead" ]]; then
    echo ""
    echo "  [WARN] Live site was unreachable. Backup contains Wayback Machine"
    echo "  snapshots only (HTML — no CSS/JS/images)."
  fi

  echo ""
}

# ==============================================================================
# Main pipeline
# ==============================================================================

mkdir -p "${BACKUP_DIR}/site" "${BACKUP_DIR}/logs" "${BACKUP_DIR}/wayback"
touch "${BACKUP_DIR}/url-list-raw.txt"

check_tools
check_longpaths
probe_connectivity

if [[ "$ACCESS_METHOD" == "dead" ]]; then
  log "[WARN] Live site inaccessible — skipping to Wayback fallback"
  run_wayback_fallback
  consolidate_url_list
  print_summary
  exit 0
fi

download_sitemaps
run_wget_mirror
scan_challenge_pages

if [[ "$WGET_SUCCESS" == "false" ]]; then
  log "[INFO] wget mirror incomplete — running Python scraper fallback"
  run_python_scraper
  scan_challenge_pages  # re-check after scraper run
fi

if [[ "$WGET_SUCCESS" == "false" ]]; then
  log "[INFO] Live site still incomplete — running Wayback Machine fallback"
  run_wayback_fallback
fi

download_uploads
consolidate_url_list
print_summary
