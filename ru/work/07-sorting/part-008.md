## 7.8 The Selection Sort

Selection sort is a more efficient version of bubble sort, as it performs only one data exchange per round by seeking only the index of the maximum value during traversal. After completing the traversal, it swaps that maximum item into its correct position. Like bubble sort, after the first traversal, the maximum item is in the last position, and after the second traversal, the second-largest value is in the second-to-last position. To sort n items, n-1 passes are required. Although selection sort and bubble sort have the same number of comparisons, selection sort is faster because of its reduced number of data exchanges. The time complexity of both algorithms is O(n2). The figure below shows the entire sorting process of selection sort, in which the maximum unsorted item is selected during each traversal and placed in the correct position. Unlike bubble sort, selection sort does not exchange pairs during the traversal.

![Figure 7.7: Selection sort](images/fig-7.7.png)

*Figure 7.7: Selection sort*

```rust
// selection_sort.rs

fn selection_sort(nums: &mut Vec<i32>) {
    let mut left = nums.len() - 1; // left marker
    while left > 0 {
        let mut pos_max = 0;
        for i in 1..=left {
            if nums[i] > nums[pos_max] {
                pos_max = i; // current loop's max value
            }
        }
        nums.swap(left, pos_max);
```

```rust
        left -= 1; // unsorted elements reduced by 1
    }
}

fn main() {
    let mut nums = vec![54,32,99,18,75,31,43,56,21,22];
    selection_sort(&mut nums);
    println!("sorted nums: {:?}", nums);
    // sorted nums: [18, 21, 22, 31, 32, 43, 54, 56, 75, 99]
}
```

Although bubble sort and selection sort have the same time complexity, there are still opportunities for optimization. One such optimization is to perform bidirectional sorting, which can be achieved by adopting the cocktail sort approach. Similarly, selection sort can also be modified to perform bidirectional sorting, which changes the coefficient of complexity but not the overall time complexity. Readers are encouraged to consider the implementation of this approach.
