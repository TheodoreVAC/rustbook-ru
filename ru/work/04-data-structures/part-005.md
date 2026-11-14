## 4.5 Deque

A deque also is a linear data structure with two ends: the front and the rear. Unlike a queue, a deque allows items to be added and removed from both ends. This flexibility makes it a hybrid linear structure that can function as both a stack and a queue. Although a deque shares similarities with both a stack and a queue, it does not enforce LIFO or FIFO ordering. The order of adding and removing data determines whether it acts like a stack or a queue. It is important to note that a deque should not be used as a replacement for either a stack or a queue, as each data structure has its own unique properties and is designed for specific computational purposes. The image below provides an example of Deque.

![Figure 4.14: Deque](images/fig-4.14.png)

*Figure 4.14: Deque*

### 4.5.1 The Deque Abstract Data Type

The deque data structure is an ordered collection of items that allows adding and removing items from either end. It is defined by the following operations:

- new() creates a new deque with no arguments and returns an empty deque.
- add_front(item) adds item to the front of the deque, requiring item as a parameter, and does not return any content.
- add_rear(item) adds item to the back of the deque, requiring item as a parameter, and does not return any content.
- remove_front() removes the front item from the deque, requiring no arguments, returns item, and modifies the deque.
- remove_rear() removes the rear item from the deque, requiring no arguments, returns item, and modifies the deque.
- is_empty() tests whether the deque is empty, requires no arguments, and returns a boolean value.
- size() returns the number of items in the deque, requires no arguments, and returns a usize integer.
- iter() returns an immutable iteration form of the deque, with the deque unchanged and no arguments required.
- iter_mut() returns a mutable iteration form of the deque, with the deque mutable and no arguments required.
- into_iter() changes the deque into an iterable form, with the deque consumed and no arguments required.

Assuming that d is an already created empty deque, the following table shows the results of a series of operations. Note that the front is on the right-hand side. When moving items in and out, it is important to keep track of the front and back contents, as modifying both ends can make the result look somewhat messy.

**Table 4.5: Deque Operations**

| operations | value | return |
| --- | --- | --- |
| d.is_empty() | [] | true |
| d.add_rear(1) | [1] |  |
| d.add_rear(2) | [2,1] |  |
| d.add_front(3) | [2,1,3] |  |
| d.add_front(4) | [2,1,3,4] |  |
| d.remove_rear() | [1,3,4] | 2 |
| d.remove_front() | [1,3] | 4 |
| d.size() | [1,3] | 2 |
| d.is_empty() | [1,3] | false |
| d.add_front(2) | [1,3,2] |  |
| d.add_rear(4) | [4,1,3,2] |  |
| d.size() | [4,1,3,2] | 4 |
| d.is_empty() | [4,1,3,2] | false |
| d.add_rear(5) | [5,4,1,3,2] |  |
| d.add_front(10) | [5,4,1,3,2,10] |  |

### 4.5.2 Implementing a Deque in Rust

To implement the deque abstract data type in Rust, we can use a Vec as the underlying data structure. The left end of the Vec serves as the rear of the deque, while the right end serves as the front. To prevent the deque from growing indefinitely, a capacity parameter is added to control the maximum length of the deque.

```rust
// deque.rs

// deque definition
#[derive(Debug)]
struct Deque<T> {
    cap: usize, // capacity
    data: Vec<T>, // save elements in data
}

impl<T> Deque<T> {
    fn new(cap: usize) -> Self {
        Self {
            cap: cap,
            data: Vec::with_capacity(cap),
        }
    }

    fn is_empty(&self) -> bool {
        0 == self.len()
    }

    fn is_full(&self) -> bool {
        self.len() == self.cap
    }

    fn len(&self) -> usize {
        self.data.len()
    }

    fn clear(&mut self) {
        self.data = Vec::with_capacity(self.cap);
    }

    // use the tail of a Vec as the start of the deque
    fn add_front(&mut self, val: T) -> Result<(), String> {
        if self.len() == self.cap {
            return Err("No space avaliable".to_string());
        }
        self.data.push(val);

        Ok(())
    }

    // the head of the Vec is the tail of the deque
    fn add_rear(&mut self, val: T) -> Result<(), String> {
        if self.len() == self.cap {
```

```rust
            return Err("No space avaliabl".to_string());
        }
        self.data.insert(0, val);

        Ok(())
    }

    // remove data from queue head
    fn remove_front(&mut self) -> Option<T> {
        if self.len() > 0 {
            self.data.pop()
        } else {
            None
        }
    }

    // remove data from queue tail
    fn remove_rear(&mut self) -> Option<T> {
        if self.len() > 0 {
            Some(self.data.remove(0))
        } else {
            None
        }
    }

    // Implemention of iteration for the deque
    // into_iter: deque modified and became a iterator
    // iter: deque unmodified and get a unmutable iterator
    // iter_mut: deque unmodified and get a mutable iterator
    fn into_iter(self) -> IntoIter<T> {
        IntoIter(self)
    }

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
```

```rust
// Implementing 3 iterations
struct IntoIter<T>(Deque<T>);
impl<T: Clone> Iterator for IntoIter<T> {
    type Item = T;
    fn next(&mut self) -> Option<Self::Item> {
        // first element of a tuple is not empty
        if !self.0.is_empty() {
            Some(self.0.data.remove(0))
        } else {
            None
        }
    }
}

struct Iter<'a, T: 'a> { stack: Vec<&'a T>, }
impl<'a, T> Iterator for Iter<'a, T> {
    type Item = &'a T;
    fn next(&mut self) -> Option<Self::Item> {
        if 0 != self.stack.len() {
            Some(self.stack.remove(0))
        } else {
            None
        }
    }
}

struct IterMut<'a, T: 'a> { stack: Vec<&'a mut T> }
impl<'a, T> Iterator for IterMut<'a, T> {
    type Item = &'a mut T;
    fn next(&mut self) -> Option<Self::Item> {
        if 0 != self.stack.len() {
            Some(self.stack.remove(0))
        } else {
            None
        }
    }
}

fn main() {
    basic();
    iter();

    fn basic() {
        let mut d = Deque::new(4);
        let _r1 = d.add_front(1);
        let _r2 = d.add_front(2);
        let _r3 = d.add_rear(3);
        let _r4 = d.add_rear(4);

        if let Err(error) = d.add_front(5) {
            println!("add_front error: {error}");
        }
```

```rust
        println!("{:?}", d);

        match d.remove_rear() {
            Some(data) => println!("remove rear data {data}"),
            None => println!("empty deque"),
        }

        match d.remove_front() {
            Some(data) => println!("remove front data {data}"),
            None => println!("empty deque"),
        }
        println!("empty: {}, len: {}", d.is_empty(), d.len());
        println!("full: {}, {:?}", d.is_full(), d);

        d.clear();
        println!("{:?}", d);
    }

    fn iter() {
        let mut d = Deque::new(4);
        let _r1 = d.add_front(1);
        let _r2 = d.add_front(2);
        let _r3 = d.add_rear(3);
        let _r4 = d.add_rear(4);

        let sum1 = d.iter().sum::<i32>();
        let mut addend = 0;
        for item in d.iter_mut() {
            *item += 1;
            addend += 1;
        }

        let sum2 = d.iter().sum::<i32>();
        println!("{sum1} + {addend} = {sum2}");
        assert_eq!(14, d.into_iter().sum::<i32>());
    }
}
```

Here is an example output of an execution.

```text
add_front error: No space avaliable
Deque { cap: 4, data: [4, 3, 1, 2] }
remove rear data 4
remove front data 2
empty: false, len: 2
full: false, Deque { cap: 4, data: [3, 1] }
Deque { cap: 4, data: [] }
10 + 4 = 14
```

As we can see from the output, a deque has similarities to both a queue and a stack, and can be thought of as a combination of the two. The specific implementation of a deque can vary depending on the situation, and which end is considered the front and which end is considered the rear should be determined based on the context.

### 4.5.3 Palindrome Checker

Palindromes are strings in which the characters at the same position from both ends are the same, such as ”radar”, ”sos”, and ”rustsur”. In this section, we will present an algorithm for checking whether a given string is a palindrome. One approach is to use a queue to enqueue the characters of the string and then dequeue the characters to compare them with the reversed original string. This method is simple, but it requires a lot of memory. A more efficient approach is to use a deque.

![Figure 4.15: Palindrome Checker](images/fig-4.15.png)

*Figure 4.15: Palindrome Checker*

To check for palindromes using a deque, we start by processing the input string from left to right and adding each character to the rear of the deque. At this point, the front of the deque holds the first character of the string, while the rear holds the last character. We can then use the deque’s feature of dequeuing from both ends to compare the front and rear characters. If they match, we continue dequeuing the front and rear characters until either all the characters are used up, leaving an empty deque, or a deque of size 1 is left. In both cases, the string is a palindrome. Any other situation indicates that the string is not a palindrome. Below is the code implementaion of palindrome detection using a deque.

```rust
// palindrome_checker.rs
fn palindrome_checker(pal: &str) -> bool {
    let mut d = Deque::new(pal.len());
    for c in pal.chars() {
        let _r = d.add_rear(c);
    }

    let mut is_pal = true;
    while d.size() > 1 && is_pal {
        let head = d.remove_front();
        let tail = d.remove_rear();
        if head != tail {
            is_pal = false;
        }
    }
    is_pal
}

fn main() {
    let pal = "rustsur";
    let is_pal = palindrome_checker(pal);
    println!("{pal} is palindrome string: {is_pal}");
    // rustsur is palindrome string: true

    let pal = "panda";
    let is_pal = palindrome_checker(pal);
    println!("{pal} is palindrome string: {is_pal}");
    // panda is palindrome string: false
}
```
