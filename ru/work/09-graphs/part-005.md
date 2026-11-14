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
