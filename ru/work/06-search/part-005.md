## 6.5 The Hash Search

The search algorithms we have discussed so far use the positional information of items in a collection to perform searches. Binary search can find data items in logarithmic time by sorting the collection. However, if an algorithm has prior knowledge of the stored addresses of different items, it can retrieve them directly without comparing them one by one. This method is called Hash Search, a search algorithm with a complexity of O(1), making it the fastest search algorithm available. To implement Hash Search, the item’s address must exist first. A data structure that provides an efficient way to store and retrieve items’ addresses is needed. This data structure is known as a hash table, which stores data items in such a way that they are easy to locate, with each item’s position referred to as a slot or address. These slots are named starting from 0, or any other value. Once the first slot is chosen, all subsequent slots are incremented accordingly. Initially, the hash table contains no items, and each slot is empty. A hash table can be implemented using Vec, with each element initialized to None. The figure below shows a hash table with size m = 11, meaning that there are m slots named 0 to 10.

![Figure 6.4: Hash table](images/fig-6.4.png)

*Figure 6.4: Hash table*

The mapping between data items and their corresponding slots in the hash table is accomplished through a hash function. The hash function takes any item in the collection and returns a specific slot name, a process known as hashing. For example, if there are integer items [24, 61, 84, 41, 56, 31], and a hash table with a capacity of 11 slots, each item’s location in the hash table can be obtained by inputting it into the hash function. A simple hash function involves using modulo, since any number modulo 11 will have a remainder within 11, ensuring that there is always a slot available to store the data. hash(item) = item%11

(6.6)

Here is the result after modulo hash calculation.

![Figure 6.5: Modulo hash](images/fig-6.5.png)

*Figure 6.5: Modulo hash*

Calculated the hash value, the item can be inserted into the corresponding slot in the hash table, as depicted in the figure above. Currently, 6 of the 11 slots in the table are occupied, resulting in a load factor of λ = 6/11. The load factor is a useful metric to evaluate the hash table, particularly when it needs to store a large number of items. A high load factor indicates that there is limited space for additional items, necessitating resizing the table. In languages like Rust and Go, resizing occurs automatically when the load factor exceeds a particular threshold, preparing for future data insertion. Although the data stored in the hash table is unsorted, the hash function enables the calculation of the slot of a data item regardless of its disorderliness. For instance, to check if the number 56 exists in the table, its hash value can be computed (hash(56) = 1), and slot 1 can be examined to locate 56, indicating its presence in the table. The search operation has a complexity of O(1), making hash search very efficient. However, conflicts may occur and must be resolved, or else the hash table cannot be utilized. For example, if 97 is added, and its hash value (hash(97) = 9) corresponds to an occupied slot (9) that contains 31 instead of 97, a collision occurs that necessitates resolution.

### 6.5.1 Hash Functions

In the previous section, the hash function computed the remainder of the item directly, ensuring that the remainder falls within a specific range. Any algorithm that can produce a value within a particular range based on the item can be used as a hash function. By improving the hash function, we can minimize the probability of collisions and create an effective hash table. One such approach to improving the hash function is the ”sum of groups” method, which divides items into equal-sized blocks (the last block may be different), adds them up, and then computes the remainder. For instance, if the data item is the phone number ”316-545-0134,” it can be split into twodigit numbers, padded with zeroes if required, resulting in [31, 65, 45, 01, 34]. The sum is 176, and taking the remainder of 11 yields a hash value (slot) of 0. The phone number may also be split into three-digit numbers or reversed before computing the remainder. Many hash functions are available, as any value that can be computed and then have its remainder taken can be used in various ways.

Another hash algorithm is the ”mid-square” method. The item is squared first, and then the middle portion of the square is extracted as the value for which the remainder is computed. For example, if the number is 36, its square is 1296, and taking the middle portion, 29, and then computing the remainder of 11 yields hash(29) = 7, indicating that 36 should be stored in slot 7. When storing a string, the remainder can also be calculated based on the ASCII values of its characters. The string ”rust” has four characters with ASCII values of [114, 117, 115, 116], and their sum is 462. Computing the remainder results in hash(462) = 0. Other strings, such as ”Java” with ASCII values [74, 97, 118, 97], may also be tried. Its sum is 386, and taking the remainder gives hash(386) = 1, indicating that ”Java” should be stored in slot 1, as shown in the figure below.

7 9 0 3 5 6 8 10 1 2 4 go css rust Java None None None None C# C++ html

The following is an implementation of hash function for ASCII value.

```rust
// hash.rs

fn hash1(astr: &str, size: usize) -> usize {
    let mut sum = 0;
    for c in astr.chars() {
        sum += c as usize;
    }

    sum % size
}

fn main() {
    let s1 = "rust"; let s2 = "Rust";
    let size = 11;

    let p1 = hash1(s1, size);
    let p2 = hash1(s2, size);
    println!("{s1} in slot {p1}, {s2} in slot {p2}");
    // rust in slot 0, Rust in slot 1
}
```

To mitigate collisions that may arise when using the above hash function, one can modify it slightly. For example, one can use the position of different characters in a string as weights and multiply the ASCII values by their positional weights. hash(rust) = (0 ∗114 + 1 ∗117 + 2 ∗115 + 3 ∗116)%11

= 695%11 (6.7) = 2

Starting the index from 1 is preferred to ensure that the first character contributes to the total. Below is an example calculation and code snippet. hash(rust) = (1 ∗114 + 2 ∗117 + 3 ∗115 + 4 ∗116)%11

= 1157%11 (6.8) = 2

```rust
// hash.rs
fn hash2(astr: &str, size: usize) -> usize {
    let mut sum = 0;
    for (i, c) in astr.chars().enumerate() {
        sum += (i + 1) * (c as usize);
    }
    sum % size
}

fn main() {
    let (s1, s2, size) = ("rust", "Rust", 11);
    let p1 = hash2(s1, size);
    let p2 = hash2(s2, size);
    // rust in slot 2, Rust in slot 3
}
```

Efficiency is crucial when designing a hash function to ensure that it does not become the bottleneck of the system. If the hash function is too complex, it could break the O(1) complexity.

### 6.5.2 Collison Resolution

To address the issue of hash collisions, collision resolution methods are necessary. For instance, if a hash function with position as weight is used and the index starts from 0, the strings ”rust” and ”Rust” will collide. When two items are hashed to the same slot, a method must be used to insert the conflicting item into another slot of the hash table. This process is called collision resolution. Although perfect hash tables do not exist due to limited memory and complex real-world situations, one intuitive method for resolving collisions is to search the hash table and attempt to find the next empty slot to save the conflicting item. The simplest method is called open addressing, specifically linear probing. Linear probing attempts to linearly probe the next empty slot in the hash table, starting from the original collision point until the first empty slot is found. Note that you can start searching again from the beginning after reaching the end. The following figure shows a hash table with 11 slots, where we try to insert 35 and 47.

0 3 5 6 7 8 9 10 1 2 4 None 56 None None None 61 84 31 None 24 41

When inserting 35, its position should be slot 2, but we find that slot 2 already contains 24. Therefore, we start searching for an empty slot from slot 2 and find that slot 3 is empty, so we insert 35 there.

0 3 5 6 7 8 9 10 1 2 4 None None None None 56 24 35 61 84 41 31

When we insert 47, we find that slot 3 has the value 35, so we search for the next empty slot and find that slot 4 is empty, so we insert 47 there.

7 9 0 3 5 6 8 10 1 2 4 None None None 56 24 35 47 61 84 41 31

To search for items in a hash table built using open addressing, we must use the same method as used during its construction. For instance, if we are searching for item 56 with a hash of 1, we locate it in slot 56 and return true. However, if we are looking for item 35, which has a hash of 2, we may find another item like 24 instead of 35 due to collisions. To avoid returning false, we need to conduct a sequential search until we locate 35, an empty slot, or we loop back to 24 before returning the result. However, using a sequential search may lead to data clustering, where items cluster in the table due to multiple collisions occurring in the same hash slot. Linear probing fills subsequent slots with conflicting items, forcing the originally intended values to be inserted elsewhere. Sequential searches are time-consuming, with a complexity greater than O(1). To address data clustering, open addressing technology can be extended to skip several slots instead of sequentially searching for the next open slot. By checking every three slots when a conflict occurs, for example, the conflicting items are more evenly distributed, thus dispersing the conflict. This method has a significant effect and can alleviate data clustering, as shown in the figure below.

0 3 5 6 7 8 9 10 1 2 4 None 47 None None 56 24 35 61 84 41 31

When adding item 35, a conflict may occur, prompting the search to skip every three slots from that point onwards, thus dispersing the conflict. Consequently, item 47 can be inserted without any conflict. This method has proven effective in alleviating data clustering, as demonstrated in the following figure. Rehashing is the process of finding an alternative slot in a hash table after a collision occurs. This process involves calculating a new hash value using a specified skip size, which must ensure that all slots in the table can eventually be accessed. To guarantee this, it is advisable to use a prime number as the table size, as exemplified by the use of 11 in the accompanying example. rehash(pos) = (pos + n)%size

(6.9)

Another approach to resolving conflicts is the chain method. This method involves setting up a linked list to store data items for each conflicting position, as shown in Figure (6.6). When searching, conflicts are resolved by sequentially searching the chain, which has a complexity of O(n). If the data in the conflict chain is sorted, a binary search can be utilized to achieve a complexity of O(log2(n)). If the chain becomes too long, it can be transformed into a red-black tree to enhance its structural stability. In many programming languages, the chain method is the default implementation for resolving conflicts in hash table data structures.

![Figure 6.6: Collison Resolution by Chain Method](images/fig-6.6.png)

*Figure 6.6: Collison Resolution by Chain Method*

### 6.5.3 Implementing a HashMap in Rust

The most commonly used collection type in Rust is the HashMap. It is an associative data type that stores key-value pairs. The key is utilized to locate the position of the value, and due to the position uncertainty, this type of search is akin to searching on a map. Thus, this data structure is called HashMap. HashMap is an unordered collection of key-value pairs where the keys are unique, and there is a one-to-one relationship between the keys and the values. Here is the abstract data type definition of HashMap:

- new(): creates a new HashMap, takes no arguments and returns an empty HashMap collection.
- insert(k,v): adds a new key-value pair to the HashMap, taking parameters k and v. If the key exists, the old value is replaced with the new value. No return value is provided.
- remove(k): removes value corresponding to k from the HashMap, takes parameter k, and returns the corresponding value v.
- get(k): returns the value v stored in the HashMap for the given key k (which may be empty None), takes parameter k.
- contains(k): returns true if the key k exists in the HashMap, otherwise false, takes parameter k.
- len(): returns the number of key-value pairs stored in the HashMap, takes no arguments.

The table below displays the results of operations assuming that ’h’ is an already created empty HashMap (represented as {} here).

**Table 6.2: HashMap operations**

| Operation | Value | Return |
| --- | --- | --- |
| h.is_empty() | {} | true |
| h.insert(”a”, 1) | {a:1} |  |
| h.insert(”b”, 2) | {a:1, b:2} |  |
| h.insert(”c”, 3) | {a:1, b:2, c:3} |  |
| h.get(”b”) | {a:1, b:2, c:3} | Some(2) |
| h.get(”d”) | {a:1, b:2, c:3} | None |
| h.len() | {a:1, b:2, c:3} | 3 |
| h.contains(”c”) | {a:1, b:2, c:3} | true |
| h.contains(”e”) | {a:1, b:2, c:3} | false |
| h.remove(”a”) | {b:2, c:3} | Some(1) |
| h.remove(”a”) | {b:2, c:3} | None |
| h.insert(”a”, 1) | {b:2, c:3, a:1} |  |
| h.contains(”a”) | {b:2, c:3, a:1} | true |
| h.len() | {b:2, b:3, a:1} | 3 |
| h.get(”a”) | {b:2, c:3, a:1} | Some(1) |
| h.remove(”c”) | {b:2, a:1} | Some(3) |

In actual implementation, a HashMap in Rust is made up of two separate Vecs - one for storing the keys (called slot) and the other for storing the values (called data). The slot Vec saves the keys with the index starting from 1, while the default value in the slot Vec is 0. The HashMap is encapsulated by a struct, and a cap parameter is added to control the capacity.

```rust
// hashmap.rs

#[derive(Debug, Clone, PartialEq)]
struct HashMap <T> {
    cap: usize, // capacity
    slot: Vec<usize>, // store data address (index)
    data: Vec<T>, // store elements
}
```

The rehash function in Rust can be implemented using a linear search method that adds 1, which is simple and easy to implement. The initial size of the HashMap is set to 11, but it can also be set to other prime numbers, such as 13, 17, 19, 23, 29, etc. Below is the complete implementation code for a HashMap in Rust.

```rust
// hashmap.rs

impl<T: Clone + PartialEq + Default> HashMap<T> {
    fn new(cap: usize) -> Self {
        // Initialize slot and data
        let mut slot = Vec::with_capacity(cap);
        let mut data = Vec::with_capacity(cap);
        for _i in 0..cap{
            slot.push(0);
            data.push(Default::default());
        }

        HashMap { cap, slot, data }
    }

    fn len(&self) -> usize {
        let mut len = 0;
        for &d in self.slot.iter() {
            // If slot is not empty, then increase len by 1
            if 0 != d {
                len += 1;
            }
        }
        len
    }

    fn is_empty(&self) -> bool {
        let mut empty = true;
        for &d in self.slot.iter() {
            if 0 != d {
                empty = false;
                break;
            }
        }
        empty
    }

    fn clear(&mut self) {
        let mut slot = Vec::with_capacity(self.cap);
        let mut data = Vec::with_capacity(self.cap);
        for _i in 0..self.cap{
            slot.push(0);
            data.push(Default::default());
        }

        self.slot = slot;
        self.data = data;
```

```rust
    }

    fn hash(&self, key: usize) -> usize {
        key % self.cap
    }

    fn rehash(&self, pos: usize) -> usize {
        (pos + 1) % self.cap
    }

    fn insert(&mut self, key: usize, value: T) {
        if 0 == key { panic!("Error: key must > 0"); }

        let pos = self.hash(key);
        if 0 == self.slot[pos] {
            // If the slot is empty, insert directly
            self.slot[pos] = key;
            self.data[pos] = value;
        } else {
            // If the slot is not empty, then
            // find next available position
            let mut next = self.rehash(pos);
            while 0 != self.slot[next]
                && key != self.slot[next] {
                next = self.rehash(next);

                // If the slot is full, exit
                if next == pos {
                    println!("Error: slot is full!");
                    return;
                }
            }

            // Insert the data in the found slot
            if 0 == self.slot[next] {
                self.slot[next] = key;
                self.data[next] = value;
            } else {
                self.data[next] = value;
            }
        }
    }

    fn remove(&mut self, key: usize) -> Option<T> {
        if 0 == key { panic!("Error: key must > 0"); }

        let pos = self.hash(key);
        if 0 == self.slot[pos] {
            // If the slot is empty, return None
            None
        } else if key == self.slot[pos] {
            // If found the same key,
```

```rust
            // update the slot and data
            self.slot[pos] = 0;
            let data = Some(self.data[pos].clone());
            self.data[pos] = Default::default();
            data
        } else {
            let mut data: Option<T> = None;
            let mut stop = false;
            let mut found = false;
            let mut curr = pos;

            while 0 != self.slot[curr] && !found && !stop {
                if key == self.slot[curr] {
                    // If the value is found, delete the data
                    found = true;
                    self.slot[curr] = 0;
                    data = Some(self.data[curr].clone());
                    self.data[curr] = Default::default();
                } else {
                    // If rehashing returns to the initial
                    // position, it means that it has searched
                    // a full circle and still not found
                    curr = self.rehash(curr);
                    if curr == pos {
                        stop = true;
                    }
                }
            }

            data
        }
    }

    fn get_pos(&self, key: usize) -> usize {
        if 0 == key { panic!("Error: key must > 0"); }

        // Calculate the data position
        let pos = self.hash(key);
        let mut stop = false;
        let mut found = false;
        let mut curr = pos;

        // Loop through to find the data
        while 0 != self.slot[curr] && !found && !stop {
            if key == self.slot[curr] {
                found = true;
            } else {
                // If rehashing returns to the initial position
                // it means that it has searched a full circle
                // and still not found
                curr = self.rehash(curr);
                if curr == pos {
```

```rust
                    stop = true;
                }
            }
        }

        curr
    }

    // Get a reference and a mutable reference to val
    fn get(&self, key: usize) -> Option<&T> {
        let curr = self.get_pos(key);
        self.data.get(curr)
    }

    fn get_mut(&mut self, key: usize) -> Option<&mut T> {
        let curr = self.get_pos(key);
        self.data.get_mut(curr)
    }

    fn contains(&self, key: usize) -> bool {
        if 0 == key {
            panic!("Error: key must > 0");
        }
        self.slot.contains(&key)
    }

    // Implement iteration and mutable iteration for hashmap
    fn iter(&self) -> Iter<T> {
        let mut iterator = Iter { stack: Vec::new() };
        for item in self.data.iter() {
            iterator.stack.push(item);
        }
        iterator
    }

    fn iter_mut(&mut self) -> IterMut<T> {
        let mut iterator = IterMut { stack: Vec::new() };
        for item in self.data.iter_mut() {
            iterator.stack.push(item);
        }
        iterator
    }
}

// Implementation of iteration
struct Iter<'a, T: 'a> { stack: Vec<&'a T>, }
impl<'a, T> Iterator for Iter<'a, T> {
    type Item = &'a T;
    fn next(&mut self) -> Option<Self::Item> {
        self.stack.pop()
    }
}
```

```rust
struct IterMut<'a, T: 'a> { stack: Vec<&'a mut T>, }
impl<'a, T> Iterator for IterMut<'a, T> {
    type Item = &'a mut T;
    fn next(&mut self) -> Option<Self::Item> {
        self.stack.pop()
    }
}

fn main() {
    basic();
    iter();

    fn basic() {
        let mut hmap = HashMap::new(11);
        hmap.insert(2,"dog");
        hmap.insert(3,"tiger");
        hmap.insert(10,"cat");

        println!("empty: {}, size: {:?}",
                    hmap.is_empty(), hmap.len());
        println!("contains key 2: {}", hmap.contains(2));

        println!("key 3: {:?}", hmap.get(3));
        let val_ptr = hmap.get_mut(3).unwrap();
        *val_ptr = "fish";
        println!("key 3: {:?}", hmap.get(3));
        println!("remove key 3: {:?}", hmap.remove(3));
        println!("remove key 3: {:?}", hmap.remove(3));

        hmap.clear();
        println!("empty: {}, size: {:?}",
                    hmap.is_empty(), hmap.len());
    }

    fn iter() {
        let mut hmap = HashMap::new(11);
        hmap.insert(2,"dog");
        hmap.insert(3,"tiger");
        hmap.insert(10,"cat");

        for item in hmap.iter() {
            println!("val: {item}");
        }

        for item in hmap.iter_mut() {
            *item = "fish";
        }

        for item in hmap.iter() {
            println!("val: {item}");
        }
```

```text
    }
}
```

Here is the code execution output.

```text
empty: false, size: 3
contains key 2: true
key 3: Some("tiger")
key 3: Some("fish")
remove key 3: Some("fish")
remove key 3: None
empty: true, size: 0
val: cat
val:
val:
val:
val:
val:
val:
val: tiger
val: dog
val:
val:
val: fish
val: fish
val: fish
val: fish
val: fish
val: fish
val: fish
val: fish
val: fish
val: fish
val: fish
```

### 6.5.4 Analysis of HashMap

A hash table provides a lookup complexity of O(1) in the best case. However, due to collisions, the number of comparisons during the lookup process can vary. The severity of collisions affects the performance of the hash table, and a good evaluation metric is the load factor λ. A small load factor means the chance of collisions is low, and items are more likely to be in their corresponding slot. A large load factor means the table is filling up quickly, and there are more collisions, leading to a more complex conflict resolution process. The result of each search is either success or failure. For searches performed using linear probing

1 1+ 1−λ

open addressing, the average number of comparisons for success is about

, and for failure, it is 2 1−λ )2 1 1+( . Even when using chaining, the average number of comparisons for success is 1 + λ/2,

about

2

and for failure, it is λ. Overall, the lookup complexity of a hash table is around O(λ). When using the chaining method in a hash table, an increase in collisions results in more items being added to the same chain. As a result, searching for a specific item in the chain takes longer, making it the main contributor to the search time.
