## 6.4 The Binary Search

An ordered dataset is advantageous for search algorithms because sequential search on sorted data sets requires comparing only n-1 remaining items if the first item is not the one being searched for. However, although this method can be terminated when a value outside of the range is encountered, it is still relatively slow. Is there a faster search algorithm for sorted datasets? Absolutely, it’s called binary search. In the following discussion, we will analyze and implement binary search in Rust.

### 6.4.1 Implementing a Binary Search

As its name implies, binary search is a very important search algorithm that works by dividing the dataset into two parts for searching using low, mid, and high to control the range of the search. It starts from the middle item, not in order. If the middle item is the one being searched for, the search is completed. If it is not, we can use the ordered property of the sorted set to eliminate half of the remaining items. If the item being searched for is greater than the middle item, we can eliminate the middle item and the half of the elements smaller than the middle item, which means we don’t need to compare the first item to the middle item. This is because, if the target item is greater than the middle value, it is definitely not in the first half, whether it is in the set or not. Conversely, if the target item is less than the middle item, the second half of the data can be skipped. After removing half of the data, look at the middle item in the remaining half of the data, repeat the comparison and omission process, and finally obtain the result. This search is relatively fast and very intuitive, so it is called binary search.

![Figure 6.3: Binary search](images/fig-6.3.png)

*Figure 6.3: Binary search*

Binary search is a search algorithm that is used on sorted data sets. It is faster than sequential search since it divides the data set into two parts using low, mid, and high to control the range of the search. If the middle item is the one being searched for, the search is completed. If not, the ordered property of the

sorted set is used to eliminate half of the remaining items. By repeating the comparison and omission process, the target item is found relatively quickly. To implement binary search, we set low and high to the far left and far right, respectively. For instance, if we want to find 60, we compare it with the middle value of 44. If it is greater than 44, we move low to 56 and mid to 66. We then compare it with 66 and find that it is less than 66, so we move high to 58 and mid to 56. This process continues until we reach the target item.

```rust
// binary_search.rs

fn binary_search1(nums: &[i32], num: i32) -> bool {
    let mut low = 0;
    let mut high = nums.len() - 1;
    let mut found = false;

    // note: <= not <
    while low <= high && !found {
        let mid: usize = (low + high) >> 1;

        //low + high may cause overflow, use substraction
        //let mid: usize = low + ((high - low) >> 1);

        if num == nums[mid] {
            found = true;
        } else if num < nums[mid] {
            // num < mid, drop right half of data
            high = mid - 1;
        } else {
            // num >= mid, drop left half of data
            low = mid + 1;
        }
    }

    found
}

fn main() {
    let nums = [1,3,8,10,15,32,44,48,50,55,60,62,64];

    let target = 3;
    let found = binary_search1(&nums, target);
    println!("nums contains {target}: {found}");
    // nums contains 3: true

    let target = 63;
    let found = binary_search1(&nums, target);
    println!("nums contains {target}: {found}");
    // nums contains 63: false
}
```

Binary search satisfies the three laws of recursion and can be implemented using recursion. However, recursive implementation involves slicing the dataset and discarding the mid item, which can cause stack overflow risk. Therefore, it is generally recommended to use an iterative approach to implement binary search.

```rust
// binary_search.rs

fn binary_search2(nums: &[i32], num: i32) -> bool {
    // base case1: target does not exisit
    if 0 == nums.len() { return false; }

    let mid: usize = nums.len() >> 1;

    // base case2: target exisits
    if num == nums[mid] {
        return true;
    } else if num < nums[mid] {
        // minimize problem size
        return binary_search2(&nums[..mid], num);
    } else {
        return binary_search2(&nums[mid+1..], num);
    }
}

fn main() {
    let nums = [1,3,8,10,15,32,44,48,50,55,60,62,64];

    let target = 3;
    let found = binary_search2(&nums, target);
    println!("nums contains {target}: {found}");
    // nums contains 3: true

    let target = 63;
    let found = binary_search2(&nums, target);
    println!("nums contains {target}: {found}");
    // nums contains 63: false
}
```

In summary, binary search is a fast and intuitive search algorithm that works best on sorted data sets. It can be implemented using recursion but an iterative approach is generally preferred to avoid stack overflow risk.

### 6.4.2 Analysis of Binary Search

The binary search algorithm has a best-case scenario when the middle item is the target, and its time complexity is O(1). With each comparison, binary search eliminates half of the remaining items, allowing us to determine the worst-case complexity by finding the maximum number of comparisons. After the first comparison, there are n/2 remaining items, then n/4, and so on, until the remaining items are reduced to n/2i = 1, at which point the binary search ends.

n 2i = 1 (6.2) i = log2(n)

As a result, the binary search algorithm performs at most log2(n) comparisons, giving it a time complexity of O(log2(n)), which is superior to algorithms with a time complexity of O(n). However, it’s important to note that in the recursive implementation of binary search, the default stack usage consumes memory, resulting in a space complexity that’s inferior to the iterative version.

While binary search may seem efficient, it’s not worth sorting and using binary search when n is very small. In such cases, sequential search may be more efficient. Additionally, sorting large datasets for binary search can be time-consuming and memory-intensive, making sequential search a more efficient option. However, binary search is well-suited for datasets that are neither too large nor too small, making it an ideal choice for many practical scenarios.

### 6.4.3 The Interpolation Search

Interpolation search is a variant of binary search that’s specifically designed for sorted data. When the data is evenly distributed, interpolation search can quickly approach the search area and improve efficiency. Unlike binary search, interpolation search doesn’t use the median directly to bound the search range. Instead, it finds the upper and lower bounds using an interpolation algorithm. This algorithm uses two points (x0, y0) and (x1, y1) to perform linear interpolation and determine the value of y corresponding to any point x in the range [x0, x1] or the value of x corresponding to any y.

y −y0 = y1 −y0 x −x0 x1 −x0 (6.3)

x = (y −y0)(x1 −x0)

+ x0 y1 −y0

To illustrate this, let’s consider an example of searching for the element 27 in the sorted set of 14 elements [1, 9, 10, 15, 16, 17, 19, 23, 27, 28, 29, 30, 32, 35]. We use the index as the x-axis and the element value as the y-axis. It’s found that x0 = 0, x1 = 13, and y0 = 1, y1 = 35. Therefore, the x value corresponding to y = 27 can be calculated. x = (27 −1)(13 −0)

+ 0 35 −1 (6.4) x = 9

Starting with nums[9] which has a value of 28, which is greater than 27, we use it as the upper bound. Since the index of 28 is 9, we continue the interpolation algorithm to search for elements in the range [0,8]. x = (27 −1)(8 −0)

+ 0 27 −1 (6.5) x = 8

Finally, we arrive at nums[9], which has a value of 27, and the algorithm ends.

```rust
// interpolation_search.rs

fn interpolation_search(nums: &[i32], target: i32) -> bool {
    if nums.is_empty() {
        return false;
    }

    let mut low = 0usize;
    let mut high = nums.len() - 1;
    loop {
        let low_val = nums[low];
        let high_val = nums[high];

        // in this case, target isn't in the nums
        if high <= low || target < low_val
```

```rust
            || target > high_val {
            return false;
        }

        // calculate the position for insertion
        let offset = (target - low_val) * (high - low) as i32
                     / (high_val - low_val);
        let interpolant = low + offset as usize;

        // update high and low
        if nums[interpolant] > target {
            high = interpolant - 1;
        } else if nums[interpolant] < target {
            low = interpolant + 1;
        } else {
            // found: nums[interpolant] = target
            return true;
        }
    }
}
```

Here is an use example of this search.

```rust
fn main() {
    let nums = [1,9,10,15,16,17,19,23,27,28,29,30,32,35];
    let target = 27;
    let found = interpolation_search(&nums, target);
    println!("nums contains {target}: {found}");
    // nums contains 27: true

    let nums = [0,1,2,10,16,19,31,35,36,38,40,42,43,55];
    let found = interpolation_search(&nums, target);
    println!("nums contains {target}: {found}");
    // nums contains 27: false
}
```

Upon careful analysis of the code, we can see that the only difference between interpolation search and binary search is the calculation method of the interpolant. In all other aspects, the two algorithms are almost identical. When the data is evenly distributed, the time complexity of interpolation search is O(loglog(n)). The proof of this result is complex and can be found in this paper [11]. However, the worst-case and average-case complexity of interpolation search are both O(n).

### 6.4.4 The Exponential Search

Exponential search is a variant of binary search that utilizes the exponential function to estimate the midpoint, making it suitable for sorted data without bounds. The algorithm continuously compares the value at positions of 20, 21, 22, 2k to the target value, then determines the search range, and finally performs binary search within that range. The time complexity of exponential search is O(log(i)), where i is the position of the target value. For instance, to find the value 22 in the sorted set of 15 elements [2,3,4,6,7,8,10,13,15,19,20,22,23,24,28], exponential search first checks whether the value at position 20 = 1 is greater than 22. It then continues

to check the values at positions 21, 22, and 23, which are 4, 7, and 15, all of which are less than 22. Checking position 24 = 16 is beyond the range, so the upper bound is the last index, 14.

```rust
// exponential_search.rs

fn exponential_search(nums: &[i32], target: i32) -> bool {
    let size = nums.len();
    if size == 0 { return false; }

    // find the upper bound
    let mut high = 1usize;
    while high < size && nums[high] < target {
        high <<= 1;
    }
    // use the half of the upper bound as the lower bound
    let low = high >> 1;

    // use binary_search method implemented previously
    binary_search(&nums[low..size.min(high+1)], target)
}

fn main() {
    let nums = [1,9,10,15,16,17,19,23,27,28,29,30,32,35];
    let target = 27;
    let found = exponential_search(&nums, target);
    println!("nums contains {target}: {found}");
    // nums contains 27: true
}
```

Note that in the implementation of the exponential search algorithm, the lower bound at line 13 is half of the high but can also be set to 0. However, setting it to 0 may reduce efficiency. The complexity of exponential search is divided into two parts: finding the upper bound for dividing the search range, and performing binary search. The complexity of finding the upper bound is related to the target value i, and its complexity is O(log(i)). The complexity of binary search is O(log(n)), where n is the length of the search range. The length of the search range is high −low = 2log(i) −2log(i)−1 = 2log(i)−1, and its complexity is O(log(2log(i)−1)) = O(log(i)). Therefore, the total complexity is O(log(i) + log(i)) = O(log(i)).
