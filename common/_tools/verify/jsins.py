# -*- coding: utf-8 -*-
import sys,json,re
sys.path.insert(0,'/private/tmp/claude-501/-Users-mira-Documents-projects-lab-laroboti/047a947d-ed46-4108-b1fc-459d43763c11/scratchpad')
sys.path.insert(0,'/Users/mira/Documents/projects/lab-laroboti/fixes/common/_tools')
import bundle,to_caddy,jsdiag
P='/Users/mira/Documents/projects/lab-laroboti/js/js.html'
txt=bundle.load(P); L,end=json.JSONDecoder().raw_decode(txt[11:])
U={u['key']:u for u in L['units']}
n=0
for k,svg in jsdiag.D.items():
    u=U[k]; h=re.sub(r'<div class="diagram">.*?</svg></div>','',u['intro'],flags=re.S)
    m=re.match(r'\s*<p>.*?</p>',h,re.S)
    u['intro']=(h[:m.end()]+svg+h[m.end():]) if m else svg+h
    parts=[u['title'],'Шаг %s. %s'%(u['num'],u['title']),to_caddy._plain(u.get('intro')),to_caddy._plain(u.get('result')),to_caddy._plain(u.get('why'))]
    for d in u.get('deep') or []: parts.append(to_caddy._plain(d.get('summary',''))+' '+to_caddy._plain(d.get('html','')))
    parts+=[to_caddy._plain(q) for q in u.get('quiz') or []]
    if u.get('outro'): parts.append(u['outro']['label']+' '+to_caddy._plain(u['outro']['html']))
    parts+=['Почитать: '+l_['t'] for l_ in u.get('links') or []]
    u['text']=re.sub(r'\s+',' ',' '.join(parts)).strip(); n+=1
new='window.LAB='+json.dumps(L,ensure_ascii=False,separators=(',',':'))+txt[11+end:]
bundle.transform(P,lambda o:new); print('схем вставлено',n)
