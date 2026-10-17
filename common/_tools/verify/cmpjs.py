# -*- coding: utf-8 -*-
import sys,json,re,html,difflib
sys.path.insert(0,'/Users/mira/Documents/projects/lab-laroboti/fixes/common/_tools')
import bundle
S='/private/tmp/claude-501/-Users-mira-Documents-projects-lab-laroboti/047a947d-ed46-4108-b1fc-459d43763c11/scratchpad/'
L=json.JSONDecoder().raw_decode(bundle.load('/Users/mira/Documents/projects/lab-laroboti/js/js.html')[11:])[0]
res=json.load(open(S+'js_out.json'))
def lines(t): return [re.sub(r'\s+',' ',x).strip() for x in t.split('\n') if x.strip()]
only=sys.argv[1:]
for u in L['units']:
    if u['kind']!='step' or u['key'] not in res or (only and u['num'] not in only): continue
    r=u.get('result') or ''
    pre=re.findall(r'<pre[^>]*>(?:<code>)?(.*?)(?:</code>)?</pre>',r,re.S)
    exp=html.unescape('\n'.join(pre)) if pre else None
    runs=[x for x in res[u['key']] if x['cmd'].startswith('docker compose exec')]
    act='\n'.join(x['out'] for x in runs)
    if exp is None:
        print(u['num'],'result: текст без блока кода' if r else 'result: ПУСТО','| вывод',len(act),'знаков'); continue
    a,b=lines(exp),lines(act)
    if a==b: print(u['num'],'OK совпало'); continue
    d=[l for l in difflib.unified_diff(a,b,'ожидали','получили',lineterm='',n=0) if not l.startswith(('---','+++','@@'))]
    print(u['num'],'РАСХОЖДЕНИЕ',len(d),'строк'); [print('    ',x[:140]) for x in d[:8]]
