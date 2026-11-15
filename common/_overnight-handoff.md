# Передача работы: ночной автономный проход 14–15.11.2026

Составлено 15.11.2026 около 11:00. Кто продолжает — читает этот файл целиком, затем `fixes/common/_state-log.md` (записи за 14–15.11 сверху) и `CLAUDE.md` в корне репозитория.

## Где что лежит

- Рабочая ветка везде: **`auto/overnight-14-11`** (родитель `anitech-performance` и подмодули, которых коснулась работа). В `main` ничего не мерджили и не пушили, force-push не использовали. Вопрос «мерджить ли ветку в main — целиком или по лабам» решает владелец (она спит/занята; не мерджить самим).
- Сайт и деплой работают из `main`, поэтому ветка безопасна. Указатели подмодулей в родителе на ветке смотрят на коммиты веток подмодулей (они есть на GitHub).
- Рабочая папка (временные файлы, стенды, скрипты) — `/private/tmp/claude-501/-Users-mira-Documents-projects-lab-laroboti/51daccf6-ec3c-49ac-8893-9ddb49203ef7/scratchpad/` (после перезагрузки Mac может исчезнуть; ничего ценного там нет, всё важное закоммичено). Полезные скрипты: `step.py` (печать текста шагов: `python3 step.py <html> step-N-M`), `dumpsteps.py`, `rebuild.py` (пересборка поля `text` шага из полей; применять только если `build(u)==u['text']`), `port.py` (раскладка php-блоков по файлам), `rec_*.py` (образцы записи результатов агентов в журналы), `edit_*.py` (образцы правок методичек через `bundle.transform`), `pw/` (Playwright, `chk4.mjs` — проверка видимого текста; Chromium `~/Library/Caches/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-mac-arm64/chrome-headless-shell`).

## Что сделано (всё записано в `fixes/<направление>/<лаба>.md`, `_state-log.md`, `works/changelog.html`, закоммичено и запушено в ветку)

- Статус ✅: Tailwind (7–9), php-coffee (6–9), Bash (вычитка + перегон 163 блоков), Express (оба открытых пункта закрыты, прогон 1→18 повторён; вычитка 1–8, 10, 19).
- RabbitMQ: сессии 7–10 и шаги 2.3–2.4, 9.2 проверены на живом брокере; «Проверь себя» в 28 шагах; статус остаётся 🟡 (не проверены 9.3, 10.3, итоговое ТЗ).
- Centrifugo: сессии 1–3 прогнаны (🟡), дальше 4–21.
- Результаты («Ожидаемый результат») вписаны: GraphQL (все шаги с запросами), Redis 1.4/1.6/2.3, Laravel 10.3–10.4, TypeScript 1.1/5.4/9.1, Vue 1.1/5.4, PHP (2.1, 2.3, 3.3, 6.3, 8.3, 9.3), Laravel Performance 6.5.
- Схемы: Angular (16), GraphQL (12).
- Вычитка без запуска: Inertia/GraphQL/Angular сессии 1–6, laravel-performance, php, js, postgresql («Проверь себя» вместо «Тренировки» в 44 шагах), Docker Actions, Nuxt/algorithms (проверены, правок не потребовалось).

## Что осталось (по приоритету)

1. **Агенты, остановленные лимитом ~06:25 (сброс был в 10:50)** — их работа сохранена в подмодулях (проверить `git -C <подмодуль> log --oneline -5`, `git status`; незапушенное запушить). Продолжить с того места (новым агентом, если старых нет в `ListAgents`):
   - **Kubernetes** (`kubernetes/`): прогон 16 сессий в Docker (kind), вписывание настоящего вывода вместо «вывод не получен»; генератор `python3 tools/build-manual.py kubernetes --allow-missing`, исходники `kubernetes/src/*.md`; один кластер за раз.
   - **Centrifugo** (`centrifugo/`): сессии 4–21 (с шага 4.1), стенд сессий 1–3 — `scratchpad/agent-centrifugo/rw`; у этой лабы `text` шага = intro+result+why+deep (используй `scratchpad/agent-centrifugo/build2.py`); сверить «два флага» (аноним/клиент) в 7.5 и 8A.
   - **Inertia** (`inertia/`): «Ожидаемые результаты» шагов 2.1, 3.1, 4.1–4.3, 5.1–5.5 + «нужен прогон»: 1.4 (appName), 2.3 (номер строки SiteLayout), 2.1/3.1 (недостающие `use` в Factory/Resource); часть правок уже в локальных коммитах (проверить `git -C inertia log origin/auto/overnight-14-11..HEAD`).
   - **Laravel** (`laravel/`): t46 закрыт 15.11 (срез 5.3, 6.1, 6.3, 7.1, 7.2, 9.x прогнан, коммит `a7f9e5d`); осталось прогнать шаги 1.1–5.2, 6.2, 6.4, 7.3–8.3 (результаты 8.x иллюстративные); решение владельца — закреплять ли Vite 7 в 6.3.
   - **RabbitMQ задания 6.3/9.3/10.3**: проверить, что сценарии «Production Hell» воспроизводятся как описано (стенды `scratchpad/rmq`, `rmqlab`, `promlab`).
   - **Nuxt t45**: прод-сборка, `nuxt-security`, WebSocket/SSE за прокси, ссылки i18n.nuxt.com.
2. Результаты Inertia/TS/Vue и т. д. — что ещё пусто: Inertia 2.1–5.5; у старых шагов PostgreSQL вывод лежит в тексте (старый формат); итоговые ТЗ без ответа — не решать.
3. Мелкие дела из `fixes/common/_todo.json` (открытые): t05 Caddy (две копии на одном порту), t43 CSS (другие браузеры), t45 Nuxt, t48 Inertia (хвост находок 04.10), t102 (вводные разделы в оглавлении шести лаб), t103 Inertia (PHP 8.4, SSR-сборка), Go Start / Go Pro — не трогать.
4. Из отчётов агентов — не правилось, нужны решения владельца: единый словарь кодов ошибок в Express (5.4 против 11.1), дубль Express 18.1 ↔ 6.1; в Laravel 7.2/9.2 — см. выше.

## Правила (из CLAUDE.md и ночных уроков)

- Порядок после правки: запись в `fixes/<направление>/<лаба>.md` → `_verification.md` (только если статус реально меняется) → README лабы и строка в `CLAUDE.md` → новый пункт в `works/changelog.html` (день `2026-11-15`) → запись в `fixes/common/_state-log.md` (новые сверху) → `python3 tools/build-verification.py && python3 tools/build-progress.py && python3 tools/build-seo.py && python3 tools/check-site.py` (должно быть «OK») → коммит в подмодулях (`git add` конкретных файлов), push ветки → сверить `HEAD == origin/auto/overnight-14-11` у подмодуля (`dirty=0`) → bump в родителе явным списком (`git add a b c`; в zsh переменная со словами не разбивается) → push.
- Методички править только через `bundle.jsub` / `bundle.transform` (`fixes/common/_tools/bundle.py`), поле `text` — `rebuild.py`; видимый текст проверять в Chromium.
- Docker: запускать и закрывать самой, чистить только созданное (по точным именам), без `pkill` по маске и `rm` по маске; на macOS нет `timeout`; не печатать трассы Laravel целиком; Python с кириллицей — только из файла с `# -*- coding: utf-8 -*-`; брокер RabbitMQ в Docker Desktop иногда падает с `eacces` на `.erlang.cookie` — перезапустить.
- Честно писать, что не проверено. Итоговые ТЗ не решать. Ключи и пароли в файлы не писать.
- Агентов запускать не больше 6 одновременно, каждый — в своём подмодуле и в ветке `auto/overnight-14-11`, общие записи (fixes/works/CLAUDE.md/родитель) делает руководитель.

## Что убрать в самом конце

Созданное ночью в Docker (проверять по `scratchpad/img_before.txt` — что было до): образы `rmqapp-app`, `oopverify-*`, `agent*`, `bash-check`, `cfl-tools`, `prom/prometheus:latest`, `redis:8-alpine`/`redis:8`, `centrifugo/centrifugo:v6`, `node:24-slim`, `postgres:18`, `rabbitmq:4-management`, `axllent/mailpit` — **только если их не было до** и ими не пользуются работающие агенты; контейнеры `cfl-*`, `agent*`, `kubernetes-dind` и тома/сети с этими префиксами. Остановить фоновый keepalive: `kill $(cat scratchpad/keepalive.pid)` (PID по файлу, не по маске). Сказать владельцу в итоге: что сделано, что нет, что решать (мердж ветки, статусы).
