# mybnbdesign
MyBnBDesign - Professional Airbnb and short-term rental interior design services

SEO discovery maintenance: after regenerating education or reference hubs, run `python3 scripts/build_seo_discovery.py` to restore contextual links and the existing-guide cohort sitemap. The production build validates every JSON-LD block with `scripts/check-structured-data.mjs`; insert links only into HTML content, never into serialized structured-data strings.

Reviewed legacy owners: `python3 scripts/build_reviewed_legacy.py` replaces the 50 explicitly reviewed legacy pages, creates page-specific CSV decision worksheets, restores their hub links and builds `sitemap-reviewed-design.xml`. Run after any broader provider or education regeneration. `python3 scripts/build_keyword_lessons.py` restores the original applied lessons on eight existing keyword owners. Neither script creates additional HTML routes. Provider facts are separated from editorial exercises; unresolved identities are disclosed instead of assigned prices, ratings or results.
