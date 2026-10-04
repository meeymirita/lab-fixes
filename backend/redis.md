# Redis Lab — итоги вычитки и проверки

**Вычитка:** ✅ пройдено 24.09; найдено 7 (тех 2, противоречий 4, текст 1); все внесены в методичку.  
**Проверка запуском и в браузере:** см. разделы «🧪» ниже и таблицу `fixes/common/_verification.md` (там же уровень проверки и что не проверялось).

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
