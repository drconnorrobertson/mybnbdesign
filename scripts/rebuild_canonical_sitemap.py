"""Build the established sitemap from reviewed, indexable self-canonical HTML owners."""
from pathlib import Path
import sys,re,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from audit_internal_discovery import Page,ORIGIN
NS='http://www.sitemaps.org/schemas/sitemap/0.9';E.register_namespace('',NS)
dates={}
for sm in ROOT.glob('sitemap*.xml'):
 for row in E.parse(sm).getroot():
  loc=row.find('{*}loc');lm=row.find('{*}lastmod')
  if loc is not None and lm is not None and lm.text and re.fullmatch(r'\d{4}-\d{2}-\d{2}',lm.text):dates[loc.text]=max(dates.get(loc.text,''),lm.text)
urls=[]
for f in ROOT.rglob('*.html'):
 if any(p.startswith('.') or p in ('dist','node_modules') for p in f.relative_to(ROOT).parts):continue
 r='/'+f.relative_to(ROOT).as_posix();r=r[:-10] if r.endswith('/index.html') else r
 p=Page(f.read_text());url=ORIGIN+r
 if p.canonical==url and not p.noindex:urls.append(url)
assert len(urls)==len(set(urls))
root=E.Element('{'+NS+'}urlset')
for u in sorted(urls):
 row=E.SubElement(root,'{'+NS+'}url');E.SubElement(row,'{'+NS+'}loc').text=u
 if u in dates:E.SubElement(row,'{'+NS+'}lastmod').text=dates[u]
E.indent(root);(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n'+E.tostring(root,encoding='unicode')+'\n')
print('Established main sitemap canonical URLs:',len(urls))
