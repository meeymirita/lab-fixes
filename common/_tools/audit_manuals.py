# -*- coding: utf-8 -*-
"""Сквозная проверка всех методичек (структура и ссылки, без запуска кода).

Запуск из корня репозитория:  python3 fixes/common/_tools/audit_manuals.py [лаба ...]
Проверяет: пустые разделы и шаги, битые якоря #step-N-M / #sec-N, ссылки «шаг N.M» и «сессия N» на несуществующее,
повторяющиеся блоки, дубли ссылок и вопросов, незакрытые теги, остатки старой вёрстки («Перед шагом», {{ }}, undefined).
Выводит находки по лабам; код возврата 1, если найдены ошибки (не предупреждения)."""
import html as H, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bundle

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
src = open(os.path.join(ROOT, 'fixes/common/_tools/prep.py'), encoding='utf-8').read()
LABS = eval('{' + re.search(r'\nLABS = \{(.*?)\n\}\n', src, re.S).group(1) + '}')
SKIP = {'go-start', 'go-pro'}          # не задействованы (решение владельца 17.10.2026)
PAIRED = ('div', 'p', 'ul', 'ol', 'li', 'table', 'tbody', 'tr', 'td', 'th', 'pre', 'code', 'details', 'summary', 'b', 'a', 'span', 'h3')
VOID = {'br', 'img', 'hr', 'input', 'wbr', 'meta', 'link'}
TOKEN = re.compile(r'</?([A-Za-z][\w-]*)[^>]*?/?>')


def plain(h):
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', ' ', h or ''))).strip()


def balance(h):
    """Незакрытые парные теги в html-фрагменте (вне блоков <pre>: там код)."""
    h = re.sub(r'<pre.*?</pre>', '<pre></pre>', h, flags=re.S)
    h = re.sub(r'<svg.*?</svg>', '', h, flags=re.S)
    stack, bad = [], []
    for m in TOKEN.finditer(h):
        tag = m.group(1).lower()
        if tag not in PAIRED or m.group(0).endswith('/>'):
            continue
        if m.group(0).startswith('</'):
            if stack and stack[-1] == tag:
                stack.pop()
            elif tag in stack:
                bad.append('закрыт <%s> при открытых %s' % (tag, stack[stack.index(tag) + 1:]))
                del stack[stack.index(tag):]
            else:
                bad.append('лишний </%s>' % tag)
        else:
            stack.append(tag)
    if stack:
        bad.append('не закрыты: %s' % stack)
    return bad


def fields(u):
    for f in ('intro', 'result', 'why', 'html'):
        if isinstance(u.get(f), str):
            yield f, u[f]
    for i, d in enumerate(u.get('deep') or []):
        yield 'deep[%d]' % i, d.get('html', '')
    for i, q in enumerate(u.get('quiz') or []):
        yield 'quiz[%d]' % i, q
    if isinstance(u.get('outro'), dict):
        yield 'outro', u['outro'].get('html', '')


def audit(lab):
    L = json.JSONDecoder().raw_decode(bundle.load(os.path.join(ROOT, LABS[lab]))[len('window.LAB='):])[0]
    errs, warns = [], []
    units = L['units']
    keys = [u['key'] for u in units]
    if len(keys) != len(set(keys)):
        errs.append('повторяющиеся ключи: %s' % sorted({k for k in keys if keys.count(k) > 1}))
    byk = {u['key']: u for u in units}
    steps = [u for u in units if u['kind'] == 'step']
    nums = {u['num'] for u in steps}
    secs = {u['num'] for u in units if u['kind'] != 'step'}
    nsess = len(L.get('sessions') or [])
    # сессии
    seen = {}
    for s in L.get('sessions') or []:
        for k in s['steps']:
            if k not in byk:
                errs.append('сессия %s ссылается на несуществующий шаг %s' % (s['n'], k))
            elif byk[k].get('session') != s['n']:
                warns.append('шаг %s: session=%s, а в списке сессии %s' % (k, byk[k].get('session'), s['n']))
            seen[k] = seen.get(k, 0) + 1
    for u in steps:
        if u['key'] not in seen:
            errs.append('шаг %s не входит ни в одну сессию' % u['key'])
        elif seen[u['key']] > 1:
            errs.append('шаг %s входит в несколько сессий' % u['key'])
    for u in units:
        k = u['key']
        # пустое
        if u['kind'] == 'step':
            if not plain(u.get('intro')):
                errs.append('%s: пустой intro' % k)
            if 'why' in u and not plain(u.get('why')) and u.get('why') is not None and u['why'] != '':
                warns.append('%s: пустой why' % k)
        elif not plain(u.get('html')) and not u.get('gloss'):
            errs.append('%s «%s»: пустая страница раздела' % (k, u['title'][:40]))
        for d in u.get('deep') or []:
            if not plain(d.get('html')):
                errs.append('%s: пустой блок «Под капотом» «%s»' % (k, d.get('summary', '')[:30]))
        o = u.get('outro')
        if isinstance(o, dict) and not plain(o.get('html')):
            warns.append('%s: пустой итог «%s»' % (k, o.get('label')))
        qs = [plain(q) for q in u.get('quiz') or []]
        if len(qs) != len(set(qs)):
            errs.append('%s: повторяющиеся вопросы' % k)
        if any(not q for q in qs):
            errs.append('%s: пустой вопрос' % k)
        urls = [l.get('u') for l in u.get('links') or []]
        if len(urls) != len(set(urls)):
            errs.append('%s: повторяющиеся ссылки' % k)
        for l in u.get('links') or []:
            if not l.get('u', '').startswith('http') or not l.get('t'):
                errs.append('%s: ссылка без адреса/названия %r' % (k, l))
        # поля
        for f, h in fields(u):
            if not isinstance(h, str):
                continue
            for b in balance(h):
                errs.append('%s.%s: %s' % (k, f, b))
            for m in re.finditer(r'href="#([^"]+)"', h):
                t = m.group(1)
                if t.startswith('step-') and t not in byk:
                    errs.append('%s.%s: якорь #%s ведёт на несуществующий шаг' % (k, f, t))
                elif t.startswith('sec-') and t[4:] not in secs:
                    errs.append('%s.%s: якорь #%s ведёт на несуществующий раздел' % (k, f, t))
            t = plain(h)
            for m in re.finditer(r'(?:шаг[аеу]?|шагов)\s+(\d+\.\d+)', t, re.I):
                if m.group(1) not in nums:
                    warns.append('%s.%s: «%s» — такого шага нет' % (k, f, m.group(0)))
            for m in re.finditer(r'сесси[ийяюе]\s+(\d+)(?!\.\d)', t, re.I):
                if int(m.group(1)) > nsess:
                    warns.append('%s.%s: «%s» — в лабе %d сессий' % (k, f, m.group(0), nsess))
            for pat, what in ((r'Перед шагом', 'остаток «Перед шагом»'), (r'ПЕРЕД ШАГОМ', 'остаток «ПЕРЕД ШАГОМ»'), (r'\{\{|\}\}(?!\})', 'шаблонные скобки'),
                              (r'\bundefined\b(?!\s*[,;)\]=])', None), (r'\[object ', '[object …]'), (r'\bTODO\b|lorem ipsum', 'заглушка')):
                if what and re.search(pat, t if what != 'шаблонные скобки' else re.sub(r'<pre.*?</pre>', '', h, flags=re.S)) and f not in ('result',):
                    if what == 'шаблонные скобки' and lab in ('vue', 'nuxt', 'angular', 'laravel', 'laravel-performance', 'inertia', 'caddy', 'centrifugo', 'tailwind'):
                        continue
                    warns.append('%s.%s: %s' % (k, f, what))
        # повтор блоков внутри шага: два одинаковых абзаца/врезки подряд
        for f in ('intro', 'why'):
            h = u.get(f) if isinstance(u.get(f), str) else ''
            blocks = [plain(b) for b in re.findall(r'<(?:p|div class="(?:tip|trap)")[^>]*>.*?</(?:p|div)>', h, re.S)]
            blocks = [b for b in blocks if len(b) > 60]
            dup = {b[:70] for b in blocks if blocks.count(b) > 1}
            if dup:
                errs.append('%s.%s: повторяющиеся блоки %s' % (k, f, sorted(dup)))
        if u['kind'] == 'step':
            if len({plain(d.get('summary', '')) for d in u.get('deep') or []}) != len(u.get('deep') or []):
                warns.append('%s: одинаковые заголовки «Под капотом»' % k)
    # оглавление и вступление: якоря
    for f in ('tocHtml', 'introHtml'):
        for m in re.finditer(r'href="#([^"]+)"', L.get(f) or ''):
            t = m.group(1)
            if (t.startswith('step-') and t not in byk) or (t.startswith('sec-') and t[4:] not in secs):
                errs.append('%s: якорь #%s ведёт в никуда' % (f, t))
    # глоссарий
    for u in units:
        g = u.get('gloss')
        if isinstance(g, list):
            terms = [x.get('term', '').strip().lower() for x in g]
            if any(not x.get('term') or not plain(x.get('def')) for x in g):
                errs.append('%s: в глоссарии пустой термин или определение' % u['key'])
            dup = {t for t in terms if terms.count(t) > 1}
            if dup:
                warns.append('%s: повторяющиеся термины глоссария %s' % (u['key'], sorted(dup)[:5]))
    # один и тот же заголовок у разных разделов
    ts = [u['title'] for u in units if u['kind'] != 'step']
    for t in set(ts):
        if ts.count(t) > 1:
            warns.append('повторяющийся заголовок раздела «%s»' % t[:50])
    return errs, warns


def main():
    labs = [a for a in sys.argv[1:] if not a.startswith('--')] or [k for k in LABS if k not in SKIP]
    total_e = 0
    for lab in labs:
        errs, warns = audit(lab)
        total_e += len(errs)
        print('%-22s ошибок %-3d предупреждений %d' % (lab, len(errs), len(warns)))
        for e in errs[:40]:
            print('   ✖', e[:240])
        if '--warn' in sys.argv:
            for w in warns[:40]:
                print('   ·', w[:240])
    sys.exit(1 if total_e else 0)


if __name__ == '__main__':
    main()
