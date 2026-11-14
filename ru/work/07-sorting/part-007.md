## 7.7 The Merge Sort

The previouly learned divide and conquer strategy can be used to improve the performance of sorting algorithms, specifically merge sort. Both merge sort and quicksort use recursion to continuously divide the list in half for sorting. If the set has only one item, it is considered sorted. If there are multiple items, the set is split, and recursive calls to merge sort are made for both intervals. Once sorted, a merge operation combines the two intervals into a single sorted set. This process is illustrated in the figures shown below.

![Figure 7.5: Split procedures of merge sort](images/fig-7.5.png)

*Figure 7.5: Split procedures of merge sort*

![Figure 7.6: Merge procedures of merge sort](images/fig-7.6.png)

*Figure 7.6: Merge procedures of merge sort*

Merge sort breaks down the set into basic cases with one or two elements, allowing for easy direct comparison. Then, the merge process begins by first sorting the smallest subsequence of the basic case. Two-by-two merging is performed until the set is completely sorted. Even if the set is not evenly divided, the performance is not affected, as the difference is at most one element. The merge operation is straightforward, as each subsequence is already sorted, and only one comparison is necessary at a time. The resulting sequence is always ordered. Below is a Rust implementation of merge sort, consisting of two sorts and one merge operation, which is straightforward.

```rust
// merge_sort.rs

fn merge_sort(nums: &mut [i32]) {
    if nums.len() > 1 {
        let mid = nums.len() >> 1;
        merge_sort(&mut nums[..mid]); // sort the first half
        merge_sort(&mut nums[mid..]); // sort the last half
        merge(nums, mid); // merge all
```

```rust
    }
}

fn merge(nums: &mut [i32], mid: usize) {
    let mut i = 0; // mark element in first half of data
    let mut k = mid; // mark element in last half of data
    let mut temp = Vec::new();

    for _j in 0..nums.len() {
        if k == nums.len() || i == mid {
            break;
        }

        // put into a temp colletion
        if nums[i] < nums[k] {
            temp.push(nums[i]);
            i += 1;
        } else {
            temp.push(nums[k]);
            k += 1;
        }
    }

    // to make sure all data been solved
    if i < mid && k == nums.len() {
        for j in i..mid {
            temp.push(nums[j]);
        }
    } else if i == mid && k < nums.len() {
        for j in k..nums.len() {
            temp.push(nums[j]);
        }
    }

    // put temp data back to nums, finish sort
    for j in 0..nums.len() {
        nums[j] = temp[j];
    }
}

fn main() {
    let mut nums = [54,32,99,22,18,75,31,43,56,21];
    merge_sort(&mut nums);
    println!("sorted nums: {:?}", nums);
    // sorted nums: [18, 21, 22, 31, 32, 43, 54, 56, 75, 99]
}
```

To analyze the time complexity of merge sort, we can divide the sorting process into two parts: sorting and merging. The sorting complexity is O(log2(n)), as we learned in the binary search section. The merging step involves placing each item in the set on the sorted list, with a maximum of n times, resulting in a complexity of O(n). As recursive and merging operations are combined, the performance of merge sort is O(nlog2(n)).

The space complexity of merge sort is relatively high at O(n). To reduce space usage, we can consider optimizing merge sort using insertion sort. One approach is to use insertion sort directly when the length is less than a certain threshold(such as 64) and to use merge sort when the length is greater than the threshold. This algorithm is called insertion merge sort and improves the merge sort algorithm to some extent. However, implementation details are left to the reader.
