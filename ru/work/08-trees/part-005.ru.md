## 8.5 Сбалансированное двоичное дерево поиска

В предыдущем разделе мы построили двоичное дерево поиска и выяснили, что его производительность в некоторых случаях может деградировать до O(n) — например, когда дерево несбалансированно и одна его сторона содержит значительно больше узлов, чем другая. Такая неэффективность приводит к замедлению последующих операций. Для эффективной обработки данных необходимо строить сбалансированное двоичное дерево. В этом разделе рассматривается дерево AVL,

сбалансированное двоичное дерево поиска, способное автоматически поддерживать баланс. Оно названо в честь своих изобретателей: Г. М. Адельсон-Вельского и Е. М. Ландиса. Дерево AVL — это тоже обычное двоичное дерево поиска, но отличается способом выполнения операций над деревом. В деревьях AVL для определения сбалансированности дерева в ходе операций используется фактор баланса (balance factor). Фактор баланса — это разность высот левого и правого поддеревьев узла, определяемая как: balanceFactor = height(leftSubTree) −height(rightSubTree)

(8.2)

Согласно такому определению фактора баланса, если фактор больше нуля, то левое поддерево перевешивает. Если он меньше нуля, перевешивает правое поддерево, а если он равен нулю, дерево сбалансировано. Для эффективной реализации дерева AVL значения фактора баланса −1, 0 и 1 считаются допустимыми, поскольку в этих случаях разность высот левого и правого поддеревьев равна всего 1, что по существу и есть баланс. Как только фактор баланса узла выходит за этот диапазон, например становится равным 2 или −2, дерево необходимо повернуть для восстановления баланса. На следующем рисунке показаны случаи несбалансированности левого и правого поддеревьев, причём фактор баланса каждого узла указан его значением.

-2 0 -1 0 -1 0

### 8.5.1 Дерево AVL

Чтобы двоичное дерево оставалось сбалансированным, необходимо выполнять условие на фактор баланса, которое допускает только три возможности: перевес слева, равновесие или перевес справа. Следует отметить, что дерево с перевесом слева или справа, для которого фактор баланса по-прежнему равен −1, 0 или 1, также считается сбалансированным. На рисунке ниже изображено наиболее несбалансированное дерево с перевесом слева, удовлетворяющее условию на фактор баланса, для деревьев высоты 0, 1, 2 и 3.

0 1 1 1 0 0 1 1 1 0 1 0 0 0

Анализируя общее число узлов в дереве, можно вывести формулу для числа узлов в дереве высоты h: для дерева высоты 0 имеется только один узел; для дерева высоты 1 — 2 узла; для дерева высоты 2 — 4 узла; для дерева высоты 3 — 7 узлов и так далее. Nh = 1 + Nh−1 + Nh−2

(8.3)

Примечательно, что эта формула напоминает последовательность Фибоначчи. Зная число узлов в дереве, можно получить формулу высоты для дерева AVL с помощью уравнения Фибоначчи, где i-е число Фибоначчи

задаётся следующим уравнением:

F0 = 0 F1 = 1 (8.4)

Fi = Fi−1 + Fi−2 Для вычисления числа узлов в дереве AVL можно использовать следующую формулу, в которой F0 = 1. Nh = Fh+2 −1

(8.5) √

С ростом i отношение Fi/Fi−1 приближается к золотому сечению Φ = (1 +

5)/2, поэтому Φ можно использовать для

представления Fi, которое вычисляется как Fi = Φi

5 . Nh = Φh √ 5 + 1 (8.6)

На основе этих формул можно вывести формулу высоты для деревьев AVL. log(Nh −1) = log( Φh

√ 5)

log(Nh −1) = hlogΦ −1

2log5 (8.7)

h = log(Nh −1) + 1

2log5 logΦ

h = 1.44log(Nh) В этой формуле h — высота дерева AVL, а Nh — число узлов. Отсюда следует, что высота дерева AVL не более чем в 1,44 раза превышает логарифм числа узлов, а сложность поиска составляет O(logN), что весьма эффективно.

### 8.5.2 Реализация дерева AVL на Rust

Чтобы вставить новый узел в дерево AVL, сначала он добавляется как листовой узел, что автоматически даёт ему фактор баланса 0. Однако фактор баланса родительского узла необходимо обновить в зависимости от того, является ли новый узел левым или правым дочерним узлом. Если это правый дочерний узел, фактор баланса родителя уменьшается на 1, а если левый, фактор баланса увеличивается на 1. Это обновление рекурсивно распространяется вверх по дереву, пока не будет достигнут корень или узел, фактор баланса которого станет равным 0. В нашей реализации дерево AVL представлено перечислением с двумя вариантами: Null, обозначающим пустое дерево, и Tree, обозначающим узел дерева. Тип AvlNode используется для хранения данных, левого и правого поддеревьев и фактора баланса каждого узла.

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

Для реализации дерева AVL нужно добавить две функции: insert и rebalance. Для сравнения данных узлов также вводится свойство сравнения, называемое Ording. Кроме того, необходимы функции replace и max для обновления значений и вычисления высоты дерева.

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

Функция insert рекурсивно обновляет фактор баланса, а функция rebalance восстанавливает баланс дерева AVL. Эффективная ребалансировка важна для поддержания правильной работы дерева AVL без ущерба для производительности. Ребалансировка включает один или несколько поворотов дерева, которые выполняются посредством левого или правого поворота. Чтобы выполнить левый поворот, можно действовать согласно шагам, показанным на рисунке (8.8): (1) правый дочерний узел (B) назначается новым корнем поддерева; (2) старый корень (A) становится левым дочерним узлом нового корня; (3) если у нового корня (B) уже есть левый дочерний узел, он становится правым дочерним узлом нового левого дочернего узла (A). Аналогично, чтобы выполнить правый поворот, можно действовать так: (1) левый дочерний узел (B) назначается новым корнем поддерева; (2) старый корень (A) становится правым дочерним узлом нового корня; (3) если у нового корня (B) уже есть правый дочерний узел, он становится левым дочерним узлом нового правого дочернего узла (A). Два дерева на рисунке несбалансированы, и их можно сбалансировать в дерево справа, выполнив левый и правый повороты с корнем A.

![Рисунок 8.8: Несбалансированное дерево и его повороты](images/fig-8.8.png)

*Рисунок 8.8: Несбалансированное дерево и его повороты*

Для выполнения поворотов в поддереве можно использовать правила левого и правого поворота. Однако иногда после выполнения одного поворота баланс всё ещё может быть нарушен в противоположную сторону.

C A -2 2 левый поворот C A 1 -1 B B 0 0

В таких случаях нужно использовать новые правила поворота, описанные ниже:

- Чтобы сбалансировать поддерево левым поворотом, сначала проверяется фактор баланса правого дочернего узла. Если правое поддерево перевешивает, выполняется правый поворот в нём, а затем левый поворот.
- Аналогично, чтобы сбалансировать поддерево правым поворотом, сначала проверяется фактор баланса левого дочернего узла. Если левое поддерево перевешивает, выполняется левый поворот в нём, а затем правый поворот.

Хотя процесс поворота поддерева легко понять концептуально, его реализация в коде может быть сложной, поскольку требуется перемещать узлы в правильном порядке, сохраняя все свойства двоичного дерева поиска. Кроме того, механизмы владения в Rust делают перемещение узлов и обновление связей между указателями подверженными ошибкам. Для реализации функций поворота используются функции получения узла и поддерева, такие как left_subtree и right_subtree.

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

Для поддержания баланса дерева можно выполнять операции поворота. Однако также необходимо реализовать методы получения важной информации о дереве, такие как число узлов, значения узлов, высота дерева, минимальное и максимальное значения и поиск узлов. Для этого в сбалансированном двоичном дереве реализуются методы size, leaf_size, depth, node, min, max и contains.

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

Помимо этих методов, можно реализовать четыре метода обхода, обычно используемых для двоичных деревьев: inorder, preorder, postorder и levelorder. Эти методы обхода позволяют посещать каждый узел дерева и манипулировать им в определённом порядке, что бывает полезно в различных сценариях, например при выводе дерева, поиске конкретного узла или вычислении некоторых статистических характеристик дерева.

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

Ниже приведены результаты выполнения.

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

### 8.5.3 Анализ дерева AVL

Сбалансированное двоичное дерево AVL включает функцию ребалансировки, а также операции левого и правого поворота для поддержания своего баланса, что позволяет его операциям сохранять относительно хорошую производительность при сложности в худшем случае O(log2(n)). Однако важно отметить, что деревья AVL выполняют значительное число операций поворота для поддержания баланса. Красно-чёрное дерево — это оптимизированное двоичное дерево, которое требует меньшего числа поворотов по сравнению с деревом AVL. Оно представляет собой ослабленный вариант дерева AVL и может использоваться в сценариях с частыми вставками, удалениями и изменениями для достижения лучшей производительности.
