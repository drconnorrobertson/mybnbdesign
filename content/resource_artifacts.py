"""Practical artifacts retained and expanded at ten established resource routes.

These are original planning worksheets, not claims about financial or guest outcomes.
Keep the artifacts with the editorial data so rendered pages and downloads agree.
"""

ARTIFACTS = {}

def add(slug, sections):
    ARTIFACTS['/resources/' + slug + '/'] = sections

def section(identifier, title, text='', headers=None, rows=None, template=None, items=None):
    return dict(id=identifier, title=title, text=text, headers=headers or [],
                rows=rows or [], template=template or '', items=items or [])

add('airbnb-furnishing-checklist', [
section('inventory-method', 'Use the inventory as a purchasing and reset record',
'''Complete a separate sheet for each room. The lists below are prompts rather than a requirement to buy every item. Record the planned guest use, the quantity actually needed, the retained quantity, the quantity to order, and the place each item belongs. A useful inventory also identifies the exact size or model, its care instructions, its delivery status, and who checks it at handover.

Start with the furnished capacity and the real operating plan. Count dining places with chairs in use, beds with their actual linen sizes, and storage with luggage present. Do not infer permitted occupancy from the number of chairs or beds. Check relevant property requirements separately. Where a supplied appliance or activity requires technical review, keep that approval outside the shopping checklist and record who is responsible.

Before ordering, mark each line as retain, repair, buy, optional, or not applicable. Split sets into their replaceable components: a lost pillowcase does not necessarily require a new sheet set, and a broken mug does not require another full dinner service. Include freight, assembly, receiving, disposal, and spare quantities in the purchasing sheet rather than treating the product price as the whole cost.''',
template='''ROOM INVENTORY RECORD
Property / room: [name]
Prepared by / date: [person / date]
Planned guest activities: [sleeping / dining / work / storage / other]
Item: [specific item]
Size, model, finish: [exact specification]
Required quantity: [quantity]   Retained and usable: [quantity]
Order quantity: [quantity]     Optional spare quantity: [quantity]
Status: [retain / repair / buy / optional / not applicable]
Unit quote / delivery / assembly / tax: [actual written costs]
Vendor / lead time / delivery reference: [confirmed information]
Reset location / care document: [location / document]
Acceptance check / owner / due date: [check / person / date]'''),
section('living-room-inventory', 'Living room and dining inventory',
'''Trial the full guest group before approving a layout. Include seating with feet on the floor, chairs pulled out, and a sofa bed open if supplied. Leave controls, cleaning access, doors, and usable travel routes in view. The inventory is complete when the items fit and can be reset, not just when the purchase list has been ticked.''',
headers=['Category', 'Items to check', 'Specification or reset question'], rows=[
['Seating', 'Sofa; armchairs; any supplied sofa bed; protective covers where appropriate', 'Usable seats, open-bed footprint, upholstery care, replaceable components'],
['Tables', 'Coffee or side tables; dining table; dining chairs', 'Stable condition, chair pullout, drink placement, cleaning access'],
['Lighting', 'Fixed lights; reading/task lamps; compatible bulbs and recorded spares', 'Controls reachable from actual seats; glare and nighttime route tested'],
['Entertainment', 'Television where supplied; remote; operating instructions; documented cables', 'Guest setup accurately described; no owner accounts or private paperwork exposed'],
['Storage', 'Luggage landing; coat/shoe storage; book or game storage if supplied', 'Storage does not block movement; contents can be counted and reset'],
['Finishing items', 'Rug if appropriate; wall art; selected washable throws or cushions', 'Exact care method, secure installation review, manageable decoration quantity'],
['Dining reset', 'Placemats or table protection where supplied; serving pieces; spare chair parts if appropriate', 'Table protection follows finish instructions and is easy to reproduce'],
]),
section('kitchen-inventory', 'Kitchen inventory by the meals you actually support',
'''Write a simple meal trial before choosing quantities: prepare breakfast, assemble a basic cooked meal, and clear up afterward. Check the equipment provided with that trial and the property’s guest capacity. Choose compatible cookware from the exact appliance instructions. Do not add a device just to lengthen the amenity list; each supplied device needs storage, operating instructions, cleaning, and a reset check.''',
headers=['Category', 'Inventory prompts', 'Count or compatibility check'], rows=[
['Cookware', 'Frying pan; saucepan; larger pot; lids; baking tray; oven dish where relevant', 'Compatible with supplied cooktop/oven; capacity matches the intended meal'],
['Preparation', 'Cutting boards; suitable knives; measuring tools; mixing bowl; colander', 'Stable, cleanable storage; components counted separately'],
['Utensils', 'Spatula; stirring spoon; ladle; tongs; whisk; peeler; opener', 'Tools fit the actual cookware and supported cooking tasks'],
['Dishware', 'Dinner plates; side plates; bowls; mugs', 'Usable quantity for the guest allocation and laundry/dishwashing process'],
['Glassware and cutlery', 'Drinking glasses; forks; knives; spoons; teaspoons', 'Replaceable model or size recorded; no chipped or unsuitable pieces counted'],
['Serving and storage', 'Serving bowl; platter where supplied; food-storage containers and lids', 'Pair lids with containers; confirm safe intended use from product instructions'],
['Appliances', 'Refrigerator; cooktop/oven; coffee setup; kettle; toaster; other actual supplied appliances', 'Installed and commissioned; manual and guest instructions available'],
['Consumables', 'Any listed coffee/tea allocation; approved dish-cleaning supplies; bin liners', 'Only promise the actual quantity and replenishment standard'],
['Cleaning and linens', 'Kitchen towels; approved cloths; drying setup; waste/recycling bins', 'Drying location, replacement frequency, and reset owner specified'],
]),
section('bedroom-inventory', 'Bedroom and guest-bedroom inventory',
'''Use one record per sleeping position and bed size, including a separate record for a convertible bed. Check the mattress, frame, protector, sheet depth, and cover together before buying multiples. Optional pillow choices need clean storage and care instructions. Furniture marketed for children, bunks, or infant use needs its own exact product and qualified suitability review; a room list is not a safety approval.''',
headers=['Category', 'Inventory prompts', 'Functional check'], rows=[
['Bed system', 'Bed/frame; mattress; exact fitted protector; fitted/flat sheets as used; pillowcases; cover or blanket', 'Dimensions and making method tested as one system'],
['Linen stock', 'Installed sets; sets in laundry; working stock; separately justified spare components', 'Quantity follows the actual changeover and laundry-return cycle'],
['Pillows', 'Installed pillows; optional alternatives if supplied; appropriate protectors/cases', 'Care labels, identifying labels, and clean dry storage documented'],
['Bedside use', 'Suitable bedside surface; reading light; reachable power; personal-item landing', 'Test from the actual bed position; avoid obstructing doors or curtains'],
['Storage', 'Luggage support; clothes storage; usable hangers; any supplied laundry bag', 'Capacity and placement match the room rather than unused floor area'],
['Window and climate', 'Window treatment; operating instructions; approved control labels', 'Light gaps and control access checked in actual nighttime conditions'],
['Guest bedroom', 'A separately counted complete bed/linen system for every supplied bed', 'Do not assume a spare room can share stock or instructions with the main bedroom'],
]),
section('bathroom-outdoor-utility-inventory', 'Bathroom, outdoor, utility and connectivity inventory',
'''Inspect bathroom contents after a realistic guest-use trial, including towel drying and placement of personal toiletries. Outdoors, distinguish permanently installed items from loose pieces that require a weather handoff. For supplies stored in an owner cupboard, separate guest access from the cleaner’s stock and record the approved storage arrangement. Keep property-specific emergency equipment and inspection requirements in a qualified checklist rather than inventing a universal shopping quantity.''',
headers=['Area', 'Inventory prompts', 'Handover check'], rows=[
['Bathroom linens', 'Bath towels; hand towels; washcloths where supplied; bath mat; working linen stock', 'Actual allocation, laundry cycle, dry storage, and towel-drying locations'],
['Bathroom accessories', 'Hooks/rails; mirror; waste bin; toilet-paper holder; cleaner-approved dispensers; personal-item surface', 'Reach, mounting review, cleanability, and replenishment owner'],
['Bathroom extras', 'Hair dryer or other listed amenity if supplied; its manual and storage', 'Exact instructions available; damaged equipment excluded from reset'],
['Outdoor activities', 'Suitable table/chairs or loungers; approved shade; cushion covers; storage', 'Exposure suitability, dry storage, weather limits, and loose-item count'],
['Utility and laundry', 'Washer/dryer if supplied; manuals; iron/board if supplied; baskets; permitted care supplies', 'Installed process, machine capacity, drying, and access instructions'],
['Cleaning support', 'Approved cleaning tools; vacuum if supplied; spare bags/parts; waste supplies', 'Owner and guest responsibilities distinguished; product labels retained'],
['Connectivity', 'Actual Wi-Fi/network instructions; supplied charging setup; guest-use technology instructions', 'Test connection and controls; keep private account or access details out of public worksheets'],
['Safety review', 'Property-specific installed safety equipment, inspection records, and responsible contacts', 'Confirm relevant requirements and operating instructions with qualified providers'],
]),
section('furnishing-purchase-controls', 'Order, receive and maintain the complete list',
'''A higher product price does not establish longer service life, and a cheaper product may become expensive after assembly or repeated replacement. Compare exact specifications and complete installed costs. Keep a contingency separate from optional decoration, and record any substitution before purchase. At receipt, reconcile counts, dimensions, damage, and missing parts against the approved line rather than relying on a delivery photograph alone.''',
items=[
'Measure retained items and exclude unusable stock before setting order quantities.',
'Record actual quotes, stock confirmation, returns terms, delivery scope, and receiving responsibilities.',
'Approve substitutions against room fit, care, finish, function, cost, and delivery constraints.',
'Photograph received condition, match shipment identifiers, and follow the vendor’s actual discrepancy process.',
'Complete the room reset trial, label spare components, and file warranty/care information at handover.',
'Reconcile the inventory after loss, repair, or replacement so the next order reflects the current property.',
]),
])

add('briefing-designer-str', [
section('design-brief-template', 'Copy and complete the design brief',
'''A brief should let another person make a consistent decision without guessing what the owner meant. Fill in the fields below before the first scope meeting. Use measured facts and label estimates or unknowns. Keep private access details, guest records, account credentials, and sensitive owner information out of a general design pack; share only the material the actual project requires through an appropriate channel.''',
template='''SHORT-TERM RENTAL DESIGN BRIEF
Project name / version / date: [name / version / date]
Decision owner and working contact: [person / business contact]
Property type and rooms in scope: [type / room list]
Measured floor plan and annotated photo folder: [document references]
Fixed constraints and uncertain dimensions: [doors / windows / utilities / unknowns]
Permitted guest capacity and intended activities: [separately confirmed capacity / uses]
Existing items to retain, repair or remove: [inventory references]
Design direction and reference images: [links / what you like about each image]
Colors, finishes or themes to avoid: [specific restrictions]
Essential guest functions and optional amenities: [priority list]
Cleaning, laundry, storage and repair requirements: [actual operating process]
Accessibility or other technical review needs: [questions / qualified reviewer]
Property/building constraints to confirm: [relevant restrictions / responsible person]
Total available project allowance: [actual amount / inclusions]
Delivery, tax, assembly, disposal and contingency: [included / excluded / allowance]
Service scope required: [design / purchasing / receiving / install / styling / photos]
Target readiness date and unavailable access dates: [dates]
Approval milestones and response owner: [milestones / person]
Delivery route, receiving contact and storage: [survey / person / location]
Substitution approval process: [who approves / what evidence is required]
Required handover documents: [inventory / care / warranties / reset photos / issues]
Success at acceptance: [observable tests, not a promised revenue result]
Open questions and responsible owners: [question / person / due date]'''),
section('designer-pre-meeting-pack', 'Assemble the evidence behind the brief',
'''Send a concise document index with the brief so the designer can find the relevant evidence. A reference photograph is useful when you explain whether it represents a color, material, layout, or atmosphere; it is less useful as an instruction to reproduce a room with different dimensions. Include both what you like and what should not be copied. Document existing wear and service constraints before assuming that a retained item is suitable.''',
headers=['Document', 'Include', 'Question it resolves'], rows=[
['Measured survey', 'Room dimensions, ceiling constraints, fixed fixtures, doors/windows and unresolved measurements', 'What can actually fit and which dimensions need confirmation?'],
['Annotated photographs', 'Wide views plus labels for retained items, control locations and condition issues', 'What is present today, and what cannot be inferred from a plan?'],
['Retained inventory', 'Size/model, condition, repair decision and approved reset use', 'Which purchases are unnecessary or need compatibility checks?'],
['Guest-use brief', 'Sleeping, dining, luggage, work and activity needs for the planned capacity', 'Which functions take priority over optional styling?'],
['Operating notes', 'Cleaner feedback, laundry process, spare storage and repair responsibility', 'Can the installed design be cleaned and maintained?'],
['References and restrictions', 'A few labeled reference images plus relevant property/building constraints', 'Which aesthetic choices are intentional and which need qualified review?'],
['Budget sheet', 'Actual available funds and full installed-cost categories', 'Is the selection within the same stated scope?'],
]),
section('designer-scope-budget-table', 'Compare proposals against one scope',
'''Separate service fees from the products and third-party work. Ask who places orders, owns vendor communication, handles receiving discrepancies, approves substitutions, and completes installation. A proposal can appear less expensive because it omits work the owner still has to pay for or perform. Do not infer return on investment from a design quote; define success through delivered scope and tested function.''',
headers=['Scope line', 'Record in every proposal', 'Owner question'], rows=[
['Concept and plans', 'Rooms, drawings, revision rounds, and approval deliverables', 'Which layouts and specifications become part of the final pack?'],
['Product sourcing', 'Selection list, procurement responsibility and substitution process', 'Who confirms current availability and exact product identity?'],
['Purchasing and receipts', 'Payment process, receipts, order tracking and warranty handover', 'Who owns the vendor relationship and records?'],
['Freight and receiving', 'Delivery type, access limitations, storage and inspection responsibilities', 'Who resolves missing/damaged items under the vendor’s terms?'],
['Installation', 'Assembly, placement, qualified work, disposal and final cleaning scope', 'Which tasks or specialist approvals remain outside the designer’s service?'],
['Launch and handover', 'Reset photos, care register, commissioning trial and unresolved issues', 'What evidence is required before acceptance?'],
['Cost changes', 'Actual fee/product totals, exclusions, contingency and written change approval', 'What can change the price and who must approve it first?'],
]),
section('designer-project-gates', 'Build dates from dependencies, not a universal duration',
'''Ask for a schedule based on confirmed access, approval time, procurement information, room readiness, and actual delivery arrangements. Generic promises about an eight-week project or a two-day install are not a substitute for this property’s dependencies. A target date is a planning constraint until its prerequisites have been confirmed.''',
headers=['Gate', 'Evidence needed to proceed', 'Record'], rows=[
['Brief approved', 'Scope, priorities, measured facts and unresolved questions agreed', 'Decision owner / date / open questions'],
['Plan approved', 'Usable layout, retained items, budget reconciliation and technical review needs identified', 'Version / approval / conditions'],
['Order approved', 'Exact items, installed costs, stock and delivery scope confirmed', 'Quote references / substitution rules'],
['Ready for delivery', 'Room readiness, access route, receiving contact and storage confirmed', 'Readiness owner / evidence / date'],
['Install and test', 'Items reconciled, qualified work handled, full guest-use/reset trial completed', 'Defects / owner / completion evidence'],
['Handover accepted', 'Care, warranty, inventory, reset photos and unresolved issues delivered', 'Acceptance record / follow-up plan'],
]),
section('designer-proposal-questions', 'Resolve unclear answers before appointing the team',
'''Keep a written question log rather than treating a polished presentation as evidence of the whole service. Ask for examples of the relevant deliverables and how the team deals with substitutions, missed delivery dates, damaged products, and operational constraints. A response should identify scope, responsibility, and a practical next step; an unsupported promise about bookings does not answer those questions.''',
items=[
'Which comparable scope has the team delivered, and which evidence can be reviewed?',
'What rooms, revisions, purchasing tasks, install tasks, and exclusions are in the written proposal?',
'Who checks measurements and who is accountable for delivery-route confirmation?',
'How are fabric care, laundry capacity, cleaner access, and replacement parts considered?',
'What requires qualified technical review, and who obtains it?',
'How are changes, substitutions and additional charges documented before approval?',
'What communication cadence, decision log and escalation contact will the project use?',
'Which final records and tests establish acceptance, and how are open issues handed over?',
]),
])

add('damage-resistant-materials', [
section('material-comparison-matrix', 'Compare exact materials without calling any option indestructible',
'''Compare products within their actual intended use. A material name alone does not establish suitability: finish, seams, mounting, backing, exposure, installation, and care instructions all matter. The table is a question list for samples and written specifications, not a ranking of brands or a universal performance promise. For flooring, wet areas, electrical work, or other regulated work, keep technical specification and installation review with qualified providers.''',
headers=['Location', 'Options to compare', 'Evidence and practical trial'], rows=[
['Living/dining floor', 'Exact resilient, tile, wood or other proposed flooring products', 'Intended use, finish care, joints/edges, installed sample and qualified specification review'],
['Wet-area surface', 'Exact proposed floor/wall system, grout/joints and accessories', 'Product suitability, installation details, drainage/cleaning access and relevant qualified review'],
['Countertop/tabletop', 'Exact stone, engineered surface, laminate, wood or coated finish', 'Care instructions, edge details, approved spill response and repair/service options'],
['Upholstery', 'Exact fabric, removable-cover system and cushion construction', 'Care label, permitted products/process, drying, spare covers and replacement availability'],
['Bed linens', 'Exact sheet, protector, cover and towel products', 'Fit, manufacturer laundry process, drying capacity and component replacement'],
['Paint/wall finish', 'Exact product, color, sheen and substrate preparation', 'Cleaning instructions, touch-up sample, batch/reference record and qualified application advice'],
['Furniture structure', 'Exact wood/veneer, metal or other frame and joinery', 'Edges, connectors, stable condition, service access and replacement parts'],
['Outdoor furniture', 'Exact frame, finish, textile and loose components', 'Intended exposure, weather limits, approved care, drying and seasonal storage'],
]),
section('material-selection-record', 'Keep a fill-in selection record for every high-use surface',
'''Use a record per product or assembly, not one broad statement such as “all furniture is durable.” Attach the actual product documents and identify which version or finish was selected. If the supplier cannot confirm a promised property in writing, mark it unknown and resolve it before relying on it. Where a warranty excludes the intended use, record that limit rather than treating the product as warranted for the rental.''',
template='''MATERIAL AND PRODUCT SELECTION RECORD
Room / item / intended use: [location / item / actual activity]
Exact manufacturer / product / model / finish: [identifiers]
Supplier and dated specification: [document reference]
Intended-use and exposure limits: [manufacturer information]
Care label and approved process: [document reference]
Cleaning products/tools permitted and excluded: [manufacturer instructions]
Sample or trial location / date: [location / date]
Trial observations: [cleaning / finish / drying / access / fit]
Qualified specification or installation review: [person / scope / unresolved questions]
Repair method / replacement component availability: [confirmed information]
Warranty and intended-use limitations: [document reference / limits]
Full installed quote and service needs: [actual costs / scope]
Selected / rejected / pending: [decision and reason]
Approval owner / care owner / next review trigger: [people / event]'''),
section('material-cleaning-sample-trial', 'Run a controlled cleaning and reset trial',
'''Ask the supplier how to evaluate a sample without damaging it or invalidating its warranty. Use only the documented process for the exact material. A test on a hidden or spare sample can show practical handling and drying needs; it does not certify long-term performance or establish a safety rating. Do not transfer one brand’s fabric or surface instructions to a different product.

Record what the cleaner has to move, disassemble, carry, wash, dry, and reinstall. A removable rug or cover may be technically washable but difficult to process with the property’s actual machines and space. If a trial leaves the material damp, changes its appearance, or requires unavailable equipment, pause the selection and ask the supplier for a suitable alternative or process.''',
headers=['Trial step', 'Record', 'Decision question'], rows=[
['Prepare', 'Exact sample and written instructions; approved tools/products; test owner', 'Is the process authorized for this product?'],
['Observe care', 'Handling, access, removal, washing/cleaning and drying observations', 'Can the cleaner reproduce the process with the available resources?'],
['Inspect after drying', 'Finish, texture, seams, fit, visible residue and condition photos', 'Did the sample return to an acceptable condition?'],
['Compare repair', 'Supplier-approved repair, part availability and reorder identity', 'Can a damaged component be serviced without replacing the assembly?'],
['Approve or pause', 'Decision, limits, missing information and responsible person', 'What evidence must be resolved before ordering multiples?'],
]),
section('material-cost-and-maintenance', 'Compare installed cost and maintenance separately',
'''Replace generic price-per-square-foot tables with dated quotes for the exact installed scope. Include preparation, labor, freight, removal, and required finishing work where relevant. Keep predicted life or replacement timing clearly hypothetical until supported by records. The useful comparison is a transparent scenario, not a claim that a named material always saves money.''',
template='''MATERIAL COST COMPARISON
Option A / Option B: [exact products]
Product quote and date: [actual values]
Preparation / installation / freight / removal: [actual quoted scope]
Approved care process and staff/equipment needs: [documented process]
Repair/replacement parts and current quote: [confirmed information]
Assumed replacement scenario, if used: [explicitly hypothetical assumptions]
Unpriced items or unknowns: [questions and owner]
Reason for selection: [fit / care / serviceability / installed cost / other evidence]''',
items=[
'At each reset, observe condition and handle visible issues using the product’s approved process.',
'Keep manufacturer care documents available to the people doing the work.',
'Schedule maintenance from product instructions, condition and qualified advice rather than a universal quarterly treatment.',
'Record repairs, changed components and finish references so future replacements remain compatible.',
'Escalate unknown faults or unsuitable products to the responsible supplier or qualified provider; do not improvise a technical fix.',
]),
])

add('design-for-superhost', [
section('guest-use-room-audit', 'Audit the guest experience one activity at a time',
'''Design can address a practical problem, but it cannot establish a platform status or promise a rating. Use this audit to observe the installed property rather than to score likely reviews. Walk through as someone arriving for the first time, then repeat it with the people responsible for the reset. Distinguish a furnishing problem from a broken product, an inaccurate description, or missing instructions.

Record light, sound, odor, temperature, reach, comfort and storage as observations, including the time and conditions. A musty smell or an unfamiliar fault may need investigation by the responsible qualified provider rather than a decorative change. Do not assume that every complaint has a design solution.''',
headers=['Activity', 'Observe in the real setup', 'Record an actionable issue'], rows=[
['Arrival', 'Finding the entrance, seeing controls, opening doors and putting down luggage', 'Location, condition, exact confusion and responsible owner'],
['Bedroom use', 'Bed fit, reading controls, charging, curtains, luggage and linen condition', 'Actual bed position, time/lighting conditions and repeatable observation'],
['Bathroom use', 'Personal-item landing, supplied toiletries, towel drying and cleanability', 'Missing function, reset mismatch or mounting/service question'],
['Kitchen use', 'Finding utensils, using supplied equipment, dining and clearing up', 'Task the guest cannot complete and the exact item/instruction involved'],
['Living/work use', 'Usable seating, reachable light/power, screen glare and storage', 'Conflict between activities, not an assumed demographic preference'],
['Outdoor use', 'Actual available seating, shade controls, loose items and weather handoff', 'What is supplied, its operating limits and who resets it'],
['Departure/reset', 'Guest instructions, linen handling, missing items and cleaner access', 'An instruction or layout change that can be trialed and documented'],
]),
section('guest-feedback-triage-template', 'Copy the feedback and action log',
'''Use actual feedback that you are authorized to review, and avoid putting private guest records into a public design pack. Summarize the issue rather than making assumptions about a guest’s identity or preferences. A repeated observation may justify a trial change; it does not prove the cause of an overall score or the effect on bookings.''',
template='''GUEST FEEDBACK AND DESIGN ACTION LOG
Issue reference / date: [internal reference / date]
Observed activity or reported problem: [factual summary]
Room / exact furnishing or instruction: [location / item]
Evidence available: [test observation / condition photo / authorized feedback summary]
Evidence still missing: [question]
Category: [repair / layout / care/reset / information / technical investigation]
Immediate practical limit or concern: [what cannot be used or understood]
Proposed action and reason: [specific change tied to the observation]
Responsible person / approval / due date: [owner / approval / date]
Trial method: [repeat the same guest-use activity under recorded conditions]
Result and remaining issue: [observable result, not predicted rating uplift]
Listing/guide/reset information to update: [documents]
Follow-up date or trigger: [date / event]'''),
section('guest-feedback-priority-matrix', 'Prioritize by function, evidence and dependency',
'''Deal with unsafe, failed or unavailable functions through the appropriate response before considering cosmetic improvements. Then compare tasks by guest-use impact, confidence in the evidence, cost, access needs, and dependency. “Low cost” still needs a written scope and approval. Do not treat a decorative purchase as the automatic response to a poorly understood issue.''',
headers=['Priority group', 'Example of the decision', 'Acceptance evidence'], rows=[
['Qualified investigation or failed function', 'A reported fault needs the responsible provider; restrict assumptions about the cause', 'Relevant investigation/repair and operating instructions recorded'],
['Clear information/reset mismatch', 'Supplied linen or appliance instructions differ from the actual setup', 'Guide, listing and reset record agree with what is present'],
['Repeatable layout conflict', 'A chair or luggage position blocks another intended activity', 'The same activity trial works in the approved arrangement'],
['Care or replacement problem', 'A damaged component is repeatedly missed or cannot be cleaned in time', 'Care process, spare stock or approved replacement is usable'],
['Optional visual change', 'Aesthetic preference without a failed essential function', 'Approved scope, budget and maintainable reset; no outcome guarantee'],
]),
section('guest-feedback-closeout', 'Close the loop with a repeatable test',
'''Assign one person to reconcile the action log with the current inventory and room reset. Re-test the activity that triggered the change; “new product delivered” is not the same as “problem resolved.” Keep the original conditions visible when comparing results. Review a trial with the cleaner as well as the owner so an attractive change does not add an impractical reset burden.''',
items=[
'Confirm the replacement or changed instruction matches the exact installed product.',
'Repeat the guest-use trial and record the observable result or unresolved question.',
'Update accurate photographs, amenity descriptions and guest instructions when the supplied setup changes.',
'Retain the revised room reset and care record, and reconcile spare quantities.',
'Check the current platform’s official criteria separately if status questions matter; do not infer eligibility from a furnishing audit.',
]),
])

add('design-mistakes-kill-bookings', [
section('room-design-audit-matrix', 'Use a room-by-room problem and evidence checklist',
'''A design audit should explain what a guest cannot do, what the observer actually saw, and what would resolve the issue. It cannot show that a furnishing choice caused lost bookings without separate evidence. Start with the real setup at its intended capacity, including retained furniture, door swings, control locations, and the cleaner’s route. The table preserves the practical room checks without treating a taste preference as a measured commercial result.''',
headers=['Area', 'Common issue to test', 'Practical evidence and response'], rows=[
['Personal clutter and storage', 'Owner items or decorative objects occupy the space guests need', 'List the guest activity displaced; remove/relocate approved items and repeat the task'],
['Lighting', 'Controls cannot be found, task light is missing, or reflections interfere with use', 'Test arrival, reading, dining and overnight routes in actual nighttime conditions'],
['Furniture scale', 'The table fits only with chairs pushed in; sofa bed blocks another function when open', 'Draw and trial furniture in use; test doors, luggage and cleaning access'],
['Color and finishes', 'Samples look different under installed lights or conflict with retained fixed finishes', 'Compare physical samples in the room; record product/color/finish identities'],
['Photography styling', 'The photographed setup contains temporary furniture or unavailable amenities', 'Compare the image with the room reset and actual inventory; correct the representation'],
['Bedroom', 'Protector/sheets do not fit, personal items lack a surface, or curtains leave unwanted light gaps', 'Trial the complete bed system and nighttime controls before adding decoration'],
['Bathroom', 'No usable personal-item landing, towel drying is limited, or accessories are difficult to clean', 'Trial a realistic guest use and cleaner reset; confirm mounting/service scope'],
['Kitchen', 'Missing utensils, incompatible cookware, unclear controls or storage conflicts', 'Prepare and clear a simple supported meal with the provided inventory'],
['Outdoor/entry', 'Loose items lack a weather handoff or wet gear intrudes on the arrival route', 'Trial arrival and storage; document approved exposure limits and reset responsibility'],
]),
section('design-issue-card-template', 'Record each issue as a testable task',
'''One task card per issue keeps a vague “refresh the room” request from becoming an unrelated shopping exercise. A good card names the activity, the conflict, the retained constraints, the smallest sensible trial, and the person who can accept the result. Separate an observation from a possible cause. For example, “the end dining chair hits the door” is an observation; “the table is the wrong shape” is a hypothesis to test.''',
template='''FUNCTIONAL DESIGN ISSUE CARD
Room / issue reference / date: [room / reference / date]
Activity and conditions: [arrival / dining / sleeping / cleaning / other]
What was observed: [specific conflict or missing function]
Evidence: [measured sketch / photo / condition test / reset observation]
What is uncertain: [unconfirmed cause or dimension]
Retained constraints: [fixed items / doors / budget / product requirements]
Trial change: [rearrangement / sample / instruction / repair investigation]
Technical review required: [question / qualified person]
Actual complete cost or quote needed: [known cost / unknown scope]
Decision and approval owner: [person]
Acceptance test: [repeatable activity and observable result]
Reset, inventory and photo updates: [documents to revise]
Open items and follow-up: [owner / date]'''),
section('design-audit-walkthrough', 'Run a realistic walkthrough before approving the change',
'''Use the same route a guest will follow, beginning with arrival and continuing through the essential room activities. Open doors and convertible furniture rather than assessing an empty room. Repeat the inspection with lights in their actual operating states. Where a safety or regulated requirement is involved, record the question for the responsible qualified provider; a taped-floor trial cannot establish compliance.

Invite the cleaner to show how linen moves, rugs are handled, and surfaces are reached. A layout can appear generous while requiring furniture to be moved every reset. Test a new arrangement before ordering a replacement. If the smallest trial creates a different conflict, return to the recorded constraints rather than forcing the first idea through.''',
items=[
'Arrival: luggage can be set down while the supplied entrance and controls are used.',
'Dining: chairs and table are tested at the actual intended seated capacity.',
'Sleeping: all beds, convertible beds, curtains and bedside functions are tested in use.',
'Storage: luggage, clothes and supplied amenities have an identifiable reset position.',
'Kitchen/bathroom: the intended guest tasks can be completed using actual supplies.',
'Cleaning: the cleaner can reach and process the areas and textiles in the installed layout.',
'Photographs/instructions: the documented setup matches the accepted arrangement.',
]),
section('design-audit-action-order', 'Turn observations into an ordered improvement plan',
'''Keep failures and technical questions ahead of optional aesthetic changes. For each approved task, record its owner, complete scope, dependencies and evidence of completion. Group tasks when the same access visit or supplier is required, but do not hide unresolved decisions inside a larger purchase. The final record should show why each change was selected and which activity it improves, without claiming a booking effect.''',
headers=['Sequence', 'Required output', 'Before moving on'], rows=[
['Observe and document', 'Issue cards with measured facts and unresolved questions', 'Confirm which functions are actually affected'],
['Investigate and trial', 'Relevant provider review or a reversible layout/sample trial', 'Record the result and any new conflict'],
['Approve scope and cost', 'Exact selection/repair/instruction change and full cost', 'Resolve fit, care, installation and approval responsibility'],
['Implement and re-test', 'Delivered task plus repeat of the original activity', 'Close remaining defects and update the reset'],
['Maintain the record', 'Revised inventory, photographs, care and instructions', 'Keep the accepted setup reproducible for future changes'],
]),
])

add('insurance-friendly-design', [
section('insurance-record-pack', 'Prepare a furnishing record pack for the actual insurance review',
'''Use this guide to organize information for your qualified insurance adviser and relevant service providers. It does not determine coverage, establish compliance, prescribe inspection intervals, or promise a premium reduction. Describe the actual short-term rental use accurately when obtaining advice. Ask the adviser what evidence and policy questions matter for this property, rather than assuming that a furniture or security purchase changes the insurance position.

Keep one index linking the current room inventory, product specifications, installation documents, receipts, condition photographs, and maintenance records. Retain actual paid costs and dated replacement quotes as different fields. Do not present a generic online price as the amount your policy would reimburse. The adviser’s requirements govern the records needed for a particular review or claim.''',
headers=['Record group', 'Useful documents to organize', 'Question for the responsible adviser/provider'], rows=[
['Property and actual use', 'Current property description, rental operation, amenities and relevant changes', 'What use and features need to be disclosed or reviewed?'],
['Furnishing inventory', 'Room, item/model, quantity, purchase date, receipt and condition photos', 'What inventory evidence or valuation information is required?'],
['Materials and installation', 'Exact product specifications, intended-use limits, installation scope and relevant provider records', 'Which technical questions or documentation need qualified review?'],
['Maintenance and repairs', 'Fault reports, inspection/service documents, invoices and completion evidence', 'What process and records are appropriate to the actual products and property?'],
['Special amenities', 'Documents for any supplied pool, balcony, outdoor, cooking or other relevant feature', 'What exclusions, conditions or separate requirements apply?'],
['Policy and adviser record', 'Current documents, contact details, questions and written responses', 'Which proposed changes need approval or clarification before implementation?'],
]),
section('insurance-inventory-template', 'Copy the inventory and document index',
'''Photograph the current item and its identifying details where available, and keep the receipt or supplier record with the same identifier. Record retained items honestly when receipts or dates are missing. Store the pack in an appropriately controlled location with a backup separate from the property, and confirm that the person who will need it can retrieve it. These records support an organized conversation; they do not guarantee claim acceptance or a particular settlement.''',
template='''FURNISHING INVENTORY FOR INSURANCE REVIEW
Property / room / record identifier: [property / room / ID]
Item, model, finish and serial number where available: [actual identifiers]
Quantity and installed location: [quantity / location]
Purchase date / supplier / receipt reference: [known facts or unknown]
Amount paid: [actual receipt amount]
Dated replacement quote, if requested: [separate quote reference]
Current condition photo references: [files / date]
Installation and relevant qualified-provider documents: [references]
Product care, warranty and intended-use limitations: [documents]
Maintenance/repair history reference: [log]
Insurance adviser question / written response: [question / response reference]
Missing information / responsible person / next action: [gap / owner / task]'''),
section('insurance-review-question-list', 'Discuss design-related questions without assuming coverage',
'''A room or surface choice may raise practical questions that deserve technical review. Document the exact proposed product, its intended use, and the work being contemplated. Ask the qualified provider to address relevant requirements rather than labelling a material “insurance friendly,” “non-slip,” or “fireproof” on the strength of a marketing description.''',
headers=['Area to discuss', 'Facts to bring', 'Question to record'], rows=[
['Floors, wet areas and stairs', 'Exact surfaces, transitions, product information and installation documents', 'What relevant specification, maintenance or qualified inspection is needed?'],
['Furniture and mounting', 'Product identifiers, condition, mounting instructions and intended room use', 'Who should confirm installation and suitability for the intended use?'],
['Cooking and supplied equipment', 'Actual appliances, installation/service records and operating instructions', 'Which technical or insurance questions remain unresolved?'],
['Water or moisture issues', 'Observed issue, location, photographs and relevant provider assessment', 'Who investigates the cause and records the completed work?'],
['Family-oriented amenities', 'Exact supplied products and intended users/use', 'What suitability review, instructions or restrictions need confirmation?'],
['Outdoor, pool or balcony features', 'Actual amenities, service records, relevant property constraints and operating limits', 'Which policy or qualified-provider requirements apply to these features?'],
['Security/access changes', 'The specific proposed change and its documented purpose', 'Is any adviser or provider review required? Do not assume a discount.'],
]),
section('insurance-maintenance-log', 'Maintain a factual service and follow-up log',
'''Set schedules from the relevant instructions and qualified advice, then record the work actually done. Avoid a universal annual inspection promise for every system or a blanket quarterly replacement rule. A record should distinguish reported, inspected, repaired, tested, and still open. Close a task only when the responsible person has documented its completion within their scope.''',
template='''PROPERTY SERVICE AND FOLLOW-UP LOG
Date / property / item or system: [date / property / item]
Trigger: [product schedule / observed fault / provider advice / other]
Observation or reported issue: [facts and evidence]
Responsible provider and scope: [person / qualifications or service role / scope]
Assessment or work reference: [report / invoice / document]
Work performed and completion date: [actual completed work]
Test or acceptance evidence: [documented result within the provider's scope]
Restrictions or open issues: [unresolved items]
Next review trigger / date and responsible person: [trigger / person]
Insurance-adviser update required: [question / owner / response reference]'''),
section('insurance-incident-record', 'Know where to find the applicable incident instructions',
'''Keep the current adviser, insurer, property contact and relevant emergency instructions accessible through the approved operating process. If damage or an incident occurs, follow applicable emergency and policy instructions and seek the appropriate qualified help. Record factual observations and communications when it is appropriate to do so; do not use this template to invent notification deadlines, coverage, liability conclusions, or settlement amounts.''',
items=[
'Know who holds the current policy documents and who is authorized to communicate about them.',
'Locate the actual incident/reporting instructions before a problem occurs.',
'Record dates, observed condition, document references and the people handling the issue.',
'Distinguish an observed fault from an unconfirmed cause or insurance conclusion.',
'Retain relevant communications and completed-work records in the controlled property pack.',
'Ask the qualified adviser what further evidence or action is required for the specific circumstances.',
]),
])

add('photography-staging-guide', [
section('photo-preparation-checklist', 'Prepare the actual guest setup before the shoot',
'''Use a preparation checklist and a room shot list rather than a collection of styling tricks. The photographs should help a guest understand the space and the amenities actually available. Temporary props, furniture, or views that materially change the represented setup can make the images inaccurate. Record the accepted room reset before photography so the team knows what belongs in the final frame.

Reserve access for the agreed photography scope and resolve readiness issues before arrival. Schedule according to the property’s actual light, access and weather constraints, with the photographer’s advice. Do not assume a universal time of day, two-hour session, or a fixed camera setting will suit every room.''',
items=[
'Confirm the supplied furniture, linens, amenities and controls match the current inventory and listing scope.',
'Complete the room reset and remove private paperwork, access credentials and owner items from the photographed areas.',
'Check visible condition, glass, mirrors, linens and other surfaces using the appropriate care process.',
'Confirm supplied lighting works and identify reflections or mixed-light issues for the photographer to evaluate.',
'Open the actual storage, doors and convertible arrangements needed to document guest functions.',
'Prepare a list of essential room views, useful detail views and any relevant limits that need clear representation.',
'Agree access, readiness, weather contingency, deliverables, usage rights and file handover with the photographer.',
'Keep one person responsible for checking the images against the room reset before approval.',
]),
section('room-photo-shot-list', 'Build a room-by-room shot list',
'''A wide view gives context, while a useful detail view explains a guest function. Do not use a lens or edit to imply that a room is larger, an amenity is present, or a view is available when that would misrepresent the actual property. Ask the photographer how to capture the necessary context without losing the information a guest needs.''',
headers=['Area', 'Context view', 'Useful detail or second view', 'Accuracy check'], rows=[
['Arrival/entry', 'Actual entrance and luggage/coat landing where relevant', 'Usable storage or control location without exposing access credentials', 'The shown entrance and route are the ones guests use'],
['Living room', 'Relationship between seating, tables, doors and supplied entertainment', 'Reading light, personal-item surface or another actual guest function', 'Seating and movement remain representative of the reset'],
['Dining', 'Table and available seating in their usable arrangement', 'Connection to the kitchen or outdoor dining where supplied', 'Do not use extra temporary seats or hide a conflicting door'],
['Kitchen', 'Work area, supplied appliances and storage context', 'Coffee setup, cookware/dishware storage or a clear functional detail', 'Included equipment and consumables match the actual allocation'],
['Bedrooms', 'Every supplied sleeping room with its complete bed setup', 'Luggage/clothes storage, bedside controls or a convertible bed arrangement', 'Show actual bed sizes and available functions accurately'],
['Bathrooms', 'Actual bathroom arrangement and available surfaces', 'Towel drying, storage or supplied toiletries where useful', 'Do not stage products or amenities that are unavailable to guests'],
['Work/storage', 'Actual workspace or guest storage in context, if offered', 'Power, lighting and usable chair/surface arrangement', 'The photographed setup is available throughout the described stay'],
['Outdoor spaces', 'The guest-accessible seating/dining arrangement and relevant context', 'Shade or another actual supplied function', 'Seasonal/weather availability and property limits are represented accurately'],
]),
section('photographer-brief-template', 'Copy the photography brief and deliverables record',
'''Use a written brief to agree the scope, the representation standard, the required files and the approval process. Choose a professional based on relevant examples and a clear proposal rather than an unverified booking-conversion claim. If using a phone or your own camera, the same shot list and acceptance checks still apply.''',
template='''RENTAL PHOTOGRAPHY BRIEF
Property / approved room-reset version: [name / version]
Rooms and guest-accessible areas to cover: [list]
Essential context/detail views: [shot-list references]
Convertible, seasonal or conditional arrangements: [what needs accurate explanation]
Private or excluded areas/details: [areas / credentials / owner items]
Shoot access and readiness owner: [date/access arrangements / person]
Light/weather constraints and contingency: [observations / agreed plan]
Representation standard: [accurate supplied setup; no fabricated features/views]
Editing scope and exclusions: [agreed corrections / prohibited changes]
Required master and platform-export files: [formats/specifications confirmed at handover]
Usage rights and agreement reference: [written agreement]
Delivery, revision and approval process: [dates / owner / included revisions]
Current platform requirements checked by/date: [person / date / official reference]
Final image-to-inventory check: [owner / result / unresolved issues]'''),
section('photo-light-composition-review', 'Evaluate light, framing and editing against the room',
'''Clean the lens, stabilize the camera appropriately, and take a test image before the main sequence. Review whether bright and shaded areas retain the information the guest needs. Compare straight room edges, surface colors, reflections and relevant views against the actual property. Ask the photographer to choose suitable exposure, equipment and technique for the conditions; do not apply fixed ISO, shutter or ultra-wide settings as a universal recipe.

Correcting an exposure or a color cast can help the image represent the room, but edits should not add or remove material property features. Keep master files and distinguish a platform crop from a change to the represented scene. Review cover crops at the current upload preview so important room information is not accidentally cut off. Generic historical pixel counts or platform-ranking assertions are not current requirements.''',
items=[
'Check that the framing explains the space rather than hiding an essential limitation.',
'Compare the edited wall, textile and finish colors with the installed products under the relevant light.',
'Keep private access details, account screens and sensitive records out of the image.',
'Preserve material features, views and supplied amenities accurately through editing.',
'Use current official platform guidance and the actual upload preview for dimensions, supported formats and crops.',
'Retain the original/master files, exports, usage agreement and final approval record.',
]),
section('photo-acceptance-record', 'Accept and update the photographs systematically',
'''Review the delivered set room by room against the shot list, current inventory and written brief. Note missing rooms, unclear functions, inaccurate props, unsuitable crops and unresolved editing questions before uploading. After a furnishing or seasonal availability change, identify which images need review. A photo refresh should be driven by an actual change or an identified representation problem, not a promised platform advantage.''',
headers=['Check', 'Record', 'Owner action'], rows=[
['Coverage', 'Required views delivered, missing views and room identifiers', 'Resolve missing information with the photographer'],
['Representation', 'Image agrees with actual furniture, amenities, views and seasonal limits', 'Correct the image or actual description before publication'],
['Technical handover', 'Masters, exports, agreed rights and revision scope supplied', 'File the handover documents and confirm current upload requirements'],
['Platform preview', 'Important context survives the actual cover/detail crops', 'Select a suitable export/crop without altering the represented property'],
['Future changes', 'Inventory or reset change that affects an image', 'Assign a review owner and retain the accepted current set'],
]),
])

add('seasonal-decor-calendar', [
section('seasonal-calendar-setup', 'Adapt the calendar to local conditions and actual availability',
'''The month-by-month calendar below is a planning example using a Northern Hemisphere seasonal sequence. Shift it for the property’s climate, operating season, hemisphere, local constraints, and actual guest setup. Optional decoration is secondary to functioning furniture, suitable textiles, clean storage and an accurate listing. A calendar task is complete when its owner records the check; the date alone does not show that the property is ready.

Keep a stable year-round base and a small, documented set of optional seasonal items. Choose changes that the cleaner can count, place, care for and store. Do not assume a holiday theme suits every guest, and do not promise review mentions or increased bookings from a seasonal swap. Avoid adding scents or temporary features without an explicit operating decision and an appropriate review of the actual product/use.'''),
section('month-by-month-calendar', 'Copy the month-by-month furnishing calendar',
'''Use each row as a prompt for a local operating plan. Assign an owner, set a suitable date or condition trigger, and record the outcome. Replace optional visual changes with the property’s approved setup; keep unavailable amenities out of the listing and guest guide.''',
headers=['Month', 'Example condition/reset focus', 'Optional visual change', 'Owner record'], rows=[
['January', 'Reconcile inventory after the busy period; review wear and storage', 'Return to the documented neutral base if holiday items were used', 'Missing/damaged item log; outgoing-bin contents'],
['February', 'Check nighttime lighting, linens and climate-control instructions', 'Trial a small compatible textile change if useful', 'Exact product/care record; reset photo'],
['March', 'Inspect outdoor stored items before planned reopening', 'Prepare approved outdoor pieces after condition/drying checks', 'Readiness questions; parts and care tasks'],
['April', 'Review arrival route, wet-gear handling and outdoor availability', 'Use a limited maintained plant or accessory only if the operating plan supports it', 'Actual availability; care owner; photo review'],
['May', 'Confirm shade, outdoor seating, cushion storage and guest instructions', 'Coordinate optional outdoor textiles with their approved care', 'Exposure limits; loose-item inventory; reset plan'],
['June', 'Trial outdoor dining and indoor/outdoor transitions', 'Keep summer decoration manageable and documented', 'Guest-use trial; storage/cleaning notes'],
['July', 'Observe high-use furniture and available working stock', 'Replace a worn optional item only after approving the exact specification', 'Condition and reorder record; full installed cost'],
['August', 'Review towel drying, laundry capacity and outdoor cushion condition', 'Retain useful seasonal items rather than swapping automatically', 'Laundry/condition log; unresolved issues'],
['September', 'Plan the next weather/storage handoff and inspect spare parts', 'Trial an appropriate textile change against the actual room', 'Approved change; storage capacity; reset photo'],
['October', 'Review lower-light arrival and night controls; prepare relevant seasonal storage', 'Use optional seasonal accents only if approved and easily reset', 'Control check; loose-item and bin record'],
['November', 'Confirm indoor guest capacity, dining function and linen working stock', 'Keep any seasonal table decoration out of functional guest space', 'Full-capacity trial; actual supplied inventory'],
['December', 'Record any approved holiday setup, safe installation review and removal owner', 'Keep themes optional and consistent with the actual property/guest brief', 'Installation/review questions; outgoing date; reference photos'],
]),
section('seasonal-swap-kit', 'Build an identified swap kit with a complete return plan',
'''Use one labelled kit per approved arrangement, with a contents list and reference photographs. Separate clean, dry incoming items from outgoing pieces awaiting care. Mark incomplete kits clearly so a cleaner does not improvise with mismatched or damaged components. Storage should suit the exact product instructions and allow inspection before the next use.

A swap kit does not guarantee a fifteen-minute task. Observe an actual swap and record preparation, cleaning, drying, carrying, placement and packing separately. Include the tasks that happen outside the room. If the process is too large for the available changeover time, simplify the optional setup rather than assuming the team will move faster.''',
template='''SEASONAL SWAP KIT CARD
Property / arrangement / kit identifier: [name / arrangement / ID]
Approved use dates or condition trigger: [dates / weather or operating trigger]
Incoming contents and exact quantities: [item / model / quantity]
Outgoing contents and exact quantities: [item / quantity]
Storage locations and product care documents: [locations / references]
Preparation required before placement: [cleaning / drying / inspection]
Placement sequence and reference photo IDs: [steps / photos]
Required qualified review or installation: [scope / provider / approval]
Outgoing care, inspection and packing sequence: [steps]
Missing/damaged items and action owner: [issue / person]
Observed working time and access needs: [actual trial record]
Reset owner / checker / completion record: [people / date]
Listing/photos/guest guide to update: [records affected]'''),
section('seasonal-budget-storage', 'Budget and store optional items as a separate scope',
'''Keep seasonal spending visible instead of mixing it into essential repairs. Record the actual item price and the care, handling, storage, installation and disposal costs that accompany it. Reuse suitable items when the condition and approved care support it. An inexpensive accessory that repeatedly requires cleaning or cannot be stored properly may be a poor operational choice even when its purchase price is low.''',
headers=['Decision', 'Record', 'Question before approval'], rows=[
['Purchase', 'Exact item, quantity, complete cost and intended seasonal use', 'Which actual guest or operational need does it address?'],
['Care', 'Manufacturer process, drying and cleaner resources', 'Can the item be returned to an acceptable reset condition?'],
['Storage', 'Labelled location, capacity, suitable conditions and contents list', 'Can the complete clean kit be stored and retrieved?'],
['Installation', 'Relevant product instructions and qualified review/scope where needed', 'Who approves and completes the work?'],
['Removal', 'Owner, trigger/date, inspection and care sequence', 'Where does the outgoing item go and what happens to damage?'],
['Representation', 'Actual seasonal availability and affected images/instructions', 'Does the listing still describe what guests receive?'],
]),
section('seasonal-turnover-instructions', 'Hand the calendar to the people doing the reset',
'''Use a versioned instruction card at the point of work. Show what comes out, what goes in, where each piece belongs, and where outgoing pieces are stored or sent for care. Review the kit with the cleaner before the first swap. If the property is occupied or a product is not ready, record the changed plan and keep the guest description accurate.''',
items=[
'Agree the calendar or condition trigger with the operating team and identify the decision owner.',
'Inspect the incoming kit before the planned access window and resolve missing components.',
'Use approved placement photos and exact quantities; avoid adding improvised decoration.',
'Record outgoing condition, complete care/drying, and store pieces according to their instructions.',
'Reconcile bins and mark incomplete kits before closing the task.',
'Update reset records, guest instructions and listing photographs where the supplied setup changes.',
]),
])

add('ultimate-guide-str-design', [
section('project-stage-gates', 'Follow the project from survey to usable handover',
'''A complete rental design project joins scope, measurement, room function, product selection, cost, delivery, installation, care and guest communication. Use the stage gates below to see what has to exist before the next commitment. Revisit an affected gate after a substitution or scope change. Do not treat a mood board or a delivered sofa as evidence that the whole property is ready.

Use aesthetic references to describe intent, then test the intent against the actual space and operation. The goal is an arrangement the guest can use and the team can maintain. Claims about revenue lift, payback or guest ratings need separate evidence and are not acceptance criteria in this planning guide.''',
headers=['Stage', 'Required output', 'Decision before proceeding'], rows=[
['Survey and retained inventory', 'Measured plan, annotated photos, condition records and delivery-route questions', 'Which facts are confirmed, and which items can remain?'],
['Guest-function scope', 'Room activities, usable capacity, essential/optional list and technical-review needs', 'What must the property actually support?'],
['Layout and references', 'Furniture-in-use plan, trial results, retained finishes and labelled aesthetic references', 'Does the arrangement support the intended activities and care?'],
['Specification and cost', 'Exact products, care requirements, complete installed quotes and separate contingency', 'Are fit, serviceability, scope and cost understood?'],
['Procurement', 'Approved orders, stock confirmation, substitution rules and order tracking', 'What has been committed and who resolves changes?'],
['Receiving and installation', 'Ready rooms, confirmed access, inspected deliveries and relevant qualified work', 'Do received products match approved selections and actual constraints?'],
['Guest-use and reset trial', 'Arrival-to-bed test, full dining/sleeping use, cleaner/laundry trial and defects log', 'Which functions or records remain unresolved?'],
['Photography and handover', 'Accurate images, current inventory, care/warranty pack, instructions and acceptance record', 'Can the operating team reproduce and maintain the delivered setup?'],
]),
section('project-room-by-room', 'Plan each room around function, comfort and reset',
'''Apply the same measured process to every room, but do not buy the same list for every property. A compact apartment, a family-oriented house and a seasonal outdoor space have different activity conflicts and care resources. Keep permitted occupancy and relevant technical requirements separate from your furnishing capacity trial.''',
headers=['Room/area', 'Essential planning questions', 'Acceptance trial'], rows=[
['Entry', 'Where do bags, shoes and wet gear go? Can the entrance and supplied controls be used?', 'Walk arrival with the intended luggage and actual door operation'],
['Living room', 'Are seats, personal-item surfaces, light, screen position and storage usable together?', 'Use the seats, controls and doors; open any supplied convertible bed'],
['Dining/kitchen', 'Can the intended group sit, prepare a supported meal and clear up with actual supplies?', 'Pull out chairs; trial cookware, utensils, appliance instructions and storage'],
['Bedrooms', 'Does each complete bed system fit? Are curtains, light, power and luggage functions usable?', 'Make and use each bed; test bedside reach and actual nighttime light gaps'],
['Bathrooms', 'Can guests place personal items, use supplied amenities and dry towels? Can the cleaner reach surfaces?', 'Trial use and reset with the actual towel/toiletry allocation'],
['Work or multi-use zone', 'Does work conflict with dining, sleeping or power/control access?', 'Use the chair, surface and lighting during the other planned room activities'],
['Outdoor spaces', 'Which activities are realistic under product exposure limits and property constraints?', 'Trial seating/dining and the weather/storage handoff with responsible people'],
['Utility/owner storage', 'Can laundry, supplies and spare parts be processed and stored without disrupting guest space?', 'Walk a real reset, linen return and spare-item retrieval'],
]),
section('project-material-care-system', 'Connect materials to the operating system',
'''Inspect the exact product and assembly, not only its aesthetic or a generic material label. Useful decisions include fabric care, rug handling, paint records, tabletop finishes, replaceable covers, cushion parts and stable furniture condition. Ask for intended-use limits and written warranty/care information. Keep product-specific technical specification and installation with qualified providers.

Treat laundry and cleaning capacity as part of the specification. A washable item still needs a compatible approved process, sufficient drying and suitable clean storage. Agree the reset with the cleaner before multiplying an attractive but awkward textile across rooms. Maintain a product register that allows the team to identify the exact replacement component after a failure.''',
items=[
'Compare physical finish/fabric samples in the installed light and with retained surfaces.',
'Read exact intended-use, care and warranty documents and identify missing information.',
'Trial handling, cleaning and drying through the resources the operation actually has.',
'Record product identifiers, approved care, spare components and current reorder information.',
'Document qualified-review questions and approved installation responsibilities.',
'Accept maintainable function and condition rather than a promise that a material is indestructible.',
]),
section('project-budget-worksheet', 'Build a transparent budget rather than an ROI promise',
'''Start with available funds and confirmed scope. Product totals alone omit receiving, delivery, assembly, installation, disposal, tax and operating setup. Separate contingency from optional decoration and a longer-term replacement reserve. Compare actual quotes on the same inclusions and identify unpriced work. A budget tier is a chosen allowance for this project, not evidence of a universal market cost or rental-return forecast.''',
template='''COMPLETE FURNISHING PROJECT BUDGET
Project / scope version / date: [name / version / date]
Available funds and approval owner: [actual amount / person]
Retained items and approved repairs: [inventory / actual repair quotes]
Furniture and required components: [itemized actual quote references]
Textiles, kitchen and bathroom supplies: [itemized actual quote references]
Lighting/window items and relevant qualified work: [approved scope/quotes]
Outdoor items and weather/storage needs: [approved scope/quotes]
Design, sourcing and procurement fees: [written proposal]
Freight, receiving, access and temporary storage: [confirmed scope/quotes]
Assembly, installation, disposal and final cleaning: [confirmed scope/quotes]
Tax or other actual applicable charges: [confirmed amounts]
Photography and handover scope: [written proposal]
Separate contingency and approval rules: [explicit project allowance]
Optional work that can be deferred: [items / decision trigger]
Unpriced items and open questions: [scope / owner / due date]
Approved total and funds remaining: [reconciled actual amounts]
Any illustrative scenario: [clearly labelled assumptions, not a revenue prediction]'''),
section('project-critical-path', 'Coordinate procurement and installation through actual dependencies',
'''Track each item’s selection, approval, stock, shipment, receipt and placement separately. A vendor’s stock statement is not the same as a confirmed delivery appointment. Check packaged and assembled dimensions against the full route, including turns, stairs, elevators and relevant access arrangements. Assign receiving responsibility and follow each vendor’s actual discrepancy/return process.

Approve substitutions before they change fit, care, appearance, cost or delivery scope. Hold the room readiness review before furniture arrives, then reconcile received condition and missing parts. Plan the final reset and photography after unresolved guest functions are addressed. Dates should come from these dependencies rather than an unsupported universal launch duration.''',
headers=['Dependency', 'Record', 'Owner action'], rows=[
['Room readiness', 'Completed relevant work, clear access and usable installation conditions', 'Confirm readiness with the responsible providers'],
['Orders and stock', 'Exact approved product, vendor confirmation and order reference', 'Identify unavailable items and obtain substitution approval'],
['Delivery route', 'Packaged/assembled dimensions, route survey and provider handling plan', 'Resolve uncertain turns, access rules and receiving arrangements'],
['Receiving', 'Counts, identifiers, condition photos and discrepancy deadlines/process', 'Follow the vendor’s actual terms and assign unresolved issues'],
['Install and trial', 'Placement, assembly/qualified work and guest/cleaner-use tests', 'Re-test affected decisions and close documented defects'],
['Handover', 'Current records and operating-team acceptance', 'Assign follow-up owners for anything still open'],
]),
section('project-photography-and-guest-guide', 'Describe what the guest will actually receive',
'''Photograph the accepted room reset and use a shot list that explains bedrooms, bathrooms, storage, dining, arrival and other actual guest functions. Keep temporary props, unavailable seasonal features and private credentials out of published images. Use current official platform guidance and upload previews when preparing export files rather than relying on historical image-size or ranking claims.

Write guest instructions from a real test stay. Record where controls, supplies and storage are, and use manufacturer instructions for actual equipment. A welcome book needs a usable arrival message, property-specific rules, appliance directions, local recommendations verified by the operator, and the approved contact/emergency information. Keep a concise printed reference available if a digital guide depends on connectivity, and reconcile both versions after changes.'''),
section('project-maintenance-seasonal-closeout', 'Hand over maintenance and seasonal decisions with owners',
'''Deliver the inventory, product/care register, warranties, spare records, reset photographs, guest instructions and unresolved-issue log as one indexed pack. Identify who updates each record. Review seasonally available furniture and décor against condition, care, storage and actual listing availability. Optional visual changes need a countable swap kit and an owner rather than an assumed review or booking benefit.

Use later feedback to identify repair, layout, care/reset, information or technical-investigation tasks. Re-test a relevant guest activity after a change. Keep a factual record of what was observed and accepted. An operating history can improve the next design decision without implying that a particular purchase guarantees a commercial outcome.''',
template='''PROJECT ACCEPTANCE AND HANDOVER
Property / scope and inventory version: [name / versions]
Guest-use and cleaner/laundry trials: [date / records / result]
Installed products, care and warranty pack: [index reference]
Spare stock and reorder information: [record/location]
Reset photos and current guest instructions: [versions]
Accurate photography and listing review: [approval reference]
Qualified-provider work and remaining questions: [records / open items]
Unresolved defects or missing items: [issue / owner / due date]
Seasonal/weather handoff and storage: [record / responsible person]
Operating-team acceptance: [person / date / conditions]
Next review trigger: [event / date / owner]'''),
])

add('welcome-book-template', [
section('welcome-message-template', 'Copy the welcome message and property overview',
'''Replace every bracketed field with verified property information before sharing the guide. Remove any optional sentence that is not true for the rental. Keep a welcoming introduction short enough that guests can quickly find the practical details. The example does not assume a view, amenity, location, or service that the property lacks.''',
template='''WELCOME TO [PROPERTY NAME]
Welcome, and thank you for staying with us. We hope you enjoy your time at [property name].

This guide explains the arrival process, supplied equipment, house guidelines and checkout steps for this property. Start with [location/link of the quick-reference page].

You can find [actual supplied feature or essential item] at [verified location]. [Delete this sentence if unnecessary.]

For a question during your stay, use [approved host contact method]. Our normal contact availability is [actual arrangement]. For an urgent or emergency situation, follow the property’s verified emergency information at [location in guide].

Please let us know through [approved contact method] if something in the supplied setup differs from this guide.
Enjoy your stay,
[Host or property team name]'''),
section('arrival-checkout-templates', 'Copy the check-in and checkout instruction blocks',
'''Write these instructions after following the route yourself. Separate arrival information that may contain private access details from publicly shareable property description. Share access credentials only through the approved guest process. Include the actual luggage, parking and entrance arrangements, and test whether the instructions can be understood on a phone before arrival.''',
template='''CHECK-IN QUICK REFERENCE
Property name and arrival location: [verified guest arrival location]
Check-in date/time arrangement: [actual confirmed arrangement]
Parking or arrival instructions: [actual permitted arrangement and relevant limits]
Entrance and route: [plain description tested on site]
Access instructions: [provided separately through the approved guest channel]
Where to place luggage or wet gear: [actual location]
First-night essentials: [light/climate controls / towels / bedding / guide location]
If an arrival step does not work: [approved contact process]

CHECKOUT QUICK REFERENCE
Checkout date/time arrangement: [actual confirmed arrangement]
Required checkout tasks: [only the actual communicated tasks]
Used towels/linens: [actual location or instructions]
Waste/recycling: [verified process, locations and applicable instructions]
Appliances and climate controls: [manufacturer-aligned property instructions]
Keys/access and departure: [approved process, with private details shared appropriately]
Final personal-item check: [suggested places to check]
Issue or forgotten item: [approved contact process]
Thank you for staying at [property name].'''),
section('house-rules-template', 'Copy a property-specific house-rules template',
'''Populate this block from the actual rules and arrangements already established for the property. The template does not create a policy, determine local requirements, or prescribe a universal quiet hour, pet rule or occupancy limit. Check that the guest guide and listing agree, and ask the relevant adviser or property authority when a requirement is uncertain.''',
template='''HOUSE GUIDELINES FOR [PROPERTY NAME]
Guest capacity and permitted visitors: [actual established arrangement]
Quiet/noise expectations: [actual applicable hours and instructions]
Parking: [actual permitted spaces, access route and restrictions]
Smoking/vaping: [actual established rule and any applicable locations]
Pets or animals: [actual established arrangement; do not invent a fee or permission]
Use of indoor/outdoor amenities: [actual operating limits and instructions]
Seasonal or weather limitations: [actual features and conditions]
Care of furnishings: [clear product-appropriate instructions for guest tasks]
Waste and recycling: [verified local/property process]
Owner-only areas or supplies: [actual boundaries and clear labels]
If damage, a fault or a question arises: [approved contact process]
Other applicable property-specific rules: [verified rules only]'''),
section('wifi-appliance-template', 'Copy the connectivity and equipment instruction page',
'''Keep network credentials and access codes in the appropriate guest-only version. Public worksheets contain placeholders. For appliances, write directions for the exact installed model and have the responsible person test the steps. Avoid substituting generic operating or safety instructions for the manufacturer’s directions. Identify where the real manual is available and how a guest can ask for help.''',
template='''CONNECTIVITY AND EQUIPMENT
Wi-Fi connection: [guest network and credentials supplied through the approved private guide]
Connection help: [verified basic property instructions / approved contact]
Supplied television or entertainment setup: [actual setup / guest account process / controls]

EQUIPMENT CARD — repeat for each supplied appliance
Equipment name / exact model: [actual item]
Location of controls: [verified location]
Basic guest task: [task the equipment is supplied to support]
Tested operating steps: [manufacturer-aligned steps for this exact model]
Relevant operating limits: [actual product instructions]
Manual location or approved reference: [document location]
After-use instructions: [actual property/product process]
Fault or unclear operation: [approved help/contact process]'''),
section('local-emergency-reference', 'Maintain local recommendations and verified emergency information',
'''Use a short list of relevant recommendations that the operator can verify. Record the business name, location, official contact/reference, date checked and any property-specific travel notes actually known. Avoid presenting a venue as always open or inventing a travel time. Distinguish a personal suggestion from an included amenity or guaranteed service.

Maintain the emergency page with the people responsible for the property’s operating process. Use verified local information and applicable instructions; do not copy an emergency number or procedure from another jurisdiction. Keep the guest arrival location, approved urgent contact and relevant equipment/instruction locations accurate. Review this page after a contact or operating change.''',
template='''LOCAL RECOMMENDATION RECORD
Name and type: [business/place / activity]
Official location/contact/reference: [verified details]
Reason for including it: [relevant factual feature or clearly labelled personal suggestion]
Hours/reservation or access information: [verified reference, not a guarantee]
Date checked / person: [date / person]

PROPERTY EMERGENCY QUICK REFERENCE
Verified property/guest arrival address or location: [actual location]
Relevant verified local emergency contact information: [information checked for this jurisdiction]
Approved property urgent contact and process: [actual arrangement]
Relevant equipment/instruction locations: [actual documented locations]
Applicable directions reviewed by/date: [responsible person / date]
Information that must be kept in the controlled guest version: [private details]'''),
section('welcome-book-format-comparison', 'Compare printed, digital and combined formats',
'''Choose the format around access, update responsibility and guest use. A digital guide can be convenient before arrival but may depend on a device, connectivity or the chosen service. A printed guide is available at the property but needs version control and replacement when damaged. A combined approach is useful only if both copies remain consistent. Test any QR code and provide a plain fallback route; the code alone is not an accessibility or availability guarantee.''',
headers=['Decision', 'Printed guide', 'Digital guide', 'Combined approach'], rows=[
['Arrival access', 'Usually read on site; send essential arrival details through the approved process separately', 'May be shared before arrival through the approved guest channel', 'Send essentials in advance and retain a usable on-site reference'],
['Connectivity/device', 'Readable without a phone connection once the guest finds it', 'Check device, account, link and connectivity requirements of the actual service', 'Keep a concise printed fallback for essential verified instructions'],
['Updating', 'Replace affected pages and mark the current version/date', 'Publish the approved version and test actual links/permissions', 'Reconcile both copies from one controlled source'],
['Privacy', 'Place guest-only/private information according to the approved property process', 'Check sharing/access settings; avoid publishing credentials openly', 'Separate public property description from private guest instructions'],
['Care/cost', 'Record actual printing, format, protection and replacement needs', 'Record actual service costs and responsibilities; do not assume it is free', 'Budget both update tasks and identify the person who owns them'],
['Finding information', 'Use a short contents page, clear sections and legible text', 'Test the guide on a phone and use clear navigation', 'Keep section names and essential instructions consistent'],
]),
section('welcome-book-version-log', 'Test and maintain the guide through a version log',
'''Run an arrival-to-bed and checkout trial using only the guide. Note each point where the tester has to ask a question or guess. Fix the instruction or the underlying setup before accepting the guide. Keep the content concise, readable and tied to actual controls and supplied items. Do not overwhelm the first page with promotions, long stories or unverified recommendations.''',
template='''WELCOME GUIDE VERSION AND TEST LOG
Property / version / approval date: [name / version / date]
Source document owner: [person]
Printed copies and digital location: [actual locations / access arrangement]
Arrival-to-bed test: [person / date / unresolved questions]
Equipment instruction test: [exact items / person / date / result]
Checkout instruction test: [person / date / result]
Local/emergency information checked: [person / date / references]
Changed furnishing/control/contact/rule: [actual change]
Affected guide pages and photographs: [sections / files]
Private/public version check: [who checked / result]
Printed and digital reconciliation complete: [person / date]
Next review trigger and owner: [event / person]'''),
])
