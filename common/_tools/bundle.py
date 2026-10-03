"""Читает и правит методички-«бандлы» (редизайн 02.10.2026: текст лежит в сжатом JSON внутри HTML).

Запуск из корня репозитория:
    python3 fixes/common/_tools/bundle.py dump <html> [out.txt]     — текст методички (window.LAB=...) в файл/stdout
    python3 fixes/common/_tools/bundle.py grep <html> <regex>       — строки-совпадения (с контекстом)
    (из Python: bundle.rewrite(path, [(regex, замена), ...]) — пакетная замена по регулярке)
    python3 fixes/common/_tools/bundle.py sub  <html> <старое> <новое> [--count N]
                                                                     — точная замена строки внутри методички и перепаковка
"""
import base64, gzip, json, re, sys

def _find(s):
    m = re.search(r'<script type="__bundler/manifest">(.*?)</script>', s, re.S)
    man = json.loads(m.group(1))
    for k, v in man.items():
        if v['mime'].endswith('javascript'):
            raw = base64.b64decode(v['data'])
            txt = (gzip.decompress(raw) if v.get('compressed') else raw).decode('utf-8')
            if txt.startswith('window.LAB='):
                return v, txt
    raise SystemExit('window.LAB не найден')

def load(path):
    return _find(open(path, encoding='utf-8').read())[1]

def sub(path, old, new, count=None):
    s = open(path, encoding='utf-8').read()
    v, txt = _find(s)
    n = txt.count(old)
    if not n:
        return 0
    if count is not None and n != count:
        raise SystemExit(f'ожидали {count} вхождений, найдено {n}: {old!r}')
    new_txt = txt.replace(old, new)
    data = gzip.compress(new_txt.encode('utf-8'), mtime=0) if v.get('compressed') else new_txt.encode('utf-8')
    b64 = base64.b64encode(data).decode()
    assert s.count(v['data']) == 1
    open(path, 'w', encoding='utf-8').write(s.replace(v['data'], b64))
    assert load(path) == new_txt
    return n

def patch_template(path, old, new, count=1):
    """Правка сырого шаблона страницы (__bundler/template: HTML+CSS страницы методички). Слэш в нём записан как \\u002F."""
    s = open(path, encoding='utf-8').read()
    m = re.search(r'(<script type="__bundler/template">)(.*?)(</script>)', s, re.S)
    raw = m.group(2)
    if raw.count(old) < 1:
        return 0
    new_raw = raw.replace(old, new, count)
    json.loads(new_raw)   # остаётся валидной JSON-строкой
    open(path, 'w', encoding='utf-8').write(s[:m.start(2)] + new_raw + s[m.end(2):])
    return 1


def rewrite(path, pairs):
    """pairs: список (regex, замена). Возвращает {regex: число замен}. Пакует обратно."""
    s = open(path, encoding='utf-8').read()
    v, txt = _find(s)
    stats, new_txt = {}, txt
    for rx, rep in pairs:
        new_txt, n = re.subn(rx, rep, new_txt)
        stats[rx] = n
    if new_txt != txt:
        data = gzip.compress(new_txt.encode('utf-8'), mtime=0) if v.get('compressed') else new_txt.encode('utf-8')
        assert s.count(v['data']) == 1
        open(path, 'w', encoding='utf-8').write(s.replace(v['data'], base64.b64encode(data).decode()))
        assert load(path) == new_txt
    return stats

if __name__ == '__main__':
    cmd, path = sys.argv[1], sys.argv[2]
    if cmd == 'dump':
        t = load(path)
        open(sys.argv[3], 'w').write(t) if len(sys.argv) > 3 else print(t)
    elif cmd == 'grep':
        for m in re.finditer('.{0,60}(?:%s).{0,60}' % sys.argv[3], load(path)):
            print(m.group(0))
    elif cmd == 'sub':
        c = int(sys.argv[sys.argv.index('--count') + 1]) if '--count' in sys.argv else None
        print(sub(path, sys.argv[3], sys.argv[4], c), 'замен')
