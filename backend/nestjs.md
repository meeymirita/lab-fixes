# NestJS Lab — итоги вычитки и проверки

**Вычитка:** ✅ пройдено 24.09 (относится к старой 5-сессионной версии, ниже); перестройка 5→14 сессий дописана 15.10.2026, построчной вычитки новых сессий 2–14 ещё не было — см. запись 15.10 в `_state-log.md`. Находок: 4 (тех 1, противоречий 3, текст 0) в старой версии.  
**Проверка запуском и в браузере:** см. разделы «🧪» ниже и таблицу `fixes/common/_verification.md` (там же уровень проверки и что не проверялось).

## 🧪 Построчная вычитка и полный прогон сессий 1–14 (24.10.2026, Docker, Node 24, NestJS CLI 11.0.24, Prisma 7.10.1, PostgreSQL 18)
Проект собран **с нуля по блокам методички** (`nest new` → сессия 14), каждая команда и curl из шагов выполнены, итог: `npm test` — 7 passed, `npm run test:e2e` — 6 passed, `docker compose --profile app up --build` — api healthy. Найдено и исправлено в тексте:
- **7.2 (главное).** (а) строка `getRequest<{ headers: Record<string, string | undefined>; user?: unknown }>()` была записана с неэкранированными `<…>`: браузер съедал `<string, string | undefined>`, в окне получалось `getRequest; user?: unknown }>()` (код не компилировался); (б) `Auth()` импортировал `roles.decorator`, который появлялся только в 9.1 — `TS2307` на сборке; (в) **ожидаемые `200` на `curl -H "X-Api-Key: …" /api/tickets` в тексте не получались**: `ApiKeyGuard` стоял локально через `@UseGuards`, а глобальный `JwtAuthGuard` срабатывает раньше и отвечает 401 (поэтому и «ловушка про порядок» в тексте была неверной); (г) `ConfigService` без `<Env, true>` не давал `{ infer: true }`. Шаг переписан: `roles.decorator` создаётся в 7.2, `ApiKeyGuard` — глобальный и регистрируется **перед** `JwtAuthGuard`, тот пропускает запрос с уже установленным `req.user`; результат проверен (верный ключ 200, неверный 401, без ключа и токена 401), «Под капотом» про И/ИЛИ переписан.
- **10.2.** «второй рубеж» (`@Exclude()` на поле `internal`) скрывал лишь **флаг**, сама внутренняя заметка клиенту всё равно уходила (в старом тексте это признавалось в конце); в «ожидаемом результате» стояла бессмысленная ошибка `jq`. Теперь второй рубеж фильтрует записи целиком (`!c.internal || canSeeInternalComments`), DTO отдаёт `internal`, результат проверен: при выключенном первом рубеже клиент получает только публичную запись, агент — обе.
- **5.1 / 6.1.** с driver adapter у `P2002` **нет `meta.target`** — `fields` в ответе фильтра был `undefined` (в тексте обещалось `fields: ["email"]`); теперь `constraint: "User_email_key"` из `meta.driverAdapterError.cause.constraint.index`; ссылка «фильтр из 4.3» → 5.1.
- **9.2 ↔ 10.1 (порядок).** шаг 9.2 велел править `CommentsService`, которого ещё нет (появляется в 10.1); публикация события `comment.created` перенесена в листинг 10.1.
- **14.2 (compose).** healthcheck `wget http://localhost:3000/…` **никогда не становился healthy** (в alpine `localhost` → `::1`, приложение слушает IPv4): заменено на `127.0.0.1`, контейнер healthy; добавлено пояснение и совет по `P3018 … already exists` (один раз при холодной сборке `migrate` упал — повторные запуски с нуля проходили чисто).
- **Числа и выводы приведены к фактическим:** 1.6 (вторая ошибка `Object не зарегистрирован`), 2.2 (полный текст ошибки `PORT`), 5.2 (`HIGH → URGENT`, а не `MEDIUM`; тикет 1 в сидах — `HIGH`), 3.3 (`Raw query failed. Code: N/A`), 8.1 (после кражи актуальный `jar.txt` получает `reuse detected`, а не `already used`), 11.1 (`exception` содержит `cause`), 12.2 (реальная схема `CreateTicketDto`), 12.3 (логин для токена входит в лимит), 13.2 (`SERVICE_API_KEY` в `.env.test`), раздел 1 («пять сессий» → четырнадцать), 2.2 (квиз: `ConfigService<Env, true>` терялся при отображении).
- Прочее: `.env` и `docker compose --profile app` под Prisma 7.10.1 работают; `Test`-спеки проходят только с `moduleNameMapper` (шаг 3.2 говорит об этом, подтверждено: без него `Cannot find module './internal/class.js'`).

**Не проверено запуском:** задания «Production Hell» 14.3 — только формулировки (они для самостоятельного решения); `--scale api=2` за Traefik; Vue-клиент.

## 15.10.2026 — находка при продолжении перестройки после сбоя IDE
Перестройка 5→14 сессий (начатая 12.10) была дописана до конца в сессии работы, прерванной сбоем IDE — результат остался на диске незакоммиченным и незаписанным в журнал. При продолжении (диагностика состояния + чек-лист) найдено:

- **[тех] Раздел 1 (теория), 8 блоков-«заблуждений»** — написаны инлайн-стилем (`<div style="margin:24px 0;padding:24px 28px;background:var(--color-accent);color:#fff">`) вместо установленного 12.10 стандарта (правило «caddy как ориентир», `feedback_caddy_as_standard` в памяти). Сверка с уже готовыми PostgreSQL/Bash/Express подтвердила: правильный паттерн — голый `<div>` для блока-проблемы + `<div class="tip">` для блока-решения, без инлайн-стилей. Исправлено через `bundle.jsub(unit='sec-1')` (8 замен).
- **[тех] В шаблоне `nestjs.html` не было CSS-правила `.tip,.trap`** — значит 10 блоков `<div class="tip">`, уже написанных в сессии 1, рендерились бы без оформления (плоский текст без рамки). У caddy/postgresql/bash/express это правило есть (патчено индивидуально по мере появления `.tip`-боксов в их контенте, не является частью общего шаблона по умолчанию). Добавлено через `bundle.patch_template` — то же правило, что в остальных лабах.

Обе находки — не в контенте, а в вёрстке/оформлении; содержание сессий 2–14 (текст, код, задания) не вычитывалось построчно.

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
