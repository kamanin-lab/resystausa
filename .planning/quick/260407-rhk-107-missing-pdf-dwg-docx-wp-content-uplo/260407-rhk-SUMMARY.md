---
phase: quick
plan: 260407-rhk
subsystem: resysta-backup/site/wp-content/uploads
tags: [download, pdf, zip, docx, archival, ip-bypass]
dependency_graph:
  requires: [260407-qhd]
  provides: [complete-technical-file-archive]
  affects: [products, typical-drawing-details, cad-bim-and-csi]
tech_stack:
  added: []
  patterns: [python-requests-ip-bypass, file-header-validation]
key_files:
  created:
    - resysta-backup/site/wp-content/uploads/2018/12/ (4 Revit/Materials ZIPs)
    - resysta-backup/site/wp-content/uploads/2022/05-09/ (4 files)
    - resysta-backup/site/wp-content/uploads/2023/03/ (40 files)
    - resysta-backup/site/wp-content/uploads/2023/05/ (1 DOCX)
    - resysta-backup/site/wp-content/uploads/2023/09/ (4 files)
    - resysta-backup/site/wp-content/uploads/2024/08-10/ (12 files)
    - resysta-backup/site/wp-content/uploads/2025/03/ (2 DOCXs)
    - resysta-backup/site/wp-content/uploads/2025/10-12/ (14 files)
    - .planning/quick/260407-rhk-107-missing-pdf-dwg-docx-wp-content-uplo/download-missing.py
    - .planning/quick/260407-rhk-107-missing-pdf-dwg-docx-wp-content-uplo/validate-downloads.py
    - .planning/quick/260407-rhk-107-missing-pdf-dwg-docx-wp-content-uplo/missing-files.txt
    - .planning/quick/260407-rhk-107-missing-pdf-dwg-docx-wp-content-uplo/download-report.txt
  modified: []
decisions:
  - "Used Python requests library (not wget) for per-file header control and Cloudflare challenge detection"
  - "HTTP only to 74.208.236.71:80 — HTTPS skipped due to TLS cert mismatch on bare IP"
  - "Random 1.5-2.5s delay between requests, 3-5s on retry — no rate limiting triggered"
metrics:
  duration: "~5 minutes (107 files, 1.5-2.5s delay)"
  completed: 2026-04-07
  tasks_completed: 2
  files_created: 111
---

# Quick Task 260407-rhk: Download 107 Missing Technical Files — Summary

**One-liner:** Downloaded all 107 missing product spec PDFs, AutoCAD DWG ZIPs, Revit BIM ZIPs, and CSI DOCX files via HTTP IP bypass to 74.208.236.71 with full binary header validation.

---

## What Was Done

Task 260407-rhk completed the critical gap identified in the backup audit (260407-qhd): 107 technical files were missing from `wp-content/uploads/` despite being referenced in HTML download links across product pages and the CAD/BIM page.

### Task 1: Scan + Download

A Python script (`download-missing.py`) was written and executed that:

1. Scanned all 554 HTML files in the backup for `href` URLs pointing to `resystausa.com/wp-content/uploads/` with `.pdf`, `.zip`, or `.docx` extensions
2. Checked each against the local filesystem to build the missing-file list
3. Downloaded all 107 missing files via `http://74.208.236.71` with `Host: resystausa.com` header
4. Validated each download for Cloudflare challenge page detection (Content-Type: text/html)
5. Applied random 1.5-2.5s delays between requests

**Result: 107/107 downloaded, 0 failed, 0 retries needed.**

### Task 2: Validation

A separate validation script (`validate-downloads.py`) re-scanned HTML files, confirmed 0 still-missing files, and validated binary file headers:

- PDFs: first 4 bytes = `%PDF`
- ZIPs and DOCXs: first 2 bytes = `PK` (0x504B)

**Result: 107/107 valid. No Cloudflare challenge pages. No zero-size files.**

---

## Files Downloaded by Type

| Type | Count | Description |
|------|-------|-------------|
| PDF | 50 | Product spec sheets + typical drawing detail PDFs (2022-2025) |
| ZIP (DWG) | 47 | AutoCAD drawing ZIPs for each product (2022-2025) |
| ZIP (Revit/BIM) | 4 | HybridDecking 2016/2017/2018 RVT + Materials Resysta |
| ZIP (fence products) | 3 | RESFB, RESFI, RESFP, RESFPB, RESFT fence system ZIPs |
| DOCX | 3 | CSI spec docs: 07460resR10, 06603truR18, 06730truR18 |
| **Total** | **107** | |

---

## Verification Results

| Check | Result |
|-------|--------|
| PDF count in uploads | 93 (was 43, +50) |
| ZIP count in uploads | 55 (was 1, +54) |
| DOCX count in uploads | 3 (was 0, +3) |
| Cloudflare challenge pages | 0 |
| Zero-size files | 0 |
| Invalid file headers | 0 |
| Files still missing after download | 0 |

---

## Commits

| Hash | Description |
|------|-------------|
| 22da640 | feat(quick-260407-rhk): download 107 missing technical files from resystausa.com |

---

## Deviations from Plan

None — plan executed exactly as written. All 107 files downloaded successfully on the first pass with no retries required.

---

## Known Stubs

None. All files are real binary content validated by header inspection.

---

## Threat Flags

None. All downloaded files are binary (PDF/ZIP/DOCX) with no new network endpoints introduced.

---

## Self-Check: PASSED

- `wp-content/uploads/2018/12/HybridDecking_Resysta-2016.rvt_.zip` — FOUND
- `wp-content/uploads/2023/03/RESCLIPHF100.pdf` — FOUND
- `wp-content/uploads/2023/05/07460resR10.docx` — FOUND
- `wp-content/uploads/2025/12/RESCHP011208.zip` — FOUND
- Commit 22da640 — FOUND (107 files created)
- download-report.txt STATUS: PASS confirmed
