import { chromium } from 'playwright';
const b=await chromium.launch({executablePath:process.env.EXE});
const p=await (await b.newContext({viewport:{width:760,height:900},deviceScaleFactor:1})).newPage();
await p.goto('file:///private/tmp/claude-501/-Users-mira-Documents-projects-lab-laroboti/047a947d-ed46-4108-b1fc-459d43763c11/scratchpad/pw/diag_preview.html');
const n=await p.$$eval('.diagram',e=>e.length);
for(let i=0;i<n;i+=5){const els=await p.$$('.diagram');const box=await els[i].boundingBox();const last=await els[Math.min(i+4,n-1)].boundingBox();
 await p.screenshot({path:`/Users/mira/Documents/projects/lab-laroboti/screenshots-check/2026-10-17/js-diagrams-${i/5+1}.png`,fullPage:true,clip:{x:0,y:box.y-30,width:760,height:last.y+last.height-box.y+40}});}
await b.close();
