# -*- coding: utf-8 -*-
"""patch.py <lab> <file.json>: {ключ: {quiz:[..], outro:{label,html}}} — дописывает поля и пересчитывает text шага."""
import sys,json,re
sys.path.insert(0,'fixes/common/_tools')
import bundle,to_caddy
lab,f=sys.argv[1:3]
P=f'{lab}/{lab}.html'
data=json.load(open(f,encoding='utf-8'))
txt=bundle.load(P); L,end=json.JSONDecoder().raw_decode(txt[11:])
U={u['key']:u for u in L['units']}
for k,v in data.items():
    u=U[k]; u.update(v)
    parts=[u['title'],'Шаг %s. %s'%(u['num'],u['title']),to_caddy._plain(u.get('intro')),to_caddy._plain(u.get('result')),to_caddy._plain(u.get('why'))]
    for d in u.get('deep') or []: parts.append(to_caddy._plain(d.get('summary',''))+' '+to_caddy._plain(d.get('html','')))
    parts+=[to_caddy._plain(q) for q in u.get('quiz') or []]
    if u.get('outro'): parts.append(u['outro']['label']+' '+to_caddy._plain(u['outro']['html']))
    for l in u.get('links') or []: parts.append('Почитать: '+l['t'])
    u['text']=re.sub(r'\s+',' ',' '.join(parts)).strip()
new='window.LAB='+json.dumps(L,ensure_ascii=False,separators=(',',':'))+txt[11+end:]
bundle.transform(P,lambda o:new); print('patched',list(data))
