# Связность цепочки OOP → Чистый PHP → RabbitMQ → Redis → Laravel (бэкенд)

Порядок прохождения: OOP (2) → Чистый PHP (3) → RabbitMQ (6) → Redis (7) → Laravel/TaskFlow (13).
Проверка стыков: всё, что лаба использует, объяснено в ней или в предыдущих; ссылки «как в X-лабе» ведут на реальное содержание.
Теги: **[пробел]**, **[наследство]**, **[расхождение]**, **[дубль]** — как в `_chain_frontend.md` / `_chain_devops.md`.

## Стык OOP → Чистый PHP

- **[расхождение] README vs методичка «Чистый PHP»** — уже подробно разобрано в `fixes/php.md` (22 ссылки на Laravel-лабу как на пройденную вместо OOP-лабы) — не повторяю, решение там принято (вариант А).

### Что проверено и в порядке
- Чистый PHP не содержит ни одной ссылки на RabbitMQ (грep по `part_*.txt` — 0 совпадений) — корректно, RabbitMQ ещё не пройден на этом месте цепочки.
- Домен «кофейня» заявлен в README Чистого PHP («та же кофейня, что в OOP-лабе») — сам текст методички ссылок на OOP-лабу не содержит (это уже в `fixes/php.md`, пункт про правку в OOP вместо Laravel).

## Стык → RabbitMQ

- **[расхождение] OOP-лаба (2-я) ссылается на RabbitMQ-лабу (6-я) как на уже пройденную** — вступление: «Стек — как в RabbitMQ Lab: Laravel 13 (PHP 8.4), PostgreSQL, RabbitMQ с Management UI, Mailpit… Брокер появляется только в сессии 5 и делает ровно то, что вы уже умеете: один topic-exchange, две очереди» → по порядку (`_order.md`) OOP идёт 2-й, RabbitMQ — 6-й, то есть «то, что вы уже умеете» на момент прохождения OOP неверно — RabbitMQ ещё не пройден. Комментарий в коде: `// app/Infrastructure/Amqp/AmqpConnectionFactory.php — как в RabbitMQ Lab` (9. Задания, блок 92) — тоже отсылка вперёд как на известное. → исправить на будущее время: «то же самое вы увидите в RabbitMQ-лабе» / «связка похожа на то, что будет в RabbitMQ-лабе (пройдёте её позже)».
- **[расхождение] Раздел 13 «Что дальше» OOP-лабы, таблица** — строка «Outbox для EventPublisher … связь с лабой: **ваш** RabbitMQ Lab, раздел 5» — притяжательное «ваш» подразумевает, что RabbitMQ-лаба уже пройдена (как в Laravel-лабе, где это корректно — RabbitMQ 6-я, Laravel 13-я). Для OOP-лабы (2-я) это неверно. → заменить на «RabbitMQ Lab (будет позже в программе), раздел 5».
- **[расхождение] Там же — строка «Redis Lab — ваш следующий проект»** — по факту следующая лаба по порядку (`_order.md`) — Чистый PHP (3-я), затем RabbitMQ (6-я), и только потом Redis (7-я). «Следующий проект» после OOP — не Redis. → заменить на «дальше по программе» / убрать слово «следующий».
- **[расхождение] «OOP Lab — Worker Kit» и класс `RetryChainPolicy` — не существуют** — OOP-лаба трижды ссылается на «OOP Lab — Worker Kit» (раздел 6.3 crash-тест, раздел «Что дальше», Repository-раздел про `InMemoryOrderRepository`) и на `IdempotentProcessor` «из Worker Kit», а Laravel-лаба (сессия 7.3) пишет: «Сравните этот механизм retry с вашим `RetryChainPolicy` из RabbitMQ-лабы (Worker Kit)». Проверено: ни файла, ни класса `RetryChainPolicy`, ни сущности «Worker Kit» нет ни в реальном коде RabbitMQ-лабы (`rabbitmq/laravel-app/`), ни в самой методичке RabbitMQ (`grep -c "Worker Kit" RabbitMQ_Lab_Plan_v1_pro_max.html` → 0). Реальный retry в RabbitMQ-лабе — не класс, а inline-логика в `EmailWorkerCommand` с заголовком `x-retry-count` + каскад TTL-очередей `email.retry.1/2/3` → DLX. → либо убрать все упоминания «Worker Kit»/`RetryChainPolicy` как несуществующей сущности, либо (если это будущий контент) явно пометить «будет добавлено» и не выдавать за пройденный материал.

### Что проверено и в порядке
- Реальный код RabbitMQ-лабы (`app/Services/Amqp/AmqpConnectionFactory.php`, `AbstractAmqpWorker`) использует `config('rabbitmq.prefetch')`, `heartbeat: 30`, `ProcessedMessage`; OOP-лаба строит свою версию (`App\Infrastructure\Amqp`, `basic_qos(0, 1, false)` — захардкожен prefetch=1, без ProcessedMessage) — это **другой**, упрощённый учебный код, не заявленный как идентичный файл-в-файл, так что расхождение в реализации само по себе не ошибка (это отдельный репозиторий, README прямо говорит «ни от чего не зависит»).
- Версии в `docker-compose.yaml` OOP-лабы (`postgres:17`, `rabbitmq:4-management`) совпадают с RabbitMQ-лабой по RabbitMQ (`rabbitmq:4-management`) — см. раздел «Сквозное» про Postgres.
- Чистый PHP не ссылается на RabbitMQ — корректно (см. выше).

## Стык RabbitMQ → Redis

- **[расхождение] Одноимённое поле `orders.priority` в Redis-лабе не используется и не соответствует по типу RabbitMQ-лабе** — миграция Redis-лабы (шаг 1.4): `Schema::create('orders', …) $t->string('priority')->default('normal');` — но реальный механизм приоритета в лабе (шаг «Приоритет через ZSet», раздел 9.2) работает через отдельный ключ `orders:priority` (ZSET по времени создания), эта колонка нигде дальше по тексту не читается и не пишется. Для сравнения — в RabbitMQ-лабе `orders.priority` реально используется: `unsignedTinyInteger('priority')->default(0)` идёт в заголовок AMQP-сообщения для `x-max-priority`. Получается «унаследованное» по домену имя поля с другим типом и без реализации. → либо убрать колонку `priority` из миграции Redis-лабы (раз она не нужна для ZSET-подхода), либо явно объяснить в шаге 1.4, что колонка — просто «на будущее»/для параллели с RabbitMQ, и её не потребуется читать напрямую.

### Что проверено и в порядке
- Домен переиспользован на уровне концепции, не кода (как и написано в README «домен заказов переиспользуется» — само редис-README после правки в `fixes/redis.md` уже говорит «рекомендуется после RabbitMQ Lab»): `products(name, stock)`, `orders(user_id, status, …)`, `order_items(order_id, product_id, qty)` — структурно совпадают с RabbitMQ-лабой (`products`, `orders`, `order_items`), только `order_items.quantity` в RabbitMQ назван `qty` в Redis (косметика, не ломает понимание).
- `processed_messages` в Redis-лабе (`stream_id`, `consumer_group`) осознанно переименованы относительно RabbitMQ (`message_id`, `consumer`) — методичка сама это объясняет («с заменой поля идентификации сообщения») — не расхождение, а документированная адаптация.
- Outbox Pattern корректно упомянут как «в RabbitMQ-лабе было, здесь сознательно не сделано» — проверено, что в реальном коде RabbitMQ-лабы Outbox действительно есть (`OutboxMessage`, `OutboxWriter`, `OutboxRelayCommand`), раздел 5 методички RabbitMQ называется «Транзакционная публикация событий (Outbox Pattern)» — ссылка «ваш RabbitMQ_Lab_Plan.html, раздел 5» в Redis-лабе (раздел 15 «Что дальше», через таблицу) ведёт на правильный номер раздела.
- PostgreSQL: RabbitMQ-лаба (пройдена, код заморожен) — `postgres:16`; Redis-лаба (методичка и подразумеваемый docker-compose) — `postgres:17`. См. раздел «Сквозное».

## Стык → Laravel

- **[дубль/исправление аудита] `fixes/laravel.md` ошибочно утверждает «OOP-лаба — ни разу» не упоминается** — фактическая проверка (`grep -o "ООП-лаб[а-я]*"`) находит **11 упоминаний** «ООП-лабы» (кириллица) в методичке TaskFlow: раздел 1 (Manager = «ровно ваш match в AppServiceProvider из ООП-лабы»), раздел 3 (contextual binding = «тот же Strategy, что и в ООП-лабе», `extend` = «тот же Decorator из ООП-лабы»), раздел 6 (middleware = «тот же Decorator, что в ООП-лабе»), сессия 5.2 («как в ООП-лабе, но теперь с реальным сервисом»), сессия 9 («тот же принцип, что был в ООП-лабе и Vue-лабе», «что дальше» ссылается на «что дальше» в ООП-лабе). Расхождение в `fixes/laravel.md` объясняется тем, что там искали латиницу «OOP-лаба», а в тексте везде кириллица «ООП-лаба». → в `fixes/laravel.md` пункт 1 (README «ссылается на OOP-лабу») можно закрывать как уже выполненный, вариант Б («убрать „ссылается―» из README) не нужен — методичка действительно ссылается, просто нужно поправить формулировку самого README на «ссылается» (уже так и есть) без изменений методички.
- Все проверенные ссылки по содержанию совпадают с реальным кодом OOP-лабы (Strategy — `DiscountPolicy`/`PaymentMethod`, Decorator — `BeverageDecorator`/добавки, `match` в `AppServiceProvider` для `Notifier`) — контентно ссылки верные, только номер факта в аудите был неверный.
- **[расхождение] `RetryChainPolicy` (Worker Kit)** — см. раздел «Стык → RabbitMQ» выше; та же несуществующая сущность цитируется и в Laravel-лабе (сессия 7.3, «ПРОВЕРЬ СЕБЯ»).

### Что проверено и в порядке
- Домены не смешиваются: Laravel-лаба явно строит другой домен (TaskFlow) и нигде не выдаёт заказы кофейни/интернет-магазина за свой — корректно.
- RabbitMQ версии совпадают: `rabbitmq:4-management` в обеих лабах (RabbitMQ-лаба и Laravel-лаба).
- Подход к очередям осознанно противопоставлен, а не выдан за идентичный: RabbitMQ-лаба — свой `AbstractAmqpWorker` на php-amqplib; Laravel-лаба — `vladimir-yuldashev/laravel-queue-rabbitmq`, и текст сам объясняет разницу («драйвер даёт из коробки то, что вы писали руками») — не расхождение, а явное сравнение.
- Ссылка «ваш RabbitMQ_Lab_Plan.html, раздел 5» (Outbox) в разделе 9 «Что дальше» Laravel-лабы — номер раздела верный (проверено выше).
- PostgreSQL 17 в Laravel-лабе (README и `docker-compose`) согласован с Redis (17); RabbitMQ (16) — единственное исключение, см. ниже.

## Сквозное (версии и т.п.)

- **[расхождение] PostgreSQL: только RabbitMQ-лаба (уже пройдена, код заморожен) осталась на `postgres:16`; все остальные звенья цепочки — уже на `postgres:17`.** Проверено фактически по файлам, не только по README: `php-coffee/docker-compose.yaml` → `postgres:17` (и в самой методичке тот же образ), `rabbitmq/docker-compose.yml` → `postgres:16`, Redis-методичка (докер-compose в тексте) → `postgres:17`, Laravel-методичка (докер-compose в тексте) → `postgres:17`. Это точнее, чем формулировка «RabbitMQ и OOP ещё на 16» — OOP уже переведена на 17, отставание только у RabbitMQ. Трогать RabbitMQ не нужно (лаба пройдена, менять зафиксированный код нет смысла) — как и решено в `fixes/site.md`.
- RabbitMQ (брокер): везде `rabbitmq:4-management` — RabbitMQ-лаба, OOP-лаба, Laravel-лаба. Согласовано, расхождений нет.
- Laravel везде 13, PHP везде 8.4 — согласовано по всей цепочке (OOP, Чистый PHP, RabbitMQ, Redis, Laravel).
- Redis везде 7 (`redis:7-alpine`/`redis:7`) — согласовано между Redis-лабой и Laravel-лабой.

### Что проверено и в порядке
- Имена классов Outbox/ProcessedMessage не конфликтуют по сути между RabbitMQ и Redis (см. «Стык RabbitMQ → Redis») — расхождение только в поле `orders.priority`, уже отмечено выше.
- Docker Compose стиль (healthcheck, depends_on с condition: service_healthy, profiles) единообразен между OOP, RabbitMQ, Redis и Laravel методичками — расхождений в подходе не найдено.
