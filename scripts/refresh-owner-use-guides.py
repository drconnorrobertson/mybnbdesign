"""Apply reviewed owner-use articles before static staging; preserve publication dates."""
from pathlib import Path
from html import escape
import json,re
ROOT=Path(__file__).resolve().parents[1]
guides=json.loads((ROOT/'scripts/owner-use-guides.json').read_text())
changed={}
for d in guides:
 p=ROOT/d['file'];s=p.read_text();changed[d['url']]=d['updated']
 s=re.sub(r'<title>.*?</title>','<title>'+escape(d['title'])+' | MyBnBDesign</title>',s,count=1,flags=re.S)
 for key,value in [('description',d['description']),('og:title',d['title']),('twitter:title',d['title']),('og:description',d['description']),('twitter:description',d['description'])]:
  s=re.sub(r'(<meta\s+(?:name|property)="'+re.escape(key)+r'"\s+content=")[^"]*("\s*/?>)',lambda m:m[1]+escape(value,quote=True)+m[2],s)
 header='<h1>'+escape(d['title'])+'</h1><div class="blog-meta"><span>By MyBnBDesign Team</span> | <time datetime="2026-10-02">Published October 2, 2026</time> | <time datetime="2026-11-22">Reviewed November 22, 2026</time></div>'
 assert len(re.findall(r'<article\b',s))==1,d['file']
 s=re.sub(r'(<article\b[^>]*>).*?(</article>)',lambda m:m[1]+header+d['body']+m[2],s,count=1,flags=re.S)
 def schema(m):
  data=json.loads(m[1]);items=data if isinstance(data,list) else [data]
  for item in items:
   if item.get('@type')=='BlogPosting':
    assert item['datePublished']=='2026-10-02'
    item.update(headline=d['title'],description=d['description'],dateModified=d['updated'],citation=list(dict.fromkeys(re.findall(r'href="(https://[^"]+)"',d['body']))));item.pop('keywords',None)
   if item.get('@type')=='BreadcrumbList':
    for crumb in item.get('itemListElement',[]):
     if crumb.get('item')==d['url']:crumb['name']=d['title']
  return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False).replace('<','\\u003c')+'</script>'
 s=re.sub(r'<script type="application/ld\+json">(.*?)</script>',schema,s,flags=re.S)
 def crumbs(m):
  block=m[0];return re.sub(r'(<span>)[^<]*(</span>\s*</nav>)',lambda n:n[1]+escape(d['title'])+n[2],block)
 s=re.sub(r'<nav\b[^>]*aria-label="Breadcrumb"[^>]*>.*?</nav>',crumbs,s,flags=re.S)
 s=re.sub(r'<style id="owner-use-guide-style">.*?</style>','',s,flags=re.S).replace('</head>',d['style']+'</head>');p.write_text(s)
for p in ROOT.glob('sitemap*.xml'):
 s=p.read_text()
 def date(m):
  block=m[0];match=re.search(r'<loc>(.*?)</loc>',block)
  if not match or match[1].strip() not in changed:return block
  tag='<lastmod>'+changed[match[1].strip()]+'</lastmod>'
  return re.sub(r'<lastmod>.*?</lastmod>',tag,block) if '<lastmod>' in block else block.replace('</loc>','</loc>'+tag)
 p.write_text(re.sub(r'<url>.*?</url>',date,s,flags=re.S))
print('Refreshed three reviewed owner-use guides; publication dates preserved.')
