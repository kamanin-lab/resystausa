# Quick Task 260407-fou: Make complete local backup of resystausa.com website - Context

**Gathered:** 2026-04-07
**Status:** Ready for planning

<domain>
## Task Boundary

Create a complete local backup of resystausa.com — a WordPress site behind Cloudflare that the client is losing access to. The backup must capture HTML pages, images, CSS, JS, fonts, and PDFs. Real server IP: 74.208.236.61 (IONOS). Output: resysta-backup/ structured folder with url-list.txt for SEO mapping.

</domain>

<decisions>
## Implementation Decisions

### Script format
- Single bash script (backup.sh) that runs the full pipeline with inline fallback logic

### Failure handling
- Auto-proceed to fallbacks: script automatically runs Python scraper then Wayback Machine when wget produces challenge pages — no manual intervention required

### wget target
- Run both access methods simultaneously with --no-clobber: direct IP (http://74.208.236.61 HTTP port 80 + Host header) and domain HTTPS (https://resystausa.com + Chrome UA) in parallel

### Claude's Discretion
- Windows LongPathsEnabled check before wget (from research)
- Use --restrict-file-names=windows flag (NTFS safety)
- Post-mirror grep scan for Cloudflare challenge markers before declaring success
- Python scraper must target direct IP, not domain, to avoid TLS fingerprinting
- waybackpack CDX pre-check before full download
- 1-2s random delay between all requests

</decisions>

<specifics>
## Specific Ideas

- Script: backup.sh in project root
- Output path: G:\01_OPUS\Projects\resystausa\resysta-backup\
- Direct IP: 74.208.236.61, HTTP port 80 only (no HTTPS — TLS cert mismatch)
- Chrome UA: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
- Challenge page markers to grep: _cf_chl_opt, cf-browser-verification, "Just a moment"
- Wayback from-date: 20250101

</specifics>

<canonical_refs>
## Canonical References

- input.txt — original task specification with all curl/wget commands
- .planning/research/STACK.md — tool selection rationale
- .planning/research/PITFALLS.md — critical warnings (Windows MAX_PATH, TLS mismatch, silent challenge pages)
- .planning/research/ARCHITECTURE.md — fallback chain design

</canonical_refs>
