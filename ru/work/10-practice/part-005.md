## 10.5 Least Recently Used(LRU) Algorithm

The cache eviction algorithm, or page replacement algorithm, is a commonly used memory management technique in virtual paging storage and data caching. Its principle is based on the assumption that if data has been recently accessed, it is more likely to be accessed again in the future. Therefore, data blocks that are in memory but not used will be removed based on which data is the least recently used, freeing up space and saving memory. LRU (Least Recently Used) is a popular eviction algorithm used to eliminate data based on the access record of data when storage is limited. Assuming a hash-linked list is used to cache user information with a capacity of 5, and currently caching 4 user information, as shown in the figure.

001 002 003 004 Info a Info b Info c Info d

When a client queries user 5, the data is not in the hash-linked list, so it needs to be read from the database and inserted into the cache. At this point, the rightmost node of the linked list represents the

most recently accessed user 5, and the leftmost represents the least recently accessed user 1.

001 002 003 004 005 Info a Info b Info c Info d Info e

Next, when another client accesses user 2, the data is found in the hash-linked list, so user 2 is simply removed from its current position and reinserted into the rightmost of the linked list.

001 003 004 005 Info a Info c Info d Info e 002 Info b

After these accesses, the hash-linked list looks like the figure shown.

001 003 004 005 002 Info a Info c Info d Info e Info b

Later, a client accesses user 6, but the data is not in the cache, so it also needs to be inserted.

001 003 004 005 002 006 Info a Info c Info d Info e Info b Info f

However, since the cache has reached its limit, the least recently accessed data, user 1, needs to be deleted first. Then, user 6 can be inserted at the rightmost end of the hash-linked list.

003 004 005 002 006 Info c Info d Info e Info b Info f

The LRU algorithm is a common cache eviction algorithm that frees up memory by removing the least recently used data. To implement this algorithm, we need to define the data structure and operations abstracted from the graph. This includes managing keys, entries, and front and back pointers. The necessary operation functions include insert, remove, contains, and auxiliary functions.

```rust
// lru.rs
use std::collections::HashMap;

// Definition for entry of LRU
struct Entry<K, V> {
    key: K,
    val: Option<V>,
```

```rust
    next: Option<usize>,
    prev: Option<usize>,
}

struct LRUCache<K, V> {
    cap: usize,
    head: Option<usize>,
    tail: Option<usize>,
    map: HashMap<K, usize>,
    entries: Vec<Entry<K, V>>,
}
```

To store the keys, we will use a HashMap, and a Vec to store the entries. The head and tail pointers can be simplified to the index of the Vec. To customize the cache capacity, we can implement a with_capacity function, with new setting the capacity to 100 by default.

```rust
// lru.rs
use std::hash::Hash;

const CACHE_SIZE: usize = 100;

impl<K: Clone + Hash + Eq, V> LRUCache<K, V> {
    fn new() -> Self {
        Self::with_capacity(CACHE_SIZE)
    }

    fn len(&self) -> usize {
        self.map.len()
    }

    fn is_empty(&self) -> bool {
        self.map.is_empty()
    }

    fn is_full(&self) -> bool {
        self.map.len() == self.cap
    }

    fn with_capacity(cap: usize) -> Self {
        LRUCache {
            cap: cap,
            head: None,
            tail: None,
            map: HashMap::with_capacity(cap),
            entries: Vec::with_capacity(cap),
        }
    }
}
```

When inserting data, if the key already exists, the value will be updated directly and the original value will be returned. If the inserted value does not exist, the returned value should be None, hence the use of Option as the return type. The access method is used to remove the original value and update the value, and ensure_room is used to remove the least recently used data when the cache reaches capacity.

```rust
// lru.rs

impl<K: Clone + Hash + Eq, V> LRUCache<K, V> {
    fn insert(&mut self, key: K, val: V) -> Option<V> {
        if self.map.contains_key(&key) {
            // Update if key exists
            self.access(&key);
            let entry = &mut self.entries[self.head.unwrap()];
            let old_val = entry.val.take();
            entry.val = Some(val);
            old_val
        } else {
            // insert if key not exists
            self.ensure_room();

            // Update the original head pointer
            let index = self.entries.len();
            self.head.map(|e| {
                self.entries[e].prev = Some(index);
            });

            // The new head node
            self.entries.push(Entry {
                key: key.clone(),
                val: Some(val),
                prev: None,
                next: self.head,
            });

            self.head = Some(index);
            self.tail = self.tail.or(self.head);
            self.map.insert(key, index);

            None
        }
    }

    fn get(&mut self, key: &K) -> Option<&V> {
        if self.contains(key) { self.access(key); }

        let entries = &self.entries;
        self.map.get(key).and_then(move |&i| {
            entries[i].val.as_ref()
        })
    }

    fn get_mut(&mut self, key: &K) -> Option<&mut V> {
        if self.contains(key) { self.access(key); }

        let entries = &mut self.entries;
        self.map.get(key).and_then(move |&i| {
```

```rust
            entries[i].val.as_mut()
        })
    }

    fn contains(&mut self, key: &K) -> bool {
        self.map.contains_key(key)
    }

    // Ensure there is enough capacity, remove the
    // least recently used item if full
    fn ensure_room(&mut self) {
        if self.cap == self.len() {
            self.remove_tail();
        }
    }

    fn remove_tail(&mut self) {
        if let Some(index) = self.tail {
            self.remove_from_list(index);
            let key = &self.entries[index].key;
            self.map.remove(key);
        }
        if self.tail.is_none() {
            self.head = None;
        }
    }

    // Get the value of a key, remove the
    // old position and add to the head
    fn access(&mut self, key: &K) {
        let i = *self.map.get(key).unwrap();
        self.remove_from_list(i);
        self.head = Some(i);
    }

    fn remove(&mut self, key: &K) -> Option<V> {
        self.map.remove(&key).map(|index| {
                self.remove_from_list(index);
                self.entries[index].val.take().unwrap()
            })
    }

    fn remove_from_list(&mut self, i: usize) {
        let (prev, next) = {
            let entry = self.entries.get_mut(i).unwrap();
            (entry.prev, entry.next)
        };

        match (prev, next) {
            // The data item is in the middle of the cache
            (Some(j), Some(k)) => {
                let head = &mut self.entries[j];
```

```rust
                head.next = next;
                let next = &mut self.entries[k];
                next.prev = prev;
            },
            // The data item is at the end of the cache
            (Some(j), None) => {
                let head = &mut self.entries[j];
                head.next = None;
                self.tail = prev;
            },
            // The data item is at the head of the cache
            _ => {
                if self.len() > 1 {
                    let head = &mut self.entries[0];
                    head.next = None;
                    let next = &mut self.entries[1];
                    next.prev = None;
                }
            },
        }
    }
}
```

The following are use example of LRU.

```rust
// lru.rs

fn main() {
    let mut cache = LRUCache::with_capacity(2);
    cache.insert("foo", 1);
    cache.insert("bar", 2);
    cache.insert("baz", 3);
    cache.insert("tik", 4);
    cache.insert("tok", 5);

    assert!(!cache.contains(&"foo"));
    assert!(!cache.contains(&"bar"));
    assert!(cache.contains(&"baz"));
    assert!(cache.contains(&"tik"));

    cache.insert("qux", 6);
    assert!(cache.contains(&"qux"));
}
```
