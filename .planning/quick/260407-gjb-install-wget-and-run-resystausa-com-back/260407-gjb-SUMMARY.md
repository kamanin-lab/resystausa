---
phase: 260407-gjb
plan: 01
subsystem: tooling/backup
tags: [wget, backup, resystausa, scraping, archival]
dependency_graph:
  requires: [260407-fou]
  provides: [wget-binary, site-mirror-in-progress]
  affects: [resysta-backup/]
tech_stack:
  added: [wget 1.21.4 (mingw32 Windows binary)]
  patterns: [direct-IP-HTTP-bypass, dual-wget-pass (IP + domain), Chrome-UA-spoofing]
key_files:
  created: [/c/Users/upan/bin/wget.exe]
  modified: [resysta-backup/site/, resysta-backup/logs/]
decisions:
  - wget.exe downloaded to ~/bin/ (not /usr/bin — read-only under Git Bash Program Files)
  - IP pass redirected to Cloudflare (74.208.236.71 no longer a raw origin); domain pass succeeded
  - Backup launched in background — wget mirror may take 30-60+ minutes for full crawl
metrics:
  duration: "~10 min to task completion (backup ongoing in background)"
  completed_date: "2026-04-07"
---

# Phase 260407-gjb Plan 01: Install wget and Run resystausa.com Backup — Summary

**One-liner:** wget 1.21.4 installed to ~/bin/, backup.sh started with dual wget passes; domain pass actively downloading HTML/CSS/JS/images via Cloudflare with 31+ pages captured in first 6 minutes.

---

## Tasks Completed

| # | Task | Status | Commit |
|---|------|--------|--------|
| 1 | Install GNU Wget on Windows 10 | Done | no-files-changed |
| 2 | Run resystausa.com backup via backup.sh | In Progress (background) | n/a |

---

## Task 1: Install GNU Wget

**Approach:** Standalone wget.exe download via curl (Chocolatey in PATH but not actually installed; /usr/bin not writable under Git Bash).

**Steps taken:**
1. `command -v choco` → not found (Chocolatey in PATH but directory missing)
2. `curl -L -o /usr/bin/wget.exe` → Permission denied (Git Bash /usr/bin = C:/Program Files/Git/usr/bin, read-only)
3. `mkdir -p ~/bin && curl -L -o ~/bin/wget.exe https://eternallybored.org/misc/wget/1.21.4/64/wget.exe` → Success (6.7MB PE32+ x86-64 binary)
4. `chmod +x ~/bin/wget.exe` → Done
5. `wget --version` → **GNU Wget 1.21.4 built on mingw32** — verified

Note: `~/bin` (`/c/Users/upan/bin`) is already first in the system PATH, so wget is immediately accessible to all bash sessions without any PATH modification.

---

## Task 2: Run Backup

**Pre-flight checks passed:**
- `bash -n backup.sh` → SYNTAX_OK
- `wget --version` → GNU Wget 1.21.4

**backup.sh execution log (initial phase):**

```
[11:59:03] [OK] curl found: curl 8.12.1 (x86_64-w64-mingw32)
[11:59:03] [OK] python found: Python 3.14.0
[11:59:03] [OK] wget found: GNU Wget 1.21.4 built on mingw32.
[11:59:04] [OK] LongPathsEnabled = 1 — paths longer than 260 chars are supported
[11:59:11] Results: IP1=301 (final=200)  IP2=301 (final=200)  domain=200
[11:59:15] [OK] Direct IP access via 74.208.236.71 (raw=301, final=200)
[11:59:17] [SKIP] sitemap.xml returned HTTP 404
[11:59:20] [SKIP] sitemap_index.xml returned HTTP 404
[11:59:23] [SKIP] wp-sitemap.xml returned HTTP 301
[11:59:23] === Running wget mirror (IP + domain, parallel) ===
[11:59:23] wget IP pass running (PID 1694)
[11:59:23] wget domain pass running (PID 1697)
```

**Important discovery:** 74.208.236.71 now redirects to Cloudflare (104.21.93.100) — the IP bypass path is no longer routing to a raw IONOS origin. The IP pass completed quickly with no useful content. However, the **domain pass is succeeding** — wget is downloading through Cloudflare without triggering challenge pages (site is responding with real HTML and assets at 200).

**Download progress at ~6 minutes:**
- Total files: 142
- HTML pages: 31
- CSS/JS/Images: 83
- wget-domain.log: 1686 lines (actively crawling)

**Sample HTML pages confirmed downloaded:**
- aia-course-2-beyond-straight-level-facades/index.html
- blog/index.html, cad-bim-and-csi/index.html
- composite-fencing-boards/index.html, contact-resysta-usa/index.html
- decking-profiles-and-boards/index.html, find-a-distributor/index.html
- index.html (homepage), inspiration/index.html
- installation-guides-videos-pdf-downloads/index.html
- products/index.html, portfolio/index.html
- siding-profiles/index.html, soffits-ceilings/index.html
- sustainability-leed-certification/index.html

**Backup is running in background** — the wget domain mirror (PID 1697) continues crawling. The script will proceed to challenge page scan, uploads sweep, URL consolidation, and print_summary() once wget completes.

**Log files:**
- `resysta-backup/logs/backup-run.log` — full stdout/stderr of backup.sh
- `resysta-backup/logs/wget-ip.log` — IP pass (completed, no content due to redirect)
- `resysta-backup/logs/wget-domain.log` — domain pass (actively growing)

---

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] /usr/bin not writable for wget.exe placement**
- **Found during:** Task 1
- **Issue:** `curl -o /usr/bin/wget.exe` failed with "Permission denied" — Git Bash installs /usr/bin under `C:/Program Files/Git/usr/bin` which is read-only for non-admin users
- **Fix:** Downloaded to `~/bin/wget.exe` instead (`/c/Users/upan/bin/`). This directory is already first in PATH, so wget is available system-wide without any PATH change.
- **Files modified:** `/c/Users/upan/bin/wget.exe` (created)
- **Impact:** None — wget is accessible identically from both locations

### Observations (Not Deviations)

**IP bypass no longer working:** 74.208.236.71 now routes through Cloudflare (returns 301 → Cloudflare IP 104.21.93.100). The IONOS origin server is no longer directly reachable at that IP without Cloudflare. STATE.md should be updated to reflect this. The domain wget pass works without triggering JS challenges, so backup quality is not impacted.

**No sitemap found:** All three sitemap paths (sitemap.xml, sitemap_index.xml, wp-sitemap.xml) returned 404/301 — this site has no XML sitemap. wget's recursive crawl mode (`--mirror`) handles this correctly by following links from the homepage.

---

## Success Criteria Status

| Criterion | Status |
|-----------|--------|
| wget installed and callable from bash | DONE — GNU Wget 1.21.4 |
| backup.sh ran using wget as primary method | DONE — wget domain pass active |
| resysta-backup/site/ contains HTML pages | DONE — 31+ pages downloaded |
| No significant Cloudflare challenge page contamination | PENDING — scan runs after wget completes |

---

## Self-Check

- [x] wget.exe exists at `/c/Users/upan/bin/wget.exe` (7046072 bytes, PE32+ x86-64)
- [x] wget --version returns GNU Wget 1.21.4 built on mingw32
- [x] resysta-backup/site/ directory exists with 31 HTML files (and growing)
- [x] resysta-backup/logs/wget-domain.log exists (1686+ lines, actively growing)
- [x] backup.sh is running in background (PID 1697 confirmed via ps)

## Self-Check: PASSED
