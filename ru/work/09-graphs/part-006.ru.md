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


