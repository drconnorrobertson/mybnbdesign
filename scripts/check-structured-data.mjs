import fs from 'node:fs';
import path from 'node:path';
const root=path.resolve(process.argv[2]||'dist');let pages=0,blocks=0;const errors=[];
function validate(value){
 if(Array.isArray(value)){value.forEach(validate);return;}
 if(!value||typeof value!=='object')return;
 if(value['@type']==='BreadcrumbList')for(const crumb of value.itemListElement||[]){
  const item=typeof crumb.item==='string'?crumb.item:crumb.item?.['@id'];
  if(!item)throw Error('Breadcrumb item is missing a URL');
  const url=new URL(item);
  if(!['https:','http:'].includes(url.protocol))throw Error('Breadcrumb item must be an HTTP URL');
  if(item.startsWith('https://www.mybnbdesign.com')&&url.hostname!=='www.mybnbdesign.com')throw Error('Malformed MyBnBDesign breadcrumb URL: '+item);
  if(typeof crumb.name!=='string'||!crumb.name.trim()||crumb.name.startsWith('/'))throw Error('Breadcrumb name must be a readable label');
 }
 Object.values(value).forEach(validate);
}
function walk(dir){for(const e of fs.readdirSync(dir,{withFileTypes:true})){if(e.name.startsWith('.')||e.name==='node_modules')continue;const p=path.join(dir,e.name);if(e.isDirectory())walk(p);else if(e.name.endsWith('.html')){pages++;const text=fs.readFileSync(p,'utf8');for(const m of text.matchAll(/<script\b[^>]*type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi)){blocks++;try{validate(JSON.parse(m[1]));}catch(err){errors.push(`${path.relative(root,p)}: ${err.message}`);}}}}}
walk(root);if(errors.length){console.error(errors.join('\n'));process.exit(1);}console.log(`Structured data: ${blocks} JSON-LD blocks valid across ${pages} HTML pages; breadcrumb URLs and labels checked.`);
