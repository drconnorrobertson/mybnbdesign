"""Apply the verified November commercial comparison sections idempotently."""
from pathlib import Path
from html import escape as e
import json,re,sys
REPO=Path(__file__).resolve().parents[1]
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else REPO
DATA=json.loads((REPO/'scripts/commercial-comparisons.json').read_text())
def link(u,t):return '<a href="'+e(u,quote=True)+'">'+e(t)+'</a>'
def update(route,title,description,body):
 f=ROOT/route.lstrip('/')
 if route.endswith('/'):f=f/'index.html'
 if not f.exists():raise RuntimeError('Missing comparison owner: '+route)
 s=f.read_text();block='<!-- brand-choice:start --><section class="brand-choice" style="padding:24px;margin:24px auto;max-width:1080px;border:1px solid #cbd5e1;border-radius:10px">'+body+'</section><!-- brand-choice:end -->'
 if '<!-- brand-choice:start -->' in s:s=re.sub(r'<!-- brand-choice:start -->.*?<!-- brand-choice:end -->',lambda _:block,s,flags=re.S)
 else:
  # Follow the hero rather than nesting a section in its heading.
  start=s.index('<h1');end=s.find('</section>',start)
  mainend=s.find('</main>',start)
  if end<0 or end>mainend:end=s.index('</h1>',start)+len('</h1>')
  else:end+=len('</section>')
  s=s[:end]+block+s[end:]
 s=re.sub(r'<title>.*?</title>',lambda _:'<title>'+e(title)+'</title>',s,count=1,flags=re.S)
 s=re.sub(r'(<h1\b[^>]*>).*?(</h1>)',lambda m:m[1]+e(title)+m[2],s,count=1,flags=re.S)
 for key,value in [('description',description),('og:title',title),('twitter:title',title),('og:description',description),('twitter:description',description)]:
  pat=r'<meta\s+(?:name|property)=["\']'+key+r'["\']\s+content=["\'][^"\']*["\']\s*/?>'
  tag='<meta '+('property' if key.startswith('og:') else 'name')+'="'+key+'" content="'+e(value,quote=True)+'">'
  if re.search(pat,s):s=re.sub(pat,lambda _:tag,s,count=1)
  else:s=s.replace('</head>',tag+'</head>',1)
 def schema(m):
  d=json.loads(m[2])
  def walk(v):
   if isinstance(v,dict):
    typ=v.get('@type',[]);typ=[typ] if isinstance(typ,str) else typ
    if set(typ)&{'Article','WebPage','BlogPosting','CollectionPage'}:
     if 'headline' in v:v['headline']=title
     if 'name' in v:v['name']=title
     v['description']=description
     if 'dateModified' in v:v['dateModified']='2026-11-18'
    for x in v.values():walk(x)
   elif isinstance(v,list):
    for x in v:walk(x)
  walk(d);return m[1]+json.dumps(d,ensure_ascii=False)+m[3]
 s=re.sub(r'(<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',schema,s,flags=re.S)
 f.write_text(s)
 for sitemap in ROOT.glob('sitemap*.xml'):
  xml=sitemap.read_text()
  def dated(m):
   if '<loc>'+DATA['origin']+route+'</loc>' not in m[0]:return m[0]
   if '<lastmod>' in m[0]:return re.sub(r'<lastmod>.*?</lastmod>','<lastmod>2026-11-18</lastmod>',m[0])
   return m[0].replace('</url>','<lastmod>2026-11-18</lastmod></url>')
  nxt=re.sub(r'<url>.*?</url>',dated,xml,flags=re.S)
  if nxt!=xml:sitemap.write_text(nxt)
for p in DATA['providers']:
 brand=DATA['brand'];direct=p['direct'];alt=p['alternative']
 shared='<p><strong>Official source checked November 18, 2026:</strong> '+e(p['fact'])+' '+link(p['url'],'Read the provider’s own site')+'.</p>'
 body='<h2>'+e(p['heading'])+'</h2><p>'+e(p['reason'])+'</p><ul>'+''.join('<li>'+e(x)+'</li>' for x in p['points'])+'</ul>'+shared+'<p>'+link(DATA['services'],'See '+brand+' services')+' · '+link(alt,'Compare '+p['name']+' alternatives')+'</p><p>'+link(DATA['cta'],DATA['cta_text'])+'</p><p><small>Published by '+e(brand)+', a competing provider. This recommendation describes client fit and published scope, not independently tested superiority. Confirm current fees, availability and deliverables in writing.</small></p>'
 update(direct,brand+' vs '+p['name']+': Scope & Best Fit', 'Compare '+brand+' and '+p['name']+'. See why our service fits this buyer, the published scope and questions to resolve before choosing.',body)
 altbody='<h2>Start your shortlist with '+e(brand)+'</h2><p>'+e(p['reason'])+'</p><p>'+link(direct,brand+' vs '+p['name']+': compare our service directly')+'</p>'+shared+'<p>Compare the same project brief and complete cost across providers. An unlisted service is unconfirmed, not proof that it is unavailable.</p><p>'+link(DATA['cta'],DATA['cta_text'])+'</p>'
 update(alt,p['name']+' Alternatives: Why Choose '+brand+'?', 'Considering '+p['name']+' alternatives? Review '+brand+' fit, compare service scope and prepare the questions for your next provider call.',altbody)
 # Add a short crawlable route from the homepage and existing comparison hub.
cards='<h2>Why choose '+e(DATA['brand'])+'? Compare your shortlist</h2><ul>'+''.join('<li>'+link(p['direct'],DATA['brand']+' vs '+p['name'])+' · '+link(p['alternative'],'Alternatives')+'</li>' for p in DATA['providers'])+'</ul>'
for route in ['index.html','compare/index.html']:
 f=ROOT/route;s=f.read_text();block='<!-- brand-comparison-links:start --><section style="padding:32px 24px;max-width:1080px;margin:auto">'+cards+'</section><!-- brand-comparison-links:end -->'
 s=re.sub(r'<!-- brand-comparison-links:start -->.*?<!-- brand-comparison-links:end -->','',s,flags=re.S)
 if '</main>' in s:s=s.replace('</main>',block+'</main>',1)
 else:s=s.replace('<footer',block+'<footer',1)
 f.write_text(s)
print(DATA['brand']+': updated '+str(2*len(DATA['providers']))+' comparison/alternative pages and two discovery routes')
