import { chromium } from 'playwright';
const [scn]=process.argv.slice(2);
const b=await chromium.launch({executablePath:process.env.EXE});
const ctx=await b.newContext();const p=await ctx.newPage();
const logs=[],reqs=[];
p.on('console',m=>logs.push(m.type()+': '+m.text()));p.on('pageerror',e=>logs.push('pageerror: '+e.message));
p.on('requestfinished',r=>reqs.push(r.method()+' '+r.url().replace('http://localhost:15500','').replace('http://localhost:3001','API').replace('http://localhost:13001','API')));
p.on('requestfailed',r=>reqs.push('FAILED '+r.url()));
await p.route('http://localhost:3001/**',r=>r.continue({url:r.request().url().replace('localhost:3001','localhost:13001')}));
const U='http://localhost:15500';
async function snap(){return p.evaluate(()=>({title:document.title,h1:document.querySelector('h1')?.innerText,items:[...document.querySelectorAll('li, tr, .ticket')].length,body:document.body.innerText.replace(/\s+/g,' ').slice(0,300),selects:document.querySelectorAll('select').length,url:location.pathname}))}
await p.goto(U);await p.waitForTimeout(800);
if(scn==='6.1'){console.log(JSON.stringify(await snap()));}
if(scn==='6.2'){console.log('до',JSON.stringify(await snap()));
  const first=p.locator('select').first();const before=await first.inputValue();const target=before==='open'?'in_progress':'open';
  await first.selectOption(target);await p.waitForTimeout(600);
  console.log('сменили',before,'->',target);await p.reload();await p.waitForTimeout(800);
  console.log('после перезагрузки первый select =',await p.locator('select').first().inputValue());
  await p.locator('select').first().selectOption(before);await p.waitForTimeout(400);}
if(scn==='7.1'){console.log(JSON.stringify(await snap()));}
if(scn==='7.2'){const p2=await ctx.newPage();await p2.route('http://localhost:3001/**',r=>r.continue({url:r.request().url().replace('localhost:3001','localhost:13001')}));const l2=[];p2.on('console',m=>l2.push(m.text()));p.on('console',()=>{});await p2.goto(U);await p2.waitForTimeout(800);
  console.log('localStorage ключи:',JSON.stringify(await p.evaluate(()=>Object.keys(localStorage))));
  await p2.evaluate(()=>localStorage.setItem('filters',JSON.stringify({status:'open'})));await p2.waitForTimeout(500);
  console.log('вкладка1 логи:',JSON.stringify(logs.slice(-4)));console.log('вкладка2 логи:',JSON.stringify(l2.slice(-3)));}
if(scn==='8.1'||scn==='8.2'){console.log(JSON.stringify(await snap()));
  const a=p.locator('a').first();const t=await a.innerText().catch(()=>'');console.log('первая ссылка:',t);
  const navBefore=reqs.filter(r=>r.includes('GET /')&&!r.includes('/app/')&&!r.includes('API')).length;
  await a.click();await p.waitForTimeout(800);console.log('после клика',JSON.stringify(await snap()));
  const docReqs=reqs.filter(r=>/GET \/(tickets\/\d+)?$/.test(r));console.log('запросы документа:',JSON.stringify(docReqs));
  await p.goBack();await p.waitForTimeout(500);console.log('после «назад» url=',await p.evaluate(()=>location.pathname));}
console.log('запросы:',JSON.stringify(reqs.slice(0,14)));console.log('логи консоли:',JSON.stringify(logs.slice(0,6)));
await b.close();
