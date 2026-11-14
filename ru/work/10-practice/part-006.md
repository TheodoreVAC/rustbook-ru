## 10.6 Consistent Hashing

The Consistent Hashing algorithm was initially proposed by Karger et al. of MIT to address hotspot issues in distributed caching. However, after years of development, it has become a widely applied algorithm. To understand its application, let’s consider caching images in Redis. A single Redis instance can handle small data volumes and low access rates, and a master-slave configuration may be sufficient.

However, when data volumes grow, and access rates increase, a cluster must be created to distribute data across multiple machines. For example, if there are 5 machines, the position index of an image would be index = hash(key) % 5, where key is an index related to the image. However, adding or removing machines changes N, and previously calculated indices will become invalid. This is where consistent hashing comes in. It creates a circle that ranges from 0 to 232 −1, mapping data to a position on the circle.

232 −1 0 Node3 Node1 Node2

To achieve caching, data must be added to a specific segment of the circle based on its hash value. The corresponding node located just clockwise from the segment will store the data.

232 −1 0 Node3 Node1 Node2

Suppose Node3 fails, causing data between Node2 and Node3 to be transferred to Node1.

232 −1 0 Node1 Node2

When a new machine, Node4, is added, the data originally stored on Node3 will now be stored on Node4.

232 −1 0 Node3 Node1 Node4 Node2

The Consistent Hashing algorithm is fault-tolerant and scalable since it only relocates a small portion of the data when nodes are added or removed. This feature enables the algorithm to achieve consistency. To implement Consistent Hashing, a Ring is needed to store nodes representing machines.

```rust
// conshash.rs

use std::fmt::Debug;
use std::string::ToString;
use std::hash::{Hash, Hasher};
use std::collections::{BTreeMap, hash_map::DefaultHasher};

// Ring node definition, used for storing the host, ip and port
#[derive(Clone, Debug)]
struct Node {
    host: &'static str,
    ip: &'static str,
    port: u16,
}

// implement a to_string function
impl ToString for Node {
    fn to_string(&self) -> String {
        self.ip.to_string() + &self.port.to_string()
    }
}

// Definition for the Ring
struct Ring<T: Clone + ToString + Debug> {
    replicas: usize, // partition number
    ring: BTreeMap<u64, T>, // store data
}
```

Replicas in the Ring are utilized to avoid node clustering and ensure even data distribution across nodes. Multiple virtual nodes can be created for each node to solve the node clustering problem. The default hash calculator provided by the standard library, with a default of 10 nodes, can be used for hash calculation, or custom nodes can be created. For the Consistent Hashing algorithm, at least node insertion, node deletion, and query functions must be supported. Additionally, batch versions of insertion and deletion can be implemented for batch processing.

```rust
// conshash.rs

const DEFAULT_REPLICAS: usize = 10;

// Hash calculation function
fn hash<T: Hash>(val: &T) -> u64 {
    let mut hasher = DefaultHasher::new();
    val.hash(&mut hasher);

    hasher.finish()
}

impl<T> Ring<T> where T: Clone + ToString + Debug {
    fn new() -> Self {
        Self::with_capacity(DEFAULT_REPLICAS)
    }

    // new with a replicas parameter
    fn with_capacity(replicas: usize) -> Self {
        Ring {
            replicas: replicas,
            ring: BTreeMap::new()
        }
    }

    // Batch insertion of nodes
    fn add_multi(&mut self, nodes: &[T]) {
        if !nodes.is_empty() {
            for node in nodes.iter() {
                self.add(node);
            }
        }
    }

    fn add(&mut self, node: &T) {
        for i in 0..self.replicas {
            let key = hash(&(node.to_string()
                                + &i.to_string()));
            self.ring.insert(key, node.clone());
        }
    }

    // Batch deletion of nodes
    fn remove_multi(&mut self, nodes: &[T]) {
        if !nodes.is_empty() {
            for node in nodes.iter() {
                self.remove(node);
            }
        }
    }
```

```rust
    fn remove(&mut self, node: &T) {
        // assertion to ensure that the node exists
        assert!(!self.ring.is_empty());

        for i in 0..self.replicas {
            let key = hash(&(node.to_string()
                                + &i.to_string()));
            self.ring.remove(&key);
        }
    }

    // Get nodes
    fn get(&self, key: u64) -> Option<&T> {
        if self.ring.is_empty() {
            return None;
        }

        let mut keys = self.ring.keys();
        keys.find(|&k| k >= &key)
            .and_then(|k| self.ring.get(k))
            .or(keys.nth(0).and_then(|x| self.ring.get(x)))
    }
}

fn main() {
    let replica = 3;
    let mut ring = Ring::with_capacity(replica);
    let node = Node{
        host:"localhost",
        ip:"127.0.0.1",
        port:23
    };
    ring.add(&node);

    for i in 0..replica {
        let key = hash(&(node.to_string() + &i.to_string()));
        let res = ring.get(key);
        assert_eq!(node.host, res.unwrap().host);
    }

    println!("{:?}", &node);
    ring.remove(&node);
    // Node { host: "localhost", ip: "127.0.0.1", port: 23 }
}
```
