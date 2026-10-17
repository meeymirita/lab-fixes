import { chromium } from 'playwright';
import fs from 'fs';
const [lab,keysFile]=process.argv.slice(2);
const keys=fs.readFileSync(keysFile,'utf8').trim().split('\n');
const b=await chromium.launch({executablePath:process.env.EXE,args:['--host-resolver-rules=MAP cdnjs.cloudflare.com 0.0.0.0']});
async function grab(port){
  const c=await b.newContext({viewport:{width:1280,height:900}});const p=await c.newPage();
  const errs=[];p.on('pageerror',e=>errs.push(String(e).slice(0,150)));
  await p.route(/workers\.dev|yandexcloud|fonts\.g/,r=>r.abort());
  await p.goto(`http://localhost:${port}/${lab}.html`);await p.waitForTimeout(1500);
  const res={};
  for(const k of keys){
    await p.evaluate(h=>{location.hash=h},k);await p.waitForTimeout(250);
    res[k]=await p.evaluate(()=>{const m=document.querySelector('main')||document.body;return {t:m.innerText.replace(/\s+/g,' ').trim(),styled:[...m.querySelectorAll('[style]')].length,tip:[...m.querySelectorAll('.tip,.trap')].length}});
  }
  await c.close();return {res,errs};
}
const a=await grab(8771), n=await grab(8772);
let diffs=0,styledNew=0;
for(const k of keys){
  const x=a.res[k].t.toLowerCase(), y=n.res[k].t.toLowerCase();
  styledNew+=n.res[k].styled;
  if(x!==y){diffs++; if(diffs<=6){ // найдём первое расхождение
    let i=0;while(i<x.length&&x[i]===y[i])i++;
    console.log('DIFF',k,'at',i,'\n  old:',x.slice(Math.max(0,i-40),i+120),'\n  new:',y.slice(Math.max(0,i-40),i+120));}}
}
console.log(`steps ${keys.length}, differing ${diffs}, inline-styled elements in new: ${styledNew}, errors old=${a.errs.length} new=${n.errs.length}`,n.errs.slice(0,3));
console.log('tip/trap boxes new total:',keys.reduce((s,k)=>s+n.res[k].tip,0),' old total:',keys.reduce((s,k)=>s+a.res[k].tip,0));
await b.close();
