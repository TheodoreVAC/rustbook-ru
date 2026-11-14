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
