"""Deterministically render the original host library and reviewed legacy repairs.

Use --output-root to render a review copy before applying link changes to the site.
"""
from pathlib import Path
from urllib.parse import urlsplit
import argparse, sys, html, json, re, xml.etree.ElementTree as E

SOURCE = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SOURCE))
from content.host_guides import GUIDES, CLUSTERS, SOURCES
import content.materials, content.layouts, content.lighting, content.comfort
import content.maintenance, content.outdoors, content.launch, content.repairs
from content.resource_artifacts import ARTIFACTS

ORIGIN='https://www.mybnbdesign.com'
DATE='2026-10-06'
NS='http://www.sitemaps.org/schemas/sitemap/0.9'
E.register_namespace('',NS)
esc=lambda x:html.escape(str(x),quote=True)

def route(g):return g.get('route','/resources/guides/'+g['slug']+'/')
def url(g):return ORIGIN+route(g)
def target(root,r):
    p=root/r.lstrip('/')
    return p/'index.html' if r.endswith('/') else p
def paragraphs(s):return ''.join('<p>'+esc(p.strip())+'</p>\n' for p in s.strip().split('\n\n'))
def bullets(s,ordered=False):
    tag='ol' if ordered else 'ul'
    return '<'+tag+'>'+''.join('<li>'+esc(p.strip())+'</li>' for p in s.strip().splitlines() if p.strip())+'</'+tag+'>'
def link(r,label):return '<a href="'+esc(r)+'">'+esc(label)+'</a>'
def breadcrumbs(items):
    return '<nav class="library-breadcrumb" aria-label="Breadcrumb"><ol>'+''.join('<li>'+link(r,t)+'</li>' for r,t in items)+'</ol></nav>'

def shell(title,description,r,main,crumbs,article=False,extra_schema=None,published=None):
    canonical=ORIGIN+r
    schema=[dict(**{'@context':'https://schema.org','@type':'Article' if article else 'CollectionPage','@id':canonical},
                 headline=title if article else None,name=title,description=description,url=canonical,
                 dateModified=DATE,**({'datePublished':published or DATE,'author':{'@type':'Organization','name':'MyBnBDesign','url':ORIGIN+'/'},'publisher':{'@type':'Organization','name':'MyBnBDesign','url':ORIGIN+'/'},'mainEntityOfPage':{'@type':'WebPage','@id':canonical}} if article else {})),
            {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i+1,'name':t,'item':ORIGIN+x} for i,(x,t) in enumerate(crumbs)]}]
    schema[0]={k:v for k,v in schema[0].items() if v is not None}
    if extra_schema:schema.append(extra_schema)
    js=json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} | MyBnBDesign</title><meta name="description" content="{esc(description)}"><meta name="robots" content="index, follow">
<link rel="canonical" href="{esc(canonical)}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{esc(canonical)}"><meta property="og:type" content="{'article' if article else 'website'}"><meta property="og:site_name" content="MyBnBDesign"><meta name="twitter:card" content="summary"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(description)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;1,500&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.min.css?v=20261003-layout"><link rel="stylesheet" href="/assets/host-library.css">
<script type="application/ld+json">{js}</script></head><body>
<a href="#main" class="skip-link">Skip to content</a>
<nav class="nav" id="nav" aria-label="Main navigation"><div class="container nav__inner"><a href="/" class="nav__logo">MyBnB<span>Design</span></a><ul class="nav__links" id="navLinks"><li><a href="/services.html" class="nav__link">Services</a></li><li><a href="/portfolio.html" class="nav__link">Portfolio</a></li><li><a href="/resources/" class="nav__link">Resources</a></li><li><a href="/book/" class="nav__link nav__link--cta">Book a Call</a></li></ul><button class="nav__toggle" id="navToggle" aria-label="Open menu" aria-controls="navLinks" aria-expanded="false"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><line x1="3" y1="7" x2="21" y2="7"/><line x1="3" y1="17" x2="21" y2="17"/></svg></button></div></nav>
<main id="main" class="library">{main}</main>
<footer class="footer"><div class="container footer__inner"><a href="/" class="footer__logo">MyBnB<span>Design</span></a><span class="footer__mid">A <a href="https://www.bnbaccelerator.com" rel="noopener">BnB Accelerator</a> Company</span><span class="footer__copy">&copy; 2026 MyBnBDesign</span></div></footer>
<script>document.getElementById('navToggle').addEventListener('click',()=>document.getElementById('navLinks').classList.toggle('is-open'));const nav=document.getElementById('nav');window.addEventListener('scroll',()=>nav.classList.toggle('is-scrolled',window.scrollY>80),{{passive:true}});</script><script src="/assets/menu.js?v=20261003-layout"></script>
</body></html>'''

def header(title,description,crumbs):
    return '<header class="library-header">'+breadcrumbs(crumbs)+'<p class="eyebrow">THE HOST PLANNING LIBRARY</p><h1>'+esc(title)+'</h1><p class="lead">'+esc(description)+'</p><p class="guide-date">Updated <time datetime="'+DATE+'">October 6, 2026</time></p></header>'

def card(g):
    return '<article class="library-card"><h3>'+link(route(g),g['title'])+'</h3><p>'+esc(g['description'])+'</p>'+link(route(g),'Read the guide →')+'</article>'

def cta():
    return '<section class="guide-cta"><h2>Plan your rental with a clear brief</h2><p>Bring your room measurements, priorities, and project questions to a conversation about your property.</p><a href="/book/" class="btn">Book a design conversation</a></section>'

def artifact_text(g):
    """Export the same reviewed inventory and template content as the page."""
    parts=[g['title'], ORIGIN+route(g), 'Replace bracketed fields with verified property information.']
    for s in g.get('artifacts', []):
        parts.extend(['', s['title'], s['text']])
        if s['headers']:
            for row in s['rows']:
                parts.append('\n'.join(f'{label}: {value}' for label,value in zip(s['headers'],row)))
        if s['template']:parts.append(s['template'])
        parts.extend('- '+item for item in s['items'])
    return '\n\n'.join(p for p in parts if p)+'\n'

def render_artifacts(g):
    sections=g.get('artifacts', [])
    if not sections:return ''
    body='<section class="resource-artifacts" aria-labelledby="resource-worksheets"><h2 id="resource-worksheets">Inventories, templates and working records</h2><p>Use the worksheets below with your actual property information. <a href="'+esc(route(g)+'worksheet.txt')+'" download>Download the complete plain-text worksheet</a></p>'
    body+='<nav aria-label="Worksheet sections"><ul>'+''.join('<li>'+link('#'+s['id'],s['title'])+'</li>' for s in sections)+'</ul></nav>'
    for s in sections:
        body+='<section aria-labelledby="'+esc(s['id'])+'"><h3 id="'+esc(s['id'])+'">'+esc(s['title'])+'</h3>'+paragraphs(s['text'])
        if s['headers']:
            body+='<div class="artifact-table-wrap" role="region" aria-label="'+esc(s['title'])+' table" tabindex="0"><table class="artifact-table"><caption>'+esc(s['title'])+'</caption><thead><tr>'+''.join('<th scope="col">'+esc(h)+'</th>' for h in s['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(cell)+'</td>' for cell in row)+'</tr>' for row in s['rows'])+'</tbody></table></div>'
        if s['template']:body+='<pre class="artifact-template">'+esc(s['template'])+'</pre>'
        if s['items']:body+='<ul>'+''.join('<li>'+esc(item)+'</li>' for item in s['items'])+'</ul>'
        body+='</section>'
    return body+'</section>'

def render_guide(g):
    r=route(g);cluster=CLUSTERS[g['cluster']];hub='/resources/'+g['cluster']+'/'
    crumbs=[('/','Home'),('/resources/','Resources'),(hub,cluster['title']),(r,g['title'])]
    siblings=[x for x in GUIDES if x['cluster']==g['cluster'] and x is not g and not x.get('repair')]
    # Curated cluster relationships, not arbitrary city or synonym variants.
    cross={'planning':'quote-scope-comparison','materials':'furniture-product-care-register','layouts':'test-stay-commissioning-log','lighting':'room-reset-photo-standard','comfort':'laundry-turnover-capacity','maintenance':'furnishing-handover-pack','outdoors':'seasonal-outdoor-handoff','launch':'landed-furnishing-cost'}[g['cluster']]
    chosen=siblings[:2]+[x for x in GUIDES if x['slug']==cross and x is not g]
    content=header(g['title'],g['description'],crumbs)
    content+='<article class="guide-content">'+paragraphs(g['intro'])+render_artifacts(g)+'<h2>Make the decision from the actual setup</h2>'+paragraphs(g['decision'])
    content+='<section class="guide-example"><h2>Worked planning example</h2><p><strong>Illustrative scenario:</strong> Examples, prices, quantities, and timing assumptions below are hypothetical; use actual product information and local quotes for your property.</p>'+paragraphs(g['example'])+'</section>'
    content+='<h2>Practical checklist</h2>'+bullets(g['checklist'],True)+'<h2>Carry the decision into the handover</h2>'+paragraphs(g['handoff'])
    content+='<section class="guide-sources"><h2>Sources and product instructions</h2><p>The sources below provide technical background. The planning examples and checklists are original. Use instructions for the exact installed product and obtain qualified review for relevant technical requirements.</p><ul>'+''.join('<li>'+link(SOURCES[k][1],SOURCES[k][0])+'</li>' for k in g['sources'])+'</ul><p>Source links reviewed October 6, 2026.</p></section>'
    content+='<section class="guide-related"><h2>Related planning steps</h2><ul>'+''.join('<li>'+link(route(x),x['title'])+'</li>' for x in chosen)+'<li>'+link(hub,'Explore '+cluster['title'].lower())+'</li></ul></section>'+cta()+'</article>'
    return shell(g['title'],g['description'],r,content,crumbs,article=True,published=g.get('published'))

def render_hub(key):
    c=CLUSTERS[key];r='/resources/'+key+'/'
    crumbs=[('/','Home'),('/resources/','Resources'),(r,c['title'])]
    guides=[g for g in GUIDES if g['cluster']==key and not g.get('repair')]
    repaired=[g for g in GUIDES if g['cluster']==key and g.get('repair')]
    body=header(c['title'],c['description'],crumbs)+'<div class="guide-content">'+paragraphs(c['intro'])+'<h2>Work through the decisions in order</h2>'+bullets('\n'.join(c['steps']),True)+'<p>Start with the earliest unresolved decision. Use the examples as worksheets, then replace their assumptions with measurements, written product specifications, and local operating information.</p></div><section aria-label="Detailed topic guides" class="library-grid">'+''.join(card(g) for g in guides)+'</section>'
    body+='<div class="guide-content"><h2>Broader guides and service questions</h2><ul>'+''.join('<li>'+link(route(g),g['title'])+'</li>' for g in repaired)+'<li>'+link(c['legacy'],'Related service or property planning guidance')+'</li></ul><p>'+link('/resources/','Browse the full planning library')+'</p>'+cta()+'</div>'
    items={'@context':'https://schema.org','@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'url':url(g),'name':g['title']} for i,g in enumerate(guides)]}
    return shell(c['title'],c['description'],r,body,crumbs,extra_schema=items)

def render_resources():
    r='/resources/';title='Short-Term Rental Design Planning Library';desc='Use practical rental design guides for budgets, materials, layouts, lighting, comfort, maintenance, outdoor spaces, procurement, and launch.'
    crumbs=[('/','Home'),(r,'Resources')]
    body=header(title,desc,crumbs)+'<div class="guide-content"><p>Plan the property by its real activities and constraints. Choose a topic below or search the guide collection for a specific decision. Each detailed guide includes a worked hypothetical example, an actionable checklist, and a handover step.</p><p>Start with '+link('/resources/planning/','scope, measurements, and the furnishing budget')+', then test layouts and materials before purchasing. For projects already installed, use the maintenance and guest-comfort guides to improve the reset and feedback process.</p></div>'
    body+='<section class="library-grid" aria-label="Planning topics">'+''.join('<article class="library-card"><h2>'+link('/resources/'+k+'/',c['title'])+'</h2><p>'+esc(c['description'])+'</p><p>'+str(sum(g['cluster']==k and not g.get('repair') for g in GUIDES))+' detailed decision guides</p></article>' for k,c in CLUSTERS.items())+'</section>'
    body+='<section class="guide-content"><h2>Start-to-finish project guides</h2><ul>'+''.join('<li>'+link(route(g),g['title'])+'</li>' for g in GUIDES if g.get('repair') and route(g).startswith('/resources/'))+'</ul></section>'
    body+='<section aria-label="Search detailed planning guides"><h2 style="font-size:2rem;margin-top:44px">Find a specific planning step</h2><label for="guide-search">Search by topic or activity</label><input class="library-search" id="guide-search" type="search" placeholder="Try delivery, cushions, linens or lighting"><p id="guide-search-status" class="library-search-status" role="status" aria-live="polite">60 detailed guides</p><div id="guide-search-results" class="library-grid">'+''.join(card(g) for g in GUIDES if not g.get('repair'))+'</div></section><div class="guide-content">'+cta()+'</div>'
    script='''<script>const input=document.getElementById('guide-search');const cards=[...document.querySelectorAll('#guide-search-results .library-card')];input.addEventListener('input',()=>{const q=input.value.trim().toLowerCase();let count=0;cards.forEach(c=>{c.hidden=!c.textContent.toLowerCase().includes(q);if(!c.hidden)count++;});document.getElementById('guide-search-status').textContent=count+' matching guide'+(count===1?'':'s');});</script>'''
    return shell(title,desc,r,body,crumbs).replace('</body>',script+'</body>')

def upsert_panel(path,key,body):
    text=path.read_text();marker='<!-- '+key+' -->';end='<!-- /'+key+' -->';panel=marker+'\n'+body+'\n'+end
    if '/assets/host-library.css' not in text:
        text=text.replace('</head>','<link rel="stylesheet" href="/assets/host-library.css">\n</head>')
    pattern=re.escape(marker)+'.*?'+re.escape(end)
    if marker in text:text=re.sub(pattern,lambda m:panel,text,flags=re.S)
    else:
        position=text.find('<footer')
        if position<0:position=text.find('</main>')
        if position<0:position=text.find('</body>')
        text=text[:position]+panel+'\n'+text[position:]
    path.write_text(text)

def build(root):
    for g in GUIDES:
        f=target(root,route(g))
        if g.get('repair') and f.is_file():
            old=re.search(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})',f.read_text())
            if old and old[1]<=DATE:g['published']=old[1]
        f.parent.mkdir(parents=True,exist_ok=True);f.write_text(render_guide(g))
        if route(g) in ARTIFACTS:
            (f.parent/'worksheet.txt').write_text(artifact_text(g))
    for k in CLUSTERS:
        f=target(root,'/resources/'+k+'/');f.parent.mkdir(parents=True,exist_ok=True);f.write_text(render_hub(k))
    target(root,'/resources/').write_text(render_resources())
    # Reviewed existing color-guide wording is fixed before new discovery links.
    edits={
      'blog/art-deco-color-palette-guide.html': [('an Art Deco palette can command premium nightly rates and generate the kind of listing photos that go viral','an Art Deco palette can provide a distinctive visual direction when its scale and finishes suit the property')],
      'blog/bathroom-color-palettes-for-spa-feel.html': [('create the complete spa experience that earns rave reviews','create a coordinated bathroom arrangement with useful guest functions')],
      'blog/neutral-palettes-that-work-in-every-market.html': [
        ('Neutral Palettes That Work in Every Market','Neutral Palettes to Test in Your Rental'),
        ('Neutral Palettes That Work In Every Market','Neutral Palettes to Test in Your Rental'),
        ('Five Neutral Palettes That Always Work','Five Neutral Palettes to Compare'),
        ('Neutral color palettes that appeal to every guest in every market. The safest, most profitable palette choices for STR owners.','Compare five neutral color directions for a rental, then test samples against the installed lighting, finishes, furnishings, and cleaning needs.'),
        ('Neutral color palettes are the safest, most profitable choice for short-term rental owners who want broad appeal.','Neutral color palettes provide a restrained starting point for a rental design brief.'),
        ('a well-executed neutral palette will attract guests across demographics, age groups, and design preferences','test a neutral palette against the property, intended guest activities, and actual lighting'),
        ('The business case for neutrals is strong. They do not date as quickly as trendy colors, they work with furniture and decor changes over time, and they appeal to the widest possible guest base. When your target market is everyone, neutrals are your best investment.','Neutral finishes can make later furniture comparisons easier, but the right choice depends on existing surfaces, care requirements, and the room’s light. Compare physical samples in the furnished space before specifying a whole-property scheme.'),
        ('It photographs beautifully and appeals to design-conscious guests without alienating anyone.','Check the samples in daylight and artificial light, then photograph the actual room to evaluate color consistency.'),
        ('It works in every climate and property type and ages gracefully over time.','Compare the cream samples with existing fixed finishes and choose suitable, documented care requirements.'),
        ('This is currently one of the most popular aesthetics on Instagram and Pinterest, which means guests will recognize it as current and share photos of your space.','Compare the proposed textures for cleaning, repairability, and fit with existing furnishings before choosing this direction.'),
        ('This palette works particularly well in urban properties and appeals to younger travelers. The high contrast also photographs exceptionally well.','Test the contrast in the room’s installed lighting and check reflections from glossy or dark surfaces at guest eye level.'),
      ],
      'blog/farmhouse-color-palette-guide.html': [
        ('And it photographs with a warmth and charm that attracts bookings across demographics.','Compare its warm finishes in the property’s lighting and photographs before deciding whether the direction fits the brief.'),
        ('These thoughtful details communicate care and attention that guests notice and appreciate in their reviews.','Keep decorative details manageable for cleaning, storage, and consistent room resets.'),
      ],
      'blog/living-room-colors-that-feel-welcoming.html': [
        ('<a href="https://www.mybnbdesign.com/blog/airbnb-reviews-design-connection.html">five-star reviews</a>','five-star reviews'),
        ('Choose living room colors that make guests feel instantly at home. These welcoming palettes drive five-star reviews.','Compare living-room color directions against the actual light, retained furnishings, finish samples, and cleaning needs of your rental.'),
      ],
    }
    for rel,pairs in edits.items():
        f=root/rel;s=f.read_text()
        for before,after in pairs:s=s.replace(before,after)
        s=re.sub(r'("dateModified"\s*:\s*")[^"]+',lambda m:m[1]+DATE,s)
        f.write_text(s)
    # Identity parity for all newly promoted color guides, including legacy metadata.
    policy=json.loads((SOURCE/'content/blog_discovery_policy.json').read_text())
    for canonical in policy['approved_existing_additions']:
        f=root/canonical.removeprefix(ORIGIN+'/');s=f.read_text()
        s=re.sub(r'(<meta[^>]*property="og:url"[^>]*content=")[^"]+',lambda m:m[1]+canonical,s)
        s=re.sub(r'("dateModified"\s*:\s*")[^"]+',lambda m:m[1]+DATE,s)
        def repair_schema(match):
            graph=json.loads(match[2]);title=re.search(r'<h1[^>]*>(.*?)</h1>',s,re.S)[1]
            def walk(node):
                if isinstance(node,list):
                    for child in node:walk(child)
                elif isinstance(node,dict):
                    if node.get('@type') in ['Article','BlogPosting']:
                        node['mainEntityOfPage']={'@type':'WebPage','@id':canonical}
                        node['url']=canonical;node['headline']=html.unescape(re.sub('<[^>]+>','',title))
                    if isinstance(node.get('image'),str):
                        image_url=urlsplit(node['image'])
                        if image_url.netloc in ['www.mybnbdesign.com','mybnbdesign.com'] and not (root/image_url.path.lstrip('/')).is_file():node.pop('image')
                    for value in node.values():walk(value)
            walk(graph)
            return match[1]+json.dumps(graph,ensure_ascii=False,indent=2).replace('<','\\u003c')+match[3]
        s=re.sub(r'(<script[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)',repair_schema,s,flags=re.S)
        def valid_image_meta(match):
            image_url=urlsplit(match[1])
            return '' if image_url.netloc in ['www.mybnbdesign.com','mybnbdesign.com'] and not (root/image_url.path.lstrip('/')).is_file() else match[0]
        s=re.sub(r'<meta[^>]*(?:property="og:image"|name="twitter:image")[^>]*content="([^"]+)"[^>]*>',valid_image_meta,s)
        if 'twitter:image' not in s:s=s.replace('name="twitter:card" content="summary_large_image"','name="twitter:card" content="summary"')
        s=re.sub(r'^[ \t]+$', '', s, flags=re.M)
        f.write_text(s)
    # Repair pre-existing broken home-section links in these two utility pages.
    replacements={'services':'/services.html','portfolio':'/portfolio.html','contact':'/book/','tools':'/tools/'}
    for rel in ['tools/amenity-checklist/index.html','tools/design-budget-calculator/index.html']:
        f=root/rel;s=f.read_text()
        for fragment,destination in replacements.items():
            s=s.replace('href="../../#'+fragment+'"','href="'+destination+'"')
        f.write_text(s)
    panel='<section class="library-resource-panel" aria-labelledby="host-library-heading"><h2 id="host-library-heading">Plan the details before you furnish</h2><p>Use measured layouts, transparent cost worksheets, and tested care plans to turn your room ideas into a usable rental.</p><ul><li>'+link('/resources/','Explore the rental design planning library')+'</li><li>'+link('/resources/planning/','Budget, scope, and room-planning worksheets')+'</li><li>'+link('/resources/launch/','Procurement, installation, and launch checklists')+'</li></ul></section>'
    # Older article navigation targets the homepage's #blog section.
    home_panel=panel.replace('<section class="library-resource-panel"','<section id="blog" class="library-resource-panel"').replace('</ul>','<li>'+link('/blog/','Browse the design and color guide collection')+'</li></ul>')
    upsert_panel(root/'index.html','HOST_LIBRARY_HOME',home_panel)
    upsert_panel(root/'services.html','HOST_LIBRARY_SERVICES',panel.replace('host-library-heading','service-library-heading'))
    # Existing blog regeneration is run separately and consumes an explicit reviewed policy.
    ns='{'+NS+'}';tree=E.parse(root/'sitemap.xml');doc=tree.getroot();rows={x.find(ns+'loc').text:x for x in doc}
    new=[ORIGIN+'/resources/'+k+'/' for k in CLUSTERS]+[url(g) for g in GUIDES if not g.get('repair')]
    touched=[ORIGIN+'/',ORIGIN+'/services.html',ORIGIN+'/resources/']+[url(g) for g in GUIDES if g.get('repair') and route(g).startswith('/resources/')]
    # Do not add unrelated legacy or test URLs merely to increase the sitemap count.
    for u in new+touched:
        if u not in rows:
            row=E.SubElement(doc,ns+'url');E.SubElement(row,ns+'loc').text=u;rows[u]=row
        row=rows[u];lm=row.find(ns+'lastmod')
        if lm is None:lm=E.SubElement(row,ns+'lastmod')
        lm.text=DATE
    E.indent(tree);tree.write(root/'sitemap.xml',encoding='utf-8',xml_declaration=True)
    print(json.dumps({'new_guides':60,'new_topic_hubs':8,'legacy_guides_repaired':16,'main_sitemap_urls':len(rows),'rendered_root':str(root)}))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-root',type=Path,default=SOURCE);args=parser.parse_args()
    build(args.output_root.resolve())
