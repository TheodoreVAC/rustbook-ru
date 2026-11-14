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
