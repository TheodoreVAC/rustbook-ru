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
