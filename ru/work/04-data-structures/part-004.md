## 4.4 Queue

A queue is an ordered collection of items that has a front and a rear end. New items are added at the rear, and items are removed from the front. Each element added to the queue moves towards the front until it becomes the next item to be removed. This type of ordering is known as First In First Out (FIFO). A stack, in contrast, uses Last In First Out (LIFO) ordering. Queues are commonly used in everyday situations such as long lines of people waiting to board a train or bus, or at self-service restaurants. Queues have limited behavior because they have only one entrance and one exit. It is not possible to cut in line or leave early; one must wait for their turn. While it is true that real-life queues and queue data structures may allow cutting in line, this discussion does not consider that possibility. Operating systems use queues as a data structure to control processes. Multiple different queues are used in scheduling algorithms to prioritize executing programs as quickly as possible and service as many users as possible. When typing on a keyboard, a delay may occur before characters appear on the screen. This is because the keystrokes are placed in a buffer similar to a queue.

![Figure 4.11: Queue](images/fig-4.11.png)

*Figure 4.11: Queue*

### 4.4.1 The Queue Abstract Data Type

A queue is a data structure that maintains the FIFO sorting property. It is defined by the following structure and operations:

- new() creates a new queue, takes no parameters, and returns an empty queue.
- enqueue(item) adds a new item to the end of the queue, takes item as a parameter, no return.
- dequeue() removes an item from the front of the queue, takes no parameters, returns the removed item, and modifies the queue.
- is_empty() checks whether the queue is empty, takes no parameters, and returns a Boolean value.
- size() returns the number of items in the queue, takes no parameters, and returns a usize integer.
- iter() returns an immutable iteration of the queue, the queue remains unchanged, and takes no parameters.
- iter_mut() returns a mutable iteration of the queue, the queue is mutable, and takes no parameters.
- into_iter() changes the queue into an iteration, consumes the queue, and takes no parameters.

Assuming an empty queue q has already been created, the table below shows the expected results of various queue operations, with the front of the queue on the left:

**Table 4.4: Queue Operations**

| operation | value | return |
| --- | --- | --- |
| q.is_empty() | [] | true |
| q.enqueue(1) | [1] |  |
| q.enqueue(2) | [1,2] |  |
| q.enqueue(3) | [1,2,3] |  |
| q.dequeue() | [2,3] | 1 |
| q.enqueue(4) | [2,3,4] |  |
| q.enqueue(5) | [2,3,4,5] |  |
| q.deque() | [3,4,5] | 2 |
| q.size() | [3,4,5] | 3 |
| q.is_empty() | [3,4,5] | false |

### 4.4.2 Implementing a Queue in Rust

To implement a queue in Rust, we can use a Vec with the left end as the rear end of the queue and the right end as the front end. Adding an element to the queue has a complexity of O(n), while removing an element has a complexity of O(1). To prevent the queue from growing infinitely, we can set a cap parameter to limit its length.

```rust
// queue.rs

#[derive(Debug)]
struct Queue<T> {
    cap: usize, // capacity
    data: Vec<T>, // store elements
}

impl<T> Queue<T> {
    fn new(size: usize) -> Self {
        Self { cap: size, data: Vec::with_capacity(size) }
    }

    fn is_empty(&self) -> bool { 0 == Self::len(&self) }

    fn is_full(&self) -> bool { self.len() == self.cap }

    fn len(&self) -> usize { self.data.len() }

    fn clear(&mut self) {
        self.data = Vec::with_capacity(self.cap);
    }

    fn enqueue(&mut self, val: T) -> Result<(), String> {
        if self.len() == self.cap { // check left space
            return Err("No space available".to_string());
        }
        self.data.insert(0, val);
        Ok(())
    }

    // pop out values
    fn dequeue(&mut self) -> Option<T> {
        if self.len() > 0 {
            self.data.pop()
        } else {
            None
        }
    }

    // Implemntion of iterations for a queue
    // into_iter: queue modified and became a iterator
    // iter: queue unmodified and get a unmutable iterator
    // iter_mut: queue unmodified and get a mutable iterator
    fn into_iter(self) -> IntoIter<T> {
        IntoIter(self)
```

```rust
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

// Implemention of 3 iterations
struct IntoIter<T>(Queue<T>);
impl<T: Clone> Iterator for IntoIter<T> {
    type Item = T;
    fn next(&mut self) -> Option<Self::Item> {
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
```

```rust
        }
    }
}
fn main() {
    basic();
    iter();
    fn basic() {
        let mut q = Queue::new(4);
        let _r1 = q.enqueue(1); let _r2 = q.enqueue(2);
        let _r3 = q.enqueue(3); let _r4 = q.enqueue(4);
        if let Err(error) = q.enqueue(5) {
            println!("Enqueue error: {error}");
        }
        if let Some(data) = q.dequeue() {
            println!("dequeue data: {data}");
        } else {
            println!("empty queue");
        }
        println!("empty: {}, len: {}", q.is_empty(), q.len());
        println!("full: {}", q.is_full());
        println!("q: {:?}", q);
        q.clear();
        println!("{:?}", q);
    }

    fn iter() {
        let mut q = Queue::new(4);
        let _r1 = q.enqueue(1); let _r2 = q.enqueue(2);
        let _r3 = q.enqueue(3); let _r4 = q.enqueue(4);
        let sum1 = q.iter().sum::<i32>();
        let mut addend = 0;
        for item in q.iter_mut() {
            *item += 1;
            addend += 1;
        }
        let sum2 = q.iter().sum::<i32>();
        println!("{sum1} + {addend} = {sum2}");
        println!("sum = {}", q.into_iter().sum::<i32>());
    }
}
```

Here is the result of the execution.

```text
Enqueue error: No space available
dequeue data: 1
empty: false, len: 3
full: false
q: Queue { cap: 4, data: [4, 3, 2] }
Queue { cap: 4, data: [] }
10 + 4 = 14
sum = 14
```

### 4.4.3 Hot Potato

A queue is commonly used to simulate real-world scenarios where data is processed in a FIFO (firstin, first-out) manner. For instance, the game of hot potato involves children forming a circle and passing a potato quickly to the child next to them, with the objective of keeping the potato moving as if it were hot (see Figure 4.12). When the passing action stops, the child holding the potato is removed from the circle. The game continues until only one child remains. The game is similar to musical chairs, where people perform an action such as speaking, dancing, or leaving their seat when the music stops.

![Figure 4.12: hot potato](images/fig-4.12.png)

*Figure 4.12: hot potato*

The game of hot potato is comparable to the Josephus problem, a legendary story recounted by the historian Flavius Josephus. Josephus and his comrades were trapped by the Roman army in a cave and chose to die instead of becoming Roman slaves. They formed a circle and counted clockwise to the eighth person, who was then killed. This continued until only one person was left alive. As a mathematician, Josephus figured out where he should sit to be the last person alive and ultimately joined the Roman side. While there are variations of this story, the fundamental ideas of both the hot potato game and the Josephus problem can be simulated using a queue.

![Figure 4.13: Simulation of game of hot potato](images/fig-4.13.png)

*Figure 4.13: Simulation of game of hot potato*

To implement the hot potato game, the program accepts multiple names of children and a constant num to set the count of how many children to skip before removing one. Assuming the child holding the hot potato is always at the front of the queue, they leave the queue and re-enter at the back, effectively passing the potato to the next child who must be at the front of the queue. After num rounds of dequeuing

and enqueuing, the child at the front of the queue is permanently removed. The process repeats until only one name remains. The queue model for the Hot Potato game is clearly illustrated in the two figures above. Here is the implementation of the game based on this model.

```rust
// hot_potato.rs

fn hot_potato(names: Vec<&str>, num: usize) -> &str {
    // Initialize the queue and enqueue the names
    let mut q = Queue::new(names.len());
    for name in names {
        let _nm = q.enqueue(name);
    }

    while q.size() > 1 {
        // Dequeue and enqueue the names,
        // which simulates passing the potato
        for _i in 0..num {
            let name = q.dequeue().unwrap();
            let _rm = q.enqueue(name);
        }

        // After num dequeue/enqueue cycles
        // remove one person
        let _rm = q.dequeue();
    }

    q.dequeue().unwrap()
}
fn main() {
    let name = vec!["Mon","Tom","Kew","Lisa","Marry","Bob"];
    let survivor = hot_potato(name, 8);
    println!("The survival person is {survivor}");
    // The survival person is Marry
}
```

It is worth noting that the counting value used in the implementation is 8, which is greater than the number of people in the queue (which is 6). However, this is not a problem because the queue functions like a circle that returns to the head after reaching the tail, and continues until the count is reached. Therefore, there will always be someone dequeued in the end.
