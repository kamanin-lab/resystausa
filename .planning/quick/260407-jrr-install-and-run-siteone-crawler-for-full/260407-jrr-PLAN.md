---
type: quick
tasks: 2
autonomous: true
---

<objective>
Install SiteOne Crawler v2.1.0 and run a full SEO analysis crawl of resystausa.com.

Purpose: Generate a comprehensive SEO audit report (broken links, meta tags, headings, OpenGraph, redirects, accessibility) and an XML sitemap for URL mapping — complements the wget backup with structured SEO data.

Output: Interactive HTML report at G:/01_OPUS/Projects/resystausa/seo-report/report.html and XML sitemap at G:/01_OPUS/Projects/resystausa/seo-report/sitemap.xml
</objective>

<context>
@.planning/STATE.md
@CLAUDE.md
</context>

<tasks>

<task type="auto">
  <name>Task 1: Download and install SiteOne Crawler v2.1.0</name>
  <files>C:/Tools/siteone-crawler-v2.1.0/</files>
  <action>
1. Create the install directory:
   ```
   mkdir -p /c/Tools/siteone-crawler-v2.1.0
   ```

2. Download the Windows x64 zip using curl (with browser User-Agent per CLAUDE.md conventions):
   ```
   curl -L -o /c/Tools/siteone-crawler-v2.1.0/siteone-crawler-v2.1.0-win-x64.zip \
     "https://github.com/janreges/siteone-crawler/releases/download/v2.1.0/siteone-crawler-v2.1.0-win-x64.zip"
   ```

3. Extract the zip into the install directory. Use unzip or powershell Expand-Archive:
   ```
   cd /c/Tools/siteone-crawler-v2.1.0 && unzip -o siteone-crawler-v2.1.0-win-x64.zip
   ```
   If unzip is not available, use:
   ```
   powershell -Command "Expand-Archive -Path 'C:\Tools\siteone-crawler-v2.1.0\siteone-crawler-v2.1.0-win-x64.zip' -DestinationPath 'C:\Tools\siteone-crawler-v2.1.0' -Force"
   ```

4. List the extracted contents to identify the actual binary name (crawler.exe, siteone-crawler.exe, or crawler.bat):
   ```
   ls -la /c/Tools/siteone-crawler-v2.1.0/
   ```
   If files extracted into a subdirectory, note the path.

5. Verify the binary runs:
   ```
   /c/Tools/siteone-crawler-v2.1.0/crawler.exe --version
   ```
   (Adjust binary name based on what was found in step 4.)

6. Clean up the zip file:
   ```
   rm /c/Tools/siteone-crawler-v2.1.0/siteone-crawler-v2.1.0-win-x64.zip
   ```
  </action>
  <verify>
    <automated>ls /c/Tools/siteone-crawler-v2.1.0/*.exe 2>/dev/null || ls /c/Tools/siteone-crawler-v2.1.0/*.bat 2>/dev/null || ls /c/Tools/siteone-crawler-v2.1.0/**/*.exe 2>/dev/null</automated>
  </verify>
  <done>SiteOne Crawler binary exists at C:/Tools/siteone-crawler-v2.1.0/ and responds to --version or --help</done>
</task>

<task type="auto">
  <name>Task 2: Run SiteOne Crawler against resystausa.com</name>
  <files>G:/01_OPUS/Projects/resystausa/seo-report/report.html, G:/01_OPUS/Projects/resystausa/seo-report/sitemap.xml</files>
  <action>
1. Create the output directory:
   ```
   mkdir -p "G:/01_OPUS/Projects/resystausa/seo-report"
   ```

2. Run SiteOne Crawler in background. Use the binary path discovered in Task 1. The command pattern is:
   ```
   /c/Tools/siteone-crawler-v2.1.0/crawler.exe \
     --url=https://resystausa.com/ \
     --output="G:/01_OPUS/Projects/resystausa/seo-report/report.html" \
     --sitemap-xml-file="G:/01_OPUS/Projects/resystausa/seo-report/sitemap.xml" \
     --workers=3 \
     --wait=1000
   ```
   Adjust the binary name/path if Task 1 found it under a different name or subdirectory.

   IMPORTANT: This crawl is long-running (10-30 minutes for a full WordPress site). Run it in background using the run_in_background parameter. The executor will be notified when it completes.

   If the crawler supports additional useful flags discovered during Task 1 (e.g., --user-agent for browser UA, --max-depth, --accept-type), consider adding:
   - A browser User-Agent header if available (per CLAUDE.md: always use Chrome 124 UA)
   - Any flag to follow redirects

3. After completion, verify both output files exist and have reasonable size:
   ```
   ls -la "G:/01_OPUS/Projects/resystausa/seo-report/"
   ```

4. Report the file sizes and confirm the crawl completed successfully.
  </action>
  <verify>
    <automated>test -f "G:/01_OPUS/Projects/resystausa/seo-report/report.html" && test -s "G:/01_OPUS/Projects/resystausa/seo-report/report.html" && echo "HTML report exists and is non-empty" || echo "MISSING: report.html"</automated>
  </verify>
  <done>HTML report exists at G:/01_OPUS/Projects/resystausa/seo-report/report.html (non-empty), XML sitemap exists at G:/01_OPUS/Projects/resystausa/seo-report/sitemap.xml, crawl completed without fatal errors</done>
</task>

</tasks>

<verification>
- SiteOne Crawler v2.1.0 installed at C:/Tools/siteone-crawler-v2.1.0/
- HTML SEO report generated at G:/01_OPUS/Projects/resystausa/seo-report/report.html
- XML sitemap generated at G:/01_OPUS/Projects/resystausa/seo-report/sitemap.xml
- Both files are non-empty and represent a complete crawl of resystausa.com
</verification>

<success_criteria>
1. SiteOne Crawler binary is installed and executable on the system
2. Full-site crawl of resystausa.com completed (all accessible pages)
3. Interactive HTML report covers: SEO issues, broken links (404s), meta tags, headings, OpenGraph, redirects
4. XML sitemap contains discovered URLs for future SEO mapping
5. Rate limiting respected (1 second wait between requests via --wait=1000)
</success_criteria>
