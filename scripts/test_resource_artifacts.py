"""Regression checks for practical scope at the ten established resource routes."""
from pathlib import Path
from html.parser import HTMLParser
import html
import json
import re
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.build_host_library import GUIDES, CLUSTERS, render_guide, artifact_text, target, route
from content.resource_artifacts import ARTIFACTS

# Independent editorial acceptance criteria: an essay-only rewrite must fail.
SCOPES={
 'airbnb-furnishing-checklist':(['living-room-inventory','kitchen-inventory','bedroom-inventory','bathroom-outdoor-utility-inventory'],['Frying pan','pillowcases','Bath towels','Order quantity:']),
 'briefing-designer-str':(['design-brief-template','designer-scope-budget-table','designer-project-gates'],['SHORT-TERM RENTAL DESIGN BRIEF','Measured floor plan','Substitution approval process:']),
 'damage-resistant-materials':(['material-comparison-matrix','material-selection-record','material-cost-and-maintenance'],['Upholstery','Paint/wall finish','Outdoor furniture']),
 'design-for-superhost':(['guest-use-room-audit','guest-feedback-triage-template','guest-feedback-closeout'],['Living','Bathroom','observ']),
 'design-mistakes-kill-bookings':(['room-design-audit-matrix','design-issue-card-template','design-audit-action-order'],['Bedroom','Kitchen','Decision and approval owner:']),
 'insurance-friendly-design':(['insurance-inventory-template','insurance-review-question-list','insurance-maintenance-log'],['Amount paid:','Current condition photo references:','Work performed and completion date:']),
 'photography-staging-guide':(['photo-preparation-checklist','room-photo-shot-list','photographer-brief-template','photo-acceptance-record'],['Arrival/entry','Bedrooms','Bathrooms','Usage rights']),
 'seasonal-decor-calendar':(['month-by-month-calendar','seasonal-swap-kit','seasonal-budget-storage'],['January','December','Northern Hemisphere']),
 'ultimate-guide-str-design':(['project-stage-gates','project-room-by-room','project-budget-worksheet','project-maintenance-seasonal-closeout'],['COMPLETE FURNISHING PROJECT BUDGET','Freight, receiving','PROJECT ACCEPTANCE AND HANDOVER']),
 'welcome-book-template':(['welcome-message-template','arrival-checkout-templates','house-rules-template','wifi-appliance-template','local-emergency-reference','welcome-book-version-log'],['WELCOME TO [PROPERTY NAME]','CHECK-IN QUICK REFERENCE','CHECKOUT QUICK REFERENCE','HOUSE GUIDELINES','EQUIPMENT CARD','PROPERTY EMERGENCY QUICK REFERENCE']),
}

class WorksheetHTML(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=[];self.headings=0;self.tables=0;self.column_headers=0;self.templates=0;self.downloads=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='h1':self.headings+=1
        if tag=='table':self.tables+=1
        if tag=='th' and a.get('scope')=='col':self.column_headers+=1
        if tag=='pre' and a.get('class')=='artifact-template':self.templates+=1
        if tag=='a' and 'download' in a:self.downloads.append(a['href'])

class ResourceArtifacts(unittest.TestCase):
    def test_all_ten_existing_scopes_are_attached_to_repairs(self):
        expected={'/resources/'+s+'/' for s in SCOPES}
        self.assertEqual(set(ARTIFACTS),expected)
        repairs=[g for g in GUIDES if g.get('repair')]
        self.assertEqual(len(repairs),16)
        self.assertEqual(len([g for g in GUIDES if not g.get('repair')]),60)
        self.assertEqual(len(CLUSTERS),8)
        self.assertEqual({route(g) for g in repairs if g.get('artifacts')},expected)

    def test_inventory_template_and_record_scope_survives_rendering(self):
        for slug,(sections,phrases) in SCOPES.items():
            with self.subTest(resource=slug):
                r='/resources/'+slug+'/'
                g=dict(next(g for g in GUIDES if route(g)==r))
                saved=target(ROOT,r).read_text()
                schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',saved,re.S)[1])
                g['published']=schema[0]['datePublished']
                page=render_guide(g); parsed=WorksheetHTML(page);text=html.unescape(page)
                self.assertEqual(parsed.headings,1)
                self.assertEqual(len(parsed.ids),len(set(parsed.ids)))
                self.assertGreaterEqual(parsed.tables,1)
                self.assertGreaterEqual(parsed.templates,1)
                self.assertGreaterEqual(parsed.column_headers,3)
                self.assertEqual(parsed.downloads,[r+'worksheet.txt'])
                for identifier in sections:self.assertIn(identifier,parsed.ids)
                download=artifact_text(g)
                for phrase in phrases:
                    self.assertTrue(phrase in text,f'{slug}: rendered worksheet missing {phrase!r}')
                    self.assertTrue(phrase in download,f'{slug}: download missing {phrase!r}')
                self.assertTrue(saved==page,f'{slug}: generated page differs from source')
                self.assertEqual((target(ROOT,r).parent/'worksheet.txt').read_text(),download)

    def test_records_have_real_fields_and_rectangular_tables(self):
        for r,sections in ARTIFACTS.items():
            with self.subTest(resource=r):
                for s in sections:
                    self.assertTrue(s['text'].strip(),s['id'])
                    for row in s['rows']:self.assertEqual(len(row),len(s['headers']),s['id'])
                    if s['template']:self.assertGreaterEqual(s['template'].count('['),8,s['id'])
                # No invented monetary, percentage or universal lifespan forecasts.
                text=' '.join(s['text']+s['template']+' '.join(' '.join(row) for row in s['rows']) for s in sections)
                self.assertNotRegex(text,r'\d+\s*%|\$\d|\d+[-–]\d+\s*years')

    def test_verification_file_is_exact_and_not_promoted_to_sitemaps(self):
        name='googlea1274d45bb100c71.html'
        self.assertEqual((ROOT/name).read_bytes(),('google-site-verification: '+name).encode())
        for sitemap in ROOT.glob('sitemap*.xml'):self.assertNotIn(name,sitemap.read_text())

if __name__=='__main__':unittest.main()
