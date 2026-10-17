# -*- coding: utf-8 -*-
"""post.py <lab> <changelog-текст> <state-log-текст>: добавляет запись в changelog 17.10 и в журнал (этап B)."""
import sys,re
lab,cl,sl=sys.argv[1:4]
p='works/changelog.html'
s=open(p,encoding='utf-8').read()
i=s.index("title:'Обложки Laravel, RabbitMQ и Vue")
j=s.index("\n]},",i)
item="\n  {lab:'%s', type:'changed', text:'%s'},"%(lab,cl.replace("'","\\'"))
s=s[:j]+item+s[j:]
open(p,'w',encoding='utf-8').write(s)
p='fixes/common/_state-log.md'
t=open(p,encoding='utf-8').read()
hdr="### 17.10.2026 (позже) — этап B: перевод лаб в формат Caddy (по одной, отдельными коммитами)"
if hdr not in t:
    a="### 17.10.2026 (позже) — этап A"
    t=t.replace(a,hdr+"\n- Инструмент: `fixes/common/_tools/to_caddy.py <лаба> [--write]` (сухой прогон по умолчанию; ключи шагов не меняет, сам проверяет порядок ключей и состав сессий, сравнивает видимый текст до/после). Ответы на вопросы «Проверь себя» и `outro` конца сессии, которых не хватало, пишет ассистент по тексту шага; `est` — деление времени сессии на число шагов (владелец правит при прохождении).\n\n"+a,1)
t=t.replace(hdr+"\n","%s\n- **%s:** %s\n"%(hdr,lab,sl) if False else hdr+"\n",1)
# вставляем строку лабы сразу после первой строки «Инструмент»
k=t.index(hdr); e=t.index("\n\n",k)
t=t[:e]+"\n- **%s:** %s"%(lab,sl)+t[e:]
open(p,'w',encoding='utf-8').write(t)
