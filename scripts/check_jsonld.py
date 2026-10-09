"""Parse every JSON-LD block in every site HTML file; exit nonzero on errors."""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class Blocks(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.blocks = []
        self.current = None
        self.feed(text)
        self.close()
        if self.current is not None:
            self.blocks.append((self.line, ''.join(self.current)))

    def handle_starttag(self, tag, attrs):
        if tag == 'script' and dict(attrs).get('type', '').lower() == 'application/ld+json':
            self.current = []
            self.line = self.getpos()[0]

    def handle_data(self, data):
        if self.current is not None:
            self.current.append(data)

    def handle_endtag(self, tag):
        if tag == 'script' and self.current is not None:
            self.blocks.append((self.line, ''.join(self.current)))
            self.current = None

def check(root):
    files = sorted(p for p in root.rglob('*.html')
                   if not any(part.startswith('.') for part in p.relative_to(root).parts))
    errors = []
    count = 0
    def reject_constant(value):
        raise ValueError('Non-JSON constant: ' + value)
    for file in files:
        for number, (line, text) in enumerate(Blocks(file.read_text()).blocks, 1):
            count += 1
            try:
                json.loads(text, parse_constant=reject_constant)
            except (ValueError, RecursionError) as error:
                errors.append({'path': file.relative_to(root).as_posix(), 'block': number,
                               'line': line, 'error': str(error)})
    return {'html_files': len(files), 'jsonld_blocks': count,
            'invalid_blocks': len(errors), 'invalid_files': len({e['path'] for e in errors}),
            'errors': errors}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check(args.root.resolve())
    rendered = json.dumps(result, indent=2) + '\n'
    print(rendered, end='')
    if args.report:
        args.report.write_text(rendered)
    raise SystemExit(bool(result['errors']))
