# -*- coding: utf-8 -*-
import sys,json,re,html
sys.path.insert(0,'fixes/common/_tools')
import bundle
lab=sys.argv[1]
L=json.JSONDecoder().raw_decode(bundle.load(f'{lab}/{lab}.html')[11:])[0]
RX=re.compile(r'<pre class="([^"]*)" data-lang="([^"]*)"><code>(.*?)</code></pre>',re.S)
for u in L['units']:
    if u['kind']!='step': continue
    out=[]
    for f in ('intro','result'):
        for m in RX.finditer(u.get(f) or ''):
            code=html.unescape(m.group(3)); first=code.strip().split('\n')[0][:70]
            out.append(f'{f[0]}:{m.group(2)}:{len(code)}:{first}')
    print(u['num'],u['title'][:50]); [print('   ',o) for o in out]
