"""Promote category guides; retain shared-protocol workbooks as usable worksheets."""
from pathlib import Path
from html import escape
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from content.design_reference.topics import CATEGORIES, TOPICS
from content.design_reference.stages import STAGES

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist').resolve()
ORIGIN = 'https://www.mybnbdesign.com'
EDITORIAL = {
 'arrival': ('Design the arrival around a tired guest', 'Walk the route from parking to the door while carrying a bag. Decide where keys, shoes and luggage go before choosing a console or decorative objects. An entry bench is useful only if its location leaves room for the door and for another guest to pass.', 'Compare the entry in daylight and after dark. Photograph the actual arrival sequence and label the approved storage locations in the turnover record. Keep decorative styling subordinate to a legible route and clear guest instructions.'),
 'sleep': ('Specify a complete sleep setup', 'Treat the bed, mattress, linens, storage and turnover routine as one purchase. Confirm the room configuration and exact product instructions before ordering. Count the pieces needed for a normal reset and decide where the spare set can be stored.', 'Ask the person who will reset the room to review the proposed setup. Test access around the installed arrangement and the actual linen workflow. A photograph of a neatly made bed does not explain replacement availability or how the room will be maintained.'),
 'seating': ('Choose a seating arrangement before a sofa', 'Draw the gathering arrangement around the intended group, nearby doors and the room’s activities. Check side tables and lamps with the chairs occupied. Compare cleaning access and the route used to move the furniture into the property before accepting a final selection.', 'Review the room from a guest’s position, rather than only from the listing-photo angle. Record the accepted arrangement so the turnover team can restore it. If a substituted piece changes access, comfort or the number of usable places, reopen the room plan.'),
 'dining': ('Match meal service to the actual layout', 'Stage the intended meal setting with plates, chairs and serving items. An advertised seating count should describe a configuration the property can actually support. Where a table extends, include the process for moving chairs and storing the extra parts in the operating plan.', 'Check the path between the kitchen and table during a simulated meal and cleanup. Compare the everyday arrangement with the full-group arrangement. Record which configuration guests should find on arrival and which equipment is available on request.'),
 'kitchen': ('Build the kitchen around guest tasks', 'List the meals the kitchen is intended to support, then map preparation, cooking, serving and cleanup. Buy inventory for those tasks rather than for a generic photo checklist. Confirm the exact appliance instructions and identify where frequently replaced pieces will be sourced.', 'Run a simple arrival-to-breakfast exercise with the installed inventory. Can someone find the items, use the available workspace and return everything to its labeled location? Resolve missing pieces and crowded storage before calling the kitchen ready.'),
 'bathroom': ('Plan the bathroom reset with the storage', 'Coordinate towels, hooks, dispensers, bins and replacement stock as a single operating setup. Review where wet and dry items will sit and how the cleaner will reach the surfaces. Keep exact product care instructions with the approved inventory.', 'Have the reset team walk the finished room and identify the steps that depend on a spare, a refill or access behind an object. Test the actual storage arrangement and record what a complete guest-ready setup includes. Revisit the plan when a product changes.'),
 'lighting': ('Design a usable lighting sequence', 'Map arrival, reading, food preparation and bedtime separately. Record the installed fixture and control relationships, then ask the appropriate professional to resolve technical compatibility or installation questions. A matching appearance is insufficient evidence that a replacement will work.', 'Walk the property after dark using the controls as a first-time guest would. Check whether the intended task can be understood without a long explanation. Photograph the accepted setup, label the relevant controls and preserve exact replacement identifiers.'),
 'windows': ('Balance daylight, privacy and room operation', 'Review each window from inside and outside at the times the room is used. Decide which concerns the treatment should address: visibility, glare, sleep or operating access. Use actual opening measurements and product requirements rather than copying dimensions from a similar room.', 'Test the accepted treatment through its normal operating sequence. Record how it is reset and cleaned, where replacement parts are kept and which configuration appears in listing photos. Recheck the surrounding furniture if a treatment changes reach or access.'),
 'storage': ('Separate guest storage from owner stock', 'Map what guests bring, what the property supplies and what the turnover team needs to replenish. Give each category an actual location. A generous inventory is difficult to maintain when spare items displace usable guest storage or cannot be found during a reset.', 'Walk a normal turnover with the installed labels and quantities. Trace one replacement from delivery to its room, then identify who updates the inventory. Keep owner-only stock and the instructions for obtaining it clear to the responsible team.'),
 'surfaces': ('Choose finishes with the care workflow in mind', 'Compare the proposed finish, rug or upholstery with the property’s actual cleaning and removal process. Review exact care labels, compatibility requirements and replacement options. A description such as washable does not establish that the local team has suitable equipment or space.', 'Ask the reset team to review the accepted arrangement before final styling. Record the products and care instructions used, along with the arrangement that should be restored. Keep photographs and replacement details connected to the same room inventory.'),
 'outdoors': ('Plan outdoor spaces for changing conditions', 'Define the intended season and guest activities before buying furniture, shade or storage. Document the actual site and product requirements and assign technical questions to qualified providers. Include storage, inspections and the process for taking items out of service.', 'Walk the route from the indoor space to the outdoor setup, then plan a normal reset and an off-season changeover. Identify who handles weather-related changes and where components will be stored. Listing photos should reflect the arrangement and season guests can actually expect.'),
 'amenities': ('Select an amenity with a support plan', 'For a workspace, entertainment setup or guest device, define the ordinary task it should support. List the controls, accessories and service requirements needed to complete that task. Consider whether the property team can support the exact model when a guest has a question.', 'Ask someone unfamiliar with the setup to follow the approved instructions. Keep account access and private owner information outside guest-facing records. Document the accepted inventory, replacement process and person responsible for updates before promoting the amenity.'),
 'operations': ('Connect purchasing to installed evidence', 'Use one revision-controlled record to connect orders, deliveries, substitutions and what is actually installed. Give each unresolved item an owner and next action. The original shopping board should not become the final inventory without checking changes and credits.', 'At handoff, reconcile a room to invoices, accepted quantities and completion records. Distinguish delivery from installation and from guest readiness. Give the operating team the current instructions and open punch list so that a payment or attractive photograph is not mistaken for completed work.'),
 'identity': ('Make the property story accurate and maintainable', 'Choose a small set of visual and written cues that the property can carry consistently. Verify local claims, reproduction rights and product descriptions before publishing them. Connect guest information to the actual installed features rather than a generic destination narrative.', 'Review the finished listing and room information beside current photographs and inventory. Assign responsibility for updating changes, removing obsolete instructions and preserving permissions. A coherent identity depends on accurate details across the guest journey, not simply a repeated logo or color.'),
}

excluded = set()
for file in (OUT / 'learn/reference').rglob('index.html'):
    route = '/' + file.relative_to(OUT).as_posix()[:-10]
    # /learn/reference/{category}/{element}/{decision}/ only. Category owners stay indexable.
    if len(route.strip('/').split('/')) == 5:
        text = file.read_text()
        pattern = r'<meta\b(?=[^>]*\bname=[\"\x27]robots[\"\x27])[^>]*>'
        tag = '<meta name="robots" content="noindex, follow">'
        text = re.sub(pattern, tag, text, flags=re.I) if re.search(pattern, text, re.I) else text.replace('</head>', tag + '</head>', 1)
        file.write_text(text)
        excluded.add(ORIGIN + route)

if len(excluded) != len(TOPICS) * len(STAGES):
    raise ValueError('Reference inventory does not match the reviewed component/stage model')

for key, c in CATEGORIES.items():
    file = OUT / 'learn/reference' / key / 'index.html'
    text = file.read_text()
    text = text.replace(c['title'] + ': STR design workbooks', c['title'] + ': STR design guide')
    text = text.replace('STR DESIGN REFERENCE · COMPONENT WORKBOOK', 'STR DESIGN REFERENCE · DESIGN GUIDE')
    original_description = 'Study ' + str(c['expected']) + ' design elements across nineteen practical decisions, with specific evidence cards and editable property records.'
    description = 'Plan ' + c['title'].lower() + ' for a short-term rental. Compare fit, purchasing, installation and care with a practical component checklist.'
    text = text.replace(original_description, description)
    text = re.sub(r'<!-- category-editorial:start -->.*?<!-- category-editorial:end -->', '', text, flags=re.S)
    heading, first, second = EDITORIAL[key]
    panel = '<!-- category-editorial:start --><section class="guide-content"><h2>' + escape(heading) + '</h2><p>' + escape(first) + '</p><p>' + escape(second) + '</p>'
    panel += '<p>Guide updated October 19, 2026.</p><h3>Choose the evidence before the product</h3><ul>'
    for topic in [t for t in TOPICS if t['category'] == key]:
        panel += '<li><strong>' + escape(topic['name']) + ':</strong> ' + escape(topic['selection']) + '</li>'
    panel += '</ul><p>Use the component worksheets below when a specific task remains unresolved. For the whole project, follow the <a href="/design-roadmap/">design roadmap</a>, review <a href="/portfolio.html">the portfolio</a>, or discuss the <a href="/services.html">design service scope</a>.</p></section><!-- category-editorial:end -->'
    text = text.replace('<section class="reference-elements">', panel + '<section class="reference-elements">', 1)
    text = re.sub(r'("dateModified"\s*:\s*")[^"]+', r'\g<1>2026-10-19', text)
    file.write_text(text)

NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
ET.register_namespace('', NS)
for file in OUT.glob('sitemap*.xml'):
    tree = ET.parse(file)
    changed = False
    for row in list(tree.getroot()):
        loc = row.find('{*}loc')
        if loc is not None and loc.text in {ORIGIN + '/learn/reference/' + key + '/' for key in EDITORIAL}:
            lastmod = row.find('{*}lastmod')
            if lastmod is None:
                lastmod = ET.SubElement(row, '{'+NS+'}lastmod')
            lastmod.text = '2026-10-19'
            changed = True
        if loc is not None and loc.text in excluded:
            tree.getroot().remove(row)
            changed = True
    if changed:
        tree.write(file, encoding='utf-8', xml_declaration=True)

submitted = {loc.text for sitemap in OUT.glob('sitemap*.xml') for loc in ET.parse(sitemap).getroot().findall('.//{*}loc')}
assert not excluded & submitted, 'Utility workbook leaked into a sitemap'
assert all(ORIGIN + '/learn/reference/' + key + '/' in submitted for key in EDITORIAL), 'Guide missing from sitemap'
assert all((OUT / url[len(ORIGIN):].strip('/') / 'worksheet.csv').is_file() for url in excluded), 'Worksheet download missing'
print(json.dumps(dict(utility_workbooks_preserved_noindex=len(excluded), category_guides_strengthened=len(EDITORIAL))))
