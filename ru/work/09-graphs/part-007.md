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
