## 9.6 Breadth First Search(BFS)

The study of graphs and graph theory is a complex subject matter with various excellent algorithms developed for graph study. However, the Breadth-First Search (BFS) and Depth-First Search (DFS) algorithms are the most commonly used ones. In the case of the ladder problem, BFS is used to find the shortest path since graphs are non-linear and traditional binary and linear search algorithms cannot be used for this task.

fool pool foil foul cool searching queue pool foil foul cool

The BFS algorithm explores the edges in the graph to find all vertices in G(assuming the distance between points is 1) that have a path starting from a given vertex s. It does this by first finding all vertices that are one unit away from s, then all vertices that are two units away, and so on, until all vertices are found. The search is performed layer by layer, which is why it is called breadth-first search. The points connected to the starting vertex are considered as one layer, put into a queue first, and then the algorithm finds the next layer of connecting points for those in the queue and repeats the process until the search is complete. During the search, vertices can be colored to indicate their status. Initially, all vertices are white. As the search progresses, vertices connected to the current search vertex are set to gray. The algorithm checks each gray vertex, and if it is not the target value, it is set to black, and the search continues for white vertices connected to the gray vertex. This process continues until the search task is completed or the entire graph search is complete. This search method is similar to the garbage collection mechanism of some languages, such as the tricolor garbage collection in the Go language.

### 9.6.1 Implementing a BFS

To implement a simple BFS algorithm, we first need to create a graph. The specific form of the graph depends on the purpose of the algorithm. Here, we will demonstrate the BFS algorithm using a simple graph, where nodes contain data and a link to the next node. We will store only the first node and the link to the next node in the graph.

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

The code above shows the implementation of the graph. The following code uses this graph to implement the basic breadth-first search algorithm. The build_graph function constructs the graph and encapsulates it into a tuple, which is then saved to a vector. The second value of the tuple indicates whether the node has been visited, with 0 indicating not visited and 1 indicating visited.

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

The output of the code, which prints the adjacent nodes of each vertex and all vertices, is shown below.

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

This algorithm uses Vec as a queue to search for the shortest transformation path in a word ladder. In addition to printing the values of each node’s connections, it also prints all nodes in the order they are searched. To better represent node colors, an enum representing colors needs to be defined and node colors need to be updated accordingly. A distance value needs to be added to the node to represent the distance from the starting point in order to calculate the shortest distance.

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

The code above, providing a color and node, is more complex than the basic BFS algorithm. To add nodes to the queue, the Queue implementation from Chapter 4 is introduced. The graph definition for solving the word ladder problem includes the number of nodes, edges, and a hashMap for storing node values and their structs.

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

With this graph, a word ladder graph can be constructed by arranging the words according to their patterns.

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

The BFS algorithm is then used to search for the shortest path. Note that although three colors are defined, only white nodes will be added to the queue, so gray nodes can be set to black or left unset. This BFS function constructs the breadth-first search tree, and the search queue is emptied when the algorithm finds the result ”sage”.

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

During the search process, the breadth-first search tree is constructed, and the node coloring during the search process is shown in the figure. At the beginning, all nodes adjacent to ”fool”, including ”pool”, ”foil”, ”foul”, and ”cool”, are taken, and these nodes are added to the queue for searching.

fool pool foil foul cool poll searching queue poll foil foul cool

When bfs checks the node ”cool”, it finds that it is gray, indicating that there is a shorter path to ”cool”. When checking ”pool”, a new node ”poll” is added.

fool pool foil foul cool poll fail searching queue poll fail

The next vertex on the queue is ”foil”, and the only new node that can be added to the tree is ”fail”. When bfs continues to process the queue, the next two nodes do not add any new points to the queue.

fool pool foil foul cool poll fail pole pall pope pale page sale sage searching queue

Finally, the shortest path is the number of levels from ”fool” to ”sage”, which is 6 levels(shortest path is 6). Readers can test this code with different words.

### 9.6.2 Analysis of BFS

The time complexity of breadth-first search (BFS) depends on the number of vertices and edges in the graph. To create a graph in BFS, we need to process at least V vertices, resulting in a time complexity of O(V ). During the search, BFS processes one edge at a time, resulting in a time complexity of O(E). Thus, the total time complexity of BFS is O(V + E). If all vertices are connected to the starting node, the queue needs to store at least the number of graph nodes, leading to a space complexity of O(V ). Interestingly, a graph can also be seen as a polyhedron split open, and its vertex-edge-face count must satisfy Euler’s formula V −E + F = 2. By rearranging this formula, we get V + E = 2E −F + 2, which implies that the complexity of BFS is O(V +E) = O(2E −F +2). In the case of the word ladder graph(Figure 9.5.1), the vertex, edge, and face counts are 18, 14, and 6 respectively, and the formula is verified by substituting these values. Here, what I want to say is that the BFS algorithm for graphs seems to be extended to the geometric field which is a big inspiration for me.

### 9.6.3 The Knight’s Tour Problem

The Knight’s tour is a classic puzzle where a knight chess piece moves on a chessboard to visit every square exactly once, forming a tour. This problem has fascinated many people including players, mathematicians, and computer scientists for many years, and there are various algorithms to solve it. The graph search is the most straightforward solution, which requires two steps: representing the knight’s moves and finding a path of length rows × columns −1, where the starting square is not counted. An 8 × 8 chessboard has a maximum of 1.305 × 1035 possible tours. To represent the Knight’s tour problem as a graph, each square on the chessboard is represented as a node, and each legal move of the knight is represented as an edge in the graph. The knight is represented as a yellow square in the figure below.

20 23 21 22 24 21 23 15 16 17 18 19 15 19 12 10 13 11 12 14 5 9 3 1 5 7 9 6 8 movable vertices 0 3 1 2 4

To construct a complete graph of size n × n, the knight’s eight possible moves must be considered. By traversing the entire graph, a move list can be created for each position, all of which can be converted into edges in the graph.

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

Once all the movable edges of each node have been found, the Knight’s tour graph can be constructed.

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

The search algorithm used to solve the Knight’s tour problem is called depth-first search. While breadth-first search explores vertices on the same level as widely as possible, depth-first search explores multiple levels of the tree as deeply as possible. Various strategies can be employed using depth-first search to solve the problem. The first strategy prohibits nodes from being visited multiple times, while the second strategy allows nodes to be visited multiple times during tree construction. When the depthfirst search algorithm encounters a dead (i.e., a point with no movable points) end, it backtracks to the previous deepest point and continues the exploration.

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

The knight’s tour pathes can obtained using the knight_tour algorithm.

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

The knight’s tour problem can be solved using the recursive version of depth-first search algorithm called the knight_tour algorithm. This algorithm searches for a path of length 64, which is the number of squares on the chessboard. The algorithm explores the graph by moving to the next vertex until it reaches a dead end or exhausts the entire graph, and then backtracks. To track the visited vertices, depth-first search uses colors where unvisited vertices are white and visited vertices are gray. Backtracking occurs when the knight_tour function returns false, indicating that a dead end has been reached. Unlike breadth-first search, which uses a queue to track the next vertex to be visited, depth-first search is recursive and has an implicit stack that helps the algorithm backtrack.
