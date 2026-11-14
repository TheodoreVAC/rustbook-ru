## 7.6 The Shell Sort

Shell sort, also known as diminishing increment sort, is a sorting algorithm that divides the original set into smaller subsets and applies insertion sort to each subset. The way of selecting subsets is the key to Shell sort. Rather than evenly splitting the set into contiguous sublists, Shell sort selects items every few items to add to the subset, with the distance between them called the gap.

![Figure 7.3: Shell sort](images/fig-7.3.png)

*Figure 7.3: Shell sort*

To understand Shell sort, consider the figure above. The set in the figure has nine items. If a gap of three is used, there will be a total of three subsets, each with three items of the same color. These separated elements can be considered as connected together, so insertion sort can be used to sort elements of the same color. After sorting the subsets, the overall set is still unordered, as shown in the figure below. Although the overall set is unordered, it is not completely unordered. Subsets of the same color are ordered. By sorting the entire set using insertion sort, the set can be completely sorted quickly. The number of insertion sort moves is small at this point because adjacent items are in their own subsets’ ordered positions, and these adjacent items are almost ordered. Therefore, only a few insertion moves are needed to complete the sorting.

![Figure 7.4: Shell sort](images/fig-7.4.png)

*Figure 7.4: Shell sort*

In Shell sort, the increment is the key feature, and different increments can be used to determine the number of subsets. The gap value is adjusted continuously in the implementation of Shell sort to achieve sorting.

```rust
// shell_sort.rs

fn shell_sort(nums: &mut [i32]) {
    // Internal function for insertion sort
    // with elements exhcanged distance is gap
    fn ist_sort(nums: &mut [i32], start: usize, gap: usize) {
        let mut i = start + gap;

        while i < nums.len() {
            let mut pos = i;
            let curr = nums[pos];

            while pos >= gap && curr < nums[pos - gap] {
                nums[pos] = nums[pos - gap];
                pos -= gap;
```

```rust
            }

            nums[pos] = curr;
            i += gap;
        }
    }

    // minimize the gap in every loop untill 1
    let mut gap = nums.len() / 2;
    while gap > 0 {
        for start in 0..gap {
            ist_sort(nums, start, gap);
        }

        gap /= 2;
    }
}
```

The following are use cases.

```rust
fn main() {
    let mut nums = [54,32,99,18,75,31,43,56,21,22];
    shell_sort(&mut nums);
    println!("sorted nums: {:?}", nums);
    // sorted nums: [18, 21, 22, 31, 32, 43, 54, 56, 75, 99]

    let mut nums = [1000,-1,2,-20,89,64,0,99,73];
    shell_sort(&mut nums);
    println!("sorted nums: {:?}", nums);
    // sorted nums: [-20, -1, 0, 2, 64, 73, 89, 99, 1000]
}
```

Shell sort divides the original set into smaller subsets and applies insertion sort to each subset. The subsets are selected by choosing an item every few items with the distance between them called the gap. The set is then considered as connected together, and insertion sort is used to sort elements of the same color. The final insertion operation in Shell sort is much less than in insertion sort because the collection has been pre-sorted by earlier increments. This makes the overall sorting very efficient. Although the complexity analysis of Shell sort is slightly more complicated, it is roughly between O(n) and O(n2). By changing the gap value according to the formula 2k −1 (1, 3, 7, 15, 31), the

3 2 ), which is very fast. Additionally, binary search can

complexity of Shell sort is approximately O(n be used to further improve Shell sort, similar to insertion sort. However, the index processing in binary search needs to add the gap value. Readers are encouraged to think about implementing this improved algorithm.
