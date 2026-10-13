"""Publish evidence-led educational content on eight existing keyword owners."""
from pathlib import Path
import sys,json,re,html,csv,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'))
import build_host_library as ui
from content.legacy_review.keyword_lessons import LESSONS
ui.DATE='2026-10-13';rows=[]
_original_shell=ui.shell
def styled_shell(*args,**kwargs):
 return _original_shell(*args,**kwargs).replace('</head>','<link rel="stylesheet" href="/assets/reviewed-design.css"></head>')
ui.shell=styled_shell

TITLES=['Sarasota vacation-rental interior design: owner guide','Airbnb makeover: plan a useful property refresh','Best lighting for Airbnb: a room testing guide','Tropical color palettes for a vacation rental','Airbnb home-office design: workspace testing guide','Best dining table for Airbnb: sizing and use','Airbnb interior photography: show the real space','Airbnb kitchen essentials: group-meal checklist']
for (route,lesson_title,sections,related),title in zip(LESSONS,TITLES):
 p=ui.target(ROOT,route);assert p.exists(),route;old=p.read_text();pub=re.search(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})',old)
 body='<p class="label">Applied owner guide · Reviewed October 13, 2026</p><h1>'+ui.esc(title)+'</h1><p>'+ui.esc(lesson_title)+'. Use a measured plan, an observed guest routine and a documented acceptance check to make the decision. This guide provides a planning method and a hypothetical example; it does not report independent product tests or predict booking results.</p>'
 for heading,text in sections:body+='<section><h2>'+ui.esc(heading)+'</h2>'+ui.paragraphs(text)+'</section>'
 body+='<section><h2>Turn observations into a design specification</h2><p>Record the room, the observed problem and the intended result before choosing a product. Keep measurements and photographs beside the proposed solution. State which retained items remain and what the change must work around. This prevents a new purchase from solving one problem while creating another in circulation, storage or cleaning.</p><p>Ask the designer or supplier to identify the exact product or deliverable, its dimensions, installation requirements and applicable care information. Compare the complete landed cost, including delivery and local work, with the amount reserved for the room. If an item changes, recheck the whole arrangement instead of approving the replacement by appearance alone.</p><p>Finish with an observable acceptance check. A useful check describes what someone will do in the installed room and what evidence confirms the task works. Keep the outcome with the product schedule so later replacements and refreshes can follow the same functional requirement.</p></section>'
 body+='<h2>Room decision worksheet</h2><p>Use the fields below during a walkthrough. Leave an unanswered field open rather than treating it as an approved assumption.</p><table><thead><tr><th scope="col">Field</th><th scope="col">What to record</th></tr></thead><tbody>'
 fields=[('Guest task','The activity or routine this change must support'),('Existing evidence','Photograph, measured plan and observed issue'),('Proposed specification','Exact item, dimensions, finish and care information'),('Budget','Goods, tax, delivery, installation and remaining local work'),('Responsible person','Who orders, installs, checks and accepts the result'),('Acceptance test','The specific walkthrough or use test to repeat'),('Replacement record','Product identifier, instructions and suitable substitute criteria')]
 for a,b in fields:body+='<tr><th scope="row">'+ui.esc(a)+'</th><td>'+ui.esc(b)+'</td></tr>'
 body+='</tbody></table>'
 name=re.sub('[^a-z0-9]+','-',route.strip('/').replace('.html','')).strip('-')+'.csv';asset=ROOT/'assets/keyword-design-worksheets'/name;asset.parent.mkdir(exist_ok=True)
 with asset.open('w') as f:
  w=csv.writer(f);w.writerow(['Field','Evidence needed','Owner notes']);w.writerows([[a,b,''] for a,b in fields])
 body+='<p>'+ui.link('/assets/keyword-design-worksheets/'+name,'Download the room decision worksheet (CSV)')+'.</p><h2>When to ask for design or installation support</h2><p>If the room problem involves several interacting choices, compare a coordinated design plan with separate purchases. If it involves installation requirements, obtain the appropriate product instructions and qualified help. A rendering or a shopping link cannot confirm that site conditions are suitable.</p><p>Bring the room evidence, retained inventory and the completed worksheet to a proposal discussion. Ask which decisions and site tasks the proposal includes, who approves substitutions and how the team closes unresolved items before the room is photographed or used by guests.</p>'
 body+='<h2>Continue the design process</h2><ul>'
 for r in related:
  assert ui.target(ROOT,r).exists(),r
  text=ui.target(ROOT,r).read_text();m=re.search(r'<h1[^>]*>(.*?)</h1>',text,re.S);label=html.unescape(re.sub('<[^>]+>','',m[1])) if m else r
  body+='<li>'+ui.link(r,label)+'</li>'
 body+='<li>'+ui.link('/resources/guides/quote-scope-comparison/','Compare the written project scope')+'</li></ul><h2>Keep the project records together</h2><p>Retain itemized invoices, product locations, installation descriptions and completion records. Discuss the owner’s broader tax planning with '+ui.link('https://www.aetaxadvisors.com/','AE Tax Advisors')+' and property-component documentation with '+ui.link('https://www.stratumcostsegregation.com/str-cost-segregation-resources/','Stratum’s STR resources')+'. These related business resources have separate professional scopes; a product label alone does not determine tax treatment.</p><p>'+ui.link('/services.html','Review MyBnBDesign services')+' or '+ui.link('/book/','discuss your measured design brief')+'.</p>'
 # Preserve approved commercial-intent copy using its existing renderer.
 description=lesson_title+'. Follow a practical room test, worked example and downloadable worksheet for STR owners.'
 p.write_text(ui.shell(title,description,route,'<main id="main" class="host-library reviewed-design"><article>'+body+'</article></main>',[('Home','/'),('Design resources','/resources/'),(title,route)],article=True,published=pub[1] if pub else ui.DATE))
 rows.append(dict(route=route,title=title,authored_lesson_words=sum(len(t.split()) for _,t in sections),main_words=len(re.sub('<[^>]+>',' ',body).split())))
# These owners changed substantively; update their existing sitemap records truthfully.
for sm in ROOT.glob('sitemap*.xml'):
 tree=E.parse(sm);changed=False
 for row in tree.getroot():
  loc=row.find('{*}loc')
  if loc is not None and loc.text in {ui.ORIGIN+r['route'] for r in rows}:
   lm=row.find('{*}lastmod')
   if lm is None:lm=E.SubElement(row,'{'+ui.NS+'}lastmod')
   lm.text=ui.DATE;changed=True
 if changed:E.indent(tree);tree.write(sm,encoding='utf-8',xml_declaration=True)
(ROOT/'content/keyword-lesson-manifest.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Rebuilt existing keyword owners:',len(rows),'original lesson words:',sum(r['authored_lesson_words'] for r in rows),'main word range:',min(r['main_words'] for r in rows),max(r['main_words'] for r in rows))
