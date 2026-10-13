"""Build the component lifecycle reference with explicit shared instructional protocols.
128 component records x 19 distinct decision objectives, plus 14 category hubs and one index.
"""
from pathlib import Path
import sys,json,csv,re,hashlib,xml.etree.ElementTree as E
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'))
from content.design_reference.topics import TOPICS,CATEGORIES
from content.design_reference.stages import STAGES
from content.design_reference.cases import CASES
import build_host_library as ui
ui.DATE='2026-10-13';BASE=ui.ORIGIN;H=ui.esc;PREFIX='/learn/reference/'
LABELS={'function':'Intended function','measure':'Site and fit evidence','selection':'Selection question','reset':'Local reset and care','failure':'Failure mode to investigate','test':'Ordinary-use check','records':'Source records to preserve'}
SOURCES={'warranty':('FTC: Warranties','https://consumer.ftc.gov/articles/warranties'),'shopping':('FTC: Online shopping','https://consumer.ftc.gov/articles/online-shopping'),'recalls':('CPSC: Recalls and product safety warnings','https://www.cpsc.gov/Recalls'),'light':('FTC: Shopping for light bulbs','https://consumer.ftc.gov/articles/shopping-light-bulbs'),'moisture':('EPA: Mold and moisture','https://www.epa.gov/mold/brief-guide-mold-moisture-and-your-home'),'access':('U.S. Access Board: Accessible routes','https://www.access-board.gov/ada/guides/chapter-4-accessible-routes/'),'airbnb':('Airbnb: Essential amenities','https://www.airbnb.com/help/article/2343')}
def link(u,t):return ui.link(u,t)
def route(t,s):return PREFIX+t['category']+'/'+t['slug']+'/'+s['slug']+'/'
def hub(t):return PREFIX+t['category']+'/'
def document(path,title,desc,body,crumbs,article=True):
 head='<header class="library-header">'+ui.breadcrumbs(crumbs)+'<p class="eyebrow">STR DESIGN REFERENCE · COMPONENT WORKBOOK</p><h1>'+H(title)+'</h1><p class="lead">'+H(desc)+'</p><p>Published October 13, 2026 · MyBnBDesign</p></header>'
 out=ui.shell(title,desc,path,head+body,crumbs,article=article,published=ui.DATE)
 return out.replace('</head>','<link rel="stylesheet" href="/assets/design-reference.css"><script defer src="/assets/design-reference.js"></script></head>')
def write(path,text):
 p=ROOT/path.lstrip('/')/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);return p
class Words(HTMLParser):
 def __init__(self):super().__init__();self.depth=0;self.count=0
 def handle_starttag(self,tag,attrs):
  if tag=='article':self.depth+=1
 def handle_endtag(self,tag):
  if tag=='article':self.depth=max(0,self.depth-1)
 def handle_data(self,data):
  if self.depth:self.count+=len(data.split())
def sources(t,s):
 keys=['warranty']
 if s['slug'] in ('landed-cost-budget','quote-scope-review','receiving-and-condition-check'):keys+=['shopping']
 if t['category'] in ('lighting','windows'):keys+=['light']
 if t['category'] in ('surfaces','outdoors','bathroom'):keys+=['moisture']
 if s['slug'] in ('measurement-survey','guest-use-commissioning'):keys+=['access']
 if s['slug'] in ('photo-and-listing-accuracy','design-brief','operating-review'):keys+=['airbnb']
 if t['category'] not in ('identity','operations'):keys+=['recalls']
 return keys
FINANCIAL_CATEGORIES={'arrival','sleep','seating','dining','kitchen','bathroom','lighting','windows','storage','surfaces','outdoors','amenities'}
MANIFEST=[]
for t in TOPICS:
 for i,s in enumerate(STAGES):
  path=route(t,s);title=t['name']+' for STRs: '+s['title'].lower();desc=s['question']+' A practical '+t['name'].lower()+' workbook with component evidence, a worked exercise and an editable decision record.'
  crumbs=[('/','Home'),('/learn/','Education'),(PREFIX,'Design reference'),(hub(t),CATEGORIES[t['category']]['title']),(path,s['title'])]
  body='<article class="guide-content reference-guide"><p class="reference-method"><strong>How this reference works:</strong> This workbook applies a shared '+H(s['title'].lower())+' protocol to the '+H(t['name'].lower())+' evidence below. Component notes, exercises and fields help you use your property facts; this is not an independently tested product review.</p>'
  body+='<nav class="reference-toc" aria-label="Workbook contents"><ul><li>'+link('#component-evidence','Component evidence')+'</li><li>'+link('#decision-protocol','Decision protocol')+'</li><li>'+link('#worked-exercise','Worked exercise')+'</li><li>'+link('#decision-record','Editable worksheet')+'</li></ul></nav>'
  body+='<section id="component-evidence"><h2>The '+H(t['name'].lower())+' evidence card</h2><p>Begin with the actual element and the property task. The notes below identify what to investigate; they do not supply universal dimensions, care permissions, lifespan or product ratings. Exact instructions and qualified review control where those requirements apply.</p><dl class="reference-evidence">'+''.join('<dt>'+LABELS[k]+'</dt><dd>'+H(t[k])+'</dd>' for k in LABELS)+'</dl></section>'
  body+='<section id="decision-protocol"><h2>'+H(s['question'])+'</h2>'
  for heading,text in s['sections']:body+='<h3>'+H(heading)+'</h3>'+ui.paragraphs(text)
  body+='</section><section><h2>Apply the protocol to this element</h2>'
  wrappers={
   'function':('Turn the function into an acceptance condition','Write what must be observable at the actual property. Distinguish the intended activity from appearance or a marketing label. Connect the required result to a room, user task and evidence source, and identify who can approve the decision. If the result is unclear, revise the brief before allowing the next purchase or instruction to depend on it.'),
   'measure':('Verify the controlling site relationship','Use an actual dated measurement or relevant provider document, and record which configuration was reviewed. A photograph can explain context without proving a fit-sensitive fact. Keep approximations labeled and assign the remaining verification. If the property or element changes, review whether the earlier evidence still applies before repeating the decision.'),
   'selection':('Ask for the exact supporting information','Use the installed or proposed identifier, revision and written scope. Record which requirement the provider evidence supports and which question remains open. Similar appearance is not compatibility, and a general product or service label does not close the task. Preserve the original source so another reviewer can follow the choice without relying on an unsupported summary.'),
   'reset':('Check the local operating process','Ask the actual local team to walk the approved sequence. Include retrieval, access, ordinary use, care and return where relevant. Follow exact instructions and route specialist questions appropriately. Record observations and limitations rather than claiming that a brief trial establishes universal performance, a fixed labor saving or a guaranteed replacement interval.'),
   'failure':('Keep the observed issue separate from its cause','Use the note as a prompt to investigate, not a diagnosis that must be true here. Record the actual condition, identifiers and context. Assign the review to the provider or qualified professional able to assess it. Keep a cosmetic preference distinct from a defect, and define the evidence required to close the accepted remedy.'),
   'test':('Choose a limited ordinary-use check','Prepare the accepted configuration and record the relevant conditions. Use product instructions and appropriate professional review instead of inventing a technical challenge. Explain what the observation supports and what it cannot establish. If the setup changes later, repeat the affected check rather than extending the first result to a different product or arrangement.'),
   'records':('Make the evidence traceable','Connect the current element, property, room and revision to original documents. Retain approvals, changes and unresolved questions beside the summary. Identify the receiving person and the version they should use. A complete-looking form does not close a missing fact; assign the next evidence or professional review instead of manufacturing an answer.')}
  for key in s['focus']:
   heading,explanation=wrappers[key];body+='<h3>'+heading+'</h3><p><strong>For '+H(t['name'].lower())+':</strong> '+H(t[key])+'</p><p>'+H(explanation)+'</p>'
  body+='</section><section id="worked-exercise" class="guide-example"><h2>Worked planning exercise</h2><p><strong>Hypothetical workflow; not a client case or outcome.</strong></p>'+ui.paragraphs(CASES[s['slug']].format(**dict(t,name=t['name'].lower())))+'</section>'
  body+='<section><h2>Run the property lab</h2>'+ui.paragraphs(s['lab'])+'<p>Use the exact '+H(t['name'].lower())+' record when carrying out this lab. Record the condition before the decision and the accepted evidence afterward. Keep a missing source or uncertain answer visible to the approver. The lab organizes an ordinary project task and does not replace product instructions, a relevant professional assessment or the owner’s separate operating responsibilities.</p></section>'
  body+='<section id="decision-record"><h2>Your '+H(t['name'].lower())+' decision record</h2><p>Replace prompts with verified property information. Keep source documents with the downloaded record. Entries remain in this page until reload, are not sent to MyBnBDesign and are exported only when you choose to download them. Avoid putting private credentials in the worksheet. A checked action records progress, not independent verification.</p><form data-reference-form><fieldset><legend>'+H(s['title'])+' evidence</legend><label>Property and room reference<input type="text" name="property" autocomplete="off"></label>'+''.join('<label>'+H(f)+'<textarea name="field-'+str(j)+'" rows="2"></textarea></label>' for j,f in enumerate(s['fields']))+'</fieldset><fieldset><legend>Decision review</legend><label class="reference-check"><input type="checkbox" name="evidence">The actual source and current element revision are recorded.</label><label class="reference-check"><input type="checkbox" name="questions">Unresolved questions have a named verifier or professional reviewer.</label><label class="reference-check"><input type="checkbox" name="accepted">The accepted decision or remedy has supporting evidence.</label><label class="reference-check"><input type="checkbox" name="updates">Affected inventory, instructions and financial records are updated where relevant.</label></fieldset><p id="reference-progress" role="status" aria-live="polite">0 of 4 review actions checked.</p><button type="button" id="reference-export">Download completed decision record</button> <button type="button" id="reference-print">Print workbook</button></form><p>'+link(path+'worksheet.csv','Download a blank CSV worksheet')+'</p></section>'
  if s['slug']=='landed-cost-budget':
   body+='<section><h2>Entered-cost worksheet</h2><p>This totals only your entries in one currency. Blank values count as zero for arithmetic but remain unquoted scope questions. Enter actual quoted charges and do not add tax or delivery again if already included. No market price, tax rate or revenue return is assumed.</p><fieldset id="reference-costs"><legend>Actual quoted or clearly labeled assumed amounts</legend><label>Quantity<input id="rc-quantity" type="number" min="0" step="1" value="0"></label>'+''.join('<label>'+label+'<input id="rc-'+key+'" type="number" min="0" step="0.01" value="0"></label>' for key,label in [('unit','Unit cost'),('tax','Applicable tax amount'),('shipping','Shipping'),('receiving','Receiving and storage'),('installation','Installation or implementation'),('other','Other quoted charges'),('credits','Documented credits')])+'<p id="reference-cost-result" role="status" aria-live="polite">Entered total: 0.00</p></fieldset></section>'
  body+='<section><h2>Common questions for this decision</h2>'+''.join('<h3>'+H(q)+'</h3>'+ui.paragraphs(a) for q,a in s['faqs'])+'</section>'
  financial=s['financial'] and t['category'] in FINANCIAL_CATEGORIES
  if financial:
   body+='<section class="guide-sources"><h2>Coordinate the property and tax records</h2><p>For the broader tax strategy discussion, use '+link('https://www.aetaxadvisors.com/','AE Tax Advisors')+'. For component evidence and study preparation, see '+link('https://www.stratumcostsegregation.com/str-cost-segregation-resources/','Stratum’s STR cost segregation resources')+'. These are related business resources recommended by MyBnBDesign. Keep the actual '+H(t['name'].lower())+' purchase, work and replacement facts traceable; the preparer and relevant study provider determine scope and treatment. This workbook does not establish eligibility, classifications, deduction amounts or guaranteed savings.</p></section>'
  keys=sources(t,s)
  body+='<section class="guide-sources"><h2>Primary background and exact product information</h2><p>The protocol and exercises are planning guidance. The resources below provide background, not a product-specific approval. Consult the current instructions for the exact installed element and qualified property review where applicable.</p><ul>'+''.join('<li>'+link(SOURCES[k][1],SOURCES[k][0])+'</li>' for k in keys)+'</ul></section>'
  body+='<section><h2>Keep the decision connected to the property</h2><p>File the accepted record with the current inventory and the original supporting documents. Give the next responsible person the result, open questions and version that applies. If a later change affects fit, care, availability or ordinary use, reopen the relevant checks instead of assuming the first approval remains valid. Review the actual property evidence before selecting another product or making a broader claim.</p></section>'
  body+='<nav class="reference-course" aria-label="Element learning sequence"><h2>Continue the '+H(t['name'].lower())+' learning sequence</h2><ol>'+''.join('<li>'+('<strong aria-current="page">'+H(x['title'])+'</strong>' if x['slug']==s['slug'] else link(route(t,x),x['title']))+'</li>' for x in STAGES)+'</ol><p>'+link(hub(t)+'#'+t['slug'],'All '+CATEGORIES[t['category']]['title'].lower()+' elements')+' · '+link(PREFIX,'The complete design reference')+' · '+link('/learn/','Authored design lessons')+' · '+link('/design-roadmap/','Whole-project roadmap')+'</p></nav>'+ui.cta()+'</article>'
  parser=Words();parser.feed(body);assert parser.count>=1000,(t['slug'],s['slug'],parser.count)
  p=write(path,document(path,title,desc,body,crumbs))
  with (p.parent/'worksheet.csv').open('w',newline='') as f:
   w=csv.writer(f);w.writerow(['Element','Decision','Field','Property evidence','Owner and next action']);w.writerows((t['name'],s['title'],field,'','') for field in ['Property and room reference']+s['fields'])
  MANIFEST.append(dict(route=path,category=t['category'],element=t['name'],element_slug=t['slug'],decision=s['slug'],title=title,main_words=parser.count,financial_links=financial,body_sha256=hashlib.sha256(body.encode()).hexdigest()))
# Each category is a complete course index; element anchors avoid extra near-duplicate hub URLs.
HUBS=[]
for key,c in CATEGORIES.items():
 path=PREFIX+key+'/';items=[t for t in TOPICS if t['category']==key]
 body='<div class="guide-content"><p>Choose an element, then the unresolved decision. Each element uses the same nineteen-stage lifecycle so the task and supporting records remain clear. Component-specific evidence changes the application; the shared protocols are identified on each workbook.</p><label for="reference-search">Find an element or decision</label><input id="reference-search" class="library-search" type="search" placeholder="Search this category"><p id="reference-search-status" role="status" aria-live="polite">'+str(len(items))+' elements</p></div><section class="reference-elements">'
 for t in items:
  body+='<section class="guide-content reference-element" data-reference-element id="'+t['slug']+'"><h2>'+H(t['name'])+'</h2><p>'+H(t['function'])+'</p><p><strong>Evidence to begin with:</strong> '+H(t['measure'])+'</p><ol>'+''.join('<li>'+link(route(t,s),s['title'])+'</li>' for s in STAGES)+'</ol></section>'
 body+='</section><div class="guide-content"><h2>Use the reference with the project roadmap</h2><p>Begin with the earliest unresolved decision for the element. Keep the actual site, product and service evidence together and assign open questions to a person who can answer them. The workbooks organize an owner’s process and are not universal product specifications or professional certifications.</p><p>'+link(PREFIX,'All reference categories')+' · '+link('/learn/','Detailed authored design lessons')+' · '+link('/design-roadmap/','The whole-property design roadmap')+'</p></div>'
 write(path,document(path,c['title']+': STR design workbooks','Study '+str(len(items))+' design elements across nineteen practical decisions, with specific evidence cards and editable property records.',body,[('/','Home'),('/learn/','Education'),(PREFIX,'Design reference'),(path,c['title'])],False));HUBS.append(path)
path=PREFIX;body='<div class="guide-content"><p>The STR design reference covers 128 elements in fourteen areas, from arrival to long-term operation. Each element has nineteen distinct decision workbooks: brief, survey, specification, trial, cost, quote scope, receiving, installation, commissioning, reset, care, support, faults, substitutions, refreshes, photography, provider terms, financial records and operating review.</p><p><strong>Editorial method:</strong> These are structured instructional workbooks. They combine component-specific evidence with openly shared lifecycle protocols and original hypothetical exercises. They are not 2,432 independent field studies, product tests or search-demand findings. Use actual property facts, exact product instructions and appropriate professional review.</p><p>For narrative lessons and practical design labs, visit '+link('/learn/','the owner’s design manual')+'. For project order, follow '+link('/design-roadmap/','the twelve-stage roadmap')+'.</p></div><section class="library-grid">'
for key,c in CATEGORIES.items():
 n=sum(t['category']==key for t in TOPICS);body+='<article class="library-card"><h2>'+link(PREFIX+key+'/',c['title'])+'</h2><p>'+str(n)+' elements · '+str(n*19)+' decision workbooks</p><p>'+H(', '.join(t['name'] for t in TOPICS if t['category']==key))+'</p></article>'
body+='</section><div class="guide-content"><h2>Work from evidence to a usable decision</h2><p>Find the relevant element and choose the decision you need to resolve. Use its evidence card to identify actual site facts, product or service requirements, an ordinary-use test and source records. Complete the worksheet with verified information, leave uncertainty visible and download the record before leaving the page. Then continue to the next lifecycle decision.</p><p>The workbooks do not predict revenue, certify compliance or determine tax treatment. Relevant financial-record discussions link to AE Tax Advisors and Stratum, while professional conclusions remain with the actual advisers and providers.</p>'+ui.cta()+'</div>'
write(path,document(path,'The STR design reference: 128 elements and 2,432 decision workbooks','A complete component lifecycle index for STR owners: planning, fit, selection, purchasing, installation, care, replacement and records.',body,[('/','Home'),('/learn/','Education'),(PREFIX,'Design reference')],False));HUBS.append(path)
# Stable discovery from the existing public owners.
panel='<section class="library-header"><h2>'+link(PREFIX,'Explore the STR design reference')+'</h2><p>128 design elements across fourteen areas, with practical lifecycle workbooks and editable property records.</p><p>'+link('/learn/','Read the authored design lessons')+' · '+link('/design-roadmap/','Follow the whole-project roadmap')+'</p></section>'
for rel in ['index.html','resources/index.html','learn/index.html','design-roadmap/index.html']:
 ui.upsert_panel(ROOT/rel,'DESIGN_REFERENCE_5000',panel)
# Regenerate a dedicated sitemap for this library without promoting unrelated legacy pages.
ns=ui.NS;E.register_namespace('',ns);root=E.Element('{'+ns+'}urlset')
for r in sorted(HUBS+[m['route'] for m in MANIFEST]):
 row=E.SubElement(root,'{'+ns+'}url');E.SubElement(row,'{'+ns+'}loc').text=BASE+r;E.SubElement(row,'{'+ns+'}lastmod').text=ui.DATE
E.indent(root);(ROOT/'sitemap-design-reference.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n'+E.tostring(root,encoding='unicode')+'\n')
robots=ROOT/'robots.txt';text=robots.read_text();line='Sitemap: '+BASE+'/sitemap-design-reference.xml'
text='\n'.join(x for x in text.splitlines() if x!=line)+'\n'
text=text.replace('Sitemap: '+BASE+'/sitemap-blog.xml','Sitemap: '+BASE+'/sitemap-blog.xml'+'\n'+line)
robots.write_text(text)
(ROOT/'content/design-reference-manifest.json').write_text(json.dumps({'editorial_method':'Component-specific records plus shared decision protocols; not independent product tests','elements':len(TOPICS),'decisions':len(STAGES),'category_hubs':14,'collection_hubs':1,'routes':MANIFEST,'hubs':HUBS},indent=2)+'\n')
print(json.dumps({'workbooks':len(MANIFEST),'hubs':len(HUBS),'total_new_html':len(MANIFEST)+len(HUBS),'min_main_words':min(m['main_words'] for m in MANIFEST),'max_main_words':max(m['main_words'] for m in MANIFEST),'financial_link_workbooks':sum(m['financial_links'] for m in MANIFEST)}))
assert len(MANIFEST)==2432 and len(HUBS)==15
assert len({m['route'] for m in MANIFEST})==2432
assert len({m['body_sha256'] for m in MANIFEST})==2432
