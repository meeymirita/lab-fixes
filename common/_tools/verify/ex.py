# -*- coding: utf-8 -*-
import sys,json
sys.path.insert(0,'fixes/common/_tools')
import bundle
def load(p): return json.JSONDecoder().raw_decode(bundle.load(p)[len('window.LAB='):])[0]
lab,key=sys.argv[1],sys.argv[2]
L=load(f'{lab}/{lab}.html'); u=[x for x in L['units'] if x['key']==key][0]
for k,v in u.items():
    if k=='text': continue
    print('##',k, '→', (json.dumps(v,ensure_ascii=False) if not isinstance(v,str) else v)[:int(sys.argv[3]) if len(sys.argv)>3 else 900].replace('\n','⏎'))
