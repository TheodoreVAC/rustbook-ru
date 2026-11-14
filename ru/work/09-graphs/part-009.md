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
