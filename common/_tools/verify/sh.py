# -*- coding: utf-8 -*-
import sys,json,re,html
sys.path.insert(0,'fixes/common/_tools')
import bundle,to_caddy
lab=sys.argv[1]; keys=sys.argv[2:]
txt=bundle.load(f'{lab}/{lab}.html'); L=json.JSONDecoder().raw_decode(txt[11:])[0]
rep={'outro_manual':[],'outro_kept':[],'dropped_links':[]}
L=to_caddy.convert_lab(L,rep)   # смотрим уже после конвертации
U={u['key']:u for u in L['units']}
for k in keys:
    u=U[k]
    print('##',k,u['title'])
    print('  WHY:',to_caddy._plain(u.get('why'))[:420])
    print('  DEEP:',[to_caddy._plain(d['summary'])[:70] for d in u.get('deep') or []])
    print('  RESULT:',to_caddy._plain(u.get('result'))[:260])
    print('  INTRO:',to_caddy._plain(u.get('intro'))[:600])
