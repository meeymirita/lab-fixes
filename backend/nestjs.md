ТУТ Я ЛИЧНО НАПИСАЛ ЧТО РАБОТА ПО NestJS уже никак не связано это полное изучение с нуля как отдельная технология

# NestJS Lab — находки


Методичка: `nestjs/NestJS_Lab_Plan.html` (самая большая, ~340 КБ). Битых якорей в оглавлении нет.
Версии согласованы между README, карточкой на сайте и методичкой: NestJS 11, Prisma 6, PostgreSQL 16, Node 22.

## 🔴 Главное: обещание совместимости с Vue-фронтом не выполняется

В методичке (раздел «О проекте»): «API спроектирован так, чтобы тот фронтенд [из Vue Lab] можно было направить на этот бэкенд».
В README NestJS: «тот фронтенд можно направить на этот бэкенд». В корневом README: NestJS «собирает с нуля тот самый бэкенд, который в Vue-лабе был дан готовым».

Сравнил код Vue-лабы (`web/src/api/*`, `stores/auth.js`, `server/src/data.ts`) с кодом NestJS-лабы:

| Что | Vue-фронт ждёт | NestJS отдаёт | Итог |
|---|---|---|---|
| Логин `POST /api/auth/login` | `{ token, user }` → `token.value = res.token; user.value = res.user` | `{ accessToken }` (user — отдельно через `GET /auth/me`), refresh — в cookie | ❌ фронт получит `undefined` |
| Роли | `'agent' \| 'admin'`, `isAdmin = role === 'admin'` | enum `CUSTOMER / AGENT / ADMIN` (верхний регистр) | ❌ |
| Статусы | `'open' \| 'in_progress' \| 'resolved' \| 'closed'` (+ валидатор в `StatusBadge`) | `OPEN / IN_PROGRESS / RESOLVED / CLOSED` | ❌ StatusBadge упадёт на валидаторе |
| Приоритеты | `'low' \| 'medium' \| 'high'` | `LOW / MEDIUM / HIGH / URGENT` | ❌ |
| Список тикетов | `?limit=50` → `{ items, total }` | `?page&perPage` → `{ items, total, page, perPage }` | ⚠️ `limit` при `forbidNonWhitelisted` даст 400 |
| WebSocket | `io({ path: '/socket.io' })`, без авторизации, событие `ticket.updated` (с точкой) | namespace `/ws`, токен в `handshake.auth.token`, события `ticket:updated` (с двоеточием), payload `{ ticket, changes }` | ❌ |

**Что сделать (на выбор):**
1. Честно переписать фразу: «домен тот же, что у Vue Lab, но контракт свой (роли, статусы, JWT с ротацией) — Vue-фронт без адаптера не подключится». И поправить корневой README.
2. Или добавить в конец NestJS-лабы шаг «Подключаем Vue-фронт»: маппинг enum → lowercase в ответе (interceptor/serializer), алиас `limit → perPage`, логин, возвращающий и `user`, и отдельное пространство Socket.IO с событиями через точку. Хорошее упражнение на interceptors.

## 🟡 Мелочи

- В тексте рядом стоят `ticket.updated` (внутреннее событие EventEmitter2) и `ticket:updated` (событие Socket.IO). Это сознательно, но новичок легко перепутает — стоит одной строкой явно сказать «точка — внутри процесса, двоеточие — наружу в сокет».
- Node 22 — на сентябрь 2026 уже maintenance LTS (активный LTS — Node 24). Работать будет, но в стек-таблице можно написать «Node 22+ (проверено на 22, 24 тоже подходит)».
- Prisma 6 зафиксирована сознательно, с объяснением про Prisma 7 — это хорошо. В GraphQL-лабе при этом Prisma 7 — в `_order.md`/README стоит одной фразой отметить, что это намеренно (чтобы не выглядело как рассинхрон).
- `docker-compose.yml` в репозитории лабы — заглушка `services:` без сервисов (`docker compose config` на ней падает). Нормально до начала прохождения, просто знай.


---

## ✍️ Варианты решений

Оставь в каждом вопросе **один** вариант (остальные удали или поставь `[x]` у нужного).
Потом я прочитаю этот файл и перепишу лабу ровно по выбранному. ⭐ — моя рекомендация.

### 1. Связь с Vue Lab (ты написал: «уже никак не связано»)
- [x] ⭐ A — убрать обещание «тот фронтенд можно направить на этот бэкенд» в 3 местах (методичка, README лабы, корневой README) и везде писать: «полное изучение NestJS с нуля как отдельной технологии, домен Helpdesk похож на Vue Lab только по смыслу»
- [ ] B — оставить как есть

### 2. События `ticket.updated` (внутри) и `ticket:updated` (в сокет)
- [x] ⭐ A — добавить одну поясняющую строку «точка — внутри процесса, двоеточие — наружу в сокет»
- [ ] B — оставить как есть

### 3. Версия Node
- [x] ⭐ A — в таблице стека писать «Node 22+ (24 LTS тоже подходит)», код не трогать
- [ ] B — перевести лабу целиком на Node 24 (таблица, образы, текст)
- [ ] C — оставить Node 22

### 4. Prisma 6 здесь и Prisma 7 в GraphQL
- [x] ⭐ A — оставить Prisma 6 (объяснение уже есть), в корневой README добавить фразу, что разные версии — намеренно
- [ ] B — перевести NestJS-лабу на Prisma 7 (большая переделка шагов раздела 3)

### 5. Пустой `docker-compose.yml` (заглушка `services:`) в репозитории лабы
- [x] ⭐ A — решить один раз для всех лаб в `site.md` (вопрос 4)
- [ ] B — отдельно для этой лабы: заполнить минимальным рабочим compose (PostgreSQL)

---

## 📖 Вычитка методички

### Часть 1 (разделы 1–3)
- **[противоречие] Оглавление / нумерация шагов раздела 9** — в сайдбаре и в заголовках методички шаги «Сессии 5» внутри раздела «9. Пошаговая сборка проекта (5 сессий)» пронумерованы `9.1, 9.2, 10.1, 10.2, 10.3` (подтверждено в HTML: `data-key="step-10-1"` со `<span class="num">Шаг 10.1</span>`, ближайший предшествующий `id="sec-9"`), а сразу следом идёт отдельный раздел `id="sec-10"` с заголовком «10. Полный чек-лист концепций» — совершенно другая тема. Номер шага «10.1–10.3» совпадает с номером соседнего, но не связанного с ним раздела 10, из-за чего в оглавлении читатель может решить, что шаг 10.1 относится к разделу «Полный чек-лист концепций». → Исправить: перенумеровать шаги Сессии 5 в `9.3–9.7` (или иначе развести последовательность шагов и номера верхнеуровневых разделов), либо явно пояснить в тексте, что нумерация шагов сквозная по разделу 9 и не совпадает с номерами разделов 10–13.
- — остальное в разделах 1–3 (разбор задачи, устройство NestJS/DI/модулей/scopes/lifecycle-хуков, таблица Nest↔Laravel, итоговая архитектура, стек, структура проекта, обоснование выбора Prisma) проверено построчно и сверено с кодовыми блоками (pre_blocks.txt), расхождений и технических ошибок не найдено. Глоссарные сноски¹⁻²⁹ идут по возрастанию без пропусков и дублей.

### Часть 2 (разделы 3–9, начало Сессии 1)
- — раздел 3 (архитектурная диаграмма, таблица модулей), раздел 4 (стек, дерево проекта, «почему Prisma»), раздел 5 (access/refresh JWT, ротация и reuse detection), раздел 6 (сценарий жизненного цикла тикета, таблица прав RBAC), раздел 7 (Pipes/Guards/Interceptors/Filters, таблица RxJS-операторов, APP_GUARD/APP_PIPE vs useGlobalGuards), раздел 8 (EventEmitter2 vs брокер, Socket.IO комнаты/неймспейсы, масштабирование), начало раздела 9 (шаг 1.1 `nest new`) — технических ошибок и противоречий не найдено; примеры команд и структура файлов соответствуют NestJS 11 / Prisma 6.

### Часть 3 (Сессия 1 шаги 1.2–2.3, начало Сессии 2 — шаг 3.1)
- — код песочницы (`scratch/decorators.ts`, `scratch/mini-di.ts`), настройка `tsconfig.build.json`/`exclude`, модуль `health` (`HealthService`/`HealthController`/`app.setup.ts`/`main.ts`), `ConfigModule` с `validateEnv` (class-validator/class-transformer), кастомные провайдеры (`CLOCK`, `APP_INFO`, `useValue`/`useFactory`), `docker-compose.yml` для Postgres 16 и `init.sql` для `helpdesk_test` — код синтаксически и логически корректен, соответствует официальному поведению NestJS/TypeScript (в т.ч. точный код ошибки TS1272 и причины несовместимости esbuild/tsx с `emitDecoratorMetadata`), расхождений с остальным текстом методички не найдено.

### Часть 4 (шаги 3.2–4.2)
- — схема `prisma/schema.prisma` (модели User/Ticket/Comment/TicketHistory/RefreshToken, именованные связи `@relation("TicketAuthor"/"TicketAssignee")`, индексы), `PrismaService`/`PrismaModule` (`@Global()`, `extends PrismaClient`, `onModuleInit/onModuleDestroy`), сид (`prisma/seed.ts`, идемпотентность через `upsert`/`count`, порядок id пользователей 1–5), DTO и глобальный `ValidationPipe` (`whitelist`/`forbidNonWhitelisted`/`transform`, поведение `@IsOptional()` с `null`, `PartialType` из `@nestjs/swagger`), CRUD тикетов (`$transaction([findMany, count])`, `ParseIntPipe`, коды ответов) проверены построчно и точечно прогнаны через `tsc` (с заглушками типов `@nestjs/*`/`@prisma/client`) — расхождений и технических ошибок не найдено; curl-примеры соответствуют состоянию кода на этом шаге.

### Часть 5 (шаги 4.3–5.2)
- — `PrismaExceptionFilter` (коды P2002/P2003/P2025, `@Catch(Prisma.PrismaClientKnownRequestError)`, поведение только для HTTP), интерактивная транзакция и история изменений в `update()` (`tx` vs `this.prisma`, `diffTicket`), регистрация и `publicUserSelect`, `JwtStrategy`/`AuthModule`/`JwtModule.registerAsync`, первая версия `AuthService`/`AuthController` (логин, `validateCredentials`, единообразное сообщение об ошибке) — код скомпилирован (tsc, заглушки типов) без ошибок, числа в curl-примерах (id пользователя, коды состояний) согласуются с сидами и остальной методичкой; расхождений не найдено.

### Часть 6 (шаги 5.3–6.2)
- **[тех] Шаг 6.2, пример проверки ролей/владения** — `curl -s -X PATCH -H "Authorization: Bearer $AG" -H "$J" -d '{"status":"RESOLVED"}' localhost:3000/api/tickets/1 | jq .message` с ожидаемым выводом `# OPEN → RESOLVED not allowed` → ошибка: пример молча предполагает, что тикет #1 всё ещё в статусе `OPEN`, но в шаге 4.4 этот же тикет #1 уже был переведён в статус `IN_PROGRESS` командой `curl -s -X PATCH ... -d '{"status":"IN_PROGRESS","priority":"URGENT"}' localhost:3000/api/tickets/1` — и это изменение сохраняется (не откатывается; откатывается только последующий экспериментальный `throw new Error('boom')`, который в тексте явно предлагается затем убрать). Между шагами 4.4 и 6.2 в методичке нет ни `prisma migrate reset`, ни пересидки (`migrate reset` вообще используется только для тестовой БД `helpdesk_test` в e2e, см. шаг 9.2/раздел про npm-скрипты). Если читать методичку последовательно и выполнять все curl-примеры, к шагу 6.2 тикет #1 будет в статусе `IN_PROGRESS`, а переход `IN_PROGRESS → RESOLVED` **разрешён** таблицей `TRANSITIONS` (`IN_PROGRESS: ['RESOLVED', 'OPEN']`) — PATCH агента вернёт 200 с обновлённым тикетом, а не сообщение об ошибке. → Исправить: либо использовать в этом примере другой (нетронутый) тикет — например `/tickets/1` заменить на тикет, который ранее не изменялся, либо явно предупредить в шаге 4.4/6.2, что состояние тикета #1 меняется по ходу методички, и скорректировать ожидаемый статус/переход под фактическое состояние (`IN_PROGRESS → OPEN` не разрешён по той же таблице и подошёл бы как рабочий контрпример) или явно указать в шаге 6.2 «сбросьте тестовые данные (`npx prisma migrate reset`) перед этой проверкой».
- — остальное в шагах 5.3–6.2 (`JwtAuthGuard`/`@Public()`/`@CurrentUser()`, порядок нескольких `APP_GUARD`, ротация refresh-токенов и обнаружение повторного использования в `AuthService.refresh()`/`findValidRow()`/`issueTokens()` — код прогнан через `tsc`, ошибок типов нет, race-condition/compare-and-set через `updateMany({ where: { revokedAt: null } })` описан корректно), `RolesGuard`, `TicketPolicy` (`TRANSITIONS`, `STAFF_ONLY_FIELDS`, `scopeFor`, 404 вместо 403) — технически корректны, соответствуют официальному поведению NestJS/Prisma/class-validator; сноски глоссария 30–34 расставлены по возрастанию без пропусков и совпадают с определениями в разделе 11.

### Часть 7 (шаги 7.1–8.1)
- — остальное в шагах 7.1–8.1 (комментарии/внутренние заметки, доменные события EventEmitter2, WebSocket-шлюз TicketsGateway, начало middleware/interceptors) проверено технически — код, импорты, состав модулей (TicketsModule exports, AuthModule exports JwtModule, @Global() PrismaModule), сигнатуры сервисов/политик (TicketPolicy.scopeFor/canSeeInternalComments/assertCanUpdate) и curl-примеры сверены с остальной методичкой — расхождений не найдено.

### Часть 8 (шаги 8.1–9.2)
- **[противоречие] Шаг 8.1, «Под капотом: … что не отменяет таймаут …»** — «Настоящая отмена требует `AbortController`, передаваемого вниз, и таймаутов на уровне БД (`statement_timeout`). Задание 6 в Production Hell.» → в таблице шага 10.3 тема «Таймаут, который ничего не отменил» — это задание **№5** (№6 в этой же таблице — «Перебор паролей по разным email») → исправить на «Задание 5 в Production Hell».
- **[противоречие] Шаг 8.3, «Под капотом: … IP за прокси»** — «…лимит по IP легко обойти пулом адресов — для логина надёжнее ключ «IP + email» (задание 7 в Production Hell).» → в таблице шага 10.3 тема ключа «IP + email» для rate limiting — это задание **№6** (№7 в этой же таблице — «Цикл модулей», про `forwardRef`, к rate limiting отношения не имеет) → исправить на «задание 6 в Production Hell».
- — остальное в шагах 8.1–9.2 (middleware/interceptors, Swagger + CLI-плагин, CORS/helmet/throttler, unit-тесты с моками Prisma, начало e2e-сетапа test/utils.ts, test/auth.e2e-spec.ts) проверено технически (импорты, DI, порядок APP_GUARD/APP_INTERCEPTOR, соответствие env-переменных ранее заданным, jest.resetAllMocks vs clearAllMocks, argon2/cookie-парсинг) — иных расхождений не найдено.

### Часть 9 (окончание шага 9.2 — `test/tickets.e2e-spec.ts`, шаги 10.1–10.3, начало раздела 10 «Чек-лист» и раздела 11 «Глоссарий»)
- — `test/tickets.e2e-spec.ts` (изоляция чужого тикета — 404 и `total: 0` в списке; смена статуса агентом с записью истории и запретом клиенту, транзакция `OPEN→IN_PROGRESS→OPEN→CLOSED→(CLOSED→OPEN, 422)`; видимость внутренних заметок клиенту/агенту), «Под капотом» шага 9.2 (две ловушки e2e: чтение `.env` поверх `.env.test` и «голое» `createNestApplication()` без `configureApp()`), `src/audit/*` (динамический модуль через `ConfigurableModuleBuilder().setClassMethodName('forRoot').build()`, `AuditService`/`AuditListener` с `@OnEvent('**', { async: true })` — сверено, что `wildcard: true` для `EventEmitterModule.forRoot()` действительно включён на шаге 7.2, иначе `'**'` не сработал бы), `HealthController` (`PrismaHealthIndicator`/`pingCheck` — состав экспортов и сигнатура проверены распаковкой пакета `@nestjs/terminus` — метод и параметры совпадают), `main.ts` (`enableShutdownHooks()`), `Dockerfile`/`.dockerignore`/`docker-compose.yml` (multi-stage build, `node_modules/.prisma`, профиль `app`, healthcheck) и таблица «Production Hell» (10 заданий) — технически корректны и внутренне непротиворечивы (сама таблица и подводящий к ней текст «Зачем» с заданиями №1 и №7 совпадают); нумерация задачи 10.3 в тексте шагов 8.1/8.3 («Задание 6»/«задание 7») уже отмечена как противоречие агентом C в «Части 8» — повторно не дублирую. Чек-лист (раздел 10): все ссылки `#step-N-M`/`#sec-N` в таблице ведут на реально существующие якоря в документе (проверено программно), несовпадений видимого номера с целью не найдено.
- — остальное в этой части (начало раздела 11 «Глоссарий», термины 1–5) проверено, расхождений не найдено.

### Часть 10 (раздел 11 «Глоссарий» термины 6–39, раздел 12 «Вопросы для самопроверки», раздел 13 «Что дальше»)
- — раздел 11: все 39 терминов пронумерованы по порядку, счётчики `id="term-N"`/`id="ref-N"` (сноски из текста методички) совпадают 1:1 без пропусков и дублей (проверено программно); термины 38 «Динамический модуль» и 39 «Liveness / readiness» соответствуют своим первым упоминаниям в шагах 10.1 и 10.2.
- — раздел 12: все вопросы для самопроверки соответствуют материалу, изложенному в методичке (в т.ч. про `EventEmitter2`, WebSocket-аутентификацию, CORS, `trust proxy`, unit- vs e2e-тесты, `forRoot`/`forFeature`, liveness/readiness, `CMD ["node", "dist/main.js"]`); явная ссылка «(шаг 2.1)» на вопрос про ошибку `Nest can't resolve dependencies` ведёт на корректный якорь.
- — раздел 13 «Что дальше»: перечисленные пакеты и разделы официальной документации (`@nestjs/graphql`, `@nestjs/bullmq`, `@nestjs/microservices`, `@nestjs/cqrs`, `@socket.io/redis-adapter`, `nestjs-pino`, `@nestjs/schedule`, CASL, Fastify-адаптер, Nest workspaces/Nx, Prisma 7) — актуальные, существующие инструменты; ссылка «задание 9 из Production Hell» для Redis-адаптера WebSocket соответствует пункту №9 таблицы шага 10.3 (без противоречий). Расхождений не найдено.

### ✍️ Решение по вычитке
- [x] ⭐ A — исправить всё из вычитки выше
- [ ] B — исправить только [тех] и [противоречие]
- [ ] C — выборочно (отметь пункты выше)

---

## 🔁 Повторная вычитка (части 2–5 и 7, после правок 24.09)

### Часть 2 (разделы 3–9, начало Сессии 1) — повторно
Дополнительно к первому проходу целенаправленно перепроверено на скрытые рассинхроны:
- Таблица стека и таблица прав RBAC раздела 6 (часть 2) сверены с итоговым кодом `TicketPolicy`/`TicketsController`/`CommentsService` (части 6–7): «Менять title/description — свой, пока OPEN» ↔ `assertCanUpdate` (не staff: запрет `STAFF_ONLY_FIELDS`, иначе только при `status===OPEN`); «status/priority/assignee — 403 клиенту, по графу переходов агенту/админу» ↔ `TRANSITIONS`; «удалить — только admin» ↔ `@Roles(Role.ADMIN)` на `remove()`; «внутренние заметки — не видит/не пишет клиент» ↔ `canSeeInternalComments`/`ForbiddenException` в `CommentsService.create` — совпадений с кодом не нарушено.
- Ссылки «задание N в шаге 9.5» (раздел про циклы модулей в конце части 2 и далее) сверены с актуальной нумерацией шагов в HTML (`id="step-9-1"…"step-9-5"`, Production Hell действительно шаг 9.5 — старое рассогласование «10.3 vs 9.5», найденное в первом проходе для частей 8/9, уже устранено правкой от 24.09) — соответствует.
- Сноски глоссария 26–29 (argon2²⁶, RBAC²⁷, Observable²⁸, «Доменное событие»²⁹), идущие в этой части, продолжают последовательность 1–25 из части 1 без пропуска и без обгона части 4 (30–31) и части 5 (32–34) — порядок сквозной по всему документу, разрывов не найдено.
— остальное (архитектурная диаграмма и таблица модулей/экспортов/зависимостей раздела 3, стек и дерево проекта раздела 4, JWT-теория раздела 5, Pipes/Guards/Interceptors/Filters раздела 7, EventEmitter2/Socket.IO раздела 8, начало раздела 9) повторно прочитано построчно — расхождений не найдено.

### Часть 3 (Сессия 1 шаги 1.2–2.3, начало Сессии 2 — шаг 3.1) — повторно
- Прогнан вручную вывод `scratch/mini-di.ts`: порядок `console.log` в `resolve()` — строка «создаю X(deps)» печатается **до** рекурсивного разрешения зависимостей (а не после), поэтому фактический порядок строк — `TicketsService(...)` → `TicketRepository(...)` → `AppLogger()` → далее логи `.list()`/`.findAll()` — воспроизведён вручную и совпадает с указанным в методичке выводом дословно, включая `[class TicketsService]` в `scratch/decorators.ts` (актуальное поведение `util.inspect`/`console.log` для ES-классов в Node ≥10) и путь `/tickets` (без слэша, из-за `.replace(/\/$/, '')`) / `/tickets/:id`.
- `tsconfig.build.json` `exclude` (`scratch`, `prisma`, `scripts`, `test`, `**/*spec.ts`) сверен с деревом проекта из части 2 — все перечисленные там папки (`scratch/`, `scripts/ws-client.mjs`, `prisma/seed.ts`) действительно должны быть исключены из сборки; расхождений нет.
— остальное (DI-теория TS1272/import type, `docker-compose.yml` для Postgres 16→17, `init.sql`, `ConfigModule`/`validateEnv`, кастомные провайдеры `CLOCK`/`APP_INFO`) перепроверено, расхождений не найдено.

### Часть 4 (шаги 3.2–4.2) — повторно
- Сверено сквозное соответствие `prisma/schema.prisma` (часть 4) ↔ `prisma/seed.ts` (часть 4) ↔ `DEMO_AUTHOR_ID = 4` в `TicketsService` (часть 4, шаг 4.2): порядок `upsert` в сиде — admin(1), agent(2), agent2(3), customer(4), customer2(5) — `customer@helpdesk.local` действительно получает id 4 на чистой БД, комментарий в коде «# customer@helpdesk.local из сидов» корректен.
- Curl-примеры шага 4.2 (`{"title":"Hi"}` → 400 по `title`/`description`; `{"...","authorId":1}` → 400 «authority should not exist») сверены с `ValidationPipe` из того же шага (whitelist/forbidNonWhitelisted/transform) и `CreateTicketDto` (`Length(5,120)`/`Length(10,5000)`, без поля `authorId`) — соответствуют; на этом шаге ещё нет `Authorization` — guard'ы появляются только в шаге 5.3, поэтому запросы без токена ожидаемо проходят.
— остальное (модели `User`/`Ticket`/`Comment`/`TicketHistory`/`RefreshToken`, именованные связи, `PrismaService`/`PrismaModule`, DTO, CRUD) перепроверено, расхождений не найдено.

### Часть 5 (шаги 4.3–5.2) — повторно
- Сверена связка `AuthService.issueTokens(user, familyId, db: Prisma.TransactionClient)` (шаг 6.1) и её вызов из `login()` с `this.prisma` (типом `PrismaService extends PrismaClient`, а не `Prisma.TransactionClient`) — структурно совместимо (excess-property check в TS не применяется к переменным, только к литералам), `tsc` подтверждает отсутствие ошибки типов; реальной несовместимости нет.
- Формат refresh-токена `${row.id}.${secret}` (id — UUID без точек, secret — base64url без точек) и разбор `raw.split('.')` в `findValidRow` — коллизий разделителя не возникает, `tsc`/логическая проверка подтверждают корректность.
- Curl-пример шага 4.3 `-d '{"assigneeId":777}' → P2003` сверен с состоянием кода на этом шаге (проверка `assertAssignable` появляется только в шаге 6.2, здесь её ещё нет — Prisma сама бросает FK-ошибку) — соответствует.
— остальное (`PrismaExceptionFilter`, интерактивная транзакция и история в `update()`, `publicUserSelect`, `JwtStrategy`/`AuthModule`/`JwtModule.registerAsync`, первая версия `AuthService`/`AuthController`) перепроверено, расхождений не найдено.

### Часть 7 (шаги 7.1–8.1) — повторно
- Сверена сигнатура `TicketsService.findOne(user: AuthUser, id: number)` (введена в шаге 6.2, часть 6) с её вызовом `await this.tickets.findOne(user, ticketId)` в `CommentsService.list`/`create` (шаг 7.1, часть 7) — порядок и типы аргументов совпадают.
- Сверены сигнатуры `TicketsService.create(user, dto)`/`update(user, id, dto)`/`remove(user, id)`, изменённые в шаге 7.2 для публикации событий, с финальными версиями этих методов из шага 6.2 — изменения аддитивные (добавлены `this.events.emit(...)` и переменные для payload события), конфликтов сигнатур нет.
- Проверено, что `CommentCreatedEvent`'s поле `ticket: Pick<Ticket, 'id' | 'authorId'>` заполняется из объекта, реально возвращаемого `TicketsService.findOne` (включает все скалярные поля тикета, в т.ч. `id`/`authorId`) — соответствует.
- Ack-сценарий `scripts/ws-client.mjs` (`agent 1` → ok, `customer 1` → ok, `customer2 1` → `Ticket #1 not found`) сверен с данными сида: тикет #1 принадлежит `customer@helpdesk.local` (id 4), `customer2` (id 5) не автор → `scopeFor` в `TicketsGateway.subscribe` корректно не находит тикет — вывод в примере точен.
— остальное (комментарии/внутренние заметки, доменные события EventEmitter2, `TicketsGateway`, `RealtimeListener`, middleware/interceptors начала шага 8.1) перепроверено, расхождений не найдено.

**Итог повторной вычитки:** в частях 2–5 и 7 новых ошибок нет (0 [тех] / 0 [противоречие] / 0 [текст]) — первый проход здесь был корректным.

---

## 🧪 Сухой прогон Prisma-части и переход на Prisma 7 — 03.10.2026 (Nest CLI 11, Prisma 7.10, PostgreSQL 18)

По решению «Prisma 7 везде» лаба переведена с Prisma 6 на 7. Новый поток проверен на реальном Nest 11: схема лабы (все 6 моделей) → `migrate dev` → `generate` → seed (идемпотентен: 5 пользователей / 3 тикета после двух запусков) → `nest build` (дист плоский, `dist/main.js`) → jest (unit и e2e с реальной БД).

Что изменилось в методичке:
- **Версии:** `npm i -g @nestjs/cli@11` (@latest теперь создаёт NestJS 12 с другим тулчейном), `prisma@7` (на npm latest — 8.0 RC), `@prisma/client@7`, `@prisma/adapter-pg@7`, `pg`, `dotenv`, `tsx`.
- **Генератор:** `prisma-client-js` в Prisma 7 не работает (ошибка валидации схемы). Новый `provider = "prisma-client"`, `output = "../src/generated/prisma"`, `moduleFormat = "cjs"`; в `datasource` больше нет `url`. Клиент импортируется **относительным путём** (`../generated/prisma/client`), а не из `@prisma/client` — все ~24 импорта в методичке заменены по глубине файла; `src/generated/` в `.gitignore`.
- **`prisma.config.ts`:** URL базы и `migrations.seed: 'tsx prisma/seed.ts'` живут здесь; секция `"prisma"` в `package.json` и `ts-node` для сида не нужны. `prisma.config.ts` добавлен в `exclude` `tsconfig.build.json`.
- **`npx prisma init` убран:** в 7-й версии он создаёт файлы для AI-агентов (`.agents`, `.windsurf`, `skills-lock.json`) и не создаёт `prisma.config.ts` — файлы создаются руками.
- **`migrate dev` больше не генерирует клиент** — отдельная команда `prisma generate`.
- **`PrismaService`** получает driver adapter: `super({ adapter: new PrismaPg({ connectionString: process.env.DATABASE_URL! }) })`; seed — тоже.
- **[тех] «Fail fast» перестаёт работать:** с адаптером `$connect()` ленивый и успешен даже при остановленной БД; приложение стартовало бы без базы. → в `onModuleInit` добавлен `await this.$queryRaw\`SELECT 1\``, сообщение в эксперименте 3.3 обновлено. ✅
- **[тех] Jest:** сгенерированный клиент импортирует `./enums.js` в ESM-стиле — jest падает с `Cannot find module './internal/class.js'`. Нужен `"moduleNameMapper": { "^(\\.{1,2}/.*)\\.js$": "$1" }` в `package.json` → `jest` и в `test/jest-e2e.json`. ✅
- **[тех] e2e с реальной БД:** Prisma 7 внутри делает динамический `import()`, jest падает `A dynamic import callback was invoked without --experimental-vm-modules`. → `NODE_OPTIONS=--experimental-vm-modules jest …` в скрипте `test:e2e:run`. ✅
- **Docker (9.4):** строка `COPY --from=build /app/node_modules/.prisma ./node_modules/.prisma` удалена: клиент теперь компилируется в `dist/generated`; `npx prisma generate` перед `npm run build` остался.
- **Пул соединений (3.3):** вместо `connection_limit` в URL — `max` в `new PrismaPg({ connectionString, max })`; арифметика «170 соединений» пересчитана под `pg.Pool` (10 по умолчанию).
- **TypeScript 6 не подходит стартеру Nest 11:** `tsc` падает на `baseUrl` (`TS5101: deprecated … stop functioning in TypeScript 7.0`). NestJS- и GraphQL-лабы остаются на TypeScript из стартера (5.x); TS 6 — только в TypeScript-лабе.
- **Не прогонялось целиком:** сессии 4–9 (DTO, JWT, роли, WebSocket, Swagger, e2e-пакет) — только проверка Prisma-типов (`Prisma.UserSelect`, `PrismaClientKnownRequestError`, `Prisma.TicketWhereInput`) и сборка.

---

## 🧪 Сухой прогон 04.10.2026 — сессии 1–9 целиком (NestJS 11.2, Prisma 7.10, PostgreSQL 18, Node 24)

Проект собран по блокам методички в Docker (node:24 + postgres:18-alpine): модули health/config/prisma/tickets/users/auth/comments/realtime/audit, DTO и ValidationPipe, фильтр Prisma, транзакции и история, JWT с ротацией refresh, роли и политика, события, WebSocket, middleware/интерсепторы, Swagger, helmet/CORS/throttler, health-чеки, Dockerfile. Итог: `tsc` и `nest build` чисто, unit — **7/7**, e2e на настоящей БД — **6/6**, prod-образ собирается и отвечает (`/api/health/ready` 200, `/live` 200). По curl и сокетам: логин, права по ролям (чужой тикет 404, клиенту нельзя менять статус 403, исполнитель-клиент 422, удаление только админу), кража refresh (повтор → 401 и отзыв семьи), внутренние заметки скрыты от клиента, заголовки `x-request-id`/`X-Handler-Time`/helmet, лимит логина (5×401 → 429), Swagger (схемы DTO из CLI-плагина), Socket.IO (ack подписки, `comment:created` агенту и автору, 404-исключение для чужого тикета).

Находки (исправлено в методичке):
- **[тех] 4.1, `npm i @nestjs/swagger`** — на npm latest 12.x, ему нужен Nest 12: `ERESOLVE` при установке в проект на Nest 11 → `@nestjs/swagger@^11`. То же в 7.3: `@nestjs/websockets@^11 @nestjs/platform-socket.io@^11`.
- **[тех] 7.2, `@nestjs/event-emitter`** — версия 12 — только ESM; unit-тест `tickets.service.spec.ts` падает: «Must use import to load ES Module» → `@nestjs/event-emitter@^3`.
- **[тех] 6.2 / 7.1 / 9.1, относительные пути импорта клиента Prisma** — в `roles.decorator.ts`, `roles.guard.ts`, `roles.guard.spec.ts` стоит `'../generated/prisma/client'` (файлы лежат на два уровня глубже `src/`), в `comments.service.ts` — `'../../generated/…'` (на уровень мельче) → `Cannot find module`; пути исправлены.
- **[тех] 9.2, `prisma migrate reset --force --skip-seed`** — в Prisma 7 флага `--skip-seed` нет (`unknown or unexpected option`), сид при reset больше не запускается → команда без флага; убрано дублирование `NODE_OPTIONS=…` в скрипте; в 3.4 исправлено утверждение про автозапуск сида.
- **[тех] 9.2, `dotenv -e .env.test`** — не перезаписывает переменную, уже заданную в окружении: при экспортированной `DATABASE_URL` `migrate reset` стирает рабочую базу, а не тестовую (у меня так и случилось в прогоне) → `dotenv -o -e .env.test` (+ пояснение).
- **[тех] 9.4, `Dockerfile`** — `npx prisma generate` в стадии сборки падает (`PrismaConfigEnvError: Cannot resolve environment variable: DATABASE_URL` — `prisma.config.ts` требует переменную даже для generate, а `.env` в образ не попадает) → `DATABASE_URL="postgresql://build:build@localhost:5432/build"` на этой строке.

Не проверялось: сценарии 4.4 (откат транзакции через искусственный `throw`) и 8.1 (таймаут 408 на медленном маршруте), задания 9.5 («Production Hell»), `docker compose --profile app` целиком (образ собран и запущен вручную, healthcheck проверен curl), graceful shutdown под нагрузкой.
