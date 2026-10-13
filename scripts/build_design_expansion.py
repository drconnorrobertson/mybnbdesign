"""Render the design curriculum, source-backed STR ecosystem map and discovery links."""
from pathlib import Path
import sys,json,csv,re,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'))
from content.design_roadmap import CHAPTERS
import build_host_library as ui
ui.DATE='2026-10-13'
H=ui.esc
ROUTES=[]
PARTNERS='<section class="guide-sources"><h2>Coordinate design records with the tax team</h2><p>For tax strategy, speak with <a href="https://www.aetaxadvisors.com/">AE Tax Advisors</a>. For property-component evidence and a study preparation checklist, visit <a href="https://www.stratumcostsegregation.com/str-cost-segregation-resources/">Stratum Cost Segregation’s STR resources</a>. AE considers the broader tax strategy; Stratum focuses on property analysis. These are related business resources recommended by MyBnBDesign. Confirm separate engagement scope and fees. Design selections do not establish tax treatment or a promised deduction.</p></section>'
def write(route,title,desc,body,article=False):
 p=ROOT/route.lstrip('/')/'index.html';p.parent.mkdir(parents=True,exist_ok=True)
 crumbs=[('/','Home'),('/design-roadmap/','Design roadmap')]
 if route!='/design-roadmap/':crumbs.append((route,title))
 header='<header class="library-header">'+ui.breadcrumbs(crumbs)+'<p class="eyebrow">STR DESIGN EDUCATION</p><h1>'+H(title)+'</h1><p class="lead">'+H(desc)+'</p><p>Updated October 13, 2026</p></header>'
 p.write_text(ui.shell(title,desc,route,header+'<article class="guide-content">'+body+'</article>',crumbs,article=article,published='2026-10-13'))
 ROUTES.append(route)
for i,c in enumerate(CHAPTERS):
 slug,title,lead,decision,execution,example,acceptance,fields,related=c;route='/design-roadmap/'+slug+'/'
 body='<p><strong>Stage '+str(i+1)+' of 12.</strong> '+ui.link('/design-roadmap/','See the full curriculum and choose your starting stage')+'</p>'
 body+='<h2>The decision to make</h2>'+ui.paragraphs(decision)+'<h2>How to carry it out</h2>'+ui.paragraphs(execution)
 body+='<section class="guide-example"><h2>Worked planning example</h2><p><strong>Illustrative scenario; not a client case or performance result.</strong></p>'+ui.paragraphs(example)+'</section>'
 body+='<h2>Decision gate: evidence before moving on</h2>'+ui.paragraphs(acceptance)
 body+='<h2>Build the working record</h2><p>Use one record per property and decision. Replace the prompts with verified information, retain the source documents and mark anything that still requires confirmation. Assign a person and a date to open questions instead of leaving them buried in conversation.</p><div class="artifact-table-wrap"><table><caption>'+H(title)+' worksheet</caption><thead><tr><th scope="col">Field</th><th scope="col">Your property evidence</th><th scope="col">Owner / next action</th></tr></thead><tbody>'+''.join('<tr><th scope="row">'+H(f)+'</th><td>[Record verified facts or mark unresolved]</td><td>[Name and date]</td></tr>' for f in fields)+'</tbody></table></div><p>'+ui.link(route+'worksheet.csv','Download the blank CSV worksheet')+'</p>'
 body+='<h2>Use the record with your project team</h2><p>Start with the current approved revision. Send the same document to the owner, designer and local coordinator so each person can see which decisions are settled. Keep quotes and manufacturer information attached to the relevant line. When a decision changes, record what changed, why it changed and which downstream documents must be updated.</p><p>At the next review, compare the installed or contracted result with the recorded requirement. Close an item only when the required evidence exists. If the record describes a planned purchase, do not relabel it as installed inventory until receiving and site checks confirm it. If the property is already operating, schedule work around the actual calendar and communicate the affected rooms and amenities to the person responsible for listing accuracy.</p>'
 body+='<h2>Go deeper</h2><p>'+ui.link(related,'Explore the related detailed design library')+' · '+ui.link('/tools/','Use the free host planning tools')+' · '+ui.link('/compare/companies/','Compare design and furnishing providers')+'</p>'
 if i in (2,8,10):body+=PARTNERS
 body+='<h2>Continue through the roadmap</h2><ul>'
 if i:body+='<li>'+ui.link('/design-roadmap/'+CHAPTERS[i-1][0]+'/','Previous: '+CHAPTERS[i-1][1])+'</li>'
 if i+1<len(CHAPTERS):body+='<li>'+ui.link('/design-roadmap/'+CHAPTERS[i+1][0]+'/','Next: '+CHAPTERS[i+1][1])+'</li>'
 body+='</ul>'+ui.cta();write(route,title,lead,body,True)
 with (ROOT/route.lstrip('/')/'worksheet.csv').open('w',newline='') as out:
  w=csv.writer(out);w.writerow(['Field','Property evidence','Owner / next action']);w.writerows((f,'','') for f in fields)
intro='<p>Work from the guest experience to the operating property. This curriculum follows twelve decisions: brief, service scope, budget, fit, material direction, comfort, daily activities, amenities, purchasing, launch, tax records and the first operating review. Each chapter provides a worked hypothetical example, a decision gate and a downloadable worksheet.</p><h2>Choose the right starting point</h2><p>For a new rental, begin with the guest and property brief before buying. For an operating property, begin with the issue log in the final chapter and return to the earliest unresolved requirement. For a remote project, resolve measurement and receiving responsibility before committing to a design-only plan. For a renovation, preserve invoice detail and the project chronology while work is underway.</p><h2>The full design roadmap</h2><ol>'+''.join('<li><h3>'+ui.link('/design-roadmap/'+c[0]+'/',c[1])+'</h3><p>'+H(c[2])+'</p><p><strong>Decision gate:</strong> '+H(c[6])+'</p></li>' for c in CHAPTERS)+'</ol>'
intro+='<h2>Keep four records connected</h2><p>The brief defines what the property should do. The floor plan tests where the actual items fit. The purchasing register records what was approved and ordered. The installed inventory documents what guests and the operating team actually receive. Give rooms and items consistent identifiers across these records so a substitution, refund or repair can be traced without rebuilding the project history.</p><h2>Use education to prepare a better design conversation</h2><p>A worksheet does not replace a site assessment or professional installation. Its purpose is to make the next conversation more specific: the property facts, the desired result, the unresolved decision and who must verify it. Bring the records to a design consultation and ask for a proposal that identifies responsibilities, costs and the handover evidence.</p>'
intro+=PARTNERS+'<h2>Explore the wider STR market</h2><p>'+ui.link('/str-ecosystem/','Find host software, operations and marketing resources')+' · '+ui.link('/alternatives/str-design-companies/','Research 57 design and furnishing offerings')+'</p>'+ui.cta()
write('/design-roadmap/','The complete short-term rental design roadmap','A twelve-stage STR design curriculum with property briefs, budgets, layouts, materials, procurement, launch checks and tax-record worksheets.',intro)
ECOSYSTEM=[
('PriceLabs','https://www.hello.pricelabs.co/','Pricing and revenue-management software','Connect the design budget to a conservative operating model, then test pricing with actual data. A recommended price does not prove design ROI.','pricing after a rental refresh',2),
('Hostaway','https://www.hostaway.com/','Property-management and channel software','Keep the installed inventory and advertised amenities aligned when updates reach several channels.','updating amenities across booking channels',9),
('Guesty','https://www.guesty.com/','Vacation-rental management software','Plan who updates listings, tasks and property information when rooms or amenities change.','design handoff for property managers',9),
('Hospitable','https://hospitable.com/','Host automation and vacation-rental software','Use the finished room configuration to review guest messages and explain controls or sleeping arrangements accurately.','guest instructions after redesign',11),
('OwnerRez','https://www.ownerrez.com/','Vacation-rental property-management software','Maintain consistent property facts and selected photography when a renovation or furnishing replacement changes the stay.','property records after furnishing',9),
('Lodgify','https://www.lodgify.com/','Vacation-rental software and direct-booking websites','A direct-booking page needs truthful room photos, capacity and amenity information from the final installation.','design and direct-booking photography',9),
('Turno','https://turno.com/','Vacation-rental cleaning coordination','Test linen storage, reset time and product care with the turnover team before completing the design.','cleaner-friendly rental design',5),
('Breezeway','https://www.breezeway.io/','Property-care and operations platform','Convert the installation punch list and room reset standards into a clear local operating handoff.','rental design inspection checklist',9),
('StayFi','https://stayfi.com/','Vacation-rental WiFi marketing','Coordinate the guest WiFi experience with the property instructions and marketing plan, confirming privacy and platform requirements separately.','WiFi placement in rental design',7),
('Touch Stay','https://touchstay.com/','Digital guest guidebooks','Translate installed appliances, lighting controls, storage and amenity instructions into accurate guest guidance.','design handoff to guest guidebook',11),
]
body='<p>These businesses serve adjacent host needs. They are potential educational audience overlaps, not all direct design competitors and not substitutes for a furnishing contract. Official category information was reviewed October 13, 2026. The suggested content angles below are editorial opportunities; search volume, ranking difficulty and traffic are unmeasured.</p><h2>Connect the host workflow to design education</h2>'
for name,source,kind,connection,angle,stage in ECOSYSTEM:
 body+='<section><h3>'+H(name)+'</h3><p><strong>'+H(kind)+'.</strong> '+H(connection)+'</p><p>Educational angle: '+H(angle)+'. Start with '+ui.link('/design-roadmap/'+CHAPTERS[stage][0]+'/',CHAPTERS[stage][1].lower())+'.</p><p>'+ui.link(source,name+' official information')+'</p></section>'
body+='<h2>Build a useful acquisition path</h2><p>Publish the design answer to a real host problem, connect it to a relevant worksheet, then offer a design consultation for visitors who need implementation. Do not imply software-vendor endorsement or a commercial partnership from inclusion here. A reader researching cleaning or guest messaging may need design help, but that does not establish demand for every keyword combination.</p><p>'+ui.link('/design-roadmap/','Follow the full design curriculum')+' · '+ui.link('/alternatives/str-design-companies/','Compare researched design services')+'</p>'+PARTNERS
write('/str-ecosystem/','The STR ecosystem: connect host operations with design','Research adjacent STR software, cleaning, guest-experience and marketing audiences with practical links to rental design education.',body)
# Stable discovery blocks survive repeated runs.
block='<section class="library-header"><h2>'+ui.link('/design-roadmap/','Follow the complete STR design roadmap')+'</h2><p>Twelve stages from guest brief to operating review, with examples and downloadable property worksheets.</p><p>'+ui.link('/alternatives/str-design-companies/','Research 57 design and furnishing providers')+' · '+ui.link('/str-ecosystem/','Explore the STR ecosystem')+'</p></section>'
for rel in ['index.html','resources/index.html','services.html','compare/index.html','alternatives/index.html']:
 p=ROOT/rel;ui.upsert_panel(p,'DESIGN_EXPANSION_20261013',block)
ns=ui.NS;tree=E.parse(ROOT/'sitemap.xml');root=tree.getroot();known={r.find('{'+ns+'}loc').text:r for r in root}
for route in ROUTES:
 url=ui.ORIGIN+route;row=known.get(url)
 if row is None:row=E.SubElement(root,'{'+ns+'}url');E.SubElement(row,'{'+ns+'}loc').text=url
 lm=row.find('{'+ns+'}lastmod')
 if lm is None:lm=E.SubElement(row,'{'+ns+'}lastmod')
 lm.text=ui.DATE
E.indent(tree);tree.write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
(ROOT/'content/design-expansion-routes.json').write_text(json.dumps(ROUTES,indent=2)+'\n')
print('Rendered',len(ROUTES),'roadmap and ecosystem routes, with 12 CSV worksheets')
