# -*- coding: utf-8 -*-
import sys,json,re,html
sys.path.insert(0,'fixes/common/_tools')
import bundle,to_caddy
P='js/js.html'
txt=bundle.load(P); L,end=json.JSONDecoder().raw_decode(txt[11:])
U={u['key']:u for u in L['units']}
def out(t): return '<pre class="out" data-lang="out"><code>%s</code></pre>'%html.escape(t.rstrip(),quote=False)
def fix_pre(h,lang_cls):
    # голые <pre>…</pre> -> с классом и <code>
    def r(m):
        body=m.group(1)
        if body.lstrip().startswith('<code'): return '<pre %s>%s</pre>'%(lang_cls,body)
        return '<pre %s><code>%s</code></pre>'%(lang_cls,body)
    return re.sub(r'<pre>(.*?)</pre>',r,h,flags=re.S)
for u in L['units']:
    if u['kind']!='step': continue
    if u.get('result'): u['result']=fix_pre(u['result'],'class="out" data-lang="out"')
    u['intro']=fix_pre(u['intro'],'class="" data-lang="text"')
t53=open('/tmp/_t53.txt',encoding='utf-8').read(); t83=open('/tmp/_t83.txt',encoding='utf-8').read()
U['step-1-1']['result']='<p>Контейнер <code>dev</code> запущен и отвечает; Node — 24-й версии (патч-версия у вас может быть другой):</p>'+out('v24.22.0')
U['step-5-3']['result']=out(t53)
U['step-6-1']['result']=('<p>Страница пустая: заголовок «Тикеты» и ни одного элемента списка. В консоли браузера — ошибка 404 на <code>/app/main.js</code>: этого файла ещё нет. Никакого билд-шага не было — файлы отдаются прямо с диска. Ответ сервера на корень:</p>'
  +out('HTTP/1.1 200 OK\nContent-Type: text/html'))
r62=U['step-6-2']['result']
U['step-6-2']['result']=r62+'<p>В консоли браузера при смене статуса первого тикета с <code>open</code> на <code>in_progress</code>:</p>'+out('Тикет #1 → in_progress')
U['step-7-1']['result']=('<p>В консоли браузера (<code>await import(...)</code>) приходит объект модуля, строка и массив:</p>'
  +out("{name: 'ticket-constants'} 'open' (3) ['open', 'in_progress', 'closed']")
  +'<p>Статический <code>import</code> в консоль вставить нельзя — браузер отвечает так:</p>'+out('Uncaught SyntaxError: Cannot use import statement outside a module')
  +'<p>Во вкладке Network при загрузке страницы сейчас три запроса: страница, <code>main.js</code> и <code>api.js</code>; <code>constants.mjs</code> появляется только после вызова <code>import()</code>.</p>')
r72=U['step-7-2']['result']
U['step-7-2']['result']=r72+'<p>Во вкладке 1 после <code>saveFilters</code> во вкладке 2:</p>'+out("изменилось в другой вкладке: {status: 'open'}")+'<p>Если в <code>localStorage</code> лежит битый JSON (например, <code>{oops</code>), <code>loadFilters()</code> возвращает <code>{}</code>, а не роняет страницу.</p>'
U['step-8-1']['result']='<p>Сам по себе <code>router.js</code> ничего не показывает: роутер подключит <code>main.js</code> в следующем шаге. Проверить можно только, что файл отдаётся браузеру как модуль — <code>Content-Type: text/javascript</code>.</p>'+out('HTTP/1.1 200 OK\nContent-Type: text/javascript')
U['step-8-3']['result']=out(t83)
U['step-8-4']['result']=('<p>Реальные размеры файлов (<code>wc -l</code>) — столбец «Строк у вас» в таблице ниже посчитан по ним:</p>'
  +out('  55 src/web/app/reactive.js\n  24 src/web/app/views.js\n  44 src/web/app/router.js\n  29 src/web/app/store.js\n  29 src/web/app/main.js\n  15 src/web/app/api.js\n 196 total'))
# числа в таблице 8.4
h=U['step-8-4']['intro']
for a,b in (('~40','~55'),('~20</td>','~25</td>'),('~35','~45')):
    pass
def cell(h,anchor,old,new):
    i=h.index(anchor); j=h.index(old,i); return h[:j]+new+h[j+len(old):]
h=cell(h,'reactive.js</code>','~40','~55')
h=cell(h,'views.js</code>','~20','~25')
h=cell(h,'router.js</code>','~35','~45')
h=cell(h,'store.js</code>','~20','~30')
U['step-8-4']['intro']=h
for k in ('step-1-1','step-5-3','step-6-1','step-6-2','step-7-1','step-7-2','step-8-1','step-8-3','step-8-4'): pass
for u in L['units']:
    if u['kind']!='step': continue
    parts=[u['title'],'Шаг %s. %s'%(u['num'],u['title']),to_caddy._plain(u.get('intro')),to_caddy._plain(u.get('result')),to_caddy._plain(u.get('why'))]
    for d in u.get('deep') or []: parts.append(to_caddy._plain(d.get('summary',''))+' '+to_caddy._plain(d.get('html','')))
    parts+=[to_caddy._plain(q) for q in u.get('quiz') or []]
    if u.get('outro'): parts.append(u['outro']['label']+' '+to_caddy._plain(u['outro']['html']))
    parts+=['Почитать: '+l['t'] for l in u.get('links') or []]
    u['text']=re.sub(r'\s+',' ',' '.join(parts)).strip()
new='window.LAB='+json.dumps(L,ensure_ascii=False,separators=(',',':'))+txt[11+end:]
bundle.transform(P,lambda o:new); print('ok')
