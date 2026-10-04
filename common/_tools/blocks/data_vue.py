# -*- coding: utf-8 -*-
DEEP = {
'1.1': ('как Vite проксирует запросы и WebSocket',
 'Dev-сервер Vite умеет пересылать часть запросов на другой адрес: в `vite.config.js` это раздел `server.proxy`. Правило для `/api` отправляет такие запросы в контейнер `api`, а для `/socket.io` включается режим `ws: true`, чтобы проксировались и WebSocket-соединения, а не только обычные запросы.\n\n'
 'Для браузера всё выглядит как обращение к собственному origin, поэтому нет ни CORS, ни настройки адреса бэкенда в коде. Работает прокси только в режиме `dev`: в проде его роль берёт на себя nginx, и в шаге 5.4 вы настроите её руками.'),
'1.3': ('почему у ref есть .value, а у reactive нет',
 'Vue отслеживает чтение и запись свойств через `Proxy`: при чтении поля он запоминает, кто его прочитал, при записи — уведомляет читателей. `reactive({ … })` оборачивает объект целиком, поэтому с его полями работают как обычно.\n\n'
 'Примитив — число или строку — Proxy обернуть не может, поэтому `ref(0)` хранит значение в объекте с геттером и сеттером `.value`. Это и есть причина записи с `.value` в скрипте: через неё Vue перехватывает доступ. В шаблоне `.value` не пишут, потому что Vue разворачивает ref автоматически.'),
'1.4': ('что произойдёт с v-if и v-for на одном элементе',
 'В Vue 3 у `v-if` приоритет выше, чем у `v-for`: условие вычисляется раньше цикла и не может использовать переменную цикла. Запись `<li v-for="t in tickets" v-if="t.open">` поэтому не работает так, как ждёшь (в Vue 2 было наоборот).\n\n'
 'Правильный способ — отфильтровать список заранее в `computed` (как `visible` в шаге) и проходить по нему, либо поставить `v-if` на обёртку `<template v-for>`. Отдельно запомните разницу `v-if` и `v-show`: первый создаёт и удаляет элемент, второй лишь переключает `display`.'),
'2.4': ('почему хуки жизненного цикла нужно регистрировать синхронно',
 'Функции `onMounted` и `onUnmounted` привязываются к «текущему компоненту», который Vue знает только во время выполнения `setup`. Поэтому их нужно вызывать синхронно, до первого `await`: после него «текущего» компонента уже нет, и хук не зарегистрируется (Vue предупредит в консоли).\n\n'
 'Это же правило касается composable: он должен вызываться прямо из `setup`, а не из колбэка или после ожидания. Если composable вызвать вне `setup`, его хуки привяжутся к никому, и таймер из `useNow` не остановится вместе с компонентом.'),
'3.4': ('чем setup-store отличается от options-store',
 'В Pinia состояние можно описать двумя способами. «Options-синтаксис» разделяет `state`, `getters` и `actions` на отдельные секции. «Setup-синтаксис», как в `useUiStore`, — это обычная функция, где `ref` становится состоянием, `computed` — геттером, а функции — действиями.\n\n'
 'Второй способ ближе к Composition API и позволяет использовать composable внутри стора. Но у него есть правило: всё, что должно быть частью состояния или действий, нужно вернуть из функции, иначе Pinia (и devtools) это не увидят.'),
'4.4': ('push или replace: что добавлять в историю',
 '`router.push` добавляет запись в историю браузера, а `router.replace` заменяет текущую. Для фильтров, которые меняются при каждом нажатии клавиши, используют `replace`: иначе кнопка «Назад» превратилась бы в пролистывание всех промежуточных запросов поиска.\n\n'
 'Правило простое: если новое состояние — это «другая страница» с точки зрения пользователя, используйте `push`; если это уточнение текущей, то `replace`. Именно поэтому в `useRouteQuery` стоит `replace`, а при переходе на страницу тикета — обычная навигация.'),
'5.3': ('почему vi.mock поднимается наверх файла',
 'Вызов `vi.mock(\'../api\')` Vitest при сборке переносит в начало файла, до всех `import`. Иначе модуль успел бы загрузиться настоящим, и подмена не сработала бы. Поэтому внутри `vi.mock` нельзя использовать переменные, объявленные ниже, — они ещё не существуют; для этого есть `vi.hoisted`.\n\n'
 'Для таймеров есть пара `vi.useFakeTimers()` и `vi.advanceTimersByTime(ms)`: время «перематывается» мгновенно, и тест `useNow` не ждёт реальные 30 секунд. Не забывайте возвращать настоящие таймеры в `afterEach`, иначе соседние тесты ведут себя странно.'),
'5.4': ('что такое tree-shaking и code splitting',
 'При сборке Vite (на Rollup) выбрасывает неиспользуемый код: если вы импортируете из библиотеки одну функцию, остальные в бандл не попадают. Это возможно потому, что ES-модули статичны: связи между файлами известны до запуска. Такой приём называют tree-shaking.\n\n'
 'Code splitting — другое: динамический `import()` в маршрутах (`() => import(\'./BoardView.vue\')`) превращается в отдельный чанк, и страница загружается только при переходе на неё. Имена файлов получают хеш, поэтому браузер кеширует их надолго, а новая сборка не конфликтует со старой.'),
}
WHY_EXTRA = {}
READ = {
'1.2': [('https://vite.dev/config/server-options#server-proxy', 'Vite: server.proxy', 'как настраивается прокси для /api и WebSocket.')],
'1.3': [('https://vuejs.org/guide/essentials/reactivity-fundamentals.html', 'Vue: Reactivity Fundamentals', 'ref, reactive и как они устроены.')],
'1.4': [('https://vuejs.org/guide/essentials/list.html', 'Vue: List Rendering', 'v-for, key и приоритет с v-if.')],
'2.1': [('https://vuejs.org/guide/components/props.html', 'Vue: Props', 'объявление и проверка props.')],
'2.2': [('https://vuejs.org/guide/components/v-model.html', 'Vue: Component v-model', 'defineModel и двусторонняя привязка.')],
'2.3': [('https://vuejs.org/guide/components/slots.html', 'Vue: Slots', 'слоты, scoped slots и значения по умолчанию.')],
'2.4': [('https://vuejs.org/guide/essentials/lifecycle.html', 'Vue: Lifecycle Hooks', 'порядок хуков и когда они вызываются.')],
'3.1': [('https://pinia.vuejs.org/core-concepts/', 'Pinia: Defining a Store', 'setup- и options-синтаксис.')],
'3.2': [('https://pinia.vuejs.org/core-concepts/getters.html', 'Pinia: Getters', 'вычисляемые значения стора.')],
'3.3': [('https://pinia.vuejs.org/core-concepts/actions.html', 'Pinia: Actions', 'асинхронные действия и обработка ошибок.')],
'3.4': [('https://vuejs.org/guide/components/provide-inject.html', 'Vue: Provide / Inject', 'когда подходит provide, а когда стор.')],
'4.1': [('https://router.vuejs.org/guide/', 'Vue Router: Getting Started', 'маршруты, ссылки и навигация.')],
'4.2': [('https://router.vuejs.org/guide/advanced/navigation-guards.html', 'Vue Router: Navigation Guards', 'beforeEach, meta и редиректы.')],
'4.3': [('https://router.vuejs.org/guide/essentials/nested-routes.html', 'Vue Router: Nested Routes', 'дочерние маршруты и router-view.')],
'4.4': [('https://router.vuejs.org/guide/essentials/navigation.html', 'Vue Router: Programmatic Navigation', 'push, replace и query.')],
'5.1': [('https://socket.io/docs/v4/client-api/', 'Socket.IO: Client API', 'подключение, события и отключение.')],
'5.2': [('https://vuejs.org/guide/built-ins/transition-group.html', 'Vue: TransitionGroup', 'анимация списков.')],
'5.3': [('https://vitest.dev/guide/', 'Vitest: Getting Started', 'тесты, моки и таймеры.')],
'5.4': [('https://vite.dev/guide/build.html', 'Vite: Building for Production', 'как устроена сборка и разделение кода.')],
}
