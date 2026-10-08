# Host planning library

The content modules contain original, practical rental-design decision guides and
reviewed repairs to existing routes. Each guide has a distinct decision, a clearly
hypothetical example, a checklist, a handover step, and public primary-source links.
The renderer retains the main site's navigation and booking destination.

## Render and verify

From the repository root:

```sh
python3 scripts/build_host_library.py
python3 scripts/upgrade_tool_discovery.py
python3 scripts/rebuild_discovery.py
python3 scripts/validate_host_library.py
python3 scripts/check_internal_links.py
python3 scripts/check_host_regeneration.py
```

For review before applying page or link edits, copy the site to a separate directory
and pass `--output-root /path/to/review-copy` to both renderers. Pass
`--root /path/to/review-copy` to the three validators. The validators use only the
Python standard library and require no installed packages.

`blog_discovery_policy.json` preserves the existing published blog collection and
explicitly lists the additional color guides reviewed for promotion. Other
unsitemapped legacy pages are not automatically promoted. The internal-discovery
audit reports structural reachability; unavailable Search Console metrics must
remain unavailable and are not evidence of ranking.

The editorial modification date in the renderer is an explicit review date. Change
it only when the content actually changes or receives another substantive review;
regeneration alone does not establish a new update date. Existing untouched sitemap
dates are retained, and modified/new routes receive the actual editorial date.

Never use the older mass city/room generators to expand this collection. Edits
should address a new, useful host decision with original actionable content.

The October 7 tools upgrade is reapplied by `build_host_library.py`. The ROI tool uses a user-entered hypothetical ADR change defaulting to zero; it no longer infers a 15–40% revenue increase from the amount spent. Its outputs are gross-revenue scenarios before expenses.
