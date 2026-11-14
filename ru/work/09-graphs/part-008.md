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
