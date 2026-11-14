## 8.5 Balanced Binary Search Tree

In the previous section, we constructed a binary search tree and learned that its performance can degrade to O(n) in certain cases, such as when the tree is unbalanced with one side having significantly more nodes than the other. This inefficiency can lead to poor subsequent operations. To ensure efficient data processing, building a balanced binary tree is essential. In this section, we will discuss an AVL tree,

a balanced binary search tree that can automatically maintain balance. It is named after its inventors: G.M. Adelson-Velskii and E.M.Land. The AVL tree is also an ordinary binary search tree, but with a difference in the way the tree operations are performed. AVL trees use a balance factor to determine if the tree is balanced during operations. The balance factor is the difference in height between the left and right subtrees of a node, and it is defined as: balanceFactor = height(leftSubTree) −height(rightSubTree)

(8.2)

Given this balance factor definition, if the balance factor is greater than zero, then the left subtree is heavy. If it is less than zero, then the right subtree is heavy, and if it is zero, then the tree is balanced. To implement an AVL tree efficiently, balance factors of -1, 0, and 1 are all considered balanced because the difference in height between the left and right subtrees is only 1 in these cases, which is essentially balanced. Once a node’s balance factor is outside this range, such as 2 or -2, the tree needs to be rotated to maintain balance. The following figure illustrates the case of unbalanced left and right subtrees, and each node’s balance factor is indicated by its value.

-2 0 -1 0 -1 0

### 8.5.1 AVL Tree

To ensure a balanced binary tree, it is crucial to fulfill the balance factor condition, which allows for only three possible cases: left-heavy, balanced, or right-heavy. It is worth noting that a left-heavy or rightheavy tree that still meets the condition of having a balance factor of -1, 0, or 1 can also be considered balanced. The figure below depicts the most imbalanced left-heavy tree that meets the balance factor condition for trees of height 0, 1, 2, and 3.

0 1 1 1 0 0 1 1 1 0 1 0 0 0

By analyzing the total number of nodes in the tree, we can derive a formula for the number of nodes in a tree of height h, as follows: For a tree of height 0, there is only one node; for a tree of height 1, there are 2 nodes; for a tree of height 2, there are 4 nodes; for a tree of height 3, there are 7 nodes, and so on. Nh = 1 + Nh−1 + Nh−2

(8.3)

Remarkably, this formula resembles the Fibonacci sequence. With the number of nodes in the tree, we can obtain the height formula for an AVL tree using the Fibonacci equation, where the ith Fibonacci

number is given by the following equation:

F0 = 0 F1 = 1 (8.4)

Fi = Fi−1 + Fi−2 To calculate the number of nodes in an AVL tree, we can use the following formula where F0 = 1. Nh = Fh+2 −1

(8.5) √

As i increases, the ratio Fi/Fi−1 approaches the golden ratio Φ = (1 +

5)/2, so Φ can be used to

represent Fi, which can be calculated as Fi = Φi

5 . Nh = Φh √ 5 + 1 (8.6)

Based on these formulas, we can derive a height formula for AVL trees. log(Nh −1) = log( Φh

√ 5)

log(Nh −1) = hlogΦ −1

2log5 (8.7)

h = log(Nh −1) + 1

2log5 logΦ

h = 1.44log(Nh) In this formula, h is the height of the AVL tree, and Nh is the number of nodes. This implies that the height of an AVL tree is at most 1.44 times the logarithm of the number of nodes, and the search complexity is O(logN), which is highly efficient.

### 8.5.2 Implementing a AVL Tree in Rust

To insert a new node into an AVL tree, we first add it as a leaf node, which automatically gives it a balance factor of 0. However, the balance factor of the parent node will need to be updated, depending on whether the new node is a left or right child. If it is a right child, the parent node’s balance factor will be reduced by 1, and if it is a left child, the balance factor will be increased by 1. This update is propagated up the tree recursively, until we reach the root or a node whose balance factor becomes 0. In our implementation, we represent the AVL tree as an enumeration with two cases: Null, which represents an empty tree, and Tree, which represents a node in the tree. The AvlNode type is used to store the data, left and right subtrees, and balance factor of each node.

```rust
// avl.rs

// Use a enum to define the Avl tree
#[derive(Clone, Debug, PartialEq)]
enum AvlTree<T> {
    Null,
    Tree(Box<AvlNode<T>>),
}

// Definish of Avl tree node
#[derive(Debug)]
struct AvlNode<T> {
```

```text
    key: T,
    left: AvlTree<T>, // left subtree
    right: AvlTree<T>, // right subtree
    bfactor: i8, // balance factor
}
```

To implement the AVL tree, we need to add two functions: insert and rebalance. To compare node data, we also introduce a comparison property called Ording. Additionally, we need the replace and max functions to update values and calculate the tree height.

```rust
// avl.rs

use std::cmp::{max, Ordering::*};
use std::fmt::Debug;
use std::mem::replace;
use AvlTree::*;

impl<T> AvlTree<T> where T : Clone + Ord + Debug {
    // new tree is Empty
    fn new() -> AvlTree<T> {
        Null
    }

    fn insert(&mut self, key: T) -> (bool, bool) {
        let ret = match self {
            Null => {
                // If there is no node, insert directly
                let node = AvlNode {
                    key: key,
                    left: Null,
                    right: Null,
                    bfactor: 0,
                };
                *self = Tree(Box::new(node));

                (true, true)
            },
            Tree(ref mut node) => match node.key.cmp(&key) {
                // Compare the value of the node and determine
                // which side to insert from
                // inserted: whether insertion is performed
                // deepened: whether the depth is increased

                // If they are equal, no insertion is needed
                Equal => (false, false),
                // node value is smaller, insert to the right
                Less => {
                    let (inserted, deepened)
                        = node.right.insert(key);
                    if deepened {
                        let ret = match node.bfactor {
                            -1 => (inserted, false),
                             0 => (inserted, true),
```

```rust
                             1 => (inserted, false),
                             _ => unreachable!(),
                        };
                        node.bfactor += 1;

                        ret
                    } else {
                        (inserted, deepened)
                    }
                },
                // node value is greater, insert to the left
                Greater => {
                    let (inserted, deepened)
                        = node.left.insert(key);
                    if deepened {
                        let ret = match node.bfactor {
                            -1 => (inserted, false),
                             0 => (inserted, true),
                             1 => (inserted, false),
                             _ => unreachable!(),
                        };
                        node.bfactor -= 1;

                        ret
                    } else {
                        (inserted, deepened)
                    }
                },
            },
        };
        self.rebalance();

        ret
    }

    // Adjust the balance factors of each node
    fn rebalance(&mut self) {
        match self {
            // If there is no data, no adjustment is needed
            Null => (),
            Tree(_) => match self.node().bfactor {
                // If the right subtree is heavy
                -2 => {
                    let lbf = self.node()
                                  .left
                                  .node()
                                  .bfactor;

                    if lbf == -1 || lbf == 0 {
                        let (a, b) = if lbf == -1 {
                            (0, 0)
                        } else {
```

```rust
                            (-1,1)
                        };

                        // Rotate and update the balance factor
                        self.rotate_right();
                        self.node().right.node().bfactor = a;
                        self.node().bfactor = b;
                    } else if lbf == 1 {
                        let (a, b) = match self.node()
                                               .left.node()
                                               .right.node()
                                               .bfactor
                        {
                            -1 => (1, 0),
                             0 => (0, 0),
                             1 => (0,-1),
                             _ => unreachable!(),
                        };

                        // First rotate left, then rotate right
                        // finally update the balance factor
                        self.node().left.rotate_left();
                        self.rotate_right();
                        self.node().right.node().bfactor = a;
                        self.node().left.node().bfactor = b;
                        self.node().bfactor = 0;
                    } else {
                        unreachable!()
                    }
                },
                // If the left subtree is heavy
                2 => {
                     let rbf=self.node().right.node().bfactor;
                     if rbf == 1 || rbf == 0 {
                         let (a, b) = if rbf == 1 {
                            (0, 0)
                         } else {
                            (1,-1)
                         };

                         self.rotate_left();
                         self.node().left.node().bfactor = a;
                         self.node().bfactor = b;
                     } else if rbf == -1 {
                        let (a, b) = match self.node()
                                               .right.node()
                                               .left.node()
                                               .bfactor
                        {
                             1 => (-1,0),
                             0 => (0, 0),
                            -1 => (0, 1),
```

```text
                             _ => unreachable!(),
                        };

                        // First rotate right, then rotate left
                        // finally update the balance factor
                        self.node().right.rotate_right();
                        self.rotate_left();
                        self.node().left.node().bfactor = a;
                        self.node().right.node().bfactor = b;
                        self.node().bfactor = 0;
                     } else {
                         unreachable!()
                     }
                },
                _ => (),
            },
        }
    }
}
```

The insert function updates the balance factor recursively, while the rebalance function restores balance to the AVL tree. Effective rebalancing is crucial for maintaining proper AVL tree functionality without compromising performance. Rebalancing involves rotating the tree once or multiple times, which can be done through left or right rotations. To perform a left rotation, we can follow the steps shown in Figure (8.8): (1) Promote the right child (B) as the new root of the subtree. (2) Move the old root (A) to the left child of the new root. (3) If the new root (B) already has a left child, make it the right child of the new left child (A). Similarly, to perform a right rotation, we can follow these steps: (1) Promote the left child (B) as the new root of the subtree. (2) Move the old root (A) to the right child of the new root. (3) If the new root (B) already has a right child, make it the left child of the new right child (A). The two trees in the figure are unbalanced, and we can rebalance them into the tree on the right by performing left and right rotations with A as the root.

![Figure 8.8: Unbalanced tree and its rotations](images/fig-8.8.png)

*Figure 8.8: Unbalanced tree and its rotations*

To perform rotations on a subtree, we can use left and right rotation rules. However, sometimes after performing one rotation, the balance may still be lost in the opposite direction.

C A -2 2 left rotation C A 1 -1 B B 0 0

In such cases, new rotation rules need to be used as follows:

- To balance a subtree with left rotation, we first check the balance factor of the right child node. If the right child is heavy, we perform a right rotation on it, and then a left rotation.
- Similarly, to balance a subtree with right rotation, we first check the balance factor of the left child node. If the left child is heavy, we perform a left rotation on it, and then a right rotation.

Although the process of subtree rotation is easy to understand conceptually, its code implementation can be complex because of the need to move nodes in the correct order while preserving all properties of the binary search tree. Additionally, ownership mechanisms in Rust make moving nodes and updating pointer relationships prone to errors. To implement rotation functions, we use node and subtree retrieval functions such as left_subtree and right_subtree.

```rust
// avl.rs

impl<T> AvlTree<T> where T : Ord {
    // get a avlNode
    fn node(&mut self) -> &mut AvlNode<T> {
        match self {
            Null => panic!("Empty tree"),
            Tree(node) => node,
        }
    }

    // get the left/right subtrees
    fn left_subtree(&mut self) -> &mut Self {
        match self {
            Null => panic!("Error: Empty tree!"),
            Tree(node) => &mut node.left,
        }
    }

    fn right_subtree(&mut self) -> &mut Self {
        match self {
            Null => panic!("Error: Empty tree!"),
            Tree(node) => &mut node.right,
        }
    }

    fn rotate_left(&mut self) {
        let mut n = replace(self, Null);
        let mut right = replace(n.right_subtree(), Null);
        let right_left = replace(right.left_subtree(), Null);
        *n.right_subtree() = right_left;
```

```rust
        *right.left_subtree() = n;
        *self = right;
    }

    fn rotate_right(&mut self) {
        let mut n = replace(self, Null);
        let mut left = replace(n.left_subtree(), Null);
        let left_right = replace(left.right_subtree(), Null);
        *n.left() = left_right;
        *left.right_subtree() = n;
        *self = left;
    }
}
```

To maintain the balance of the tree, we can perform rotation operations. However, we also need to implement methods to obtain important information about the tree, such as the number of nodes, node values, tree height, minimum and maximum values, and node queries. This requires implementing methods such as size, leaf_size, depth, node, min, max, and contains for the balanced binary tree.

```rust
// avl.rs

impl<T> AvlTree<T> where T : Ord {
    // Calculate the nodes number: number of left and right
    // child nodes + root node, calculated recursively
    fn size(&self) -> usize {
        match self {
            Null => 0,
            Tree(n) => 1 + n.left.size() + n.right.size(),
        }
    }

    // Calculate the leaf nodes number: calculated recursively
    fn leaf_size(&self) -> usize {
        match self {
            Null => 0,
            Tree(node) => {
                if node.left == Null && node.right == null {
                    return 1;
                }
                let left_leaf = match node.left {
                    Null => 0,
                    _ => node.left.leaf_size(),
                };
                let right_leaf = match node.right {
                    Null => 0,
                    _ => node.right.leaf_size(),
                };
                left_leaf + right_leaf
            },
        }
    }

    // Calculate the number of non-leaf nodes
```

```rust
    fn none_leaf_size(&self) -> usize {
      self.size() - self.leaf_size()
    }

    // The depth of the tree is the maximum depth of the left
    // and right subtrees plus one, calculated recursively
    fn depth(&self) -> usize {
        match self {
          Null => 0,
          Tree(n) => max(n.left.depth(),n.right.depth()) + 1,
        }
    }

    fn is_empty(&self) -> bool {
        match self {
            Null => true,
            _ => false,
        }
    }

    // Get the maximum and minimum node values of the tree
    fn min(&self) -> Option<&T> {
        match self {
            Null => None,
            Tree(node) => {
                match node.left {
                    Null => Some(&node.key),
                    _ => node.left.min(),
                }
            },
        }
    }

    fn max(&self) -> Option<&T> {
        match self {
            Null => None,
            Tree(node) => {
                match node.right {
                    Null => Some(&node.key),
                    _ => node.right.min(),
                }
            },
        }
    }

    // determine if key is in the tree
    fn contains(&self, key: &T) -> bool {
        match self {
            Null => false,
            Tree(n) => {
                match n.key.cmp(&key) {
                    Equal => { true },
```

```rust
                    Greater => {
                        match &n.left {
                            Null => false,
                            _ => n.left.contains(key),
                        }
                    },
                    Less => {
                        match &n.right {
                            Null => false,
                            _ => n.right.contains(key),
                        }
                    },
                }
            },
        }
    }
}
```

In addition to these methods, we can implement the four traversal methods commonly used for binary trees: inorder, preorder, postorder, and levelorder. These traversal methods allow us to visit and manipulate each node in the tree in a specific order, which can be useful in various scenarios such as printing the tree, searching for a specific node, or computing some statistics about the tree.

```rust
// avl.rs

impl<T> AvlTree<T> where T : Ord {
    // Internal implementation of preorder, inorder, postorder,
    // and level-order traversal
    fn preorder(&self) {
        match self {
            Null => (),
            Tree(node) => {
                println!("key: {:?}", node.key);
                node.left.preorder();
                node.right.preorder();
            },
        }
    }

    fn inorder(&self) {
        match self {
            Null => (),
            Tree(node) => {
                node.left.inorder();
                println!("key: {:?}", node.key);
                node.right.inorder();
            },
        }
    }

    fn postorder(&self) {
        match self {
            Null => (),
```

```rust
            Tree(node) => {
                node.left.postorder();
                node.right.postorder();
                println!("key: {:?}", node.key);
            },
        }
    }

    fn levelorder(&self) {
        let size = self.size();
        let mut q = Queue::new(size);

        let _r = q.enqueue(self);
        while !q.is_empty() {
            let front = q.dequeue().unwrap();
            match front {
                Null => (),
                Tree(node) => {
                    println!("key: {:?}", node.key);
                    let _r = q.enqueue(&node.left);
                    let _r = q.enqueue(&node.right);
                },
            }
        }
    }
}

// External implementation of preorder, inorder, postorder,
// and level-order traversal
fn preorder<T: Clone + Ord + Debug>(avl: &AvlTree<T>) {
    match avl {
        Null => (),
        Tree(node) => {
            println!("key: {:?}", node.key);
            preorder(&node.left);
            preorder(&node.right);
        },
    }
}

fn inorder<T: Clone + Ord + Debug>(avl: &AvlTree<T>) {
    match avl {
        Null => (),
        Tree(node) => {
            inorder(&node.left);
            println!("key: {:?}", node.key);
            inorder(&node.right);
        },
    }
}

fn postorder<T: Clone + Ord + Debug>(avl: &AvlTree<T>) {
```

```rust
    match avl {
        Null => (),
        Tree(node) => {
            postorder(&node.left);
            postorder(&node.right);
            println!("key: {:?}", node.key);
        },
    }
}

fn levelorder<T: Clone + Ord + Debug>(avl: &AvlTree<T>) {
    let size = avl.size();
    let mut q = Queue::new(size);
    let _r = q.enqueue(avl);
    while !q.is_empty() {
        let front = q.dequeue().unwrap();
        match front {
            Null => (),
            Tree(node) => {
                println!("key: {:?}", node.key);
                let _r = q.enqueue(&node.left);
                let _r = q.enqueue(&node.right);
            },
        }
    }
}

fn main() {
    basic();
    order();

    fn basic() {
        let mut t = AvlTree::new();
        for i in 0..5 { let (_r1, _r2) = t.insert(i); }

        println!("empty:{},size:{}",t.is_empty(),t.size());
        println!("leaves:{},depth:{}",t.leaf_size(),t.depth());
        println!("internals:{}",t.none_leaf_size());
        println!("min-max key:{:?}-{:?}",t.min(), t.max());
        println!("contains 9:{}",t.contains(&9));
    }

    fn order() {
        let mut avl = AvlTree::new();
        for i in 0..5 { let (_r1, _r2) = avl.insert(i); }

        println!("internal pre-in-post-level order");
        avl.preorder(); avl.inorder();
        avl.postorder(); avl.levelorder();
        println!("outside pre-in-post-level order");
        preorder(&avl); inorder(&avl);
        postorder(&avl); levelorder(&avl);
```

```text
    }
}
```

The following are outputs afterr execution.

```text
empty:false,size:5
leaves:3,depth:3
internals:2
min-max key:Some(0)-Some(4)
contains 9:false
internal pre-in-pos-level order
key: 1
key: 0
key: 3
key: 2
key: 4
key: 0
key: 1
key: 2
key: 3
key: 4
key: 0
key: 2
key: 4
key: 3
key: 1
key: 1
key: 0
key: 3
key: 2
key: 4
outside pre-in-pos-level order
key: 1
key: 0
key: 3
key: 2
key: 4
key: 0
key: 1
key: 2
key: 3
key: 4
key: 0
key: 2
key: 4
key: 3
key: 1
key: 1
key: 0
key: 3
key: 2
key: 4
```

### 8.5.3 Analysis of AVL Tree

An AVL balanced binary tree includes a rebalancing function and left and right rotation operations to maintain its balance, which enables its operations to maintain a relatively good performance with a worstcase complexity of O(log2(n)). However, it is important to note that AVL trees perform a significant number of rotation operations to maintain balance. A red-black tree is an optimized binary tree that requires fewer rotations compared to an AVL tree. It is a weakened version of the AVL tree and can be used in scenarios with frequent insertions, deletions, and modifications to achieve better performance.
