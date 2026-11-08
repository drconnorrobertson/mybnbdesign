"""Apply the reviewed smart-lock handbook without changing its established URL."""
from pathlib import Path
from html import escape
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'content/editorial/smart-lock-handbook.json').read_text())
page = ROOT / data['file']
text = page.read_text()
text = re.sub(r'<title>.*?</title>', '<title>' + escape(data['title']) + ' | MyBnBDesign</title>', text, count=1, flags=re.S)
for name, value in [('description', data['description']), ('og:title', data['title']), ('twitter:title', data['title']), ('og:description', data['description']), ('twitter:description', data['description'])]:
    pattern = r'<meta\s+(?:name|property)="' + re.escape(name) + r'"\s+content="[^"]*"\s*/?>'
    tag = '<meta ' + ('property' if name.startswith('og:') else 'name') + '="' + name + '" content="' + escape(value, quote=True) + '">'
    text = re.sub(pattern, lambda _: tag, text)

def schema(match):
    obj = json.loads(match[1])
    if obj.get('@type') == 'BlogPosting':
        obj.update(headline=data['title'], description=data['description'], dateModified=data['updated'], mainEntityOfPage={'@type': 'WebPage', '@id': data['url']})
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + '\n</script>'
text = re.sub(r'<script type="application/ld\+json">(.*?)</script>', schema, text, flags=re.S)
hero = '<div class="hero">\n<h1>' + escape(data['title']) + '</h1>\n<p>' + escape(data['description']) + '</p>\n</div>'
text = re.sub(r'<div class="hero">.*?</div>', lambda _: hero, text, count=1, flags=re.S)
body = '<article>\n<p><small>Published October 2, 2026 · Reviewed November 8, 2026</small></p>\n' + data['body'] + '\n</article>'
text = re.sub(r'<article>.*?</article>', lambda _: body, text, count=1, flags=re.S)
text = text.replace('MyBnBDesign helps short-term rental owners create spaces that earn <a href="https://www.mybnbdesign.com/blog/airbnb-reviews-design-connection.html">five-star reviews</a> and maximize revenue. Let our team handle the design so you can focus on hosting.', 'Discuss the arrival layout, finish coordination, and design scope for your rental with MyBnBDesign. Product compatibility and installation require a separate review of the actual door and device.')
page.write_text(text)
NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
ET.register_namespace('', NS)
for sitemap in ROOT.glob('sitemap*.xml'):
    tree = ET.parse(sitemap)
    changed = False
    for row in tree.getroot():
        loc = row.find('{*}loc')
        if loc is not None and loc.text == data['url']:
            modified = row.find('{*}lastmod')
            if modified is None:
                modified = ET.SubElement(row, '{' + NS + '}lastmod')
            modified.text = data['updated']
            changed = True
    if changed:
        ET.indent(tree)
        tree.write(sitemap, encoding='utf-8', xml_declaration=True)
print('Reviewed smart-lock handbook refreshed at its existing canonical URL.')
