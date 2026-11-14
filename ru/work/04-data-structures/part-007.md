## 4.7 Vec

In this chapter, we have demonstrated how the basic data type Vec can be used to implement various abstract data types, including stacks, queues, deques, and linked lists. Vec is a powerful yet simple data container that offers mechanisms for data collection and various operations, which is why we repeatedly use it as the underlying data structure for implementing other data types. It is similar to Python’s List and is very convenient to use. However, not all programming languages include Vec, or not all data types may be suitable for it. In some cases, Vec or similar data containers must be implemented separately by programmers.

### 4.7.1 The Vec Abstract Data Type

Vec is a collection of items that maintain a relative position to other items. Here are the various operations of the Vec abstract data type:

- new(): Creates a new empty Vec, takes no arguments.
- push(item): Adds the item to the end of the Vec, takes item as a parameter.
- pop(): Deletes the last item in the Vec and returns it, take no arguments.
- insert(pos, item): Inserts the item at position pos in the Vec, takes pos and item parameters.
- remove(idx): Removes the item at index idx from the Vec and returns it, takes a parameter.
- find(item): Checks if the item exists in the Vec and returns a boolean value, takes an item parameter.
- is_empty(): Checks if the Vec is empty and returns a boolean value, takes no arguments.
- size(): Calculates the number of items in the Vec and returns a usize integer, takes no arguments.
- iter(): Returns an immutable iteration form of the Vec.
- iter_mut(): Returns a mutable iteration form of the Vec, takes no arguments.
- into_iter(): Consumes the Vec and returns an iterable form of the Vec, takes no arguments.

Assuming v is an empty Vec that has been created, the table below shows the Vec after different operations, with the left side being the head.

**Table 4.7: Operations on a Vec**

| operation | value | return |
| --- | --- | --- |
| v.is_empty() | [] | true |
| v.push(1) | [1] |  |
| v.push(2) | [1,2] |  |
| v.push(3) | [1,2,3] |  |
| v.size() | [1,2,3] | 3 |
| v.pop() | [1,2] | 3 |
| v.push(5) | [1,2,5] |  |
| v.find(4) | [1,2,5] | false |
| v.insert(0,8) | [8,1,2,5] |  |
| v.pop() | [8,1,2] | 5 |
| v.remove(0) | [1,2] | 8 |
| v.size() | [1,2] | 2 |

Finally, it is worth noting that while Vec is a powerful data structure, it may not always be the best choice for a particular use case. Programmers should carefully consider the requirements of their project and choose the appropriate data structure accordingly.

### 4.7.2 Implementing a Vec in Rust

Vec is composed of linked list nodes, where each node contains a data item and an explicit reference to the next node. Given the location of the first node, subsequent items can be accessed by following the next link.

Since references play a crucial role in Vec, it is necessary to maintain a reference to the first node. The linked list is created with None indicating that the list does not reference any content, as shown in Figure (4.19). The head of the linked list refers to the first node of the list, which stores the address of the next node. It is important to note that the Vec itself does not contain any node objects but only a reference to the first node in the linked list structure.

![Figure 4.19: LinkedList Formed Vec](images/fig-4.19.png)

*Figure 4.19: LinkedList Formed Vec*

To add a new item to the linked list, the only entry point is through the head of the list. As all other nodes can only be accessed by following the next link from the first node, the most efficient way to add a new node is to add it to the head of the linked list. This approach adds the new item as the first element, with the existing items linked to it. While the implementation of Vec presented here is unordered, it is possible to implement an ordered Vec using a data comparison function with total or partial orders. The following LVec provides only a portion of the functionality of the standard library Vec, and print_lvec is used to print its data items.

```rust
// lvec.rs

use std::fmt::Debug;

#[derive(Debug)]
struct Node<T> {
    elem: T,
    next: Link<T>,
}

type Link<T> = Option<Box<Node<T>>>;

impl<T> Node<T> {
    fn new(elem: T) -> Self {
        Self {
            elem: elem,
            next: None
        }
    }
}

// LinkedList Vec definition
#[derive(Debug)]
struct LVec<T> {
    size: usize,
    head: Link<T>,
}

impl<T: Copy + Debug> LVec<T> {
    fn new() -> Self {
        Self { size: 0, head: None }
```

```rust
    }

    fn is_empty(&self) -> bool {
        0 == self.size
    }

    fn len(&self) -> usize {
        self.size
    }

    fn clear(&mut self) {
        self.size = 0;
        self.head = None;
    }

    fn push(&mut self, elem: T) {
        let node = Node::new(elem);
        if self.is_empty() {
            self.head = Some(Box::new(node));
        } else {
            let mut curr = self.head.as_mut().unwrap();

            // find the last node in the list
            for _i in 0..self.size-1 {
                curr = curr.next.as_mut().unwrap();
            }

            // insert the new data after the last node
            curr.next = Some(Box::new(node));
        }
        self.size += 1;
    }

    // add a new LVec to the end of the stack
    fn append(&mut self, other: &mut Self) {
        while let Some(node) = other.head.as_mut().take() {
            self.push(node.elem);
            other.head = node.next.take();
        }
        other.clear();
    }

    fn insert(&mut self, mut index: usize, elem: T) {
        if index >= self.size { index = self.size; }

        // three cases for inserting a new node
        let mut node = Node::new(elem);
        if self.is_empty() { // LVec is empty
            self.head = Some(Box::new(node));
        } else if index == 0 { // insert at the beginning of
           the list node.next = self.head.take();
```

```rust
            self.head = Some(Box::new(node));
        } else { // insert int the middle of the list
            let mut curr = self.head.as_mut().unwrap();
            for _i in 0..index - 1 { // find the right insert
               position curr = curr.next.as_mut().unwrap();
            }
            node.next = curr.next.take();
            curr.next = Some(Box::new(node));
        }
        self.size += 1;
    }

    fn pop(&mut self) -> Option<T> {
        if self.size < 1 {
            return None;
        } else {
            self.remove(self.size - 1)
        }
    }

    fn remove(&mut self, index: usize) -> Option<T> {
        if index >= self.size { return None; }

        // two cases for deleting a node
        let mut node;
        if 0 == index {
            node = self.head.take().unwrap();
            self.head = node.next.take();
        } else { // find the position which will be deleteed
           and arrange the links properly let mut curr = self.head.as_mut().unwrap();
            for _i in 0..index - 1 {
                curr = curr.next.as_mut().unwrap();
            }
            node = curr.next.take().unwrap();
            curr.next = node.next.take();
        }
        self.size -= 1;

        Some(node.elem)
    }

   fn into_iter(self) -> IntoIter<T> {
        IntoIter(self)
    }

    fn iter(&self) -> Iter<T> {
        Iter { next: self.head.as_deref() }
    }

    fn iter_mut(&mut self) -> IterMut<T> {
```

```rust
        IterMut { next: self.head.as_deref_mut() }
    }

    // print LVec
    fn print_lvec(&self) {
        if 0 == self.size {
            println!("Empty lvec");
        }
        for item in self.iter() {
            println!("{:?}", item);
        }
    }
}

// Implemtion of three iterations
struct IntoIter<T: Copy + Debug >(LVec<T>);
impl<T: Copy + Debug> Iterator for IntoIter<T> {
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
            &node.elem
        })
    }
}

struct IterMut<'a, T: 'a> { next: Option<&'a mut Node<T>> }
impl<'a, T> Iterator for IterMut<'a, T> {
    type Item = &'a mut T;
    fn next(&mut self) -> Option<Self::Item> {
        self.next.take().map(|node| {
            self.next = node.next.as_deref_mut();
            &mut node.elem
        })
    }
}

fn main() {
    basic();
    iter();

    fn basic() {
        let mut lvec1: LVec<i32> = LVec::new();
        lvec1.push(10); lvec1.push(11);
```

```rust
        lvec1.push(12); lvec1.push(13);
        lvec1.insert(0,9);

        lvec1.print_lvec();

        let mut lvec2: LVec<i32> = LVec::new();
        lvec2.insert(0, 8);
        lvec2.append(&mut lvec1);

        println!("len: {}", lvec2.len());
        println!("pop {:?}", lvec2.pop().unwrap());
        println!("remove {:?}", lvec2.remove(0).unwrap());

        lvec2.print_lvec();
        lvec2.clear();
        lvec2.print_lvec();
    }

    fn iter() {
        let mut lvec: LVec<i32> = LVec::new();
        lvec.push(10); lvec.push(11);
        lvec.push(12); lvec.push(13);

        let sum1 = lvec.iter().sum::<i32>();
        let mut addend = 0;
        for item in lvec.iter_mut() {
            *item += 1;
            addend += 1;
        }
        let sum2 = lvec.iter().sum::<i32>();
        println!("{sum1} + {addend} = {sum2}");

        assert_eq!(50, lvec.into_iter().sum::<i32>());
    }
}
```

Here is the execution result.

```text
9
10
11
12
13
len: 6
pop 13
remove 8
9
10
11
12
Empty lvec
46 + 4 = 50
```

It’s important to note that LVec is a linked list with n nodes, and any method that requires traversing nodes, such as insert, push, pop, remove, etc., has a time complexity of O(n). Although on average it may only require traversing half as many nodes, in the worst case, every node in the list must be processed.
