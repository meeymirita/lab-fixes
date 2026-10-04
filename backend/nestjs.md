# NestJS Lab — итоги вычитки и проверки

**Вычитка:** ✅ пройдено 24.09; найдено 4 (тех 1, противоречий 3, текст 0); все внесены в методичку.  
**Проверка запуском и в браузере:** см. разделы «🧪» ниже и таблицу `fixes/common/_verification.md` (там же уровень проверки и что не проверялось).

## Находки чтения методички (23–26.09 и 04.10) — дайджест
Полные формулировки не хранятся: каждая находка исправлена в методичке. Здесь — суть, чтобы понимать, какие классы ошибок встречались.

- **[противоречие] Оглавление / нумерация шагов раздела 9** — в сайдбаре и в заголовках методички шаги «Сессии 5» внутри раздела «9. Пошаговая сборка проекта (5 сессий)» пронумерованы `9.1, 9.2, 10.1, 10.2, 10.3` (подтверждено…
- **[тех] Шаг 6.2, пример проверки ролей/владения** — `curl -s -X PATCH -H "Authorization: Bearer $AG" -H "$J" -d '{"status":"RESOLVED"}' localhost:3000/api/tickets/1 | jq .message` с ожидаемым выводом `# OPEN → RESOLVED not al…
- **[противоречие] Шаг 8.1, «Под капотом: … что не отменяет таймаут …»** — «Настоящая отмена требует `AbortController`, передаваемого вниз, и таймаутов на уровне БД (`statement_timeout`). Задание 6 в Production Hell.» → в табли…
- **[противоречие] Шаг 8.3, «Под капотом: … IP за прокси»** — «…лимит по IP легко обойти пулом адресов — для логина надёжнее ключ «IP + email» (задание 7 в Production Hell).» → в таблице шага 10.3 тема ключа «IP + email» для ra…

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


## 🧪 Закрытие 🟡 — 04.10.2026 (стенд `ns-run`: Postgres 18 + собранный Helpdesk API)
- **4.4 откат транзакции:** `throw new Error('boom')` после `createMany` в `update` → PATCH возвращает 500, тикет остаётся `OPEN/HIGH` версии 1, история пуста (0 строк) — транзакция откатилась целиком, как написано.
- **8.1 таймаут:** временный `@Get('slow')` на 12 с в `HealthController` → ответ `408 {"message":"Request Timeout"}` ровно через 10 с.
- Правок методички не потребовалось.

## 🧪 `docker compose --profile app` целиком — 04.10.2026
`migrate` (стадия `build`, `prisma migrate deploy`) → `api` (стадия `runtime`, пользователь `node`): `/api/health/ready` — `{"status":"ok","info":{"database":{"status":"up"}}}`; при `docker compose stop postgres` — `ready` 503 (в логе `Health Check has failed`), `live` 200; после `start postgres` `ready` снова 200; `docker compose stop api` — корректная остановка. Правок методички не потребовалось. Задания 9.5 «Production Hell» — для самостоятельного решения.
