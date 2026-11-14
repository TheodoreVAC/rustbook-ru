## 7.5 The Insertion Sort

Insertion sort achieves sorting by iteratively inserting data items into a sorted subsequence. Although its performance is still O(n2), its approach is distinct from other sorting algorithms. It always maintains a sorted subsequence at the lower end of the dataset and inserts new items into the subsequence, expanding it until the entire collection is sorted. The algorithm starts by assuming that the initial subsequence has only one item located at position 0. During the next traversal, items 1 to n-1 are compared with the first item. If an item is smaller than the first item, it is inserted before the first item. If it is larger than the first item, the subsequence is expanded by one. This process is repeated for the remaining unsorted items until the entire collection is sorted. In the following figure, the sorted region is shown in red, and the unsorted region in blue. Each row represents a sorting operation, and the bottom row shows the sorted result.

![Figure 7.2: Insertion sort](images/fig-7.2.png)

*Figure 7.2: Insertion sort*

```rust
// insertion_sort.rs
fn insertion_sort(nums: &mut [i32]) {
    if nums.len() < 2 { return; }
    for i in 1..nums.len() {
        let mut pos = i;
        let curr = nums[i];
        while pos > 0 && curr < nums[pos-1] {
            // move element to right
            nums[pos] = nums[pos-1];
            pos -= 1;
        }

        // insert element: curr
        nums[pos] = curr;
    }
}
fn main() {
    let mut nums = [54,32,99,18,75,31,43,56,21];
    insertion_sort(&mut nums);
    println!("sorted nums: {:?}", nums);
    // sorted nums: [18, 21, 31, 32, 43, 54, 56, 75, 99]
}
```

The insertion sort requires comparing each new element with the already sorted elements one by one. However, the binary search algorithm discussed in Chapter 6 can efficiently locate the position of an element in a sorted subsequence. Therefore, binary search can be utilized for acceleration.

```rust
// binary_insertion_sort.rs

fn binary_insertion_sort(nums: &mut [i32]) {
    let mut temp;
    let mut left;
    let mut mid;
    let mut right;

    for i in 1..nums.len() {
        left = 0;

        // Sorted array boundaries
        right = i - 1;

        // Data to be sorted
        temp = nums[i];

        // Binary search finds the position of temp
        while left <= right {
            mid = (left + right) >> 1;
            if temp < nums[mid] {
                // To prevent right = 0 - 1 case
                if 0 == mid {
                    break;
                }
                right = mid - 1;
            } else {
                left = mid + 1;
            }
        }

        // Move data back
        for j in (left..=i-1).rev() {
            nums.swap(j, j+1);
        }

        // Insert temp into the empty space
        if left != i {
            nums[left] = temp;
        }
    }
}

fn main() {
    let mut nums = [1,3,2,8,6,4,9,7,5,10];
    binary_insertion_sort(&mut nums);
    println!("sorted nums: {:?}", nums);
    // sorted nums: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
}
```
