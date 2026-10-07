"""Готовит методичку к вычитке агентами.

Запуск из корня репозитория:
    python3 fixes/common/_tools/prep.py <лаба> <папка_вывода>
Пример:
    python3 fixes/common/_tools/prep.py kubernetes /tmp/proof-kubernetes

Создаёт в папке вывода:
    part_01.txt, part_02.txt, … — текст методички кусками по ~20 тыс. символов
    pre_blocks.txt             — все блоки кода <pre> с заголовком раздела над каждым
"""
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

LABS = {
    'redis': 'redis/redis.html',
    'traefik': 'traefik/traefik.html',
    'vue': 'vue/vue.html',
    'typescript': 'typescript/typescript.html',
    'laravel': 'laravel/laravel.html',
    'docker': 'docker/docker.html',
    'php': 'php/php.html',
    'js': 'js/js.html',
    'kubernetes': 'kubernetes/kubernetes.html',
    'nestjs': 'nestjs/nestjs.html',
    'graphql': 'graphql/graphql.html',
    'php-coffee': 'php-coffee/php-coffee.html',
    'rabbitmq': 'rabbitmq/rabbitmq.html',
    'postgresql': 'postgresql/postgresql.html',
    'nuxt': 'nuxt/nuxt.html',
    'angular': 'angular/angular.html',
    'css': 'css/css.html',
    'tailwind': 'tailwind/tailwind.html',
    'inertia': 'inertia/inertia.html',
    'laravel-performance': 'laravel-performance/laravel-performance.html',
    'algorithms-php': 'algorithms-php/algorithms-php.html',
    'caddy': 'caddy/caddy.html',
    'go-start': 'go-start/go-start.html',
    'go-pro': 'go-pro/go-pro.html',
}
PART = 20000


def read_lab(path):
    """Методички после редизайна 02.10.2026 — «бандлы»: текст лежит в сжатом JSON (см. bundle.py).
    Собираем из него обычный HTML: введение + разделы с заголовками."""
    raw = open(path, encoding='utf-8').read()
    if '__bundler/manifest' not in raw:
        return raw
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import bundle
    txt = bundle.load(path)
    lab, _ = json.JSONDecoder().raw_decode(txt[len('window.LAB='):])
    def strings(v):
        if isinstance(v, str):
            yield v
        elif isinstance(v, dict):
            for x in v.values():
                yield from strings(x)
        elif isinstance(v, list):
            for x in v:
                yield from strings(x)

    out = [lab.get('introHtml', '')]
    for u in lab['units']:
        body = u.get('html', '')
        if u.get('kind') == 'step':   # шаги: код и пояснения лежат в intro / why / deep / quiz / result / outro
            body = ''.join(f'<div>{x}</div>' for k in ('intro', 'why', 'result', 'deep', 'quiz', 'outro') for x in strings(u.get(k)))
        out.append(f"<h2>{u.get('num', '')} {u.get('title', '')}</h2>{body}")
    return '\n'.join(out)


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.blocks = []
        self.skip = 0
        self.head = ''
        self.in_head = None
        self.pre_depth = 0
        self.pre = None

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip += 1
        if tag in ('h2', 'h3', 'h4'):
            self.in_head = ''
        if tag == 'pre':
            self.pre_depth += 1
            if self.pre_depth == 1:
                self.pre = ''

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip -= 1
        if tag in ('h2', 'h3', 'h4') and self.in_head is not None:
            self.head = self.in_head.strip()[:90]
            self.in_head = None
        if tag == 'pre':
            self.pre_depth -= 1
            if self.pre_depth == 0 and self.pre is not None:
                self.blocks.append((self.head, self.pre))
                self.pre = None

    def handle_data(self, data):
        if self.skip:
            return
        self.text.append(data)
        if self.in_head is not None:
            self.in_head += data
        if self.pre is not None:
            self.pre += data


def main():
    lab, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    p = Parser()
    p.feed(read_lab(LABS[lab]))
    text = re.sub(r'\s+', ' ', html.unescape(''.join(p.text)))

    parts, i = [], 0
    while i < len(text):
        j = min(len(text), i + PART)
        if j < len(text):
            k = text.rfind('. ', i + PART - 2000, j)
            if k > 0:
                j = k + 1
        parts.append(text[i:j])
        i = j
    for n, part in enumerate(parts, 1):
        with open(os.path.join(out, f'part_{n:02d}.txt'), 'w', encoding='utf-8') as f:
            f.write(part)

    with open(os.path.join(out, 'pre_blocks.txt'), 'w', encoding='utf-8') as f:
        for n, (head, body) in enumerate(p.blocks, 1):
            f.write(f'===== BLOCK {n} | под заголовком: {head}\n{body.rstrip()}\n\n')
    print(lab, 'parts:', len(parts), 'pre blocks:', len(p.blocks))


main()
