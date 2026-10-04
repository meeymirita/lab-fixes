# GraphQL Lab (CineGraph) — итоги вычитки и проверки

**Вычитка:** ✅ пройдено 24.09; найдено 3 (тех 2, противоречий 1, текст 0); все внесены в методичку.  
**Проверка запуском и в браузере:** см. разделы «🧪» ниже и таблицу `fixes/common/_verification.md` (там же уровень проверки и что не проверялось).

## Находки чтения методички (23–26.09 и 04.10) — дайджест
Полные формулировки не хранятся: каждая находка исправлена в методичке. Здесь — суть, чтобы понимать, какие классы ошибок встречались.

- **[противоречие] Шаг 3.2 vs раздел 5 (часть 2) и шаг 1.4 (часть 3)** — раздел 5 для запроса `movies(limit: 10) { title director { name } cast { character person { name } } }` даёт «Movie.cast 10 … CastCredit.person ~28 … ────…
- **[тех] Шаг 2.3, «Под капотом»** — «Поменять глобально можно опцией nullable в buildSchemaOptions» → в `@nestjs/graphql` (проверено по пакету 14.0.2, `BuildSchemaOptions`: dateScalarMode, numberScalarMode, scalarsMap, orphane…
- **[тех] Шаг 2.4** — пример интроспекции `{ __type(name: "Movie") { name description fields { name type { kind name ofType { kind name ofType { name } } } } } }` даёт только 3 уровня вложенности (`type`→`ofType`→`ofType.ofType…

## 🧪 Сухой прогон 03.10.2026 (Nest CLI 11/latest, Prisma 7.10, PostgreSQL 18, Redis 8)
Установочные команды шага 1.1 выполнены дословно, затем с закреплёнными версиями; Prisma-часть (config, схема, миграция, генерация, seed) и компиляция кода сессий проверены. Целиком приложение автоматически не собралось: несколько блоков — патчи (`— добавляем в класс`, `переписан`), и модули `auth/users/reviews` в методичке разнесены по блокам с `@Module` внутри файлов резолверов.

- **[тех] Шаг 1.1: `npx @nestjs/cli@latest new api` теперь создаёт NestJS 12** (`@nestjs/core ^12.0.1`), а `npm i @nestjs/graphql @nestjs/apollo` ставит версию 14. Лаба написана под NestJS 11 + `@nestjs/graphql` 13. → `@nestjs/cli@11`, `@nestjs/graphql@13`, `@nestjs/apollo@13`; набор резолвится без конфликтов (graphql 16.14, @apollo/server 5.5). ✅
- **[тех] Шаг 1.1: `npm i -D prisma` ставит `8.0.0-rc.19`** (на npm у `prisma` latest — релиз-кандидат), а `@prisma/client` — 7.10. CLI 8 и клиент 7 несовместимы. → `prisma@7`, `@prisma/client@7`, `@prisma/adapter-pg@7`. ✅
- **[тех] Шаг 6.1 / 6.4: `app.module.ts` не компилируется на `graphql-ws` 6.2** — `onConnect: (ctx: { …; extra: Record<string, unknown> })` — `ctx.extra` теперь типизирован как `unknown`, TS2322 в `subscriptions['graphql-ws']`. → `extra: unknown` и `(ctx.extra as Record<string, unknown>).token = …`. ✅
- Подтверждено: `prisma migrate dev`, `prisma generate`, `prisma db seed` (через `tsx`) работают на PostgreSQL 18 с `prisma.config.ts`; `tsconfig.build.json` с `exclude: [..., "prisma", "prisma.config.ts"]` нужен (иначе `dist/src/main.js`).
- Для e2e с реальной БД (`test/app.e2e-spec.ts`) под Jest нужен `NODE_OPTIONS=--experimental-vm-modules` и `moduleNameMapper` для `.js`-импортов сгенерированного клиента — см. `nestjs.md`; в этой лабе e2e-шаг 6.5 не доведён до прогона.

---

## 🧪 Сухой прогон 04.10.2026 — сессии 1–6 целиком (NestJS 11.2, @nestjs/graphql 13.4, Apollo Server 5.5, Prisma 7.10, PostgreSQL 18, Redis 8)
Проект собран по блокам методички в Docker: схема и миграция, сид (10 фильмов, 33 пользователя), code-first схема, резолверы, DataLoader, аутентификация (JWT), мутации рецензий, ошибки и маскировка, права на поля, интерфейсы и юнионы, курсорная пагинация, подписки (graphql-ws) на памяти и на Redis, защита от тяжёлых запросов. Итог: `tsc` и `nest build` чисто, unit — **3/3**, e2e — **7/7**. Проверено вживую (curl/Python и клиент graphql-ws): каталог и `null` для несуществующего фильма, синтаксическая ошибка (400), подсказка «Did you mean», CSRF-защита GET, интроспекция, DataLoader (**4 SQL** вместо ≈43 на `CatalogPage`; один `GROUP BY` на рейтинги), `me` с токеном и без, `addReview` (повтор → `ALREADY_REVIEWED`, `rating: 11` → `BAD_USER_INPUT` с деталями, без токена → `UNAUTHENTICATED`, чужая рецензия → `FORBIDDEN`), частичный ответ по `email` (точный `path`), `createMovie` только для ADMIN, интерфейсы/юнионы (`__typename`, фрагменты, ошибка запроса `character` без фрагмента), курсорная пагинация (без дублей, мусорный курсор → `BAD_USER_INPUT`), всплытие `null` (запросы A–D совпали с ожиданием), маскировка в production («Internal server error», интроспекция и GraphiQL выключены), глубина (`Глубина запроса … превышает лимит 8`) и сложность (100 алиасов `search` → `QUERY_TOO_COMPLEX`), подписка: на двух инстансах с in-memory PubSub события **не** доходят (0), с Redis — приходят (в payload `createdAt` восстановлен в `Date`).

Находки (исправлено в методичке):
- **[тех] 3.3, `filter: MovieFilter | null`** — при `strictNullChecks` TypeScript пишет в `design:paramtypes` не класс, а `Object`: `ValidationPipe` молча пропускает проверку, правила `@Min(1888)`, `@MaxLength(100)` из `MovieFilter` не срабатывают (запрос с `yearFrom: 1500` проходит) → тип аргумента без `| null`, с пояснением.
- **[тех] 6.4, `ComplexityPlugin`** — `getComplexity()` сам приводит `variables` и **бросает** на невалидных; плагин делает любую ошибку в переменных (несуществующий enum, `"2015"` вместо `Int`, пропущенная обязательная переменная) ответом 500 `INTERNAL_SERVER_ERROR` вместо 400 `BAD_USER_INPUT` от Apollo (и ошибку в логе) → `try/catch` вокруг `getComplexity` с `return` (ошибку отдаст Apollo при выполнении).
- **[тех] 5.4, `MovieReviewsResolver`** — `constructor(private readonly reviews: ReviewsService)` и метод-резолвер `reviews(...)` — `TS2300: Duplicate identifier 'reviews'` → параметр переименован в `reviewsService`.
- **[тех] 1.1, `ioredis`** — `npm i ioredis` ставит 6.x, а `graphql-redis-subscriptions` собран на 5.x: `new RedisPubSub({ publisher: new Redis(url), … })` — `TS2322` (несовместимые типы клиентов), сборка падает → `ioredis@^5`.
- **[тех] 1.1/6.5, `@nestjs/jwt`** — версия 12 — только ESM: jest падает с «Must use import to load ES Module» (все пакеты `@nestjs/*` 12 — `"type": "module"`) → `@nestjs/jwt@^11`.
- **[тех] 6.5, запуск тестов** — клиент Prisma 7 импортирует `./enums.js` (нужен `moduleNameMapper` в конфиге jest) и внутри делает динамический `import()` (для e2e нужен `NODE_OPTIONS=--experimental-vm-modules`) → инструкции добавлены в шаг 6.5.
- **[тех] 1.4, `prisma/seed.ts`** — `as const satisfies ReadonlyArray<{ director; cast }>`: `TS2353` («excess property 'title'») в IDE и `tsc -p tsconfig.json`, а `const reviews = []` выводится как `never[]` (`TS2345`) → расширен тип `satisfies`, у массива указан тип (`tsx` и `nest build` эти ошибки не показывают: `prisma/` исключён из сборки).

Заодно по тем же причинам поправлена NestJS-лаба: `@nestjs/config@^4`, `@nestjs/jwt@^11`, `@nestjs/passport@^11`, `@nestjs/terminus@^11` (раньше был закреплён только `event-emitter@^3`).


## 🧪 Клиент, Redis и WebSocket — 04.10.2026
- **6.3 клиент `client/index.html`** (Chromium, `esm.sh/graphql-ws@6`, два инстанса `:3000` и `:3001` на `PUBSUB_DRIVER=redis`): вход «✓ Аня», `Inception` загружается, подписка на фильм 2 на `:3001` получила рецензию, добавленную через `:3000`, без ошибок консоли.
- **6.2 `ioredis` (autoResubscribe):** после `docker restart` Redis подписка пережила перезапуск — событие, опубликованное через 7 с, пришло.
- **6.4/6.6:** `depthLimit` режет по HTTP (`Глубина запроса 13 превышает лимит 8`), а тот же запрос по WebSocket (graphql-ws) **выполняется** — условие задания 6.6 («работают ли depthLimit и ComplexityPlugin для WebSocket») подтверждено. Сами задания «Production Hell» — для самостоятельного решения.
