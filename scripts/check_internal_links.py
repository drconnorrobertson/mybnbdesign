"""Check every local HTML anchor against a real route and optional fragment."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, unquote
import argparse
import json

SOURCE = Path(__file__).resolve().parents[1]
ORIGIN = 'https://www.mybnbdesign.com'

class Links(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.anchors = []
        self.ids = set()
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'a' and attrs.get('href'):
            self.anchors.append(attrs['href'])

def run(root):
    pages = {p.relative_to(root).as_posix(): Links(p.read_text())
             for p in root.rglob('*.html')
             if not any(part.startswith('.') for part in p.relative_to(root).parts)}
    local_anchors = 0
    errors = []
    for file, page in pages.items():
        route = '/' + file
        if route.endswith('/index.html'):
            route = route[:-10]
        for href in page.anchors:
            parsed = urlsplit(urljoin(ORIGIN + route, href))
            if parsed.scheme not in ('http', 'https') or parsed.netloc not in ('www.mybnbdesign.com', 'mybnbdesign.com'):
                continue
            local_anchors += 1
            path = unquote(parsed.path).lstrip('/')
            candidates = ['index.html'] if not path else [path, path + 'index.html' if path.endswith('/') else path + '/index.html']
            if not path.endswith('/') and not Path(path).suffix:
                candidates.append(path + '.html')
            found = next((c for c in candidates if (root / c).is_file()), None)
            if found is None:
                errors.append({'source': file, 'href': href, 'reason': 'missing target'})
            elif parsed.fragment and found in pages and unquote(parsed.fragment) not in pages[found].ids:
                errors.append({'source': file, 'href': href, 'reason': 'missing fragment'})
    report = {'html_files': len(pages), 'local_anchors': local_anchors, 'errors': errors}
    print(json.dumps({'html_files': len(pages), 'local_anchors': local_anchors,
                      'error_count': len(errors), 'first_errors': errors[:20]}, indent=2))
    return report

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=SOURCE)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = run(args.root.resolve())
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + '\n')
    raise SystemExit(bool(report['errors']))
