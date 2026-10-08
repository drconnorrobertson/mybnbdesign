"""Render a decision-led tools hub and preserve its entry points on rebuild."""
from pathlib import Path
import sys, re, json, html, xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import build_host_library as lib
DATE='2026-10-07'
TOOLS=[
('design-budget-calculator','Airbnb furnishing budget calculator','Estimate a category budget, then replace allowances with delivered and installed vendor quotes.','landed-furnishing-cost','Add freight, tax, assembly and receiving to the furniture price. Keep repair allowances and launch reserves separate so a shopping budget does not become your entire opening budget.'),
('furniture-shopping-list','Vacation rental furniture shopping list','Create a room inventory and check quantities against your actual guest capacity.','guest-capacity-furnishing-matrix','Count usable sleeping places, dining seats, bedside surfaces and towel sets against the same guest capacity. A product list cannot establish fit: measure the room, doorways and delivery route before ordering.'),
('amenity-checklist','Airbnb amenity planning checklist','Prioritize amenities by guest needs, space, operating effort and maintenance ownership.','guest-feedback-design-triage','Separate essential guest tasks from optional amenities. Assign a reset owner, spare supply and maintenance record to every item. Check local requirements and exact product instructions before installation.'),
('color-palette-guide','Vacation rental color palette planner','Compare palette directions with daylight, retained finishes and real material samples.','dining-finish-sample-test','Test samples in the actual room at morning and evening light levels. Check them beside flooring, cabinets and retained furniture. A palette suggestion is a starting direction rather than a specification for purchasing paint or fabric.'),
('roi-calculator','Design investment scenario calculator','Test a user-entered nightly-rate change while holding occupancy constant.','furniture-cost-per-use','Treat the assumed rate change as a hypothesis. Gross revenue uplift does not equal profit. Management fees, turnover costs, replacements and any nights lost during the project can reduce the amount available to recover the investment.')]

def panel(path, marker, body):
 s=path.read_text();block='<!-- '+marker+':start -->'+body+'<!-- '+marker+':end -->'
 pat=r'<!-- '+re.escape(marker)+r':start -->.*?<!-- '+re.escape(marker)+r':end -->'
 s=re.sub(pat,'',s,flags=re.S)
 if '</main>' in s:s=s.replace('</main>',block+'</main>',1)
 elif '<footer' in s:s=s.replace('<footer',block+'<footer',1)
 else:s=s.replace('</body>',block+'</body>',1)
 path.write_text(s)

def build(root=ROOT):
 previous_date=lib.DATE
 lib.DATE=DATE
 title='Airbnb Design Tools & Furnishing Calculators'
 desc='Plan your Airbnb furnishing budget, room inventory, amenities, colors and design investment scenarios with free tools and practical checklists.'
 body=lib.header(title,desc,[('/','Home'),('/tools/','Design tools')])
 body+='<div class="guide-content"><p>Work from the property you actually have: measurements, retained items, intended guest capacity, delivery access and operating responsibilities. These free tools organize a design brief; their outputs are planning assumptions rather than a vendor quote or a booking forecast.</p><h2>Choose the tool for your next decision</h2><p>Begin with the furnishing budget and room inventory. Once the essentials fit, choose amenities and test colors. Use the investment scenario only when you have a documented reason for the nightly-rate assumption.</p></div><div class="library-grid">'
 for slug,name,intro,guide,detail in TOOLS:
  body+='<article class="library-card"><h2>'+lib.link('/tools/'+slug+'/',name)+'</h2><p>'+intro+'</p><p>'+detail+'</p><p>'+lib.link('/resources/guides/'+guide+'/','Use the supporting planning worksheet')+'</p></article>'
 body+='</div><div class="guide-content"><h2>Turn estimates into a purchase-ready brief</h2><ol><li>Record your room dimensions, guest count and retained furniture.</li><li>Use the budget tool to establish allowances for each category.</li><li>Request product-level quotes including freight, tax, receiving and installation.</li><li>Resolve substitutions and timing before approving purchases.</li><li>Document care, warranties, spare stock and a reset photo for the operating team.</li></ol><h2>Common planning questions</h2><h3>How much should I budget to furnish an Airbnb?</h3><p>The answer depends on room count, items you retain, service scope, product specifications and delivered costs. Start with the calculator, then use actual quotes. A per-bedroom allowance cannot account for your outdoor scope, freight access or repairs.</p><h3>Does a design upgrade guarantee more bookings?</h3><p>No. Price, location, availability, operating performance and competing listings also affect bookings. Model a no-uplift scenario and separate gross revenue from additional operating profit before approving an upgrade.</p><h3>Can I use these tools before hiring a designer?</h3><p>Yes. Bring the draft inventory, measured floor plan and priorities to the consultation. Confirm who will measure, order, receive, install and close the punch list in the written proposal.</p><p>'+lib.link('/faq-pricing.html','Design pricing questions')+' · '+lib.link('/faq-furniture.html','Furniture selection questions')+' · '+lib.link('/faq-process.html','Design process questions')+'</p>'+lib.cta()+'</div>'
 schema={'@context':'https://schema.org','@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'name':x[1],'url':lib.ORIGIN+'/tools/'+x[0]+'/'} for i,x in enumerate(TOOLS)]}
 (root/'tools/index.html').write_text(lib.shell(title,desc,'/tools/',body,[('/','Home'),('/tools/','Design tools')],extra_schema=schema))
 entry='<section class="library-resource-panel"><h2>Plan your Airbnb furnishing budget and inventory</h2><p>Use '+lib.link('/tools/','free Airbnb design tools and furnishing calculators')+' to organize your room inventory, budget, amenities and design assumptions before requesting quotes.</p></section>'
 for rel in ['index.html','resources/index.html','services.html']:panel(root/rel,'DESIGN_TOOLS_DISCOVERY',entry)
 for slug,name,intro,guide,detail in TOOLS:
  section='<section class="container" style="padding:32px 24px;max-width:900px;margin:auto"><h2>Use this result in your design brief</h2><p>'+detail+'</p><p>'+lib.link('/resources/guides/'+guide+'/','Open the supporting worksheet')+' · '+lib.link('/tools/','Compare all design planning tools')+' · '+lib.link('/book/','Discuss your measured brief')+'</p></section>'
  panel(root/'tools'/slug/'index.html','TOOL_PLANNING_CONTEXT',section)
 tree=E.parse(root/'sitemap.xml');ns='{http://www.sitemaps.org/schemas/sitemap/0.9}';doc=tree.getroot();rows={x.find(ns+'loc').text:x for x in doc}
 for rel in ['/','/resources/','/services.html','/tools/']+['/tools/'+x[0]+'/' for x in TOOLS]:
  u=lib.ORIGIN+rel;row=rows.get(u)
  if row is None:row=E.SubElement(doc,ns+'url');E.SubElement(row,ns+'loc').text=u
  lm=row.find(ns+'lastmod')
  if lm is None:lm=E.SubElement(row,ns+'lastmod')
  lm.text=DATE
 E.indent(tree);tree.write(root/'sitemap.xml',encoding='utf-8',xml_declaration=True)
 lib.DATE=previous_date
 print('Tools hub, five context sections, three discovery links and sitemap updated.')
if __name__=='__main__':build(Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT)
