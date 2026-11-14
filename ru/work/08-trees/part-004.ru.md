## 8.4 Binary Search Tree

Однако линейные структуры данных не подходят для представления деревьев большого объёма, так как копирование и перемещение данных становятся очень затратными по времени. Для решения этой проблемы в данном разделе рассматривается реализация деревьев с помощью узлов. В частности, этот раздел посвящён двоичным деревьям, у которых есть только два дочерних узла. Чтобы лучше понять двоичные деревья, мы изучаем двоичные деревья поиска для поиска, которые хранят данные в виде пар «ключ — значение», подобно HashMap.

### 8.4.1 Абстрактный тип данных «двоичное дерево поиска»

Двоичное дерево поиска предоставляет следующие абстрактные типы данных:

- new() создаёт новое дерево, не принимает параметров и возвращает пустое дерево.
- insert(k, v) сохраняет данные (k, v) в дереве, принимает ключ k и значение v и ничего не возвращает.
- contains(&k) ищет в дереве ключ k, принимает параметр &k и возвращает логическое значение.
- get(&k) возвращает значение v ключа k из дерева, не удаляя его, и принимает параметр &k.
- max() возвращает максимальный ключ k и его значение v в дереве и не принимает параметров.
- min() возвращает минимальный ключ k и его значение v в дереве и не принимает параметров.
- len() возвращает количество элементов данных в дереве, не принимает параметров и возвращает целое число типа usize.
- is_empty() проверяет, пусто ли дерево, не принимает параметров и возвращает логическое значение.
- iter() возвращает дерево в виде итератора, не принимает параметров и не изменяет дерево.
- preorder() выполняет обход в прямом порядке (pre-order), не принимает параметров и выводит каждую пару k-v.
- inorder() выполняет обход в симметричном порядке (in-order), не принимает параметров и выводит каждую пару k-v.
- postorder() выполняет обход в обратном порядке (post-order), не принимает параметров и выводит каждую пару k-v.

В таблице ниже показано двоичное дерево поиска после различных операций; узлы дерева представлены кортежами и заключены в квадратные скобки, при этом предполагается, что t — только что созданное пустое дерево.

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

### 8.4.2 Реализация двоичного дерева поиска в Rust

В отличие от куч, где левый и правый дочерние узлы не сравниваются по значению, в двоичном дереве поиска ключ левого дочернего узла меньше ключа родительского узла, а ключ правого дочернего узла больше ключа родительского узла. Это правило left < parent < right рекурсивно применяется ко всем поддеревьям.

![Figure 8.5: Binary search tree](images/fig-8.5.png)

*Figure 8.5: Binary search tree*

В приведённом выше примере 70 — корневой узел; 31 меньше и становится левым узлом, а 93 больше и становится правым узлом. Затем вставляется 14, которое меньше 70 и спускается к 31, а поскольку оно меньше 31, оно становится левым узлом 31. Аналогичные шаги выполняются при вставке других данных, и в итоге формируется двоичное дерево поиска. Симметричный обход (in-order) этого дерева даёт последовательность [14, 23, 31, 70, 73, 93, 94], отсортированную от меньшего к большему, поэтому двоичное дерево поиска также можно использовать для сортировки данных. С помощью симметричного обхода мы получаем результат сортировки по возрастанию, а с помощью зеркального симметричного обхода, то есть обхода в порядке «право-корень-лево», — результат сортировки по убыванию. Для реализации двоичного дерева поиска мы определяем его как структуру BST (BinarySearchTree), которая включает ключи, значения и ссылки на левый и правый дочерние узлы. В соответствии с определением абстрактного типа данных реализация двоичного дерева поиска показана ниже.

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

Ниже приведена реализация обходов в прямом, симметричном, обратном порядке и обхода по уровням.

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

Ниже приведены выходные данные после выполнения программы двоичного дерева поиска.

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

При вставке 76 в дерево путь поиска показан чёрными узлами.

![Figure 8.6: Insertion into a BST](images/fig-8.6.png)

*Figure 8.6: Insertion into a BST*

Удаление узла в двоичном дереве поиска — сложная операция. Первый шаг — найти узел, который нужно удалить, причём его может не оказаться в дереве. После того как узел найден, необходимо определить, есть ли у него дочерние узлы; возможны три случая: дочерних узлов нет, есть один дочерний узел или есть два дочерних узла.

**Table 8.4: Key deletion cases**

| No | Node | node k | delete mothod |
| --- | --- | --- | --- |
| 1 | No node | None | Directly return |
| 2 | One root node | None | Directly delete |
| 3 | Multiple nodes | None | Directly delete |
| 4 | Multiple nodes | One child | Replace k with child node |
| 5 | Multiple nodes | Two children | Replace k with the successor node |

Если узел является листовым узлом без дочерних узлов, достаточно удалить ссылку на него из родительского узла. Если у него один дочерний узел, мы изменяем ссылку родительского узла так, чтобы она указывала непосредственно на этот дочерний узел. Самый сложный случай — когда у узла два дочерних узла. В этом случае мы находим минимальный узел в правом поддереве, называемый узлом-преемником, и заменяем удаляемый узел узлом-преемником. У узла-преемника также могут быть дочерние узлы, и их взаимосвязи необходимо соответствующим образом скорректировать. Конкретные ситуации показаны на следующем рисунке, где пунктирной рамкой обозначен удаляемый узел k, а справа показано двоичное дерево, полученное после удаления узла.

70 70 leaf node 31 93 31 93 14 73 94 14 73 94 23 76 23 70 70 one child node 31 93 93 14 14 73 94 23 73 94 23 76 70 70 two child nodes 31 93 31 76 73 94 73 94 14 14 23 76 23

Удаление листового узла — самый простой случай, а удаление внутреннего узла с одним дочерним узлом выполняется несложно. Самый трудный случай — когда у узла два дочерних узла, поскольку при этом требуется скорректировать взаимосвязи нескольких узлов.

### 8.4.3 Analysis of Binary Search Tree

Теперь, когда двоичное дерево поиска полностью реализовано, проанализируем временную сложность каждого метода. Обходы и len() имеют временную сложность O(n), так как им нужно обработать все n элементов. Метод contains() сравнивает данные с левым и правым дочерними узлами и в зависимости от результата выбирает ветвь. Он проходит не более чем по самому длинному пути от корня до листового узла. Высота двоичного дерева связана с общим числом узлов: 20 + 21 + 2i... + 2h = n

(8.1) h = log2(n)

Используя свойства двоичного дерева, можно приблизительно считать максимальную длину пути равной h = log2(n). Таким образом, временная сложность contains() составляет O(log2(n)). Вставка, удаление и изменение основаны на поиске, поскольку перед продолжением обработки элемент необходимо найти. Их временная сложность зависит только от поиска и может быть выполнена за постоянное время. Следовательно, производительность методов contains(), insert() и get() — всё это O(log2(n)). Высота h двоичного дерева является ограничивающим фактором их производительности. Если вставляемые данные всегда находятся в отсортированном состоянии, двоичное дерево может выродиться в линейный связный список, и производительность методов contains(), insert() и remove() будет O(n). На рисунке ниже показан этот сценарий.

![Figure 8.7: bst in a linear linked list](images/fig-8.7.png)

*Рисунок 8.7: bst в виде линейного связного списка*

В этом разделе мы не реализовали функцию remove(), поскольку она не входит в определение абстрактного типа данных, а двоичные деревья поиска используются главным образом для вставки и поиска данных, а не для удаления. Однако заинтересованные читатели могут в качестве упражнения попытаться реализовать функцию remove(). Чтобы повысить производительность за счёт уменьшения высоты дерева, можно преобразовать двоичное дерево в многопутевое дерево, например в B-деревья и B+-деревья. У таких деревьев много дочерних узлов, поэтому высота дерева невелика и запросы выполняются быстро. Они широко применяются при реализации баз данных и файловых систем. Например, база данных MySQL использует B+-деревья для хранения данных с узлами, представляющими страницы памяти размером 16 КБ. Если каждая запись данных имеет размер 1 КБ, один узел может хранить 16 записей. При использовании для хранения индекса с ключом bigint расходуется 8 байтов, а индекс занимает 6 байтов, всего 14 байтов. Таким образом, один узел может хранить примерно 16∗1024/14 = 1170 индексов. При высоте 3 B+-дерево может хранить около 1170∗1170∗16 = 21902400 индексов, что позволяет хранить около 20 миллионов записей данных. Для получения данных требуется не более двух запросов, что объясняет, почему запросы к базе данных выполняются так быстро. Заинтересованные читатели могут прочитать книги, посвящённые MySQL, чтобы узнать больше.


