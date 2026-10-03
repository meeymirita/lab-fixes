# Inertia Lab — находки

> **Вычитка методички ещё не проводилась** (статус в `common/_proofread.md` — ⬜ не начато). Ниже — только результаты сухого прогона стенда сессии 1, сделанного 03.10.2026 при обновлении версий.

## 🧪 Сухой прогон шагов 1.1–1.3 — 03.10.2026 (Laravel 13.17, Inertia 3.8, Vue 3.5, Vite 7, TypeScript 6.0, Node 24)

Версия Inertia 3 актуальна: релиз 26.03.2026, требует PHP 8.2+ и Laravel 11+, `@inertiajs/vite` поддерживает Vite 7 и 8 (документация inertiajs.com/docs/v3). Серверная часть по методичке (`inertia-laravel:^3.0`, `inertia:middleware`, корневой шаблон с `<x-inertia::head />` и `<x-inertia::app />`) работает. Клиентская часть: `createInertiaApp({ pages: './Pages', withApp })` с Pinia собирается и открывается в браузере: первый визит — полный HTML с объектом страницы, клик по `<Link>` — XHR с заголовком `X-Inertia: true`, без перезагрузки.

- **[тех] Шаг 1.3: `npm install -D @vitejs/plugin-vue typescript vue-tsc` ставит TypeScript 7.0.2**, и `npm run typecheck` падает: `vue-tsc` не умеет работать с TS 7 (`ERR_PACKAGE_PATH_NOT_EXPORTED` при поиске `tsc`). → `typescript@~6.0`. ✅
- **[тех] Шаг 1.3: `tsconfig.json` с `"baseUrl": "."` на TypeScript 6 даёт `TS5101: Option 'baseUrl' is deprecated and will stop functioning in TypeScript 7.0`.** → `baseUrl` убран, `paths` записан относительно файла: `"@/*": ["./resources/js/*"]` (без `./` — `TS5090`). ✅
- **[тех] Скелет Laravel 13 приносит Vite 8 и `laravel-vite-plugin` 3.x, который требует именно Vite ^8** (с Vite 7 npm пишет `invalid`). По решению «Vite 7 везде» добавлено `npm install -D vite@^7 laravel-vite-plugin@^2`; `vite build` и `typecheck` проходят, страницы работают. ✅
- **[текст]** `php artisan install:api` и прочие сообщения скелета не затронуты; `composer run dev` не проверялся (запускает несколько процессов).
- **Не прогонялось:** сессии 2–8 (модель данных, лента, формы, Wayfinder, SSR, роли и политики) — только стенд сессии 1.
