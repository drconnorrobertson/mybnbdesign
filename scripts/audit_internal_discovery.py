"""Inventory canonical orphan pages without assuming unavailable Search Console metrics."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit
from collections import deque
import argparse, json, re, html

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://www.mybnbdesign.com'

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.canonical = ''; self.noindex = False; self.links=[]; self.title=''; self.h1=''
        self.capture=''; self.body=[]; self.ignored=0
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='link' and a.get('rel')=='canonical': self.canonical=a.get('href','')
        if tag=='meta' and a.get('name','').lower()=='robots' and 'noindex' in a.get('content','').lower(): self.noindex=True
        if tag=='a' and a.get('href'): self.links.append(a['href'])
        if tag in ['title','h1']:self.capture=tag
        if tag in ['script','style']:self.ignored+=1
    def handle_endtag(self, tag):
        if tag in ['title','h1']:self.capture=''
        if tag in ['script','style']:self.ignored=max(0,self.ignored-1)
    def handle_data(self, data):
        if self.capture=='title':self.title+=data
        if self.capture=='h1':self.h1+=data
        if not self.ignored:self.body.append(data)

def inventory():
    files={}; pages={}; excluded=[]
    for f in sorted(ROOT.rglob('*.html')):
        if any(x.startswith('.') for x in f.relative_to(ROOT).parts):continue
        text=f.read_text(); p=Page(text); rel=f.relative_to(ROOT).as_posix()
        route='/' + rel
        if route.endswith('/index.html'):route=route[:-10]
        c=urlsplit(p.canonical)
        eligible=not p.noindex and c.netloc=='www.mybnbdesign.com' and c.path==route and not c.query
        if not eligible:
            reason='noindex' if p.noindex else 'no canonical or empty/test utility' if not p.canonical else 'alternate/non-self canonical'
            excluded.append(dict(file=rel, title=p.title, canonical=p.canonical, reason=reason, bytes=len(text.encode())))
            continue
        url=ORIGIN+route
        files[rel]=url;pages[url]=dict(file=rel,title=html.unescape(p.title),links=p.links,words=len(' '.join(p.body).split()))
    incoming={u:set() for u in pages};outgoing={u:set() for u in pages}
    def target(source, href):
        q=urlsplit(urljoin(source,href))
        if q.netloc not in ['www.mybnbdesign.com','mybnbdesign.com'] or q.scheme not in ['https','http']:return None
        path=q.path.lstrip('/')
        candidates=[path, path+'index.html' if path.endswith('/') else path+'/index.html']
        for candidate in candidates:
            if candidate in files:return files[candidate]
        return None
    for u,p in pages.items():
        for h in p['links']:
            t=target(u,h)
            if t and t!=u:incoming[t].add(u);outgoing[u].add(t)
    reached=set();q=deque([ORIGIN+'/'])
    while q:
        u=q.popleft()
        if u in reached:continue
        reached.add(u);q.extend(outgoing.get(u,[])-reached)
    import xml.etree.ElementTree as E
    sm={x.text for f in ROOT.glob('sitemap*.xml') for x in E.parse(f).findall('.//{*}loc')}
    rows=[]
    for u,p in pages.items():
        if incoming[u] and u in reached:continue
        title=p['title'].split(' | ')[0]
        folder=urlsplit(u).path.split('/')[1]
        source={'blog':'/blog/','compare':'/compare/','reviews':'/reviews/','alternatives':'/compare/','resources':'/resources/','case-studies':'/case-studies/','tools':'/tools/','markets':'/markets/','faq':'/faq/'}.get(folder,'/resources/')
        if p['words']<180:decision='repair-first';reason='Short content needs editorial review before promotion'
        elif folder in ['case-studies','reviews','alternatives','compare']:
            decision='review-first';reason='Verify evidence, comparison claims, and consistency before adding promotion'
        else:decision='implement';reason='Relevant existing guide; add descriptive link in the matching topic hub after readiness review'
        rows.append(dict(url=u,title=title,words=p['words'],zero_indexable_inbound=not incoming[u],homepage_unreachable=u not in reached,inbound_count=len(incoming[u]),in_sitemap=u in sm,sitemap_only_discovery=not incoming[u] and u in sm,content_readiness=decision,proposed_source=ORIGIN+source,source_gsc_clicks=None,source_gsc_impressions=None,source_gsc_average_position=None,gsc_status='unavailable; structural source, ranking not established',anchor=title,placement='Relevant guide entry in same-site topic hub, after descriptive introduction',reason=reason))
    return dict(canonical_pages=len(pages),zero_indexable_inbound=sum(not incoming[u] for u in pages),homepage_unreachable=len(set(pages)-reached),sitemap_only_discovery=sum(not incoming[u] and u in sm for u in pages),mapping=rows,excluded=excluded)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    report=inventory();out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2))
    md=['# My BNB Design internal discovery mapping','', 'Search Console metrics are unavailable. Proposed sources are structural and relevant; rankings have not been established.','', f"Canonical pages: {report['canonical_pages']}; zero indexable inbound: {report['zero_indexable_inbound']}; homepage-unreachable: {report['homepage_unreachable']}; sitemap-only: {report['sitemap_only_discovery']}.",'','| URL / title | Readiness and discovery | Proposed source | Anchor and placement | GSC metrics | Decision |','|---|---|---|---|---|---|']
    for r in report['mapping']:
        md.append(f"| [{r['title'].replace('|','/')} ]({r['url']}) | {r['words']} words; zero inbound={r['zero_indexable_inbound']}; homepage unreachable={r['homepage_unreachable']}; sitemap={r['in_sitemap']} | {r['proposed_source']} | {r['anchor'].replace('|','/')} — {r['placement']} | Unavailable | {r['content_readiness']}: {r['reason']} |")
    md.extend(['','## Excluded utility, alternate and noncanonical files','','| File | Canonical | Reason |','|---|---|---|'])
    for r in report['excluded']:md.append(f"| {r['file']} | {r['canonical']} | {r['reason']} |")
    out.with_suffix('.md').write_text('\n'.join(md)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['mapping','excluded']}));print('Mapping rows:',len(report['mapping']),'excluded files:',len(report['excluded']))
