# -*- coding: utf-8 -*-
"""Перевод методички старого формата в формат Caddy (стандарт 12–13.10.2026): без инлайн-стилей, врезки .tip/.trap,
блоки кода pre[data-lang], «Почитать» — в поле links следующего шага, outro только в конце сессии, у шагов short/est.

Запуск из корня репозитория:
    python3 fixes/common/_tools/to_caddy.py <лаба>            — сухой прогон: отчёт, файл не меняется
    python3 fixes/common/_tools/to_caddy.py <лаба> --write    — записать (через bundle.transform)

Ключи разделов и шагов НЕ меняются (по ним хранится прогресс). Язык блоков кода угадывается эвристикой (только подпись).
Недостающие quiz пишутся отдельно (по тексту шага) — здесь они только считаются.
"""
import html as H, json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bundle

TOK = re.compile(r'(<!--.*?-->|</?[A-Za-z][^>]*>|[^<]+|<)', re.S)
TAG = re.compile(r'<(/?)([A-Za-z][\w:-]*)(.*?)(/?)>$', re.S)
STYLE = re.compile(r'\sstyle="[^"]*"')
VOID = {'br', 'img', 'hr', 'input', 'meta', 'link', 'wbr'}
TRAP_WORDS = ('ЛОВУШ', 'ОШИБК', 'ВНИМАН', 'ОСТОРОЖ', 'ОПАСН', 'ГРАБЛ', 'ПРЕДУПРЕЖД', 'НЕ ДЕЛАЙ')


def _plain(h):
    return re.sub(r'\s+', ' ', H.unescape(re.sub(r'<[^>]+>', ' ', h or ''))).strip()


def _style_of(attrs):
    m = re.search(r'\sstyle="([^"]*)"', attrs)
    return re.sub(r'\s+', ' ', m.group(1)) if m else ''


def guess_lang(code):
    t = H.unescape(code).strip()
    first = t.split('\n', 1)[0].strip()
    if t.startswith('<?php') or (re.search(r'\$this->|->\w+\(|namespace \w|use App\\|function \w+\(|public function|Schema::|Route::', t) and ';' in t):
        return 'php'
    if re.match(r'^(\$ |#!|docker |composer |php artisan|npm |npx |pnpm |yarn |cd |mkdir |curl |git |cat |ls |cp |mv |sudo |brew |echo |export |make |node |nest |ng |vite |k6 |kubectl |helm |kind )', first):
        return 'bash'
    if re.match(r'^(FROM |RUN |COPY |WORKDIR |CMD |ENTRYPOINT )', first):
        return 'dockerfile'
    if re.match(r'^(SELECT |INSERT |UPDATE |DELETE |CREATE |ALTER |DROP |WITH |EXPLAIN )', first, re.I):
        return 'sql'
    if re.match(r'^(<template|<script setup|<script lang)', first):
        return 'vue'
    if first.startswith(('{', '[')) and t.rstrip().endswith(('}', ']')) and '"' in t:
        return 'json'
    if re.match(r'^(services:|version:|name:|on:|apiVersion:|kind:|jobs:)', first):
        return 'yaml'
    if re.match(r'^(import |export |const |let |type |interface |class |@\w+|enum |declare )', first) or '=>' in t:
        return 'ts' if re.search(r': (string|number|boolean|void)|interface |<T>|@Component|@Injectable', t) else 'js'
    if first.startswith('<') or re.match(r'^<!doctype', first, re.I):
        return 'html'
    if re.match(r'^[\w.#@:\[\]>*, -]+\{', first):
        return 'css'
    return 'text'


def callout_kind(tag, st):
    if tag != 'div':
        return False
    return (('padding:14px 18px' in st and 'background:var(--fill)' in st)
            or ('padding:18px 20px' in st and 'border:2px' in st)
            or ('padding:24px 28px' in st and 'background:var(--color-accent)' in st)
            or ('padding:16px 18px' in st and 'border:2px solid var(--color-accent)' in st))


def convert_html(h, field=''):
    """Строка html со style="..." -> чистая вёрстка. Токенный проход со стеком открытых тегов (терпим к кривой разметке)."""
    if not isinstance(h, str) or 'style="' not in h:
        return h
    toks = [t for t in TOK.findall(h) if t != '']
    out, stack = [], []          # stack: (имя тега, закрывающий тег для вывода, это метка?)
    i, n = 0, len(toks)
    in_label, first_text = 0, False
    while i < n:
        t = toks[i]
        m = TAG.match(t) if (t.startswith('<') and len(t) > 1 and not t.startswith('<!--')) else None
        if not m:
            if in_label and not t.startswith('<'):
                t = t.lower()
                if first_text and t.strip():
                    t = t[:1].upper() + t[1:]
                    first_text = False
            out.append(t); i += 1; continue
        closing, name, attrs, selfclose = m.group(1), m.group(2), m.group(3), m.group(4)
        low = name.lower()
        if closing:
            for k in range(len(stack) - 1, -1, -1):
                if stack[k][0] == low:
                    endtag, was_label = stack[k][1], stack[k][2]
                    if was_label:
                        in_label -= 1
                    del stack[k:]
                    out.append(f'</{endtag}>')
                    break
            else:
                out.append(t)
            i += 1; continue
        st = _style_of(attrs)
        newname, newattrs, endname, label = name, attrs, name, False
        if st:
            if low == 'pre':
                j, buf = i + 1, []
                while j < n and not re.match(r'</pre\s*>', toks[j], re.I):
                    buf.append(toks[j]); j += 1
                code = re.sub(r'<[^>]+>', '', ''.join(buf))
                is_out = field == 'result' or ('padding:16px 18px' not in st and 'background' not in st and 'font-family' in st)
                newattrs = ' class="out" data-lang="out"' if is_out else ' class="" data-lang="%s"' % guess_lang(code)
            elif low == 'span' and 'text-transform:uppercase' in st:
                newname, endname, newattrs, label = 'b', 'b', '', True
            elif low == 'span' and "font-family:'JetBrains Mono'" in st:
                newname, endname, newattrs = 'code', 'code', ''
            elif callout_kind(low, st):
                j = i + 1
                while j < n and toks[j].strip() == '':
                    j += 1
                lab = ''
                if j < n and re.match(r'<span\b', toks[j]) and 'text-transform:uppercase' in toks[j]:
                    k = j + 1
                    while k < n and not re.match(r'</span\s*>', toks[k], re.I):
                        if not toks[k].startswith('<'):
                            lab += toks[k]
                        k += 1
                newattrs = ' class="%s"' % ('trap' if any(w in lab.upper() for w in TRAP_WORDS) else 'tip')
            else:
                newattrs = STYLE.sub('', attrs)
            newattrs = STYLE.sub('', newattrs)
        if label:
            first_text = True
            in_label += 1
        out.append(f'<{newname}{newattrs}{"/" if selfclose else ""}>')
        if low not in VOID and not selfclose:
            stack.append((low, endname, label))
        i += 1
    return ''.join(out)


def _est(mins):
    return '~%d мин' % max(10, int(round(mins / 5.0)) * 5)


def _minutes(txt):
    m = re.search(r'(\d+(?:[.,]\d+)?)\s*(?:[–-]\s*(\d+(?:[.,]\d+)?))?\s*(ч|час|мин)', txt or '')
    if not m:
        return 0
    a = float(m.group(1).replace(',', '.')); b = float(m.group(2).replace(',', '.')) if m.group(2) else a
    v = (a + b) / 2
    return v * 60 if m.group(3) in ('ч', 'час') else v


def _short(title):
    if len(title) <= 48:
        return title
    c = title.split(':')[0].strip()
    return c if 10 <= len(c) <= 48 else title[:45].rstrip() + '…'


def _links_from(h):
    """<li>Почитать: <a href>Название</a> — описание.</li> -> ([{u,n,t}], остальные li)."""
    links, rest = [], []
    for li in re.findall(r'<li>(.*?)</li>', h, re.S):
        anchors = re.findall(r'<a href="([^"]+)"[^>]*>(.*?)</a>', li, re.S)
        if anchors and re.match(r'\s*(Почитать|Посмотреть|Документация)', _plain(li)):
            tail = _plain(re.sub(r'^.*</a>', '', li, flags=re.S))
            tail = re.sub(r'^[\s—–\-:]+', '', tail).rstrip('.').strip()
            for u, t in anchors:
                links.append({'u': u, 'n': tail if len(anchors) == 1 else '', 't': _plain(t)})
        else:
            rest.append(li)
    return links, rest


def _add_links(step, links):
    cur = step.get('links') or []
    have = {l['u'] for l in cur}
    step['links'] = cur + [l for l in links if l['u'] not in have]


def convert_lab(L, report):
    steps = [u for u in L['units'] if u.get('kind') == 'step']
    nums = {u['num']: u for u in steps}
    first_of_session = {}
    for u in steps:
        first_of_session.setdefault(u['session'], u)
    for u in steps:
        o = u.get('outro')
        if not isinstance(o, dict):
            continue
        o_html = convert_html(o.get('html', ''), 'outro')
        label = o.get('label', '')
        mm = re.match(r'\s*ПЕРЕД ШАГОМ\s+(\d+\.\d+)', label, re.I)
        ms = re.match(r'\s*ИТОГ СЕССИИ\s+(\d+)(?:\s*→\s*ПЕРЕД СЕССИЕЙ\s+(\d+))?', label, re.I)
        mp = re.match(r'\s*ПЕРЕД СЕССИЕЙ\s+(\d+)', label, re.I)
        if mm or mp:
            links, rest = _links_from(o_html)
            tgt = nums.get(mm.group(1)) if mm else first_of_session.get(int(mp.group(1)))
            if tgt is None or rest or not links:
                report['outro_manual'].append((u['key'], label, len(links), len(rest)))
                u['outro'] = {'label': label, 'html': o_html}
                continue
            _add_links(tgt, links)
            u['outro'] = None
        elif ms and '<li>' not in o_html:
            u['outro'] = {'label': 'Итог сессии %s' % ms.group(1), 'html': o_html}
        elif ms:
            links, rest = _links_from(o_html)
            if links:
                tgt = first_of_session.get(int(ms.group(2))) if ms.group(2) else None
                if tgt is not None:
                    _add_links(tgt, links)
                else:
                    report['dropped_links'].append((u['key'], [l['u'] for l in links]))
            body = '<ul>' + ''.join('<li>%s</li>' % x for x in rest) + '</ul>' if rest else ''
            u['outro'] = {'label': 'Итог сессии %s' % ms.group(1), 'html': body}
        elif re.match(r'\s*Конец сессии', label, re.I):
            u['outro'] = {'label': 'Итог сессии %d' % u['session'], 'html': o_html}
        else:
            u['outro'] = {'label': label, 'html': o_html}
            report['outro_kept'].append((u['key'], label))
    for u in L['units']:
        for f in ('intro', 'result', 'why', 'html'):
            if isinstance(u.get(f), str):
                u[f] = convert_html(u[f], f)
        for d in u.get('deep') or []:
            d['html'] = convert_html(d.get('html', ''), 'deep')
            if isinstance(d.get('summary'), str):
                d['summary'] = convert_html(d['summary'], 'deep')
        if isinstance(u.get('quiz'), list):
            u['quiz'] = [convert_html(q, 'quiz') for q in u['quiz']]
    for k in ('introHtml', 'tocHtml', 'subtitle'):
        if isinstance(L.get(k), str):
            L[k] = convert_html(L[k], k)
    dur = {s['n']: _minutes(s.get('dur', '')) for s in L.get('sessions', [])}
    cnt = {}
    for u in steps:
        cnt[u['session']] = cnt.get(u['session'], 0) + 1
    for u in L['units']:
        if not u.get('short'):
            u['short'] = _short(u['title'])
        if u.get('kind') == 'step' and not u.get('est'):
            mins = dur.get(u['session']) or 0
            u['est'] = _est(mins / cnt[u['session']] if mins else 30)
    for u in steps:
        parts = [u['title'], 'Шаг %s. %s' % (u['num'], u['title']), _plain(u.get('intro')), _plain(u.get('result')), _plain(u.get('why'))]
        for d in u.get('deep') or []:
            parts.append(_plain(d.get('summary', '')) + ' ' + _plain(d.get('html', '')))
        parts += [_plain(q) for q in u.get('quiz') or []]
        if isinstance(u.get('outro'), dict):
            parts.append(u['outro'].get('label', '') + ' ' + _plain(u['outro'].get('html', '')))
        for l in u.get('links') or []:
            parts.append('Почитать: ' + l['t'])
        u['text'] = re.sub(r'\s+', ' ', ' '.join(parts)).strip()
    return L


TIP_CSS = ('\\n.tip,.trap{border:2px solid var(--ink);border-left-width:8px;border-left-color:var(--color-accent);background:var(--fill);padding:14px 18px;margin:20px 0}'
           '\\n.trap{border-left-color:#d9480f}\\n.tip>b,.trap>b{display:block;margin-bottom:6px;font-size:16px}\\n.tip p,.trap p{margin:8px 0}\\n.tip table,.trap table{margin:10px 0}')


TABLE_CSS = ('\\ntable{border-collapse:collapse;width:100%;font-size:14px;margin:0 0 20px;line-height:1.5}'
             '\\nth,td{padding:8px 14px 8px 0;border-bottom:1px solid var(--hair);vertical-align:top;text-align:left}'
             '\\nth{border-bottom:2px solid var(--ink);font-weight:800;vertical-align:bottom}')


def ensure_css(path):
    """Добавляет в шаблон страницы стили врезок .tip/.trap и таблиц (в старых методичках таблицы были со style=…, без них
    остались бы браузерные «голые» таблицы). Якорь — правило pre; у разных групп шаблонов он разный."""
    s = open(path, encoding='utf-8').read()
    raw = re.search(r'<script type="__bundler/template">(.*?)</script>', s, re.S).group(1)
    res = []
    has_tip = '.tip,.trap{' in raw
    if 'th,td{padding:8px 14px 8px 0' not in raw:
        if has_tip:
            ok = bundle.patch_template(path, '\\n.tip,.trap{', TABLE_CSS + '\\n.tip,.trap{')
        else:
            ok = 0
            for old in ('pre{max-width:100%;overflow-x:auto}<\\u002Fstyle>', 'overflow-x:auto}\\n<\\u002Fstyle>'):
                pre = old.split('<\\u002Fstyle>')[0]
                if bundle.patch_template(path, old, pre + TABLE_CSS + ('' if old.startswith('pre') else '\\n') + '<\\u002Fstyle>'):
                    ok = 1
                    break
        res.append('таблицы: добавлено' if ok else 'таблицы: НЕ УДАЛОСЬ добавить')
    s = open(path, encoding='utf-8').read()
    raw = re.search(r'<script type="__bundler/template">(.*?)</script>', s, re.S).group(1)
    if '.tip,.trap{' not in raw:
        ok = 0
        for old in ('th{border-bottom:2px solid var(--ink);font-weight:800;vertical-align:bottom}<\\u002Fstyle>', 'th{border-bottom:2px solid var(--ink);font-weight:800;vertical-align:bottom}\\n<\\u002Fstyle>'):
            pre = old.split('<\\u002Fstyle>')[0]
            if bundle.patch_template(path, old, pre + TIP_CSS + ('\\n' if '\\n<' in old else '') + '<\\u002Fstyle>'):
                ok = 1
                break
        res.append('врезки: добавлено' if ok else 'врезки: НЕ УДАЛОСЬ добавить')
    return '; '.join(res) or 'всё уже есть'


def main():
    lab = sys.argv[1]
    write = '--write' in sys.argv
    path = f'{lab}/{lab}.html'
    txt = bundle.load(path)
    L, end = json.JSONDecoder().raw_decode(txt[len('window.LAB='):])
    old = json.loads(json.dumps(L))
    report = {'outro_manual': [], 'outro_kept': [], 'dropped_links': []}
    L = convert_lab(L, report)
    new_txt = 'window.LAB=' + json.dumps(L, ensure_ascii=False, separators=(',', ':')) + txt[len('window.LAB=') + end:]
    d = json.dumps(L, ensure_ascii=False)
    assert [u['key'] for u in L['units']] == [u['key'] for u in old['units']], 'порядок/ключи изменились'
    assert [s['steps'] for s in L['sessions']] == [s['steps'] for s in old['sessions']], 'состав сессий изменился'
    steps = [u for u in L['units'] if u.get('kind') == 'step']
    changed = []
    for a, b in zip(old['units'], L['units']):
        for f in ('intro', 'result', 'why', 'html'):
            if isinstance(a.get(f), str) and _plain(a[f]).lower() != _plain(b[f]).lower():
                changed.append((a['key'], f))
        for x, y in zip(a.get('quiz') or [], b.get('quiz') or []):
            if _plain(x).lower() != _plain(y).lower():
                changed.append((a['key'], 'quiz'))
        for x, y in zip(a.get('deep') or [], b.get('deep') or []):
            if _plain(x['html']).lower() != _plain(y['html']).lower():
                changed.append((a['key'], 'deep'))
    print(f'{lab}: шагов {len(steps)}, сессий {len(L["sessions"])}, инлайн-стилей осталось {d.count(chr(115)+"tyle=" + chr(92) + chr(34))}')
    print('  без quiz:', [u['key'] for u in steps if not u.get('quiz')])
    print('  без links:', len([u for u in steps if not u.get('links')]), 'из', len(steps))
    print('  текст изменился в полях (должно быть пусто):', changed[:10], len(changed))
    print('  outro, нужна ручная проверка:', report['outro_manual'])
    print('  outro оставлены как есть:', report['outro_kept'])
    print('  ссылки без адресата:', report['dropped_links'])
    last = {s['steps'][-1] for s in L['sessions']}
    print('  сессии без outro:', [u['session'] for u in steps if u['key'] in last and not u.get('outro')])
    print('  outro не в конце сессии:', [u['key'] for u in steps if u.get('outro') and u['key'] not in last])
    if write:
        bundle.transform(path, lambda old_: new_txt)
        print('записано', path)
        print('стили .tip/.trap в шаблоне:', ensure_css(path))


if __name__ == '__main__':
    main()
