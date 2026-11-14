## 6.3 The Sequential Search

When data items are stored in collections such as Vec, arrays, or slices, they have a linear relationship since each item is stored at a position relative to the other items. This means that the index values of the

data items in slices are ordered, and can be accessed in order, making these data structures linear as well. Similarly, the stacks, queues, and linked lists that we have previously studied are also linear. Based on this same linear logic inherent in the physical world, a natural search technique is linear search, which is also known as sequential search. Linear search works by starting at the first item in the slice and moving from one item to another in order until the target item is found or the entire slice is traversed. If the item being searched for is not found after traversing the entire slice, it means that the item does not exist. The following figure illustrates how this search works.

![Figure 6.1: Sequential search](images/fig-6.1.png)

*Figure 6.1: Sequential search*

### 6.3.1 Implementing an Sequential Search in Rust

The following Rust code implements sequential search, and it is straightforward to understand. The program takes a slice of integers and a target integer as input. It iterates through each element in the slice and compares it with the target value. If the value is found, the function returns a boolean value: true. Otherwise, it returns false.

```rust
// sequential_search.rs

fn sequential_search(nums: &[i32], num: i32) -> bool {
    let mut pos = 0;
    let mut found = false;

    // Continue looping if pos is within the index range and
    // the item has not been found.
    while pos < nums.len() && !found {
        if num == nums[pos] {
            found = true;
        } else {
            pos += 1;
        }
    }

    found
}
```

Here is an example of sequential search execution.

```rust
fn main() {
    let num = 8;
    let nums = [9,3,7,4,1,6,2,8,5];
    let found = sequential_search(&nums, num);
    println!("nums contains {num}: {found}");
    // nums contains 8: true
}
```

Of course, sequencial search can also return the specific position of the search item, or return None if it is not found.

```rust
// sequential_search_pos.rs

fn sequential_search_pos(nums:&[i32],num:i32) -> Option<usize>{
    let mut pos: usize = 0;
    let mut found = false;
    while pos < nums.len() && !found {
        if num == nums[pos] {
            found = true;
        } else {
            pos += 1;
        }
    }

    if found { Some(pos) } else { None }
}

fn main() {
    let num = 8;
    let nums = [9,3,7,4,1,6,2,8,5];
    match sequential_search_pos(&nums, num) {
        Some(pos) => println!("{num}'s index: {pos}"),
        None => println!("nums does not contain {num}"),
    }
    // 8's index: 7
}
```

### 6.3.2 Analysis of Sequential Search

To analyze the complexity of the sequential search algorithm, we need to set a basic computational unit. Since comparison operation is the primary operation in searching, counting the number of comparisons is the most important. Data items in a set are randomly placed and unordered, and the probability of a data item being at any position in the set is the same according to probability theory. If the target item is not in the set, the only way to know this result is to compare the target with all the data items in the set. If there are n items, then the sequential search requires n comparisons, and the complexity is O(n). What if the target item is in the set? Is the complexity still O(n)? When searching for a target item in a set, the analysis of the algorithm’s complexity is not always straightforward. There are three possibilities: the best case scenario is when the target item is at the beginning of the set, and only one comparison is needed, resulting in a complexity of O(1). In the worst case scenario, the target item is at the end of the set, and it takes n comparisons to find it, resulting in a complexity of O(n). Finally, the target item may be distributed throughout the set, and there are n-2 possible complexities, ranging from O(2) to O(n −1). In this scenario, the number of possible comparisons ranges from 1 to n times, and the average complexity equals the sum of all possible complexities divided by the total number of comparisons.

n ∑

O(i)/n = O(n/2) = O(n)

(6.1) i=1

When the set becomes large, the complexity of sequential search on a random sequence is O(n), as 1/2 can be ignored. However, if the data items are ordered in ascending order and the probability of the

target item existing in any of the n positions is still the same, the search performance can be improved. If the target item does not exist, the search can be accelerated through techniques like binary search. For example, if searching for the target item 50, the comparison is performed in order until 56. At this point, it can be determined that there is no target value of 50 behind it because the items behind 56 are larger than 56, and the algorithm stops searching.

![Figure 6.2: Sequential search on ordered data](images/fig-6.2.png)

*Figure 6.2: Sequential search on ordered data*

The sequential search algorithm used on sorted data sets is shown below. It optimizes the algorithm by setting the ”stop” variable to control the search and stop immediately when it goes beyond the range for saving time.

```rust
// ordered_sequential_search.rs

fn ordered_sequential_search(nums:&[i32], num:i32) -> bool {
    let mut pos = 0;
    let mut found = false;
    // return when reads on ordered data
    let mut stop = false;

    while pos < nums.len() && !found && !stop {
        if num == nums[pos] {
            found = true;
        } else if num < nums[pos] {
            // ordered data, return
            stop = true;
        } else {
            pos += 1;
        }
    }

    found
}

fn main() {
    let nums = [1,3,8,10,15,32,44,48,50,55,60,62,64];
    let num = 44;
    let found = ordered_sequential_search(&nums, num);
    println!("nums contains {num}: {found}");
    // nums contains 44: true

    let num = 49;
    let found = ordered_sequential_search(&nums, num);
    println!("nums contains {num}: {found}");
    // nums contains 49: false
}
```

In the case of sorted data, if the target item is not in the set and is less than the first item, only one comparison is needed to determine that the item is not in the set. In the worst case, the algorithm would need to compare the target item with all n items in the set, resulting in n comparisons. The average number of comparisons is still n/2, and the complexity remains at O(n). However, the O(n) complexity is better than the search on unordered data because most searches follow the average case. In fact, the average case complexity for sorted data sets can be twice as fast as unordered ones. Thus, sorting has always been a crucial topic in computer science. The complexity of sequential search for unordered and ordered data sets is summarized in the table below.

**Table 6.1: Complexity of Sequential Search**

| Case | Min | Avg | Max | Search Class |  |
| --- | --- | --- | --- | --- | --- |
| target exist | O(1) | O( n | 2 ) | O(n) | unorderd search |
| target not exist | O(n) | O(n) | O(n) | unorderd search |  |
| target exist | O(1) | O( n | 2 ) | O(n) | ordered search |
| target not exist | O(1) | O( n | 2 ) | O(n) | ordered search |
