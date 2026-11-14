# Graphs

## 9.1 Objectives

- Understand the concept and storage format of graphs.
- Implement several graph data structures in Rust.
- Learn two important graph search algorithms.
- Use graphs to solve various real-world problems.

## 9.2 What is Graph?

In the previous chapter, we discussed binary trees as a data structure, while this chapter focuses on graphs - a more generalized form of trees. Although trees can be viewed as simplified graphs or carefully selected graphs with certain constraints on their node relationships, graphs have no such limitations. While trees have a root node and a top-to-bottom direction, graphs lack both. Unlike trees, graphs can contain cycles. They consist of points, edges, and point-edge relationships, whereas trees consist of nodes and connections. The figure above illustrates a graph with multiple nodes and connections, which demonstrates the vertical and horizontal relationships between different items. For example, calculus and linear algebra have no direct connection, but they can jointly incubate neural networks, forming a horizontal relationship. Derivatives, on the other hand, contribute to the construction of calculus, which is a part of calculus, and this forms a vertical relationship.

Graphs are versatile data structures that can be used to represent various real-world phenomena, such as flight maps, social network graphs, and course planning graphs. In this chapter, we will learn about the concept and storage format of graphs, and how to implement them in Rust. We will also explore two essential graph search algorithms that can be applied to solve different problems. Research on graphs, their various applications, and algorithms belong to a specialized discipline called graph theory.

### 9.2.1 Vocabularies and Definitions of Graph

A graph is a more general form of a tree and is defined by the following concepts:

- Vertex (or node): an element of the graph that has a name, or key, and may have additional information, or payload.
- Edge: an element that connects two vertices and indicates a relationship between them. An edge can be unidirectional or bidirectional, and may have a weight, which represents a measure such as distance, cost, time, or closeness.
- Weight: a measure of an edge.

A graph can be represented as G = (V, E), where V is the set of vertices and E is the set of edges. The figure below shows an example of a weighted directed graph with a vertex set V = (V 0, V 1, V 2, V 2, V 4, V 5) and an edge set E consisting of various connections and their weights, with a total of 9 edges.

![Figure 9.1: Graph](images/fig-9.1.png)

*Figure 9.1: Graph*

In addition to vertices, edges, and weights, paths are used to represent the order of points. A path is a vertex sequence that represents the order of point connections, such as (v, w, x, y, z). Cyclic graphs, which have cycles, such as V 5−> V 2−> V 3−> V 5, may also exist. If there are no cycles in the graph, it is called an acyclic graph or DAG graph. Many important problems can be represented using DAG graphs.

## 9.3 Graph Storage Format

To store a non-linear graph in a linear storage device like computer memory, there are two commonly used methods: adjacency matrix and adjacency list. The adjacency matrix stores the nodes, edges, and weights of the graph in a two-dimensional matrix, which requires N 2 space for a graph with N nodes. However, this method may result in a large waste of space when the graph is sparse. In contrast, the adjacency list is similar to a hash table and saves all the edges related to each vertex by opening a chain for each vertex. Its storage space depends on the number of edges and is generally much smaller than N 2. Therefore, computers use adjacency lists to store graph data structures.

### 9.3.1 Adjacency Matrix

An adjacency matrix is a straightforward way to store a graph. In this method, the vertices of the graph are represented by the rows and columns of a two-dimensional matrix. The value stored at the intersection of row v and column w indicates the presence of an edge between vertex v and vertex w, with the value indicating the weight of the edge. When two vertices have an edge between them, they are called adjacent. The graph shown in (9.1) can be stored using an adjacency matrix.

![Figure 9.2: Adjacency matrix](images/fig-9.2.png)

*Figure 9.2: Adjacency matrix*

Although the adjacency matrix is easy to understand and analyze for small graphs, it suffers from the drawback of being very sparse. Most of the cells in the matrix are empty, leading to a significant waste of space. For a graph with N vertices, an adjacency matrix requires N 2 storage. Therefore, the adjacency matrix is not an efficient method to store large graphs.

### 9.3.2 Adjacency List

![Figure 9.3: Adjacency list](images/fig-9.3.png)

*Figure 9.3: Adjacency list*

An efficient way to save graphs is by using an adjacency list, as shown in the figure above. In this approach, an array stores all the vertices in the graph, and each vertex maintains a linked list that connects it to other vertices. By accessing the linked lists of various vertices, it is possible to know how many points it is connected to, which is similar to the chaining method used by HashMap to solve collisions. The adjacency list stores the linked points in a structure similar to HashMap because edges have weights, while arrays can only save vertices. Graphs implemented with adjacency lists are compact and have no memory waste. This structure is also very convenient for storage. The importance of basic data structures is evident here, and the HashMap implemented in previous chapters is useful for implementing adjacency lists.

## 9.4 The Graph Abstract Data Type

The graph abstract data type can be defined based on the basic definition of a graph. At the core of the graph are vertices and edges, and operations are defined around them. The following operations are defined for a graph:

- new(): Creates a new empty graph with no parameters and returns an empty graph.
- add_vertex(v): Adds a vertex with parameter v to the graph and has no return value.
- add_edge(fv,tv,w): Adds a weighted directed edge with parameters fv, tv, and w to the graph and has no return value.
- get_vertex(vk): Finds the vertex with key vk in the graph, requires parameter vk, and returns the vertex.
- get_vertices(): Returns a list of all vertices in the graph without parameters.
- vert_nums(): Returns the number of vertices in the graph without parameters.
- edge_nums(): Returns the number of edges in the graph without parameters.
- contains(vk): Checks whether the vertex is in the graph with parameter vk and returns a Boolean value.
- is_empty(): Checks whether the graph is empty without parameters and returns a Boolean value.

Assuming g is a newly created empty graph, the table below shows the results of various graph operations. [] stores vertices, and () stores edges, where the first two values are points and the third value is the edge weight, such as (1, 5, 2), which means that the edge weight between point 1 and point 5 is 2.

**Table 9.1: Operations on Graph**

| Operation | Graph value | Return value |
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

## 9.5 Implementing a Graph in Rust

To implement a graph based on an adjacency matrix in Rust, we need to first create vertices and edges, and then use a two-dimensional Vec to store the edge relationships.

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

We can represent edges using a Boolean value to indicate their existence, as they are simply relationships and do not need to be constructed as entities.

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

Therefore, the edge relationships can be implemented and stored in a two-dimensional Vec.

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

The follwing are outputs after execution.

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

Next, we will implement an adjacency list graph using HashMap. Since vertices are the core elements and edges are the relationships between vertices, we need to create a data structure Vertex to represent the vertex element. For Vertex, we need to define operations such as creating a new vertex, getting the value of the vertex itself, adding adjacent vertices, getting all adjacent vertices, and getting the weights of adjacent vertices. The neighbors variable is used to store all adjacent vertices of the current vertex.

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

Graph is a data structure used to implement graphs, which includes a HashMap that maps vertex names to vertex objects.

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

Using Graph, we can create the vertices V0-V5 and their edges as shown in the graph (9.1).

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

The following are outputs after execution.

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

### 9.5.1 The Word Ladder Problem

The graph data structure enables us to solve practical problems, such as the word ladder puzzle. In this puzzle, we must transform one word into another by changing one letter at a time, (FOOL -> SAGE), but the resulting word must exist in the dictionary. This game was invented by Lewis Carroll, the author of ”Alice’s Adventures in Wonderland,” in 1878. Multiple solutions exist for this problem, as shown in the word sequence below.

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

Our goal is to use graph algorithms to find the shortest path between the starting and ending words, as shown in column a of the figure above. To achieve this, we first convert the words into vertices and link together the words that can be transformed into each other. If two words differ by only one letter, we create a bidirectional edge between them, as shown in the figure below. Finally, we use a graph search algorithm to find the shortest path between the starting and ending vertices.

![Figure 9.4: The word ladder](images/fig-9.4.png)

*Figure 9.4: The word ladder*

To create a graph model for the word ladder problem, there are various methods available. When dealing with a list of words with the same length, a vertex can be created for each word in the list. To connect the words, each word in the list must be compared to the others. If two words being compared have only one letter different, an edge can be created between them in the graph. This method is feasible for small word lists, but for larger lists such as the CET-4 vocabulary list with 3000 words or the CET-6 list with 5000 words, the comparison is inefficient, requiring millions of comparisons. An alternative approach is to consider the letter positions of the words and group them based on similar patterns. This way, we can search for similar words at each position and group them together. For instance, if we remove the first letter of SOPE and keep the rest ”_OPE,” all four-letter words ending in ”OPE” should be connected to SOPE and collected into a set. The same process is used for ”S_PE” and all the words matching this pattern are collected. Finally, all the words matching this pattern are collected, as shown in the figure below.

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

This solution can be implemented using a HashMap. The set mentioned earlier stores words with the same pattern as keys in the HashMap, which stores similar sets of words. Once the word sets are established, the graph can be created. To start the graph, create a vertex for each word in the HashMap, and then create edges between all vertices found under the same key in the dictionary. Once the graph is implemented, the ladder search task can be completed.

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

## 9.7 Depth First Search(DFS)

The Knight’s Tour problem is a specific case of the depth-first search algorithm, which aims to create the deepest possible tree. Depth-first search is generally used to search graphs with multiple branches, with the goal of searching as deeply as possible, connecting as many nodes as possible, and branching when necessary. In some cases, depth-first search may create multiple trees, which are called a depthfirst forest. Like breadth-first search, depth-first search uses predecessor links to construct trees. To better understand depth-first search, the vertex class can be expanded with two variables indicating the start and end times of the node’s search, where the start time also indicates the number of steps before encountering the vertex, and the end time is the number of steps before the vertex is colored black. The following figure shows a small graph and the depth-first search algorithm applied to it. The thick lines indicate the edges checked, with the node on the other end of the edge already added to the depth-first tree. The search starts from vertex A, and since all vertices are colored at the start of the search, the algorithm randomly starts visiting vertex A. When visiting a vertex, the first step is to set its color to gray, indicating that the vertex is being explored, and to set the discovery time to 1. Since vertex A has two adjacent vertices (B and D), each vertex needs to be visited, and we visit adjacent vertices in alphabetical order.

A1/ B C D E F

Next, we visit vertex B, which is adjacent to vertices C and D. Vertex C leads us to the end of a branch, so it can be colored black, and the end time set to 4. Now, return to vertex B and continue explore D, which leads us to vertex E. Vertex E has two adjacent vertices, B and F. Since B is already colored black, we can skip it and visit Vertex F.

C3/ A1/ B2/ A1/ B2/ C D E F D E F C C A1/ B2/ A1/ B2/ 3/4 3/4 D5/ D5/ E6/ F7/ E F

Vertex F has only one adjacent vertex, C, already colored black, the algorithm has reached the end of the branch. Therefore, the algorithm must backtrack and continue to search until it encounters a gray vertex or exits.

C C3/ A1/ B2/ A1/ B2/ 3/4 D5/ E6/ F D5/ E F D E F 7/8 6/9 7/8 C C A1/ B2/ A1/ B 3/4 2/11 3/4 D E F D E F 5/10 6/9 7/8 5/10 6/9 7/8

Eventually, the algorithm bachtracks to original vertex and exits the search, obtaining the visited path: A →B →D →E →F.

C A B 1/12 2/11 3/4 D E F 5/10 6/9 7/8

### 9.7.1 Implementing a DFS

From the previous discussion and illustration, we can present a basic implementation of the depthfirst search algorithm that does not include color markings but implements essential exploration functionality.

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

Here is the output that displays the adjacent nodes of each vertex and the deepest path.

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

The time complexity of depth-first search (DFS) can be calculated from both the vertices and edges perspectives. In build_graph, each vertex needs to be processed once to construct the graph, resulting in a complexity of O(V ). During the search, DFS starts from a vertex and explores all adjacent vertices as deeply as possible, processing each edge with a time complexity of O(E). Therefore, the total time complexity of DFS is O(V + E). If all vertices form a chain during the DFS, the deepest search will include all nodes, resulting in a space complexity of O(V ). It is important to note that trees are a special case of graphs. Therefore, depth-first search and breadthfirst search algorithms for graphs can also be used for searching trees. The breadth-first search we learned in the chapter on trees is actually a level-order traversal. DFS and BFS are the foundation for many other important graph algorithms, making them essential for searching graphs. In the following sections, we will use BFS and DFS of the graph to solve practical problems to deepen our understanding.

### 9.7.3 Topological Sorting

Real-world problems can often be modeled as graphs and solved using graph algorithms. For example, consider the problem of designing a four-year course plan for a major, which involves ensuring correct course dependencies and a feasible sequence of courses. This problem can be complex, but with the graph data structure, we can use graph algorithms to solve it. Suppose we have four courses with their dependencies shown in the graph, a feasible course study order is [functions, derivatives, systems of equations, calculus, linear algebra, probability theory, convolutional neural networks]. To determine the order of the courses, we can use an algorithm to sort the course dependencies, which is known as topological sorting.

![Figure 9.5: Courses Topological Relationship](images/fig-9.5.png)

*Figure 9.5: Courses Topological Relationship*

Topological sorting is a variant of depth-first search that produces a linear ordering of all vertices in a directed acyclic graph. This resulting order can be used to indicate event priorities, set project schedules, generate priority graphs for database queries, and so on. The basic ideas of topological sorting are as follows:

- Call dfs() on the graph g using depth-first search to find suitable vertices.
- Store the vertices in a stack, with the last one at the bottom.
- Return the data in the stack as the result of the topological sort.

Following these steps, we can transform a graph into a linear relationship, such as the course plan mentioned above, which can be converted into a topological sequence.

![Figure 9.6: Course sheduling](images/fig-9.6.png)

*Figure 9.6: Course sheduling*

The final topological sort result is presented below. Courses with the same color can be taken in any order, while courses with different colors must be taken in the order specified by the topological sort.

![Figure 9.7: Topological sequence of course sheduling](images/fig-9.7.png)

*Figure 9.7: Topological sequence of course sheduling*

To implement the graph algorithm for course scheduling, we first define an enumeration of colors to represent the state of node exploration.

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

Then, we define the node and graph as we have done many times before.

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

With the graph in place, we can start building the course dependency graph. When exploring all course nodes in the graph, we use the color attribute to indicate whether the node has been visited or not. The schedule variable stores the result of the course topological sorting. To prevent scheduling errors, such as circular dependencies, we add a ”has_circle” variable here to control the search process. When encountering a cycle, the program exits, indicating that the input data is incorrect.

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

In addition to course selection, cooking can also be abstracted as a topological sort. For example, consider making pancakes, as shown in the figure below. The recipe is simple: 1 egg, 1 cup of pancake mix, 1 tablespoon of oil, and 3/4 cup of milk. To make pancakes, you must first turn on the stove and heat the pan. Then mix all the ingredients together with a spoon and pour the mixture into the pan. When

bubbles begin to form, flip the pancake over until both sides are golden brown. Before eating, you can add sauce.

![Figure 9.8: Pancake Cooking](images/fig-9.8.png)

*Figure 9.8: Pancake Cooking*

By using the topological sort algorithm, the above figure can be simplified into a standard cooking step diagram. In this diagram, steps with the same color can be taken in any order. This step diagram can help kitchen novices make pancakes successfully. However, making them taste good is another matter altogether.

![Figure 9.9: Pancake cooking process topological relationship](images/fig-9.9.png)

*Figure 9.9: Pancake cooking process topological relationship*

Both cooking and course selection can be abstracted as process arrangements, and therefore, the same code can theoretically be used to handle them. The implementation of the cooking process topological sort algorithm is the same as the course planning topological sort algorithm. Therefore, we will not include most of the code here, but it can be found in the source code files of this book.

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

## 9.8 Strongly Connected Components

Large graphs, like the links between web pages, are commonly represented as graphs, and search engines such as Google uses massive directed graphs to store the links on the World Wide Web. In this type of graph, pages are vertices, and hyperlinks are edges connecting them. Figure 9.10 depicts the web pages linked to Google’s main site, highlighting that the entire internet can be seen as a graph.

![Figure 9.10: Internet connection](images/fig-9.10.png)

*Figure 9.10: Internet connection*

One significant feature of these graphs is that certain vertices have an exceptionally high number of edges. For example, Google is connected to nearly every website globally, while websites like Baidu and Tencent have numerous links within China. However, many vertices have very few or just one edge, forming clusters of interconnected nodes. These clusters are known as connected components, and if a connected component can be reached by any node in it in a finite number of steps, it is called a strongly connected component. A directed graph is strongly connected if and only if every two vertices in it are mutually reachable. Strongly connected graphs are similar to nested loops and must have loops. A directed graph may have multiple strongly connected components, and each of these components is called a strongly connected component. Figure(9.11) illustrates an example of strongly connected components in a directed graph.

![Figure 9.11: Stringly connected components ant its simplication](images/fig-9.11.png)

*Figure 9.11: Stringly connected components ant its simplication*

The strongly connected components C ∈G, where vertices v and w are connected, can be represented as a point in a simplified graph (shown in the left tricolored areas). To identify strongly connected components, the Tarjan algorithm, which is based on depth-first search, is commonly used. Applying the strongly connected component algorithm to a connected graph produces three trees that correspond to three connected components, as shown in the figure below. The independent area C

consists of only itself as a node, while F, L, and H form one connected component, and A, E, G, D, and B form another connected component. The three trees obtained by the strongly connected component algorithm represent the three connected components. By shifting the problem from the node level to the connected component level, the algorithm simplifies the problem and facilitates subsequent analysis and processing.

C A E F G B L D H

### 9.8.1 The BFS Strongly Connected Components Algorithm

The provincial partition problem is an example of a strongly connected component. In China, cities are categorized into provincial administrative regions. To solve this problem, a large amount of information about cities and their interconnections is provided, and an algorithm is used to divide cities into partitions and determine the number of provinces to which these cities belong. Assuming there are n cities, some of which are connected to each other and some are not, Chengdu and Yibin both belong to Sichuan Province, so the relationship between them can be represented as [”Chengdu”, ”Yibin”] and [”Yibin”, ”Chengdu”]. Another example may be [”Guangzhou”, ”Shenzhen”], [”Guangzhou”, ”Dongguan”]... Here, cities are abstracted as points in the graph, and relationships are seen as edges. The number of provinces can be determined by finding the number of strongly connected components, which can be achieved by the breadth-first search algorithm. For each city node in the graph, its color is initially white, and when visited, it is colored gray. The breadth-first search starts from that city until all the cities in the same connected component have been visited (colored gray), indicating a province. Traversing all connected components of cities, all provinces can be found. In the case of the provincial partition problem, the answer should be 2, the number of provinces. Below is an implementation of the strongly connected component algorithm using breadth-first search. It contains only the most basic functions for point and graph implementation, and unused ones are removed. The edges variable in the graph definition saves all edge relationships for exploring edge relationships.

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

Given the graph and node definitions, we can build a city connection graph. We continually change the color of each city to gray until a group of cities is fully explored, at which point we find a strongly connected component, i.e., a province.

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

The time complexity of this algorithm is O(n2) because we need to process n city nodes, and each city node may have a relationship with all remaining cities in the graph (when there is only one province). Breadth-first search uses a queue that can hold up to all n city nodes, so the space complexity is O(n).

### 9.8.2 The DFS Strongly Connected Components Algorithm

The province partition problem can also be solved using the depth-first search algorithm. The idea of depth-first search is to traverse all city nodes, and for each city, if it has not been visited yet (colored white), color it gray, and then start a depth-first search from that city. By using the depth-first search algorithm, we can obtain the cities directly connected to that city. These cities and the city itself belong to the same connected component. We can continue performing depth-first search on these cities until all cities in the same connected component have been visited (colored gray), indicating a province has been found. Traversing all cities allows us to obtain the total number of connected components, which is the total number of provinces.

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

In terms of complexity, it is similar to BFS since it also needs to process n city nodes, and each city node may have a relationship with all the remaining cities in the graph (when there is only one province). Therefore, the time complexity is still O(n2). Depth-first search uses a stack that can hold up to n city nodes, so the space complexity is O(n).

## 9.9 Shortest Path Problem

When accessing online content or remote computing resources, such as watching videos, sending emails, or logging into a lab computer from off-campus, network communication is required. Understanding how information is transmitted from one computer to another via the internet is a fundamental aspect of computer networks.

Equipment A Equipment C Router B Router A Internet Equipment B Equipment D

The diagram above illustrates the process of internet communication. When a user requests a webpage from a server using a browser, the request first travels through the local area network and then through a router to access the internet. The request then propagates through the internet until it reaches the local area network router where the server is located. The requested webpage is then sent back to the user’s browser via the same router. The tracepath command can be used to identify the path from a user’s computer to a specific link. For instance, tracing the website xxx.cn may involve passing through 13 routers, with the first two being gateway routers of the user’s network group.

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

Each router on the internet is connected to one or more routers. Thus, running tracepath at different times of the day may yield different results since the connections between routers have a cost that varies depending on network traffic. The network connections can be viewed as a weighted graph, with connections being adjusted based on the network situation. The goal is to find the path with the minimum total weight to transmit the message. This problem is similar to the word ladder problem discussed earlier since both involve finding the minimum value, but the weights in the word ladder problem are all the same.

### 9.9.1 Dijkstra’s Algorithm

Predecessors have proposed various algorithms for studying the shortest path in network graphs, and among them, Dijkstra’s algorithm is a good option. It is a greedy iterative algorithm that finds the shortest path from a specific starting node to all other nodes in the graph, similar to breadth-first search.

![Figure 9.12: Dijkstra](images/fig-9.12.png)

*Figure 9.12: Dijkstra*

In the figure above, we want to find the shortest path from V1 to V7. By visually exploring the graph, we can see that there are two shortest paths: [V1->V4->V3->V2->V6->V5->V7] and [V1->V4>V3->V5->V7], with a shortest distance of 38. If we were to calculate this using Dijkstra’s algorithm, we would need to track and calculate various distances and then add them up. To keep track of the total distance from the starting node to each target node, we will use the dist instance variable in the graph vertex. This variable contains the total weight of the path from the start to the target node. Dijkstra’s algorithm iterates over each node in the graph, with the iteration order controlled by a priority queue, and the dist value is used to determine the order of objects in the queue. When a node is first created, dist is set to 0. Theoretically, it is possible to set dist to infinity, but in practice, setting it to 0 is feasible, or setting it to a value larger than any real distance, such as the distance that light travels in one second, which is approximately equal to the distance between the earth and the moon, because no two points on earth are so far apart.

### 9.9.2 Implementing the Dijkstra’s Algorithm

Dijkstra’s algorithm is an incremental approach to finding the shortest path step-by-step, using a priority queue to process vertices based on their priority value. The algorithm selects the closest unvisited vertex to the starting point from all vertices that haven’t yet had their shortest path found, and continues the process. However, using this algorithm on the internet poses a challenge because it requires a complete graph representation of the entire network. This means that every router must have a map of all routers in the Internet, which is impractical.

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

The following outputs are shortest path between V1 and any point(including itself).

```text
V1-V5, min distance: 18
V1-V2, min distance: 11
V1-V6, min distance: 16
V1-V3, min distance: 8
V1-V7, min distance: 38
V1-V1, min distance: 0
V1-V4, min distance: 7
```

To solve this problem, other algorithms such as the Distance Vector Routing Protocol [15] and Link State Routing Protocol [16] are used for network information transmission. These algorithms allow routers to discover the network maps saved by other routers, which contain information about interconnected nodes. This approach allows for real-time updates of the network map content and is more efficient, greatly reducing network capacity requirements.

### 9.9.3 Analysis of Dijkstra’s Algorithm

Let’s analyze the time complexity of Dijkstra’s algorithm. Firstly, building the priority queue takes O(V ) time. Once the queue is constructed, the while loop is executed once for each vertex. Since vertices are added at the beginning and removed only after that, calling pop in the loop takes O(log V ) time. We can consider this loop and the calls to pop as O(V log V ). The for loop iterates once for each edge in the graph, and calling decrease_key takes O(E log V ) time. Therefore, the total time complexity is O((V + E) log V ), and the space complexity is O(V ).

## 9.10 Summary

In this chapter, we have explored the abstract data type of graphs and their implementation. Graphs are widely used in various fields such as course scheduling, networks, transportation, computers, knowledge graphs, and databases. Graphs can be utilized to solve many problems, as long as we can transform the original problem into a graph representation. Graphs have numerous applications in the following areas:

- Strongly connected components can be used to simplify graphs.
- Depth-first search can be utilized to explore deep branches of a graph.
- Topological sorting is useful in clarifying complex graph connections.
- Dijkstra’s algorithm can be employed to search for the shortest path in a weighted graph.
- Breadth-first search can be used to search for the shortest path in an unweighted graph.
