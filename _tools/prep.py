"""Готовит методичку к вычитке агентами.

Запуск из корня репозитория:
    python3 fixes/_tools/prep.py <лаба> <папка_вывода>
Пример:
    python3 fixes/_tools/prep.py kubernetes /tmp/proof-kubernetes

Создаёт в папке вывода:
    part_01.txt, part_02.txt, … — текст методички кусками по ~20 тыс. символов
    pre_blocks.txt             — все блоки кода <pre> с заголовком раздела над каждым
"""
import html
import os
import re
import sys
from html.parser import HTMLParser

LABS = {
    'redis': 'redis/Redis_Lab_Plan.html',
    'traefik': 'traefik/Docker_and_Traefik_Lab_Plan.html',
    'vue': 'vue/Vue_Lab_Helpdesk.html',
    'typescript': 'typescript/TypeScript_Lab_Warehouse.html',
    'laravel': 'laravel/Laravel_Lab_TaskFlow.html',
    'docker': 'docker/Docker_Bash_Lab.html',
    'php': 'php/PHP_Lab_VanillaCoffee.html',
    'js': 'js/JS_Lab_VanillaHelpdesk.html',
    'kubernetes': 'kubernetes/Kubernetes_Lab_Plan.html',
    'nestjs': 'nestjs/NestJS_Lab_Plan.html',
    'graphql': 'graphql/GraphQL_Lab_Plan.html',
    'php-coffee': 'php-coffee/docs/OOP_Lab_CoffeeShop.html',
    'rabbitmq': 'rabbitmq/docs/RabbitMQ_Lab_Plan_v1_pro_max.html',
    'postgresql': 'postgresql/PostgreSQL_Lab_CoffeeShop.html',
}
PART = 20000


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
    p.feed(open(LABS[lab], encoding='utf-8').read())
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
