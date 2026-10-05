# Учёт проверок: что и чем проверено

Нужен, чтобы в любой новой сессии было ясно: какие блоки кода методички **реально запускались** (в Docker или в браузере), а какие проверены только чтением. Обновлять сразу после каждой проверки (правило пользователя, см. «Журнал состояния» в `CLAUDE.md`). Находки и правки — в `fixes/<направление>/<лаба>.md`.

> **Парный файл:** `works/verification.html` (страница для просмотра в браузере) собирается из этого файла — `python3 tools/build-verification.py`. Изменил этот файл → пересобери html; правишь html вручную → внеси то же сюда. `tools/check-site.py` ловит расхождение.

> Лабы с ✅ и «—» в колонке «Что не проверено» на `works/progress.html` получают зелёную галочку «Полностью вычитана и проверена» (читает `tools/build-progress.py`).

> **Внешние ресурсы.** Пункты, для которых нужен аккаунт, публичный домен или ключи (Blackfire, Let's Encrypt, GitHub Actions и т. п.), считаются выполненными: в колонке «Что не проверено» стоит «—» и в скобках сноска, что сделать самому при реальном прохождении. Так же оформлены «Production Hell» — задания без подсказок: они для самостоятельного решения, проверено только, что их условия воспроизводятся. На странице прогресса сноска показывается под зелёной галочкой.

## Уровни

| Знак | Что значит |
|---|---|
| ✅ | Каждый блок кода шага собран и запущен (Docker и/или браузер), результат сверён с «Ожидаемым результатом» |
| 🟡 | Проверена часть шагов (указано какие) |
| 👁 | Страница отрисована в настоящем браузере (Playwright + Chromium), скриншоты в `screenshots-check/<дата>/` |
| 📖 | Только вычитка текстом, код не запускался |

Способ: **D** — Docker (контейнеры, сборка), **B** — браузер (Chromium), **T** — только текст.

## По лабам (на 05.10.2026: все лабы вычитаны и проверены; Caddy — частично, см. «Что не проверено»)

| Лаба | Уровень | Способ | Что проверено | Что не проверено | Где подробности |
|---|---|---|---|---|---|
| Algorithms PHP | ✅ | D | 26 файлов тестов (все по одному, числа сошлись), все `bench/*.php` | — (только текстовый шаг 13.3, шпаргалка) | `fixes/backend/algorithms-php.md` |
| Laravel Performance | ✅ | D | Сессии 1–9 целиком (Laravel 13.17, 1 млн заказов, k6, Debugbar, Telescope, SPX, OPcache/JIT, кеш, EXPLAIN, Octane, утечки состояния, итоговое сравнение 8.4, таблица 9.1, бюджет 9.2, prod-образ) | — (нужны внешние ресурсы: аккаунт Blackfire для 4.5, GitHub Actions для workflow 9.2 — проверите сами) | `fixes/backend/laravel-performance.md` |
| CSS | ✅ 👁 | D+B | Итоговая сборка всех блоков 1.1–6.3 (nginx в Docker + Chromium, 4 ширины, светлая/тёмная), см. таблицу ниже; 04.10 вечером: «сломанные» состояния отдельными замерами и кадрами (слои, min-inline-size, minmax/auto-fit, media против container, sticky с overflow-x: hidden), анимации (@property, popover, reduced-motion), view transitions | — | `fixes/frontend/css.md` |
| Tailwind | ✅ 👁 | D+B | 04.10: все 280 классов компилируются (Tailwind 4.3.3); итоговые три страницы Pulse собраны из блоков 1.1–5.4 и открыты в Chromium (лендинг, тарифы, меню-popover, дашборд, настройки, тёмная тема, мобильный вид), 1 правка (`app.js` на `settings.html`); 6.1 размеры (50 → 64 → 50 КБ), 6.2 Prettier, 6.3 образ nginx | — | `fixes/frontend/tailwind.md` |
| Inertia | ✅ 👁 | D+B | 04.10: сессии 1–6 целиком (собрано по блокам: модели, лента, SSR, вход, лайки/комментарии, студия, редактор, дашборд, модерация, ошибки), `vue-tsc`, `vite build` + SSR, `php artisan test` 8/8, Chromium по ролям (читатель/автор/редактор), prod-режим с кешами и падением SSR; supervisor и deploy.sh (перезапуск SSR, check-ssr) | — (задания 6.3 «Production Hell» без подсказок — решаете сами) | `fixes/backend/inertia.md` |
| Kubernetes | ✅ | D | вся лаба на живом кластере (03.10) | — | `fixes/devops/kubernetes.md` |
| Docker | ✅ | D | сессии 1–3, «Production Hell» (03.10) | — | `fixes/devops/docker.md` |
| Traefik | ✅ | D | сессии 1–2, canary, mkcert (03.10) | — (нужен публичный домен: Let's Encrypt — проверите сами) | `fixes/devops/traefik.md` |
| Caddy | 🟡 | D | 05.10: сессии 1–6 и 9–11 локально (Caddy 2.11.7, Node 24), сессии 7, 8, 12 и шаг 13.5 в Docker (Compose-стенд Edge, PHP-FPM, xcaddy, свой модуль на Go, восстановление из бэкапа) | systemd-служба (13.1), кластер с общим хранилищем (13.4), Laravel за Caddy (8.3), FrankenPHP; публичный домен/Let's Encrypt (4.4, 13.2) — проверите сами | `fixes/devops/caddy.md` |
| ООП (php-coffee) | ✅ | D | шаги 1.1–5.3, 25 тестов, HTTP + RabbitMQ (03.10) | — | `fixes/backend/php-coffee.md` |
| Чистый PHP | ✅ | D | сессии 1–8 (03.10) | — | `fixes/backend/php.md` |
| PostgreSQL | ✅ | D | стенд, сид (1 млн), EXPLAIN, lost update, на 17 и 18; сессии 8–12; 04.10: все SQL-блоки сессий 0–6 и 7.1 по шагам (psql), сверка выводов; 7.1/7.3/7.4 двумя настоящими сеансами, pgbench | — | `fixes/backend/postgresql.md` |
| Redis | ✅ | D | 03.10: приложение собрано по шагам 1.1–3.4, каждая служба проверена на живом Redis 8 (cache-aside, Lua-резерв, скользящее окно, Streams, два воркера, приоритеты); 3 исправления кода + Dockerfile | — (задания 3.5 без подсказок — решаете сами) | `fixes/backend/redis.md` |
| RabbitMQ | ✅ | D | пройдена пользователем полностью — «всё идеально» (05.10); compose на PG18 | — | `fixes/backend/rabbitmq.md` |
| Laravel | ✅ | D | 04.10: сессии 1–10 (весь бэкенд TaskFlow на Postgres 18/Redis 8/RabbitMQ 4/Mailpit/Reverb: связи, ресурсы, middleware, политики, приглашения, очередь, уведомления, кеш, лимиты, broadcasting auth), `php artisan test` 8/8, curl по ролям; 3.3 (SQL трёх пагинаций), 7.3 (retry/backoff), 9.4 (Echo в Chromium), select на Vue-доске 6.3 | — | `fixes/backend/laravel.md` |
| NestJS | ✅ | D | 04.10: сессии 1–9 (весь Helpdesk API: DTO, Prisma, JWT+refresh, роли, события, WebSocket, Swagger, helmet/throttler, health, Dockerfile), `nest build`, unit 7/7, e2e 6/6, curl и сокеты по ролям, prod-образ; 4.4 (откат), 8.1 (408), `docker compose --profile app` целиком | — (задания 9.5 «Production Hell» без подсказок — решаете сами) | `fixes/backend/nestjs.md` |
| GraphQL | ✅ | D | 04.10: сессии 1–6 (схема, резолверы, DataLoader 4 SQL, JWT, мутации, ошибки, права на поля, интерфейсы/юнионы, курсорная пагинация, подписки на памяти и Redis на двух инстансах, depth/complexity, prod-режим), `nest build`, unit 3/3, e2e 7/7; клиент client/index.html в Chromium, перезапуск Redis (ioredis), depth-limit по WebSocket | — (задания 6.6 «Production Hell» без подсказок — решаете сами) | `fixes/backend/graphql.md` |
| JS | ✅ | D | все скрипты и тесты (03.10) | — | `fixes/frontend/js.md` |
| TypeScript | ✅ 👁 | D+B | сравнение 5.9/6.0; 04.10: весь workspace по шагам 1.1–5.4 (typecheck, 23 теста, сборка cli/web, CLI, API на Express, страница Vue в Chromium, ошибки типов 5.3); 9 правок; **повторно собрана строго из исправленного текста (04.10, поздний вечер): typecheck, 23 теста, CLI, `import:csv`, страница Vue в Chromium — всё ок** | — | `fixes/frontend/typescript.md` |
| Vue | ✅ 👁 | D+B | 04.10: скаффолды, все блоки 1.1–5.3 (57 файлов + 15 патчей), `vite build`, Vitest 7/7, бэкенд Nest (login/tickets/PATCH), сценарий в Chromium (8 шагов); WebSocket между вкладками, индикатор при stop/start api, образ 5.4 (nginx) | — | `fixes/frontend/vue.md` |
| Nuxt | ✅ 👁 | D+B | 04.10: все блоки 1.1–6.3 (80 файлов + патчи), `nuxi typecheck`, `nuxi build` с пререндером, собранный сервер (API, поиск, sitemap, auth), 10/10 тестов, сценарий в Chromium; образ 6.4, hydration 4.4 (воспроизведено и вылечено), queryCollection 5.2 | — | `fixes/frontend/nuxt.md` |
| Angular | ✅ 👁 | D+B | 04.10: все блоки сессий 1–6 (52 файла + ручное слияние фрагментов), `ng build`, `ng test` 6/6, API + `ng serve` в Docker, сценарий в Chromium (вход, фильтры, расписание, форма и конфликт брони, мои брони, админка, выход), prod-образ nginx (SPA-fallback, кеш, `config.json`); SSE: одно общее соединение против пяти, живое обновление между пользователями | — | `fixes/frontend/angular.md` |

## Сайт (страницы проекта)

| Что | Способ | Результат (04.10) |
|---|---|---|
| `index.html`: карточки, карта маршрутов (ответвления), счётчик 21 | 👁 B | работает, ошибок консоли нет, битых картинок нет |
| `works/progress.html`: 21 строка, картинки, подсчёт | 👁 B | работает |
| Методичка с якорем `#sec-3`, `#step-2-1` (GraphQL) | 👁 B | переходит в нужный раздел; кнопка «Все работы» на месте |
| Оглавление в модалке лаб, `works/changelog.html` | T (Node/jsdom) | читается из `window.LAB` у всех 21 |

## CSS Lab — по шагам и блокам (пройден 04.10: итоговая сборка; найдено 2 правки — 2.2 и символы)

Способ: собираю сайт в временной папке по блокам методички, открываю в Chromium (Playwright), снимаю скриншоты (широкий и узкий экран, светлая и тёмная тема), сверяю с «Ожидаемым результатом». «Сломанные» блоки («сначала так», «ВРЕМЕННО») применяю отдельно, чтобы увидеть поломку, затем фикс.

Статус: ⬜ не начато · 🔄 идёт · ✅ блок собран, открыт в браузере, совпал с текстом · ⚠️ расхождение (см. находки)

| Шаг | Блоков кода | Статус | Примечание |
|---|---|---|---|
| 1.1 Стенд, разметка, `main.css` | 8 | ✅ | собран, отрисован в Chromium |
| 1.2 Reset, типографика | 2 | ✅ | собран, отрисован в Chromium |
| 1.3 Каскад, `@layer` | 6 | ✅ | собран, отрисован в Chromium |
| 1.4 Box model | 3 | ✅ | собран, отрисован в Chromium |
| 2.1 Токены | 4 | ✅ | собран, отрисован в Chromium |
| 2.2 Цвет oklch | 3 | ✅ | собран, отрисован в Chromium |
| 2.3 Тёмная тема | 3 | ✅ | собран, отрисован в Chromium |
| 2.4 Текст | 2 | ✅ | собран, отрисован в Chromium |
| 3.1 Шапка/подвал flex | 2 | ✅ | собран, отрисован в Chromium |
| 3.2 Медиа-объект | 3 | ✅ | собран, отрисован в Chromium |
| 3.3 Тарифы flex | 2 | ✅ | собран, отрисован в Chromium |
| 4.1 Каркас grid | 1 | ✅ | собран, отрисован в Chromium |
| 4.2 Сетка спикеров | 3 | ✅ | собран, отрисован в Chromium |
| 4.3 Программа | 3 | ✅ | собран, отрисован в Chromium |
| 4.4 Subgrid | 2 | ✅ | собран, отрисован в Chromium |
| 5.1 Mobile-first | 2 | ✅ | собран, отрисован в Chromium |
| 5.2 Container queries | 2 | ✅ | собран, отрисован в Chromium |
| 5.3 Форма `:has()` | 2 | ✅ | собран, отрисован в Chromium |
| 5.4 Поля формы | 1 | ✅ | собран, отрисован в Chromium |
| 6.1 Липкая шапка | 4 | ✅ | собран, отрисован в Chromium |
| 6.2 Движение | 2 | ✅ | собран, отрисован в Chromium |
| 6.3 View transitions | 1 | ✅ | собран, отрисован в Chromium |
| 6.4 Сборка Lightning CSS | 2 | ✅ | собран, отрисован в Chromium |

---

# Пошаговый учёт по остальным лабам (04.10)

✅ — блок(и) шага собраны и запущены (способ — в заголовке лабы); 🟡 — часть сценариев шага не гонялась; ⚠️ — найдено расхождение, исправлено в методичке; 📖 — только чтение; ⬜ — не делал. Подробности находок — `fixes/<направление>/<лаба>.md`.


## Nuxt — D+B: typecheck, build, API, 10/10 тестов, Chromium

| Шаг | Статус | Примечание |
|---|---|---|
| 1.1 Стенд: docker-compose, скаффолд Nuxt 4, typecheck | ✅ |  |
| 1.2 Файловый роутинг: все зоны, динамические параметры, catch-al | ✅ |  |
| 1.3 Layouts, компоненты и что генерирует Nuxt в .nuxt/ | ✅ |  |
| 1.4 SSR vs SPA руками: view-source, ssr: false, window на сервер | ✅ |  |
| 2.1 Первый server route, тип ответа из хендлера, Date: JSON прот | ✅ |  |
| 2.2 Payload: ломаем двойным запросом через $fetch и чиним | ✅ |  |
| 2.3 Реактивный query, lazy, pick, refresh: история инцидентов | ✅ |  |
| 2.4 Ошибки: 404 из хендлера, fatal-ошибка страницы, clearError | ✅ |  |
| 2.5 Hydration mismatch: ломаем временем и часовым поясом, чиним  | ✅ |  |
| 3.1 Drizzle + SQLite: схема, миграции, Nitro-плагин, статус из Б | ✅ |  |
| 3.2 API обращений: readValidatedBody + Zod, getValidatedQuery, s | ✅ |  |
| 3.3 shared/: одна схема на клиент и сервер, типы через z.infer | ✅ |  |
| 3.4 Форма обращения: клиентская валидация той же схемой, ошибки  | ✅ |  |
| 4.1 nuxt-auth-utils: пользователи в сиде, вход, requireUserSessi | ✅ |  |
| 4.2 Route middleware: auth и agent, сервер и клиент, redirect | ✅ |  |
| 4.3 «Мои обращения»: ломаем $fetch без cookie при SSR, чиним use | ✅ |  |
| 4.4 Утечка состояния между пользователями: ломаем модульным ref, | ⚠️ | hydration воспроизведён и вылечен: `<ClientOnly>` + компонент (исправлено в методичке) |
| 4.5 Кабинет агента: ssr: false, очередь и смена статуса через Pi | ✅ |  |
| 5.1 Nuxt Content v3: типизированная коллекция, страницы статей,  | ✅ |  |
| 5.2 Поиск по базе знаний: defineCachedEventHandler, queryCollect | ⚠️ | явный import queryCollection (исправлено) |
| 5.3 routeRules на prod-сборке: пререндер базы знаний, SWR для ст | ✅ |  |
| 5.4 Страница статуса: новый инцидент через API, устаревание SWR, | ✅ |  |
| 6.1 SEO: useSeoMeta, canonical, @nuxtjs/sitemap и @nuxtjs/robots | ✅ |  |
| 6.2 runtimeConfig: приватное и публичное, переменные окружения п | ✅ |  |
| 6.3 Тесты: unit для shared, компонент в Nuxt-окружении, e2e по A | ✅ |  |
| 6.4 nuxt build: что в .output, multi-stage Dockerfile, запуск pr | ⚠️ | образ собран и запущен; в slim падал `npm ci` (исправлено: node:24 на build) |
| 6.5 Финал: карта проекта и таблица «Vue Lab vs Nuxt Lab» | ✅ |  |

## Angular — D+B: ng build, ng test 6/6, Chromium, prod-образ

| Шаг | Статус | Примечание |
|---|---|---|
| 1.1 Стенд: docker-compose, готовый API, ng new, прокси /api | ✅ |  |
| 1.2 Первые компоненты: модели, RoomCard и RoomGrid, input/output | ✅ |  |
| 1.3 Сигналы: фильтры на signal/computed, model() в дочернем филь | ✅ |  |
| 1.4 OnPush и zoneless: ломаем мутацией и setInterval, чиним сигн | ✅ |  |
| 2.1 DI руками: сервис в root и в компоненте, InjectionToken, Nul | ✅ |  |
| 2.2 HttpClient: сервис RoomsApi, временный интерцептор токена, O | ✅ |  |
| 2.3 httpResource: параметры-сигналы, loading/error, отмена преды | ✅ |  |
| 2.4 RxJS там, где он нужен: поиск с debounce — ломаем гонкой mer | ✅ |  |
| 2.5 Интерцепторы: лог запросов, глобальная обработка ошибок, пор | ✅ |  |
| 3.1 Маршруты: оболочка приложения, lazy-страницы, параметры пути | ✅ |  |
| 3.2 Дочерние маршруты: вкладки комнаты, наследование параметров, | ✅ |  |
| 3.3 Resolver против загрузки в компоненте: данные до входа, 404  | ✅ |  |
| 3.4 URL как состояние: дата расписания в query-параметре, навига | ✅ |  |
| 4.1 Signal Forms: модель на linkedSignal из параметров маршрута, | ✅ |  |
| 4.2 Межполевые правила: конец позже начала, рабочие часы, не в п | ✅ |  |
| 4.3 Асинхронная проверка: validateHttp — свободен ли слот, pendi | ✅ |  |
| 4.4 Отправка: submit(), конфликт 409 от сервера, свой контрол вы | ⚠️ | TimeSelect показывал не то время (исправлено) |
| 4.5 Reactive Forms: форма комнаты в админке — typed FormGroup, с | ✅ |  |
| 5.1 Вход: AuthStore на сигналах, страница входа, интерцептор ток | ✅ |  |
| 5.2 Guards: вход обязателен, админка не грузится для чужой роли, | ✅ |  |
| 5.3 BookingsStore: состояние на сигналах, оптимистичная отмена с | ✅ |  |
| 5.4 Живые обновления: SSE как Observable, share, takeUntilDestro | ✅ |  |
| 6.1 Свой pipe и @defer: обзор недели как ленивый чанк | ✅ |  |
| 6.2 Тесты на Vitest: компонент через TestBed, стор с HttpTesting | ⚠️ | CanMatchFn в тесте (исправлено) |
| 6.3 Продакшн: ng build и бюджеты, runtime-конфиг через provideAp | ✅ |  |
| 6.4 Финал: карта приложения и таблица «Vue Lab · Nuxt Lab · Angu | ✅ |  |

## Inertia — D+B: vue-tsc, build+SSR, 8/8 тестов, Chromium по ролям

| Шаг | Статус | Примечание |
|---|---|---|
| 1.1 Чистый Laravel 13 и точка отсчёта на Blade | ✅ |  |
| 1.2 Серверная часть Inertia — resources/views/app.blade.php и mi | ✅ |  |
| 1.3 Клиентская часть: Vue, TypeScript, Vite-плагин — resources/j | ✅ |  |
| 1.4 Протокол руками: curl против Inertia | ✅ |  |
| 2.1 Модель данных: посты, теги, комментарии, лайки | ✅ |  |
| 2.2 Лента: ресурсы и первая настоящая страница — Feed/Index.vue | ✅ |  |
| 2.3 Layout, shared data и глобальные типы | ✅ |  |
| 2.4 Типизированные маршруты — Laravel Wayfinder | ✅ |  |
| 3.1 Страница поста — PostController@show и безопасный HTML | ✅ |  |
| 3.2 SEO: title, description, canonical, OpenGraph | ✅ |  |
| 3.3 SSR: включаем, ломаем, чиним | ✅ |  |
| 3.4 Комментарии при прокрутке — Inertia::optional и WhenVisible | ✅ |  |
| 4.1 Аутентификация на сессиях руками — Auth/Login.vue | ✅ |  |
| 4.2 Flash-уведомления и первый Pinia-store — stores/ui.ts | ✅ |  |
| 4.3 Комментарии и лайки: error bag и оптимистичное обновление | ✅ |  |
| 4.4 Роли и Policies, студия автора — Studio/Posts/Index.vue | ✅ |  |
| 4.5 Редактор поста: useForm, файлы, автосохранение — Studio/Post | ✅ |  |
| 5.1 Поиск и фильтры в URL — FeedController | ✅ |  |
| 5.2 Бесконечная лента и prefetch — Inertia::scroll | ✅ | prefetch проверен по сети в Chromium |
| 5.3 Дашборд автора: отложенные props и группы — Studio/Dashboard | ✅ |  |
| 5.4 Polling и запросы без визита — usePoll и useHttp | ✅ | опросы на 16 и 31 с, счётчик обновился |
| 5.5 Модерация, страницы ошибок и шифрование истории | ✅ |  |
| 6.1 Тесты: assertInertia, права, формы, типы | ✅ |  |
| 6.2 Сборка и запуск в продакшн-режиме: ассеты, SSR-сервер, верси | ✅ |  |
| 6.3 Production Hell — задания без подсказок | ✅ | задания без подсказок — решаете сами* |

## Laravel — D: Postgres/Redis/RabbitMQ/Mailpit/Reverb, 8/8 тестов, curl

| Шаг | Статус | Примечание |
|---|---|---|
| 1.1 Стенд: Docker, Laravel 13, Sanctum/Reverb/RabbitMQ-драйвер | ✅ |  |
| 1.2 Схема TaskFlow: модели, миграции, enum-типы Role/TaskStatus/ | ✅ |  |
| 2.1 Модели без связей, casts для enum, preventLazyLoading с перв | ✅ |  |
| 2.2 hasMany/belongsTo: метод vs свойство, лог SQL, кэш связи на  | ✅ |  |
| 2.3 N+1 живьём: LazyLoadingViolationException, with() по цепочке | ✅ |  |
| 2.4 belongsToMany вживую: имя pivot-таблицы, withPivot, wherePiv | ✅ |  |
| 2.5 Свой Pivot-класс Membership: casts на pivot, ->using(), ->as | ✅ |  |
| 2.6 assignees и labels: простые pivot, attach/sync/syncWithoutDe | ✅ |  |
| 2.7 Полиморфные связи: MorphTo/MorphMany на attachments и activi | ✅ |  |
| 2.8 hasManyThrough и разница with / whereHas / withCount | ✅ |  |
| 3.1 Коллекции в деле: groupBy, partition, countBy, keyBy, reduce | ✅ |  |
| 3.2 API Resources: whenLoaded, whenCounted, whenPivotLoaded, вло | ✅ |  |
| 3.3 paginate vs simplePaginate vs cursorPaginate: SQL и компроми | ⚠️ | cursorPaginate терял строки с одинаковым created_at (исправлено: latest()->latest('id')) |
| 4.1 CRUD задач: Form Requests, prepareForValidation, Rule::enum/ | ✅ |  |
| 4.2 Своё middleware EnsureWorkspaceRole: параметры, route(), att | ✅ |  |
| 4.3 Единообразные ошибки API: withExceptions, своё исключение с  | ✅ |  |
| 5.1 Container изнутри: build(), bind vs singleton, app()->call() | ✅ |  |
| 5.2 TaskNotifier: интерфейс + биндинг по конфигу, TaskAssigner,  | ✅ |  |
| 5.3 Contextual binding: when/needs/give на ActivityLogger | ✅ |  |
| 6.1 Sanctum SPA: login/logout через сессию и CSRF-cookie | ✅ |  |
| 6.2 Policy: view/create/update/delete + своё действие assign, be | ✅ |  |
| 6.3 Минимальный Vue: логин, список воркспейсов, доска задач | ✅ | собрано в Chromium: вход, воркспейсы, доска, смена статуса select (PATCH 200); прокси на localhost:8000 из контейнера (исправлено) |
| 6.4 Приглашения в воркспейс: токен-ссылка, authorize() в FormReq | ✅ |  |
| 7.1 TaskObserver: created/updating/deleted, isDirty, ловушка мас | ✅ |  |
| 7.2 Event + два независимых Listener: auto-discovery, ShouldQueu | ✅ |  |
| 7.3 Job: retry/backoff, ShouldBeUnique, failed_jobs — параллель  | ✅ | 3 попытки, паузы 5 и 15 с, failed_jobs |
| 7.4 Под капотом queue:work: параллель с вашим AbstractAmqpWorker | ✅ |  |
| 8.1 Mailable: markdown-письма, ShouldQueue, Mail::queue() | ✅ |  |
| 8.2 Notification: mail + database одним классом, вытесняет самод | ✅ |  |
| 8.3 Artisan-команда + Schedule: дайджест с withoutOverlapping и  | ✅ |  |
| 9.1 Cache::remember + инвалидация в Observer, ключи по сущности | ✅ |  |
| 9.2 Cache::lock: распределённый мьютекс против гонки при создани | ✅ |  |
| 9.3 RateLimiter: throttle по пользователю, свой ответ 429 | ✅ |  |
| 9.4 Broadcasting: PrivateChannel, Reverb, Laravel Echo на Vue-до | ⚠️ | в Chromium событие доходит; прокси Vite на localhost:8000 из контейнера (исправлено) |
| 10.1 Фабрики для всех моделей: состояния, has()/for(), деревья св | ✅ |  |
| 10.2 Feature-тесты: RefreshDatabase, actingAs, Policy и валидация | ✅ |  |
| 10.3 Fakes: Event/Notification/Mail::fake(), мок интерфейса через | ✅ |  |
| 10.4 Полный прогон тестов, карта проекта, «было / стало» | ✅ | 8/8 тестов, карта проекта — текст |

## NestJS — D: tsc, build, unit 7/7, e2e 6/6, curl и сокеты, prod-образ

| Шаг | Статус | Примечание |
|---|---|---|
| 1.1 Создаём проект | ✅ |  |
| 1.2 TypeScript-минимум для Nest — scratch/decorators.ts | ✅ |  |
| 1.3 Мини-DI-контейнер руками — scratch/mini-di.ts | ✅ |  |
| 2.1 Первый модуль — src/health/ и src/app.setup.ts | ✅ |  |
| 2.2 Конфигурация с валидацией — src/config/env.validation.ts | ✅ |  |
| 2.3 Провайдеры: токены, useValue, useFactory — src/common/clock. | ✅ |  |
| 3.1 PostgreSQL в Docker — docker-compose.yml | ✅ |  |
| 3.2 Схема данных и первая миграция — prisma/schema.prisma | ✅ |  |
| 3.3 PrismaService и глобальный модуль — src/prisma/ | ✅ |  |
| 3.4 Тестовые данные — prisma/seed.ts | ✅ |  |
| 4.1 DTO и глобальный ValidationPipe — src/tickets/dto/ | ✅ |  |
| 4.2 CRUD тикетов — src/tickets/tickets.service.ts и контроллер | ✅ |  |
| 4.3 Ошибки Prisma в HTTP — src/common/filters/prisma-exception.f | ✅ |  |
| 4.4 Транзакции и история изменений — src/tickets/ticket.diff.ts | ✅ | откат проверен: 500, тикет и история не изменились |
| 5.1 Регистрация и безопасный вывод — src/users/ | ✅ |  |
| 5.2 Логин и JwtStrategy — src/auth/jwt.strategy.ts | ✅ |  |
| 5.3 Глобальный guard, @Public() и @CurrentUser() | ✅ |  |
| 6.1 Refresh-токены: ротация и обнаружение кражи — src/auth/auth. | ✅ |  |
| 6.2 Роли и владение — RolesGuard и src/tickets/ticket.policy.ts | ✅ |  |
| 7.1 Комментарии и внутренние заметки — src/comments/ | ✅ |  |
| 7.2 Доменные события — src/tickets/ticket.events.ts | ✅ |  |
| 7.3 WebSocket-шлюз — src/realtime/tickets.gateway.ts | ✅ |  |
| 8.1 Middleware и interceptors: request id, access-лог, таймаут | ✅ | 408 через 10 с |
| 8.2 Документация API — Swagger и CLI-плагин | ✅ |  |
| 8.3 Безопасность: CORS, helmet, rate limiting | ✅ |  |
| 9.1 Unit-тесты: сервис с моком Prisma и guard | ✅ |  |
| 9.2 E2E: настоящая БД, настоящий HTTP — test/ | ✅ |  |
| 9.3 Свой динамический модуль — src/audit/ | ✅ |  |
| 9.4 Health-чеки, graceful shutdown и Docker-образ | ✅ |  |
| 9.5 Production Hell — задания без подсказок | ✅ | задания без подсказок — решаете сами* |

## GraphQL — D: build, unit 3/3, e2e 7/7, запросы и подписки на 2 инстансах

| Шаг | Статус | Примечание |
|---|---|---|
| 1.1 Создаём репозиторий и проект NestJS | ✅ |  |
| 1.2 Инфраструктура — docker-compose.yml | ✅ |  |
| 1.3 Модель данных — prisma/schema.prisma | ✅ |  |
| 1.4 Миграция и тестовые данные — prisma/seed.ts | ✅ |  |
| 1.5 Подключение к БД — src/prisma/prisma.service.ts | ✅ |  |
| 2.1 Подключаем GraphQL — src/app.module.ts | ✅ |  |
| 2.2 Первые типы схемы — src/movies/models.ts | ✅ |  |
| 2.3 Первый резолвер: Query.movies и Query.movie — src/movies/mov | ✅ |  |
| 2.4 Что на проводе: curl, интроспекция, schema.gql | ✅ |  |
| 3.1 Связи через резолверы полей (наивно) — src/movies/movies.res | ✅ |  |
| 3.2 Воспроизводим и считаем N+1 | ✅ |  |
| 3.3 Аргументы, input-типы и переменные — src/movies/inputs.ts | ✅ |  |
| 4.1 DataLoader на каждый запрос — src/loaders/loaders.factory.ts | ✅ |  |
| 4.2 Вычисляемые поля и чужой модуль — src/reviews/movie-reviews. | ✅ |  |
| 4.3 Первые мутации: регистрация, вход, пользователь в контексте  | ✅ |  |
| 4.4 Мутации рецензий: guard, валидация, владение — src/reviews/r | ✅ |  |
| 5.1 Ошибки: коды, маскировка, частичные ответы — src/graphql/for | ✅ |  |
| 5.2 Права на уровне полей и ролей — src/users/users.resolver.ts | ✅ |  |
| 5.3 Интерфейсы и юнионы: фильмография и поиск — src/movies/credi | ✅ |  |
| 5.4 Курсорная пагинация рецензий — src/reviews/movie-reviews.res | ✅ |  |
| 6.1 Подписки: живая лента рецензий — src/pubsub/pubsub.module.ts | ✅ |  |
| 6.2 Два инстанса — и подписки ломаются. Redis PubSub — src/pubsu | ✅ |  |
| 6.3 Клиент без библиотек — client/index.html | ✅ | client/index.html открыт в Chromium: вход, фильм, подписка между инстансами |
| 6.4 Защита от тяжёлых запросов — src/graphql/complexity.plugin.t | ✅ |  |
| 6.5 Тесты: батчинг и e2e по /graphql — test/app.e2e-spec.ts | ✅ |  |
| 6.6 Production Hell — задания без подсказок | ✅ | задания без подсказок — решаете сами*; условие про WebSocket подтверждено |

## Laravel Performance — D: k6, SPX, OPcache, кеш, Octane, prod-образ

| Шаг | Статус | Примечание |
|---|---|---|
| 1.1 Стенд: Laravel + PostgreSQL + Redis + Nginx | ✅ |  |
| 1.2 Схема данных и датасет: 1 млн заказов | ✅ |  |
| 1.3 Приложение с намеренными проблемами | ✅ |  |
| 1.4 Перцентили: почему среднее врёт | ✅ |  |
| 1.5 Первый замер руками: curl и ApacheBench | ✅ |  |
| 2.1 Smoke-тест: первый скрипт | ✅ |  |
| 2.2 Load-тест: стадии, thresholds и чтение отчёта | ✅ |  |
| 2.3 Сценарии: smoke / load / stress / spike | ✅ |  |
| 2.4 🔨 Сломать → починить: упавший порог и код возврата | ✅ |  |
| 2.5 Базовые цифры: таблица «ДО» | ✅ |  |
| 3.1 Debugbar: что делает один запрос | ✅ |  |
| 3.2 Telescope: запросы, кеш и события API | ✅ |  |
| 3.3 🔨 Сломать → починить: запретить lazy loading и починить N+1 | ✅ |  |
| 3.4 Почему Telescope нельзя оставлять на проде | ✅ |  |
| 4.1 SPX: установка и первый запуск | ✅ |  |
| 4.2 Wall-time и CPU: два разных «медленно» | ✅ |  |
| 4.3 Находим узкое место в отчёте: flamegraph | ✅ |  |
| 4.4 Правим узкое место и меряем «ДО / ПОСЛЕ» | ✅ |  |
| 4.5 Blackfire: тот же сценарий в облаке | ✅ | нужен аккаунт — проверяете сами* |
| 5.1 OPcache: как PHP компилирует код и что кешируется | ✅ |  |
| 5.2 Включаем OPcache и меряем эффект | ✅ |  |
| 5.3 Настройки для продакшна и поломка со «старым кодом» | ✅ |  |
| 5.4 JIT: ускорение чистых вычислений | ✅ |  |
| 5.5 Честный замер: помогает ли JIT вашему веб-приложению | ✅ |  |
| 6.1 optimize и route:cache | ✅ |  |
| 6.2 🔨 Сломать → починить: env() вне конфигов | ✅ |  |
| 6.3 Кеш ответа в Redis: теги и инвалидация | ✅ |  |
| 6.4 🔨 Сломать → починить: cache stampede и блокировки | ✅ |  |
| 6.5 Индексы и EXPLAIN: оптимизация по результатам профилирования | ✅ |  |
| 7.1 Модель: приложение живёт между запросами | ✅ |  |
| 7.2 Запускаем Octane на FrankenPHP в Docker | ✅ |  |
| 7.3 Первое сравнение: FPM против Octane на k6 | ✅ |  |
| 7.4 🔨 Сломать → починить: изменения кода и перезагрузка воркеров | ✅ |  |
| 8.1 🔨 Сломать → починить: два пользователя, чужие данные | ✅ |  |
| 8.2 Чиним: состояние на запрос через scoped-привязку | ✅ |  |
| 8.3 Утечка памяти и перезапуск воркеров | ✅ |  |
| 8.4 Итоговое сравнение «PHP-FPM против Octane» | ✅ | три прогона на каждом, медианы p95 |
| 9.1 Итоговая таблица «до → после» по эндпоинтам | ✅ | ×43…×187 |
| 9.2 Бюджет p95 и регрессионный тест k6 в CI | ✅ | пороги ✓, при p(95)<2 код 99; workflow не запускался |
| 9.3 Prod-образ: multi-stage + nginx | ✅ |  |
| 9.4 Чек-лист «тормозит — что делать по шагам» и что дальше | ✅ | чек-лист (текст) |

## TypeScript — D+B: typecheck, 23 теста, сборка, CLI, API, Chromium

| Шаг | Статус | Примечание |
|---|---|---|
| 1.1 Стенд: Docker, workspaces, tsconfig.base, tsx, vitest | ⚠️ | в tsconfig.base нужен `"types": ["node"]` (TS 6) — исправлено |
| 1.2 От JS к TS: аннотации, вывод, ошибки компилятора — playground/01 | ✅ |  |
| 1.3 Union, литералы, as const, type/interface, структурность — 02_un | ✅ |  |
| 1.4 Функции, колбэки, generics, unknown/any/never, catch — 03_functi | ✅ |  |
| 1.5 strict на практике, readonly, первый тест и тест на тип — 04_str | ✅ |  |
| 2.1 Branded IDs, Item, Location, Result<T, E> | ✅ |  |
| 2.2 Movement как размеченное объединение, exhaustive switch, Movemen | ✅ |  |
| 2.3 applyMovement: Result<Stock, StockError>, иммутабельный снимок,  | ✅ |  |
| 2.4 Ручные type guards и assertion functions; index.ts пакета | ✅ |  |
| 3.1 Repository<T extends Entity>: интерфейс, InMemory, JsonFile с gu | ✅ |  |
| 3.2 TypedEmitter<Events>: mapped types и generic-методы | ✅ |  |
| 3.3 Утилитные типы, groupBy с условием, satisfies для конфига | ✅ |  |
| 3.4 Сервис Warehouse: DI через интерфейсы, DistributiveOmit, события | ✅ |  |
| 4.1 parseArgs, CommandName из template literal, диспетчер под satisf | ⚠️ | locationId в импорте; `wh` из корня (data/) — исправлено |
| 4.2 Zod: схема = валидация + тип; toMovement как граница; import:csv | ⚠️ | сообщение Zod 4 — исправлено |
| 4.3 Декларации: .d.ts для vendor/table.js, declare module, declare g | ⚠️ | globals.d.ts: `declare global` — исправлено |
| 4.4 Сборка esbuild, --define, bin | ⚠️ | размер бандла ~750 КБ — исправлено |
| 5.1 ApiContract и generic-клиент с conditional types | ✅ |  |
| 5.2 Express, реализующий контракт: Response<ApiContract[R]['response | ⚠️ | API запускать из корня — исправлено |
| 5.3 Vue 3 + TS: typed props/emits, store на контракте, vue-tsc | ⚠️ | страница была пустой: `@warehouse/core/browser` — исправлено |
| 5.4 Финал: полный typecheck, карта проекта, «до / после» | ✅ |  |

## PostgreSQL — D: psql, pgbench, 1 млн заказов, два сеанса

| Шаг | Статус | Примечание |
|---|---|---|
| 0.1 Таблицы, ключи, связи и NULL — sql/00_sandbox.sql | ✅ |  |
| 0.2 INNER JOIN: склеиваем заказы с клиентами и напитками | ✅ |  |
| 0.3 LEFT, RIGHT, FULL JOIN и ловушка «условие в WHERE» | ✅ |  |
| 0.4 Self-join, CROSS JOIN, anti-join и semi-join | ✅ |  |
| 0.5 JOIN + GROUP BY: нули, count(*) против count(col) и «размножение | ✅ |  |
| 1.1 Postgres в Docker с инструментами наблюдения — docker-compose.ym | ✅ |  |
| 1.2 psql как рабочее место — .psqlrc | ✅ |  |
| 1.3 Схема кофейни — sql/01_schema.sql | ✅ | ошибки CHECK/FK в тексте — ожидаемы |
| 2.1 Миллион заказов за минуту — sql/02_seed.sql | ✅ |  |
| 2.2 SQL за пределами CRUD — sql/03_toolkit.sql | ✅ |  |
| 2.3 Как таблица лежит на диске: страницы, ctid, размеры и count(*) | ✅ |  |
| 3.1 Первый EXPLAIN: «последние заказы клиента» | ✅ |  |
| 3.2 EXPLAIN ANALYZE и BUFFERS: факт против оценки | ✅ |  |
| 3.3 Первый B-tree: индексы под внешние ключи — sql/10_indexes.sql | ✅ |  |
| 3.4 Составной индекс: убираем Sort… и планировщик слушается не всегд | ✅ |  |
| 4.1 Статистика: почему оценка врёт и как её починить | ✅ |  |
| 4.2 Частичные и функциональные индексы: экран бариста и вход по emai | ✅ | ошибка IMMUTABLE в тексте — ожидаема |
| 4.3 Покрывающий индекс и Index Only Scan: история покупок без похода | ✅ |  |
| 4.4 Когда индекс не используется и какие индексы удалить | ✅ |  |
| 5.1 Три алгоритма JOIN, loops и work_mem: отчёт «топ продуктов за ме | ✅ |  |
| 5.2 GIN: поиск по куску имени, по тегам, по jsonb и полнотекстовый | ✅ |  |
| 5.3 BRIN: индекс на 32 КБ для журнала событий | ✅ |  |
| 5.4 Расширенная статистика: связанные колонки | ✅ |  |
| 6.1 N+1 глазами базы — sql/20_n_plus_one.sql | ✅ |  |
| 6.2 Пагинация: OFFSET против keyset | ✅ | плейсхолдер `<created_at>` в тексте — ожидаемая ошибка |
| 6.3 Охота на медленные запросы: pg_stat_statements, лог, auto_explai | ✅ |  |
| 7.1 Транзакция руками: BEGIN, COMMIT, ROLLBACK, SAVEPOINT | ✅ | нарушение CHECK в тексте — ожидаемо; [A]/[B] двумя сеансами |
| 7.2 Потерянное обновление: 50 продаж, списано 6 — bench/*.sql | ✅ |  |
| 7.3 Read Committed вблизи: неповторяемое чтение и перепроверка WHERE | ✅ | двумя сеансами |
| 7.4 Repeatable Read: один снимок на транзакцию и ошибка 40001 | ✅ | двумя сеансами + pgbench |
| 8.1 Serializable и write skew: кофейня без бариста — sql/30_concurre | ✅ |  |
| 8.2 Ограничения как последняя линия обороны: CHECK, частичный UNIQUE | ✅ |  |
| 9.1 Строковые блокировки: FOR UPDATE, NOWAIT, lock_timeout и внешние | ✅ |  |
| 9.2 Очередь заказов для бариста на SKIP LOCKED | ✅ |  |
| 9.3 Дедлок: воспроизвести, прочитать, вылечить — sql/30_concurrency/ | ✅ |  |
| 9.4 Кто кого держит: pg_stat_activity, pg_blocking_pids, отмена запр | ✅ |  |
| 10.1 Табличные блокировки и миграции без простоя | ✅ |  |
| 10.2 Advisory locks: «только один экземпляр задачи» | ✅ |  |
| 11.1 MVCC руками: xmin, xmax, ctid и страница под микроскопом — sql/4 | ✅ |  |
| 11.2 Мёртвые строки и VACUUM: раздуваем таблицу вдвое | ✅ |  |
| 11.3 Долгая транзакция держит горизонт: VACUUM бессилен | ✅ |  |
| 11.4 Autovacuum, HOT, fillfactor и wraparound | ✅ |  |
| 12.1 Партиционирование журнала событий по месяцам — sql/50_partitioni | ✅ |  |
| 12.2 Жизнь с партициями: ограничения, retention, default-партиция | ✅ |  |
| 12.3 Production Hell — задания без подсказок | ✅ |  |

## Docker — D: сессии 1–3 и «Production Hell» в Docker Desktop 29.5.3

Образ, `.dockerignore`, три версии `entrypoint.sh`, том `pgdata`, сеть `lab-net`, ожидание БД, multi-stage, Compose с healthcheck, `.env`, лимиты (`mem=19MiB / 256MiB`) — запущены по шагам; PostgreSQL 18 хранит данные в `/var/lib/postgresql/18/docker`, том монтируется в `/var/lib/postgresql`, данные переживают пересоздание контейнера. Подробности и все находки — [fixes/devops/docker.md](https://github.com/meeymirita/lab-fixes/blob/main/devops/docker.md).

| Что проверено | Статус | Примечание |
|---|---|---|
| Сессии 1–3: образ, entrypoint ×3, том, сеть, multi-stage, Compose + healthcheck, `.env`, лимиты | ✅ | 03.10 |
| 2.4 SIGTERM и `exec` | ✅ | правка: у PID 1 нет обработчика сигналов — добавлен в `server.js`; «~10 с без exec» не воспроизводится, проверка через `docker kill -s TERM … && docker ps` |
| 1.4 `ps aux` в контейнере | ✅ | правка: в `node:*-slim` нет procps → `cat /proc/1/cmdline` |
| 3.4 «Production Hell» (сломанный compose → исправленный) | ✅ | прогнан 03.10 вечером; найдена шестая ошибка (без `.env` пустой `POSTGRES_PASSWORD`, `db` падает) — добавлена в разбор |

## Kubernetes — D: вся лаба на живом кластере (kind v0.33, Kubernetes v1.37)

Кластер создан по шагу 1.1, `api` и `frontend` собраны из блоков Traefik-лабы и загружены `kind load docker-image`. Все шаги 1.2–3.3: Pod, Deployment, Service + DNS, ConfigMap/Secret, PostgreSQL 18 + PVC (данные пережили удаление пода), Adminer, probes, requests/limits, Traefik как Ingress (IngressRoute, basic-auth Middleware), metrics-server + `kubectl top`, HPA (`cpu: 1%/50%`). Подробности — [fixes/devops/kubernetes.md](https://github.com/meeymirita/lab-fixes/blob/main/devops/kubernetes.md).

| Что проверено | Статус | Примечание |
|---|---|---|
| 1.1–2.x: кластер, Pod, Deployment, Service, ConfigMap/Secret, PVC, probes, лимиты | ✅ | 03.10 |
| 3.1 Traefik как Ingress | ✅ | 2 правки: не создавался ServiceAccount (`traefik-ingress-controller`), CRD/RBAC на `v3.1` вместо `v3.7`; после правок `api.localhost/health` → 200, `db.localhost` без пароля 401, с паролем 200 |
| 3.2–3.3 metrics-server, `kubectl top`, HPA | ✅ | |
| Версии | ✅ | kind v0.24 → v0.33, `kindest/node` v1.31 → v1.37 (на нём весь прогон проходит) |

## Traefik — D: сессии 1–2, canary и TLS через mkcert (Traefik v3.7)

Весь стек: whoami, dashboard с basic-auth, API ×3 с балансировкой и healthcheck (6 запросов → 2/2/2), frontend со StripPrefix, PostgreSQL 18 + Adminer, цепочка middlewares, weighted canary, TLS `*.localhost` через mkcert. Подробности — [fixes/devops/traefik.md](https://github.com/meeymirita/lab-fixes/blob/main/devops/traefik.md).

| Что проверено | Статус | Примечание |
|---|---|---|
| Сессии 1–2: роутеры, dashboard, балансировка, StripPrefix, Adminer, middlewares | ✅ | 03.10 |
| 2.5 цепочка middlewares | ✅ | правка: `secure-headers@file,api-ratelimit@file` (без суффикса Traefik ищет среди Docker-labels → 404) |
| 3.3 canary (weighted) | ✅ | правка: `priority: 100` (при 10 — 100 v1 / 0 v2; при 100 — 90/10, как в тексте) |
| 3.1 TLS через mkcert | ✅ | `https://whoami.localhost` → 200, issuer `mkcert development CA`; `mkcert -install` (пароль администратора) не запускался — `curl -k` |
| 3.2 Let's Encrypt | — | нужен публичный домен — проверите сами |

## Caddy — D: сессии 1–6 и 9–11 локально, 7, 8, 12 и 13.5 в Docker

05.10: сессии 1–6 и 9–11 запущены локально (Caddy v2.11.7, Node 24, macOS), сессии 7, 8, 12 и шаг 13.5 — в Docker Desktop (`caddy:2`, `node:24-slim`, `php:8.4-fpm`, `caddy:2-builder`). Найдено и исправлено 31 неточность. Подробности — [fixes/devops/caddy.md](https://github.com/meeymirita/lab-fixes/blob/main/devops/caddy.md).

| Что проверено | Статус | Примечание |
|---|---|---|
| Сессии 1–6 (запуск, статика, прокси, HTTPS, балансировка, безопасность) | ✅ | локально; тексты ошибок, заголовки и числа совпали, кроме отмеченных правок (macOS: порт занят, `timeout`, LibreSSL, `::1`) |
| Сессии 9–11 (логи, метрики, Caddyfile «как профи», Admin API, `@id`, `--resume`) | ✅ | локально |
| 7.1–7.5 Docker и Compose (стенд Edge, тома, `.env` с хешем) | ✅ | правки: `reload` при `admin off`, пропавший после `sed -i` файл, потеря `/data` |
| 8.1–8.2 PHP-FPM, «File not found» | ✅ | правка: `/srv/php` не монтируется (read-only) → `/opt/php`; в логе php нет «Primary script unknown» |
| 12.2–12.4 xcaddy, свой модуль на Go, две ошибки | ✅ | правки: версия Caddy в `go.mod` и у `xcaddy`, формат токена Cloudflare, текст «not an ordered HTTP handler» |
| 13.5 восстановление из бэкапа | ✅ | отпечаток корневого сертификата до и после совпал |
| 13.1 systemd-служба, 13.4 кластер с общим хранилищем | — | не запускались (unit-файл сверен с официальным) |
| 8.3 Laravel за Caddy, FrankenPHP | — | не запускались (Laravel не разворачивался) |
| 4.4 публичный домен, Let's Encrypt, 13.2 сеть | — | нужен домен и открытые порты — проверите сами |

## ООП (php-coffee) — D: шаги 1.1–5.3, 25 тестов, HTTP + RabbitMQ

Docker `php:8.4-cli`, Laravel 13.17, PostgreSQL 18, RabbitMQ 4 (на `php:8.5-cli` те же 25 тестов проходят). Подробности — [fixes/backend/php-coffee.md](https://github.com/meeymirita/lab-fixes/blob/main/backend/php-coffee.md).

| Что проверено | Статус | Примечание |
|---|---|---|
| 1.1 стенд | ✅ | 2 правки: `env_file … required: false`; `composer create-project` во временный каталог |
| 1.4–1.5 `lab0`, вывод в колонки | ✅ | правка: `mb_str_pad()` (кириллица в `printf("%-40s")`), вывод совпадает побуквенно |
| 2.x домен и HTTP API, оплата | ✅ | `curl /up`, миграции, заказ → оплата картой |
| 5.2 воркеры (barista, уведомления) | ✅ | правка: `use Illuminate\Support\Facades\{Log, Mail}` в уведомителях |
| 5.3 тесты | ✅ | 25 passed (два стандартных `ExampleTest` скелета); топология RabbitMQ из `definitions.json` |

## Чистый PHP — D: сессии 1–8 (PHP 8.4, PostgreSQL 18, PHPUnit)

Скрипты `src/01…19`, веб-эндпоинты через `php -S`, Composer PSR-4, роутер, контейнер (autowiring), PDO (инъекция и prepared), транзакции, CSRF, `.env`-парсер, финальный API, PHPUnit (4 теста); на PHP 8.5.11 код тоже работает без `Deprecated`. Подробности — [fixes/backend/php.md](https://github.com/meeymirita/lab-fixes/blob/main/backend/php.md).

| Что проверено | Статус | Примечание |
|---|---|---|
| Сессии 1–6: язык, Composer, PSR-4, роутер, контейнер | ✅ | правки: 4.2 `escape: ''` (Deprecated в 8.4), 6.1 четыре класса разнесены по файлам |
| Сессии 7–8: PDO, транзакции, CSRF, финальный API | ✅ | правки: 1.1 `libpq-dev` для `pdo_pgsql`, 7.1/7.2/8.1 `postgresql-client` и `PGPASSWORD`, 7.1 `echo` в `pdo-vulnerable.php`, 8.1 `DROP TABLE IF EXISTS` в `schema.sql` |
| 8.3 PHPUnit | ✅ | 4 теста проходят, Composer ставит PHPUnit ^13.4 |

## Redis — D: приложение по шагам 1.1–3.4 на живом Redis 8.10

PostgreSQL 18, Laravel 13.17, phpredis, `php:8.4-cli`. Каждая служба проверена на живом Redis: cache-aside с блокировкой, Lua-резерв склада, скользящее окно (`[true×5, false, false]`), Streams (XADD/XGROUP/XREADGROUP/XPENDING), два конкурирующих воркера (20 сообщений → `processed_messages = 20`, PEL пуст), XAUTOCLAIM, ZSET + `bzPopMin`. Подробности — [fixes/backend/redis.md](https://github.com/meeymirita/lab-fixes/blob/main/backend/redis.md).

| Что проверено | Статус | Примечание |
|---|---|---|
| 1.x кеш и блокировки | ✅ | правка: `REDIS_PREFIX=` пустой (Laravel добавляет `laravel-database-` ко всем ключам, воркер не видел сообщений) |
| 1.8, 3.1 Streams и воркеры | ✅ | правка: `xAck($stream, $group, [$id])` — phpredis принимает массив |
| 3.3 приоритетная очередь | ✅ | правка: `zAdd($key, 'nx', $score, $member)` |
| Dockerfile приложения | ✅ | в методичке не дан (artisan на хосте), в compose добавлен комментарий; для прогона собран свой |
| 3.5 задания без подсказок | — | решаете сами |

## RabbitMQ — D: пройдена пользователем + проверка на PostgreSQL 18

Лаба полностью пройдена пользователем (05.10.2026: «прошёл, там всё идеально») и заморожена; 03.10 при переводе на PostgreSQL 18 (том монтируется в `/var/lib/postgresql`) проверено на копии: `postgres` и `rabbitmq` становятся `healthy`, образ приложения собирается, `composer install` и `php artisan migrate` проходят на PostgreSQL 18.6 (все миграции лабы). Подробности — [fixes/backend/rabbitmq.md](https://github.com/meeymirita/lab-fixes/blob/main/backend/rabbitmq.md).

| Что проверено | Статус | Примечание |
|---|---|---|
| Прохождение лабы пользователем | ✅ | Outbox, воркеры, DLQ |
| Compose и миграции на PostgreSQL 18 | ✅ | старый том `pgdata` от PostgreSQL 16 образ 18 не откроет — нужен `docker compose down -v` |

## Algorithms PHP — D: 26 файлов тестов и все бенчи (PHP 8.4.26, PHPUnit 12.5)

Проект собран заново по блокам методички (Dockerfile, compose, `composer.json`, `phpunit.xml`), все 26 файлов тестов запущены по одному командой из методички: 68 тестов, 363 проверки — числа совпали с «Ожидаемым результатом» везде. Подробности — [fixes/backend/algorithms-php.md](https://github.com/meeymirita/lab-fixes/blob/main/backend/algorithms-php.md).

| Что проверено | Статус | Примечание |
|---|---|---|
| 26 файлов тестов | ✅ | 68 тестов, 363 проверки |
| Все `bench/*.php` | ✅ | порядки величин сходятся; абсолютные мс на этом стенде в 2–4 раза выше (в тексте «≈») |
| 5.3 `s5_list_vs_array.php` | ✅ | правка: `Segmentation fault` (рекурсивное освобождение 100 000 узлов) → ручной разбор цепочки |
| 4.2 `UndoHistory` и `OrderQueue` | ✅ | правка: два класса — два файла (PSR-4) |
| 6.4 вывод `s6_nobase` | ✅ | правка: `Fatal error: … on line 3` без префикса `PHP ` |
| 13.3 | — | только текстовый шаг (шпаргалка) |

## JS — D: 27 файлов, 11 скриптов, тесты (node:24)

Файлы собраны по заголовкам блоков; прогнаны все 11 скриптов `src/playground/*.js` и тесты — выводы десяти скриптов совпадают со строкой в строку (`06_closures.js` отличается только замерами времени, в методичке они `~15-40ms`). Подробности — [fixes/frontend/js.md](https://github.com/meeymirita/lab-fixes/blob/main/frontend/js.md).

| Что проверено | Статус | Примечание |
|---|---|---|
| 11 скриптов `src/playground/*.js` | ✅ | выводы совпадают |
| `npm test` (6 тестов) | ✅ | правка: на Node 24 `node --test src/__tests__` падает → `node --test src/__tests__/*.test.js` |
| Версии в тексте | ✅ | `node --version  # v24.x` |

## Vue — D+B: скаффолды, 57 файлов, Vitest 7/7, Chromium (Vue 3.5, Vite 7.3, NestJS 11)

04.10: проект собран по блокам методички (`npm create vue@latest`, `@nestjs/cli@11`, 57 файлов, 15 блоков-патчей слиты по тексту), `docker-compose.yml` поднят как написано. Подробности — [fixes/frontend/vue.md](https://github.com/meeymirita/lab-fixes/blob/main/frontend/vue.md).

| Что проверено | Статус | Примечание |
|---|---|---|
| `vite build`, Vitest 7/7 | ✅ | чанки по маршрутам |
| Бэкенд Nest (login 201, список 200, PATCH 200, без токена 401) | ✅ | |
| Сценарий в Chromium: список 12 карточек, фильтр в URL, вход, смена статуса, страница тикета, канбан, редирект, 404 | ✅ | ошибок консоли нет |
| 5.1 WebSocket между двумя вкладками | ✅ | тост в другой вкладке без дубля; индикатор ● зелёный → серый при `stop api` → зелёный |
| 5.4 `vite build`, nginx (SPA-fallback, прокси API, WebSocket) | ✅ | правка: числа и версия Vite заменены на фактические |
| 1.2 `npm i @nestjs/websockets …` | ✅ | правка: закреплены `^11` (без версий ставится NestJS 12 → ERESOLVE) |
| 5.3 `TicketCard.spec.js` | ✅ | правка: `RouterLinkStub` вместо `stubs: ['RouterLink']` |

## Tailwind — D+B: 280 классов, итоговые страницы Pulse в Chromium (Tailwind 4.3.3, Vite 7.3.6)

Проверено 03–04.10: сборка стенда, все 29 HTML-блоков, три итоговые страницы, шаги 6.1–6.3. Подробности — [fixes/frontend/tailwind.md](https://github.com/meeymirita/lab-fixes/blob/main/frontend/tailwind.md).

| Что проверено | Статус | Примечание |
|---|---|---|
| 1.1 стенд (Vite 7 и 8, три HTML-входа) | ✅ | добавлено `npm i -D vite@^7` («Vite 7 везде») |
| Классы из блоков | ✅ | из 280 уникальных 275 получили правило; 5 остальных ожидаемы (`bogus-class`, `…`, `card`, `legacy-banner`, `not-prose`) |
| Итоговые три страницы Pulse в Chromium (лендинг, тарифы, меню-popover, дашборд, настройки, тёмная тема, мобильный вид) | ✅ | правка: `app.js` падал на `settings.html` (`querySelector` без проверки) |
| 6.1 размеры | ✅ | 50 → 64 → 50 КБ (в тексте заменены фактические числа) |
| 6.2 Prettier | ✅ | `--check` проходит |
| 6.3 образ nginx | ✅ | `/app`, `/app.html`, `/`, `/settings` — 200, `/nope` — 404, ассеты `immutable`, HTML `no-cache` |
