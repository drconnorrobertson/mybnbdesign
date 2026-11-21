"""Repair reversed legacy breadcrumb tuples in published JSON-LD only."""
from pathlib import Path
import json,re,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else 'dist')
origin='https://www.mybnbdesign.com'
changed=0
for p in root.rglob('*.html'):
 text=p.read_text()
 def repair(m):
  data=json.loads(m[2]);fixed=False
  def visit(value):
   nonlocal fixed
   if isinstance(value,list):
    for item in value:visit(item)
   elif isinstance(value,dict):
    if value.get('@type')=='BreadcrumbList':
     for crumb in value.get('itemListElement',[]):
      name,item=crumb.get('name'),crumb.get('item')
      if isinstance(name,str) and name.startswith('/') and isinstance(item,str) and item.startswith(origin) and not item[len(origin):].startswith(('/','?','#')):
       crumb['name']=item[len(origin):];crumb['item']=origin+name;fixed=True
    for item in value.values():visit(item)
  visit(data)
  return m[1]+json.dumps(data,ensure_ascii=False).replace('<','\\u003c')+m[3] if fixed else m[0]
 updated=re.sub(r'(<script\b[^>]*type=["\x27]application/ld\+json["\x27][^>]*>)(.*?)(</script>)',repair,text,flags=re.S|re.I)
 if updated!=text:p.write_text(updated);changed+=1
print(json.dumps({'breadcrumb_pages_repaired':changed}))
