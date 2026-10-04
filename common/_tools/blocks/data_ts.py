# -*- coding: utf-8 -*-
DEEP = {
'1.1': ('как пакеты workspaces видят друг друга',
 'Когда в корневом `package.json` объявлены `workspaces`, `npm install` не копирует пакеты друг в друга, а создаёт в `node_modules` символические ссылки: `node_modules/@warehouse/core` указывает на папку `packages/core`. Поэтому `import … from \'@warehouse/core\'` в соседнем пакете работает без публикации в npm, а правка в `core` сразу видна всем.\n\n'
 'Из этого следует и ограничение: пока в `core` нет скомпилированных файлов, импорт по имени пакета зависит от того, откуда берёт код `tsx`, `vitest` или `esbuild`. В лабе это решено тем, что все они читают исходники `.ts` напрямую.'),
'1.2': ('почему let string, а const — литерал (widening)',
 'Когда вы пишете `const unit = \'pcs\'`, TypeScript выводит тип литерала `\'pcs\'`: константа не изменится. А `let unit = \'pcs\'` получит тип `string`, потому что значение можно переписать на любое другое. Это называют расширением типа (widening).\n\n'
 'Из-за этого свойства объекта `{ unit: \'pcs\' }` имеют тип `string`, а не `\'pcs\'`: объект изменяем. Чтобы сохранить литерал, используют `as const` или явную аннотацию. Это та самая причина, по которой в шаге 1.3 литеральные типы нужно закреплять намеренно.'),
'1.3': ('чем type отличается от interface',
 'Для описания формы объекта подходят оба, и в большинстве случаев разницы нет. Но она есть. `interface` можно расширять через `extends` и «дописывать» повторным объявлением с тем же именем (declaration merging). `type` умеет больше по видам: объединения (`A | B`), кортежи, примитивы-псевдонимы и вычисляемые типы, но повторно объявить его нельзя.\n\n'
 'Практическое правило: публичные контракты объектов, которые могут расширяться (например, типы библиотеки), — `interface`; всё, что строится из других типов (объединения, условные и mapped-типы), — `type`. В лабе это встретится в обоих видах.'),
'1.4': ('почему колбэк с void может возвращать значение',
 'Тип функции `() => void` не означает «функция ничего не возвращает». Он означает «возвращаемое значение будет проигнорировано». Поэтому в массив-колбэк для `forEach` можно передать функцию, которая что-то возвращает: ошибки не будет.\n\n'
 'Это сделано намеренно: иначе нельзя было бы передать в `forEach` стрелку вида `x => list.push(x)`, которая возвращает число. Для самой функции, объявленной с `: void`, правила строже: она не должна возвращать значение. Различие стоит запомнить, когда будете читать сигнатуры колбэков.'),
'1.5': ('чем readonly отличается от as const',
 '`readonly` запрещает изменять массив или свойство, но действует поверхностно: `Readonly<Item>` не даёт переписать поле `name`, но объект, лежащий внутри поля, остаётся изменяемым. Тип `readonly Item[]` убирает методы вроде `push`.\n\n'
 '`as const` работает глубже: он превращает литерал в максимально узкий и неизменяемый тип целиком, включая вложенные массивы и объекты (кортеж остаётся кортежем, строки — литералами). Поэтому для списков допустимых значений используют именно его, а для защиты аргумента функции от случайной правки — `readonly`.'),
'2.4': ('чем отличается type guard от assertion function',
 'Type guard — функция с возвращаемым типом `x is Movement`. Она возвращает `true` или `false`, и в ветке `if` TypeScript считает значение уточнённым. Сама проверка ничего не бросает: что делать при `false`, решает вызывающий код.\n\n'
 'Assertion function имеет сигнатуру `asserts x is Movement`: она либо возвращает управление (тогда после вызова тип уже уточнён), либо бросает ошибку. Это удобно на границе: одна строка `assertMovement(data)`, и дальше значение имеет доверенный тип. Выбор простой: нужна ветка — guard, нужно «упасть, если неверно» — assertion.'),
'4.3': ('что делает skipLibCheck и когда он вредит',
 'Параметр `skipLibCheck: true` отключает проверку типов во всех файлах `.d.ts`: и в библиотеках из `node_modules`, и в ваших собственных. Это ускоряет компиляцию и избавляет от чужих ошибок и конфликтов версий, поэтому его включают почти везде.\n\n'
 'Цена — ваши собственные декларации тоже не проверяются. Ошибка в `table.d.ts` (опечатка в типе, несовместимость с другой декларацией) останется незамеченной, пока не проявится в местах использования. Поэтому декларации стоит проверять отдельно или хотя бы через использование в коде и тесты на типы.'),
'4.4': ('что такое isolatedModules и зачем он esbuild',
 'esbuild обрабатывает каждый файл отдельно, не видя остальных, и не знает типов. Режим `isolatedModules` просит компилятор сразу ловить конструкции, которые так обработать нельзя. Например, реэкспорт типа без слова `type` (`export { Movement }`) — esbuild не может понять, тип это или значение, и оставит лишнее. Поэтому пишут `export type { Movement }`.\n\n'
 'То же касается `const enum` из другого файла и файла без импортов и экспортов. Поэтому в проекте с esbuild, tsx или Vite этот режим включают: он делает проверку `tsc` строже, но гарантирует, что сборка поведёт себя так же, как вы ожидаете.'),
'5.1': ('как infer достаёт тип изнутри',
 'В условных типах слово `infer` объявляет «неизвестную часть», которую TypeScript выведет сам: `T extends Promise<infer U> ? U : T` читается как «если `T` — промис, верни то, что внутри, иначе `T`». Так работает и встроенный `Awaited`.\n\n'
 'В `ApiContract` тот же приём позволяет по строке маршрута получить тип ответа без дублирования. Условные типы к тому же распределяются: если подставить объединение, проверка выполняется для каждого его члена отдельно, и результат тоже объединение. Это поведение и использовано в `Debrand`.'),
}
WHY_EXTRA = {}
READ = {
'1.2': [('https://www.typescriptlang.org/docs/handbook/2/basic-types.html', 'TypeScript: The Basics', 'статическая проверка, вывод типов и ошибки компилятора.')],
'1.3': [('https://www.typescriptlang.org/docs/handbook/2/everyday-types.html', 'TypeScript: Everyday Types', 'union, литералы, type и interface.')],
'1.4': [('https://www.typescriptlang.org/docs/handbook/2/functions.html', 'TypeScript: More on Functions', 'колбэки, generics и void.')],
'1.5': [('https://www.typescriptlang.org/tsconfig/#strict', 'TSConfig: strict', 'какие проверки включает strict.')],
'2.1': [('https://www.typescriptlang.org/docs/handbook/2/narrowing.html', 'TypeScript: Narrowing', 'typeof, in и размеченные объединения.')],
'2.2': [('https://www.typescriptlang.org/docs/handbook/2/objects.html', 'TypeScript: Object Types', 'свойства, readonly и расширение.')],
'2.3': [('https://www.typescriptlang.org/docs/handbook/2/generics.html', 'TypeScript: Generics', 'параметры типа и ограничения.')],
'2.4': [('https://www.typescriptlang.org/docs/handbook/2/narrowing.html#using-type-predicates', 'TypeScript: Using type predicates', 'как писать свои type guards.')],
'3.1': [('https://www.typescriptlang.org/docs/handbook/2/generics.html', 'TypeScript: Generics', 'generic-классы и интерфейсы.')],
'3.2': [('https://www.typescriptlang.org/docs/handbook/utility-types.html', 'TypeScript: Utility Types', 'Partial, Pick, Omit, Record и другие.')],
'3.3': [('https://www.typescriptlang.org/docs/handbook/2/mapped-types.html', 'TypeScript: Mapped Types', 'как создавать типы на основе других.')],
'3.4': [('https://www.typescriptlang.org/docs/handbook/2/conditional-types.html', 'TypeScript: Conditional Types', 'extends, infer и распределение.')],
'4.1': [('https://nodejs.org/api/util.html#utilparseargsconfig', 'Node.js: util.parseArgs', 'разбор аргументов командной строки.'),
        ('https://zod.dev/', 'Zod', 'схемы, parse и вывод типов.')],
'4.2': [('https://zod.dev/api', 'Zod: API', 'z.object, z.enum, parse и safeParse.')],
'4.3': [('https://www.typescriptlang.org/docs/handbook/declaration-files/introduction.html', 'TypeScript: Declaration Files', 'как устроены .d.ts.')],
'4.4': [('https://esbuild.github.io/api/', 'esbuild: API', 'build, define и platform.')],
'5.1': [('https://www.typescriptlang.org/docs/handbook/2/indexed-access-types.html', 'TypeScript: Indexed Access Types', 'T[K] и доступ к типам по ключу.')],
'5.2': [('https://vuejs.org/guide/typescript/overview.html', 'Vue: Using Vue with TypeScript', 'vue-tsc и типизация компонентов.')],
'5.3': [('https://vitest.dev/guide/testing-types.html', 'Vitest: Testing Types', 'expectTypeOf и проверка типов.')],
}
