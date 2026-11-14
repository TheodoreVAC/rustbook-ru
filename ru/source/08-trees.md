# Trees

## 8.1 Objectives

- Understanding trees and their usage.
- Implementing a priority queue using a binary heap.
- Understanding binary search trees and balanced binary trees.
- Implementing binary search trees and balanced binary trees.

## 8.2 What is Tree?

In previous chapters, we covered linear data structures such as stacks, queues, and linked lists, where each data item is connected to the next one.

a c e b d

A tree is a new data structure that expands upon this linear structure by connecting multiple data items.

a c b e d g f

Like a natural tree, this data structure has a root, branches, and leaves, which are interconnected. Trees are used in various fields of computer science, such as operating systems, graphics, databases, and computer networks. Throughout the rest of the text, we will refer to this data structure as a ”tree.”

Before delving into trees, it’s essential to understand some common tree examples, such as a biological classification tree. From this graph, we can see the specific location of entry ’People’ (lower left), which is very helpful for studying relationships and properties. This type of tree is hierarchical, with well-defined structures comprising seven levels: kingdom, phylum, class, order, family, genus, and species. The highest level represents the most abstract concept, while the lowest level represents the most specific. By starting from the root of the tree and following the arrows to the bottom, we can obtain a complete path that indicates the full name of a species. Organisms can find their place on this tree of life, displaying their relative relationships. For instance, the complete name of the ”human” species is ”animal kingdom-chordate phylum-mammal class-primate order-hominidae family-homo genus-homo sapiens species.” Each node’s set of child nodes is independent of another node’s set of child nodes, which makes the relationships between nodes clear. This property also means that modifying one node’s child nodes will not affect other nodes. It is especially useful when trees are used as data storage containers, as it allows tools to modify data on specific nodes while keeping other data unchanged. Lastly, each leaf node is unique, and there is only one unique path from the root to each leaf node. This property makes data storage efficient since the unique path can be used as a storage path. The file system in our computers is based on an improved tree structure. The file system tree and biological classification tree have many similarities, and the path from the root directory to any subdirectory uniquely identifies

that subdirectory and all files within it. If you’re familiar with Unix-like operating systems, you should recognize paths like /root, /home/user, and /etc as nodes on a tree, where / is the root node. Trees can also be used to represent web page files, which are collections of resources that have a hierarchical structure. For example, the web page data of Google.cn’s search interface shows that the <> tag elements are also arranged hierarchically.

```text
<html lang="zh"><head><meta charset="utf-8">
  <head>
      <meta charset="utf-8">
      <title>Google</title>
      <style>
        html { background: #fff; margin: 0 1em; }
        body { font: .8125em/1.5 arial, sans-serif; }
      </style>
  </head>
  <body>
  <div>
    <h1><a href="http://www.google.com.hk/webhp?hl=zh-CN">
        <strong id="target">google.com.hk</strong></a></h1>
    <p>Please save our website</p>
  </div>
  <ul>
    <li><a href="http://translate.google.cn/">translate</a></li
       > </ul>
  </body>
</html>
```

In web page files, the HTML root encapsulates all the other elements, as illustrated in the diagram below. This hierarchical structure allows web pages to be displayed in a consistent manner across different devices and browsers. By using trees to represent web page files, we can efficiently store and retrieve data and modify individual elements without affecting the entire page’s layout.

### 8.2.1 Vocabularies and Definitions of Tree

After discussing some examples of trees, we will now define the various properties of a tree.

- Node: A node is the fundamental unit of a tree, consisting of a ”key” name and an optional ”payload” information. Payload information is not always necessary for tree algorithms, but it is typically important in applications that require additional information on nodes, such as file names, file content, or timestamps.
- Root: The root is the top-level node in a tree, with no incoming edges. All nodes in a tree can be reached by following edges from the root. This is analogous to the concepts of the / or C drive in an operating system.
- Edge: An edge connects two nodes and represents the relationship between them. Every node in a tree, except the root, has exactly one incoming edge and potentially several outgoing edges. An edge defines a path that can be used to locate a specific node.
- Path: A path is a sequence of edges that connect nodes. It is not a structure in itself, but rather an associative relationship that emerges from the logical arrangement of edges. For instance, /home/user/files/sort.rs is a path that identifies the location of the file sort.rs.
- Child Node: A child node is a node that is one level below another node, originating from the same parent node. For example, sort.rs is a child node of files/. Child nodes are not unique, and there may be zero, one, or many child nodes, similar to the parent-child relationship in human society. Hence, child nodes are often named after kinship terms.
- Parent Node: A parent node is a node from which all lower-level nodes originate. For instance, files/ is the parent node of sort.rs. The parent node is unique, as a child can only have one parent.
- Subtree: A subtree is a set of nodes and edges that consists of a parent node and all its descendants. Since a tree is a recursive structure, taking any node from the tree creates a new subtree.
- Leaf Node: A leaf node is a node without child nodes, at the bottom level of the tree.
- Internal Node: An internal node has child nodes and a parent node.
- Depth: The depth of a node is the number of edges traversed from the root to that node. The depth of the root node is zero. In /home/user/files, the depth of files is 2. A depth of zero does not mean that there is no depth, but rather the depth is zero, indicating the first level.
- Height: The height of a tree is the maximum depth of any node in the tree.

To define a tree, we start with the foundational knowledge presented above:

- A tree has a root node, which is the topmost node in the hierarchy.
- Each node, except for the root node, is connected to a parent node and may have zero or more child nodes, forming a branching structure.
- The path from the root node to any other node in the tree is unique, meaning there is only one path to reach that node.

The following image shows an example of a tree structure with left and right child nodes labeled as ”lc” and ”rc,” respectively. As trees are recursive structures, the structure of a subtree is the same as that of its parent node.

![Figure 8.1: tree](images/fig-8.1.png)

*Figure 8.1: tree*

### 8.2.2 Tree Representation

Trees are a powerful non-linear data structure, but representing them in a computer requires linear data structures. One common approach to representing a tree is using an array. In this approach, the elements of the tree are stored in an array, with the root at the first index and the child nodes following in a logical order.

```text
tree = [ 'a',
          ['b',
            ['c',[],[]],
            ['d',[],[]],
          ],
          ['e',
            ['f',[],[]],
            []
          ],
       ]
```

Array access methods can be used to access the tree elements, making it easy to obtain subtrees and elements. However, this approach becomes cumbersome and impractical for larger trees with many levels, as accessing deeper nodes requires complex nested access methods.

```rust
println!("root {:?}", tree[0]);
println!("left subtree {:?}", tree[1]);
println!("right subtree {:?}", tree[2]);
```

An alternative approach to representing trees is to use nodes. In this approach, each node in the tree is represented by an object or a struct, which stores the node’s key and payload information, as well as links to its child nodes. The links between nodes form the edges of the tree. This approach is similar to the linked list data structure, where each node has a link to the next node. The node-based representation of a tree is more flexible than the array-based approach and can handle larger trees with ease. The figure below shows an example of a binary tree represented using nodes.

a c b e d f

This structure is straightforward and avoids the complexity of nested arrays for accessing elements. The key now is how to define tree nodes. One feasible method is to use the struct to define a node.

```rust
use std::cmp::{max, Ordering::*};
use std::fmt::{Debug, Display};

// Binary tree child node link
type Link<T> = Option<Box<BinaryTree<T>>>;

// Binary tree definition
```

```rust
#[derive(Debug, Clone, PartialEq)]
struct BinaryTree<T> {
    key: T, // data storage
    left: Link<T>, // left child node address storage
    right: Link<T>, // right child node address storage
}
```

The struct has a key that stores data and left and right pointers that store the addresses of the left and right child nodes.

```rust
// binary_tree.rs

impl<T: Clone + Ord + ToString + Debug> BinaryTree<T> {
    fn new(key: T) -> Self {
        Self { key: key, left: None, right: None }
    }

    // New child node is added as the
    // left child node of the root node
    fn insert_left_tree(&mut self, key: T) {
        if self.left.is_none() {
            let node = BinaryTree::new(key);
            self.left = Some(Box::new(node));
        } else {
            let mut node = BinaryTree::new(key);
            node.left = self.left.take();
            self.left = Some(Box::new(node));
        }
    }

    // New child node is added as the
    // right child node of the root node
    fn insert_right_tree(&mut self, key: T) {
        if self.right.is_none() {
            let node = BinaryTree::new(key);
            self.right = Some(Box::new(node));
        } else {
            let mut node = BinaryTree::new(key);
            node.right = self.right.take();
            self.right = Some(Box::new(node));
        }
    }
}
```

When inserting a new child node into a tree, there are two possible cases to consider. The first case is when the node has no child nodes, in which case the new node can be directly inserted as its child. The second case is when the node already has child nodes, in which case the new node’s child nodes must first be attached to the appropriate positions in the tree before the new node itself can be added as a child of the original node. The code defining the tree nodes may be confusing since it uses the term ”BinaryTree” instead of ”Node.” However, when multiple nodes are linked together to form a tree, the entire subtree can be considered a single node, which simplifies the insertion process. It is important to note, however, that the internal structure of the node is still relevant, so it is written as ”BinaryTree” rather than ”Node.”

Nonetheless, either term can be used to implement the tree. Below is the code for calculating the number of different types of nodes and the depth of the tree.

```rust
// binary_tree.rs

impl<T: Clone + Ord + ToString + Debug> BinaryTree<T> {
    // calculate total node number
    fn size(&self) -> usize {
        self.calc_size(0)
    }

    fn calc_size(&self, mut size: usize) -> usize {
        size += 1;

        if !self.left.is_none() {
            size =self.left.as_ref().unwrap().calc_size(size);
        }
        if !self.right.is_none() {
            size =self.right.as_ref().unwrap().calc_size(size);
        }

        size
    }

    // calculate the total leaf nodes number
    fn leaf_size(&self) -> usize {
        // both left and right nodes are none
        // which means current node is a leaf node
        if self.left.is_none() && self.right.is_none() {
            return 1;
        }

        // calculate the total leaf nodes of
        // both left and right substrees
        let left_leaf = match &self.left {
            Some(left) => left.leaf_size(),
            None => 0,
        };
        let right_leaf = match &self.right {
            Some(right) => right.leaf_size(),
            None => 0,
        };

        // leaf nodes = leaf nodes(left) + leaf nodes(right)
        left_leaf + right_leaf
    }

    // calculate non-leaf nodes,
    // it is actually very easy to calculate
    fn none_leaf_size(&self) -> usize {
        self.size() - self.leaf_size()
    }
```

```rust
    // calculate the depth of a tree
    fn depth(&self) -> usize {
        let mut left_depth = 1;
        if let Some(left) = &self.left {
            left_depth += left.depth();
        }

        let mut right_depth = 1;
        if let Some(right) = &self.right {
            right_depth += right.depth();
        }

        // return the max depth
        max(left_depth, right_depth)
    }
}
```

To manipulate the data of a binary tree node, you need to implement methods for accessing the left and right child nodes, setting and getting the root node value, and modifying node values. Additionally, methods for determining the existence of a node value and finding the maximum and minimum node values can also be helpful.

```rust
// binary_tree.rs

impl<T: Clone + Ord + ToString + Debug> BinaryTree<T> {
    // get left subtree
    fn get_left(&self) -> Link<T> {
        self.left.clone()
    }

    fn get_right(&self) -> Link<T> {
        self.right.clone()
    }

    // get and set key
    fn get_key(&self) -> T {
        self.key.clone()
    }

    fn set_key(&mut self, key: T) {
        self.key = key;
    }

    // find min/max key in the tree
    fn min(&self) -> Option<&T> {
        match self.left {
            None => Some(&self.key),
            Some(ref node) => node.min(),
        }
    }

    fn max(&self) -> Option<&T> {
```

```rust
        match self.right {
            None => Some(&self.key),
            Some(ref node) => node.max(),
        }
    }

    // determine whether a key is in the tree
    fn contains(&self, key: &T) -> bool {
        match &self.key.cmp(key) {
            Equal => true,
            Greater => {
                match &self.left {
                    Some(left) => left.contains(key),
                    None => false,
                }
            },
            Less => {
                match &self.right {
                    Some(right) => right.contains(key),
                    None => false,
                }
            },
        }
    }
}
```

### 8.2.3 Parse Tree

The following is an explanation of how a binary tree can be used to store data, using the example of storing the expression (1 + (2 * 3)). The expression is fully parenthesized, which indicates the order of operations. The tree structure that corresponds to this expression is shown in the accompanying diagram.

+ 1 * 3 2

To store data in the tree, we follow certain rules based on the tree’s structure. These rules are as follows:

- If the current symbol is (, a new node is added as the left child node, and we descend to that node.
- If the current symbol is one of ”+”, ”-”, ”*”, or ”/”, we set the root value to that symbol, add a new right child node, and descend to the right child node.
- If the current symbol is a number, we set the root value to that number and return to the parent node.
- If the current symbol is ), we return to the parent node of the current node.

To convert the mathematical expression (1 + (2 * 3)) into the tree shown in the figure, we can use the data storage rules defined for the tree. The specific steps are as follows: (1) Create the root node. (2) Read the symbol (, create a new left child node, and descend to the node. (3) Read the symbol 1, set the node value to 1, and return to the parent node. (4) Read the symbol +, set the node value to +, create a new right child node, and descend to the node. (5) Read the symbol (, create a new left child node, and descend to the node. (6) Read the symbol 2, set the node value to 2, and return to the parent node. (7) Read the symbol *, set the node value to *, create a new right child node, and descend to the node. (8) Read the symbol 3, set the node value to 3, and return to the parent node. (9) Read the symbol ), return to the parent node. Using a tree allows for the storage of the arithmetic expression while maintaining the structural information of the data. In fact, programming languages use trees to store all code during compilation and generate abstract syntax trees. By analyzing the functionality of each part of the syntax tree, intermediate code is generated, optimized, and then final code is generated. If you understand the principles of compilation, this should be familiar to you.

### 8.2.4 Tree Traversals

The purpose of data storage is to efficiently perform operations such as adding, deleting, searching, and modifying data. In a tree structure, locating a specific node is essential to perform these operations. However, unlike linear data structures that can be traversed using indexes, trees are nonlinear structures, so the search method is different. To access nodes in a tree, there are three commonly used methods that differ in the order in which nodes are visited. These methods are pre-order traversal, in-order traversal, and post-order traversal, and they are analogous to the traversal methods of linear data structures. To illustrate these methods, imagine this book as a tree with the table of contents as the root, each chapter as its child nodes, and each subsection as the child nodes of their respective chapters. Pre-order traversal is the first method, and it starts from the root node, then moves to the left subtree, and finally the right subtree. To traverse a tree algorithmically using pre-order traversal, recursively call the pre-order traversal method on the left subtree from the root node. For example, in the book tree described above, the pre-order traversal algorithm visits the table of contents first, followed by chapter 1, section 1, section 2, and so on. Once chapter 1 is finished, the algorithm returns to the table of contents and recursively calls pre-order traversal on chapter 2, visiting chapter 2, section 1, section 2, and so on.

The pre-order traversal algorithm is simple and can be implemented as an internal method or an external function.

```rust
// binary_tree.rs

impl<T: Clone + Ord + ToString + Debug> BinaryTree<T> {
    fn preorder(&self) {
        println!("key: {:?}", &self.key);
        match &self.left {
            Some(node) => node.preorder(),
            None => (),
        }
        match &self.right {
            Some(node) => node.preorder(),
            None => (),
        }
    }
}

// pre-order: implemented externally [by recursion]
fn preorder<T: Clone + Ord + ToString + Debug>(bt: Link<T>) {
    if !bt.is_none() {
        println!("key: {:?}", bt.as_ref().unwrap().get_key());
        preorder(bt.as_ref().unwrap().get_left());
        preorder(bt.as_ref().unwrap().get_right());
    }
}
```

The post-order traversal starts from the left subtree, followed by the right subtree, and finally the root node.

```rust
// binary_tree.rs

impl<T: Clone + Ord + ToString + Debug> BinaryTree<T> {
    fn postorder(&self) {
        match &self.left {
            Some(node) => node.postorder(),
            None => (),
        }
        match &self.right {
            Some(node) => node.postorder(),
            None => (),
        }
        println!("key: {:?}", &self.key);
    }
}

// post-order: implemented externally [by recursion]
fn postorder<T: Clone + Ord + ToString + Debug>(bt: Link<T>) {
    if !bt.is_none() {
        postorder(bt.as_ref().unwrap().get_left());
        postorder(bt.as_ref().unwrap().get_right());
        println!("key: {:?}", bt.as_ref().unwrap().get_key());
```

```text
    }
}
```

The in-order traversal starts from the left subtree, followed by the root node, and finally the right subtree.

```rust
// binary_tree.rs

impl<T: Clone + Ord + ToString + Debug> BinaryTree<T> {
    fn inorder(&self) {
        if self.left.is_some() {
            self.left.as_ref().unwrap().inorder();
        }
        println!("key: {:?}", &self.key);
        if self.right.is_some() {
            self.right.as_ref().unwrap().inorder();
        }
    }
}

// in-order: implemented externally [by recursion]
fn inorder<T: Clone + Ord + ToString + Debug>(bt: Link<T>) {
    if !bt.is_none() {
        inorder(bt.as_ref().unwrap().get_left());
        println!("key: {:?}", bt.as_ref().unwrap().get_key());
        inorder(bt.as_ref().unwrap().get_right());
    }
}
```

To evaluate an arithmetic expression like (1 + (2 * 3)) that is stored in a tree, we need to retrieve the operator and operands in the correct order. While pre-order traversal starts as much as possible from the root node, it is not suitable for computing expressions as we need to start from the leaf nodes. Postorder traversal, on the other hand, is the correct method to retrieve data as it starts from the left subtree, followed by the right subtree, and finally the root node. By first retrieving the values of the left and right child nodes, then retrieving the operator of the root node, we can perform one operation and save the result in the position of the operator, and then continue post-order traversal by visiting the right child node until we calculate the final value. Additionally, in-order traversal can be used on the tree that saves the arithmetic expression (1 + (2 * 3)) to retrieve the original expression 1 + 2 * 3. However, since the tree does not save parentheses, the recovered expression is only in the correct order, but the priority may not be correct. To include parentheses in the output, we can modify the in-order traversal.

```rust
// binary_tree.rs

impl<T: Clone + Ord + ToString + Debug> BinaryTree<T> {
    // form a expression: [internal implementation]
    fn iexp(&self) -> String {
        let mut exp = "".to_string();

        exp += "(";
        let exp_left = match &self.left {
            Some(left) => left.iexp(),
            None => "".to_string(),
```

```rust
        };
        exp += &exp_left;

        exp += &self.get_key().to_string();

        let exp_right = match &self.right {
            Some(right) => right.iexp(),
            None => "".to_string(),
        };
        exp += &exp_right;
        exp += ")";

        exp
    }
}

// form a expression: [external implementation]
fn oexp<T>(bt: Link<T>) -> String
  where: T: Clone + Ord + ToString + Debug + Display
{
    let mut exp = "".to_string();
    if !bt.is_none() {
        exp = "(".to_string() +
              &oexp(bt.as_ref().unwrap().get_left());
        exp += &bt.as_ref().unwrap().get_key().to_string();
        exp += &(oexp(bt.as_ref().unwrap().get_right()) + ")");
    }

    exp
}
```

In addition to the three traversal methods discussed earlier, there is another method called level-order traversal that visits the nodes layer by layer. As we have previously implemented the queue data structure required for level-order traversal, we can directly use it to implement this traversal method.

```rust
// binary_tree.rs

impl<T: Clone + Ord + ToString + Debug> BinaryTree<T> {
    fn levelorder(&self) {
        let size = self.size();
        let mut q = Queue::new(size);

        // enqueue the root node
        let _r = q.enqueue(Box::new(self.clone()));
        while !q.is_empty() {
            // dequeue the first node, and output its value
            let front = q.dequeue().unwrap();
            println!("key: {:?}", front.get_key());

            // enqueue the left/right child node
            match front.get_left() {
                Some(left) => {
                  let _r = q.enqueue(left);
```

```rust
                },
                None => {},
            }

            match front.get_right() {
                Some(right) => {
                  let _r = q.enqueue(right);
                },
                None => {},
            }
        }
    }
}

// level-order: implemented externally [by recursion]
fn levelorder<T: Clone + Ord + ToString + Debug>(bt: Link<T>) {
    if bt.is_none() { return; }

    let size = bt.as_ref().unwrap().size();
    let mut q = Queue::new(size);

    let _r = q.enqueue(bt.as_ref().unwrap().clone());
    while !q.is_empty() {
        // dequeue the first node, and print its value
        let front = q.dequeue().unwrap();
        println!("key: {:?}", front.get_key());

        match front.get_left() {
            Some(left) => {
              let _r = q.enqueue(left);
            },
            None => {},
        }

        match front.get_right() {
            Some(right) => {
              let _r = q.enqueue(right);
            },
            None => {},
        }
    }
}
```

Here are some use examples of binary trees.

```rust
// binary_tree.rs

fn main() {
    basic();
    order();

    fn basic() {
        let mut bt = BinaryTree::new(10usize);
```

```rust
        let root = bt.get_key();
        println!("root key: {:?}", root);

        bt.set_key(11usize);
        let root = bt.get_key();
        println!("root key: {:?}", root);

        bt.insert_left_tree(2usize);
        bt.insert_right_tree(18usize);

        println!("left child: {:#?}", bt.get_left());
        println!("right child: {:#?}", bt.get_right());

        println!("min key: {:?}", bt.min().unwrap());
        println!("max key: {:?}", bt.max().unwrap());

        println!("tree nodes: {}", bt.size());
        println!("tree leaves: {}", bt.leaf_size());
        println!("tree internals: {}", bt.none_leaf_size());
        println!("tree depth: {}", bt.depth());
        println!("tree contains '2': {}", bt.contains(&2));
    }

    fn order() {
        let mut bt = BinaryTree::new(10usize);
        bt.insert_left_tree(2usize);
        bt.insert_right_tree(18usize);

        println!("internal pre-in-post-level order");
        bt.preorder();
        bt.inorder();
        bt.postorder();
        bt.levelorder();

        let nk = Some(Box::new(bt.clone()));
        println!("outside pre-in-post-level order");
        preorder(nk.clone());
        inorder(nk.clone());
        postorder(nk.clone());
        levelorder(nk.clone());

        println!("internal exp: {}", bt.iexp);
        println!("outside exp: {}", oexp(nk));
    }
}
root key: 10 root key: 11 left child: Some( BinaryTree { key: 2,
```

```text
        left: None,
        right: None,
    },
)
right child: Some(
    BinaryTree {
        key: 18,
        left: None,
        right: None,
    },
)
min key: 2
max key: 18
tree nodes: 3
tree leaves: 2
tree internals: 1
tree depth: 2
tree contains '2': true
internal pre-in-post-level order:
key: 10
key: 2
key: 18
key: 2
key: 10
key: 18
key: 2
key: 18
key: 10
key: 10
key: 2
key: 18
outside pre-in-post-level order:
key: 10
key: 2
key: 18
key: 2
key: 10
key: 18
key: 2
key: 18
key: 10
key: 10
key: 2
key: 18
internal exp: ((2)10(18))
outside exp: ((2)10(18))
```

To simplify the descriptions of the three traversal orders, we can use abbreviations. Pre-order traversal can be abbreviated as ”rt-l-r” to indicate that we first visit the root, then the left subtree, and finally the right subtree. Combining the three traversal orders, we have ”rt-l-r” for pre-order traversal, ”l-rt-r” for in-order traversal, and ”l-r-rt” for post-order traversal. It’s worth noting that there can also be a ”rt-r-l” traversal order, but this is simply the mirror image of pre-order traversal. Since left and right are relative,

”l-rt-r” and ”r-rt-l” can be regarded as mirror images of each other. Similarly, ”r-l-rt” is the mirror image of post-order traversal, and ”r-rt-l” is the mirror image of in-order traversal. The table below summarizes the traversal methods for easy reference:

**Table 8.1: Pre-In-Post order and their mirror order method**

| No | tranversal method | order | mirror-order | mirror tranversal method |
| --- | --- | --- | --- | --- |
| 1 | pre-order | rt-l-r | rt-r-l | mirror-pre-order |
| 2 | in-order | l-rt-r | r-rt-l | mirror-in-order |
| 3 | post-order | l-r-rt | r-l-rt | mirror-post-order |
| 4 | mirror-pre-order | rt-r-l | rt-l-r | pre-order |
| 5 | mirror-in-order | r-rt-l | l-rt-r | in-order |
| 6 | mirror-post-order | r-l-rt | l-r-rt | post-order |

## 8.3 Binary Heap

In the previous sections, we learned about the queue, a first-in, first-out linear data structure. Another variation of the queue is the priority queue, which dequeues items based on priority rather than their order of addition. In this type of queue, the highest-priority item is dequeued first, regardless of when it was added. When a new item is added to a priority queue, it will move to the front if its priority is high enough. This movement is a way of sorting based on a certain metric, to ensure that high-priority items are at the front. The priority queue is useful for tasks that involve priorities, such as scheduling processes in an operating system. In this scenario, a priority queue is used to obtain the priority of each process and sort them accordingly. For example, if you are listening to music and browsing news on your phone, and receive an incoming call, the system will give the call the highest priority and interrupt both the news and music to display the incoming call interface. This is an example of managing processes using a priority queue, and assigning a very high priority to the incoming call. To implement a priority queue, we need to sort it based on some rule to place high-priority items at the front. However, inserting items into the queue has a complexity of O(n), and sorting the queue has a complexity of at least O(nlog(n)). To achieve faster results, a binary heap can be used to sort the priority queue. A binary heap is essentially a complete binary tree and allows queuing and dequeuing in O(log(n)) time, making it ideal for efficient scheduling systems. Despite being defined as a binary tree, a linear data structure such as an array, slice, or Vec can be used to implement the binary heap. As long as the operations follow the definition of a binary heap, a linear data structure can implement its functionality and be used as a non-linear data structure. Additionally, there are two common forms of binary heaps: the min heap and the max heap, depending on whether the smallest or largest data item is at the top. This means that there are also two forms of priority queues.

### 8.3.1 The Binary Heap Abstract Data Type

A min-heap can be used as a priority queue, and its abstract data type includes the following methods:

- new() creates a new binary heap with no parameters and returns an empty heap.
- push(k) adds a new item with parameter value k to the heap and returns nothing.
- pop() returns and removes the minimum item from the heap and modifies the heap.
- min() returns the minimum item in the heap without modifying the heap.
- size() returns the number of items in the heap as a numerical value.
- is_empty() returns a Boolean value indicating whether the heap is empty or not.
- build(arr) constructs a new heap from an array or vector of data, with arr as the parameter.

If a binary heap ’h’ has already been created as a priority queue, the table below shows the results of the heap operations performed, with the top item of the heap on the right. The priority value of an item is its value, with smaller values being higher priority and therefore appearing on the right.

**Table 8.2: Operations on binary heap**

| opertions | heap value | return value | operations | heap value | return value |
| --- | --- | --- | --- | --- | --- |
| h.is_empty() | [] | true | h.is_empty() | [8,6,3,2,1] | false |
| h.push(3) | [3] | h.pop() | [8,6,3,2] | 1 |  |
| h.push(8) | [8,3] | h.min() | [8,6,3,2] | 2 |  |
| h.min() | [8,3] | 3 | h.pop() | [8,6,3] | 2 |
| h.push(6) | [8,6,3] | h.pop() | [8,6] | 3 |  |
| h.size() | [8,6,3] | 3 | h.build([5,4]) | [8,6,5,4] |  |
| h.push(2) | [8,6,3,2] | h.build([1]) | [8,6,5,4,1] |  |  |
| h.push(1) | [8,6,3,2,1] | h.min() | [8,6,5,4,1] | 1 |  |

### 8.3.2 Implementing a Binay Heap in Rust

To ensure efficient performance of a binary heap, it is crucial to leverage its logarithmic property. For a binary heap stored in a linear data structure, keeping it balanced is key to achieving logarithmic performance. A balanced binary heap has approximately equal numbers of nodes in its left and right subtrees, and it strives to fill each node’s left and right child nodes, with at most one node having a non-full set of children in the worst case.

![Figure 8.2: Binary Heap](images/fig-8.2.png)

*Figure 8.2: Binary Heap*

To illustrate, let’s consider a heap [0,5,9,11,14,18,19,21,33,17,27] stored using a Vec, and the corresponding tree structure displayed above. As the parent and child nodes are stored in a linear data structure, their relationship is straightforward to compute. If a node is at index p, then its left child node is at 2p, and its right child node is at 2p + 1. Here, p starts from index 1, and index 0 is not used for data, so it is set to 0 as a placeholder.

![Figure 8.3: Heap in Vec](images/fig-8.3.png)

*Figure 8.3: Heap in Vec*

For instance, the index of 5 is p = 1, and its left child node is at index 2 ∗p = 2, where the value is 9. Therefore, 9 is the left child node of 5 in the tree structure. Similarly, the parent node of any child node is located at index p/2. For example, if p = 2 for 9, then its parent node is at index 2/2=1, and if p = 3

for the right child node 11, then its parent node is at index 3/2 = 1 (the division result is rounded down). Hence, computing the parent node of any child node only requires the expression p/2, while child nodes are computed using 2p and 2p+1. We previously defined macros for computing parent and child node indices, and we will continue to use them for calculation purposes.

```text
// binary_heap.rs

// calculate parent node index
macro_rules! parent {
    ($child:ident) => {
        $child >> 1
    };
}

// calculate left child node index
macro_rules! left_child {
    ($parent:ident) => {
        $parent << 1
    };
}

// calculate right child node index
macro_rules! right_child {
    ($parent:ident) => {
        ($parent << 1) + 1
    };
}
```

To begin with, the binary heap is defined as a data structure that includes a field representing the size of the heap. The size field does not include the first data item 0, which is considered a placeholder. The data saved in the heap is assumed to be i32. When initializing the heap, data is present at index 0, but the size is set to 0.

```rust
// binary_heap.rs

// Binary heap definision
// Implement Debug and Clone Trait
#[derive(Debug, Clone)]
struct BinaryHeap {
    size: usize, // data count
    data: Vec<i32>, // data container
}

impl BinaryHeap {
    fn new() -> Self {
        BinaryHeap {
            size: 0,
            data: vec![0] // first 0 not count in total
        }
    }

    fn size(&self) -> usize {
        self.size
```

```rust
    }

    fn is_empty(&self) -> bool {
        0 == self.size
    }

    // Get the minimum data in the heap
    fn min(&self) -> Option<i32> {
        if 0 == self.size {
            None
        } else {
            // Some(self.data[1].clone());
            // clone used for genric type
            Some(self.data[1])
        }
    }
}
```

When adding data to the heap, adding it to the end of the heap will disrupt the balance, so the data needs to be moved up to maintain balance.

5 9 11 18 19 14 21 7 33 17 27 5 9 11 7 19 14 21 33 17 27 18 5 7 11 14 9 19 21 33 17 27 18

As each data item is added, the size of the heap is increased, and the data is moved up if necessary to maintain balance.

```rust
// binary_heap.rs

impl BinaryHeap {
    // Add a data to the end and adjust the heap
    fn push(&mut self, val: i32) {
        self.data.push(val);
        self.size += 1;
        self.move_up(self.size);
    }

    // little data move up.
    // c(child, current), p(parent)
    fn move_up(&mut self, mut c: usize) {
        loop {
            // calculate the parent index of current node
            let p = parent!(c);
            if p <= 0 {
                break;
            }

            // If the current node's data is smaller than
            // the parent node's data, swap them
            if self.data[c] < self.data[p] {
                self.data.swap(c, p);
            }

            // The parent node becomes the current node
            c = p;
        }
    }
}
```

To retrieve the minimum value from the heap, three cases need to be considered: when there is no data in the heap, return None; when there is only one data item, pop it directly; when there are multiple data items, swap the top and end data of the heap, adjust the heap, and then return the minimum value at the end. The move_down function is used to move elements down to maintain balance, and the min_child function is used to find the minimum child node.

```rust
// binary_heap.rs

impl BinaryHeap {
    // pop out the top value
    fn pop(&mut self) -> Option<i32> {
        if 0 == self.size {
            // no data, return None
            None
        } else if 1 == self.size {
            self.size -= 1;

            self.data.pop()
```

```rust
        } else {
            // swap data and then adjust the heap
            self.data.swap(1, self.size);
            let val = self.data.pop();
            self.size -= 1;
            self.move_down(1);

            val
        }
    }

    // bigger data move down
    fn move_down(&mut self, mut c: usize) {
        loop {
            let lc = left_child!(c);
            if lc > self.size { break; }

            // the index of mininum child node of current node
            let mc = self.min_child(c);
            if self.data[c] > self.data[mc] {
                self.data.swap(c, mc);
            }

            // the mininum child node becomes current node
            c = mc;
        }
    }

    // Calculate the index of the minimum child node
    fn min_child(&self, c: usize) -> usize {
        let (lc, rc) = (left_child!(c), right_child!(c));

        if rc > self.size {
            // right child node is out of range,
            // left child node is the minimum child node
            lc
        } else if self.data[lc] < self.data[rc] {
            // left child node is smaller than right child node
            lc
        } else {
            // right child node is smaller than left child node
            rc
        }
    }
}
```

The process of deleting the minimum element from the heap involves taking out the element at the top of the heap and moving the last element to the top. The top element is not the minimum value at this point and does not meet the heap definition, so the heap needs to be rebuilt. To rebuild the heap, the top element needs to be moved down using the move_down function. This function uses a macro to calculate whether to swap with the left or right child node based on the node index, eventually swapping the top element with its minimum child node until the heap is restored.

5 18 7 11 9 19 14 21 33 17 27 5 7 9 11 14 18 19 21 33 17 27

Finally, data can be added to the heap in batches. For instance, a slice of data [0,5,4,3,1,2] can be added to the heap at once to avoid frequent calls to the push function. The original data in the heap can either be kept unchanged while adding the slice data one by one or deleted before adding the slice data. The latter approach results in a new heap that includes only the data in the slice.

![Figure 8.4: delete data and rebuild the heap](images/fig-8.4.png)

*Figure 8.4: delete data and rebuild the heap*

To implement the binary min heap, we define the build_new and build_add functions, as shown below.

```rust
// binary_heap.rs

impl BinaryHeap {
    // build a new heap
    fn build_new(&mut self, arr: &[i32]) {
        // delete all data
        for _i in 0..self.size {
            let _rm = self.data.pop();
        }

        // add new data
        for &val in arr {
```

```rust
            self.data.push(val);
        }

        // change the size
        self.size = arr.len();

        // adjust the heap to make it a min-heap
        let size = self.size;
        let mut p = parent!(size);
        while p > 0 {
            self.move_down(p);
            p -= 1;
        }
    }

    // add slice data one by one
    fn build_add(&mut self, arr: &[i32]) {
        for &val in arr {
            self.push(val);
        }
    }
}
```

With these functions, we have completed the construction of a binary min heap. The entire process should be easy to understand, and based on this, one can write the code for a binary max heap as well. Here’s an example of using a binary heap.

```rust
// binary_heap.rs

fn main() {
    let mut bh = BinaryHeap::new();
    let nums = [-1,0,2,3,4];
    bh.push(10); bh.push(9);
    bh.push(8); bh.push(7); bh.push(6);

    bh.build_add(&nums);
    println!("empty: {:?}", bh.is_empty());
    println!("min: {:?}", bh.min());
    println!("pop min: {:?}", bh.pop());

    bh.build_new(&nums);
    println!("size: {:?}", bh.len());
    println!("pop min: {:?}", bh.pop());
}
```

The following are the outputs after execution.

```text
empty: false
min: Some(-1)
size: 10
pop min: Some(-1)
size: 5
pop min: Some(-1)
```

### 8.3.3 Analysis of Binary Heap

The binary heap stores data linearly in a Vec, but its sorting is based on a tree structure. As discussed earlier, the height of a tree is O(nlog2(n)), and heap sorting moves from the bottom layer to the top layer of the tree, with the number of movements being equal to the number of layers. Hence, the time complexity of heap sorting is O(nlog2(n)). Since constructing a heap requires processing all n items, the complexity is O(n). Overall, the time complexity of the binary heap is O(nlog2(n)) + O(n) = O(nlog2(n)).

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

## 8.6 Summary

This chapter introduced us to trees, an efficient data structure that enables us to implement a wide range of useful algorithms. Trees find extensive applications in storage, networking, and other domains. Throughout this chapter, we completed the following tasks using trees:

- Parseed and evaluated expressions.
- Implemented binary heaps as priority queues.
- Implemented binary trees, binary search trees, and balanced binary search trees.

In the previous chapters, we learned about several abstract data types used to implement mapping relationships (Maps), including ordered tables, hash tables, binary search trees, and balanced binary search trees. The table below compares the worst-case performance of various operations supported by these data types. While red-black trees are an improvement over AVL trees, their complexity and performance remain similar to AVL trees, with only differences in coefficients. For further information, readers are encouraged to consult relevant resources.

**Table 8.5: Performance of various abstract data types**

| Operation | Ordered table | Hash table | BST | AVL | Red-black tree |
| --- | --- | --- | --- | --- | --- |
| insert | O(n) | O(1) | O(n) | O(log(n)) | O(log(n)) |
| contains | O(log(n)) | O(1) | O(n) | O(log(n)) | O(log(n)) |
| delete | O(n) | O(1) | O(n) | O(log(n)) | O(log(n)) |
