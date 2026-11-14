## 4.6 LinkedList

An ordered collection of data items is important to maintain the relative position of data and efficient indexing. Arrays and linked lists both allow data to be collected in an ordered manner and saved in relative positions, making them suitable for implementing ordered data types. For example, Rust’s default implementation of Vec uses an array. This section focuses on linked lists, which offer some unique advantages. Unlike arrays, linked lists do not require elements to be stored in contiguous memory. Each item in the collection has a reference to the next item, so the items can be randomly placed without the need to allocate a block of memory, resulting in higher efficiency. To use a linked list, we need to specify the position of the first item explicitly. Once we know the position of the first item, we can determine the position of the second item and so on until the end of the entire linked list.

![Figure 4.16: Linked list](images/fig-4.16.png)

*Figure 4.16: Linked list*

Usually, linked lists provide a reference to the head of the list, and the last item must be set to null or an empty next item, also known as the tail. With this setup, we can easily traverse the linked list from the head to the tail, or vice versa, by following the references between items. This makes linked lists an efficient data structure for implementing other ordered data types.

### 4.6.1 The LinkedList Abstract Data Type

The abstract data type of a linked list consists of its structure and operations. As previously mentioned, a linked list is an ordered collection of nodes, and the entire list can be traversed from the head node. The structure of a linked list is simple, with each node containing an element and a reference to the next node. The following definitions and operations apply to a linked list:

- new(): Creates a new head node that points to a Node, takes no arguments, and returns a pointer.
- push(item): Adds a new Node, takes an item parameter, and returns None.
- pop(): Deletes the head node of the linked list, takes no arguments, and returns a Node.
- peek(): Returns a referent to the head node of the linked list, takes no arguments.
- peek_mut(): Returns the head node of the linked list, takes no arguments, and returns a mutable reference to the node.
- is_empty(): Returns a Boolean value indicating whether the current linked list is empty, takes no arguments.
- size(): Returns the length of the linked list as a usize integer value, takes no arguments.
- iter(): Returns an immutable iteration of the linked list without modifying the linked list, takes no arguments.
- iter_mut(): Returns a mutable iteration of the linked list with the linked list mutable, takes no arguments.
- into_iter(): Consumes the linked list and returns an iterable form of the linked list, takes no arguments.

Assuming that l is an empty linked list, the table below shows the result of a sequence of linked list operations, with Link<num> representing the address pointing to the node containing num, and the left end of the list being the head node.

**Table 4.6: LinkedList Operations**

| Operation | Value | Return |
| --- | --- | --- |
| l.is_empty() | [None->None] | true |
| l.push(1) | [1->None] |  |
| l.push(2) | [2->1->None] |  |
| l.push(3) | [3->2->1->None] |  |
| l.peek() | [3->2->1->None] | Link<3> |
| l.pop() | [2->1->None] | 3 |
| l.size() | [2->1->None] | 2 |
| l.push(4) | [4->2->1->None] |  |
| l.peek_mut() | [4->2->1->None] | mut Link<4> |
| l.iter() | [4->2->1->None] | [4,2,1] |
| l.is_empty() | [4->2->1->None] | false |
| l.size() | [4->2->1->None] | 3 |
| l.into_iter() | [None->None] | [4,2,1] |

### 4.6.2 Implementing a LinkedList in Rust

To represent an item in a linked list, we use a node abstraction that includes the data item and the address of the next item. The node also provides methods to access and modify the data item. As shown in the figure below, a Node consists of data and the address of the next node.

![Figure 4.17: Node](images/fig-4.17.png)

*Figure 4.17: Node*

In Rust, None is used to represent the absence of a next node in both the Node and the linked list. The new function initializes a grounded node with its next field set to None. Explicitly assigning None to the next field is a good practice that helps avoid dangling pointers, a common issue in languages like C/C++.

![Figure 4.18: LinkedList](images/fig-4.18.png)

*Figure 4.18: LinkedList*

The following code shows the implementation of the linked list, with the node link defined as Link for code clarity.

```rust
// linked_list.rs

// The node link uses a Box pointer (size determined),
// because only with a determined size can memory be allocated.
type Link<T> = Option<Box<Node<T>>>;
```

```rust
// Linked list definition
struct List<T> {
    size: usize, // Number of nodes in the linked list
    head: Link<T>, // Head node
}

// Linked list node
struct Node<T> {
    elem: T, // data
    next: Link<T>, // Link to the next node
}

impl<T> List <T> {
    fn new() -> Self {
        Self {
            size: 0,
            head: None
        }
    }

    fn is_empty(&self) -> bool { 0 == self.size }

    fn len(&self) -> usize { self.size }

    fn clear(&mut self) {
        self.size = 0;
        self.head = None;
    }

    // add a new node ahead of the head node
    fn push(&mut self, elem: T) {
        let node = Box::new(Node {
            elem: elem,
            next: self.head.take(),
        });
        self.head = Some(node);
        self.size += 1;
    }

    // take will move data out from node and left a vaccum
    fn pop(&mut self) -> Option<T> {
        self.head.take().map(|node| {
            self.head = node.next;
            self.size -= 1;
            node.elem
        })
    }

    // peek get a unmutable reference
    fn peek(&self) -> Option<&T> {
        self.head.as_ref().map(|node| &node.elem )
    }
```

```rust
    // peek_mut get a mutable reference
    fn peek_mut(&mut self) -> Option<&mut T> {
        self.head.as_mut().map(|node| &mut node.elem )
    }

    // Implementation of iteration for the linked list.
    // into_iter: makes the linked list an iterator
    // by consuming it
    // iter: returns an immutable iterator without modifying
    // the linked list
    // iter_mut: returns a mutable iterator without modifying
    // the linked list
    fn into_iter(self) -> IntoIter<T> {
        IntoIter(self)
    }

    fn iter(&self) -> Iter<T> {
        Iter { next: self.head.as_deref() }
    }

    fn iter_mut(&mut self) -> IterMut<T> {
        IterMut { next: self.head.as_deref_mut() }
    }
}

// Implementation of three iterations
struct IntoIter<T>(List<T>);
impl<T> Iterator for IntoIter<T> {
    type Item = T;
    fn next(&mut self) -> Option<Self::Item> {
        // (List<T>) tuple's 0th item
        self.0.pop()
    }
}

struct Iter<'a, T: 'a> { next: Option<&'a Node<T>> }
impl<'a, T> Iterator for Iter<'a, T> {
    type Item = &'a T;
    fn next(&mut self) -> Option<Self::Item> {
        self.next.map(|node| {
            self.next = node.next.as_deref();
            &node.elem
        })
    }
}

struct IterMut<'a, T: 'a> { next: Option<&'a mut Node<T>> }
impl<'a, T> Iterator for IterMut<'a, T> {
    type Item = &'a mut T;
    fn next(&mut self) -> Option<Self::Item> {
        self.next.take().map(|node| {
```

```rust
            self.next = node.next.as_deref_mut();
            &mut node.elem
        })
    }
}

// Custom implementation of Drop for the linked list
impl<T> Drop for List<T> {
    fn drop(&mut self) {
        let mut link = self.head.take();
        while let Some(mut node) = link {
            link = node.next.take();
        }
    }
}

fn main() {
    basic_test();
    into_iter_test();
    iter_test();
    iter_mut_test();

    fn basic_test() {
        let mut list = List::new();
        list.push(1); list.push(2); list.push(3);

        assert_eq!(list.len(), 3);
        assert_eq!(list.is_empty(), false);
        assert_eq!(list.pop(), Some(3));
        assert_eq!(list.peek(), Some(&2));
        assert_eq!(list.peek_mut(), Some(&mut 2));

        list.peek_mut().map(|val| {
            *val = 4;
        });

        assert_eq!(list.peek(), Some(&4));
        list.clear();
        println!("basics test Ok!");
    }

    fn into_iter_test() {
        let mut list = List::new();
        list.push(1); list.push(2); list.push(3);

        let mut iter = list.into_iter();
        assert_eq!(iter.next(), Some(3));
        assert_eq!(iter.next(), Some(2));
        assert_eq!(iter.next(), Some(1));
        assert_eq!(iter.next(), None);

        println!("into_iter test Ok!");
```

```rust
    }

    fn iter_test() {
        let mut list = List::new();
        list.push(1); list.push(2); list.push(3);

        let mut iter = list.iter();
        assert_eq!(iter.next(), Some(&3));
        assert_eq!(iter.next(), Some(&2));
        assert_eq!(iter.next(), Some(&1));
        assert_eq!(iter.next(), None);
        println!("iter test Ok!");
    }

    fn iter_mut_test() {
        let mut list = List::new();
        list.push(1); list.push(2); list.push(3);

        let mut iter = list.iter_mut();
        assert_eq!(iter.next(), Some(&mut 3));
        assert_eq!(iter.next(), Some(&mut 2));
        assert_eq!(iter.next(), Some(&mut 1));
        assert_eq!(iter.next(), None);
        println!("iter_mut test Ok!");
    }
}
```

### 4.6.3 LinkedList Stack

To implement a stack, we can also use a linked list, which is another type of linear data structure. In this case, we can use the head of the linked list to store the top element of the stack. As new items are added to the stack, they will be inserted at the head of the linked list. The implementation for this approach is shown below. Note that since the push and pop functions modify the linked list nodes, we use the take function to extract the node value.

```rust
// list_stack.rs

// Linked List Node
#[derive(Debug, Clone)]
struct Node<T> {
    data: T,
    next: Link<T>,
}

// Node Self-contained Reference
type Link<T> = Option<Box<Node<T>>>;

impl<T> Node<T> {
    fn new(data: T) -> Self {
        Self {
            data: data,
            next: None // No next link when initialized
```

```rust
        }
    }
}

// Linked list stack
#[derive(Debug, Clone)]
struct LStack<T> {
    size: usize,
    top: Link<T>, // Top controls the entire stack
}

impl<T: Clone> LStack<T> {
    fn new() -> Self {
        Self {
            size: 0,
            top: None
        }
    }

    fn is_empty(&self) -> bool {
        0 == self.size
    }

    fn len(&self) -> usize {
        self.size
    }

    fn clear(&mut self) {
        self.size = 0;
        self.top = None;
    }

    // take out the node on the top, leaving an empty space
    // that could be filled later
    fn push(&mut self, val: T) {
        let mut node = Node::new(val);
        node.next = self.top.take();
        self.top = Some(Box::new(node));
        self.size += 1;
    }

    fn pop(&mut self) -> Option<T> {
        self.top.take().map(|node| {
            let node = *node;
            self.top = node.next;
            self.size -= 1;
            node.data
        })
    }

    // Return a reference to the data in the linked list stack
    fn peek(&self) -> Option<&T> {
```

```rust
        self.top.as_ref().map(|node| &node.data)
    }

    fn peek_mut(&mut self) -> Option<&mut T> {
        self.top.as_deref_mut().map(|node| &mut node.data)
    }

    // into_iter: the linked list stack changes
    // iter: the linked list stack remains unchanged
    // iter_mut: the linked list stack remains unchanged
    fn into_iter(self) -> IntoIter<T> {
        IntoIter(self)
    }

    fn iter(&self) -> Iter<T> {
        Iter { next: self.top.as_deref() }
    }

    fn iter_mut(&mut self) -> IterMut<T> {
        IterMut { next: self.top.as_deref_mut() }
    }
}

// Implement three iterations
struct IntoIter<T: Clone>(LStack<T>);
impl<T: Clone> Iterator for IntoIter<T> {
    type Item = T;
    fn next(&mut self) -> Option<Self::Item> {
        self.0.pop()
    }
}

struct Iter<'a, T: 'a> { next: Option<&'a Node<T>> }
impl<'a, T> Iterator for Iter<'a, T> {
    type Item = &'a T;
    fn next(&mut self) -> Option<Self::Item> {
        self.next.map(|node| {
            self.next = node.next.as_deref();
            &node.data
        })
    }
}

struct IterMut<'a, T: 'a> { next: Option<&'a mut Node<T>> }
impl<'a, T> Iterator for IterMut<'a, T> {
    type Item = &'a mut T;
    fn next(&mut self) -> Option<Self::Item> {
        self.next.take().map(|node| {
            self.next = node.next.as_deref_mut();
            &mut node.data
        })
    }
```

```rust
}

fn main() {
    basic();
    iter();

    fn basic() {
        let mut s = LStack::new();
        s.push(1); s.push(2); s.push(3);

        println!("empty: {:?}", s.is_empty());
        println!("top: {:?}, size: {}", s.peek(), s.len());
        println!("pop: {:?}, size: {}", s.pop(), s.len());

        let peek_mut = s.peek_mut();
        if let Some(data) = peek_mut {
            *data = 4
        }
        println!("top {:?}, size {}", s.peek(), s.len());

        println!("{:?}", s);
        s.clear();
        println!("{:?}", s);
    }

    fn iter() {
        let mut s = LStack::new();
        s.push(1); s.push(2); s.push(3);

        let sum1 = s.iter().sum::<i32>();
        let mut addend = 0;
        for item in s.iter_mut() {
            *item += 1;
            addend += 1;
        }
        let sum2 = s.iter().sum::<i32>();
        println!("{sum1} + {addend} = {sum2}");

        assert_eq!(9, s.into_iter().sum::<i32>());
    }
}
```

The output of the code will depend on how the stack is used and what functions are called.

```text
empty: false
top: Some(3), size: 3
pop: Some(3), size: 2
top Some(4), size 2
LStack { size: 2, top: Some(Node { data: 4,
         next: Some(Node { data: 1, next: None }) }) }
LStack { size: 0, top: None }
6 + 3 = 9
```
