# Учёт проверок: что и чем проверено

Нужен, чтобы в любой новой сессии было ясно: какие блоки кода методички **реально запускались** (в Docker или в браузере), а какие проверены только чтением. Обновлять сразу после каждой проверки (правило пользователя, см. «Журнал состояния» в `CLAUDE.md`). Находки и правки — в `fixes/<направление>/<лаба>.md`.

> **Парный файл:** `works/verification.html` (страница для просмотра в браузере) собирается из этого файла — `python3 tools/build-verification.py`. Изменил этот файл → пересобери html; правишь html вручную → внеси то же сюда. `tools/check-site.py` ловит расхождение.

> Лабы с ✅ и «—» в колонке «Что не проверено» на `works/progress.html` получают зелёную галочку «Полностью вычитана и проверена» (читает `tools/build-progress.py`).

## Уровни

| Знак | Что значит |
|---|---|
| ✅ | Каждый блок кода шага собран и запущен (Docker и/или браузер), результат сверён с «Ожидаемым результатом» |
| 🟡 | Проверена часть шагов (указано какие) |
| 👁 | Страница отрисована в настоящем браузере (Playwright + Chromium), скриншоты в `screenshots-check/<дата>/` |
| 📖 | Только вычитка текстом, код не запускался |

Способ: **D** — Docker (контейнеры, сборка), **B** — браузер (Chromium), **T** — только текст.

## По лабам (на 04.10.2026)

| Лаба | Уровень | Способ | Что проверено | Что не проверено | Где подробности |
|---|---|---|---|---|---|
| Algorithms PHP | ✅ | D | 26 файлов тестов (все по одному, числа сошлись), все `bench/*.php` | — (только текстовый шаг 13.3, шпаргалка) | `fixes/backend/algorithms-php.md` |
| Laravel Performance | ✅ | D | Сессии 1–9 целиком (Laravel 13.17, 1 млн заказов, k6, Debugbar, Telescope, SPX, OPcache/JIT, кеш, EXPLAIN, Octane, утечки состояния, итоговое сравнение 8.4, таблица 9.1, бюджет 9.2, prod-образ) | Blackfire 4.5 (нужен аккаунт), workflow GitHub Actions 9.2 | `fixes/backend/laravel-performance.md` |
| CSS | ✅ 👁 | D+B | Итоговая сборка всех блоков 1.1–6.3 (nginx в Docker + Chromium, 4 ширины, светлая/тёмная), см. таблицу ниже | промежуточные «сломанные» состояния отдельными кадрами, анимации/sticky при прокрутке | `fixes/frontend/css.md` |
| Tailwind | ✅ 👁 | D+B | 04.10: все 280 классов компилируются (Tailwind 4.3.3); итоговые три страницы Pulse собраны из блоков 1.1–5.4 и открыты в Chromium (лендинг, тарифы, меню-popover, дашборд, настройки, тёмная тема, мобильный вид), 1 правка (`app.js` на `settings.html`) | 6.1 числа «размер CSS», 6.2 Prettier, образ 6.3 | `fixes/frontend/tailwind.md` |
| Inertia | ✅ 👁 | D+B | 04.10: сессии 1–6 целиком (собрано по блокам: модели, лента, SSR, вход, лайки/комментарии, студия, редактор, дашборд, модерация, ошибки), `vue-tsc`, `vite build` + SSR, `php artisan test` 8/8, Chromium по ролям (читатель/автор/редактор), prod-режим с кешами и падением SSR | задания 6.3 (открытые), supervisor/deploy.sh; polling 5.4 и prefetch 5.2 проверены 04.10 (см. таблицу ниже); хвосты вычитки закрыты (остался вопрос про «2.7») | `fixes/backend/inertia.md` |
| Kubernetes | ✅ | D | вся лаба на живом кластере (03.10) | — | `fixes/devops/kubernetes.md` |
| Docker | ✅ | D | сессии 1–3, «Production Hell» (03.10) | — | `fixes/devops/docker.md` |
| Traefik | 🟡 | D | сессии 1–2, canary, mkcert (03.10) | Let's Encrypt (нужен публичный домен) | `fixes/devops/traefik.md` |
| ООП (php-coffee) | ✅ | D | шаги 1.1–5.3, 25 тестов, HTTP + RabbitMQ (03.10) | — | `fixes/backend/php-coffee.md` |
| Чистый PHP | ✅ | D | сессии 1–8 (03.10) | — | `fixes/backend/php.md` |
| PostgreSQL | 🟡 | D | стенд, сид (1 млн), EXPLAIN, lost update, на 17 и 18; сессии 8–12 | — | `fixes/backend/postgresql.md` |
| Redis | ✅ | D | 03.10: приложение собрано по шагам 1.1–3.4, каждая служба проверена на живом Redis 8 (cache-aside, Lua-резерв, скользящее окно, Streams, два воркера, приоритеты); 3 исправления кода + Dockerfile | задания 3.5 (без подсказок) | `fixes/backend/redis.md` |
| RabbitMQ | ✅ | D | пройдена пользователем + compose на PG18 | — | `fixes/backend/rabbitmq.md` |
| Laravel | ✅ | D | 04.10: сессии 1–10 (весь бэкенд TaskFlow на Postgres 18/Redis 8/RabbitMQ 4/Mailpit/Reverb: связи, ресурсы, middleware, политики, приглашения, очередь, уведомления, кеш, лимиты, broadcasting auth), `php artisan test` 8/8, curl по ролям | смена статуса в select на Vue-доске (6.3) глазами | `fixes/backend/laravel.md` |
| NestJS | ✅ | D | 04.10: сессии 1–9 (весь Helpdesk API: DTO, Prisma, JWT+refresh, роли, события, WebSocket, Swagger, helmet/throttler, health, Dockerfile), `nest build`, unit 7/7, e2e 6/6, curl и сокеты по ролям, prod-образ | задания 9.5, `docker compose --profile app` целиком | `fixes/backend/nestjs.md` |
| GraphQL | ✅ | D | 04.10: сессии 1–6 (схема, резолверы, DataLoader 4 SQL, JWT, мутации, ошибки, права на поля, интерфейсы/юнионы, курсорная пагинация, подписки на памяти и Redis на двух инстансах, depth/complexity, prod-режим), `nest build`, unit 3/3, e2e 7/7 | клиент `client/index.html`, задания 6.6, атаки на подписки, рестарт Redis | `fixes/backend/graphql.md` |
| JS | ✅ | D | все скрипты и тесты (03.10) | — | `fixes/frontend/js.md` |
| TypeScript | 🟡 | D | сравнение 5.9/6.0 | `vitest`/`zod`/`express` на новых мажорах | `fixes/frontend/typescript.md` |
| Vue | ✅ 👁 | D+B | 04.10: скаффолды, все блоки 1.1–5.3 (57 файлов + 15 патчей), `vite build`, Vitest 7/7, бэкенд Nest (login/tickets/PATCH), сценарий в Chromium (8 шагов) | WebSocket между вкладками, перетаскивание в канбане, 5.4 образ | `fixes/frontend/vue.md` |
| Nuxt | ✅ 👁 | D+B | 04.10: все блоки 1.1–6.3 (80 файлов + патчи), `nuxi typecheck`, `nuxi build` с пререндером, собранный сервер (API, поиск, sitemap, auth), 10/10 тестов, сценарий в Chromium | образ 6.4 (Dockerfile) не собирался, Hydration-предупреждение 4.4 — открыто | `fixes/frontend/nuxt.md` |
| Angular | ✅ 👁 | D+B | 04.10: все блоки сессий 1–6 (52 файла + ручное слияние фрагментов), `ng build`, `ng test` 6/6, API + `ng serve` в Docker, сценарий в Chromium (вход, фильтры, расписание, форма и конфликт брони, мои брони, админка, выход), prod-образ nginx (SPA-fallback, кеш, `config.json`) | живое обновление SSE между двумя вкладками, перетаскивание | `fixes/frontend/angular.md` |

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
| 4.4 Утечка состояния между пользователями: ломаем модульным ref, | ⚠️ | hydration-предупреждение при первом заходе |
| 4.5 Кабинет агента: ssr: false, очередь и смена статуса через Pi | ✅ |  |
| 5.1 Nuxt Content v3: типизированная коллекция, страницы статей,  | ✅ |  |
| 5.2 Поиск по базе знаний: defineCachedEventHandler, queryCollect | ⚠️ | типы `queryCollection` на сервере |
| 5.3 routeRules на prod-сборке: пререндер базы знаний, SWR для ст | ✅ |  |
| 5.4 Страница статуса: новый инцидент через API, устаревание SWR, | ✅ |  |
| 6.1 SEO: useSeoMeta, canonical, @nuxtjs/sitemap и @nuxtjs/robots | ✅ |  |
| 6.2 runtimeConfig: приватное и публичное, переменные окружения п | ✅ |  |
| 6.3 Тесты: unit для shared, компонент в Nuxt-окружении, e2e по A | ✅ |  |
| 6.4 nuxt build: что в .output, multi-stage Dockerfile, запуск pr | 📖 | только чтение (образ не собирался) |
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
| 6.3 Production Hell — задания без подсказок | 📖 | задания без подсказок не решались |

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
| 6.3 Минимальный Vue: логин, список воркспейсов, доска задач | ⚠️ | собрано и запущено в Chromium (логин, воркспейсы, доска); прокси на localhost:8000 из контейнера (исправлено) |
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
| 10.4 Полный прогон тестов, карта проекта, «было / стало» | 📖 | карта проекта |

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
| 9.5 Production Hell — задания без подсказок | 📖 | задания без подсказок |

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
| 6.3 Клиент без библиотек — client/index.html | 📖 | client/index.html не открывал (грузит esm.sh) |
| 6.4 Защита от тяжёлых запросов — src/graphql/complexity.plugin.t | ✅ |  |
| 6.5 Тесты: батчинг и e2e по /graphql — test/app.e2e-spec.ts | ✅ |  |
| 6.6 Production Hell — задания без подсказок | 📖 | задания без подсказок |

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
| 4.5 Blackfire: тот же сценарий в облаке | 📖 | Blackfire — нужен аккаунт |
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
| 9.4 Чек-лист «тормозит — что делать по шагам» и что дальше | 📖 | чек-лист |
