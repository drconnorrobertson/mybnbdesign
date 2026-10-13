"""Publish reviewed educational owners and cover remaining canonical sitemap omissions."""
from pathlib import Path
from urllib.parse import urljoin,urlsplit
import sys,json,re,csv,html,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'))
import build_host_library as ui
from content.education_next.guides import GUIDES
from content.education_next.repairs import FAQS,CASES,COMPARISONS
ui.DATE='2026-10-13';rows=[]
PARTNERS='<section><h2>Keep the design and financial records connected</h2><p>Retain itemized invoices, room locations, product specifications, installation descriptions and completion records. Discuss the owner’s broader tax planning with '+ui.link('https://www.aetaxadvisors.com/','AE Tax Advisors')+' and property-component documentation with '+ui.link('https://www.stratumcostsegregation.com/str-cost-segregation-resources/','Stratum’s STR cost segregation resources')+'. These are related business resources recommended by MyBnBDesign with separate professional scopes. A design label or hypothetical return scenario does not determine tax treatment.</p></section>'
def para(s):return ui.paragraphs(s)
def section(h,s):return '<section><h2>'+ui.esc(h)+'</h2>'+para(s)+'</section>'
def related(links):
 body='<h2>Related design work</h2><ul>'
 for route in links:
  p=ui.target(ROOT,route);assert p.exists(),route
  text=p.read_text();m=re.search('<h1[^>]*>(.*?)</h1>',text,re.S);label=html.unescape(re.sub('<[^>]+>','',m[1])) if m else route
  body+='<li>'+ui.link(route,label)+'</li>'
 return body+'</ul>'
def worksheet(route,fields):
 name=re.sub('[^a-z0-9]+','-',route.strip('/').replace('.html','')).strip('-')+'.csv';p=ROOT/'assets/education-next-worksheets'/name;p.parent.mkdir(exist_ok=True)
 with p.open('w') as f:
  w=csv.writer(f);w.writerow(['Decision or evidence','Owner notes','Responsible party','Verification date']);w.writerows([[x,'','',''] for x in fields])
 return '<h2>Use the decision worksheet</h2><p>'+ui.link('/assets/education-next-worksheets/'+name,'Download this guide’s evidence worksheet (CSV)')+'. Complete it with the actual property information and proposals.</p><ul>'+''.join('<li>'+ui.esc(x)+'</li>' for x in fields)+'</ul>'
def write(route,title,body,kind):
 p=ui.target(ROOT,route);assert p.exists(),route;old=p.read_text();pub=re.search(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})',old)
 description=title+'. Use a practical owner method, evidence checklist and related STR design resources.'
 doc=ui.shell(title,description,route,'<main id="main" class="host-library reviewed-design"><article><p class="label">STR owner education · Reviewed October 13, 2026</p><h1>'+ui.esc(title)+'</h1>'+body+'</article></main>',[('Home','/'),('Design resources','/resources/'),(title,route)],article=True,published=pub[1] if pub else ui.DATE)
 doc=doc.replace('</head>','<link rel="stylesheet" href="/assets/reviewed-design.css"></head>');p.write_text(doc)
 rows.append(dict(route=route,title=title,kind=kind,main_words=len(html.unescape(re.sub('<[^>]+>',' ',body)).split()),reviewed=ui.DATE))
for g in GUIDES:
 body='<p>Use this guide to turn the design goal into a property-specific decision. Worked examples are hypothetical; no independent product ranking or promised booking result is asserted.</p>'
 for title,text in g['sections']:body+=section(title,text)
 body+=worksheet(g['route'],g['fields']+['Exact products and permitted care','Complete landed cost and local work','Guest-use and turnover acceptance','Final record and approved substitutes'])
 body+=section('Make the decision reviewable','Keep the measured plan, actual product or deliverable specification and approval together. A useful record names the problem, the proposed change and the test that will establish whether it works. Distinguish estimated dates and costs from confirmed commitments. If the proposed item changes, review the affected room decisions rather than approving it solely because its appearance is similar.\n\nAfter implementation, repeat the guest-use and operating checks and record what remains unresolved. A photograph is useful evidence of the arrangement, but it does not replace care information, installation instructions or a complete handoff. Review observed operating results before carrying the same specification to another property.')
 body+=related(g['related'])+PARTNERS+'<p>'+ui.link('/services.html','Review MyBnBDesign services')+' · '+ui.link('/book/','Discuss your measured property brief')+'.</p>'
 write(g['route'],g['title'],body,'educational guide')
for route,title,items in FAQS:
 body=para('Use these answers to prepare a clear rental-design decision. The scope is '+title.lower()+', with practical evidence to gather from your actual property and proposal. Prices, timelines and tax treatment are not universal across projects.')
 for q,a in items:body+=section(q,a)
 body+=worksheet(route,[q for q,a in items]+['Proposal and property evidence','Decision owner and approval date'])
 body+=related(['/resources/guides/quote-scope-comparison/','/resources/guides/scope-before-shopping/','/design-roadmap/'])+PARTNERS
 write(route,title,body,'distinct FAQ owner')
case_routes={}
for slug,title,intro,decision,test,result,links in CASES:
 route='/case-studies/'+slug+'.html';case_routes[route]=title
 body='<p><strong>Hypothetical planning example.</strong> '+ui.esc(intro)+'</p><p>Use this scenario to prepare a measured brief. Replace its hypothetical assumptions with your actual property information and test the proposed decisions before purchasing.</p>'
 body+=section('The design decision',decision)+section('Evidence to gather',test)
 body+=section('Build the measured brief','Record the rooms, intended guest group, retained inventory and the actual property constraints. Keep photographs and dimensions with the plan, including relevant doors, windows, controls and delivery access. Identify unresolved site conditions and the responsible parties before product selection. The purpose is to describe what the design must accomplish rather than to reproduce a reference image.\n\nFor each proposed change, state the guest routine it supports and the evidence that would show it works. Check the complete arrangement with furniture in use. A room can appear spacious when empty while failing the meal, work or luggage routine that guests actually need.')
 body+=section('Compare the implementation routes','Decide which work the owner can coordinate and what requires design or site support. Request the same room list from each candidate and separate design, goods, delivery, receiving, assembly, specialist work and final acceptance. Leave unanswered responsibilities visible. A lower headline fee does not settle the comparison when it leaves essential local work outside the proposal.\n\nConfirm who verifies dimensions, approves substitutions and handles delivery problems. Keep the accepted plan version with the product schedule so the installer and owner can refer to the same decision record.')
 body+=section('Accept the design through use','After the agreed work is complete, repeat the guest and turnover routines. Inspect condition, follow applicable product instructions and use qualified help for specialist installation. Record unresolved items with a named owner and completion date. Photograph the final arrangement that guests will receive and keep reference concepts clearly distinguished from actual property photographs.')
 body+=section('What a completed exercise produces',result+' This is the intended planning deliverable, not an assertion that a real property achieved it. Any later performance evaluation needs a defined metric, period and comparison method, with other operating changes recorded.')
 body+=worksheet(route,['Hypothetical assumptions replaced with real property data','Retained inventory and measured plan','Guest routine to test','Actual product and care evidence','Complete scope and cost','Acceptance result and unresolved items'])+related(links)+PARTNERS
 write(route,title,body,'hypothetical planning example')
for route,title,intro,example,check,link in COMPARISONS:
 body=para(intro)+section('Worked owner decision',example)+section('Evidence before commitment',check)
 body+=section('Compare the same finished condition','Prepare the same measured plan, retained inventory, required rooms and guest brief for each approach. Decide whether you need advice, a complete design handoff or installed and checked rooms. Keep those deliverables distinct. A shopping list and an installed rental can both be useful assignments, but they do not represent the same amount of work.\n\nRequest visible responsibility and cost for design, goods, freight, receiving, assembly, mounting, household inventory and final styling as applicable. Identify who resolves unavailable products and damaged deliveries. Compare totals after assigning excluded work to someone rather than treating missing lines as free services.')
 body+=section('Check the operating handoff','Test the installed arrangement through the actual guest routine and a cleaning reset. Keep care instructions, product variants and approved substitutes with the room inventory. A complete handoff should explain the finished condition, unresolved items and the owner’s support route. Use observations to improve the next decision instead of assuming that a service label predicts the operating outcome.')
 body+=worksheet(route,['Work the owner will perform','Deliverables purchased from each candidate','Retained and newly purchased inventory','Complete landed and execution cost','Approval and substitution process','Guest-readiness acceptance'])+related([link,'/resources/guides/quote-scope-comparison/'])+PARTNERS
 write(route,title,body,'execution comparison guide')
route='/blog/best-paint-colors-for-airbnb-bedrooms.html';title='Airbnb bedroom paint colors: test samples in the room'
body=section('Start with the retained room','Record the flooring, bed, bedding, window treatment and large furniture before selecting paint. The wall color will be viewed alongside those surfaces, not in isolation. Identify the mood you want and the tasks the bedroom must support, including reading, unpacking and finding controls after dark. A paint name or an inspiration photograph does not establish the result in a different room.')
body+=section('Use actual samples under actual light','Follow the paint supplier’s sample and application guidance and compare appropriate samples beside the retained materials. Observe daylight and the installed artificial lighting. Record which direction becomes dominant, which surfaces look different and whether the palette supports the intended room. Do not choose a whole-property color based only on a digital swatch or one unusually bright room.')
body+=section('Worked decision: retain a warm wood headboard','In a hypothetical bedroom, the owner compares two neutral directions beside a retained warm wood headboard and existing flooring. One sample creates an unwanted contrast after dark. The owner tests another direction with the actual bedding before committing to the room. These observations inform that property’s selection; they are not a universal claim that a particular color family is best for every rental.')
body+=section('Specify preparation and care separately','Ask the responsible painter or qualified party about actual surface condition, preparation and applicable product instructions. A color selection does not resolve an underlying moisture or substrate problem. Keep the paint product, finish, color identifier and application records together so later touch-ups can be assessed accurately. Follow manufacturer instructions for application, ventilation and use conditions.')
body+=section('Check the complete bedroom','After the work is complete under the applicable instructions, test the room’s night-use routine and inspect the chosen palette beside the final furnishings. Photograph the real arrangement and keep the color identifier in the room record. If another room has different retained materials or light, repeat the sample comparison rather than assuming the same result.')
body+=worksheet(route,['Retained material and bedding samples','Day/night color observations','Surface condition and responsible professional','Exact paint product and finish','Completed room check'])+related(['/blog/airbnb-bedroom-design-guide.html','/blog/scandinavian-color-palette-guide.html','/learn/rental-bedroom-nighttime-commissioning/'])+PARTNERS
write(route,title,body,'educational guide')
# The old case-study directory also implied verified results. Make its purpose explicit.
body='<p>These worked planning examples are hypothetical educational exercises. They are not verified completed client projects, revenue results or guest testimonials. Use the property routines and evidence checks to prepare your own measured brief.</p><ul>'+''.join('<li>'+ui.link(r,t)+'</li>' for r,t in case_routes.items())+'</ul>'+section('How to use an example','Replace the hypothetical assumptions with actual room dimensions, retained furniture, intended guests and operating constraints. Test the proposed decision through guest use and turnover before choosing products. Compare the same finished condition in each proposal, then keep the accepted plan and product records together.\n\nFor evidence of a completed assignment, request project-specific documentation and a clear explanation of the design team’s role. A hypothetical example should never be used as proof of past financial performance.')+related(['/design-roadmap/','/resources/guides/quote-scope-comparison/','/mybnbdesign-reviews/'])
write('/case-studies/','STR design planning examples and owner exercises',body,'planning example directory')
# Update references to the repaired examples, including nested legacy anchors, without altering other content.
labels={**case_routes,'/case-studies/':'Worked STR design planning examples'}
def rewrite_anchors(chunk,source):
 stack=[];edits=[]
 for m in re.finditer(r'</?a\b[^>]*>',chunk,re.I):
  if m[0].lower().startswith('</a'):
   if not stack:continue
   start,tag,target=stack.pop()
   if target in labels:edits.append((start,m.end(),'<a href="'+ui.esc(target)+'">'+ui.esc(labels[target])+'</a>'))
  else:
   href=re.search(r'\bhref\s*=\s*["\']([^"\']+)',m[0],re.I);q=urlsplit(urljoin(source,html.unescape(href[1]))) if href else None;target=q.path if q and q.netloc in ['www.mybnbdesign.com','mybnbdesign.com'] else ''
   stack.append((m.start(),m[0],target))
 selected=[]
 for e in sorted(edits,key=lambda x:(x[0],-x[1])):
  if not selected or e[0]>=selected[-1][1]:selected.append(e)
 for start,end,new in reversed(selected):chunk=chunk[:start]+new+chunk[end:]
 return chunk
old_manifest=ROOT/'content/education-next-manifest.json'
prior_refs=json.loads(old_manifest.read_text()).get('case_reference_files',[]) if old_manifest.exists() else []
ref_files=[]
for p in ROOT.rglob('*.html'):
 if any(part.startswith('.') or part in ('dist','node_modules') for part in p.relative_to(ROOT).parts):continue
 text=p.read_text()
 if 'case-studies/' not in text:continue
 c=re.search(r'<link[^>]*rel="canonical"[^>]*href="([^"]+)"',text);source=c[1] if c else ui.ORIGIN+'/'+p.relative_to(ROOT).as_posix()
 pieces=re.split(r'(<script\b[^>]*>[\s\S]*?</script>)',text,flags=re.I);new=''.join(s if s.lower().startswith('<script') else rewrite_anchors(s,source) for s in pieces)
 if new!=text:p.write_text(new);ref_files.append(p.relative_to(ROOT).as_posix())
# Promote only the reviewed bodies, with descriptive topic links and a truthful modification date.
for hub in ['resources/index.html','learn/index.html']:
 panel='<section class="host-library"><h2>Applied STR design guides</h2><p>Work through specific guest routines, care trials and scope decisions.</p><ul>'+''.join('<li>'+ui.link(r['route'],r['title'])+'</li>' for r in rows if r['kind']=='educational guide')+'</ul><p>'+ui.link('/faq/','Owner FAQs')+' · '+ui.link('/case-studies/','Hypothetical planning examples')+'</p></section>'
 ui.upsert_panel(ROOT/hub,'education-next-guides',panel)
ui.upsert_panel(ROOT/'faq/index.html','distinct-owner-faqs','<section class="host-library"><h2>Project-specific owner questions</h2><ul>'+''.join('<li>'+ui.link(r,t)+'</li>' for r,t,_ in FAQS)+'</ul></section>')
ui.upsert_panel(ROOT/'compare/index.html','execution-choices-next','<section class="host-library"><h2>Execution and purchasing decisions</h2><ul>'+''.join('<li>'+ui.link(r,t)+'</li>' for r,t,*_ in COMPARISONS)+'</ul></section>')
# The established main sitemap provides another discovery path for every reviewed owner.
ns=ui.NS;E.register_namespace('',ns);tree=E.parse(ROOT/'sitemap.xml');known={r.find('{*}loc').text:r for r in tree.getroot()}
for r in rows:
 u=ui.ORIGIN+r['route'];node=known.get(u)
 if node is None:node=E.SubElement(tree.getroot(),'{'+ns+'}url');E.SubElement(node,'{'+ns+'}loc').text=u;known[u]=node
 lm=node.find('{*}lastmod')
 if lm is None:lm=E.SubElement(node,'{'+ns+'}lastmod')
 lm.text=ui.DATE
E.indent(tree);tree.write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
# Update existing blog records only where the underlying body changed.
for sm in [ROOT/'sitemap-blog.xml']:
 tree=E.parse(sm);changed=False
 for node in tree.getroot():
  if node.find('{*}loc').text in {ui.ORIGIN+r['route'] for r in rows}:
   lm=node.find('{*}lastmod')
   if lm is None:lm=E.SubElement(node,'{'+ns+'}lastmod')
   lm.text=ui.DATE;changed=True
 if changed:E.indent(tree);tree.write(sm,encoding='utf-8',xml_declaration=True)
(ROOT/'content/education-next-manifest.json').write_text(json.dumps({'pages':rows,'case_reference_files':sorted(set(prior_refs+ref_files))},indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'rewritten_pages':len(rows),'educational_guides':sum(r['kind']=='educational guide' for r in rows),'worksheets':len(list((ROOT/'assets/education-next-worksheets').glob('*.csv'))),'case_reference_files':len(set(prior_refs+ref_files)),'main_words_min':min(r['main_words'] for r in rows),'main_words_max':max(r['main_words'] for r in rows)}))

# Review completion permits comprehensive canonical sitemap coverage.
import subprocess
subprocess.run([sys.executable,str(ROOT/"scripts/rebuild_canonical_sitemap.py")],check=True)
