## 7.9 The Heap Sort

In addition to linear data structures like stacks and queues, non-linear data structures also exist in computers, one of which is the heap. A heap is a non-linear complete binary tree with left and right child nodes. The height of a tree with n nodes is log(n). Though trees are not studied until Chapter 8, comprehending them here can help understand the properties of heaps. There are two types of heaps: min-heaps and max-heaps. A min-heap has every node with a value less than or equal to its left and right child nodes, whereas a max-heap has every node with a value greater than or equal to its left and right child nodes. Figure (7.8) illustrates an example of a min-heap.

![Figure 7.8: Min heap](images/fig-7.8.png)

*Figure 7.8: Min heap*

Heap sort is a sorting algorithm designed using the heap data structure. It repeatedly selects the top element and moves it to the end, then rebuilds the heap to implement the sorting. It is a selection sort with worst-case, best-case, and average time complexity of O(nlog2(n)) and is an unstable sort. As shown in the figure above, the heap is similar to a linked list with multiple connections. The nodes in the heap are numbered by layer, and if this logical structure is mapped to an array, it looks like the figure below, where the first position, index 0, is occupied by 0.

![Figure 7.9: Array as a min heap](images/fig-7.9.png)

*Figure 7.9: Array as a min heap*

It is possible to represent heaps not only with trees, but also with arrays or Vecs(show in figure above). In fact, using arrays or Vecs to represent heaps is more in line with the literal meaning of the word ”heap,” which refers to a collection of things gathered together. Note that our index starts from 1, which allows us to represent the indices of the left and right child nodes as 2i and 2i+1, making it easier to calculate. To satisfy the requirements of a binary tree’s node relationships, a heap represented by an array should meet the following criteria:

- Max heap: arr[i] >= arr[2i] and arr[i] >= arr[2i+1]
- Min heap: arr[i] <= arr[2i] and arr[i] <= arr[2i+1]

Heap sort involves constructing an unsorted sequence into a min heap. The minimum value of the entire sequence is then the root node of the heap. Swap it with the last element of the sequence, and the last element becomes the minimum value. This minimum value is no longer considered in the heap, and the remaining n-1 elements are reconstructed into a heap, producing a new minimum value. Swap this minimum value to the end of the new heap, and you will have two sorted values. Repeat this process until the entire sequence is sorted.A min heap produces a descending order sorting, while a max heap produces an ascending order sorting. To better illustrate the heap sort process, a figure is provided below. The dark gray color represents the minimum element, which has been replaced by 92 and is no longer part of the heap. When 92 is at the top of the heap, it is no longer a min heap, so a new min heap is constructed to make the minimum value 24 at the top of the heap. Then, 24 is swapped with the last element in the heap, and the second-to-last element becomes dark gray. Note that the dotted line indicates that this element no longer belongs to the heap. Continuing to swap, the dark gray subsequence gradually fills the entire heap in reverse order from the last level, achieving a reverse sorting from largest to smallest. To achieve sorting from smallest to largest, a max heap should be constructed, and the corresponding logic in the min heap should be modified.

92 31 24 56 66 72 44 84 19 24 44 31 84 56 66 72 92 19 31 44 66 84 56 92 72 24 19

Here is an implementation of heap sort.

```rust
// heap_sort.rs

// calculate index of parent node
macro_rules! parent {
    ($child:ident) => {
        $child >> 1
    };
}

// calculate index of left child node
macro_rules! left_child {
    ($parent:ident) => {
        $parent << 1
    };
}

// calculate index of right child node
macro_rules! right_child {
    ($parent:ident) => {
        ($parent << 1) + 1
    };
}

fn heap_sort(nums: &mut [i32]) {
    if nums.len() < 2 { return; }

    let len = nums.len() - 1;
    let last_parent = parent!(len);
    for i in (1..=last_parent).rev() { // build a min-heap
        move_down(nums, i); // begins from 1
    }

    for end in (1..nums.len()).rev() { // rebuild min-heap
        nums.swap(1, end);
        move_down(&mut nums[..end], 1);
    }
}

// move down greater element
fn move_down(nums: &mut [i32], mut parent: usize) {
    let last = nums.len() - 1;
    loop {
        let left = left_child!(parent);
        let right = right_child!(parent);
        if left > last { break; }

        // right <= last: determin if right child node exists
        let child = if right <= last
                    && nums[left] < nums[right] {
            right
```

```rust
        } else {
            left
        };

        // swap data if child node is greater than parent node
        if nums[child] > nums[parent] {
            nums.swap(parent, child);
        }

        // update parent and child relationship
        parent = child;
    }
}

fn main() {
    let mut nums = [0,54,32,99,18,75,31,43,56,21,22];
    heap_sort(&mut nums);
    println!("sorted nums: {:?}", nums);
    // sorted nums: [0, 18, 21, 22, 31, 32, 43, 54, 56, 75, 99]
}
```

The heap is a binary tree with a time complexity of O(nlog(n)). The time is mainly consumed in two parts: building the heap and adjusting the heap n times. Building the heap processes n elements with a complexity of O(n). The longest path for each adjustment is from the root to the leaf, which is the height of the heap, logn. Therefore, the time complexity of n adjustments is O(nlog(n)), and the final total time complexity is O(nlog(n)). Macros are used here to obtain node indexes, and functions can also be used to implement them. Heap sort and selection sort are similar in that they both find the maximum or minimum value in a set.
