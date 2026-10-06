"""Validate rendered editorial output, numerical examples, and complete sitemap links."""
from pathlib import Path
import argparse, sys, json, re, xml.etree.ElementTree as E
from urllib.parse import urljoin, urlsplit
from collections import Counter
from html.parser import HTMLParser

SOURCE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SOURCE))
from content.host_guides import GUIDES, CLUSTERS
import content.materials,content.layouts,content.lighting,content.comfort
import content.maintenance,content.outdoors,content.launch,content.repairs
from scripts.audit_internal_discovery import Page
from scripts.build_host_library import route,target,ORIGIN,DATE

class Metadata(HTMLParser):
    def __init__(self,text):
        super().__init__();self.descriptions=[];self.og_urls=[];self.h1=0;self.refs=[];self.ids=set();self.ld=[];self.in_ld=False;self.buf='';self.feed(text)
    def handle_starttag(self,t,attrs):
        a=dict(attrs)
        if t=='h1':self.h1+=1
        if t=='meta' and a.get('name')=='description':self.descriptions.append(a.get('content',''))
        if t=='meta' and a.get('property')=='og:url':self.og_urls.append(a.get('content',''))
        if a.get('id'):self.ids.add(a['id'])
        for key in ['href','src']:
            if a.get(key):self.refs.append(a[key])
        if t=='script' and a.get('type')=='application/ld+json':self.in_ld=True;self.buf=''
    def handle_data(self,d):
        if self.in_ld:self.buf+=d
    def handle_endtag(self,t):
        if t=='script' and self.in_ld:self.ld.append(json.loads(self.buf));self.in_ld=False

def run(root):
    errors=[];titles=[];descriptions=[];wordcounts=[];newroutes=[]
    rendered=[route(g) for g in GUIDES]+['/resources/'+c+'/' for c in CLUSTERS]+['/resources/']
    for r in rendered:
        f=target(root,r);s=f.read_text();p=Page(s);m=Metadata(s)
        expected=ORIGIN+r
        if p.canonical!=expected:errors.append(r+': canonical mismatch')
        if m.og_urls!=[expected]:errors.append(r+': OG URL mismatch')
        if m.h1!=1:errors.append(r+': must have one h1')
        if len(m.descriptions)!=1 or not 70<=len(m.descriptions[0])<=200:errors.append(r+': description missing or inappropriate length')
        titles.append(p.title);descriptions.extend(m.descriptions)
        if not m.ld:errors.append(r+': schema missing')
        else:
            graph=m.ld[0];primary=graph[0]
            if primary['@id']!=expected or primary['url']!=expected or primary['dateModified']!=DATE:errors.append(r+': schema parity mismatch')
            if primary['@type']=='Article':
                if primary['headline']!=p.h1 or primary['mainEntityOfPage']['@id']!=expected:errors.append(r+': article identity mismatch')
                if primary['datePublished']>DATE:errors.append(r+': future publication date')
        for ref in m.refs:
            u=urlsplit(urljoin(expected,ref))
            if u.netloc not in ['www.mybnbdesign.com','mybnbdesign.com']:continue
            local=target(root,u.path if u.path else '/')
            if not local.is_file():errors.append(r+': missing local target '+ref)
            elif u.fragment:
                if u.path==r:ids=m.ids
                else:ids=Metadata(local.read_text()).ids if local.suffix=='.html' else set()
                if u.fragment not in ids:errors.append(r+': missing fragment '+ref)
    for g in GUIDES:
        wc=len(' '.join(g[k] for k in ['intro','decision','example','checklist','handoff']).split());wordcounts.append(wc)
        if wc<230:errors.append(g['slug']+': insufficient authored depth')
        if not g.get('repair'):newroutes.append(route(g))
    if len(newroutes)!=60 or len(CLUSTERS)!=8:errors.append('Incorrect new guide or hub count')
    if len(set(titles))!=len(titles):errors.append('Duplicate rendered titles')
    if len(set(descriptions))!=len(descriptions):errors.append('Duplicate rendered descriptions')
    policy=json.loads((SOURCE/'content/blog_discovery_policy.json').read_text())
    for expected in policy['approved_existing_additions']:
        s=target(root,urlsplit(expected).path).read_text();p=Page(s);m=Metadata(s)
        if p.canonical!=expected or m.og_urls!=[expected]:errors.append(expected+': promoted guide identity mismatch')
        primary=next((x for x in m.ld if isinstance(x,dict) and x.get('@type') in ['Article','BlogPosting']),None)
        if not primary or primary['mainEntityOfPage']['@id']!=expected or primary['headline']!=p.h1 or primary['dateModified']!=DATE:errors.append(expected+': promoted guide schema mismatch')
        if any(re.search(r'profitable|drive five-star|appeal to every guest',d,re.I) for d in m.descriptions):errors.append(expected+': unsupported outcome in promoted description')
    # Concrete numerical scenarios, independent of DOM markup.
    numerical={
      'landed_chairs':360+70+40+36==506,
      'installed_chair_unit':506/2==253,
      'second_quote':480+38.40==518.40,
      'quote_difference':round(518.40-506,2)==12.40,
      'replacement_allowance':1200/4+180/3+300/5==420,
      'replacement_monthly':420/12==35,
      'sofa_a_per_stay':(1000+200)/200==6,
      'sofa_b_replaced_per_stay':(700+700)/200==7,
      'sofa_b_no_replacement':700/200==3.5,
      'linen_single_cycle':3+3+3==9,
      'linen_two_cycles':3+6+3==12,
      'laundry_sequential_hours':4*2==8,
      'repair_price_difference':190-160==30,
    }
    if not all(numerical.values()):errors.append('Numerical scenario failure')
    # The text itself must contain the operands/results validated above.
    expected_phrases={
      'landed-furnishing-cost':['$360','$70','$40','$36','$506','$253','$480','$38.40','$518.40','$12.40'],
      'replacement-reserve-worksheet':['$1,200','four years','$300','three years','$60','five years','$420','$35'],
      'furniture-cost-per-use':['200 guest stays','$1,000','$200','$1,200','$6','$700','$1,400','$7','$3.50'],
      'linen-par-stock-calculation':['nine complete sets','equals twelve'],
      'laundry-turnover-capacity':['four compatible loads','two hours','eight hours'],
      'repair-or-replace-decision-log':['$160','$190','$30']}
    for slug,phrases in expected_phrases.items():
        g=next(g for g in GUIDES if g['slug']==slug)
        for phrase in phrases:
            if phrase not in g['example']:errors.append(slug+': missing validated numerical phrase '+phrase)
    sitemap_counts={};listed=set()
    for file in root.glob('sitemap*.xml'):
        doc=E.parse(file);urls=[x.text for x in doc.findall('.//{*}loc')];sitemap_counts[file.name]=len(urls)
        if len(urls)!=len(set(urls)):errors.append(file.name+': duplicate URLs')
        for u in urls:
            if u in listed:errors.append('URL listed in multiple sitemaps: '+u)
            listed.add(u);f=target(root,urlsplit(u).path)
            if not f.is_file():errors.append('Missing sitemap URL '+u);continue
            p=Page(f.read_text())
            if p.noindex or p.canonical!=u:errors.append('Ineligible sitemap URL '+u)
        for d in doc.findall('.//{*}lastmod'):
            if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',d.text or '') or d.text>DATE:errors.append('Invalid sitemap date '+str(d.text))
    for r in newroutes+['/resources/'+c+'/' for c in CLUSTERS]:
        if ORIGIN+r not in listed:errors.append('New route missing from sitemap '+r)
    report=dict(rendered_pages_checked=len(rendered),promoted_legacy_metadata_checked=len(policy['approved_existing_additions']),new_guides=60,new_hubs=8,legacy_repairs=16,authored_words=sum(wordcounts),minimum_authored_words=min(wordcounts),unique_titles=len(set(titles)),unique_descriptions=len(set(descriptions)),sitemap_counts=sitemap_counts,combined_sitemap_urls=len(listed),numerical_checks=numerical,errors=errors)
    print(json.dumps(report,indent=2));return report

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=SOURCE);parser.add_argument('--report',type=Path);args=parser.parse_args()
    r=run(args.root.resolve())
    if args.report:args.report.write_text(json.dumps(r,indent=2)+'\n')
    raise SystemExit(1 if r['errors'] else 0)
