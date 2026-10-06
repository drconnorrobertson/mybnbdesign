"""Build the blog hub and sitemap from existing, indexable, self-canonical articles."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import html, re, json, argparse, sys, xml.etree.ElementTree as E
source=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--output-root',type=Path,default=source);args=parser.parse_args()
p=args.output_root.resolve();base='https://www.mybnbdesign.com';ns='http://www.sitemaps.org/schemas/sitemap/0.9';E.register_namespace('',ns)
sys.path.insert(0,str(source))
from content.host_guides import GUIDES
import content.repairs
policy=json.loads((source/'content/blog_discovery_policy.json').read_text())
allowed=set(policy['baseline_urls']+policy['approved_existing_additions'])
allowed.update(base+g['route'] for g in GUIDES if g.get('repair') and g.get('route','').startswith('/blog/'))
items={}
for f in (p/'blog').rglob('*.html'):
 if f==p/'blog/index.html':continue
 s=f.read_text();m=re.search(r'<link[^>]*rel=[\"\']canonical[\"\'][^>]*href=[\"\']([^\"\']+)',s,re.I)
 if not m or not m[1].startswith(base+'/blog/') or re.search(r'<meta[^>]*noindex',s,re.I):continue
 route=urlparse(m[1]).path.lstrip('/');target=p/route
 if route.endswith('/'):target=target/'index.html'
 if target!=f:continue
 if m[1] not in allowed:continue
 t=re.search(r'<title>(.*?)</title>',s,re.S|re.I);d=re.search(r'<meta[^>]*name=[\"\']description[\"\'][^>]*content=[\"\']([^\"\']*)',s,re.I)
 if not t:continue
 items[m[1]]=(html.unescape(re.sub(r'\s*[|–—]\s*MyBnBDesign.*','',t[1])),html.unescape(d[1]) if d else '')
rows=''.join('<article class="card"><div class="b"><h2><a href="'+html.escape(u,quote=True)+'">'+html.escape(t)+'</a></h2><p>'+html.escape(d)+'</p><a class="more" href="'+html.escape(u,quote=True)+'">Read the guide &rarr;</a></div></article>' for u,(t,d) in sorted(items.items(),key=lambda x:x[1][0].lower()))
main='<main class="wrap" id="blog"><p>Start with <a href="/resources/">the rental design planning library</a> for practical worksheets, <a href="/services.html">service scope</a>, or <a href="/compare/">design approach comparisons</a>.</p><p>For color decisions, compare <a href="/blog/coastal-color-palette-guide.html">coastal palette options</a>, <a href="/blog/how-to-choose-a-color-scheme-for-your-rental.html">a property color-planning process</a>, and <a href="/blog/neutral-palettes-that-work-in-every-market.html">neutral palettes to test in your rooms</a>.</p><label for="blog-filter">Find a guide</label><input id="blog-filter" type="search" placeholder="Search design, furniture or photography" style="display:block;width:100%;padding:1rem;margin:1rem 0"><div class="grid" id="blog-library">'+rows+'</div></main>'
script='<script>document.getElementById("blog-filter").addEventListener("input",function(){const q=this.value.toLowerCase();document.querySelectorAll("#blog-library .card").forEach(c=>{c.hidden=!c.textContent.toLowerCase().includes(q);c.style.display=c.hidden?"none":"";});});</script>'
template=(p/'scripts/blog-index-template.txt').read_text()
(p/'blog/index.html').write_text(template.replace('{{BLOG_MAIN}}',main).replace('{{COUNT}}',str(len(items))).replace('</body>',script+'</body>'))
root=E.Element('{'+ns+'}urlset')
changed={base+g['route'] for g in GUIDES if g.get('repair') and g.get('route','').startswith('/blog/')}|set(policy['approved_existing_additions'])
for u in sorted(items):
 row=E.SubElement(root,'{'+ns+'}url');E.SubElement(row,'{'+ns+'}loc').text=u
 if u in changed:E.SubElement(row,'{'+ns+'}lastmod').text='2026-10-06'
E.indent(root);(p/'sitemap-blog.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n'+E.tostring(root,encoding='unicode')+'\n');print('Blog articles:',len(items))
