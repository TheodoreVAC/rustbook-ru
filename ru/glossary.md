# Глоссарий русского издания RustBook

Единый словарь терминов, используемый во всех главах русского издания.
Термины, встречающиеся в оригинальном английском издании, приведены слева,
русский эквивалент — справа.

**Общие правила**

* Имена API, типов, методов, функций, переменных, ключевых слов и любых
  идентификаторов Rust **не переводятся** и всегда остаются на латинице.
  Например: `Vec`, `push()`, `into_iter()`, `usize`, `Self`, `Cargo`, `rustc`.
* Термины, устоявшиеся в русской технической литературе, переводятся
  стандартным образом (см. таблицы ниже).
* Названия алгоритмов и структур данных переводятся, если перевод является
  общепринятым; в скобках приводится оригинальное название.
* Аббревиатуры (ADT, LIFO, BFS, DFS, DSL) сохраняются как есть.

---

## 1. Язык Rust: базовые понятия

| English | Русский |
|---|---|
| Rust | Rust |
| ownership | владение |
| ownership system | система владения |
| borrowing | заимствование |
| borrow checker | проверяющий заимствования |
| mutable reference | изменяемая ссылка |
| immutable reference | неизменяемая ссылка |
| lifetime | время жизни |
| lifetime elision | исключение времени жизни |
| trait | трейт |
| struct | структура |
| enum | перечисление |
| pattern matching | сопоставление с образцом |
| union | объединение |
| type alias | псевдоним типа |
| generic | обобщённый тип / дженерик |
| generics | обобщённые типы |
| monomorphization | мономорфизация |
| closure | замыкание |
| higher-order function | функция высшего порядка |
| iterator | итератор |
| iterator adaptor | адаптер итератора |
| smart pointer | умный указатель |
| raw pointer | необработанный указатель |
| reference | ссылка |
| dereference | разыменование |
| macro | макрос |
| declarative macro | декларативный макрос |
| procedural macro | процедурный макрос |
| attribute | атрибут |
| module | модуль |
| crate | крейт |
| library | библиотека |
| package | пакет |
| workspace | рабочее пространство |
| compiler | компилятор |
| compiler error | ошибка компиляции |
| linker | компоновщик |
| overflow | переполнение |
| underflow | потеря точности при вычитании |
| panic | паника |
| unwrap | `unwrap` (без перевода) |
| exception | исключение |
| error handling | обработка ошибок |
| Result | `Result` (без перевода) |
| Option | `Option` (без перевода) |
| unsafe code | небезопасный код |
| unsafe block | небезопасный блок |
| type system | система типов |
| memory safety | безопасность памяти |
| data race | гонка данных |
| concurrency | конкурентность |
| thread | поток |
| thread safety | потокобезопасность |
| synchronization | синхронизация |
| mutex | мьютекс |
| lock | блокировка |
| channel | канал |
| message passing | передача сообщений |
| interior mutability | внутренняя изменяемость |
| reference counting | подсчёт ссылок |
| copy trait | трейт `Copy` |
| clone | клонирование |
| move semantics | семантика перемещения |
| shadowing | затенение |
| scoping / scope | область видимости |
| shadow | затенённая переменная |
| mutability | изменяемость |
| mut | изменяемый |
| visibility | видимость |
| public / private | публичный / приватный |
| constant | константа |
| static | статический |
| literal | литерал |
| integer / float | целое число / число с плавающей точкой |
| boolean | логический тип |
| char | символ |
| string / `String` | строка / `String` |
| string slice / `&str` | срез строки / `&str` |
| byte string | байтовая строка |
| array | массив |
| slice | срез |
| tuple | кортеж |
| vector / `Vec` | вектор / `Vec` |
| collection | коллекция |
| container | контейнер |
| capacity | ёмкость |
| push / pop | `push` / `pop` |
| append | добавление в конец |
| insert | вставка |
| remove | удаление |
| retain | `retain` (без перевода) |
| clear | очистка |
| drain | извлечение с удалением |
| split_off | разделение |
| sort | сортировка |
| reverse | разворот |
| extend | расширение |
| iter / iter_mut / into_iter | `iter` / `iter_mut` / `into_iter` |
| borrow checker error | ошибка проверяющего заимствования |
| deref coercion | приведение через `Deref` |
| `?` operator | оператор `?` |
| `Result` combinator | комбинатор `Result` |
| builder | билдер |
| builder pattern | паттерн «билдер» |
| singleton | одиночка (синглтон) |
| dependency | зависимость |
| crate registry | реестр крейтов |
| Cargo.toml | `Cargo.toml` |
| Cargo.lock | `Cargo.lock` |
| rustup | `rustup` |
| rustc | `rustc` |
| rustdoc | `rustdoc` |
| rustfmt | `rustfmt` |
| nightly | nightly |
| stable | stable |
| beta | beta |
| toolchain | инструментарий / toolchain |

## 2. Структуры данных и алгоритмы

| English | Русский |
|---|---|
| data structure | структура данных |
| abstract data type (ADT) | абстрактный тип данных (ADT) |
| stack | стек |
| queue | очередь |
| deque | дек |
| double-ended queue | двусторонняя очередь |
| linked list | связный список |
| singly linked list | односвязный список |
| doubly linked list | двусвязный список |
| vector | вектор |
| list | список |
| hash table | хеш-таблица |
| hash map | хеш-карта |
| hash function | хеш-функция |
| hash collision | коллизия хешей |
| collision resolution | разрешение коллизий |
| chaining method | метод цепочек |
| open addressing | открытая адресация |
| binary search tree (BST) | двоичное дерево поиска (BST) |
| binary tree | двоичное дерево |
| balanced binary tree | сбалансированное двоичное дерево |
| AVL tree | дерево AVL |
| red-black tree | красно-чёрное дерево |
| B-tree | B-дерево |
| binary heap | двоичная куча |
| min-heap / max-heap | куча на минимум / куча на максимум |
| tree | дерево |
| root | корень |
| leaf node | листовой узел |
| parent node | родительский узел |
| child node | дочерний узел |
| sibling node | соседний узел |
| depth | глубина |
| height | высота |
| level | уровень |
| subtree | поддерево |
| traversal | обход |
| pre-order traversal | обход в прямом порядке (pre-order) |
| in-order traversal | обход в симметричном порядке (in-order) |
| post-order traversal | обход в обратном порядке (post-order) |
| level-order traversal | обход по уровням |
| parse tree | дерево разбора |
| mirror order | зеркальный порядок |
| rotation | поворот |
| graph | граф |
| vertex / node | вершина / узел |
| edge | ребро |
| directed graph | ориентированный граф |
| undirected graph | неориентированный граф |
| adjacency matrix | матрица смежности |
| adjacency list | список смежности |
| edge weight | вес ребра |
| cycle | цикл |
| DAG | DAG (направленный ациклический граф) |
| topological sort | топологическая сортировка |
| strongly connected component | компонента сильной связности |
| shortest path | кратчайший путь |
| breadth-first search (BFS) | поиск в ширину (BFS) |
| depth-first search (DFS) | поиск в глубину (DFS) |
| connected component | компонента связности |
| in-degree / out-degree | входящая / исходящая степень |
| adjacency | смежность |
| knight's tour | маршрут коня |
| word ladder | цепочка слов |
| recursive | рекурсивный |
| recursion | рекурсия |
| base case | базовый случай |
| tail recursion | хвостовая рекурсия |
| tail call | хвостовой вызов |
| iteration | итерация |
| divide and conquer | «разделяй и властвуй» |
| dynamic programming | динамическое программирование |
| memoization | мемоизация |
| greedy algorithm | жадный алгоритм |
| backtracking | обратный поиск с откатами |
| brute force | полный перебор (brute force) |
| big-O notation | нотация O (big-O) |
| time complexity | временная сложность |
| space complexity | пространственная сложность |
| complexity | сложность |
| best case | лучший случай |
| worst case | худший случай |
| average case | средний случай |
| linear | линейная |
| logarithmic | логарифмическая |
| quadratic | квадратичная |
| cubic | кубическая |
| exponential | экспоненциальная |
| constant | постоянная |
| bubble sort | пузырьковая сортировка |
| quick sort | быстрая сортировка |
| insertion sort | сортировка вставками |
| shell sort | сортировка Шелла |
| merge sort | сортировка слиянием |
| selection sort | сортировка выбором |
| heap sort | сортировка кучей |
| bucket sort | сортировка корзинами (bucket sort) |
| counting sort | сортировка подсчётом |
| radix sort | поразрядная сортировка |
| Tim sort | сортировка Тимсорт (TimSort) |
| cocktail sort | шейкерная сортировка (cocktail sort) |
| comb sort | гребёнчатая сортировка (comb sort) |
| binary insertion sort | двоичная сортировка вставками |
| binary search | двоичный поиск |
| sequential search | последовательный поиск |
| interpolation search | интерполяционный поиск |
| exponential search | экспоненциальный поиск |
| ordered sequential search | упорядоченный последовательный поиск |
| hash search | поиск по хешу |
| edit distance | расстояние редактирования |
| Hamming distance | расстояние Хэмминга |
| Levenshtein distance | расстояние Левенштейна |
| trie | бор (trie) |
| prefix tree | префиксное дерево |
| bloom filter | фильтр Блума |
| cuckoo filter | фильтр Кукушки |
| LRU cache | кеш LRU (наименее недавно использованный) |
| consistent hashing | согласованное хеширование |
| base58 | base58 |
| blockchain | блокчейн |
| smart contract | смарт-контракт |
| proof of work | доказательство работы |
| nonce | nonce |
| ledger | реестр |
| entropy | энтропия |
| principle of locality | принцип локальности |
| LIFO | LIFO (последним пришёл — первым ушёл) |
| FIFO | FIFO (первым пришёл — первым ушёл) |
| infix expression | инфиксная запись |
| prefix expression | префиксная запись |
| postfix expression | постфиксная запись |
| operand | операнд |
| operator | оператор |
| parenthesis | скобка |
| palindrome | палиндром |
| anagram | анаграмма |
| Hanoi tower | Ханойская башня |

## 3. Общенаучные и вычислительные термины

| English | Русский |
|---|---|
| computer science | информатика |
| algorithm | алгоритм |
| algorithm analysis | анализ алгоритмов |
| pseudo-code | псевдокод |
| programming | программирование |
| program | программа |
| source code | исходный код |
| debug | отладка |
| debugger | отладчик |
| test / unit test | тест / модульный тест |
| documentation comment | комментарий документации |
| compiler error | ошибка компиляции |
| platform | платформа |
| operating system | операционная система |
| kernel | ядро |
| shell | оболочка |
| command line | командная строка |
| environment variable | переменная окружения |
| module | модуль |
| library | библиотека |
| framework | фреймворк |
| distributed system | распределённая система |
| cloud computing | облачные вычисления |
| internet of things | Интернет вещей |
| hardware / software | аппаратное / программное обеспечение |
| abstraction | абстракция |
| encapsulation | инкапсуляция |
| modularity | модульность |
| scalability | масштабируемость |
| efficiency | эффективность |
| performance | производительность |
| optimization | оптимизация |
| benchmark | тест производительности |
| prototype | прототип |
| design pattern | паттерн проектирования |
| trade-off | компромисс |
| use case | вариант использования |
| workflow | рабочий процесс |

## 4. Оформление перевода

* Обращения к читателю: «вы» (формальное) либо безличные конструкции.
  В оригинале используется безличный стиль — при переводе избегать
  разговорных форм («давай», «давайте посмотрим»).
* Термин «вы» в значении «существительное множественного числа»
  («очередь содержит элементы») пишется со строчной буквы: «очередь
  хранит элементы».
* Числа, адреса URL, команды и фрагменты кода не переводятся.
* Названия книг и статей, приведённые в тексте, сохраняются в оригинале;
  при необходимости добавляется пояснение в квадратных скобках.
* Библиографические ссылки вида `[1]`, `[2]` сохраняются как есть.
* Типографика: используются «ёлочки» (`«»`) для цитат, тире — `—`,
  неразрывный пробел после предлогов вроде «в», «к» не ставится.
