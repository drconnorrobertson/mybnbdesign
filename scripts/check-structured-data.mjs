import fs from 'node:fs';
import path from 'node:path';
const root=path.resolve(process.argv[2]||'dist');let pages=0,blocks=0;const errors=[];
function walk(dir){for(const e of fs.readdirSync(dir,{withFileTypes:true})){if(e.name.startsWith('.')||e.name==='node_modules')continue;const p=path.join(dir,e.name);if(e.isDirectory())walk(p);else if(e.name.endsWith('.html')){pages++;const text=fs.readFileSync(p,'utf8');for(const m of text.matchAll(/<script\b[^>]*type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi)){blocks++;try{JSON.parse(m[1]);}catch(err){errors.push(`${path.relative(root,p)}: ${err.message}`);}}}}}
walk(root);if(errors.length){console.error(errors.join('\n'));process.exit(1);}console.log(`Structured data: ${blocks} JSON-LD blocks valid across ${pages} HTML pages.`);
