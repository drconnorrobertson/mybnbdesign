"""Render the decision worksheets into the production output and sitemap."""
import csv
from dataclasses import dataclass
from io import StringIO
import html
from pathlib import Path
import sys
from urllib.parse import quote
import xml.etree.ElementTree as ET

NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
ET.register_namespace("", NS)
SECTION = "decision-worksheets"
START = "<!-- decision-worksheets:start -->"
END = "<!-- decision-worksheets:end -->"

BRAND = 'MyBnBDesign'
ORIGIN = 'https://www.mybnbdesign.com'
HUB = '/design-roadmap/'
HUB_LABEL = 'Airbnb design and furnishing worksheets'
STYLESHEET = '/styles.min.css'
CTA = '/book/'
CTA_LABEL = 'Book a design consultation'
REFERENCES = ['/services.html', '/best-vacation-rental-furnishing/', '/design-roadmap/scope-and-provider-selection/', '/faq-pricing.html', '/airbnb-furnishing-quotes-comparison-checklist.html', '/tools/furniture-shopping-list/', '/design-roadmap/procurement-receiving-and-claims/', '/design-roadmap/installation-photography-and-launch/', '/design-roadmap/measured-layout-and-delivery-access/', '/design-roadmap/post-launch-review-and-refresh/']

SCENARIOS = """
lake-house|a lake house|wet gear, lake-facing gathering space and indoor-outdoor circulation|entry-to-water route, drying space and actual guest count|mud, wet towels and bulky equipment bottleneck at the door
ski-condo|a ski condo|boot storage, shared access and compact seating|common-area delivery rules, winter entry route and gear dimensions|boots and jackets occupy circulation space during full occupancy
beach-house|a beach house|sand control, durable surfaces and outdoor storage|entry surfaces, rinse location and local receiving constraints|wet furnishings and sand multiply reset time between bookings
urban-condo|an urban condo|compact rooms, delivery restrictions and flexible seating|elevator dimensions, dock hours and measured floor plan|a large sofa cannot turn out of the freight elevator
desert-retreat|a desert retreat|sun exposure, shaded outdoor seating and dust control|time-of-day sun photos, fixture locations and storage dimensions|outdoor pieces degrade early or go unused through the hottest hours
mountain-cabin|a mountain cabin|dark evenings, wet gear and narrow access|night photos, entry dimensions and winter delivery availability|a large piece cannot reach the cabin during winter installation
rural-farmhouse|a rural farmhouse|group dining, uneven rooms and limited vendor coverage|door clearances, vendor travel terms and dining dimensions|an installer cannot return promptly after hardware is missing
a-frame|an A-frame cabin|sloped ceilings, loft access and limited wall clearance|sloped-wall sections, stair dimensions and bed location|a bed or seating piece fits on paper but blocks comfortable movement
tiny-home|a tiny home|storage, furniture dimensions and convertible seating|measured clearances, luggage plan and nightly sleep configuration|converting a room to sleeping use blocks the only passage
historic-home|a historic home|narrow stairs, uneven surfaces and existing character|stair turns, floor conditions and any permitted attachment methods|a freestanding or modular option is needed to avoid damaging existing finishes
new-construction|a new construction rental|delivery timing, site readiness and finish coordination|builder handoff date, utility status and cabinet dimensions|furniture arrives before floors or access are ready
waterfront-cabin|a waterfront cabin|view corridors, damp gear and weather-sensitive delivery|view angles, drying area and outdoor storage details|high-backed furniture blocks the strongest view from seated positions
townhouse|a townhouse|vertical circulation, shared walls and furniture assembly|stair turns, shared-wall locations and loading rules|noise travels between a game zone and neighboring sleeping areas
duplex|a duplex rental|unit identity, shared inventory and clear wayfinding|unit-level room lists, shared routes and matching replacement needs|orders reach the wrong unit and identical rooms remain incomplete
group-retreat|a group retreat|large-table seating, luggage and durable shared rooms|advertised occupancy, usable clearances and a turnover route|the nominal guest count exceeds usable dining and living seating
luxury-rental|a luxury rental|finish consistency, fixture service and receiving detail|finish samples, warranty documents and receiving schedule|a key finish is backordered and substitutions look inconsistent across rooms
suburban-home|a suburban rental home|family layout, owner storage and flexible guest rooms|target guest profile, room inventory and measurements|purpose-built furniture reduces flexibility for longer stays
family-rental|a family-oriented rental|bedroom adjacency, easy cleaning and practical storage|bed layout, circulation photos and the turnover process|children’s gear and luggage crowd hallways and bedrooms
pet-friendly|a pet-friendly rental|washable materials, entry cleanup and damage replacement|fabric care specifications, fence photos and entry measurements|unwashable upholstery has to be removed from service after a stay
accessible-layout|a rental with accessibility-focused design|measured routes, clearances and accurate listing information|door openings, thresholds and current route photos|furniture placement reduces the usable clearance shown in listing photos
pool-rental|a rental with a pool|towel drying, outdoor storage and clean transitions|pool-to-house route, storage plan and outdoor finish specs|wet traffic crosses primary living areas and accelerates surface wear
game-room|a rental with a game room|play clearance, sound and component durability|manufacturer dimensions, electrical locations and adjacent room layout|play space overlaps the main walking path or disturbs sleeping rooms
studio-rental|a studio rental|combined sleeping and living space, luggage and visual separation|measured plan, bed access, and seating footprint|a sleeper conversion eliminates the walking route or luggage area
longer-stays|a vacation rental set up for longer stays|work surfaces, kitchens and functional storage|outlet locations, kitchen inventory and closet measurements|the space photographs well but storage and work surfaces are insufficient
occupied-refresh|an operating Airbnb refresh|reusing furniture, staged work and booking blocks|existing room inventory, current booking calendar and delivery lead times|replacement items arrive in different weeks and extend downtime
"""

DECISIONS = """
designer-scope|Hiring an Airbnb designer|a measured brief, room inventory and a sample deliverable|Ask for a room-by-room scope with layout, selections and revision boundaries. Compare what the designer needs from you and when each approval is due.|a proposal that identifies included rooms, owner tasks and criteria for final design approval
turnkey-furnishing|Turnkey furnishing scope|a room list, delivery constraints and a proposed handoff date|Require the proposal to specify purchasing, freight, receiving, assembly, damage handling and removal. Ask what the installer considers a finished room.|an itemized furnishing scope showing every responsibility through final installation
remote-design|Remote Airbnb interior design|a dimensioned floor plan, site photos and a designated local contact|Ask who verifies field measurements, approves substitutions and answers installation questions. Agree on how local changes are recorded and reflected in the plans.|a remote handoff schedule with a measured plan, approvals and named on-site backup
design-cost|Design and furnishing budget|a room-level quantities and allowances worksheet|Break out design, products, tax, freight, receiving, assembly and installation. Keep replacement reserves and uncertain expenses separate from committed purchase orders.|a landed-cost budget that exposes allowances and discloses what is missing from the quote
furnishing-quote|Furnishing quote comparison|two written scopes normalized to the same dates and room count|Price the owner’s remaining work and compare payment milestones, change orders and damaged-item handling. Ask when pricing changes if stock is unavailable.|a side-by-side comparison of total scope, quote exclusions and owner responsibilities
furniture-package|Furniture package selection|a dimensioned furniture list and approved substitutions|Check quantities, clearances, surface care and the delivery route for each room. Ask which package items can be replaced individually and how long replacements take.|a room-level specification with dimensions, cleaning instructions and a replacement path
procurement|Furniture procurement and receiving|a purchase order log, receiving requirements and a claims process|Match line items to shipments and install locations. Document inspection before packaging disposal, then assign an owner for claims and delayed substitutions.|an order register linking vendor, delivery window, condition and open claims
installation|Installation and Airbnb setup|an access plan, crew schedule and room-by-room punch list|Sequence freight, assembly, cleaning and photography. Confirm who coordinates site access, packaging removal and return trips for incomplete work.|an installation schedule with booking blocks, vendor contacts and completion criteria
room-layout|Guest-ready room layout|a measured plan, guest-use scenarios and photos of current circulation|Walk the path guests use with luggage and estimate seating based on the actual published guest count. Mark major depths, door swings and access before placing orders.|an approved furniture plan with verified circulation, seating and delivery dimensions
refresh-plan|Airbnb redesign and replacement planning|an inventory of retained pieces, booking gaps and replacement candidates|Decide which items affect guest experience or operating effort, then sequence replacements around confirmed delivery and turnover windows.|a phased refresh schedule with keep, repair and replace decisions plus estimated downtime
"""


DECISION_NOTES = (
    ('Ask each designer to mark which drawing, specification or approval will address this issue. Compare who verifies the arrangement at the property and what counts as a revision.', 'The proposal identifies how the issue will be addressed, what you approve and which site checks are included.'),
    ('Ask the furnishing provider to price this issue under the complete scope and name the person responsible for resolving it. Check whether that work can affect the handoff date.', 'The scope assigns responsibility for delivery through completion and identifies any work that the owner still has to arrange.'),
    ('Send the same dated photos and measurements to each remote designer. Ask them to flag what they can resolve from the drawings and which checks require your local contact.', 'The handoff identifies the person who verifies site conditions, approves substitutions and answers installation questions.'),
    ('Create two room-level budget lines for this issue: the current plan and a fallback. Compare product costs, delivery, handling and installation separately for each.', 'The quote makes the cost of the fallback visible and distinguishes a documented price from a provisional allowance.'),
    ('Ask each bidder whether its quote covers addressing this issue. Put any additional owner costs in the same comparison column so exclusions do not disappear into the total.', 'The proposals are comparable on the delivered room scope, payment dates and handling of unresolved or changed items.'),
    ('Identify the first package item this issue affects. Check its dimensions and access route, and document a replacement that fits the room and the same use.', 'The package identifies what ships, which alternatives are acceptable and which pieces can be replaced without reordering the whole room.'),
    ('Flag the affected items in the receiving log and identify what the crew should photograph or measure before signing off. Note the deadline and responsible party for resolving a discrepancy.', 'Order, shipment, room and claim records can all be matched, and the next step is assigned if an item is late or damaged.'),
    ('Put the issue on the crew’s punch list and work backward from photography. Record which tasks can continue and how someone on site can verify the fix.', 'The schedule identifies any blocked tasks and includes a room-level completion check before the property is photographed.'),
    ('Mark the affected path or furniture footprint on a measured plan. Test it using the actual activities guests will perform and check that the furniture can reach its proposed location.', 'The layout preserves usable circulation and seat count and identifies any measurement still needed before an order.'),
    ('Mark the affected item or area as keep, repair or replace. Compare the disruption, lead time and installation work for two approaches before blocking the booking calendar.', 'The refresh plan identifies what can stay in service and gives each replacement a delivery window and a backup.'),
)

ADDITIONAL_SCENARIOS = """
carriage-house|a carriage-house rental|privacy, compact storage and a separate arrival route|entry photos, measured stair turns and existing storage dimensions|arrival luggage backs up at the stairs because the entry has no clear landing space
basement-suite|a basement-suite rental|lighting, low ceiling clearances and moisture-aware finishes|ceiling measurements, daylight photos and the location of mechanical access|tall pieces block the service hatch and make a narrow room feel darker
penthouse|a penthouse rental|freight access, view corridors and wind-exposed exterior space|elevator dimensions, loading hours and balcony photos|a sectional fits the room but requires a revised delivery plan to reach it
bungalow|a bungalow rental|small living rooms, porch use and flexible guest seating|measured layout, doorway widths and a list of existing pieces|extra chairs for full occupancy block the main path to the kitchen
courtyard-property|a courtyard rental|wayfinding, shared space and outdoor furniture storage|arrival photos, a marked site plan and actual outdoor dimensions|guests confuse the shared courtyard with the private entry after dark
barn-conversion|a converted barn rental|large-volume lighting, acoustics and usable gathering zones|ceiling heights, night photographs and the measured dining zone|conversations carry into sleeping areas when the central room is occupied
log-home|a log home rental|lighting against dark walls, uneven surfaces and compatible attachments|wall details, lighting locations and clearances around major furniture|the largest room appears underlit when the existing fixtures are tested after dark
canal-home|a canal-front rental|water-facing seating, drying space and salt-exposed finishes|sightline photos, waterside access route and finish care instructions|furniture blocks the water view and wet equipment accumulates near the glass doors
hillside-home|a hillside rental|delivery approach, stairs and luggage movement|driveway dimensions, stair turns and parking-to-entry measurements|an oversized shipment cannot make a driveway turn and needs a transfer crew
golf-resort-condo|a golf-resort condo rental|club storage, compact dining and restricted receiving hours|delivery rules, storage dimensions and seating plan|the proposed club storage displaces bags and shoes needed near the entrance
work-retreat|a rental set up for team retreats|work surfaces, task lighting and shared dining clearance|outlet map, chair-count inventory and measured tables|the meeting table can seat everyone but leaves no comfortable circulation during work sessions
two-bedroom-refresh|a two-bedroom rental refresh|layout continuity, retained furniture and a short turnover window|current inventory, delivery dates and measurement photos|one delayed bed frame threatens to keep an otherwise finished room out of service
sleeping-loft|a rental with a sleeping loft|stair access, furniture height and nighttime orientation|loft dimensions, stair photos and fixture locations|an assembled piece cannot turn at the loft entry and a standard-height headboard conflicts with the slope
outdoor-kitchen|a rental with an outdoor kitchen|service access, storage and sheltered dining|site plan, equipment clearances and the route for cleaning|the layout provides seating but blocks the service route used during turnover
converted-garage|a converted-garage rental|entry comfort, visual zoning and utility access|actual entry dimensions, outlet map and mechanical clearances|a furniture divider partly blocks the only easy access to utility equipment
"""
READY_WORKSHEETS = ('design-cost-barn-conversion', 'design-cost-basement-suite', 'design-cost-bungalow', 'design-cost-canal-home', 'design-cost-carriage-house', 'design-cost-converted-garage', 'design-cost-courtyard-property', 'design-cost-golf-resort-condo', 'design-cost-hillside-home', 'design-cost-log-home', 'design-cost-outdoor-kitchen', 'design-cost-penthouse', 'design-cost-sleeping-loft', 'design-cost-two-bedroom-refresh', 'design-cost-work-retreat', 'designer-scope-barn-conversion', 'designer-scope-basement-suite', 'designer-scope-bungalow', 'designer-scope-canal-home', 'designer-scope-carriage-house', 'designer-scope-converted-garage', 'designer-scope-courtyard-property', 'designer-scope-golf-resort-condo', 'designer-scope-hillside-home', 'designer-scope-log-home', 'designer-scope-outdoor-kitchen', 'designer-scope-penthouse', 'designer-scope-sleeping-loft', 'designer-scope-two-bedroom-refresh', 'designer-scope-work-retreat', 'furnishing-quote-barn-conversion', 'furnishing-quote-basement-suite', 'furnishing-quote-bungalow', 'furnishing-quote-canal-home', 'furnishing-quote-carriage-house', 'furnishing-quote-converted-garage', 'furnishing-quote-courtyard-property', 'furnishing-quote-golf-resort-condo', 'furnishing-quote-hillside-home', 'furnishing-quote-log-home', 'furnishing-quote-outdoor-kitchen', 'furnishing-quote-penthouse', 'furnishing-quote-sleeping-loft', 'furnishing-quote-two-bedroom-refresh', 'furnishing-quote-work-retreat', 'furniture-package-basement-suite', 'furniture-package-bungalow', 'furniture-package-carriage-house', 'furniture-package-courtyard-property', 'furniture-package-penthouse', 'remote-design-barn-conversion', 'remote-design-basement-suite', 'remote-design-bungalow', 'remote-design-canal-home', 'remote-design-carriage-house', 'remote-design-converted-garage', 'remote-design-courtyard-property', 'remote-design-golf-resort-condo', 'remote-design-hillside-home', 'remote-design-log-home', 'remote-design-outdoor-kitchen', 'remote-design-penthouse', 'remote-design-sleeping-loft', 'remote-design-two-bedroom-refresh', 'remote-design-work-retreat', 'turnkey-furnishing-barn-conversion', 'turnkey-furnishing-basement-suite', 'turnkey-furnishing-bungalow', 'turnkey-furnishing-canal-home', 'turnkey-furnishing-carriage-house', 'turnkey-furnishing-converted-garage', 'turnkey-furnishing-courtyard-property', 'turnkey-furnishing-golf-resort-condo', 'turnkey-furnishing-hillside-home', 'turnkey-furnishing-log-home', 'turnkey-furnishing-outdoor-kitchen', 'turnkey-furnishing-penthouse', 'turnkey-furnishing-sleeping-loft', 'turnkey-furnishing-two-bedroom-refresh', 'turnkey-furnishing-work-retreat')


@dataclass(frozen=True)
class Scenario:
    slug: str
    description: str
    priorities: str
    evidence: str
    complication: str


@dataclass(frozen=True)
class Decision:
    slug: str
    title: str
    inputs: str
    method: str
    deliverable: str


def records(data, cls):
    return [cls(*line.split("|")) for line in data.strip().splitlines()]


def route(decision, scenario):
    return f"/{SECTION}/{decision.slug}-{scenario.slug}/"


def title(decision, scenario):
    return f"{decision.title} for {scenario.description}"


def link(url, label):
    return f'<a href="{html.escape(url, quote=True)}">{html.escape(label)}</a>'


ORIGINAL_SCENARIO_SLUGS = {item.slug for item in records(SCENARIOS, Scenario)}

def worksheet_download(decision, scenario, priorities):
    output = StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["Review item", "Evidence to request", "Source or quote", "Owner", "Due date", "Decision or follow-up"])
    writer.writerow([decision.title, decision.inputs, "", "", "", ""])
    writer.writerow(["Property records", scenario.evidence, "", "", "", ""])
    for item in priorities:
        writer.writerow([item.capitalize(), "", "", "", "", ""])
    writer.writerow(["Scenario to test", scenario.complication, "", "", "", ""])
    writer.writerow(["Before committing", decision.deliverable, "", "", "", ""])
    data_url = "data:text/csv;charset=utf-8," + quote(output.getvalue(), safe="")
    filename = f"{decision.slug}-{scenario.slug}.csv"
    return f'<a class="action" href="{data_url}" download="{filename}">Download this worksheet (CSV)</a>'


def article(decision, scenario, next_decision, next_scenario, reference, notes):
    heading = title(decision, scenario)
    meta = f"Use this worksheet to compare {decision.title.lower()} for {scenario.description}. Review {scenario.priorities} and record what changes your decision."
    other = [
        link(route(next_decision, scenario), title(next_decision, scenario)) if scenario.slug in ORIGINAL_SCENARIO_SLUGS else link(HUB + '#decision-worksheets', HUB_LABEL),
        link(route(decision, next_scenario), title(decision, next_scenario)),
        link(reference, decision.title + " guide"),
    ]
    priorities = scenario.priorities.rsplit(" and ", 1)[0].split(", ", 1) + [scenario.priorities.rsplit(" and ", 1)[-1]]
    checks = "".join(f"<li>{html.escape(item.capitalize())}</li>" for item in priorities)
    response, review = notes
    e = html.escape
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(heading)} | {BRAND}</title>
  <meta name="description" content="{e(meta, quote=True)}">
  <link rel="canonical" href="{ORIGIN}{route(decision, scenario)}">
  <link rel="stylesheet" href="{STYLESHEET}">
  <style>
    .worksheet {{max-width: 52rem; margin: auto; padding: clamp(1rem, 4vw, 3rem); color: #1e2e2a; background: #fff; line-height: 1.65}}
    .worksheet h1 {{font-size: clamp(2rem, 5vw, 3.25rem); line-height: 1.12; margin: 1.25rem 0}}
    .worksheet h2 {{font-size: 1.4rem; margin: 1.75rem 0 .65rem}}
    .worksheet a {{color:#205745; text-decoration: underline}}
    .worksheet table {{width: 100%; border-collapse: collapse; overflow-wrap: anywhere}}
    .worksheet th,.worksheet td {{padding: .55rem; border: 1px solid #bacac4; text-align: left; vertical-align: top}}
    .worksheet .action {{display:inline-block; padding:.65rem .9rem; background:#e9f3ef; margin-top:.7rem}}
  </style>
</head>
<body>
<main class="worksheet" id="main">
  <nav aria-label="Breadcrumb">{link("/", BRAND)} · {link(HUB + "#decision-worksheets", HUB_LABEL)}</nav>
  <article>
    <h1>{e(heading)}</h1>
    <p>Start with {e(decision.inputs)}. For {e(scenario.description)}, bring the following records to the comparison so the decision reflects the actual property rather than a generic brief.</p>
    <p><strong>Property evidence to gather:</strong> {e(scenario.evidence)}.</p>
    <h2>What to check at this property</h2>
    <ul>{checks}</ul>
    <p>{e(decision.method)}</p>
    <h2>Work through this example before committing</h2>
    <p>Suppose {e(scenario.complication)}. Identify which part of {e(decision.title.lower())} changes first, who can verify the impact and when you need their answer. Compare three responses: proceed with documented conditions, revise the scope or schedule, or pause until you have the missing evidence.</p>
    <p>{e(response)}</p>
    <p><strong>Before you proceed:</strong> {e(review)}</p>
    <h2>Record your decision</h2>
    <table>
      <thead><tr><th scope="col">Record</th><th scope="col">What to capture</th></tr></thead>
      <tbody>
        <tr><th scope="row">Evidence</th><td>{e(scenario.evidence.capitalize())}. Add the date, source and the question each record answers.</td></tr>
        <tr><th scope="row">Open issue</th><td>Record the affected room, unit or operating period, the person checking it and the deadline.</td></tr>
        <tr><th scope="row">Decision</th><td>Complete {e(decision.deliverable)}. Add the reason for proceeding, revising or pausing.</td></tr>
      </tbody>
    </table>
    <p>{worksheet_download(decision, scenario, priorities)}</p>
    <p class="action">{link(CTA, CTA_LABEL)}</p>
    <h2>Related guides and worksheets</h2>
    <ul>{"".join(f"<li>{item}</li>" for item in other)}</ul>
  </article>
</main>
</body>
</html>
"""


def add_hub(output, decisions, scenarios):
    groups = []
    for decision in decisions:
        links = "".join(
            f"<li>{link(route(decision, scenario), title(decision, scenario))}</li>"
            for scenario in scenarios
            if scenario.slug in ORIGINAL_SCENARIO_SLUGS or route(decision, scenario).split('/')[-2] in READY_WORKSHEETS
        )
        groups.append(f"<details><summary>{html.escape(decision.title)}</summary><ul>{links}</ul></details>")
    block = (
        START + '<section class="section" id="decision-worksheets"><div class="wrap" style="max-width:52rem;margin:auto;padding:1.5rem">'
        f"<h2>{HUB_LABEL}</h2><p>Pick the decision you’re making and the property type you’re working with. "
        "Each worksheet identifies the evidence to collect, a scenario to work through and what to record before you commit.</p>"
        + "".join(groups) + "</div></section>" + END
    )
    target = output / HUB.lstrip("/") / "index.html"
    existing = target.read_text()
    if START in existing:
        before, tail = existing.split(START, 1)
        _, after = tail.split(END, 1)
        updated = before + block + after
    else:
        close_main = existing.rfind("</main>")
        if close_main == -1:
            raise ValueError(f"No main element in {target}")
        updated = existing[:close_main] + block + existing[close_main:]
    target.write_text(updated)


def add_reference_links(output, decision, scenarios, reference):
    if reference == HUB:
        return
    target = output / reference.lstrip("/")
    if target.is_dir():
        target /= "index.html"
    existing = target.read_text()
    start = f"<!-- worksheet-links:{decision.slug}:start -->"
    end = f"<!-- worksheet-links:{decision.slug}:end -->"
    items = "".join(f"<li>{link(route(decision, scenario), title(decision, scenario))}</li>" for scenario in scenarios)
    block = (
        start + '<section class="section" style="max-width:52rem;margin:auto;padding:1.5rem">'
        f"<h2>{html.escape(decision.title)} worksheets by property type</h2>"
        f"<details><summary>Browse property-specific worksheets</summary><ul>{items}</ul></details></section>" + end
    )
    if start in existing:
        before, rest = existing.split(start, 1)
        _, after = rest.split(end, 1)
        updated = before + block + after
    else:
        marker = "</main>" if "</main>" in existing else "</body>"
        index = existing.rindex(marker)
        updated = existing[:index] + block + existing[index:]
    target.write_text(updated)


def tag(name):
    return f"{{{NS}}}{name}"


def add_sitemap(output, urls):
    main = output / "sitemap.xml"
    tree = ET.parse(main)
    root = tree.getroot()
    if root.tag == tag("sitemapindex"):
        filename = "sitemap-decision-worksheets.xml"
        sitemap_url = f"{ORIGIN}/{filename}"
        if not any(node.text == sitemap_url for node in root.iter(tag("loc"))):
            ET.SubElement(ET.SubElement(root, tag("sitemap")), tag("loc")).text = sitemap_url
        tree.write(main, encoding="utf-8", xml_declaration=True)
        root = ET.Element(tag("urlset"))
        tree = ET.ElementTree(root)
        target = output / filename
    elif root.tag == tag("urlset"):
        target = main
    else:
        raise ValueError(f"Unexpected sitemap format in {main}")
    known = {node.text for node in root.iter(tag("loc"))}
    for url in urls:
        if url not in known:
            ET.SubElement(ET.SubElement(root, tag("url")), tag("loc")).text = url
    tree.write(target, encoding="utf-8", xml_declaration=True)


def main(output):
    scenarios = records(SCENARIOS, Scenario)
    decisions = records(DECISIONS, Decision)
    additional = records(ADDITIONAL_SCENARIOS, Scenario)
    all_scenarios = scenarios + additional
    urls = []
    for index, decision in enumerate(decisions):
        for position, scenario in enumerate(all_scenarios):
            path = route(decision, scenario)
            if position >= len(scenarios) and path.split('/')[-2] not in READY_WORKSHEETS:
                continue
            target = output / path.lstrip("/") / "index.html"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(article(
                decision, scenario,
                decisions[(index + 1) % len(decisions)] if position < len(scenarios) else decision,
                scenarios[(position + 1) % len(scenarios)],
                REFERENCES[index],
                DECISION_NOTES[index],
            ))
            urls.append(ORIGIN + path)
    if len(urls) != 250 + len(READY_WORKSHEETS) or len(set(urls)) != len(urls):
        raise ValueError("Unexpected worksheet count or duplicate route")
    for decision, reference in zip(decisions, REFERENCES):
        related = scenarios + [item for item in additional if route(decision, item).split('/')[-2] in READY_WORKSHEETS]
        add_reference_links(output, decision, related, reference)
    add_hub(output, decisions, all_scenarios)
    add_sitemap(output, urls)
    print(f"Published {len(urls)} {BRAND} decision worksheets")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
