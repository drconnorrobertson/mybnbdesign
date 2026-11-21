"""Publish two sourced buying guides at their established canonical owners."""
from pathlib import Path
from html import escape
import json,re
ROOT=Path(__file__).resolve().parents[1]
FILES=['best-knife-set-for-airbnb-kitchen','best-air-purifier-for-airbnb']
changed={}
for slug in FILES:
 d=json.loads((ROOT/'content/editorial'/(slug+'.json')).read_text());p=ROOT/d['file'];text=p.read_text();changed[d['url']]=d['updated']
 text=re.sub(r'<title>.*?</title>','<title>'+escape(d['title'])+' | MyBnBDesign</title>',text,count=1,flags=re.S)
 for key,value in [('description',d['description']),('og:title',d['title']),('twitter:title',d['title']),('og:description',d['description']),('twitter:description',d['description'])]:
  text=re.sub(r'(<meta\s+(?:name|property)="'+re.escape(key)+r'"\s+content=")[^"]*("\s*/?>)',lambda m:m[1]+escape(value,quote=True)+m[2],text)
 text=re.sub(r'(<div class="hero">).*?(</div>)',lambda m:m[1]+'<h1>'+escape(d['title'])+'</h1><p>'+escape(d['description'])+'</p>'+m[2],text,count=1,flags=re.S)
 text=re.sub(r'<div class="meta">.*?</div>','<div class="meta"><span>By MyBnBDesign Team</span><span>Reviewed November 21, 2026</span><span>Buying guides</span></div>',text,count=1,flags=re.S)
 cta='<div class="cta-box"><h2>Plan the whole room before ordering</h2><p>Explore our <a style="color:inherit;text-decoration:underline" href="/services.html">Airbnb design and furnishing services</a>. For related investment and launch support, visit <a style="color:inherit;text-decoration:underline" href="https://www.bnbaccelerator.com/">BNB Accelerator</a>.</p><a href="/book/" class="cta-btn">Discuss Your Property</a></div>'
 text=re.sub(r'<article>.*?</article>','<article>'+d['body']+cta+'</article>',text,count=1,flags=re.S)
 # Preserve the original publication date; replace malformed keywords and unsupported FAQ claims.
 def schema(m):
  old=json.loads(m[1]);post=old[0] if isinstance(old,list) else old
  if post.get('@type')!='BlogPosting':return m[0]
  post.update(headline=d['title'],description=d['description'],dateModified=d['updated'])
  post.pop('keywords',None);post['publisher'].pop('logo',None)
  post['citation']=list(dict.fromkeys(re.findall(r'href="(https://[^"]+)"',d['body'])))
  return '<script type="application/ld+json">'+json.dumps(post,ensure_ascii=False).replace('<','\\u003c')+'</script>'
 text=re.sub(r'<script type="application/ld\+json">(.*?)</script>',schema,text,flags=re.S)
 styles='<style id="reviewed-buying-style">.buying-table{overflow-x:auto;margin:24px 0}.buying-table table{width:100%;border-collapse:collapse;font-size:15px;text-align:left}.buying-table th,.buying-table td{padding:14px;border:1px solid #d2d8d2;vertical-align:top}.buying-table caption{font-weight:600;text-align:left;margin-bottom:12px}article h3{margin:24px 0 12px}article li{margin:8px 0 8px 24px}.buying-table a{text-decoration:underline}</style>'
 text=re.sub(r'<style id="reviewed-buying-style">.*?</style>','',text,flags=re.S).replace('</head>',styles+'</head>')
 p.write_text(text)
parents=[('blog/airbnb-kitchen-essentials-checklist.html','Choose knives your reset team can maintain','Compare two <a href="/blog/best-knife-set-for-airbnb-kitchen/">knife sets for an Airbnb kitchen</a>, with the exact care requirements, storage questions and a downloadable inventory checklist.'),('resources/maintenance/index.html','Plan air purifier upkeep before buying','Use our <a href="/blog/best-air-purifier-for-airbnb/">Airbnb air purifier comparison</a> to record room fit, controls, filter references and the role responsible for upkeep.')]
for name,title,body in parents:
 p=ROOT/name;text=p.read_text();marker=r'<!-- reviewed-buying-link:start -->.*?<!-- reviewed-buying-link:end -->'
 block='<!-- reviewed-buying-link:start --><section style="max-width:1000px;margin:32px auto;padding:24px;line-height:1.7"><h2>'+title+'</h2><p>'+body+'</p></section><!-- reviewed-buying-link:end -->'
 if re.search(marker,text,re.S):text=re.sub(marker,lambda m:block,text,flags=re.S)
 elif '</main>' in text:text=text.replace('</main>',block+'</main>',1)
 else:text=re.sub(r'<footer\b',lambda m:block+m[0],text,count=1)
 p.write_text(text)
 changed['https://www.mybnbdesign.com/'+name.replace('index.html','')]='2026-11-21'
for p in ROOT.glob('sitemap*.xml'):
 text=p.read_text()
 def date(m):
  block=m[0];url=re.search(r'<loc>(.*?)</loc>',block)[1]
  if url not in changed:return block
  tag='<lastmod>'+changed[url]+'</lastmod>'
  return re.sub(r'<lastmod>.*?</lastmod>',tag,block) if '<lastmod>' in block else block.replace('</loc>','</loc>'+tag)
 text=re.sub(r'<url>.*?</url>',date,text,flags=re.S);p.write_text(text)
print('Published two sourced buying guides and two contextual discovery links.')
