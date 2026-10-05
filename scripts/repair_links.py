"""Repair obsolete internal routes against the files actually published by this site."""
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit
import html, json, re

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://www.mybnbdesign.com"
ALIASES = {
    "/markets/index.html": "/markets/",
    "/contact": "/contact.html",
    "/contact/": "/contact.html",
    "/faq-index.html": "/faq/",
    "/blog/airbnb-photography-tips.html": "/airbnb-photography-tips.html",
    "/blog/furniture-assembly-installation.html": "/blog/airbnb-furniture-assembly-installation.html",
}
for topic in ("mountain-cabin", "desert", "urban-apartment", "beach-house", "ski-chalet", "a-frame", "japandi", "penthouse", "historic-home"):
    ALIASES[f"/blog/{topic}.html"] = f"/blog/{topic}-airbnb-interior-design.html"
for topic in ("pricing", "process", "furniture", "photography", "budget", "property-types", "renovation", "maintenance", "working-remotely"):
    ALIASES[f"/{topic}/"] = f"/faq/{topic}/"

def exists(route):
    target = ROOT / route.lstrip("/")
    return target.is_file() or (target / "index.html").is_file()

def replacement(route):
    if route in ALIASES and exists(ALIASES[route]):
        return ALIASES[route]
    if exists(route):
        return route
    clean = route.rstrip("/")
    if exists(clean + ".html"):
        return clean + ".html"
    if route.startswith("/blog/") and route.endswith(".html"):
        candidate = "/blog/airbnb-" + route.rsplit("/", 1)[1]
        if exists(candidate):
            return candidate
    return None

def repair():
    totals = {"files_changed": 0, "links_repaired": 0, "unsupported_links_unwrapped": 0, "canonicals_repaired": 0}
    for file in sorted(ROOT.rglob("*.html")):
        if any(part in ("node_modules", ".git", "public") for part in file.relative_to(ROOT).parts):
            continue
        original = file.read_text()
        base = ORIGIN + "/" + file.relative_to(ROOT).as_posix()
        def anchor(match):
            opening, href, contents = match.group(1), html.unescape(match.group(3)), match.group(4)
            parsed = urlsplit(urljoin(base, href))
            if parsed.netloc not in ("www.mybnbdesign.com", "mybnbdesign.com") or parsed.scheme not in ("https", "http"):
                return match.group(0)
            route = replacement(parsed.path)
            if route is None:
                # Keep the copy, but do not send visitors to an unpublished destination.
                totals["unsupported_links_unwrapped"] += 1
                return contents
            if route == parsed.path:
                return match.group(0)
            totals["links_repaired"] += 1
            target = urlunsplit(("", "", route, parsed.query, parsed.fragment))
            return opening.replace(match.group(3), html.escape(target, quote=True)) + contents + "</a>"
        updated = re.sub(r'(<a\b[^>]*\bhref=(["\'])(.*?)\2[^>]*>)(.*?)</a\s*>', anchor, original, flags=re.I | re.S)
        def canonical(match):
            href = html.unescape(match.group(2))
            parsed = urlsplit(href)
            if parsed.netloc not in ("www.mybnbdesign.com", "mybnbdesign.com"):
                return match.group(0)
            if exists(parsed.path) and not re.search(r"\s", parsed.path):
                return match.group(0)
            totals["canonicals_repaired"] += 1
            return match.group(0).replace(match.group(2), base)
        updated = re.sub(r'<link\b[^>]*rel=["\']canonical["\'][^>]*href=(["\'])(.*?)\1[^>]*>', canonical, updated, flags=re.I)
        if file.relative_to(ROOT).as_posix() == "book/index.html" and not re.search(r'rel=["\']canonical["\']', updated):
            updated = updated.replace("</head>", '<link rel="canonical" href="' + ORIGIN + '/book/">\n</head>')
            totals["canonicals_repaired"] += 1
        if updated != original:
            file.write_text(updated)
            totals["files_changed"] += 1
    print(json.dumps(totals))
    return totals

if __name__ == "__main__":
    repair()
