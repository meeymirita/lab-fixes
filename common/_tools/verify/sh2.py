# -*- coding: utf-8 -*-
import sys,json,re
sys.path.insert(0,'fixes/common/_tools')
import bundle,to_caddy
lab=sys.argv[1]; a,b=int(sys.argv[2]),int(sys.argv[3])
txt=bundle.load(f'{lab}/{lab}.html'); L=json.JSONDecoder().raw_decode(txt[11:])[0]
steps=[u for u in L['units'] if u['kind']=='step'][a:b]
P=to_caddy._plain
for u in steps:
    print('##',u['key'],u['title'][:90]); print('  W:',P(u.get('why'))[:380]); print('  D:',[P(d['summary'])[:60] for d in u.get('deep') or []]); print('  R:',P(u.get('result'))[:140])
if '--sess' in sys.argv:
    for s in L['sessions']: print('SESSION',s['n'],s['title'],s['steps'][0],'..',s['steps'][-1])
