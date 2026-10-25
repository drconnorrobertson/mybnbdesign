// Keep the Vercel command short while preserving the ordered publication gates.
const {execFileSync} = require('node:child_process');
const {resolve} = require('node:path');
const root = resolve(__dirname,'..');
const stages = [
  [process.execPath,['scripts/decision-guides.cjs']],
  [process.execPath,['scripts/prepare-static.mjs']],
  [process.execPath,['scripts/instrument-conversions.mjs','dist']],
  ['python3',['scripts/curate-indexing.py','dist']],
  [process.execPath,['scripts/check-indexability.mjs','dist']],
  [process.execPath,['scripts/check-structured-data.mjs','dist']],
  [process.execPath,['scripts/brand-check.mjs','dist']],
  [process.execPath,['scripts/optimize-media.mjs','dist']],
];
for (const [command,args] of stages) execFileSync(command,args,{cwd:root,stdio:'inherit'});
