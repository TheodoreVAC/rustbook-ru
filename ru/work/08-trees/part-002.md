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
