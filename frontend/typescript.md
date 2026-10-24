# TypeScript Lab — итоги вычитки и проверки

**Вычитка:** ✅ пройдено 23.09; найдено 13 (тех 7, противоречий 6, текст 0); все внесены в методичку.  
**Проверка запуском и в браузере:** см. разделы «🧪» ниже и таблицу `fixes/common/_verification.md` (там же уровень проверки и что не проверялось).

## Находки чтения методички (23–26.09 и 04.10) — дайджест
Полные формулировки не хранятся: каждая находка исправлена в методичке. Здесь — суть, чтобы понимать, какие классы ошибок встречались.

- **[противоречие] Шаг 5.4, карта проекта («Финал: до / после»)** — итоговое дерево проекта заканчивается строкой «`tests/ 19 vitest-тестов, из них ~10 содержат expectTypeOf / @ts-expect-error`», как будто у тестов есть отдельн…
- **[тех] Раздел 2.10 → 2.12, приведение типов** — раздел 2.10: «`const cfg = { units: ['pcs', 'kg'], maxQty: 1000 } satisfies Config`» использует тип `Config`, который нигде раньше не объявлен; раздел 2.12 только потом даёт «`…
- **[противоречие] Раздел 2.12, keyof/typeof** — «`type Unit = Item['unit'] // тип поля`» обращается к полю `unit`, которого нет: `Item` определён строчкой выше в разделе 2.3 как «`{ id: string; name: string; minStock?: number;…
- **[противоречие] Раздел 4.1, generics-превью** — «`groupBy(movements, 'kind') // Map<'in' | 'out' | 'transfer', Movement[]>`» подразумевает `Movement` с тремя вариантами кind, но реальный `Movement` (сессия 2, шаг 2.2) — unio…
- **[противоречие] Раздел 5, вступление** — «Три границы в лабе: `argv / файл CSV / JSON / HTTP-тело`» перечисляет четыре элемента через слэш, а не три. → Либо сгруппировать («`argv / файл (CSV/JSON) / HTTP-тело`» — три границы…
- **[противоречие] Раздел 5, пример Zod-схемы** — `z.object({ kind: z.literal('out'), …, reason: z.enum(['sale', 'writeoff']) })` — в схеме для `out.reason` только два значения, а доменный `OUT_REASONS` (сессия 2, шаг 2.2) — «`…
- **[тех] Шаг 1.1, стенд** — «`docker compose exec dev npm run typecheck # OK (файлов ещё нет)`»: на этом шаге в `packages/core/src` существует только `playground/.gitkeep`, ни одного `.ts`-файла нет, а `tsconfig.json` пакета и…
- **[тех] Шаг 1.3, `02_unions.ts`** — комментарий «`// без default: если добавить вариант в Shape, TS скажет «not all code paths return a value» — тоже защита`»: `area` объявлена с явным возвращаемым типом `: number`, а `noImpl…
- **[противоречие] Раздел 8, структура проекта** — «`├── playground/ сессия 1: 01–05_*.ts — песочница`» утверждает, что все файлы `01–05` создаются в сессии 1. По факту (шаги 1.2–1.5) в сессии 1 создаются только `01_basics.ts`……
- **[тех] Шаг 2.3, «Зачем» под `stock.ts`** — «…и `explain()` обязан обработать все (нет `default` — при новом коде компилятор скажет «не all code paths return»)»: та же неточность, что и в шаге 1.3 (часть 2). `explain(e: Stock…
- **[тех] Шаг 3.3, `packages/core/src/config.ts` (комментарий к `satisfies`)** — «config.locations[0] // 'A1' | 'A2' | 'B1' | undefined — кортеж литералов, а не string[]» → Проверено в tsc (strict): без `as const` массив `locat…
- **[тех] Шаг 3.3, самопроверка после `totalsByKind`** — «добавьте в Movement пятый kind (как в 2.2) — satisfies Record<MovementKind, number> в totalsByKind даст ошибку «Property 'return' is missing». Уберите.» → Проверено в ts…
- **[тех] Шаг 3.4, «🔬 Под капотом: as Movement в apply»** — «После спреда { ...input, id, at } TS выводит пересечение «union без id/at» & «{ id; at }» — это корректный Movement, но компилятор не всегда умеет свернуть такое обра…

## 🧪 Проверка версий 03.10.2026 (node:24, TypeScript 5.9.3 и 6.0.3)
Сборка полного прохождения автоматически не вышла: часть блоков методички — патчи к уже созданным файлам (`warehouse.ts` дописывается в трёх местах), поэтому собрать workspace «как есть» без ручной склейки нельзя. Но для вопроса «ломает ли TypeScript 6» достаточно сравнения: на одном и том же собранном дереве наборы ошибок `tsc --noEmit` для `core`, `cli`, `api` **идентичны на 5.9.3 и 6.0.3** (4 / 6 / 22 — все из-за неполной склейки, одинаковые). Базовый `tsconfig.base.json` (`NodeNext`, `strict`, `noUncheckedIndexedAccess`, `verbatimModuleSyntax`) на 6.0 компилируется без новых ошибок и предупреждений об устаревших опциях.

- ✅ `typescript` в методичке `^5.6` → `^6.0`; в тексте «TypeScript 6.0 (код проверен и на 5.9)».
- ✅ `@types/node` `^22` → `^24` (иначе типы Node не совпадали с `node:24` после перехода на Node 24).
- Не менялось и не проверялось запуском: `vitest ^2.1`, `zod ^3.23`, `express ^5.0`, `esbuild ^0.24` — актуальны более новые мажоры (vitest 4, zod 4); перед обновлением нужен полный прогон.

Vue-лаба: `npm create vue@latest web -- --router --pinia --vitest --default` на node:24 ставит сейчас Vue 3.5.42, **Vite 8.2**, Vitest 4.1, TypeScript 6.0; `npm run build` и `npm run test:unit` проходят. В методичке «Vite 6+» заменено на «Vite 8».

- ✅ **Проверка на новых мажорах (03.10, вечер):** `zod 4.6`, `vitest 5.0`, `express 5.2`, `typescript ~6.0` — схема `discriminatedUnion` с `z.coerce`, `z.infer`, `safeParse` (в т.ч. ошибки), `vi.useFakeTimers`, типизированный `Request<…>`/`Response<…>` в Express 5 работают без правок (`tsc --noEmit` без ошибок). В методичке `vitest ^2.1` → `^5.0`, `zod ^3.23` → `^4.0`.

## 🧪 Полный сухой прогон — 04.10.2026 (node:24, TypeScript 6.0.3, Vitest 5.0.3, Zod 4, Express 5, Vue 3.5 + Vite 8, Chromium)
Workspace собран по блокам всех шагов 1.1–5.4 в Docker: `core`, `cli`, `api`, `web`. Итог: `npm run typecheck` (core + cli + api + `vue-tsc`) — OK, `npm test` — 10 файлов, 23 теста, `npm run build` (cli-бандл + web), CLI по сценарию 4.1–4.4 (`item:add`, `stock:in/out/list`, коды выхода 3 и 2, `import:csv` — 3 успеха и 3 ошибки), API на Express (200 / 422 / 400), веб-страница в Chromium (таблица из API, форма, строка с ошибкой «на складе A1 только 85 b6, нужно 1000», обновление таблицы), три намеренные ошибки типов из 5.3 (`'oops'`, `(id: number)`, пропавший `unitCost`) — все воспроизводятся.
**Найдено и исправлено в методичке (9 правок):**
- **[тех] 1.1 `tsconfig.base.json`** — в TS 6 `types` по умолчанию пустой, `@types/node` сам не подключается: `typecheck` падает на `process` (`TS2591`) → добавлено `"types": ["node"]`.
- **[тех] 4.1** — вставляемые в `warehouse.ts` методы используют `locationId`, а в импорте его нет → оговорка про импорт.
- **[тех] 4.1/4.4/5.2 — `data/` и «из корня»:** `npm run -w @warehouse/cli dev` запускает скрипт из `packages/cli`, а `data/` создан в корне → `ENOENT data/items.json` (у API — пустой `[]`). → `"wh": "tsx packages/cli/src/main.ts"` и `npx tsx watch packages/api/src/server.ts` из корня.
- **[текст] 4.2 / 5.2** — Zod 4 пишет `Invalid option: expected one of "sale"|"writeoff"|"sample"` (в тексте — формат Zod 3 «Invalid enum value…»).
- **[тех] 4.3 `globals.d.ts`** — файл-модуль (`export {}`), поэтому `declare const __WH_VERSION__` не глобален (`TS2304` в `main.ts`) → константа перенесена внутрь `declare global { … }`.
- **[текст] 4.4** — `dist/wh.js` ≈ 750 КБ (zod 4 внутри), а не «60–80 КБ».
- **[тех, серьёзно] 5.3** — страница Vue в браузере **пустая**: корневой `@warehouse/core` тянет `warehouse.ts` (`node:crypto`) и `json-repository.ts` (`node:fs`), Vite падает с `Cannot access "node:crypto.randomUUID" in client code`; `vue-tsc` без `types: node` тоже ругается → отдельная точка входа `@warehouse/core/browser` (`exports` + `src/browser.ts`), веб-файлы импортируют из неё.
- **[текст] 5.3** — «красная строка»: у `.err` нет стиля → «строка с ошибкой».
**Мелочи:** блоки с `// packages/…/package.json` — это комментарий-заголовок, а не часть JSON (при копировании целиком `npm install` падает); дублируются в одном блоке `item.ts` + `location.ts` и т. п. — чтение блока «как есть» не работает без разбиения по заголовкам.

## 🧪 Повторная сборка по исправленному тексту — 04.10.2026 (поздний вечер)
Workspace собран заново скриптом, который берёт файлы и патчи **только из блоков уже исправленной методички** (без моих ручных правок): `tsc` core/cli/api — чисто, `npm test` — 10 файлов / 23 теста, CLI (`item:add`, `stock:in/out`, `import:csv` с тремя ошибками), `vue-tsc` и `vite build` без предупреждений про `node:*`, страница Vue в Chromium (таблица из API, форма, без ошибок). Заодно блок про `@warehouse/core/browser` в 5.3 оформлен настоящим кодом (`core/package.json` и `browser.ts`), а не строкой-подсказкой.


## 🧪 Прогон сессий 6–10 (22.10.2026, Docker, Node 24, TypeScript 6.0, Vitest 5.0.5)
Новые сессии 6–10 (написаны 21.10 без запуска) прогнаны: рабочая папка собрана из блоков методички (шаги 1.1–9.5; пакет `web` и правки сессии 5 к ней — вне прогона), `tsc`, `tsc -b`, Vitest, CLI через `tsx`. Все блоки «Ожидаемый результат» шагов 6.2–9.5 заменены настоящим выводом. Найдено и исправлено:
- **6.2 (+6.4):** `Filter<T>` сохранял `readonly` полей доменных типов — `filter-string.ts` не собирался (`TS2540: Cannot assign to 'qty' because it is a read-only property`); в тип добавлен `-readonly`.
- **6.3/6.4:** рантайм не проверял оператор: `--query 'kind_gt=in'` проходил, хотя `FilterKey` такое запрещает на уровне типов. Добавлены `isKnownOp()` в `filter-spec.ts` и проверка в `parseFilterString`; теперь ошибка `оператор "gt" не подходит полю "kind"`.
- **7.1:** Vitest 5 (Vite 8, Oxc/Rolldown) **не транспилирует стандартные декораторы** TS 5 — тесты, импортирующие класс с `@logged`/`@frozen`, падают `SyntaxError: Invalid or unexpected token`. Нужны `unplugin-swc` + `@swc/core` и `vitest.config.ts` с `decoratorVersion: '2022-03'` (проверено: 12 файлов / 27 тестов зелёные). `tsx` и `esbuild` декораторы понимают без настроек.
- **7.3:** `bootstrap.ts` импортировал `isItem`/`isMovement` из `@warehouse/core`, которых там нет (они жили в `cli/main.ts`) — `TS2724`; предикаты вынесены в `guards.ts`.
- **7.4:** во фрагменте `config.ts` не хватало `import { frozen }`.
- **8.2:** `container.types.test.ts` вызывал `c.resolve(NUM)` по-настоящему и падал `Нет регистрации для токена` до проверки типов — токены регистрируются заранее.
- **8.3:** при испорченном `MovementOf` ошибки приходят в `movement.test.ts`, `movement.types.test.ts` и `schemas/movement.test.ts`, а не на строке `not.toHaveProperty('from')` — описание приведено к факту.
- **9.4:** `tsconfig.tsbuildinfo` лежит рядом с `tsconfig.json` пакета (`packages/<пакет>/tsconfig.tsbuildinfo`), а не в `dist/` — исправлены текст, команды и ключ кеша CI. Проверено: `tsc -b` 1,4 с с нуля, 0,2 с повтор; удаление `tsbuildinfo` у `cli` пересобирает только `cli`; устаревший `dist` даёт `TS2305` в `tsc`, а `tsx` видит новое — как в 9.2.
- Прочее: CLI печатает `[apply] 1ms` от `@logged` (через `console.debug`); `npm run build` кладёт `dist/wh.js` рядом с выводом `tsc` — коллизии нет.

## 🧪 Вычитка и дозапуск (24.10.2026, Docker, Node 24)
Ассистент прочитал сессии 6–10, теоретические и справочные разделы и проверил запуском то, что оставалось: шаг 1.1 буквально через `docker compose up -d` / `exec dev npm install` / `npm run typecheck` (даёт `TS18003`, как в тексте); пакет `web` (`npm create vue@latest web -- --ts --pinia`, Vite 8.2, `vue-tsc --build`) вместе с project references из 9.1–9.2. **Найдено и исправлено:**
- **9.2** — `exports` в `packages/core/package.json` терял subpath `./browser` из 5.3: `npm run -w web type-check` падал `TS2307: Cannot find module '@warehouse/core/browser'` (а `vite build` проходил, если компонент не попал в сборку). В блок добавлены оба условия для `./browser`.
- **8.1** — эксперимент с `expectTypeOf` лежал в файле без `.test.ts`, `vitest run playground/08_type_tests.ts` отвечал «No test files found»; файл переименован в `08_type_tests.test.ts` с `it(...)`, команда с полным путём, текст ошибки `TS2344` заменён настоящим (`Type 'number' does not satisfy the constraint '"Expected: number, Actual: string"'`).
- Оглавление страницы: «Задания: **пять** сессий» (старый `tocHtml`) → «десять».
- Из шагов 8.4, 9.3, 9.4 убраны ссылки на внутренние файлы сайта (`CLAUDE.md`, `audit_manuals.py`, `anitech-performance`); опечатки «почемуget/set», «библиotekaх»; вопрос 7.2 ссылался на «декоратор поля из 7.4» (там аксессор).
- Справка не знала сессий 6–9: добавлены строки в таблицу инструментов (`unplugin-swc`, `tsc -b`), дерево проекта (`di/`, фильтры), чек-лист (декораторы, DI-контейнер, фильтры на типах, project references), глоссарий (5 терминов), вопросы «Сессии 6–9» (6 вопросов); «Что дальше»: Project references и Nest — сданы в прошлое/уточнены, имя файла `Vue_Lab_Helpdesk.html` → «лаба Vue на сайте».

**Не проверено:** решение итогового ТЗ (сессия 10 — задание для самостоятельной работы, запускать нечего).
