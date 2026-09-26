# GraphQL Lab (CineGraph) — находки

Методичка: `graphql/GraphQL_Lab_Plan.html`. Битых якорей в оглавлении нет.
README, карточка и методичка согласованы: NestJS + Apollo Server (code-first), Prisma 7 + `@prisma/adapter-pg`,
PostgreSQL 17, Redis 7, DataLoader, bcryptjs.

## 🟢 Актуальность — лучшая среди лаб
- Prisma 7 описана правильно: `prisma.config.ts`, генератор `prisma-client` с выводом в проект, driver adapters,
  `migrate dev` больше не запускает generate/seed. Есть блок «ПРО ВЕРСИИ» с объяснением.
- Apollo Server 5 + `@as-integrations/express5` — верно (интеграции вынесены в отдельные пакеты).
- GraphiQL вместо удалённого playground — верно.
- Предупреждение про смену пути данных в PostgreSQL 18 — полезно.

## 🟡 Мелочи
- «NestJS 11/12» — хорошо, что с запасом; проверь при старте, какую версию реально поставит `nest new`.
- `redis:7-alpine` — актуален Redis 8 (см. `fixes/redis.md`); для подписок разницы нет.
- В этой лабе Prisma 7, в NestJS-лабе Prisma 6 — это **намеренно** (в NestJS это объяснено), но в корневом README
  стоит одной фразой сказать, чтобы не выглядело рассинхроном.
- Самостоятельность («ни от одной лабы не зависит») подтверждается текстом — ссылок на другие лабы в методичке нет.


---

## ✍️ Варианты решений

Оставь в каждом вопросе **один** вариант (остальные удали или поставь `[x]` у нужного).
Потом я прочитаю этот файл и перепишу лабу ровно по выбранному. ⭐ — моя рекомендация.

### 1. Prisma 7 здесь, Prisma 6 в NestJS
- [x] ⭐ A — одна фраза в корневом README: разные версии намеренно (NestJS зафиксирована на 6, GraphQL показывает 7)
- [ ] B — не трогать

### 2. Redis 7
- [x] ⭐ A — как решишь в `site.md` (вопрос 3)
- [ ] B — отдельно: оставить 7

---

## 📖 Вычитка методички

### Часть 1 (разделы 1–3)
- — сверил: оглавление (13 разделов + 3 сессии шагов) против всех `<h2 id="sec-N">`/`<div class="step" id="step-X-Y">` — все ссылки TOC ведут на существующие якоря, нумерация шагов (1.1–1.5, 2.1–2.4, 3.1–3.3, 4.1–4.4, 5.1–5.4, 6.1–6.6) не пересекается и не дублируется в пределах видимого текста; нумерация терминов-сносок (¹…³⁵) идёт по порядку появления без пропусков/повторов и все `href="#term-N"` резолвятся; таблица nullability ([Review]/[Review!]/[Review]!/[Review!]!) соответствует спецификации GraphQL; итоговая SDL-схема (Movie/Person/Credit/CastCredit/DirectorCredit/Review/User/ReviewConnection/Query/Mutation/Subscription) сверена с примером запроса из 2.1 (поля/типы/аргументы совпадают: movie(id: ID!), director: Person!, cast: [CastCredit!]!, reviews(first, after)) и с таблицей «модуль NestJS → корневые поля» (MoviesModule/ReviewsModule/AuthModule/UsersModule владеют ровно теми полями, что перечислены в Query/Mutation/Subscription); сценарий в разделе 6 (кол-во SQL на шаг) пересчитан вручную и совпадает с логикой батчинга из раздела 5 (шаг 2 — 7 SQL = 4 базовых + 3 на отзывы/авторов; шаг 8 — LIMIT first+1=6 согласно «трюку» из раздела 8); диаграммы (parse→validate→execute, N+1, архитектура) не противоречат сопровождающему тексту. Латиницы вместо кириллицы и сырых бэктиков не найдено (grep по исходному HTML). Расхождений не найдено.

### Часть 2 (разделы 4–9, шаг 1.1)
- — сверил: таблица стека (раздел 4) против команд `npm i` в шаге 1.1 — все пакеты из таблицы (GraphQL-триада, Prisma+adapter-pg, dataloader, class-validator/transformer, @nestjs/jwt+bcryptjs, graphql-subscriptions/graphql-redis-subscriptions/ioredis, graphql-query-complexity) присутствуют в командах установки; дерево файлов проекта (раздел 4) против структуры модулей и имён классов, упомянутых в «Под капотом» (MoviesResolver/MovieReviewsResolver ↔ movies.resolver.ts/movie-reviews.resolver.ts, LoadersFactory ↔ loaders.factory.ts) — совпадает; `.gitignore`-строка `src/generated/` в шаге 1.1 согласована с комментарием «ГЕНЕРИРУЕТСЯ, в .gitignore» у `generated/prisma/`, а `schema.gql` (коммитится) не подпадает под игнор; раздел 8 (offset vs cursor, LIMIT first+1, защита от тяжёлых запросов) сверен со схемой из раздела 3 (Query.movies — offset/limit, Movie.reviews — first/after) и со сценарием раздела 6 — противоречий нет. Раздел 9 проверен только до конца шага 1.1 (граница части); проверены анкоры `#step-1-1`/`#step-1-2` и корректность bash-команд (перенос строки через `\`, `--skip-git`, `echo >> .gitignore`). Расхождений не найдено.

### Часть 3 (шаги 1.2–2.2)
- — раздел сверен: docker-compose.yml (postgres:17 lab/lab/cinegraph, redis:7-alpine, healthchecks), .env, prisma.config.ts, schema.prisma (модели User/Person/Movie/CastMember/Review, индексы, @@unique([movieId, authorId])), tsconfig.build.json, seed.ts (состав актёров, количество пользователей/рецензий сверено со скриптом), src/prisma/prisma.service.ts, app.module.ts/main.ts, models.ts (Person/Movie/CastCredit) — имена файлов, классов и полей соответствуют дереву проекта из части 2 и друг другу; расхождений не найдено.

### Часть 4 (шаги 2.2–4.1)
- **[противоречие] Шаг 3.2 vs раздел 5 (часть 2) и шаг 1.4 (часть 3)** — раздел 5 для запроса `movies(limit: 10) { title director { name } cast { character person { name } } }` даёт «Movie.cast 10 … CastCredit.person ~28 … ──── ~49 SQL», а шаг 3.2 для того же самого запроса (CatalogPage) ожидает `grep -ac 'prisma:query' api.log # ≈ 43`. По сид-данным шага 1.4 в CastMember всего 21 запись (3+3+3+1+2+2+2+3+1+1), значит без DataLoader CastCredit.person вызовется 21 раз, а не ~28, и итог — 1+10+10+21=42, что близко к «≈43» из шага 3.2, но противоречит «~28»/«~49» из раздела 5. → В разделе 5 поправить таблицу на актуальные цифры (21 и 42/43), чтобы шаг 3.2 совпадал с теорией.
- **[тех] Шаг 2.3, «Под капотом»** — «Поменять глобально можно опцией nullable в buildSchemaOptions» → в `@nestjs/graphql` (проверено по пакету 14.0.2, `BuildSchemaOptions`: dateScalarMode, numberScalarMode, scalarsMap, orphanedTypes, skipCheck, directives, fieldMiddleware, noDuplicatedFields, addNewlineAtEnd) такой опции нет — ни `nullable`, ни `nullableByDefault` (последняя есть только в type-graphql). (Уточнено при сверке: агент предлагал `nullableByDefault` — это тоже неверно для Nest.) → Исправить: «глобального переключателя в @nestjs/graphql нет — nullability задаётся на каждом поле через `@Field({ nullable: true })`».
- **[тех] Шаг 2.4** — пример интроспекции `{ __type(name: "Movie") { name description fields { name type { kind name ofType { kind name ofType { name } } } } } }` даёт только 3 уровня вложенности (`type`→`ofType`→`ofType.ofType`, причём на третьем уровне запрошено только `name` без `kind`), а в тексте это преподносится как способ увидеть `genres: [Genre!]! — NON_NULL → LIST → NON_NULL → ENUM`. Для `[Genre!]!` нужно 4 уровня (`type.kind`, `ofType.kind`, `ofType.ofType.kind`, `ofType.ofType.ofType.name`), иначе `ofType.ofType.name` вернётся `null` (у обёрточного типа NON_NULL нет `name`), и имя `Genre` в ответе не появится. → Добавить в пример ещё один вложенный `ofType { kind name ofType { name } }`.
- — остальное (шаг 3.1: MoviesResolver/PeopleResolver/CastCreditResolver — поля и параметры @ResolveField/@Parent соответствуют models.ts; шаг 4.1: LoadersFactory/byId/groupedBy, ключи загрузчиков (person/movie/user/castByMovie/castByPerson/moviesByDirector/reviewsByAuthor) соответствуют полям Prisma-моделей из части 3; GqlContext/context() согласованы с AppModule) проверено, расхождений не найдено.

### Часть 5 (разделы Шаг 4.2–5.4)
- — сверено: анкоры/заголовки `step-4-2..step-5-4` в HTML совпадают с оглавлением и с `<span class="num">`; ссылки из TOC (`href="#step-X-Y"`) ведут на верные id, повисших якорей нет.
- — сверено: `Loaders`/`LoadersFactory` (src/loaders/loaders.factory.ts из части 4) — добавление `reviewStats` в шаге 4.2 не конфликтует с уже существующими `person/movie/user/castByMovie/castByPerson/moviesByDirector/reviewsByAuthor`; `reviewsByAuthor`, используемый в шаге 5.2 (`loaders.reviewsByAuthor.load`), действительно объявлен в 4.1.
- — сверено: `Movie`/`Person`/`Review`/`User` (модели из частей 3–4) не содержат полей `averageRating`/`reviewCount`/`email`(@Field)/`reviews` — они добавляются через `@ResolveField` в отдельных резолверах (`MovieReviewsResolver`, `UsersResolver`), конфликтов декларации полей нет.
- — сверено: `AddReviewInput`/`UpdateReviewInput`/`Review` — типы `rating`/`text`/`movieId` совпадают с `model Review` (prisma/schema.prisma, часть 3), включая `@@unique([movieId, authorId])` → корректно обрабатывается как `ALREADY_REVIEWED` (P2002) в `ReviewsService.add`.
- — сверено: `GqlContext`/`AuthUser` (common/context.ts, часть 4) — поля `req?/user/loaders` совпадают с тем, что кладёт `context()` в шаге 4.3; `GqlAuthGuard`/`RolesGuard`/`CurrentUser`/`Roles` используют `GqlExecutionContext.create(context).getContext<GqlContext>()` согласованно.
- — сверено: `MoviesResolver.movies`/`MoviesResolver.movie` (часть 4) — `movies` без `nullable` (→ `[Movie!]!`), `movie` с `{ nullable: true }` — согласуется с примерами Эксперимента 2 в шаге 5.1 (`movies` роняет весь `data`, `movie(id)` гасит ошибку на себе).
- — сверено: `process.env.LAB_FAIL_DIRECTOR_OF_MOVIE` (рычаг из part 4, резолвер `director`) корректно используется в Эксперименте 2 шага 5.1.
- — сверено: ссылки «см. раздел 7» (шаги 5.1, 5.2) указывают на раздел «7. Ошибки и nullability» — совпадает с оглавлением.
- — остальное: пройден код шагов 4.2–5.4 целиком (DataLoader reviewStats, AuthService/AuthResolver/AuthModule, ReviewsService/ReviewsResolver, users.resolver email/reviews, CreateMovieInput/createMovie, Credit/CastCredit/DirectorCredit/SearchResult, курсорная пагинация Reviews) на технические ошибки, противоречия в именах файлов/классов/полей и опечатки — расхождений не найдено.

### Часть 6 (Шаг 5.1(частично, см. выше)–6.1 начало)
- — сверено: `formatGqlError` (src/graphql/format-error.ts) — использование `unwrapResolverError`, `GraphQLFormattedError`, `formatError`/`includeStacktraceInErrorResponses` как опций Apollo Server через `GraphQLModule.forRootAsync` — валидные, реально существующие API.
- — сверено: примеры кодов ошибок (`BAD_USER_INPUT`, `UNAUTHENTICATED`, `FORBIDDEN`, `NOT_FOUND`, `ALREADY_REVIEWED`, `EMAIL_TAKEN`) в `common/errors.ts` (введён в шаге 4.3, часть 5) используются далее без новых незаявленных кодов.
- — сверено: `Credit`/`CastCredit`/`DirectorCredit`/`SearchResult` (шаг 5.3) — `CreditResolver` заменяет удаляемый `cast-credit.resolver.ts` (из части 4); поля `movie`/`person` резолвятся через существующие `loaders.movie`/`loaders.person`.
- — сверено: `ReviewConnection`/`ReviewEdge`/`PageInfo`/`encodeCursor`/`decodeCursor` (шаг 5.4) — индекс `@@index([movieId, id])` в `model Review` (часть 3) соответствует запросу `where: { movieId, id: { lt } }, orderBy: { id: 'desc' }`.
- — сверено: переход в шаг 6.1 (`PubSubModule`, `REVIEW_ADDED`, публикация события в `ReviewsService.add`) — текст обрывается на границе файла (продолжение в части 7, `reviews.resolver.ts` Subscription) — это следствие нарезки на части, не ошибка методички.
- — остальное: пройден код шага 5.1 (продолжение) и начала 6.1 целиком (formatError, PubSubModule) на технические ошибки, противоречия имён/полей и опечатки — расхождений не найдено.

### Часть 7 (шаг 6.1 продолжение — 6.4: подписки, Redis PubSub, клиент без библиотек, depth limit и complexity)
- — проверено: код `reviews.resolver.ts` (`filter`/`resolve` подписки, `clearAll()`), `pubsub.module.ts` (in-memory и Redis-версии), клиент `client/index.html` (fetch+graphql-ws), `depth-limit.rule.ts`, `complexity.plugin.ts`, итоговый `app.module.ts` — сверены между собой и со схемой из раздела 3 (поля `Review`, `Movie`, `Subscription.reviewAdded(movieId: ID!): Review!`); сверены имена файлов/классов/DI-токенов (`PUB_SUB`, `REVIEW_ADDED`) между шагами 6.1 и 6.2; проверены перекрёстные ссылки «шага 2.1» (enableCors), «шага 2.4» (CSRF/preflight), «раздела 5» (правило «один запрос — один кэш»), «шага 3.2» (запрос `CatalogPage`), номера заданий Production Hell №3/№7/№9, упомянутые в тексте, — все совпадают с таблицей заданий в части 8 (шаг 6.6); расхождений не найдено.

### Часть 8 (6.5 тесты, 6.6 Production Hell, разделы 10–12: чек-лист, глоссарий, вопросы)
- — проверено: `loaders.factory.spec.ts` и `app.e2e-spec.ts` (пути импортов `./loaders.factory`, `../prisma/prisma.service`, `../src/app.module`, соответствие GraphQL-полям и кодам ошибок `UNAUTHENTICATED`/`BAD_USER_INPUT`/`ALREADY_REVIEWED`/`FORBIDDEN`, `maxDepth: 8` — совпадает с дефолтом `GQL_MAX_DEPTH ?? 8` из части 7); таблица Production Hell (11 пунктов) сверена с упоминаниями №3/№7/№9 из части 7 — совпадает; проверена нумерация сносок глоссария: во всём документе ровно 35 ссылок `href="#term-N"` (N=1..35), без пропусков и дублей, и все id `term-1..term-35` определены в этой части; все `href="#..."` во всём файле (все части) ведут на существующие `id` — битых якорей нет; чек-лист (раздел 10) сверен построчно с шагами сборки (например, «Тесты и эволюция … 2.4, 6.5, 6.6» — в шаге 2.4 действительно `git commit` с `schema.gql`); латиницы вместо кириллицы и сырых бэктиков вне блоков кода не найдено; расхождений не найдено.

### Часть 9 (раздел 13: «Что дальше»)
- — проверено: таблица дорожной карты (Apollo Client/urql, GraphQL Code Generator, Persisted queries/APQ, Federation, @defer/@stream, Relay Global ID, GraphQL Inspector, кастомные скаляры/директивы, наблюдаемость, альтернативные серверы, Lighthouse) — темы согласуются с материалом лабы (Persisted queries — термин 35 из глоссария, Federation/defer упомянуты как развитие тем из разделов 6 и Production Hell №11); упоминание «тот же CineGraph на Laravel» сверено с независимостью лабы (раздел 1: «ни от одной другой лабы не зависит») — противоречия нет, это просто пример для сравнения, а не зависимость; расхождений не найдено.

### ✍️ Решение по вычитке
- [x] ⭐ A — исправить всё из вычитки выше
- [ ] B — исправить только [тех] и [противоречие]
- [ ] C — выборочно (отметь пункты выше)
