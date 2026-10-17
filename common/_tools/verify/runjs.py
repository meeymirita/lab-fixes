# -*- coding: utf-8 -*-
"""runjs.py [--from N.M] [--to N.M]: собирает стенд JS-лабы из блоков методички и выполняет команды шагов в Docker.
Результаты — scratchpad/js_out.json: {ключ шага: [{cmd, out, rc}]}. Рабочая папка — .manual-tmp/js-verify (не в git)."""
import sys, json, re, html, os, subprocess, time
sys.path.insert(0, '/Users/mira/Documents/projects/lab-laroboti/fixes/common/_tools')
import bundle
ROOT = '/Users/mira/Documents/projects/lab-laroboti'
W = ROOT + '/.manual-tmp/js-verify'
OUT = '/private/tmp/claude-501/-Users-mira-Documents-projects-lab-laroboti/047a947d-ed46-4108-b1fc-459d43763c11/scratchpad/js_out.json'
L = json.JSONDecoder().raw_decode(bundle.load(ROOT + '/js/js.html')[11:])[0]
RX = re.compile(r'<pre class="([^"]*)" data-lang="([^"]*)"><code>(.*?)</code></pre>', re.S)
PATH = re.compile(r'^\s*(?://|<!--|#)\s*([\w./-]+\.\w+)')
args = sys.argv[1:]
lo = args[args.index('--from') + 1] if '--from' in args else '0.0'
hi = args[args.index('--to') + 1] if '--to' in args else '99.9'
skip = set(args[args.index('--skip') + 1].split(',')) if '--skip' in args else set()
def key(n): return tuple(int(x) for x in n.split('.'))
os.makedirs(W, exist_ok=True)
res = json.load(open(OUT)) if os.path.exists(OUT) else {}

def sh(cmd, timeout=90):
    cmd = re.sub(r'docker compose exec (?!-T)', 'docker compose exec -T ', cmd)
    t = time.time()
    try:
        p = subprocess.run(cmd, shell=True, cwd=W, capture_output=True, text=True, timeout=timeout, env={**os.environ, 'COMPOSE_PROJECT_NAME': 'jsverify'})
        return {'cmd': cmd, 'out': (p.stdout + p.stderr), 'rc': p.returncode, 'sec': round(time.time() - t, 1)}
    except subprocess.TimeoutExpired as e:
        return {'cmd': cmd, 'out': ((e.stdout or b'').decode() if isinstance(e.stdout, bytes) else (e.stdout or '')) + ' [TIMEOUT]', 'rc': -9, 'sec': timeout}

for u in L['units']:
    if u['kind'] != 'step' or not (key(lo) <= key(u['num']) <= key(hi)) or u['num'] in skip:
        continue
    log = []
    for m in RX.finditer(u.get('intro') or ''):
        lang, code = m.group(2), html.unescape(m.group(3))
        first = code.strip().split('\n', 1)[0]
        if lang == 'bash':
            for line in code.strip().split('\n'):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if line.startswith('mkdir js-lab') or line.startswith('cd '):
                    line = line.split('&&', 1)[1].strip() if '&&' in line and line.startswith('mkdir js-lab') else line
                    if line.startswith('git init') or line.startswith('cd '):
                        continue
                log.append(sh(line))
            continue
        pm = PATH.match(first)
        if pm and lang != 'out':
            p = pm.group(1)
            body = code
            if p in ('docker-compose.yml', 'package.json', 'db.json'):
                body = code.split('\n', 1)[1] if first.startswith('#') else code
            os.makedirs(os.path.dirname(os.path.join(W, p)) or W, exist_ok=True)
            open(os.path.join(W, p), 'w', encoding='utf-8').write(body)
            log.append({'cmd': 'write ' + p, 'out': '', 'rc': 0})
        else:
            log.append({'cmd': 'SKIP block ' + lang + ': ' + first[:60], 'out': '', 'rc': 0})
    res[u['key']] = log
    print(u['num'], [(l['cmd'][:60], l['rc']) for l in log if not l['cmd'].startswith('write')])
    json.dump(res, open(OUT, 'w'), ensure_ascii=False, indent=1)
