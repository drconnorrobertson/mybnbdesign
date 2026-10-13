"""Restore topic-level discovery after regenerating education hubs."""
from pathlib import Path
import sys,re,html,json
ROOT=Path(__file__).resolve().parents[1]
root=ROOT
sys.path.insert(0,str(ROOT / "scripts"))
from build_host_library import upsert_panel
# Relevant education paths surface existing guides rather than adding competing URLs.
groups={
 'learn/reference/dining/index.html':['blog/best-dining-table-for-airbnb/index.html','blog/airbnb-dining-room-design.html'],
 'learn/reference/lighting/index.html':['blog/best-lighting-for-airbnb/index.html','blog/outdoor-smart-lighting-str.html','blog/smart-lighting-systems-str.html'],
 'learn/reference/kitchen/index.html':['blog/airbnb-kitchen-essentials-checklist.html','blog/airbnb-kitchen-design-guide.html'],
 'learn/reference/bathroom/index.html':['blog/airbnb-bathroom-design-guide.html','learn/bathroom-refresh-design-brief/index.html'],
 'learn/reference/amenities/index.html':['blog/airbnb-home-office-design.html','blog/tv-streaming-setup-for-guests.html','blog/digital-guidebook-display-options.html'],
 'learn/reference/arrival/index.html':['blog/smart-lock-guide-for-airbnb.html','blog/keypad-vs-smart-lock-comparison.html','blog/smart-garage-for-airbnb.html'],
 'learn/reference/operations/index.html':['blog/best-wifi-setup-for-str.html','blog/guest-wifi-network-setup.html','blog/water-leak-detector-for-str.html','blog/home-automation-budget-airbnb.html','blog/security-camera-placement-guide-str.html','blog/noise-monitoring-devices-for-airbnb.html','blog/smart-thermostat-for-vacation-rental.html','blog/smart-hvac-zoning-multi-room-str.html','blog/ring-doorbell-vs-competitors-for-str.html','blog/ev-charger-for-vacation-rental.html'],
 'learn/reference/windows/index.html':['blog/smart-blinds-for-str-properties.html'],
 'learn/reference/identity/index.html':['blog/color-psychology-in-vacation-rental-design.html','blog/trending-str-colors-2026.html','blog/tropical-color-palette-guide.html','blog/scandinavian-color-palette-guide.html','blog/airbnb-photography-guide.html'],
 'learn/reference/sleep/index.html':['blog/usb-charging-station-design.html','blog/smart-speaker-setup-for-airbnb.html'],
 'resources/index.html':['blog/vacation-rental-interior-designer-sarasota/index.html','blog/diy-airbnb-makeover-before-after-strategies/index.html','blog/airbnb-home-office-design.html','blog/tropical-color-palette-guide.html']}
for source,targets in groups.items():
 links=[]
 for rel in targets:
  p=root/rel
  if not p.exists():continue
  text=p.read_text();match=re.search(r'<h1[^>]*>(.*?)</h1>',text,re.S)
  label=html.unescape(re.sub('<[^>]+>','',match[1])) if match else rel
  url='/'+rel;url=url[:-10] if url.endswith('/index.html') else url
  links.append(f'<li><a href="{url}">{html.escape(label)}</a></li>')
 upsert_panel(root/source,'seo-topic-guides','<section class="section"><h2>Related STR design guides</h2><p>Use these guides to connect individual design decisions with the complete room, guest experience, and operating plan.</p><ul>'+''.join(links)+'</ul></section>')
# A separate sitemap makes this existing-guide discovery cohort measurable.
import xml.etree.ElementTree as E
ns='http://www.sitemaps.org/schemas/sitemap/0.9';E.register_namespace('',ns)
known={x.text for p in root.glob('sitemap*.xml') if p.name!='sitemap-design-guides.xml' for x in E.parse(p).findall('.//{*}loc')}
urls=set()
for targets in groups.values():
 for rel in targets:
  p=root/rel
  if not p.exists():continue
  text=p.read_text();c=re.search(r'<link[^>]*rel="canonical"[^>]*href="([^"]+)"',text)
  route='/'+rel;route=route[:-10] if route.endswith('/index.html') else route
  url='https://www.mybnbdesign.com'+route
  if c and c[1]==url and url not in known and not re.search(r'<meta[^>]*noindex',text,re.I):urls.add(url)
xml=E.Element('{'+ns+'}urlset')
for url in sorted(urls):E.SubElement(E.SubElement(xml,'{'+ns+'}url'),'{'+ns+'}loc').text=url
E.indent(xml);(root/'sitemap-design-guides.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n'+E.tostring(xml,encoding='unicode')+'\n')
robots=root/'robots.txt';text=robots.read_text();line='Sitemap: https://www.mybnbdesign.com/sitemap-design-guides.xml'
if line not in text:robots.write_text(text.rstrip()+'\n'+line+'\n')
print('Additional existing guides in sitemap:',len(urls))
