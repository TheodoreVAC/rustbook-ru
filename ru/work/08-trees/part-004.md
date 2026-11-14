## 8.4 Binary Search Tree

However, linear data structures for trees are not suitable for large amounts of data as copying and moving data become very time-consuming. To address this, this section explores implementing trees using nodes. Specifically, this section focuses on binary trees, which have only two child nodes. To understand binary trees better, we study binary search trees for searching, which store data using keyvalue pairs, similar to HashMap.

### 8.4.1 The Binary Search Tree Abstract Data Type

The binary search tree provides the following abstract data types:

- new() creates a new tree, takes no parameters, and returns an empty tree.
- insert(k, v) stores the data (k, v) in the tree, takes the key k and value v, and returns nothing.
- contains(&k) searches the tree for the key k, takes a parameter &k, and returns a boolean.
- get(&k) returns the value v of key k from the tree without deleting it, takes a parameter &k.
- max() returns the maximum key k and its value v in the tree, takes no parameters.
- min() returns the minimum key k and its value v in the tree, takes no parameters.
- len() returns the number of data items in the tree, takes no parameters, and returns an integer of type usize.
- is_empty() tests whether the tree is empty, takes no parameters, and returns a boolean.
- iter() returns the tree in iterator form, takes no parameters, and does not change the tree.
- preorder() performs a pre-order traversal, takes no parameters, and outputs each k-v pairs.
- inorder() performs an in-order traversal, takes no parameters, and outputs each k-v pairs.
- postorder() performs a post-order traversal, takes no parameters, and outputs each k-v pairs.

The table below displays the binary search tree after different operations, represented by tuples for tree nodes and enclosed in square brackets, assuming t is a newly created empty tree.

**Table 8.3: Operations on binary search tree**

| operation | tree value | return value |
| --- | --- | --- |
| t.is_empty() | [] | true |
| t.insert(1,‘a’) | [(1,‘a’)] |  |
| t.insert(2,‘b’) | [(1,‘a’),(2,‘b’)] |  |
| t.len() | [(1,‘a’),(2,‘b’)] | 2 |
| t.get(&4) | [(1,‘a’),(2,‘b’)] | None |
| t.get(&2) | [(1,‘a’),(2,‘b’)] | Some(‘b’) |
| t.min() | [(1,‘a’),(2,‘b’)] | (Some(1), Some(‘a’)) |
| t.max() | [(1,‘a’),(2,‘b’)] | (Some(2), Some(‘b’)) |
| t.contains(2) | [(1,‘a’),(2,‘b’)] | true |
| t.insert(2,‘c’) | [(1,‘a’),(2,‘c’)] |  |
| t.insert(3,‘d’) | [(1,‘a’),(2,‘c’),(3,‘d’)] |  |
| t.contains(4) | [(1,‘a’),(2,‘c’),(3,‘d’)] | false |
| t.get(&3) | [(1,‘a’),(2,‘c’),(3,‘d’)] | Some(‘d’) |

### 8.4.2 Implementing a Binary Search Tree in Rust

In contrast to heaps, where the left and right child nodes are not compared to their value, in a binary search tree, the key of the left child node is smaller than the key of the parent node, and the key of the right child node is greater than the key of the parent node. This rule of left < parent < right is applied recursively to all subtrees.

![Figure 8.5: Binary search tree](images/fig-8.5.png)

*Figure 8.5: Binary search tree*

In the example above, 70 is the root node, 31 is smaller and becomes the left node, and 93 is larger and becomes the right node. Then 14 is inserted, which is smaller than 70 and descends to 31, and as it is smaller than 31, it becomes the left node of 31. Similar steps are taken to insert other data, and finally, a binary search tree is formed. The inorder traversal of the tree is [14, 23, 31, 70, 73, 93, 94], which is sorted from small to large, so the binary search tree can also be used to sort data. Using inorder traversal, we obtain the ascending order sorting result, and using the mirrored inorder traversal, i.e., the ”right-root-left” order traversal, we obtain the descending order sorting result. To implement the binary search tree, we define it as a struct BST (BinarySearchTree), which includes key values and links to left and right child nodes. Following the definition of the abstract data type, the implementation of the binary search tree is shown below.

```rust
// bst.rs
use std::cmp::{max, Ordering::*};
use std::fmt::Debug;

// Binary search tree node link
type Link<T,U> = Option<Box<BST<T,U>>>;

// Definition of binary search tree
#[derive(Debug,Clone)]
struct BST<T,U> {
    key: Option<T>,
    val: Option<U>,
    left: Link<T,U>,
    right: Link<T,U>,
}

impl<T,U> BST<T,U>
    where T: Copy + Ord + Debug,
          U: Copy + Debug
{
    fn new() -> Self {
        Self {
            key: None,
```

```rust
            val: None,
            left: None,
            right: None,
        }
    }

    fn is_empty(&self) -> bool {
        self.key.is_none()
    }

    fn size(&self) -> usize {
        self.calc_size(0)
    }

    // Recursively count the number of nodes
    fn calc_size(&self, mut size: usize) -> usize {
        if self.key.is_none() { return size; }

        // Add current node count to total node count 'size'
        size += 1;
        // Count left and right child nodes
        if !self.left.is_none() {
            size = self.left.as_ref().unwrap().calc_size(size);
        }
        if !self.right.is_none() {
            size = self.right
                    .as_ref().unwrap().calc_size(size);
        }

        size
    }

    // Count leaf nodes
    fn leaf_size(&self) -> usize {
        // If both left and right are empty,
        // current node is a leaf node, return 1
        if self.left.is_none() && self.right.is_none() {
            return 1;
        }

        // Count leaf nodes in left and right subtree
        let left_leaf = match &self.left {
            Some(left) => left.leaf_size(),
            None => 0,
        };
        let right_leaf = match &self.right {
            Some(right) => right.leaf_size(),
            None => 0,
        };

        // total sum of leaf nodes
        left_leaf + right_leaf
```

```rust
    }

    // Count non-leaf nodes
    fn none_leaf_size(&self) -> usize {
        self.size() - self.leaf_size()
    }

    // Calculate tree depth
    fn depth(&self) -> usize {
        let mut left_depth = 1;
        if let Some(left) = &self.left {
            left_depth += left.depth();
        }

        let mut right_depth = 1;
        if let Some(right) = &self.right {
            right_depth += right.depth();
        }

        max(left_depth, right_depth)
    }

    fn insert(&mut self, key: T, val: U) {
        // If no data, insert directly
        if self.key.is_none() {
            self.key = Some(key);
            self.val = Some(val);
        } else {
            match &self.key {
                Some(k) => {
                    // If key exists, update val
                    if key == *k {
                        self.val = Some(val);
                        return;
                    }

                    // If no same key found,
                    // Find the subtree to insert new node
                    let child = if key < *k {
                        &mut self.left
                    } else {
                        &mut self.right
                    };

                    // Recursively go down the tree
                    // until insertion
                    match child {
                        Some(ref mut node) => {
                            node.insert(key, val);
                        },
                        None => {
                            let mut node = BST::new();
```

```rust
                            node.insert(key, val);
                            *child = Some(Box::new(node));
                        },
                    }
                },
                None => (),
            }
        }
    }

    // find the key in tree
    fn contains(&self, key: &T) -> bool {
        match &self.key {
            None => false,
            Some(k) => {
                // Compare key value and determine
                // whether to continue searching recursively
                match k.cmp(key) {
                    Equal => true, // find it
                    Greater => { // search in left subtree
                        match &self.left {
                            Some(node) => node.contains(key),
                            None => false,
                        }
                    },
                    Less => { // search in right subtree
                        match &self.right {
                            Some(node) => node.contains(key),
                            None => false,
                        }
                    },
                }
            },
        }
    }

    // get the min/max node value
    fn min(&self) -> (Option<&T>, Option<&U>) {
        // miniumun value is on the left subtree
        match &self.left {
            Some(node) => node.min(),
            None => match &self.key {
                Some(key) => (Some(&key), self.val.as_ref()),
                None => (None, None),
            },
        }
    }

    fn max(&self) -> (Option<&T>, Option<&U>) {
        // maxiumun value is on the right subtree
        match &self.right {
            Some(node) => node.max(),
```

```rust
            None => match &self.key {
                Some(key) => (Some(&key), self.val.as_ref()),
                None => (None, None),
            },
        }
    }

    // get subtree
    fn get_left(&self) -> Link<T,U> {
        self.left.clone()
    }

    fn get_right(&self) -> Link<T,U> {
        self.right.clone()
    }

    // get a value reference with parameter key
    fn get(&self, key: &T) -> Option<&U> {
        match &self.key {
            None => None,
            Some(k) => {
                match k.cmp(key) {
                    Equal => self.val.as_ref(),
                    Greater => {
                        match &self.left {
                            None => None,
                            Some(node) => node.get(key),
                        }
                    },
                    Less => {
                        match &self.right {
                            None => None,
                            Some(node) => node.get(key),
                        }
                    },
                }
            },
        }
    }
}
```

Here are the implementation of preorder, inorder, postorder, and level-order traversals.

```rust
// bst.rs

impl<T,U> BST<T,U>
    where T: Copy + Ord + Debug,
          U: Copy + Debug
{
    // Internal implementation
    fn preorder(&self) {
        println!("key: {:?}, val: {:?}",self.key, self.val);
        match &self.left {
```

```rust
            Some(node) => node.preorder(),
            None => (),
        }
        match &self.right {
            Some(node) => node.preorder(),
            None => (),
        }
    }

    fn inorder(&self) {
        match &self.left {
            Some(node) => node.inorder(),
            None => (),
        }
        println!("key: {:?}, val: {:?}",self.key, self.val);
        match &self.right {
            Some(node) => node.inorder(),
            None => (),
        }
    }

    fn postorder(&self) {
        match &self.left {
            Some(node) => node.postorder(),
            None => (),
        }
        match &self.right {
            Some(node) => node.postorder(),
            None => (),
        }
        println!("key: {:?}, val: {:?}",self.key, self.val);
    }

    fn levelorder(&self) {
        let size = self.size();
        let mut q = Queue::new(size);

        let _r = q.enqueue(Box::new(self.clone()));
        while !q.is_empty() {
            let front = q.dequeue().unwrap();
            println!("key: {:?}, val: {:?}",
                    front.key, front.val);

            match front.get_left() {
                Some(left) => { let _r = q.enqueue(left); },
                None => (),
            }
            match front.get_right() {
                Some(right) => { let _r = q.enqueue(right); },
                None => (),
            }
        }
```

```rust
    }
}

// External implementation
fn preorder<T, U>(bst: Link<T,U>)
where T: Copy + Ord + Debug,
      U: Copy + Debug
{
    if !bst.is_none() {
        println!("key: {:?}, val: {:?}",
                  bst.as_ref().unwrap().key.unwrap(),
                  bst.as_ref().unwrap().val.unwrap());
        preorder(bst.as_ref().unwrap().get_left());
        preorder(bst.as_ref().unwrap().get_right());
    }
}

fn inorder<T, U>(bst: Link<T,U>)
where T: Copy + Ord + Debug,
      U: Copy + Debug
{
    if !bst.is_none() {
        inorder(bst.as_ref().unwrap().get_left());
        println!("key: {:?}, val: {:?}",
                  bst.as_ref().unwrap().key.unwrap(),
                  bst.as_ref().unwrap().val.unwrap());
        inorder(bst.as_ref().unwrap().get_right());
    }
}

fn postorder<T, U>(bst: Link<T,U>)
where T: Copy + Ord + Debug,
      U: Copy + Debug
{
    if !bst.is_none() {
        postorder(bst.as_ref().unwrap().get_left());
        postorder(bst.as_ref().unwrap().get_right());
        println!("key: {:?}, val: {:?}",
                  bst.as_ref().unwrap().key.unwrap(),
                  bst.as_ref().unwrap().val.unwrap());
    }
}

fn levelorder<T, U>(bst: Link<T,U>)
where T: Copy + Ord + Debug,
      U: Copy + Debug
{
    if bst.is_none() { return; }

    let size = bst.as_ref().unwrap().size();
    let mut q = Queue::new(size);
    let _r = q.enqueue(bst.as_ref().unwrap().clone());
```

```rust
    while !q.is_empty() {
        let front = q.dequeue().unwrap();
        println!("key: {:?}, val: {:?}", front.key, front.val);

        match front.get_left() {
            Some(left) => { let _r = q.enqueue(left); },
            None => {},
        }

        match front.get_right() {
            Some(right) => { let _r = q.enqueue(right); },
            None => {},
        }
    }
}
```

The following are the outputs after execution of binary search tree.

```rust
// bst.rs

fn main() {
    basic();
    order();

    fn basic() {
        let mut bst = BST::<i32, char>::new();
        bst.insert(8, 'e'); bst.insert(6,'c');
        bst.insert(7, 'd'); bst.insert(5,'b');
        bst.insert(10,'g'); bst.insert(9,'f');
        bst.insert(11,'h'); bst.insert(4,'a');

        println!("bst is empty: {}", bst.is_empty());
        println!("bst size: {}", bst.size());
        println!("bst leaves: {}", bst.leaf_size());
        println!("bst internals: {}", bst.none_leaf_size());
        println!("bst depth: {}", bst.depth());

        let min_kv = bst.min();
        let max_kv = bst.max();
        println!("min key-val: {:?}-{:?}", min_kv.0, min_kv.1);
        println!("max key-val: {:?}-{:?}", max_kv.0, max_kv.1);
        println!("bst contains 5: {}", bst.contains(&5));
        println!("key: 5, val: {:?}", bst.get(&5).unwrap());
    }

    fn order() {
        let mut bst = BST::<i32, char>::new();
        bst.insert(8, 'e'); bst.insert(6,'c');
        bst.insert(7, 'd'); bst.insert(5,'b');
        bst.insert(10,'g'); bst.insert(9,'f');
        bst.insert(11,'h'); bst.insert(4,'a');

        println!("internal inorder, preorder, postorder: ");
```

```rust
        bst.inorder();
        bst.preorder();
        bst.postorder();
        bst.levelorder();
        println!("outside inorder, preorder, postorder: ");
        let nk = Some(Box::new(bst.clone()));
        inorder(nk.clone());
        preorder(nk.clone());
        postorder(nk.clone());
        levelorder(nk.clone());
    }
}
```

The following are outputs after execution.

```text
bst is empty: false
bst size: 8
bst leaves: 4
bst internals: 4
bst depth: 4
min key: Some(4), min val: Some('a')
max key: Some(11), max val: Some('h')
bst contains 5: true
key: 5, val: 'b'
internal inorder, preorder, postorder:
key: 4, val: 'a'
key: 5, val: 'b'
key: 6, val: 'c'
key: 7, val: 'd'
key: 8, val: 'e'
key: 9, val: 'f'
key: 10, val: 'g'
key: 11, val: 'h'
key: 8, val: 'e'
key: 6, val: 'c'
key: 5, val: 'b'
key: 4, val: 'a'
key: 7, val: 'd'
key: 10, val: 'g'
key: 9, val: 'f'
key: 11, val: 'h'
key: 4, val: 'a'
key: 5, val: 'b'
key: 7, val: 'd'
key: 6, val: 'c'
key: 9, val: 'f'
key: 11, val: 'h'
key: 10, val: 'g'
key: 8, val: 'e'
key: 8, val: 'e'
key: 6, val: 'c'
key: 10, val: 'g'
key: 5, val: 'b'
```

```text
key: 7, val: 'd'
key: 9, val: 'f'
key: 11, val: 'h'
key: 4, val: 'a'
outside inorder, preorder, postorder:
key: 4, val: 'a'
key: 5, val: 'b'
key: 6, val: 'c'
key: 7, val: 'd'
key: 8, val: 'e'
key: 9, val: 'f'
key: 10, val: 'g'
key: 11, val: 'h'
key: 8, val: 'e'
key: 6, val: 'c'
key: 5, val: 'b'
key: 4, val: 'a'
key: 7, val: 'd'
key: 10, val: 'g'
key: 9, val: 'f'
key: 11, val: 'h'
key: 4, val: 'a'
key: 5, val: 'b'
key: 7, val: 'd'
key: 6, val: 'c'
key: 9, val: 'f'
key: 11, val: 'h'
key: 10, val: 'g'
key: 8, val: 'e'
key: 8, val: 'e'
key: 6, val: 'c'
key: 10, val: 'g'
key: 5, val: 'b'
key: 7, val: 'd'
key: 9, val: 'f'
key: 11, val: 'h'
key: 4, val: 'a'
```

When insert 76 into the tree, its search path is shown by the black nodes.

![Figure 8.6: Insertion into a BST](images/fig-8.6.png)

*Figure 8.6: Insertion into a BST*

Deleting a node in a binary search tree is a complex operation. The first step is to find the node to be deleted, which may not exist in the tree. Once the node is found, we need to determine if it has children, which can be one of three cases: no children, one child, or two children.

**Table 8.4: Key deletion cases**

| No | Node | node k | delete mothod |
| --- | --- | --- | --- |
| 1 | No node | None | Directly return |
| 2 | One root node | None | Directly delete |
| 3 | Multiple nodes | None | Directly delete |
| 4 | Multiple nodes | One child | Replace k with child node |
| 5 | Multiple nodes | Two children | Replace k with the successor node |

If the node is a leaf node with no children, we can simply remove its reference from its parent node. If it has one child, we modify the parent node’s reference to point directly to the child node. The most challenging case is when the node has two children. In this case, we find the minimum node in the right subtree, called the successor node, and replace the node to be deleted with the successor node. The successor node may also have children, and we must adjust their relationships accordingly. The specific situations are shown in the following figure, where the dashed box represents the node k to be deleted, and the binary tree obtained after deleting the node is shown on the right.

70 70 leaf node 31 93 31 93 14 73 94 14 73 94 23 76 23 70 70 one child node 31 93 93 14 14 73 94 23 73 94 23 76 70 70 two child nodes 31 93 31 76 73 94 73 94 14 14 23 76 23

Deleting a leaf node is the simplest case, while deleting an internal node with one child is straightforward. The most difficult case is when the node has two children, as this requires adjusting the relationships of multiple nodes.

### 8.4.3 Analysis of Binary Search Tree

Now that the binary search tree has been fully implemented, let’s analyze the time complexity of each method. Traversals and len() both have a time complexity of O(n) since they need to process all n elements. The contains() method compares data with the left and right child nodes and selects a branch based on the result. It walks the longest path from the root to the leaf node at most. The height of a binary tree is related to the total number of nodes. 20 + 21 + 2i... + 2h = n

(8.1) h = log2(n)

Using the binary tree properties, we can approximate the maximum path length to be h = log2(n). Thus, the time complexity of contains() is O(log2(n)). Insertion, deletion, and modification are based on search because the element must be located before processing can continue. Their time complexity depends only on search and can be completed in constant time. Therefore, the performance of contains(), insert(), and get() methods are all O(log2(n)). The height h of the binary tree is the limiting factor of their performance. If the inserted data is always in a sorted state, the binary tree may degenerate into a linear linked list, and the performance of contains(), insert(), and remove() methods will be O(n). The figure below illustrates this scenario.

![Figure 8.7: bst in a linear linked list](images/fig-8.7.png)

*Figure 8.7: bst in a linear linked list*

In this section, we did not implement the remove() function because it is not part of the abstract data type definition, and binary search trees are primarily used for data insertion and search, not deletion. However, interested readers can try to implement the remove() function as an exercise. To improve performance by reducing the tree height, we can convert the binary tree into a multi-way tree such as B-trees and B+ trees. These trees have many child nodes, resulting in a short tree height and fast queries. They are commonly used in implementing databases and file systems. For instance, MySQL database uses B+ trees to store data, with nodes of 16K memory pages. If each data is 1k in size, one node can store 16 pieces of data. When used to store an index with a bigint key, 8 bytes are used, and the index is 6 bytes, for a total of 14 bytes. Thus, one node can store approximately 16∗1024/14 = 1170 indexes. With a height of 3, a B+ tree can store around 1170∗1170∗16 = 21902400 indexes, which can hold about 20 million pieces of data. Retrieving data only requires at most two queries, which explains why database queries are fast. Readers interested in this topic can read MySQL-related books to learn more.
