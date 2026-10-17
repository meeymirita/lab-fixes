import { chromium } from 'playwright';
const b=await chromium.launch({executablePath:process.env.EXE});
const ctx=await b.newContext();const p=await ctx.newPage();
const route=pg=>pg.route('http://localhost:3001/**',r=>r.continue({url:r.request().url().replace('localhost:3001','localhost:13001')}));
await route(p);await p.goto('http://localhost:15500');await p.waitForTimeout(600);
// 7.1: динамический import в консоли
console.log('7.1 dynamic import:',JSON.stringify(await p.evaluate("import('/app/constants.mjs').then(m=>[m.default,m.DEFAULT_STATUS,m.STATUSES])")));
// 7.1: статический import как в методичке — в классическом скрипте
const err=await p.evaluate(()=>{try{(0,eval)("import c, { DEFAULT_STATUS } from '/app/constants.mjs'");return 'нет ошибки'}catch(e){return e.name+': '+e.message}});
console.log('7.1 static import in console:',err);
const res=[];p.on('requestfinished',r=>res.push(r.url().replace('http://localhost:15500','')));
await p.reload();await p.waitForTimeout(700);console.log('7.1 запросы при загрузке:',JSON.stringify(res));
// 7.2: две вкладки
const p2=await ctx.newPage();await route(p2);await p2.goto('http://localhost:15500');await p2.waitForTimeout(500);
const l1=[],l2=[];p.on('console',m=>l1.push(m.text()));p2.on('console',m=>l2.push(m.text()));
await p.evaluate("import('/app/filters.js').then(m=>m.onFiltersChangedElsewhere(f=>console.log('изменилось в другой вкладке:',JSON.stringify(f))))");
await p2.evaluate("import('/app/filters.js').then(m=>{m.onFiltersChangedElsewhere(f=>console.log('вкладка 2 получила:',JSON.stringify(f)));m.saveFilters({status:'open'})})");
await p.waitForTimeout(600);
console.log('7.2 вкладка 1:',JSON.stringify(l1),'| вкладка 2:',JSON.stringify(l2));
console.log('7.2 localStorage:',await p.evaluate(()=>localStorage.getItem('ticket-filters')));
// повреждённый JSON
console.log('7.2 битый JSON ->',JSON.stringify(await p.evaluate("localStorage.setItem('ticket-filters','{oops');import('/app/filters.js').then(m=>m.loadFilters())")));
await p.evaluate(()=>localStorage.clear());
await b.close();
