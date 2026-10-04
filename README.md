# lab-fixes — вычитка и проверка лаб

## Папки

| Папка | Что внутри |
|---|---|
| `backend/` | php-coffee (ООП), php, algorithms-php, postgresql, redis, rabbitmq, laravel, laravel-performance, inertia, nestjs, graphql |
| `devops/` | docker, traefik, kubernetes |
| `frontend/` | js, vue, typescript, nuxt, angular, css, tailwind |
| `common/` | общее: порядок лаб, статус вычитки и процесс, учёт проверок, версии и сайт, скрипты |

## Файлы

| Файл | Что значит |
|---|---|
| `<направление>/<лаба>.md` | итоги по одной лабе: статус вычитки, дайджест находок (всё исправлено в методичке), решения, все записи о проверке запуском («🧪», с датами и версиями) |
| `common/_verification.md` | что чем проверено (Docker / браузер / текст), пошаговые таблицы, сноски «*» (аккаунт, домен, ключи, «Production Hell»). Парный файл — `works/verification.html` (`tools/build-verification.py`) |
| `common/_proofread.md` | таблица статуса вычитки + как вычитывать и проверять новую лабу |
| `common/_order.md` | порядок прохождения, зависимости, стыки между лабами |
| `common/site.md` | единые версии, сайт и инструменты, известные особенности, открытые идеи |
| `common/_tools/prep.py`, `bundle.py` | нарезка методички для чтения; чтение и правка методичек (`jsub`) |

> В файлах лаб версии и числа даны на момент записи (например, `postgres:17` в старых прогонах). Актуальные версии — `common/site.md`.
