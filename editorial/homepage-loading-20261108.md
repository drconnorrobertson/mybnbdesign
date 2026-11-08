# Homepage loading follow-up

Baseline: PageSpeed Insights mobile report captured November 8, 2026 at 11:42 AM Eastern: performance 73, FCP 1.5 s, LCP 6.9 s, TBT 120 ms, CLS 0, SEO 100. Slow 4G / emulated Moto G Power; these are lab estimates, not field Core Web Vitals.

Report: https://pagespeed.web.dev/analysis/https-www-mybnbdesign-com/oasg55affg?form_factor=mobile

The render-blocking audit lists the Google Fonts stylesheet at 750 ms and local CSS at 700 ms combined. The image cache-lifetime audit flags short-lived assets. The accessibility audit identifies a missing main landmark.

Changes: load the existing Google Fonts stylesheet asynchronously with a no-JavaScript fallback; give only content-hashed WebP assets a one-year immutable browser cache; add a main landmark around homepage content. Keep layout-critical styles synchronous. No images are replaced and no performance-score improvement is claimed before a comparable deployed test.

Checks: production pipeline passed all 5,040 HTML pages and 5,678 structured-data blocks, preserving 2,598 indexable URLs and 2,432 noindex utility worksheets. Validate the header matcher against all 10 optimized manifest paths and representative non-hashed paths. Browser preview must retain the hero, navigation, typography and canonical URL. Verify cache response headers on the preview before publication.
