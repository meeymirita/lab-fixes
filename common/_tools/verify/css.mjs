import { chromium } from 'playwright';
const [lab,key,sel]=process.argv.slice(2);
const b=await chromium.launch({executablePath:process.env.EXE,args:['--host-resolver-rules=MAP cdnjs.cloudflare.com 0.0.0.0']});
const p=await (await b.newContext({viewport:{width:1280,height:900}})).newPage();
await p.route(/workers\.dev|yandexcloud|fonts\.g/,r=>r.abort());
await p.goto(`http://localhost:8772/${lab}.html`);await p.waitForTimeout(1200);
await p.evaluate(h=>{location.hash=h},key);await p.waitForTimeout(500);
console.log(await p.evaluate(s=>{const e=document.querySelector(s);if(!e)return 'нет '+s;const c=getComputedStyle(e);return JSON.stringify({bc:c.borderCollapse,pad:c.padding,border:c.borderBottom,w:c.width,fs:c.fontSize,disp:c.display,bg:c.backgroundColor,bl:c.borderLeftWidth})},sel));
await b.close();
