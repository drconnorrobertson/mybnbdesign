import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const repo = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const out = path.join(repo,'dist');
const extensions = new Set(['.html','.css','.js','.json','.svg','.txt','.xml','.png','.jpg','.jpeg','.webp','.avif','.gif','.ico','.woff2','.woff','.ttf','.eot','.mp3','.mp4','.webm','.vtt','.webmanifest','.pdf','.csv']);
const skip = new Set(['.git','.vercel','node_modules','dist','scripts','tests','work','app','src','lib','components','api','_gen','__pycache__','brand-link-policy.json','brand-check-policy.json','package.json','package-lock.json','tsconfig.json','vercel.json']);
fs.rmSync(out,{recursive:true,force:true});fs.mkdirSync(out,{recursive:true});
const excludedPaths=new Set(JSON.parse(fs.readFileSync(path.join(repo,'scripts/publish-exclusions.json'),'utf8')).paths);
function copy(dir,dest) {
 for(const entry of fs.readdirSync(dir,{withFileTypes:true})) {
  if(skip.has(entry.name) || (entry.name.startsWith('.') && entry.name!=='.well-known')) continue;
  const from=path.join(dir,entry.name),to=path.join(dest,entry.name);
  if(excludedPaths.has(path.relative(repo,from).split(path.sep).join('/'))) continue;
  if(entry.isDirectory()) {fs.mkdirSync(to,{recursive:true});copy(from,to);}
  else if(extensions.has(path.extname(entry.name))) fs.copyFileSync(from,to);
 }
}
copy(repo,out);
if(!fs.existsSync(path.join(out,'index.html'))) throw new Error('Static publish directory is missing index.html');
console.log('Prepared static publish directory without build sources or brand policy files.');

const {execFileSync}=await import('node:child_process');
execFileSync(process.execPath,[path.join(repo,'scripts/search-intent.mjs'),'--write','--dist'],{cwd:repo,stdio:'inherit'});

for(const file of excludedPaths){if(!fs.existsSync(path.join(repo,file)))throw new Error('Excluded source missing: '+file);if(fs.existsSync(path.join(out,file)))throw new Error('Test stub leaked into output: '+file);}
console.log('Publication boundary: '+excludedPaths.size+' test stubs retained in source and excluded from output.');
