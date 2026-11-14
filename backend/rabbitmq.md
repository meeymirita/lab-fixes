# RabbitMQ Lab — итоги вычитки и проверки

**Вычитка:** ✅ пройдено 26.09; найдено 6 (тех 3, противоречий 3, текст 0); все внесены в методичку.  
**Проверка запуском и в браузере:** см. разделы «🧪» ниже и таблицу `fixes/common/_verification.md` (там же уровень проверки и что не проверялось).

## Находки чтения методички (23–26.09 и 04.10) — дайджест
Полные формулировки не хранятся: каждая находка исправлена в методичке. Здесь — суть, чтобы понимать, какие классы ошибок встречались.

- **[противоречие] Раздел 11, преамбула глоссария** — «В порядке первого появления в тексте.» → фактический порядок появления сносок в HTML (по `id="ref-N"`) — 1,2,…,16,17,**21,20**,18,19 — не совпадает с заявленным и с порядко…
- **[тех] Шаг 1.2, «🔬 Под капотом: … classic vs quorum»** — «(б) quorum-очереди поддерживают приоритеты ограниченно» → проверено вживую (`rabbitmq:4-management`, тот же образ, что в лабе): `PUT /api/queues/%2f/qtest` с `{"x-que…
- **[тех] Шаг 4.2, «Под капотом: как выбрать prefetch...»** — «Лечится маленьким prefetch или (в RabbitMQ 3.8+) consumer priority» → Consumer Priorities — фича RabbitMQ 3.2 (введена в 2013, см. официальный блог RabbitMQ «Using…
- **[противоречие] Шаг 4.3 и Шаг 5.1** — команды `LAB_CRASH_BEFORE_ACK=true docker compose up -d --force-recreate order-worker` и `LAB_SIMULATE_SMTP_FAILURE=true docker compose up -d --force-recreate email-worker` → на практике…
- **[тех] Шаг 5.2** — «TTL retry.3 можно уменьшить в definitions.json (docker compose down -v && up — определения перечитаются)» → флаг `-v` без необходимости удаляет именованный volume `pgdata` (все products/orders/outbox_mess…
- **[противоречие] Раздел 4, таблица стека, строка «БД»** — «PostgreSQL 16 → orders, outbox, processed_messages, order_events» → таблица называет таблицу аутбокса «outbox», а везде далее в этой же части (раздел 5: «INSERT INTO…

## 🧪 Проверка при переводе на PostgreSQL 18 — 03.10.2026
Лаба пройдена и заморожена, но по решению «PostgreSQL 18 везде» `docker-compose.yml` и методичка переведены с `postgres:16`: том монтируется в `/var/lib/postgresql`. Проверено на копии: `postgres` и `rabbitmq` становятся `healthy`, образ приложения собирается, `composer install` и `php artisan migrate` проходят на PostgreSQL 18.6 (все миграции лабы).

**Важно для тех, у кого уже есть локальный том `pgdata` от PostgreSQL 16:** образ 18 не откроет каталог данных 16 («database files are incompatible») — нужен `docker compose down -v` (данные лабы потеряются; лаба учебная, схема пересоздаётся миграциями).

## 🧪 Сессии 7–10 — 14–15.11.2026 (RabbitMQ 4.4.0, `rabbitmq:4-management`, php-amqplib, Docker)
Проверка на живом брокере: отдельные контейнеры и копия compose лабы (`rabbitmq`, `rabbitmq2`, `rabbitmq3`), публикация и потребление — PHP-скриптами на php-amqplib (код приложения лабы не поднимался).
- **7.1 — [исправлено]:** при `overflow: reject-publish` очередь останавливается на 5000, издатель с publisher confirms получает `basic.nack` (из 6000 — 5000 подтверждений и 1000 nack), без confirms сообщения молча теряются; `406 PRECONDITION_FAILED` тут нет. Утверждение «явный аргумент очереди побеждает политику» неточно для `max-length`: действует меньшее значение (аргумент 10 + политика 5000 → 10; аргумент 9000 + политика 5000 → 5000).
- **7.2:** SAC подтверждён: `list_consumers` показывает `active = true` у одного, при удалении активного второй становится активным и получает новые сообщения.
- **7.3:** подтверждено: политика с большим `priority` побеждает целиком, `--priority 20` чинит. Команда удаления политики — `clear_policy` (не `delete_policy`).
- **8.1 — [исправлено]:** с `x-delivery-limit: 5` сообщение доставляется 6 раз (первая + 5 повторных) и затем УДАЛЯЕТСЯ — с DLX уходит в него (at-least-once + reject-publish), без DLX пропадает. `x-max-priority` в quorum-очереди: `PRECONDITION_FAILED - invalid arg 'x-max-priority'` (подтверждено). (При `basic.nack` с requeue из моего скрипта лимит не срабатывал — чтение причины не доведено; при `basic.reject` с requeue срабатывает.)
- **8.2 — [исправлено, главное]:** `join_cluster rabbit@rabbitmq` падал (`noconnection`), потому что у сервиса `rabbitmq` нет `hostname` — узел называется `rabbit@<id контейнера>`; добавлен `hostname: rabbitmq`. Утверждение «email.dlq переизбирает лидера на rabbitmq2 за секунды» неверно: реплик у очереди одна (создана до вступления второго узла), после `stop rabbitmq` очередь недоступна; после `rabbitmq-queues grow … all` реплик две, но кворуму из двух нужны обе — остановка лидера снова делает её недоступной. Переизбрание проверено только на трёх узлах (лидер перешёл на `rabbit@rabbitmq3`). Запись cookie командой из шага (`exec` от root, `chmod 400`) работает — владелец файла остаётся `rabbitmq`. Брокер на Docker Desktop иногда сразу падает с `eacces` на `.erlang.cookie` — помогает повторный запуск.
- **8.3:** достаточно остановить любой из двух узлов, чтобы очередь пропала из `list_queues`; добавлено.
- **9.1 / 9.2 / 9.3 — [исправлено]:** на обычном `/metrics` метрики суммарные и без метки `queue` (`rabbitmq_queue_messages_ready 4`); по очередям — `/metrics/per-object` (или `/metrics/detailed?family=queue_coarse_metrics` с именами `rabbitmq_detailed_queue_*`). Правило `rabbitmq_queue_messages_ready{queue="analytics.queue"}` работает только при `metrics_path: /metrics/per-object` в `prometheus.yml`; добавлено. Плагин `rabbitmq_prometheus` в образе уже включён.
- **10.1 — [исправлено]:** паттерны прав не имеют неявных якорей (`analytics` без `^…$` разрешил чтение `analytics.queue`); с шагом `^analytics\.` всё работает как описано (чтение `analytics.queue` и consume с passive declare — да, `order.queue` и публикация — `ACCESS_REFUSED`, тег `monitoring` пускает в API). vhost `reporting` создаётся, но права выдаются на `/` — отмечено в тексте.
- **10.2:** TLS-слушатель на 5671 (`listeners.ssl.default`, `verify_none`), `openssl s_client`: `CONNECTION ESTABLISHED`, TLSv1.3, `verify error:num=18:self-signed certificate`; в тексте дополнено.
- **Не проверено:** шаги 2.3–2.4 (новые в главе 2), 9.2 (запуск Prometheus и срабатывание алерта — образ не скачивался), 9.3 и 10.3 (задания без подсказок), итоговое ТЗ 11.1 (не решается); работа лабораторных воркеров на TLS.

