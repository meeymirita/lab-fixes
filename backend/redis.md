# Redis Lab — итоги вычитки и проверки

**Вычитка:** ✅ пройдено 24.09; найдено 7 (тех 2, противоречий 4, текст 1); все внесены в методичку.  
**Проверка запуском и в браузере:** см. разделы «🧪» ниже и таблицу `fixes/common/_verification.md` (там же уровень проверки и что не проверялось).

## 🧪 Вычитка и прогон сессий 4–10 (25.10.2026, Docker: Redis 8.10.2, Laravel 13.38, phpredis 6.3, PostgreSQL 18)
Собран стенд из методички (compose с `redis`, `redis-cache`, `postgres`, реплика, три Sentinel, Laravel с Product/Order/Sanctum), выполнены все блоки шагов 4.1–10.5, кроме перечисленных ниже. У всех шагов с запуском «вывод не получен» заменён настоящим выводом. Найдено и исправлено:
- **4.1.** `hash-max-listpack-entries` по умолчанию **512**, а не 128 (у Set и ZSET — 128); команда возврата порога и вопрос про «1000» поправлены.
- **4.3.** `Redis::lRem('jobs:processing', $job, 1)` падало `TypeError … ($count) must be of type int`: фасад Laravel принимает `lRem($key, $count, $value)`; порядок исправлен.
- **4.5.** HyperLogLog «всегда около 12 КБ» — это потолок; при малом числе значений `MEMORY USAGE` = 80 байт (разреженный вид).
- **5.2.** После `redis-benchmark` с `noeviction` мелкий `SET probe 1` **проходил** (OOM возникает только при памяти выше лимита; 50 клиентов бенчмарка сами раздувают буферы): сценарий переписан (`-c 5` и крупное значение `SETRANGE fat 1500000 x`), числа получены.
- **5.3.** Заготовка Laravel читает `REDIS_CACHE_DB=1`: ключи кэша лежали в базе 1, и `redis-cli DBSIZE/--scan` из текста их не видели; добавлен `REDIS_CACHE_DB=0`. Выяснено: `Cache::lock()` хранит замки на соединении `default` (основной Redis), не на кэш-инстансе.
- **5.4.** `-r 200000` даёт 126 471 ключ (повторы), а не 200 тысяч; на списке в 100 тысяч элементов `DEL` и `UNLINK` не отличаются — разницу показывает множество из 3 млн элементов (170 мс против 12 мкс); `KEYS` на 126 тысячах ключей — 8,6 мс.
- **6.1.** Префикс ключей кэша — `laravel-cache-`, а не `laravel_cache_`.
- **6.5.** `curl -w %{time_total}` через `artisan serve` показывает ≈ 2 с даже для устаревшего значения (встроенный сервер держит соединение до конца отложенной работы): добавлено `time_starttransfer`; в консольных процессах пересчёт откладывается до конца команды.
- **7.3.** `Redis::transaction()` **не быстрее** «по одной» (96 мс против 90 мс на 2000 команд: каждая команда в MULTI идёт отдельным кругом); `pipeline` — 2 мс. Фраза «MULTI/EXEC … тоже пакетный» исправлена.
- **8.6.** `OrderController` и `routes/api.php` нигде не создавались; гость получал 1 запрос в минуту (а не «5 запросов от пользователя»): добавлены `install:api`, заглушка маршрута, токен Sanctum и `$request->user('sanctum')` в лимитере.
- **9.1.** Ответ на вопрос шага: `redis-server --appendonly yes` на каталоге с одним `dump.rdb` стартует **пустым** (RDB молча игнорируется).
- **9.2.** (а) `docker kill` **не теряет** `lastkey` даже при `everysec` (потеря секунды — только при сбое питания/ядра); (б) `yes | docker run … redis:8-alpine redis-check-aof --fix` печатает только справку: точка входа образа запускает всё как `redis-server` — нужен `--entrypoint redis-check-aof`; (в) в Redis 8 есть `aof-load-corrupt-tail-max-size`.
- **9.3.** Первая синхронизация реплики стартует с задержкой `repl-diskless-sync-delay` = 5 с (без `sleep` реплика ещё `down`); `WAIT` в отдельном `redis-cli` возвращает `1` даже при паузе реплики — `SET` и `WAIT` должны идти в одном соединении.
- **9.4.** Failover ≈ 6 секунд после остановки; старый мастер становится `slave` не сразу, а через ≈ 25–30 с (`+convert-to-slave`); `offset` реплики под нагрузкой отстаёт на десятки мегабайт (обновляется раз в секунду), а не «чуть-чуть».
- **9.5.** Значения слотов получены и сверены с настоящим `CLUSTER KEYSLOT` (`orders:stream` 14419, `orders:dlq:stream` 8194, оба `lock:{order:42}…` — 8691).
- **10.1.** Образ стартует с `protected-mode no`, `bind * -::*`; `CONFIG SET dir /tmp` **не проходит** (`can't set protected config`) — текст требовал обратного.
- **10.2.** При `REDIS_USERNAME`/`REDIS_PASSWORD` соединение `cache` Laravel 13 тоже их читает, а `redis-cache` без ACL отвечает `WRONGPASS`: введены `REDIS_CACHE_USERNAME/PASSWORD`; `cache:clear` не отказан (кэш-инстанс без ACL), отказан `FLUSHDB` под `app`.
- **10.3–10.4.** `INFO`, `SLOWLOG`, `LATENCY`, `MONITOR` входят в `@dangerous`: `redis:stats` и команды шага 10.4 нужно запускать под `admin` (под `app` — `NOPERM`).
- Раздел 11 («сессии 4–11 написаны без вычитки…») и подсказка в `works/js/prereq.js` приведены к фактам.

**Не запускалось:** сравнение phpredis и predis (10.5), TLS (10.3), заполнение `redis-cache` до 256 МБ (5.3), `kill -9` воркера List (4.3), настоящая конкуренция в 7.2 (20 процессов `tinker` стартуют по очереди), `ShouldBeUnique` и `expireAfter` в 8.3, замер времени ответа при лавине истечений (5.5), настоящий кластер Redis; шаг 11.1 — итоговое ТЗ без ответа.

## Находки чтения методички (23–26.09 и 04.10) — дайджест
Полные формулировки не хранятся: каждая находка исправлена в методичке. Здесь — суть, чтобы понимать, какие классы ошибок встречались.

- **[противоречие] Раздел 4, дерево каталогов** — «Services/ (StockReservationService, RateLimiter, StreamPublisher)» → класс, реально построенный на шаге 2.2, называется `SlidingWindowRateLimiter`, а не `RateLimiter`; `Product…
- **[тех] Шаг 1.5, `app/Services/ProductCache.php`** — `Redis::set($lockKey, $token, 'NX', 'PX', 3000);` → фасад `Redis` в Laravel при `REDIS_CLIENT=phpredis` (шаг 1.3) идёт через `PhpRedisConnection::set($key, $value, $expireR…
- **[противоречие] Шаг 2.1, заголовок «Distributed lock — StockReservationService» + подсказка «Перед шагом 2.1: перечитать раздел 5.2 (distributed lock) — теперь применим его к резервированию стока»** → код `StockReservationSe…
- **[противоречие] Перед шагом 1.4** — «📖 Почитать: Laravel 13: Eloquent → UUID keys» → ни одна из миграций шага 1.4 (`products`, `orders`, `order_items`, `processed_messages`) UUID не использует — везде `$t->id()` (автоинкреме…
- **[тех] Шаг 3.3 «Приоритет через ZSet»** — `Redis::zAdd('orders:priority', ['nx'], -microtime(true), $order->id); // отрицательный score: чем раньше создан, тем меньше число, тем раньше выйдет из ZPOPMIN` → математически наоб…
- **[противоречие] Шаг 1.2 vs Шаг 3.1** — врезка «🔬 Под капотом: почему не allkeys-lru» в шаге 1.2: «allkeys-lru может вытеснить любой ключ… включая ZSet с retry-счётчиками… воркер-надзиратель (шаг 3.1) может внезапно «забыть»…
- **[текст] Раздел 15, строка «Outbox Pattern поверх Redis»** — «закрывает риск из раздела 1.7» → раздела/подраздела «1.7» в документе нет (у раздела 1 «Что делаем и зачем» нет подпунктов, секции пронумерованы 1–15); ссылка тех…

## 🧪 Сухой прогон 03.10.2026 (Redis 8.10, PostgreSQL 18, Laravel 13.17, phpredis, php:8.4-cli)
Собрано приложение по шагам 1.1–3.4 и проверена каждая служба на живом Redis 8: `ProductCache` (cache-aside с блокировкой), Lua-резервирование склада (`true, false`, остаток 2), скользящее окно (`[true×5, false, false]`), XADD/XGROUP/XREADGROUP/XPENDING, два конкурирующих воркера (20 сообщений → `processed_messages = 20`, PEL пуст), XAUTOCLAIM (формат ответа `[cursor, {id: fields}, []]` совпадает с деструктуризацией `[$cursor, $claimed]`), ZSET + `bzPopMin`.

- **[тех] Шаги 1.3–1.8: воркер никогда не видит сообщений — Laravel добавляет префикс `laravel-database-` ко всем ключам.** `XREADGROUP` возвращает `['laravel-database-orders:stream' => …]`, а код ищет `$messages['orders:stream']` → всегда пусто. Заодно `redis-cli XINFO GROUPS orders:stream` из методички не находит поток. → `REDIS_PREFIX=` (пусто) в `.env` + пояснение. ✅
- **[тех] Шаги 1.8 и 3.1: `Redis::xAck($stream, $group, $id)` падает с `TypeError: Redis::xack(): Argument #3 ($ids) must be of type array, string given`.** phpredis принимает массив ID. Воркер падал на первом же сообщении. → `[$id]`, исправлено также в теоретическом примере. ✅
- **[тех] Шаг 3.3: `Redis::zAdd('orders:priority', ['nx'], …)` — `scores must be numeric`.** Обёртка Laravel принимает опции строкой: `zAdd($key, 'nx', $score, $member)`. ✅
- **[текст] Шаг 1.1–1.3: `build: ./laravel-app` в compose, но Dockerfile в методичке не дан**, а `composer create-project` и `php artisan` запускаются на хосте. `REDIS_CLIENT=phpredis` требует расширение ext-redis (`pecl install redis`), при этом ставится `predis/predis`. Для прогона использован свой Dockerfile (`php:8.4-cli` + pecl redis + pdo_pgsql). Без правок — решить, давать ли Dockerfile в методичке.

- ✅ Исправлено 03.10 (вечер): в compose добавлен комментарий, что Dockerfile не даётся (artisan на хосте) и что phpredis требует ext-redis.
