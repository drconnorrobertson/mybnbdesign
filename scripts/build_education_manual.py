"""Render authored lessons; never manufacture indexed pages from topic permutations."""
from pathlib import Path
import sys,json,csv,re,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'))
from content.education_manual import LESSONS,SOURCES
import build_host_library as ui
ui.DATE='2026-10-13';H=ui.esc;BASE=ui.ORIGIN;PREFIX='/learn/';MANIFEST=[]
def link(u,t):return ui.link(u,t)
def output(route,title,desc,body,article=True):
 crumbs=[('/','Home'),(PREFIX,'STR design education')]
 if route!=PREFIX:crumbs.append((route,title))
 header='<header class="library-header">'+ui.breadcrumbs(crumbs)+'<p class="eyebrow">THE STR OWNER’S DESIGN MANUAL</p><h1>'+H(title)+'</h1><p class="lead">'+H(desc)+'</p><p>Published October 13, 2026 · MyBnBDesign editorial team</p></header>'
 document=ui.shell(title,desc,route,header+body,crumbs,article=article,published=ui.DATE)
 document=document.replace('</head>','<link rel="stylesheet" href="/assets/education-manual.css"><script defer src="/assets/education-manual.js"></script></head>')
 p=ROOT/route.lstrip('/')/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(document)
 return p
PARTNERS='<section class="guide-sources"><h2>Take the financial records to the right review</h2><p>Use <a href="https://www.aetaxadvisors.com/">AE Tax Advisors</a> for the broader tax-planning discussion and <a href="https://www.stratumcostsegregation.com/str-cost-segregation-resources/">Stratum’s STR cost segregation resources</a> for property-component evidence and study preparation. These are related business resources recommended by MyBnBDesign. Confirm separate scopes and fees directly. Preserve actual invoices and project facts; this design lesson does not determine deduction eligibility or tax classification.</p></section>'
for i,g in enumerate(LESSONS):
 route=PREFIX+g['slug']+'/';ids=['section-'+str(n+1) for n in range(len(g['sections']))]
 body='<article class="guide-content"><p>'+link('/design-roadmap/','Place this lesson in the full design roadmap')+' · '+link(PREFIX,'Browse all design lessons')+'</p>'
 body+='<nav class="lesson-toc" aria-label="Lesson contents"><h2>In this lesson</h2><ol>'+''.join('<li>'+link('#'+ident,title)+'</li>' for ident,(title,_) in zip(ids,g['sections']))+'<li>'+link('#design-lab',g['lab'][0])+'</li><li>'+link('#property-worksheet','Property worksheet')+'</li><li>'+link('#common-questions','Common questions')+'</li></ol></nav>'
 for ident,(title,text) in zip(ids,g['sections']):body+='<section aria-labelledby="'+ident+'"><h2 id="'+ident+'">'+H(title)+'</h2>'+ui.paragraphs(text)+'</section>'
 body+='<section class="guide-example"><h2>Worked property example</h2><p><strong>Hypothetical planning scenario, not a client result.</strong></p>'+ui.paragraphs(g['example'])+'</section>'
 body+='<section aria-labelledby="design-lab"><h2 id="design-lab">'+H(g['lab'][0])+'</h2>'+ui.paragraphs(g['lab'][1])+'</section>'
 body+='<section aria-labelledby="property-worksheet"><h2 id="property-worksheet">Apply the lesson to your property</h2><p>Record verified information for your property. Keep source documents with the worksheet and assign unresolved questions to the person who can answer them. Entries remain in this page until it is reloaded; they are not sent to MyBnBDesign. Download your completed record before leaving.</p><form data-education-worksheet><fieldset><legend>Property evidence and decision</legend><label>Property reference<input name="property" type="text" autocomplete="off"></label>'+''.join('<label>'+H(f)+'<textarea name="field-'+str(j)+'" rows="2"></textarea></label>' for j,f in enumerate(g['fields']))+'</fieldset><fieldset><legend>Review checklist</legend>'+''.join('<label class="education-check"><input type="checkbox" name="check-'+str(j)+'">'+H(c)+'</label>' for j,c in enumerate(g['checks']))+'</fieldset><p id="education-progress" role="status" aria-live="polite">0 of '+str(len(g['checks']))+' actions checked.</p><p>A checked box records your progress; it does not independently verify a feature or professional conclusion.</p><button type="button" id="education-export">Download completed worksheet</button> <button type="button" id="education-print">Print lesson</button></form><p>'+link(route+'worksheet.csv','Download the blank CSV worksheet')+'</p></section>'
 body+='<section aria-labelledby="common-questions"><h2 id="common-questions">Common questions</h2>'+''.join('<h3>'+H(q)+'</h3>'+ui.paragraphs(a) for q,a in g['faqs'])+'</section>'
 if g['financial']:body+=PARTNERS
 body+='<section class="guide-sources"><h2>Source material and further review</h2><p>The workflow, lab and example are original planning guidance. These primary resources provide background; manufacturer instructions and qualified property-specific review remain important where relevant.</p><ul>'+''.join('<li>'+link(SOURCES[k][1],SOURCES[k][0])+'</li>' for k in g['sources'])+'</ul></section>'
 body+='<section><h2>Continue the design work</h2><ul>'+''.join('<li>'+link(r,'Related guidance: '+r.strip('/').split('/')[-1].replace('-',' '))+'</li>' for r in g['related'])+'<li>'+link(PREFIX+LESSONS[(i+1)%len(LESSONS)]['slug']+'/',LESSONS[(i+1)%len(LESSONS)]['title'])+'</li></ul></section>'+ui.cta()+'</article>'
 p=output(route,g['title'],g['summary'],body)
 with (p.parent/'worksheet.csv').open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['Field','Property evidence','Owner and next action']);w.writerows((x,'','') for x in ['Property reference']+g['fields'])
 # Count authored prose independently of template, navigation, citations and worksheet prompts.
 authored=' '.join([g['summary']]+[text for _,text in g['sections']]+[g['example'],g['lab'][1]]+[a for _,a in g['faqs']])
 words=len(authored.split());assert words>=900,(g['slug'],words)
 MANIFEST.append(dict(route=route,title=g['title'],authored_words=words,financial_links=g['financial'],status='published',sources=[SOURCES[k][1] for k in g['sources']]))
body='<div class="guide-content"><p>Use the design manual to resolve the work behind an attractive listing: room functions, guest activities, care, measurements, installation, operating standards and clear property information. Each lesson includes an original step-by-step explanation, a worked hypothetical example, a practical lab and an editable worksheet.</p><p>For the sequence of a whole project, begin with '+link('/design-roadmap/','the twelve-stage design roadmap')+'. For a specific problem, search the lessons below or explore '+link('/resources/','the detailed planning library')+'.</p><label for="education-search">Find a design lesson</label><input id="education-search" class="library-search" type="search" placeholder="Try group meals, pet-friendly, studio or bathroom"><p id="education-search-status" role="status" aria-live="polite">'+str(len(LESSONS))+' lessons</p></div><section class="library-grid" aria-label="Design lessons">'+''.join('<article class="library-card" data-education-card><h2>'+link(PREFIX+g['slug']+'/',g['title'])+'</h2><p>'+H(g['summary'])+'</p>'+link(PREFIX+g['slug']+'/','Study the lesson and use the worksheet')+'</article>' for g in LESSONS)+'</section><div class="guide-content"><h2>Choose your learning path</h2><ul><li>'+link('/resources/planning/','Project planning and budgets')+'</li><li>'+link('/resources/layouts/','Room layouts and guest movement')+'</li><li>'+link('/resources/materials/','Materials, furniture and care')+'</li><li>'+link('/resources/comfort/','Sleep and everyday comfort')+'</li><li>'+link('/resources/lighting/','Lighting and window treatments')+'</li><li>'+link('/resources/outdoors/','Outdoor and seasonal planning')+'</li><li>'+link('/resources/maintenance/','Operating standards and replacement')+'</li><li>'+link('/resources/launch/','Purchasing, installation and launch')+'</li></ul><h2>How to use the worksheets</h2><p>Collect the actual site and product evidence before making a decision. Write down unresolved questions instead of entering guesses, assign a reviewer and keep the accepted revision with the property handover. The worksheets organize your work; they do not certify compliance, establish tax treatment or predict rental returns.</p>'+ui.cta()+'</div>'
output(PREFIX,'STR design education: the owner’s design manual','Study detailed rental design lessons with original workflows, property examples, practical labs and downloadable worksheets.',body,False)
# Stable panels preserve prior site work and make every lesson reachable.
panel='<section class="library-header"><h2>'+link(PREFIX,'Study the STR owner’s design manual')+'</h2><p>Detailed lessons, practical design labs and editable worksheets for group layouts, compact rooms, comfort, care, renovations and operating handoffs.</p><p>'+link('/design-roadmap/','Follow the whole design roadmap')+' · '+link(PREFIX,'Find an educational lesson')+'</p></section>'
for rel in ['index.html','resources/index.html','design-roadmap/index.html']:
 ui.upsert_panel(ROOT/rel,'EDUCATION_MANUAL_20261013',panel)
# Link from matching existing chapters so readers reach the specific next task.
for g in LESSONS:
 for related in g['related']:
  p=ROOT/related.lstrip('/')/'index.html'
  if p.is_file():
   block='<section class="guide-content"><h2>Apply this topic in a detailed design lesson</h2><p>'+link(PREFIX+g['slug']+'/',g['title'])+'</p><p>'+H(g['summary'])+'</p></section>'
   ui.upsert_panel(p,'EDUCATION_'+g['slug'],block)
ns=ui.NS;tree=E.parse(ROOT/'sitemap.xml');root=tree.getroot();known={r.find('{'+ns+'}loc').text:r for r in root}
for route in [PREFIX]+[g['route'] for g in MANIFEST]:
 url=BASE+route;row=known.get(url)
 if row is None:row=E.SubElement(root,'{'+ns+'}url');E.SubElement(row,'{'+ns+'}loc').text=url
 lm=row.find('{'+ns+'}lastmod')
 if lm is None:lm=E.SubElement(row,'{'+ns+'}lastmod')
 lm.text=ui.DATE
E.indent(tree);tree.write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
(ROOT/'content/education-manifest.json').write_text(json.dumps(MANIFEST,indent=2)+'\n')
print(json.dumps({'lessons':len(MANIFEST),'new_html_pages':len(MANIFEST)+1,'authored_words':sum(g['authored_words'] for g in MANIFEST),'minimum_authored_words':min(g['authored_words'] for g in MANIFEST),'maximum_authored_words':max(g['authored_words'] for g in MANIFEST),'financial_link_lessons':sum(g['financial_links'] for g in MANIFEST)}))
