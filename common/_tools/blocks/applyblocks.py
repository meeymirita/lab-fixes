# -*- coding: utf-8 -*-
"""Добавляет «Под капотом», «Зачем» и плашки «ПЕРЕД ШАГОМ … Почитать» в методичку (04.10.2026).
Запуск из любой папки:  python3 fixes/common/_tools/blocks/applyblocks.py <лаба> <data_модуль>   (например: nuxt data_nuxt)
Данные (DEEP / WHY_EXTRA / READ, MODE) — в data_*.py рядом. Скрипт добавляет блоки только там, где их ещё нет, и проверяет, что все ссылки открываются.
MODE = 'intro' — плашка в конце intro шага (формат Plan: docker, kubernetes, redis, traefik, rabbitmq); иначе — в outro."""
import sys,json,re,os,html as H,importlib
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.abspath(os.path.join(HERE,'..','..','..','..')); os.chdir(ROOT)
sys.path.insert(0,'fixes/common/_tools'); import bundle
sys.path.insert(0,HERE)
src=open('fixes/common/_tools/prep.py',encoding='utf8').read().rsplit('\nmain()',1)[0]
ns={'__file__':os.path.abspath('fixes/common/_tools/prep.py'),'__name__':'prep'}
exec(compile(src,'prep','exec'),ns)
lab,mod=sys.argv[1],importlib.import_module(sys.argv[2])
import subprocess
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 Chrome/120 Safari/537.36'
bad=[]
for k,items in mod.READ.items():
    for url,*_ in items:
        c=subprocess.run(['curl','-s','-o','/dev/null','-w','%{http_code}','-L','-m','30','-A',UA,url.split('#')[0]],capture_output=True,text=True).stdout
        if c!='200': bad.append((c,url))
if bad: raise SystemExit('ссылки не открываются: '+str(bad))
print('ссылки ок:',sum(len(v) for v in mod.READ.values()))
MODE=getattr(mod,'MODE','outro')
CODE="font-family:'JetBrains Mono',ui-monospace,monospace;font-size:.88em;background:var(--fill);padding:1px 4px"
P='margin:0 0 14px;font-size:16px;line-height:1.65;text-wrap:pretty'
LI='margin:4px 0;line-height:1.6;font-size:15px'
A='color:var(--accent-ink);text-decoration:underline;text-underline-offset:2px'
def inline(t):
    t=H.escape(t,quote=False)
    return re.sub(r'`([^`]+)`',lambda m:'<code style="%s">%s</code>'%(CODE,m.group(1)),t)
def paras(t): return ''.join('<p style="%s">%s</p>'%(P,inline(x.strip())) for x in t.split('\n\n') if x.strip())
def li(url,title,note): return '<li style="%s">Почитать: <a href="%s" target="_blank" style="%s">%s</a> — %s</li>'%(LI,H.escape(url,quote=True),A,H.escape(title,quote=False),H.escape(note,quote=False))
def flat(h): return re.sub(r'\s+',' ',H.unescape(re.sub('<[^>]+>',' ',h)))
def fn(txt):
    pre='window.LAB='
    d,end=json.JSONDecoder().raw_decode(txt[len(pre):])
    st=[u for u in d['units'] if u['kind']=='step']
    byn={u['num']:u for u in st}
    stats={'deep':0,'why':0,'read':0}
    for u in st:
        n=u['num']
        dp=mod.DEEP.get(n)
        if dp and not u.get('deep'):
            u['deep']=[{'summary':dp[0],'html':paras(dp[1])}]
            u['text']=u.get('text','')+' Под капотом '+dp[0]+' '+flat(paras(dp[1])); stats['deep']+=1
        if not u.get('why') and n in mod.WHY_EXTRA:
            u['why']=inline(mod.WHY_EXTRA[n]); stats['why']+=1
    order=[u['num'] for u in st]
    for k,items in mod.READ.items():
        prev=byn[order[order.index(k)-1]]
        if MODE!='intro':
            items=[x for x in items if x[0] not in json.dumps(prev.get('outro') or '',ensure_ascii=False)]
            if not items: continue
        lis=''.join(li(*x) for x in items)
        if MODE=='intro':
            href='#step-'+k.replace('.','-')
            box=('<div style="margin:24px 0 16px;padding:18px 20px;border:2px solid var(--ink)"><span style="display:block;font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:800;color:var(--accent-ink);margin-bottom:8px">ПЕРЕД ШАГОМ <a href="%s" style="%s">%s</a></span><ul style="margin:0 0 14px;padding-left:20px">\n%s</ul></div>'%(href,A,k,'\n'.join(li(*x) for x in items)))
            if 'ПЕРЕД ШАГОМ' not in prev['intro']: prev['intro']+=box
        elif prev.get('outro') and '</ul>' in prev['outro']['html']:
            i=prev['outro']['html'].rindex('</ul>'); prev['outro']['html']=prev['outro']['html'][:i]+lis+prev['outro']['html'][i:]
        elif prev.get('outro'):
            prev['outro']['html']+= '<ul style="margin:0 0 14px;padding-left:20px">'+lis+'</ul>'
        else:
            prev['outro']={'label':'ПЕРЕД ШАГОМ '+k,'html':'<ul style="margin:0 0 14px;padding-left:20px">'+lis+'</ul>'}
        prev['text']=prev.get('text','')+' ПЕРЕД ШАГОМ '+k+' '+' '.join('Почитать: '+x[1] for x in items); stats['read']+=1
    print(lab,stats)
    return pre+json.dumps(d,ensure_ascii=False,separators=(',',':'))+txt[len(pre)+end:]
print(bundle.transform(ns['LABS'][lab],fn))
