<!--
  Файл изменён по сравнению с оригиналом проекта QMHTMY/RustBook:
  текст переведён на русский язык. Лицензия: Apache License 2.0.
  Оригинал: https://github.com/QMHTMY/RustBook
-->
# Графы

## 9.1 Цели

- Понять понятие и формат хранения графов.
- Реализовать несколько структур данных графов на Rust.
- Изучить два важных алгоритма поиска по графам.
- Использовать графы для решения различных прикладных задач.

## 9.2 Что такое граф?

В предыдущей главе мы рассматривали двоичные деревья как структуру данных, в то время как эта глава посвящена графам — более обобщённой форме деревьев. Хотя деревья можно рассматривать как упрощённые графы или тщательно подобранные графы с определёнными ограничениями на отношения между их узлами, у графов таких ограничений нет. В то время как у деревьев есть корневой узел и направление сверху вниз, у графов нет ни того ни другого. В отличие от деревьев, графы могут содержать циклы. Они состоят из точек, рёбер и отношений точка—ребро, тогда как деревья состоят из узлов и связей. Рисунок выше иллюстрирует граф с множеством узлов и связей, демонстрируя вертикальные и горизонтальные отношения между различными элементами. Например, математический анализ и линейная алгебра не имеют прямой связи, но могут совместно порождать нейросети, образуя горизонтальные отношения. Производные, с другой стороны, способствуют построению математического анализа, который является частью математического анализа, и это образует вертикальные отношения.

Графы — универсальные структуры данных, которые можно использовать для представления различных явлений реального мира, таких как карты полётов, графы социальных сетей и графы планирования учебных курсов. В этой главе мы узнаем о концепции и формате хранения графов, а также о том, как реализовать их на Rust. Мы также изучим два важных алгоритма поиска по графам, которые можно применять для решения различных задач. Исследование графов, их различных применений и алгоритмов относится к специализированной дисциплине, называемой теорией графов.

### 9.2.1 Словарь и определения графа

Граф является более общей формой дерева и определяется следующими понятиями:

- Вершина (или узел): элемент графа, имеющий имя, или ключ, и, возможно, дополнительную информацию, или полезную нагрузку.
- Ребро: элемент, соединяющий две вершины и указывающий на связь между ними. Ребро может быть однонаправленным или двунаправленным и может иметь вес, представляющий собой величину, такую как расстояние, стоимость, время или близость.
- Вес: мера ребра.

Граф может быть представлен как G = (V, E), где V — множество вершин, а E — множество рёбер. На рисунке ниже приведён пример взвешенного ориентированного графа с множеством вершин V = (V 0, V 1, V 2, V 2, V 4, V 5) и множеством рёбер E, состоящим из различных связей и их весов, всего 9 рёбер.

![Рисунок 9.1: Граф](images/fig-9.1.png)

*Рисунок 9.1: Граф*

Помимо вершин, рёбер и весов, для обозначения порядка точек используются пути. Путь — это последовательность вершин, представляющая порядок соединения точек, например (v, w, x, y, z). Могут также существовать циклические графы, имеющие циклы, например V 5−> V 2−> V 3−> V 5. Если в графе нет циклов, он называется ациклическим графом или графом DAG. Множество важных задач можно представить с помощью графов DAG.

## 9.3 Формат хранения графа

Для хранения нелинейного графа в линейном устройстве хранения, таком как память компьютера, используются два распространённых способа: матрица смежности и список смежности. Матрица смежности хранит узлы, ребра и веса графа в двумерной матрице, что требует N 2 места для графа с N узлами. Однако этот метод может привести к значительной растрате памяти, если граф разреженный. Напротив, список смежности аналогичен хеш-таблице и сохраняет все рёбра, относящиеся к каждой вершине, организуя для каждой вершины цепочку. Объём занимаемой памяти зависит от числа рёбер и обычно намного меньше N 2. Поэтому компьютеры используют списки смежности для хранения структур данных графов.

### 9.3.1 Матрица смежности

Матрица смежности — простой способ хранения графа. В этом методе вершины графа представляются строками и столбцами двумерной матрицы. Значение на пересечении строки v и столбца w указывает на наличие ребра между вершинами v и w, причём значение задаёт вес этого ребра. Если между двумя вершинами есть ребро, они называются смежными. Граф, изображённый на (9.1), можно сохранить с помощью матрицы смежности.

![Рисунок 9.2: Матрица смежности](images/fig-9.2.png)

*Рисунок 9.2: Матрица смежности*

Хотя матрица смежности легко понять и анализировать для небольших графов, у неё есть существенный недостаток: она часто бывает очень разреженной. Большинство ячеек матрицы пусты, что приводит к заметной растрате памяти. Для графа с N вершинами матрица смежности требует N 2 ячеек памяти. Поэтому матрица смежности — неэффективный способ хранения больших графов.

### 9.3.2 Список смежности

![Рисунок 9.3: Список смежности](images/fig-9.3.png)

*Рисунок 9.3: Список смежности*

Эффективный способ хранения графов — использование списка смежности, как показано на рисунке выше. В этом подходе массив хранит все вершины графа, а каждая вершина поддерживает связный список, соединяющий её с другими вершинами. Обращаясь к связным спискам различных вершин, можно узнать, с сколькими вершинами она соединена; это напоминает метод цепочек, который HashMap использует для разрешения коллизий. Список смежности хранит соединённые вершины в структуре, аналогичной HashMap, поскольку рёбра имеют вес, в то время как массивы могут хранить только вершины. Графы, реализованные через списки смежности, компактны и не тратят память зря. Эта структура также очень удобна для хранения. Здесь отчётливо видно значение базовых структур данных, а HashMap, реализованный в предыдущих главах, полезен для реализации списков смежности.

## 9.4 Абстрактный тип данных «Граф»

Абстрактный тип данных «Граф» (ADT) может быть определён на основе базового определения графа. В основе графа лежат вершины и рёбра, а операции определяются вокруг них. Для графа определены следующие операции:

- new(): создаёт новый пустой граф без параметров и возвращает пустой граф.
- add_vertex(v): добавляет в граф вершину с параметром v, возвращаемого значения нет.
- add_edge(fv,tv,w): добавляет в граф взвешенное ориентированное ребро с параметрами fv, tv и w, возвращаемого значения нет.
- get_vertex(vk): находит вершину с ключом vk в графе, требует параметр vk и возвращает вершину.
- get_vertices(): возвращает список всех вершин графа без параметров.
- vert_nums(): возвращает количество вершин в графе без параметров.
- edge_nums(): возвращает количество рёбер в графе без параметров.
- contains(vk): проверяет, содержится ли вершина в графе с параметром vk, и возвращает логическое значение.
- is_empty(): проверяет, пуст ли граф, без параметров, и возвращает логическое значение.

Пусть g — только что созданный пустой граф, таблица ниже показывает результаты различных операций над графом. [] хранит вершины, () хранит рёбра, где первые два значения — точки, а третье — вес ребра, например (1, 5, 2) означает, что вес ребра между точкой 1 и точкой 5 равен 2.

**Таблица 9.1: Операции над графом**

| Операция | Значение графа | Возвращаемое значение |
| --- | --- | --- |
| g.is_empty() | [] | true |
| g.add_vertex(1) | [1] |  |
| g.add_vertex(5) | [1,5] |  |
| g.add_edge(1,5,2) | [1,5,(1,5,2)] |  |
| g.get_vertex(5) | [1,5,(1,5,2)] | 5 |
| g.get_vertex(4) | [1,5,(1,5,2)] | None |
| g.edge_nums() | [1,5,(1,5,2)] | 1 |
| g.vert_nums() | [1,5,(1,5,2)] | 2 |
| g.contains(1) | [1,5,(1,5,2)] | true |
| g.get_verteces() | [1,5,(1,5,2)] | [1,5] |
| g.add_vertex(7) | [1,5,7,(1,5,2)] |  |
| g.add_vertex(9) | [1,5,7,9,(1,5,2)] |  |
| g.add_edge(7,9,8) | [1,5,7,9,(1,5,2),(7,9,8)] |  |
| g.contains(3) | [1,5,7,9,(1,5,2),(7,9,8)] | false |
| g.vert_nums() | [1,5,7,9,(1,5,2),(7,9,8)] | 4 |
| g.edge_nums() | [1,5,7,9,(1,5,2),(7,9,8)] | 2 |

## 9.5 Реализация графа в Rust

Чтобы реализовать в Rust граф на основе матрицы смежности, сначала нужно создать вершины и рёбра, а затем использовать двумерный Vec для хранения отношений рёбер.

```rust
// graph_matrix.rs

// Definition of graph vertex
#[derive(Debug)]
struct Vertex<'a> {
    id: usize,
    name: &'a str,
}

impl Vertex<'_> {
    fn new(id: usize, name: &'static str) -> Self {
        Self {
            id,
            name
        }
    }
}
```

Рёбра можно представить с помощью логического значения, указывающего на их существование, поскольку это просто отношения и их не требуется создавать как отдельные сущности.

```rust
// graph_matrix.rs

// Definition of graph edge
#[derive(Debug, Clone)]
struct Edge {
    edge: bool, // boolean value to show whethe edge exists
}

impl Edge {
    fn new() -> Self {
        Self { edge: false }
    }

    fn set_edge() -> Self {
        Edge { edge: true }
    }
}
```

Следовательно, отношения рёбер можно реализовать и сохранить в двумерном Vec.

```rust
// graph_matrix.rs

// Definition for Graph
#[derive(Debug)]
struct Graph {
    nodes: usize,
    graph: Vec<Vec<Edge>>, // store edges of a vertex
}
```

```rust
impl Graph {
    fn new(nodes: usize) -> Self {
        Self {
            nodes,
            graph: vec![vec![Edge::new(); nodes]; nodes],
        }
    }

    fn is_empty(&self) -> bool {
        0 == self.nodes
    }

    fn len(&self) -> usize { self.nodes }

    // add a edge and set the edge property to true
    fn add_edge(&mut self, n1: &Vertex, n2: &Vertex) {
        if n1.id < self.nodes && n2.id < self.nodes {
           self.graph[n1.id][n2.id] = Edge::set_edge();
        } else {
            println!("Error, vertex beyond the graph");
        }
    }
}

fn main() {
    let mut g = Graph::new(4);
    let n1 = Vertex::new(0,"n1");let n2 = Vertex::new(1,"n2");
    let n3 = Vertex::new(2,"n3");let n4 = Vertex::new(3,"n4");
    g.add_edge(&n1,&n2); g.add_edge(&n1,&n3);
    g.add_edge(&n2,&n3); g.add_edge(&n2,&n4);
    g.add_edge(&n3,&n4); g.add_edge(&n3,&n1);
    println!("{:#?}", g);
    println!("graph empty: {}", g.is_empty());
    println!("graph nodes: {}", g.len());
}
```

Ниже приведён вывод после выполнения.

```text
Graph {
    nodes: 4,
    graph: [
        [
            Edge { edge: false, },
            Edge { edge: true, },
            Edge { edge: true, },
            Edge { edge: false, },
        ],
        [
            Edge { edge: false, },
            Edge { edge: false, },
            Edge { edge: true, },
            Edge { edge: true, },
```

```text
        ],
        [
            Edge { edge: true, },
            Edge { edge: false, },
            Edge { edge: false, },
            Edge { edge: true, },
        ],
        [
            Edge { edge: false, },
            Edge { edge: false, },
            Edge { edge: false, },
            Edge { edge: false, },
        ],
    ],
}
graph empty: false
graph nodes: 4
```

Далее мы реализуем граф на основе списка смежности с использованием HashMap. Поскольку вершины являются основными элементами, а рёбра — отношениями между вершинами, необходимо создать структуру данных Vertex для представления элемента-вершины. Для Vertex нужно определить такие операции, как создание новой вершины, получение значения самой вершины, добавление смежных вершин, получение всех смежных вершин и получение весов смежных вершин. Переменная neighbors используется для хранения всех смежных вершин текущей вершины.

```rust
// graph_adjlist.rs

use std::hash::Hash;
use std::collections::HashMap;

// Definision of Vertex
#[derive(Debug, Clone)]
struct Vertex<T> {
    key: T,
    neighbors: Vec<(T, i32)>, // store adjacent vertices
}

impl<T: Clone + PartialEq> Vertex<T> {
    fn new(key: T) -> Self {
        Self {
          key: key,
          neighbors: Vec::new()
        }
    }

    // Check if a point is adjacent to the current point
    fn adjacent_key(&self, key: &T) -> bool {
        for (nbr, _wt) in self.neighbors.iter() {
            if nbr == key {
                return true;
            }
        }
```

```rust
        false
    }

    fn add_neighbor(&mut self, nbr: T, wt: i32) {
        self.neighbors.push((nbr, wt));
    }

    // Get the set of adjacent points
    fn get_neighbors(&self) -> Vec<&T> {
        let mut neighbors = Vec::new();
        for (nbr, _wt) in self.neighbors.iter() {
            neighbors.push(nbr);
        }

        neighbors
    }

    // Return the edge weight to the adjacent point
    fn get_nbr_weight(&self, key: &T) -> &i32 {
        for (nbr, wt) in self.neighbors.iter() {
            if nbr == key {
                return wt;
            }
        }

        &0
    }
}
```

Graph — это структура данных, используемая для реализации графов; она содержит HashMap, отображающий имена вершин в объекты вершин.

```rust
// graph_adjlist.rs

// Definish of Graph
#[derive(Debug, Clone)]
struct Graph <T> {
    vertnums: u32, // count of vertices
    edgenums: u32, // count of edges
    vertices: HashMap<T, Vertex<T>>,
}

impl<T: Hash + Eq + PartialEq + Clone> Graph<T> {
    fn new() -> Self {
        Self {
            vertnums: 0,
            edgenums: 0,
            vertices: HashMap::<T, Vertex<T>>::new(),
        }
    }

    fn is_empty(&self) -> bool { 0 == self.vertnums }
```

```rust
    fn vertex_num(&self) -> u32 { self.vertnums }

    fn edge_num(&self) -> u32 { self.edgenums }

    fn contains(&self, key: &T) -> bool {
        for (nbr, _vertex) in self.vertices.iter() {
            if nbr == key { return true; }
        }

        false
    }

    fn add_vertex(&mut self, key: &T) -> Option<Vertex<T>> {
        let vertex = Vertex::new(key.clone());
        self.vertnums += 1;
        self.vertices.insert(key.clone(), vertex)
    }

    fn get_vertex(&self, key: &T) -> Option<&Vertex<T>> {
        if let Some(vertex) = self.vertices.get(key) {
            Some(&vertex)
        } else {
            None
        }
    }

    // Get the keys of all nodes
    fn vertex_keys(&self) -> Vec<T> {
        let mut keys = Vec::new();
        for key in self.vertices.keys() {
            keys.push(key.clone());
        }

        keys
    }

    // Delete a point (and its edges)
    fn remove_vertex(&mut self, key: &T) -> Option<Vertex<T>> {
        let old_vertex = self.vertices.remove(key);
        self.vertnums -= 1;

        // Delete edges from the current point
        self.edgenums -= old_vertex.clone()
                                   .unwrap()
                                   .get_neighbors()
                                   .len() as u32;

        // Delete edges to the current point
        for vertex in self.vertex_keys() {
            if let Some(vt) = self.vertices.get_mut(&vertex) {
                if vt.adjacent_key(key) {
                    vt.neighbors.retain(|(k, _)| k != key);
```

```rust
                    self.edgenums -= 1;
                }
            }
        }

        old_vertex
    }

    fn add_edge(&mut self, from: &T, to: &T, wt: i32) {
        // If the point doesn't exist, add it first
        if !self.contains(from) {
            let _fv = self.add_vertex(from);
        }
        if !self.contains(to) {
            let _tv = self.add_vertex(to);
        }

        // Add an edge
        self.edgenums += 1;
        self.vertices.get_mut(from)
                     .unwrap()
                     .add_neighbor(to.clone(), wt);
    }

    // Determine if two vertices are adjacent
    fn adjacent(&self, from: &T, to: &T) -> bool {
        self.vertices.get(from).unwrap().adjacent_key(to)
    }
}
```

С помощью Graph можно создать вершины V0–V5 и их рёбра, как показано на графе (9.1).

```rust
// graph_adjlist.rs

fn main() {
    let mut g = Graph::new();

    for i in 0..6 { g.add_vertex(&i); }
    println!("graph empty: {}", g.is_empty());

    let vertices = g.vertex_keys();
    for vtx in vertices { println!("Vertex: {:#?}", vtx); }

    g.add_edge(&0,&1,5); g.add_edge(&0,&5,2);
    g.add_edge(&1,&2,4); g.add_edge(&2,&3,9);
    g.add_edge(&3,&4,7); g.add_edge(&3,&5,3);
    g.add_edge(&4,&0,1); g.add_edge(&4,&4,8);
    println!("vert nums: {}", g.vertex_num());
    println!("edge nums: {}", g.edge_num());
    println!("contains 0: {}", g.contains(&0));

    let vertex = g.get_vertex(&0).unwrap();
    println!("key: {}, to nbr 1 weight: {}",
```

```rust
              vertex.key, vertex.get_nbr_weight(&1));

    let keys = vertex.get_neighbors();
    for nbr in keys { println!("nighbor: {nbr}"); }

    for (nbr, wt) in vertex.neighbors.iter() {
        println!("0 nighbor: {nbr}, weight: {wt}");
    }

    let res = g.adjacent(&0, &1);
    println!("0 adjacent to 1: {res}");
    let res = g.adjacent(&3, &2);
    println!("3 adjacent to 2: {res}");

    let rm = g.remove_vertex(&0).unwrap();
    println!("remove vertex: {}", rm.key);
    println!("left vert nums: {}", g.vertex_num());
    println!("left edge nums: {}", g.edge_num());
    println!("contains 0: {}", g.contains(&0));
}
```

Ниже приведён вывод после выполнения.

```text
graph empty: false
Vertex: 3
Vertex: 4
Vertex: 1
Vertex: 2
Vertex: 5
Vertex: 0
vert nums: 6
edge nums: 8
contains 0: true
key: 0, to nbr 1 weight: 5
nighbor: 1
nighbor: 5
0 nighbor: 1, weight: 5
0 nighbor: 5, weight: 2
0 is adjacent to 1: true
3 is adjacent to 2: false
remove vertex: 0
left vert nums: 5
left edge nums: 5
contains 0: false
```

### 9.5.1 Задача о цепочке слов

Структура данных «граф» позволяет решать практические задачи, например головоломку «цепочка слов» (word ladder). В этой головоломке нужно преобразовать одно слово в другое, меняя за один раз по одной букве (FOOL -> SAGE), при этом получившееся слово должно существовать в словаре. Эта игра была придумана в 1878 году Льюисом Кэрроллом, автором «Alice’s Adventures in Wonderland». У этой задачи существует несколько решений, как показано в последовательности слов ниже.

```text
 a
       b
            c
                  d
                        e
                              f
                                    g
---------------------------------------
FOOL
      FOOL FOOL
                 FOOL
                       FOOL
                             FOOL
                                   FOOL
POOL
      FOIL FOIL
                 COOL
                       COOL
                             FOUL
                                   FOUL
POLL
      FAIL FAIL
                 POOL
                       POOL
                             FOIL
                                   FOIL
POLE
      FALL FALL
                 POLL
                       POLL
                             FALL
                                   FALL
PALE
      PALL PALL
                 POLE
                       PALL
                             FALL
                                   FALL
SALE
      PALE PALE
                 PALE
                       PALE
                             PALL
                                   PALL
SAGE
      PAGE SALE
                 SALE
                       SALE
                             POLL
                                   POLL
      SAGE SAGE
                 SAGE
                       SAGE
                             PALE
                                   PALE
                             PAGE
                                   SALE
                             SAGE
                                   SAGE
```

Наша цель — использовать графовые алгоритмы для поиска кратчайшего пути между начальным и конечным словами, как показано в столбце a приведённого выше рисунка. Для этого сначала преобразуем слова в вершины и соединим между собой слова, которые могут быть преобразованы друг в друга. Если два слова различаются только одной буквой, между ними создаётся двунаправленное ребро, как показано на рисунке ниже. Наконец, используем алгоритм поиска по графу, чтобы найти кратчайший путь между начальной и конечной вершинами.

![Рисунок 9.4: Цепочка слов](images/fig-9.4.png)

*Рисунок 9.4: Цепочка слов*

Для создания графовой модели задачи о цепочке слов существует несколько способов. При работе со списком слов одинаковой длины можно создать вершину для каждого слова из списка. Чтобы соединить слова, каждое слово из списка нужно сравнить с остальными. Если два сравниваемых слова различаются только одной буквой, между ними в графе можно создать ребро. Этот метод пригоден для небольших списков слов, но для больших списков, таких как словарь CET-4 с 3000 слов или словарь CET-6 с 5000 слов, такое сравнение неэффективно и требует миллионов сравнений. Альтернативный подход состоит в том, чтобы рассматривать позиции букв в словах и группировать слова по схожим шаблонам. Таким образом, для каждой позиции можно искать похожие слова и объединять их в группы. Например, если убрать первую букву слова SOPE и оставить остальное «_OPE», все четырёхбуквенные слова, оканчивающиеся на «OPE», должны быть связаны со словом SOPE и собраны в множество. Тот же процесс применяется к «S_PE», и все слова, соответствующие этому шаблону, собираются вместе. Наконец, собираются все слова, соответствующие этому шаблону, как показано на рисунке ниже.

```text
_OPE P_PE
           PO_E
                 POP_
POPE POPE
           POPE
                 POPE
ROPE PIPE
           POLE
                 POPS
NOPE PAPE
           PORE
HOPE
           POSE
LOPE
           POKE
COPE
```

Это решение можно реализовать с помощью HashMap. Упомянутое ранее множество хранит слова с одинаковым шаблоном в виде ключей в HashMap, который хранит наборы похожих слов. После того как множества слов сформированы, можно создать граф. Для начала создаётся вершина для каждого слова в HashMap, а затем создаются рёбра между всеми вершинами, найденными под одним и тем же ключом в словаре. Когда граф реализован, задача поиска цепочки может быть выполнена.

## 9.6 Breadth First Search(BFS)

Изучение графов и теории графов — сложная предметная область, для которой разработано множество превосходных алгоритмов. Однако наиболее часто используются алгоритмы поиска в ширину (BFS) и поиска в глубину (DFS). В задаче о цепочке слов BFS применяется для нахождения кратчайшего пути, поскольку графы нелинейны, и традиционные алгоритмы двоичного и линейного поиска для этой задачи непригодны.

fool pool foil foul cool searching queue pool foil foul cool

Алгоритм BFS исследует рёбра графа, чтобы найти все вершины в G (предполагая, что расстояние между точками равно 1), до которых существует путь из заданной вершины s. Он делает это, сначала находя все вершины, удалённые от s на одну единицу, затем все вершины, удалённые на две единицы, и так далее, пока не будут найдены все вершины. Поиск выполняется слой за слоем, поэтому он и называется поиском в ширину. Точки, соединённые с исходной вершиной, рассматриваются как один слой, сначала помещаются в очередь, а затем алгоритм находит следующий слой соединяющих точек для находящихся в очереди и повторяет процесс до завершения поиска. Во время поиска вершины можно раскрашивать, чтобы указать их состояние. Изначально все вершины белые. По мере выполнения поиска вершины, соединённые с текущей рассматриваемой вершиной, помечаются серым. Алгоритм проверяет каждую серую вершину, и если она не является целевым значением, она помечается чёрным, а поиск продолжается среди белых вершин, соединённых с серой вершиной. Этот процесс продолжается до выполнения задачи поиска или до полного обхода графа. Такой метод поиска похож на механизм сборки мусора в некоторых языках, например на трёхцветную сборку мусора в языке Go.

### 9.6.1 Implementing a BFS

Чтобы реализовать простой алгоритм BFS, сначала нужно создать граф. Конкретная форма графа зависит от назначения алгоритма. Здесь мы продемонстрируем алгоритм BFS на простом графе, в котором узлы содержат данные и ссылку на следующий узел. В графе мы будем хранить только первый узел и ссылку на следующий узел.

```rust
// bfs.rs

use std::rc::Rc;
use std::cell::RefCell;

// Node has multiple shared links,
// Box cannot be shared, only Rc can be shared.
// Rc is immutable, RefCell with internal mutability
// is used to wrap it.
type Link = Option<Rc<RefCell<Node>>>;

// Definition for a Node
struct Node {
    data: usize,
    next: Link,
}

impl Node {
    fn new(data: usize) -> Self {
        Self {
            data: data,
            next: None
        }
    }
}

// Definition for a Graph
struct Graph {
    first: Link,
    last: Link,
}

impl Graph {
    fn new() -> Self {
        Self { first: None, last: None }
    }

    fn is_empty(&self) -> bool {
        self.first.is_none()
    }

    fn get_first(&self) -> Link {
        self.first.clone()
    }

    // Print node
    fn print_node(&self) {
        let mut curr = self.first.clone();
        while let Some(val) = curr {
            print!("[{}]", &val.borrow().data);
            curr = val.borrow().next.clone();
```

```rust
        }

        print!("\n");
    }

    // Insert node, RefCell is used to borrow_mut to modify
    fn insert(&mut self, data: usize) {
        let node = Rc::new(RefCell::new(Node::new(data)));

        if self.is_empty() {
            self.first = Some(node.clone());
            self.last = Some(node);
        } else {
            self.last.as_mut()
                     .unwrap()
                     .borrow_mut()
                     .next = Some(node.clone());
            self.last = Some(node);
        }
    }
}
```

Приведённый выше код показывает реализацию графа. Следующий код использует этот граф для реализации базового алгоритма поиска в ширину. Функция build_graph строит граф и инкапсулирует его в кортеж, который затем сохраняется в вектор. Второе значение кортежа указывает, был ли узел посещён: 0 означает, что не посещён, а 1 — что посещён.

```rust
// bfs.rs

// Build the graph based on data
fn build_graph(data: [[usize;2];20]) -> Vec<(Graph, usize)> {
    let mut graphs: Vec<(Graph, usize)> = Vec::new();
    for _ in 0..9 { graphs.push((Graph::new(), 0)); }
    for i in 1..9 {
        for j in 0..data.len() {
            if data[j][0] == i {
                graphs[i].0.insert(data[j][1]);
            }
        }
        print!("[{i}]->");
        graphs[i].0.print_node();
    }
    graphs
}

fn bfs(graph: Vec<(Graph, usize)>) {
    let mut gp = graph;
    let mut nodes = Vec::new();
    gp[1].1 = 1;
    let mut curr = gp[1].0.get_first().clone();

    // Print the graph
    print!("{1}->");
```

```rust
    while let Some(val) = curr {
        nodes.push(val.borrow().data);
        curr = val.borrow().next.clone();
    }

    // Print the breadth-first graph
    loop {
        if 0 == nodes.len() {
            break;
        } else {
            // Pop the first node from nodes, mimicking a queue
            let data = nodes.remove(0);
            // If the node has not been visited,
            // add it to nodes and change its visit status to 1
            if 0 == gp[data].1 {
                gp[data].1 = 1;
                // Print the value of the current node
                print!("{data}->");
                // Add nodes connected to current node to nodes
                let mut curr = gp[data].0.get_first().clone();
                while let Some(val) = curr {
                    nodes.push(val.borrow().data);
                    curr = val.borrow().next.clone();
                }
            }
        }
    }
    println!();
}

fn main() {
    let data = [
      [1,2],[2,1],[1,3],[3,1],[2,4],[4,2],[2,5],
      [5,2],[3,6],[6,3],[3,7],[7,3],[4,5],[5,4],
      [6,7],[7,6],[5,8],[8,5],[6,8],[8,6]
    ];
    let gp = build_graph(data);
    bfs(gp);
}
```

Вывод кода, который печатает соседние узлы каждой вершины и все вершины, показан ниже.

```rust
[1]->[2][3]
[2]->[1][4][5]
[3]->[1][6][7]
[4]->[2][5]
[5]->[2][4][8]
[6]->[3][7][8]
[7]->[3][6]
[8]->[5][6]
1->2->3->4->5->6->7->8->
```

Этот алгоритм использует Vec в качестве очереди для поиска кратчайшего пути преобразования в цепочке слов. Помимо печати значений связей каждого узла, он также печатает все узлы в порядке их поиска. Чтобы лучше представлять цвета узлов, нужно определить перечисление, представляющее цвета, и соответствующим образом обновлять цвета узлов. В узел нужно добавить значение расстояния, представляющее расстояние от начальной точки, чтобы можно было вычислить кратчайшее расстояние.

```rust
// word_ladder.rs

// Enum for colors used to determine
// if a node has been searched
#[derive(Clone, Debug, PartialEq)]
enum Color {
    White, // White: not yet explored
    Gray, // Gray: currently being explored
    Black, // Black: exploration complete
}

// Definition for a Vertex
#[derive(Debug, Clone)]
struct Vertex<T> {
    color: Color,
    distance: u32, // Minimum distance from the starting node
                   // i.e. minimum number of transformations
    key: T,
    neighbors: Vec<(T, u32)>, // store all adjacent vertices
}

impl<T: Clone + PartialEq> Vertex<T> {
    fn new(key: T) -> Self {
        Self {
            color: Color::White,
            distance: 0,
            key: key,
            neighbors: Vec::new(),
        }
    }

    fn add_neighbor(&mut self, nbr: T, wt: u32) {
        self.neighbors.push((nbr, wt));
    }

    // Get adjacent nodes
    fn get_neighbors(&self) -> Vec<&T> {
        let mut neighbors = Vec::new();

        for (nbr, _wt) in self.neighbors.iter() {
            neighbors.push(nbr);
        }

        neighbors
    }
}
```

Приведённый выше код, в котором задаются цвет и узел, сложнее базового алгоритма BFS. Для добавления узлов в очередь вводится реализация Queue из главы 4. Определение графа для решения задачи о цепочке слов включает количество узлов, рёбер и hashMap для хранения значений узлов и их структур.

```rust
// word_ladder.rs

use std::collections::HashMap;
use std::hash::Hash;

// Definition of Graph
#[derive(Debug, Clone)]
struct Graph<T> {
    vertnums: u32,
    edgenums: u32,
    vertices: HashMap<T, Vertex<T>>,
}

impl<T: Hash + Eq + PartialEq + Clone> Graph<T> {
    fn new() -> Self {
        Self {
            vertnums: 0,
            edgenums: 0,
            vertices: HashMap::<T, Vertex<T>>::new(),
        }
    }

    fn contains(&self, key: &T) -> bool {
        for (nbr, _vertex) in self.vertices.iter() {
            if nbr == key { return true; }
        }

        false
    }

    // add a vertice
    fn add_vertex(&mut self, key: &T) -> Option<Vertex<T>> {
        let vertex = Vertex::new(key.clone());
        self.vertnums += 1;
        self.vertices.insert(key.clone(), vertex)
    }

    // add an edge
    fn add_edge(&mut self, from: &T, to: &T, wt: u32) {
        // Add node if it doesn't exist
        if !self.contains(from) {
            let _fvert = self.add_vertex(from);
        }
        if !self.contains(to) {
            let _tvert = self.add_vertex(to);
        }
```

```text
        self.edgenums += 1;
        self.vertices
            .get_mut(from)
            .unwrap()
            .add_neighbor(to.clone(), wt);
    }
}
```

С помощью этого графа можно построить граф цепочки слов, упорядочив слова в соответствии с их шаблонами.

```rust
// word_ladder.rs

// Construct the graph based on words and patterns
fn build_word_graph(words: Vec<&str>) -> Graph<String> {
    let mut hmap: HashMap<String,Vec<String>> = HashMap::new();

    // Build a word-pattern hashMap
    for word in words {
        for i in 0..word.len() {
            let pattn = word[..i].to_string()
                        + "_"
                        + &word[i + 1..];
            if hmap.contains_key(&pattn) {
                hmap.get_mut(&pattn)
                    .unwrap()
                    .push(word.to_string());
            } else {
                hmap.insert(pattn, vec![word.to_string()]);
            }
        }
    }

    // Double-ended graph with a distance of 1
    let mut word_graph = Graph::new();
    for word in hmap.keys() {
        for w1 in &hmap[word] {
            for w2 in &hmap[word] {
                if w1 != w2 {
                    word_graph.add_edge(w1, w2, 1);
                }
            }
        }
    }

    word_graph
}
```

Затем алгоритм BFS используется для поиска кратчайшего пути. Обратите внимание: хотя определены три цвета, в очередь будут добавляться только белые узлы, поэтому серые узлы можно помечать чёрным или оставлять без пометки. Эта функция BFS строит дерево поиска в ширину, а очередь поиска очищается, когда алгоритм находит результат «sage».

```rust
// word_ladder.rs

// Word ladder graph - breadth-first search
fn word_ladder(g: &mut Graph<String>,
               start: Vertex<String>,
               end: Vertex<String>,
               len: usize) -> u32
{
    // Check if the starting point exists
    if !g.vertices.contains_key(&start.key) {
        return 0;
    }

    if !g.vertices.contains_key(&end.key) {
        return 0;
    }

    // Prepare the queue and add the starting point
    let mut vertex_queue = Queue::new(len);
    let _r = vertex_queue.enqueue(start);

    while vertex_queue.len() > 0 {
        // Dequeue the node
        let curr = vertex_queue.dequeue().unwrap();

        for nbr in curr.get_neighbors() {
            // Clone to avoid conflicts with data in the graph
            // Vertices in the Graph are wrapped with RefCell
            // and do not need to be cloned
            let mut nbv = g.vertices.get(nbr).unwrap().clone();

            if end.key != nbv.key {
                // Only white nodes can be added to the queue;
                // other colors have already been processed
                if Color::White == nbv.color {
                    // Update the node's color and distance and
                    // add it to the queue
                    nbv.color = Color::Gray;
                    nbv.distance = curr.distance + 1;

                    // The color and distance of the node
                    // in the graph also need to be updated
                    g.vertices.get_mut(nbr)
                              .unwrap()
                              .color = Color::Gray;
                    g.vertices.get_mut(nbr)
                              .unwrap()
                              .distance = curr.distance + 1;

                    // Add white nodes to the queue
                    let _r = vertex_queue.enqueue(nbv);
```

```rust
                }
            } else {
                // Since the neighbor of curr contains end,
                // one more transformation is enough
                return curr.distance + 1;
            }
        }
    }

    0
}

fn main() {
    let words = [
      "FOOL", "COOL", "POOL", "FOUL", "FOIL", "FAIL", "FALL",
      "POLL", "PALL", "POLE", "PALE", "SALE", "PAGE", "SAGE",
    ];

    let len = words.len();
    let mut g = build_word_graph(words);

    // The starting node is added to the queue and is
    // being explored, so its color changes to gray
    g.vertices.get_mut("FOOL").unwrap().color = Color::Gray;

    // Retrieve the first and last points
    let start = g.vertices.get("FOOL").unwrap().clone();
    let end = g.vertices.get("SAGE").unwrap().clone();

    // Calculate the minimum number of transformations,
    // which is the distance.
    let distance = word_ladder(&mut g, start, end, len);
    println!("the shortest distance: {distance}");
    // the shortest distance: 6
}
```

В процессе поиска строится дерево поиска в ширину, а раскраска узлов в процессе поиска показана на рисунке. В начале берутся все узлы, соседние с «fool», включая «pool», «foil», «foul» и «cool», и эти узлы добавляются в очередь для поиска.

fool pool foil foul cool poll searching queue poll foil foul cool

Когда bfs проверяет узел «cool», он обнаруживает, что тот серый, а это указывает на наличие более короткого пути к «cool». При проверке «pool» добавляется новый узел «poll».

fool pool foil foul cool poll fail searching queue poll fail

Следующая вершина в очереди — «foil», и единственный новый узел, который можно добавить в дерево, — «fail». Когда bfs продолжает обрабатывать очередь, следующие два узла не добавляют в очередь никаких новых точек.

fool pool foil foul cool poll fail pole pall pope pale page sale sage searching queue

Наконец, кратчайший путь — это количество уровней от «fool» до «sage», равное 6 уровням (кратчайший путь равен 6). Читатели могут проверить этот код на других словах.

### 9.6.2 Analysis of BFS

Временная сложность поиска в ширину (BFS) зависит от количества вершин и рёбер в графе. Чтобы построить граф в BFS, нужно обработать как минимум V вершин, что даёт временную сложность O(V). Во время поиска BFS обрабатывает одно ребро за раз, что даёт временную сложность O(E). Таким образом, общая временная сложность BFS составляет O(V + E). Если все вершины соединены с начальным узлом, очередь должна хранить как минимум количество узлов графа, что даёт пространственную сложность O(V). Интересно, что граф можно также рассматривать как развёрнутый многогранник, и количество его вершин, рёбер и граней должно удовлетворять формуле Эйлера V − E + F = 2. Переставив эту формулу, получаем V + E = 2E − F + 2, что означает, что сложность BFS равна O(V + E) = O(2E − F + 2). В случае графа цепочки слов (рис. 9.5.1) количество вершин, рёбер и граней равно соответственно 18, 14 и 6, и формула проверяется подстановкой этих значений. Здесь я хочу сказать, что алгоритм BFS для графов, по-видимому, распространяется на геометрическую область, что является для меня большим вдохновением.

### 9.6.3 The Knight’s Tour Problem

Маршрут коня — классическая головоломка, в которой шахматная фигура конь перемещается по шахматной доске так, чтобы посетить каждую клетку ровно один раз, образуя маршрут. Эта задача многие годы увлекала многих людей, включая игроков, математиков и специалистов по информатике, и существует множество алгоритмов её решения. Поиск по графу — самое прямое решение, требующее двух шагов: представления ходов коня и нахождения пути длиной rows × columns − 1, где начальная клетка не учитывается. На шахматной доске 8 × 8 возможно максимум 1.305 × 1035 маршрутов. Чтобы представить задачу о маршруте коня в виде графа, каждая клетка шахматной доски представляется как узел, а каждый допустимый ход коня представляется как ребро графа. Конь показан на рисунке ниже жёлтым квадратом.

20 23 21 22 24 21 23 15 16 17 18 19 15 19 12 10 13 11 12 14 5 9 3 1 5 7 9 6 8 movable vertices 0 3 1 2 4

Чтобы построить полный граф размера n × n, нужно рассмотреть восемь возможных ходов коня. Обойдя весь граф, можно составить список ходов для каждой позиции, и все они могут быть преобразованы в рёбра графа.

```rust
// knight_tour.rs

use std::collections::HashMap;
use std::hash::Hash;
```

```rust
use std::fmt::Display;

// bread-width
const BDSIZE: u32 = 8;

// Color enum used to determine if a node has been searched
#[derive(Debug, Clone, PartialEq)]
enum Color {
    White, // White: not yet explored
    Gray, // Gray: currently being explored
}

// Definition of vertice
#[derive(Debug, Clone)]
struct Vertex<T> {
    key: T,
    color: Color,
    neighbors: Vec<T>,
}

impl<T: PartialEq + Clone> Vertex<T> {
    fn new(key: T) -> Self {
        Self {
            key: key,
            color: Color::White,
            neighbors: Vec::new(),
        }
    }

    fn add_neighbor(&mut self, nbr: T) {
        self.neighbors.push(nbr);
    }

    fn get_neighbors(&self) -> Vec<&T> {
        let mut neighbors = Vec::new();
        for nbr in self.neighbors.iter() {
            neighbors.push(nbr);
        }
        neighbors
    }
}
```

После того как все возможные ходы каждого узла найдены, можно построить граф маршрута коня.

```rust
// knight_tour.rs

// Knight's tour graph definition
#[derive(Debug, Clone)]
struct Graph<T> {
    vertnums: u32,
    edgenums: u32,
    vertices: HashMap<T, Vertex<T>>,
}
```

```rust
impl<T: Eq + PartialEq + Clone + Hash> Graph<T> {
    fn new() -> Self {
        Self {
            vertnums: 0,
            edgenums: 0,
            vertices: HashMap::<T, Vertex<T>>::new(),
        }
    }

    fn add_vertex(&mut self, key: &T) -> Option<Vertex<T>> {
        let vertex = Vertex::new(key.clone());
        self.vertnums += 1;
        self.vertices.insert(key.clone(), vertex)
    }

    fn add_edge(&mut self, src: &T, des: &T) {
        if !self.vertices.contains_key(src) {
          let _fv = self.add_vertex(src);
        }
        if !self.vertices.contains_key(des) {
          let _tv = self.add_vertex(des);
        }

        self.edgenums += 1;
        self.vertices.get_mut(src)
                     .unwrap()
                     .add_neighbor(des.clone());
    }
}

// Destination coordinates that can be moved to
fn legal_moves(x: u32, y: u32, bdsize: u32) -> Vec<(u32, u32)>
   { // Knight moves like a horse, which is a "L" shape move
    // Horizontal and vertical coordinates of the horse will
    // increase or decrease accordingly in eight directions
    let move_offsets = [
                (-1, 2), ( 1, 2),
        (-2, 1), ( 2, 1),
        (-2, -1), ( 2, -1),
                (-1, -2), ( 1, -2),
    ];

    // A closure function to check if the new coordinate
    // is valid (within the chessboard range)
    let legal_pos = |a: i32, b: i32| { a >= 0 && a < b };

    let mut legal_positions = Vec::new();
    for (x_offset, y_offset) in move_offsets.iter() {
        let new_x = x as i32 + x_offset;
        let new_y = y as i32 + y_offset;
```

```rust
        // Check the coordinate and add it to
        // the set of movable points
        if legal_pos(new_x, bdsize as i32)
          && legal_pos(new_y, bdsize as i32) {
            legal_positions.push((new_x as u32, new_y as u32));
        }
    }

    // Return the set of movable points
    legal_positions
}

// Build the graph of movable paths
fn build_knight_graph(bdsize: u32) -> Graph<u32> {
    // A closure function to calculate the point value
    // Point range is [0, 63]
    let calc_point = |row: u32, col: u32, size: u32| {
      (row % size) * size + col
    };

    // Set edges between points
    let mut knight_graph = Graph::new();
    for row in 0..bdsize {
        for col in 0..bdsize {
            let dests = legal_moves(row, col, bdsize);
            for des in dests {
                let src_p = calc_point(row, col, bdsize);
                let des_p = calc_point(des.0, des.1, bdsize);
                knight_graph.add_edge(&src_p, &des_p);
            }
        }
    }

    knight_graph
}
```

Алгоритм поиска, используемый для решения задачи о маршруте коня, называется поиском в глубину. Тогда как поиск в ширину исследует вершины одного уровня как можно шире, поиск в глубину исследует несколько уровней дерева как можно глубже. Для решения задачи с помощью поиска в глубину можно применять различные стратегии. Первая стратегия запрещает посещать узлы несколько раз, а вторая позволяет посещать узлы несколько раз при построении дерева. Когда алгоритм поиска в глубину встречает тупик (то есть точку, из которой нет ходов), он возвращается к предыдущей самой глубокой точке и продолжает исследование.

```rust
// depth: length of the path traveled,
// curr: current node, path: saves visited points
fn knight_tour<T>(
    kg: &mut Graph<T>,
    curr: Vertex<T>,
    path: &mut Vec<String>,
    depth: u32) -> bool
    where T: Eq + PartialEq + Clone + Hash + Display
```

```rust
{
    // Add the string value of the current node to path
    path.push(curr.key.to_string());

    let mut done = false;
    if depth < BDSIZE * BDSIZE - 1 {
        let mut i = 0;
        let nbrs = curr.get_neighbors();

        // Knight travels between neighboring points
        while i < nbrs.len() && !done {
            // Avoid multiple mutable references
            let nbr =kg.vertices.get(nbrs[i]).unwrap().clone();

            if Color::White == nbr.color {
                // Update the corresponding point color to gray
                kg.vertices.get_mut(nbrs[i])
                           .unwrap()
                           .color = Color::Gray;
                // Search for the next suitable point
                done = knight_tour(kg, nbr, path, depth + 1);
                if !done {
                    // If not found, remove the current point
                    // from path and restore the color of the
                    // corresponding point to white
                    let _rm = path.pop();
                    kg.vertices.get_mut(nbrs[i])
                               .unwrap()
                               .color = Color::White;
                }
            }

            // Explore the next neighboring point
            i += 1;
        }
    } else {
        done = true;
    }

    done
}

fn main() {
    // Build the knight's tour graph
    let mut kg: Graph<u32> = build_knight_graph(BDSIZE);

    // Choose a starting point and update the color
    // of the corresponding point in the graph
    let point = 0;
    kg.vertices.get_mut(&point).unwrap().color = Color::Gray;
    let start = kg.vertices.get(&point).unwrap().clone();
```

```rust
    // Start the knight's tour path saves all visited points
    let mut path = Vec::new();
    let successed = knight_tour(&mut kg, start, &mut path, 0);

    // Format and output the result.
    if successed {
        for row in 0..BDSIZE {
            let row_s = ((row % BDSIZE) * BDSIZE) as usize;
            let row_e = row_s + BDSIZE as usize;
            let row_str = path[row_s..row_e].join("\t");
            println!("{row_str}");
        }
    }
}
```

Пути маршрута коня можно получить с помощью алгоритма knight_tour.

```text
0
        10
                4
                        14
                                31
                                        46
                                                63
                                                        53
47
        30
                15
                        5
                                22
                                        7
                                                13
                                                        23
6
        21
                38
                        55
                                45
                                        39
                                                54
                                                        37
20
        3
                18
                        12
                                29
                                        44
                                                61
                                                        51
36
        19
                2
                        8
                                25
                                        35
                                                41
                                                        56
50
        60
                43
                        28
                                11
                                        1
                                                16
                                                        26
9
        24
                34
                        40
                                57
                                        42
                                                59
                                                        49
32
        17
                27
                        33
                                48
                                        58
                                                52
                                                        62
```

Задачу о маршруте коня можно решить с помощью рекурсивной версии алгоритма поиска в глубину, называемой алгоритмом knight_tour. Этот алгоритм ищет путь длиной 64, что равно количеству клеток на шахматной доске. Алгоритм исследует граф, переходя к следующей вершине, пока не достигнет тупика или не исчерпает весь граф, а затем выполняет возврат. Для отслеживания посещённых вершин поиск в глубину использует цвета: непосещённые вершины белые, а посещённые — серые. Возврат происходит, когда функция knight_tour возвращает false, что указывает на достижение тупика. В отличие от поиска в ширину, который использует очередь для отслеживания следующей вершины, поиск в глубину является рекурсивным и имеет неявный стек, который помогает алгоритму выполнять возврат.

## 9.7 Depth First Search(DFS)

Задача о маршруте коня — это частный случай алгоритма поиска в глубину, который направлен на создание максимально глубокого дерева. Поиск в глубину обычно используется для обхода графов с множеством ветвей: его цель — проникать как можно глубже, связывать как можно больше узлов и ветвиться при необходимости. В некоторых случаях поиск в глубину может создавать несколько деревьев, которые называются лесом поиска в глубину. Как и поиск в ширину, поиск в глубину использует ссылки на предшественников для построения деревьев. Чтобы лучше понять поиск в глубину, класс вершины можно расширить двумя переменными, указывающими время начала и окончания поиска узла: время начала также указывает количество шагов до встречи с вершиной, а время окончания — количество шагов до того, как вершина окрашивается в чёрный цвет. На следующем рисунке показан небольшой граф и применённый к нему алгоритм поиска в глубину. Толстые линии обозначают проверенные рёбра, причём узел на другом конце ребра уже добавлен в дерево поиска в глубину. Поиск начинается с вершины A, и поскольку в начале поиска все вершины окрашены, алгоритм случайным образом начинает обход с вершины A. При посещении вершины первым шагом её цвет устанавливается в серый, что указывает на то, что вершина исследуется, а время обнаружения — в 1. Поскольку у вершины A две смежные вершины (B и D), каждую вершину необходимо посетить, причём смежные вершины посещаются в алфавитном порядке.

A1/ B C D E F

Далее мы посещаем вершину B, которая смежна с вершинами C и D. Вершина C приводит нас к концу ветви, поэтому её можно окрасить в чёрный цвет и установить время окончания равным 4. Теперь возвращаемся к вершине B и продолжаем исследовать D, которая приводит нас к вершине E. У вершины E две смежные вершины — B и F. Поскольку B уже окрашена в чёрный цвет, её можно пропустить и посетить вершину F.

C3/ A1/ B2/ A1/ B2/ C D E F D E F C C A1/ B2/ A1/ B2/ 3/4 3/4 D5/ D5/ E6/ F7/ E F

У вершины F есть только одна смежная вершина — C, уже окрашенная в чёрный цвет, поэтому алгоритм достиг конца ветви. Следовательно, алгоритм должен выполнять обратный поиск с откатами (бэктрекинг) и продолжать поиск до тех пор, пока не встретит серую вершину или не завершится.

C C3/ A1/ B2/ A1/ B2/ 3/4 D5/ E6/ F D5/ E F D E F 7/8 6/9 7/8 C C A1/ B2/ A1/ B 3/4 2/11 3/4 D E F D E F 5/10 6/9 7/8 5/10 6/9 7/8

В итоге алгоритм возвращается к исходной вершине и завершает поиск, получая пройденный путь: A → B → D → E → F.

C A B 1/12 2/11 3/4 D E F 5/10 6/9 7/8

### 9.7.1 Implementing a DFS

Основываясь на предыдущем обсуждении и иллюстрации, можно представить базовую реализацию алгоритма поиска в глубину, которая не включает цветовые пометки, но реализует основной функционал исследования.

```rust
// dfs.rs
use std::rc::Rc;
use std::cell::RefCell;

// Node link
type Link = Option<Rc<RefCell<Node>>>;

struct Node {
    data: usize,
    next: Link,
}

impl Node {
    fn new(data: usize) -> Self {
        Self {
            data: data,
            next: None
        }
    }
}

// Definition of Graph
struct Graph {
    first: Link,
    last: Link,
}

impl Graph {
    fn new() -> Self {
        Self { first: None, last: None }
    }

    fn is_empty(&self) -> bool {
        self.first.is_none()
    }

    fn get_first(&self) -> Link {
        self.first.clone()
    }

    fn print_node(&self) {
        let mut curr = self.first.clone();
        while let Some(val) = curr {
            print!("[{}]", &val.borrow().data);
            curr = val.borrow().next.clone();
        }
        print!("\n");
```

```rust
    }

    // insert data
    fn insert(&mut self, data: usize) {
        let node = Rc::new(RefCell::new(Node::new(data)));
        if self.is_empty() {
            self.first = Some(node.clone());
            self.last = Some(node);
        } else {
            self.last.as_mut()
                     .unwrap()
                     .borrow_mut()
                     .next = Some(node.clone());
            self.last = Some(node);
        }
    }
}

// build a graph
fn build_graph(data: [[usize;2];20]) -> Vec<(Graph, usize)> {
    let mut graphsVec<(Graph, usize)> = Vec::new();
    for _ in 0..9 {
      graphs.push((Graph::new(), 0));
    }

    for i in 1..9 {
        for j in 0..data.len() {
            if data[j][0] == i {
              graphs[i].0.insert(data[j][1]);
            }
        }

        print!("[{i}]->");
        graphs[i].0.print_node();
    }

    graphs
}

fn dfs(graph: Vec<(Graph, usize)>) {
    let mut gp = graph;
    let mut nodes: Vec<usize> = Vec::new();
    let mut temp: Vec<usize> = Vec::new();

    gp[1].1 = 1;
    let mut curr = gp[1].0.get_first().clone();

    // print graph
    print!("{1}->");
    while let Some(val) = curr {
        nodes.insert(0,val.borrow().data);
        curr = val.borrow().next.clone();
```

```rust
    }

    // print dfs graph
    loop{
        if 0 == nodes.len() {
            break;
        }else{
            let data = nodes.pop().unwrap();
            if 0 == gp[data].1 { // Unvisited
                // Change state to visited
                gp[data].1 = 1;
                print!("{data}->");

                // Add node to temp and perform depth-first
                // search on it
                let mut curr = gp[data].0.get_first().clone();
                while let Some(val) = curr {
                    temp.push(val.borrow().data);
                    curr = val.borrow().next.clone();
                }

                while !temp.is_empty(){
                    nodes.push(temp.pop().unwrap());
                }
            }
        }
    }

    println!("");
}

fn main() {
    let data = [
      [1,2],[2,1],[1,3],[3,1],[2,4],[4,2],[2,5],
      [5,2],[3,6],[6,3],[3,7],[7,3],[4,5],[5,4],
      [6,7],[7,6],[5,8],[8,5],[6,8],[8,6]
    ];
    let gp = build_graph(data);
    dfs(gp);
}
```

Ниже приведён вывод, отображающий смежные узлы каждой вершины и самый глубокий путь.

```rust
[1]->[2][3]
[2]->[1][4][5]
[3]->[1][6][7]
[4]->[2][5]
[5]->[2][4][8]
[6]->[3][7][8]
[7]->[3][6]
[8]->[5][6]
1->2->4->5->8->6->3->7->
```

### 9.7.2 Analysis of DFS

Временная сложность поиска в глубину (DFS) может быть вычислена как с точки зрения вершин, так и с точки зрения рёбер. В `build_graph` каждая вершина должна быть обработана один раз для построения графа, что даёт сложность O(V). Во время поиска DFS начинается с некоторой вершины и исследует все смежные вершины как можно глубже, обрабатывая каждое ребро с временной сложностью O(E). Следовательно, общая временная сложность DFS равна O(V + E). Если во время DFS все вершины образуют цепочку, то самый глубокий поиск будет включать все узлы, что даёт пространственную сложность O(V). Важно отметить, что деревья являются частным случаем графов. Поэтому алгоритмы поиска в глубину и поиска в ширину для графов могут также использоваться для поиска в деревьях. Поиск в ширину, который был рассмотрен в главе о деревьях, на самом деле представляет собой обход по уровням. DFS и BFS являются основой для многих других важных алгоритмов обработки графов, что делает их необходимыми для поиска в графах. В следующих разделах будут использоваться BFS и DFS графа для решения практических задач, чтобы углубить понимание.

### 9.7.3 Topological Sorting

Задачи реального мира часто могут быть смоделированы в виде графов и решены с помощью алгоритмов обработки графов. Например, рассмотрим задачу составления четырёхлетнего учебного плана для специальности, которая включает обеспечение правильных зависимостей между курсами и допустимой последовательности курсов. Эта задача может быть сложной, но с использованием структуры данных «граф» её можно решить с помощью алгоритмов обработки графов. Предположим, у нас есть четыре курса с зависимостями, показанными на графе; допустимый порядок изучения курсов — [functions, derivatives, systems of equations, calculus, linear algebra, probability theory, convolutional neural networks]. Чтобы определить порядок курсов, можно использовать алгоритм сортировки зависимостей между курсами, который известен как топологическая сортировка.

![Figure 9.5: Courses Topological Relationship](images/fig-9.5.png)

*Figure 9.5: Courses Topological Relationship*

Топологическая сортировка — это вариант поиска в глубину, который создаёт линейное упорядочение всех вершин ориентированного ациклического графа (DAG). Полученный порядок может использоваться для указания приоритетов событий, составления расписаний проектов, генерации графов приоритетов для запросов к базе данных и так далее. Основные идеи топологической сортировки заключаются в следующем:

- Вызвать `dfs()` для графа g с использованием поиска в глубину, чтобы найти подходящие вершины.
- Сохранить вершины в стеке так, чтобы последняя из них оказалась на дне.
- Вернуть данные из стека как результат топологической сортировки.

Следуя этим шагам, можно преобразовать граф в линейное отношение, например упомянутый выше учебный план, который может быть преобразован в топологическую последовательность.

![Figure 9.6: Course sheduling](images/fig-9.6.png)

*Figure 9.6: Course sheduling*

Итоговый результат топологической сортировки представлен ниже. Курсы одного цвета можно проходить в любом порядке, а курсы разных цветов — только в порядке, заданном топологической сортировкой.

![Figure 9.7: Topological sequence of course sheduling](images/fig-9.7.png)

*Figure 9.7: Topological sequence of course sheduling*

Для реализации алгоритма обработки графа для составления расписания курсов сначала определим перечисление цветов, представляющее состояние исследования узла.

```rust
// course_topological_sort.rs
use std::collections::HashMap;
use std::hash::Hash;
use std::fmt::Display;

// Color enum used to determine if a node has been searched
#[derive(Debug, Clone, PartialEq)]
enum Color {
    White, // White: not yet explored
    Gray, // Gray: currently being explored
    Black, // Black: exploration complete
}
```

Затем определяются узел и граф, как это уже не раз делалось ранее.

```rust
// course_topological_sort.rs

// course vertex definition
#[derive(Debug, Clone)]
struct Vertex<T> {
    key: T,
    color: Color,
    neighbors: Vec<T>,
}
```

```rust
impl<T: PartialEq + Clone> Vertex<T> {
    fn new(key: T) -> Self {
        Self {
            key: key,
            color: Color::White,
            neighbors: Vec::new(),
        }
    }

    fn add_neighbor(&mut self, nbr: T) {
        self.neighbors.push(nbr);
    }
}

// couses relation graph definition
#[derive(Debug, Clone)]
struct Graph<T> {
    vertnums: u32,
    edgenums: u32,
    vertices: HashMap<T, Vertex<T>>, // all vertex
    edges: HashMap<T, Vec<T>>, // all edges
}

impl<T: Eq + PartialEq + Clone + Hash> Graph<T> {
    fn new() -> Self {
        Self {
            vertnums: 0,
            edgenums: 0,
            vertices: HashMap::<T, Vertex<T>>::new(),
            edges: HashMap::<T, Vec<T>>::new(),
        }
    }

    fn add_vertex(&mut self, key: &T) -> Option<Vertex<T>> {
        let vertex = Vertex::new(key.clone());
        self.vertnums += 1;
        self.vertices.insert(key.clone(), vertex)
    }

    fn add_edge(&mut self, src: &T, des: &T) {
        if !self.vertices.contains_key(src) {
          let _sv = self.add_vertex(src);
        }

        if !self.vertices.contains_key(des) {
          let _dv = self.add_vertex(des);
        }

        // add vertex
        self.edgenums += 1;
        self.vertices.get_mut(src)
                     .unwrap()
```

```rust
                     .add_neighbor(des.clone());

        // add edge
        if !self.edges.contains_key(src) {
            let _eg = self.edges
                          .insert(src.clone(), Vec::new());
        }

        self.edges.get_mut(src).unwrap().push(des.clone());
    }
}
```

Когда граф построен, можно приступать к созданию графа зависимостей курсов. При исследовании всех узлов-курсов в графе используется атрибут цвета, чтобы указать, был ли узел посещён. Переменная schedule хранит результат топологической сортировки курсов. Чтобы предотвратить ошибки планирования, такие как циклические зависимости, здесь добавлена переменная "has_circle" для управления процессом поиска. При обнаружении цикла программа завершается, указывая на то, что входные данные некорректны.

```rust
// course_topological_sort.rs

// Build the course dependency graph.
fn build_course_graph<T>(pre_requisites:Vec<Vec<T>>)->Graph<T>
    where T: Eq + PartialEq + Clone + Hash
{
    // Create edge relationships for dependent courses.
    let mut course_graph = Graph::new();
    for v in pre_requisites.iter() {
        let prev = v.first().unwrap();
        let last = v.last().unwrap();
        course_graph.add_edge(prev, last);
    }

    course_graph
}

// Course scheduling.
fn course_scheduling<T>(
    cg: &mut Graph<T>,
    course: Vertex<T>,
    schedule: &mut Vec<String>,
    mut has_circle: bool)
where T: Eq + PartialEq + Clone + Hash + Display
{
    // Clone to prevent conflicts with mutable references.
    let edges = cg.edges.clone();

    // Explore dependent courses.
    let dependencies = edges.get(&course.key);

    if !dependencies.is_none() {
        for dep in dependencies.unwrap().iter() {
            let course = cg.vertices.get(dep)
                                    .unwrap().clone();
```

```rust
            if Color::White == course.color {
                cg.vertices.get_mut(dep)
                           .unwrap()
                           .color = Color::Gray;

                course_scheduling(cg, course,
                                  schedule, has_circle);

                // Exit when encountering a cycle.
                if has_circle {
                    return;
                }
            } else if Color::Gray == course.color {
                has_circle = true;
                return;
            }
        }
    }

    // Change node color and add to schedule.
    cg.vertices.get_mut(&course.key)
               .unwrap()
               .color = Color::Black;
    schedule.push(course.key.to_string());
}

fn find_topological_order<T>(
    course_num: usize,
    pre_requisites: Vec<Vec<T>>)
where T: Eq + PartialEq + Clone + Hash + Display
{
    // Build the course dependency graph.
    let mut cg = build_course_graph(pre_requisites);

    // Get all course nodes into "courses".
    let vertices = cg.vertices.clone();
    let mut courses = Vec::new();
    for key in vertices.keys() {
        courses.push(key);
    }

    // Save feasible course schedules.
    let mut schedule = Vec::new();

    // Determine if there is a cycle.
    let has_circle = false;

    // Perform topological sorting of courses.
    for i in 0..course_num {
        let course = cg.vertices.get(&courses[i])
                                .unwrap()
                                .clone();
```

```rust
        // Only explore courses that are not explored
        // and do not have cycles.
        if !has_circle && Color::White == course.color {
            // Change the color of the course node to indicate
            // that it is currently being explored.
            cg.vertices.get_mut(&courses[i])
                       .unwrap()
                       .color = Color::Gray;

            course_scheduling(&mut cg, course,
                              &mut schedule, has_circle);
        }
    }

    if !has_circle {
        println!("{:#?}", schedule);
    }
}

fn main() {
    let course_num = 7;

    // Build course dependency relationships.
    let mut pre_requisites = Vec::<Vec<&str>>::new();
    pre_requisites.push(vec!["calculus", "function"]);
    pre_requisites.push(vec!["calculus", "derivation"]);
    pre_requisites.push(vec!["linear algebra", "equation"]);
    pre_requisites.push(vec!["CNN", "calculus"]);
    pre_requisites.push(vec!["CNN", "probalility thery"]);
    pre_requisites.push(vec!["CNN", "linear algebra"]);

    // Find the topological sorting result, which is a
    // reasonable course learning order.
    find_topological_order(course_num, pre_requisites);
}
```

Here is a feasible course learning order.

```text
[
    "function",
    "derivation",
    "calculus",
    "equation",
    "linear algebra",
    "probability theory",
    "CNN",
]
```

Помимо выбора курсов, приготовление пищи также можно абстрагировать как топологическую сортировку. Например, рассмотрим приготовление блинов, как показано на рисунке ниже. Рецепт прост: 1 яйцо, 1 чашка блинной смеси, 1 столовая ложка масла и 3/4 чашки молока. Чтобы приготовить блины, сначала необходимо включить плиту и разогреть сковороду. Затем ложкой смешать все ингредиенты и вылить смесь на сковороду. Когда

начинают образовываться пузырьки, перевернуть блин и обжарить его с обеих сторон до золотистой корочки. Перед едой можно добавить соус.

![Figure 9.8: Pancake Cooking](images/fig-9.8.png)

*Figure 9.8: Pancake Cooking*

С помощью алгоритма топологической сортировки приведённый выше рисунок можно упростить до стандартной схемы этапов приготовления. На этой схеме этапы одного цвета можно выполнять в любом порядке. Такая схема этапов может помочь начинающим кулинарам успешно приготовить блины. Однако сделать их вкусными — это уже совсем другое дело.

![Figure 9.9: Pancake cooking process topological relationship](images/fig-9.9.png)

*Figure 9.9: Pancake cooking process topological relationship*

И приготовление пищи, и выбор курсов могут быть абстрагированы как организация процессов, и поэтому теоретически один и тот же код может использоваться для работы с ними. Реализация алгоритма топологической сортировки процесса приготовления пищи совпадает с алгоритмом топологической сортировки для планирования курсов. Поэтому большая часть кода здесь приводиться не будет, но её можно найти в файлах исходного кода этой книги.

```rust
// cooking_topological_sort.rs

// Implementation omitted as it is identical to
// course_topological_sort
fn main() {
    let operation_num = 9;
```

```rust
    // constructe a cooking process dependency relationship
    let mut pre_requisites = Vec::<Vec<&str>>::new();
    pre_requisites.push(vec!["Mix", "3/4 cup of milk"]);
    pre_requisites.push(vec!["Mix", "1 egg"]);
    pre_requisites.push(vec!["Mix", "1 tablespoon olive oil"]);
    pre_requisites.push(vec!["Pour in 1/4 cup", "Mix"]);
    pre_requisites.push(vec!["Pour in 1/4 cup",
                             "Heat the pan"]);
    pre_requisites.push(vec!["Flip the bottom until golden",
                             "Pour in 1/4 cup"]);
    pre_requisites.push(vec!["Enjoy",
                             "Flip the bottom until golden"]);
    pre_requisites.push(vec!["Enjoy", "Heat the sauce"]);

    // Find a feasible topological result
    // which is a reasonable cooking order
    find_topological_order(operation_num, pre_requisites);
}
```

Here are two feasible cooking sequences.

```text
[
    "3/4 cup of milk",
    "1 egg",
    "1 tablespoon olive oil",
    "Mix",
    "Heat the pan",
    "Pour in 1/4 cup",
    "Flip the bottom until golden",
    "Heat the sauce",
    "Enjoy",
]
[
    "Heat the pan",
    "3/4 cup of milk",
    "1 egg",
    "1 tablespoon olive oil",
    "Mix",
    "Pour in 1/4 cup",
    "Flip the bottom until golden",
    "Heat the sauce",
    "Enjoy",
]
```

## 9.8 Компоненты сильной связности

Крупные графы, такие как связи между веб-страницами, обычно представляют в виде графов, а поисковые системы, например Google, используют огромные ориентированные графы для хранения ссылок во Всемирной паутине. В графе такого типа страницы являются вершинами, а гиперссылки — рёбрами, соединяющими их. На рисунке 9.10 изображены веб-страницы, связанные с главным сайтом Google, что показывает: весь интернет можно рассматривать как граф.

![Рисунок 9.10: Связи в интернете](images/fig-9.10.png)

*Рисунок 9.10: Связи в интернете*

Одна из заметных особенностей таких графов состоит в том, что у некоторых вершин исключительно много рёбер. Например, Google связан почти с каждым сайтом в мире, а у таких сайтов, как Baidu и Tencent, множество ссылок внутри Китая. Однако у многих вершин очень мало рёбер или всего одно, и они образуют кластеры связанных между собой узлов. Такие кластеры называют компонентами связности, а если компоненту связности можно достичь из любой её вершины за конечное число шагов, её называют компонентой сильной связности. Ориентированный граф сильно связен тогда и только тогда, когда любые две его вершины взаимно достижимы. Сильно связные графы похожи на вложенные циклы и должны содержать циклы. Ориентированный граф может содержать несколько компонент сильной связности, и каждая из этих компонент называется компонентой сильной связности. На рисунке 9.11 показан пример компонент сильной связности в ориентированном графе.

![Рисунок 9.11: Компоненты сильной связности и их упрощение](images/fig-9.11.png)

*Рисунок 9.11: Компоненты сильной связности и их упрощение*

Компоненты сильной связности C ∈ G, в которых вершины v и w связаны, можно представить точкой в упрощённом графе (показаны в трёхцветных областях слева). Для выявления компонент сильной связности обычно применяется алгоритм Тарьяна, основанный на поиске в глубину. Применение алгоритма поиска компонент сильной связности к связному графу даёт три дерева, которые соответствуют трём компонентам связности, как показано на рисунке ниже. Независимая область C

состоит только из самой себя как узла, тогда как F, L и H образуют одну компоненту связности, а A, E, G, D и B — другую компоненту связности. Три дерева, полученных алгоритмом поиска компонент сильной связности, представляют три компоненты связности. Перенося задачу с уровня узлов на уровень компонент связности, алгоритм упрощает её и облегчает последующий анализ и обработку.

C A E F G B L D H

### 9.8.1 Алгоритм компонент сильной связности на основе BFS

Задача о разделении на провинции — пример задачи о компонентах сильной связности. В Китае города распределены по провинциальным административным регионам. Для решения этой задачи предоставляется большой объём информации о городах и связях между ними, а алгоритм применяется, чтобы разбить города на группы и определить число провинций, к которым эти города относятся. Предположим, имеется n городов, часть которых связана друг с другом, а часть — нет: Chengdu и Yibin относятся к провинции Сычуань, поэтому связь между ними можно представить как [«Chengdu», «Yibin»] и [«Yibin», «Chengdu»]. Другой пример — [«Guangzhou», «Shenzhen»], [«Guangzhou», «Dongguan»]... Здесь города абстрагируются как точки графа, а связи рассматриваются как рёбра. Число провинций можно определить, найдя количество компонент сильной связности, что можно сделать с помощью алгоритма поиска в ширину. Изначально цвет каждого узла-города в графе белый, а при посещении он окрашивается в серый. Поиск в ширину начинается с этого города и продолжается, пока не будут посещены (окрашены в серый) все города одной компоненты связности, что означает одну провинцию. Обойдя все компоненты связности городов, можно найти все провинции. В случае задачи о разделении на провинции ответ должен быть равен 2 — числу провинций. Ниже приведена реализация алгоритма поиска компонент сильной связности с использованием поиска в ширину. Она содержит только самые базовые функции для реализации точки и графа, а неиспользуемые функции удалены. Переменная edges в определении графа хранит все связи между рёбрами для исследования отношений между рёбрами.

```rust
// find_province_num_bfs.rs

use std::collections::HashMap;
use std::hash::Hash;

// Enum for colors
#[derive(Debug, Clone, PartialEq)]
```

```rust
enum Color {
    White, // White: not yet explored
    Gray, // Gray: currently being explored
}

// Definition of cities
#[derive(Debug, Clone)]
struct Vertex<T> {
    key: T,
    color: Color,
    neighbors: Vec<T>,
}
impl<T: PartialEq + Clone> Vertex<T> {
    fn new(key: T) -> Self {
        Self {
            key: key,
            color: Color::White,
            neighbors: Vec::new(),
        }
    }

    fn add_neighbor(&mut self, nbr: T) {
        self.neighbors.push(nbr);
    }

    fn get_neighbors(&self) -> Vec<&T> {
        let mut neighbors = Vec::new();
        for nbr in self.neighbors.iter() {
            neighbors.push(nbr);
        }
        neighbors
    }
}

// Definition of province
#[derive(Debug, Clone)]
struct Graph<T> {
    vertnums: u32,
    edgenums: u32,
    vertices: HashMap<T, Vertex<T>>,
    edges: HashMap<T, Vec<T>>,
}

impl<T: Eq + PartialEq + Clone + Hash> Graph<T> {
    fn new() -> Self {
        Self {
            vertnums: 0,
            edgenums: 0,
            vertices: HashMap::<T, Vertex<T>>::new(),
            edges: HashMap::<T, Vec<T>>::new(),
        }
    }
```

```rust
    fn add_vertex(&mut self, key: &T) -> Option<Vertex<T>> {
        let vertex = Vertex::new(key.clone());
        self.vertnums += 1;
        self.vertices.insert(key.clone(), vertex)
    }

    fn add_edge(&mut self, src: &T, des: &T) {
        if !self.vertices.contains_key(src) {
          let _fv = self.add_vertex(src);
        }
        if !self.vertices.contains_key(des) {
          let _tv = self.add_vertex(des);
        }

        // add a vertex (city)
        self.edgenums += 1;
        self.vertices.get_mut(src)
                     .unwrap()
                     .add_neighbor(des.clone());
        // add an edge
        if !self.edges.contains_key(src) {
            let _ = self.edges.insert(src.clone(), Vec::new());
        }
        self.edges.get_mut(src).unwrap().push(des.clone());
    }
}
```

Имея определения графа и узла, можно построить граф связей между городами. Мы последовательно меняем цвет каждого города на серый, пока группа городов не будет полностью исследована; в этот момент мы находим компоненту сильной связности, то есть провинцию.

```rust
// find_province_num_bfs.rs

/ Build the city connection graph
fn build_city_graph<T>(connected: Vec<Vec<T>>) -> Graph<T>
    where T: Eq + PartialEq + Clone + Hash {
    // Set edges between nodes with relationships
    let mut city_graph = Graph::new();
    for v in connected.iter() {
        let src = v.first().unwrap();
        let des = v.last().unwrap();
        city_graph.add_edge(src, des);
    }

    city_graph
}

fn find_province_num_bfs<T>(connected: Vec<Vec<T>>) -> u32
    where T: Eq + PartialEq + Clone + Hash {
    let mut cg = build_city_graph(connected);

    // Get keys of all main city nodes
```

```rust
    let mut cities = Vec::new();
    for key in cg.edges.keys() { cities.push(key.clone()); }

    // Process each strongly connected component
    let mut province_num = 0;
    let mut q = Queue::new(cities.len());
    for ct in &cities {
        let city = cg.vertices.get(ct).unwrap().clone();
        if Color::White == city.color {
            // Change the current nodet's color and enqueue it
            cg.vertices.get_mut(ct)
                       .unwrap()
                       .color = Color::Gray;
            q.enqueue(city);
            // Process a strongly connected component
            // of a province
            while !q.is_empty() {
                // Get a node and its neighbors
                let q_city = q.dequeue().unwrap();
                let nbrs = q_city.get_neighbors();
                // Process each neighbor
                for nbr in nbrs {
                    let nbrc = cg.vertices.get(nbr)
                                          .unwrap()
                                          .clone();
                    if Color::White == nbrc.color {
                        // Enqueue the unexplored nodes
                        cg.vertices.get_mut(nbr)
                                   .unwrap()
                                   .color = Color::Gray;
                        q.enqueue(nbrc);
                    }
                }
            }
            // Finish processing a strongly connected component
            // of a province
            province_num += 1;
        }
    }

    province_num
}
fn main() {
    // Build the city dependency relationship
    let mut connected = Vec::<Vec<&str>>::new();
    connected.push(vec!["Chengdu", "Zigong"]);
    connected.push(vec!["Chengdu", "Mianyang"]);
    connected.push(vec!["Chengdu", "Deyang"]);
    connected.push(vec!["Chengdu", "Luzhou"]);
    connected.push(vec!["Chengdu", "Neijiang"]);
    connected.push(vec!["Chengdu", "Leshan"]);
```

```rust
    connected.push(vec!["Chengdu", "Yibin"]);
    connected.push(vec!["Zigong", "Chengdu"]);

    connected.push(vec!["Guangzhou", "Shenzhen"]);
    connected.push(vec!["Guangzhou", "Dongguan"]);
    connected.push(vec!["Guangzhou", "Zhuhai"]);
    connected.push(vec!["Guangzhou", "Zhongshan"]);
    connected.push(vec!["Guangzhou", "Shantou"]);
    connected.push(vec!["Guangzhou", "Foshan"]);
    connected.push(vec!["Guangzhou", "Zhanjiang"]);
    connected.push(vec!["Shenzhen", "Guangzhou"]);

    connected.push(vec!["Wuhan", "Jingzhou"]);
    connected.push(vec!["Wuhan", "Yichang"]);
    connected.push(vec!["Wuhan", "Xiangyang"]);
    connected.push(vec!["Wuhan", "Jingmen"]);
    connected.push(vec!["Wuhan", "Xiaogan"]);
    connected.push(vec!["Wuhan", "Huanggang"]);
    connected.push(vec!["Jingzhou", "Wuhan"]);

    // Find all strongly connected components, there are three
    // provinces: Sichuan, Guangdong, and Hubei
    let province_num = find_province_num_bfs(connected);
    println!("province number: {province_num}");
    // province number: 3
}
```

Временная сложность этого алгоритма — O(n²), поскольку нужно обработать n узлов-городов, и каждый узел-город может быть связан со всеми остальными городами графа (когда провинция только одна). Поиск в ширину использует очередь, которая может содержать до n узлов-городов, поэтому пространственная сложность — O(n).

### 9.8.2 Алгоритм компонент сильной связности на основе DFS

Задачу о разделении на провинции можно также решить с помощью алгоритма поиска в глубину. Идея поиска в глубину состоит в обходе всех узлов-городов: для каждого города, если он ещё не посещён (окрашен в белый), цвет меняется на серый, после чего из этого города запускается поиск в глубину. С помощью алгоритма поиска в глубину можно получить города, непосредственно связанные с данным городом. Эти города и сам город принадлежат одной компоненте связности. Можно продолжать поиск в глубину по этим городам, пока не будут посещены (окрашены в серый) все города одной компоненты связности, что означает, что провинция найдена. Обход всех городов позволяет получить общее число компонент связности, то есть общее число провинций.

```rust
// find_province_num_dfs.rs
use std::collections::HashMap;
use std::hash::Hash;

// Implementation details omitted for brevity,
// please add them yourself

// Search for neighboring nodes of current node 'city'
fn search_city<T>(cg: &mut Graph<T>, city: Vertex<T>)
    where T: Eq + PartialEq + Clone + Hash
{
```

```rust
    // Traverse the neighboring nodes of current node 'city'
    for ct in city.get_neighbors() {
        let city = cg.vertices.get(ct).unwrap().clone();
        if Color::White == city.color {
            // Change the color of current node
            cg.vertices.get_mut(ct)
                       .unwrap()
                       .color = Color::Gray;
            // Continue to search for neighboring nodes
            search_city(cg, city);
        }
    }
}

fn find_province_num_dfs<T>(city_connected: Vec<Vec<T>>) -> u32
    where T: Eq + PartialEq + Clone + Hash
{
    let mut cg = build_city_graph(city_connected);
    let mut cities = Vec::new();

    // Get the key of each main city node
    for key in cg.edges.keys() { cities.push(key.clone()); }

    let mut province_num = 0;
    // Process connected components of a province one by one
    for ct in &cities {
        let city = cg.vertices.get(ct).unwrap().clone();
        if Color::White == city.color {
            // Change the color of current node
            cg.vertices.get_mut(ct)
                       .unwrap()
                       .color = Color::Gray;
            // Search for neighboring nodes of current node
            search_city(&mut cg, city);
            // Finish processing a province connected component
            province_num += 1;
        }
    }

    province_num
}

fn main() {
    // Build city dependency relationship

    let mut city_connected = Vec::<Vec<String>>::new();

    // Same as in BFS, omitted for brevity
    let province_num = find_province_num_dfs(city_connected);
    println!("province nummber: {province_num}");
    // province nummber: 3
}
```

По сложности алгоритм аналогичен BFS, поскольку также требует обработать n узлов-городов, и каждый узел-город может быть связан со всеми остальными городами графа (когда провинция только одна). Поэтому временная сложность по-прежнему O(n²). Поиск в глубину использует стек, который может содержать до n узлов-городов, поэтому пространственная сложность — O(n).

## 9.9 Задача о кратчайшем пути

При обращении к сетевым ресурсам — например, при просмотре видео, отправке электронной почты или входе в лабораторный компьютер из-за пределов кампуса — требуется сетевое взаимодействие. Понимание того, как информация передаётся от одного компьютера к другому через интернет, — фундаментальный аспект компьютерных сетей.

Оборудование A Оборудование C Маршрутизатор B Маршрутизатор A Интернет Оборудование B Оборудование D

На схеме выше показан процесс интернет-взаимодействия. Когда пользователь запрашивает веб-страницу с сервера с помощью браузера, запрос сначала проходит через локальную сеть, а затем через маршрутизатор выходит в интернет. Далее запрос распространяется по интернету, пока не достигнет маршрутизатора локальной сети, в которой расположен сервер. Запрошенная веб-страница затем отправляется обратно в браузер пользователя через тот же маршрутизатор. Команда tracepath позволяет определить путь от компьютера пользователя до конкретного канала связи. Например, при трассировке сайта xxx.cn путь может проходить через 13 маршрутизаторов, причём первые два из них — шлюзовые маршрутизаторы сетевой группы пользователя.

```text
 1?: [LOCALHOST]
                                      pmtu 1500
 1:
     _gateway
                                      4.523 ms
 1:
     _gateway
                                      3.495 ms
 2:
     10.253.0.22
                                      2.981 ms
 3:
     no response
 4:
     ???
                                      6.166 ms
 5:
     202.115.254.237
                                    558.609 ms
 6:
     no response
 7:
     no response
 8:
     101.4.117.54
                                     48.822 ms asymm 16
 9:
     no response
10:
     101.4.112.37
                                     48.171 ms asymm 14
11:
     no response
12:
     101.4.114.74
                                     44.981 ms
13:
     202.97.15.89
                                     49.560 ms
```

Каждый маршрутизатор в интернете соединён с одним или несколькими другими маршрутизаторами. Поэтому запуск tracepath в разное время суток может давать разные результаты, поскольку стоимость соединений между маршрутизаторами меняется в зависимости от загрузки сети. Сетевые соединения можно рассматривать как взвешенный граф, в котором веса соединений подстраиваются под текущую ситуацию в сети. Цель — найти путь с минимальным суммарным весом для передачи сообщения. Эта задача аналогична задаче о цепочке слов, рассмотренной ранее, поскольку в обоих случаях требуется найти минимальное значение, однако в задаче о цепочке слов все веса одинаковы.

### 9.9.1 Алгоритм Дейкстры

Предшественники предложили различные алгоритмы для исследования кратчайшего пути в сетевых графах, и среди них алгоритм Дейкстры является хорошим выбором. Это жадный итеративный алгоритм, который находит кратчайший путь от заданного начального узла до всех остальных узлов графа — подобно поиску в ширину.

![Рисунок 9.12: Дейкстра](images/fig-9.12.png)

*Рисунок 9.12: Дейкстра*

На рисунке выше требуется найти кратчайший путь от V1 до V7. При визуальном изучении графа видно, что существует два кратчайших пути: [V1->V4->V3->V2->V6->V5->V7] и [V1->V4>V3->V5->V7], причём кратчайшее расстояние равно 38. Если вычислять его алгоритмом Дейкстры, придётся отслеживать и вычислять различные расстояния, а затем складывать их. Чтобы отслеживать суммарное расстояние от начального узла до каждого целевого узла, мы воспользуемся переменной экземпляра `dist` в вершине графа. Эта переменная содержит суммарный вес пути от начала до целевого узла. Алгоритм Дейкстры перебирает каждый узел графа, причём порядок обхода задаётся очередью с приоритетом, а значение `dist` используется для определения порядка объектов в очереди. Когда узел создаётся впервые, `dist` устанавливается в 0. Теоретически можно задать `dist` равной бесконечности, но на практике достаточно установить её в 0 либо в значение, превышающее любое реальное расстояние, — например, равное расстоянию, которое свет проходит за секунду, то есть примерно расстоянию между Землёй и Луной, поскольку никакие две точки Земли не находятся так далеко друг от друга.

### 9.9.2 Реализация алгоритма Дейкстры

Алгоритм Дейкстры — это инкрементальный подход к поиску кратчайшего пути шаг за шагом, использующий очередь с приоритетом для обработки вершин по значению их приоритета. Алгоритм выбирает ближайшую непосещённую вершину к начальной точке среди всех вершин, для которых кратчайший путь ещё не найден, и продолжает процесс. Однако применение этого алгоритма в интернете создаёт сложности, поскольку он требует полного представления всей сети в виде графа. Это означает, что каждому маршрутизатору нужна карта всех маршрутизаторов интернета, что непрактично.

```rust
// dijkstra.rs

use std::cmp::Ordering;
use std::collections::{BinaryHeap, HashMap, HashSet};

#[derive(Debug, Copy, Clone, PartialEq, Eq, Hash)]
struct Vertex<'a> {
    name: &'a str,
}
```

```rust
impl<'a> Vertex<'a> {
    fn new(name: &'a str) -> Vertex<'a> {
        Vertex {
            name
        }
    }
}

// Vertices visited
#[derive(Debug)]
struct Visited<V> {
    vertex: V,
    distance: usize,
}

// Add total ordering functionality to Visited
impl<V> Ord for Visited<V> {
    fn cmp(&self, other: &Self) -> Ordering {
        other.distance.cmp(&self.distance)
    }
}
impl<V> PartialOrd for Visited<V> {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl<V> Eq for Visited<V> {}
impl<V> PartialEq for Visited<V> {
    fn eq(&self, other: &Self) -> bool {
        self.distance.eq(&other.distance)
    }
}

// Shortest path algorithm
fn dijkstra<'a>(
    start: Vertex<'a>,
    adj_list: &HashMap<Vertex<'a>,
    Vec<(Vertex<'a>, usize)>>) -> HashMap<Vertex<'a>, usize>
{
    let mut distances = HashMap::new();
    let mut visited = HashSet::new(); // Visited vertices
    let mut to_visit = BinaryHeap::new(); // Unvisited vertices

    // Set the starting point and
    // initial distances to all points
    distances.insert(start, 0);
    to_visit.push(Visited {
        vertex: start,
        distance: 0,
    });
```

```rust
    while let Some(Visited { vertex, distance }) =
        to_visit.pop() {
        // If visited, continue with the next point
        if !visited.insert(vertex) { continue; }

        if let Some(nbrs) = adj_list.get(&vertex) {
            for (nbr, cost) in nbrs {
                let new_dist = distance + cost;
                let is_shorter =
                  distances.get(&nbr)
                           .map_or(true,
                              |&curr| new_dist < curr);
                // If the distance is shorter, insert the new
                // distance and neighbor
                if is_shorter {
                    distances.insert(*nbr, new_dist);
                    to_visit.push(Visited {
                        vertex: *nbr,
                        distance: new_dist,
                    });
                }
            }
        }
    }

    distances
}

fn main() {
    let v1 = Vertex::new("V1");
    let v2 = Vertex::new("V2");
    let v3 = Vertex::new("V3");
    let v4 = Vertex::new("V4");
    let v5 = Vertex::new("V5");
    let v6 = Vertex::new("V6");
    let v7 = Vertex::new("V7");

    let mut adj_list = HashMap::new();
    adj_list.insert(v1, vec![(v4, 7), (v2, 13)]);
    adj_list.insert(v2, vec![(v6, 5)]);
    adj_list.insert(v3, vec![(v2, 3), (v6, 9), (v5, 10)]);
    adj_list.insert(v4, vec![(v3, 1), (v5, 14)]);
    adj_list.insert(v5, vec![(v7, 20)]);
    adj_list.insert(v6, vec![(v5, 2), (v7, 30)]);

    // Find the shortest path from V1 to any point
    let distances = dijkstra(v1, &adj_list);
    for (v, d) in &distances {
        println!("{}-{}, min distance: {d}", v1.name, v.name);
    }
}
```

Приведённый ниже вывод содержит кратчайшие расстояния от V1 до любой точки (включая её саму).

```text
V1-V5, min distance: 18
V1-V2, min distance: 11
V1-V6, min distance: 16
V1-V3, min distance: 8
V1-V7, min distance: 38
V1-V1, min distance: 0
V1-V4, min distance: 7
```

Для решения этой задачи при передаче сетевой информации применяются и другие алгоритмы, например протокол маршрутизации по вектору расстояний [15] и протокол маршрутизации по состоянию каналов [16]. Эти алгоритмы позволяют маршрутизаторам обнаруживать карты сети, сохранённые другими маршрутизаторами и содержащие сведения о взаимосвязанных узлах. Такой подход допускает обновление содержимого карты сети в реальном времени и является более эффективным, существенно снижая требования к пропускной способности сети.

### 9.9.3 Анализ алгоритма Дейкстры

Проанализируем временную сложность алгоритма Дейкстры. Прежде всего, построение очереди с приоритетом занимает O(V ) времени. После того как очередь построена, цикл while выполняется по одному разу для каждой вершины. Поскольку вершины добавляются в начале, а удаляются только после этого, вызов pop в цикле занимает O(log V ) времени. Этот цикл вместе с вызовами pop можно считать O(V log V ). Цикл for выполняется по одному разу для каждого ребра графа, а вызов decrease_key занимает O(E log V ) времени. Следовательно, итоговая временная сложность равна O((V + E) log V ), а пространственная сложность — O(V ).

## 9.10 Итоги

В этой главе мы изучили абстрактный тип данных графов и способы его реализации. Графы широко используются в различных областях, таких как планирование учебных курсов, компьютерные сети, транспорт, компьютеры, графы знаний и базы данных. Графы можно использовать для решения многих задач, если удастся преобразовать исходную задачу в представление графа. Графы находят применение в следующих областях:

- Компоненты сильной связности можно использовать для упрощения графов.
- Поиск в глубину (DFS) можно использовать для исследования глубоких ветвей графа.
- Топологическая сортировка полезна для упорядочения сложных связей в графе.
- Алгоритм Дейкстры (Dijkstra) можно использовать для поиска кратчайшего пути в взвешенном графе.
- Поиск в ширину (BFS) можно использовать для поиска кратчайшего пути в невзвешенном графе.
