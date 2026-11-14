# Searching

## 6.1 Objectives

- Be able to implement sequential search and binary search algorithms.
- Understand the concept of using hash tables as a search technique.
- Use Vec to implement a HashMap data structure.

## 6.2 What is Searching?

In this chapter, we will use the data structures we have previously implemented (stacks, queues, and linked lists) to solve practical search and sort problems. Search and sort are fundamental tasks in computer science, and many software applications and algorithms are developed around them. You are likely familiar with the search function in various software applications you have used, such as finding specific characters in a Word document or using the search bar in Goolge browser to find information. Search and lookup mean the same thing, and this book does not distinguish between the two. Searching is the process of finding a specific item within a set of items. Search algorithms typically return either true or false to indicate whether the item exists in the set, and sometimes they also return the position of the item. In Rust, we can use the contains() function to query whether an item is in a set. This function checks whether the data contains a certain value and performs a search for us.

```rust
fn main() {
    let data = vec![1,2,3,4,5];
    if data.contains(&3) {
        println!("Yes");
    } else {
        println!("No");
    }
}
```

While contains() is a simple search algorithm, there are many different search methods available, including sequential search, binary search, and hash search. We will explore how these different algorithms work and what their complexities are.

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

## 6.5 The Hash Search

The search algorithms we have discussed so far use the positional information of items in a collection to perform searches. Binary search can find data items in logarithmic time by sorting the collection. However, if an algorithm has prior knowledge of the stored addresses of different items, it can retrieve them directly without comparing them one by one. This method is called Hash Search, a search algorithm with a complexity of O(1), making it the fastest search algorithm available. To implement Hash Search, the item’s address must exist first. A data structure that provides an efficient way to store and retrieve items’ addresses is needed. This data structure is known as a hash table, which stores data items in such a way that they are easy to locate, with each item’s position referred to as a slot or address. These slots are named starting from 0, or any other value. Once the first slot is chosen, all subsequent slots are incremented accordingly. Initially, the hash table contains no items, and each slot is empty. A hash table can be implemented using Vec, with each element initialized to None. The figure below shows a hash table with size m = 11, meaning that there are m slots named 0 to 10.

![Figure 6.4: Hash table](images/fig-6.4.png)

*Figure 6.4: Hash table*

The mapping between data items and their corresponding slots in the hash table is accomplished through a hash function. The hash function takes any item in the collection and returns a specific slot name, a process known as hashing. For example, if there are integer items [24, 61, 84, 41, 56, 31], and a hash table with a capacity of 11 slots, each item’s location in the hash table can be obtained by inputting it into the hash function. A simple hash function involves using modulo, since any number modulo 11 will have a remainder within 11, ensuring that there is always a slot available to store the data. hash(item) = item%11

(6.6)

Here is the result after modulo hash calculation.

![Figure 6.5: Modulo hash](images/fig-6.5.png)

*Figure 6.5: Modulo hash*

Calculated the hash value, the item can be inserted into the corresponding slot in the hash table, as depicted in the figure above. Currently, 6 of the 11 slots in the table are occupied, resulting in a load factor of λ = 6/11. The load factor is a useful metric to evaluate the hash table, particularly when it needs to store a large number of items. A high load factor indicates that there is limited space for additional items, necessitating resizing the table. In languages like Rust and Go, resizing occurs automatically when the load factor exceeds a particular threshold, preparing for future data insertion. Although the data stored in the hash table is unsorted, the hash function enables the calculation of the slot of a data item regardless of its disorderliness. For instance, to check if the number 56 exists in the table, its hash value can be computed (hash(56) = 1), and slot 1 can be examined to locate 56, indicating its presence in the table. The search operation has a complexity of O(1), making hash search very efficient. However, conflicts may occur and must be resolved, or else the hash table cannot be utilized. For example, if 97 is added, and its hash value (hash(97) = 9) corresponds to an occupied slot (9) that contains 31 instead of 97, a collision occurs that necessitates resolution.

### 6.5.1 Hash Functions

In the previous section, the hash function computed the remainder of the item directly, ensuring that the remainder falls within a specific range. Any algorithm that can produce a value within a particular range based on the item can be used as a hash function. By improving the hash function, we can minimize the probability of collisions and create an effective hash table. One such approach to improving the hash function is the ”sum of groups” method, which divides items into equal-sized blocks (the last block may be different), adds them up, and then computes the remainder. For instance, if the data item is the phone number ”316-545-0134,” it can be split into twodigit numbers, padded with zeroes if required, resulting in [31, 65, 45, 01, 34]. The sum is 176, and taking the remainder of 11 yields a hash value (slot) of 0. The phone number may also be split into three-digit numbers or reversed before computing the remainder. Many hash functions are available, as any value that can be computed and then have its remainder taken can be used in various ways.

Another hash algorithm is the ”mid-square” method. The item is squared first, and then the middle portion of the square is extracted as the value for which the remainder is computed. For example, if the number is 36, its square is 1296, and taking the middle portion, 29, and then computing the remainder of 11 yields hash(29) = 7, indicating that 36 should be stored in slot 7. When storing a string, the remainder can also be calculated based on the ASCII values of its characters. The string ”rust” has four characters with ASCII values of [114, 117, 115, 116], and their sum is 462. Computing the remainder results in hash(462) = 0. Other strings, such as ”Java” with ASCII values [74, 97, 118, 97], may also be tried. Its sum is 386, and taking the remainder gives hash(386) = 1, indicating that ”Java” should be stored in slot 1, as shown in the figure below.

7 9 0 3 5 6 8 10 1 2 4 go css rust Java None None None None C# C++ html

The following is an implementation of hash function for ASCII value.

```rust
// hash.rs

fn hash1(astr: &str, size: usize) -> usize {
    let mut sum = 0;
    for c in astr.chars() {
        sum += c as usize;
    }

    sum % size
}

fn main() {
    let s1 = "rust"; let s2 = "Rust";
    let size = 11;

    let p1 = hash1(s1, size);
    let p2 = hash1(s2, size);
    println!("{s1} in slot {p1}, {s2} in slot {p2}");
    // rust in slot 0, Rust in slot 1
}
```

To mitigate collisions that may arise when using the above hash function, one can modify it slightly. For example, one can use the position of different characters in a string as weights and multiply the ASCII values by their positional weights. hash(rust) = (0 ∗114 + 1 ∗117 + 2 ∗115 + 3 ∗116)%11

= 695%11 (6.7) = 2

Starting the index from 1 is preferred to ensure that the first character contributes to the total. Below is an example calculation and code snippet. hash(rust) = (1 ∗114 + 2 ∗117 + 3 ∗115 + 4 ∗116)%11

= 1157%11 (6.8) = 2

```rust
// hash.rs
fn hash2(astr: &str, size: usize) -> usize {
    let mut sum = 0;
    for (i, c) in astr.chars().enumerate() {
        sum += (i + 1) * (c as usize);
    }
    sum % size
}

fn main() {
    let (s1, s2, size) = ("rust", "Rust", 11);
    let p1 = hash2(s1, size);
    let p2 = hash2(s2, size);
    // rust in slot 2, Rust in slot 3
}
```

Efficiency is crucial when designing a hash function to ensure that it does not become the bottleneck of the system. If the hash function is too complex, it could break the O(1) complexity.

### 6.5.2 Collison Resolution

To address the issue of hash collisions, collision resolution methods are necessary. For instance, if a hash function with position as weight is used and the index starts from 0, the strings ”rust” and ”Rust” will collide. When two items are hashed to the same slot, a method must be used to insert the conflicting item into another slot of the hash table. This process is called collision resolution. Although perfect hash tables do not exist due to limited memory and complex real-world situations, one intuitive method for resolving collisions is to search the hash table and attempt to find the next empty slot to save the conflicting item. The simplest method is called open addressing, specifically linear probing. Linear probing attempts to linearly probe the next empty slot in the hash table, starting from the original collision point until the first empty slot is found. Note that you can start searching again from the beginning after reaching the end. The following figure shows a hash table with 11 slots, where we try to insert 35 and 47.

0 3 5 6 7 8 9 10 1 2 4 None 56 None None None 61 84 31 None 24 41

When inserting 35, its position should be slot 2, but we find that slot 2 already contains 24. Therefore, we start searching for an empty slot from slot 2 and find that slot 3 is empty, so we insert 35 there.

0 3 5 6 7 8 9 10 1 2 4 None None None None 56 24 35 61 84 41 31

When we insert 47, we find that slot 3 has the value 35, so we search for the next empty slot and find that slot 4 is empty, so we insert 47 there.

7 9 0 3 5 6 8 10 1 2 4 None None None 56 24 35 47 61 84 41 31

To search for items in a hash table built using open addressing, we must use the same method as used during its construction. For instance, if we are searching for item 56 with a hash of 1, we locate it in slot 56 and return true. However, if we are looking for item 35, which has a hash of 2, we may find another item like 24 instead of 35 due to collisions. To avoid returning false, we need to conduct a sequential search until we locate 35, an empty slot, or we loop back to 24 before returning the result. However, using a sequential search may lead to data clustering, where items cluster in the table due to multiple collisions occurring in the same hash slot. Linear probing fills subsequent slots with conflicting items, forcing the originally intended values to be inserted elsewhere. Sequential searches are time-consuming, with a complexity greater than O(1). To address data clustering, open addressing technology can be extended to skip several slots instead of sequentially searching for the next open slot. By checking every three slots when a conflict occurs, for example, the conflicting items are more evenly distributed, thus dispersing the conflict. This method has a significant effect and can alleviate data clustering, as shown in the figure below.

0 3 5 6 7 8 9 10 1 2 4 None 47 None None 56 24 35 61 84 41 31

When adding item 35, a conflict may occur, prompting the search to skip every three slots from that point onwards, thus dispersing the conflict. Consequently, item 47 can be inserted without any conflict. This method has proven effective in alleviating data clustering, as demonstrated in the following figure. Rehashing is the process of finding an alternative slot in a hash table after a collision occurs. This process involves calculating a new hash value using a specified skip size, which must ensure that all slots in the table can eventually be accessed. To guarantee this, it is advisable to use a prime number as the table size, as exemplified by the use of 11 in the accompanying example. rehash(pos) = (pos + n)%size

(6.9)

Another approach to resolving conflicts is the chain method. This method involves setting up a linked list to store data items for each conflicting position, as shown in Figure (6.6). When searching, conflicts are resolved by sequentially searching the chain, which has a complexity of O(n). If the data in the conflict chain is sorted, a binary search can be utilized to achieve a complexity of O(log2(n)). If the chain becomes too long, it can be transformed into a red-black tree to enhance its structural stability. In many programming languages, the chain method is the default implementation for resolving conflicts in hash table data structures.

![Figure 6.6: Collison Resolution by Chain Method](images/fig-6.6.png)

*Figure 6.6: Collison Resolution by Chain Method*

### 6.5.3 Implementing a HashMap in Rust

The most commonly used collection type in Rust is the HashMap. It is an associative data type that stores key-value pairs. The key is utilized to locate the position of the value, and due to the position uncertainty, this type of search is akin to searching on a map. Thus, this data structure is called HashMap. HashMap is an unordered collection of key-value pairs where the keys are unique, and there is a one-to-one relationship between the keys and the values. Here is the abstract data type definition of HashMap:

- new(): creates a new HashMap, takes no arguments and returns an empty HashMap collection.
- insert(k,v): adds a new key-value pair to the HashMap, taking parameters k and v. If the key exists, the old value is replaced with the new value. No return value is provided.
- remove(k): removes value corresponding to k from the HashMap, takes parameter k, and returns the corresponding value v.
- get(k): returns the value v stored in the HashMap for the given key k (which may be empty None), takes parameter k.
- contains(k): returns true if the key k exists in the HashMap, otherwise false, takes parameter k.
- len(): returns the number of key-value pairs stored in the HashMap, takes no arguments.

The table below displays the results of operations assuming that ’h’ is an already created empty HashMap (represented as {} here).

**Table 6.2: HashMap operations**

| Operation | Value | Return |
| --- | --- | --- |
| h.is_empty() | {} | true |
| h.insert(”a”, 1) | {a:1} |  |
| h.insert(”b”, 2) | {a:1, b:2} |  |
| h.insert(”c”, 3) | {a:1, b:2, c:3} |  |
| h.get(”b”) | {a:1, b:2, c:3} | Some(2) |
| h.get(”d”) | {a:1, b:2, c:3} | None |
| h.len() | {a:1, b:2, c:3} | 3 |
| h.contains(”c”) | {a:1, b:2, c:3} | true |
| h.contains(”e”) | {a:1, b:2, c:3} | false |
| h.remove(”a”) | {b:2, c:3} | Some(1) |
| h.remove(”a”) | {b:2, c:3} | None |
| h.insert(”a”, 1) | {b:2, c:3, a:1} |  |
| h.contains(”a”) | {b:2, c:3, a:1} | true |
| h.len() | {b:2, b:3, a:1} | 3 |
| h.get(”a”) | {b:2, c:3, a:1} | Some(1) |
| h.remove(”c”) | {b:2, a:1} | Some(3) |

In actual implementation, a HashMap in Rust is made up of two separate Vecs - one for storing the keys (called slot) and the other for storing the values (called data). The slot Vec saves the keys with the index starting from 1, while the default value in the slot Vec is 0. The HashMap is encapsulated by a struct, and a cap parameter is added to control the capacity.

```rust
// hashmap.rs

#[derive(Debug, Clone, PartialEq)]
struct HashMap <T> {
    cap: usize, // capacity
    slot: Vec<usize>, // store data address (index)
    data: Vec<T>, // store elements
}
```

The rehash function in Rust can be implemented using a linear search method that adds 1, which is simple and easy to implement. The initial size of the HashMap is set to 11, but it can also be set to other prime numbers, such as 13, 17, 19, 23, 29, etc. Below is the complete implementation code for a HashMap in Rust.

```rust
// hashmap.rs

impl<T: Clone + PartialEq + Default> HashMap<T> {
    fn new(cap: usize) -> Self {
        // Initialize slot and data
        let mut slot = Vec::with_capacity(cap);
        let mut data = Vec::with_capacity(cap);
        for _i in 0..cap{
            slot.push(0);
            data.push(Default::default());
        }

        HashMap { cap, slot, data }
    }

    fn len(&self) -> usize {
        let mut len = 0;
        for &d in self.slot.iter() {
            // If slot is not empty, then increase len by 1
            if 0 != d {
                len += 1;
            }
        }
        len
    }

    fn is_empty(&self) -> bool {
        let mut empty = true;
        for &d in self.slot.iter() {
            if 0 != d {
                empty = false;
                break;
            }
        }
        empty
    }

    fn clear(&mut self) {
        let mut slot = Vec::with_capacity(self.cap);
        let mut data = Vec::with_capacity(self.cap);
        for _i in 0..self.cap{
            slot.push(0);
            data.push(Default::default());
        }

        self.slot = slot;
        self.data = data;
```

```rust
    }

    fn hash(&self, key: usize) -> usize {
        key % self.cap
    }

    fn rehash(&self, pos: usize) -> usize {
        (pos + 1) % self.cap
    }

    fn insert(&mut self, key: usize, value: T) {
        if 0 == key { panic!("Error: key must > 0"); }

        let pos = self.hash(key);
        if 0 == self.slot[pos] {
            // If the slot is empty, insert directly
            self.slot[pos] = key;
            self.data[pos] = value;
        } else {
            // If the slot is not empty, then
            // find next available position
            let mut next = self.rehash(pos);
            while 0 != self.slot[next]
                && key != self.slot[next] {
                next = self.rehash(next);

                // If the slot is full, exit
                if next == pos {
                    println!("Error: slot is full!");
                    return;
                }
            }

            // Insert the data in the found slot
            if 0 == self.slot[next] {
                self.slot[next] = key;
                self.data[next] = value;
            } else {
                self.data[next] = value;
            }
        }
    }

    fn remove(&mut self, key: usize) -> Option<T> {
        if 0 == key { panic!("Error: key must > 0"); }

        let pos = self.hash(key);
        if 0 == self.slot[pos] {
            // If the slot is empty, return None
            None
        } else if key == self.slot[pos] {
            // If found the same key,
```

```rust
            // update the slot and data
            self.slot[pos] = 0;
            let data = Some(self.data[pos].clone());
            self.data[pos] = Default::default();
            data
        } else {
            let mut data: Option<T> = None;
            let mut stop = false;
            let mut found = false;
            let mut curr = pos;

            while 0 != self.slot[curr] && !found && !stop {
                if key == self.slot[curr] {
                    // If the value is found, delete the data
                    found = true;
                    self.slot[curr] = 0;
                    data = Some(self.data[curr].clone());
                    self.data[curr] = Default::default();
                } else {
                    // If rehashing returns to the initial
                    // position, it means that it has searched
                    // a full circle and still not found
                    curr = self.rehash(curr);
                    if curr == pos {
                        stop = true;
                    }
                }
            }

            data
        }
    }

    fn get_pos(&self, key: usize) -> usize {
        if 0 == key { panic!("Error: key must > 0"); }

        // Calculate the data position
        let pos = self.hash(key);
        let mut stop = false;
        let mut found = false;
        let mut curr = pos;

        // Loop through to find the data
        while 0 != self.slot[curr] && !found && !stop {
            if key == self.slot[curr] {
                found = true;
            } else {
                // If rehashing returns to the initial position
                // it means that it has searched a full circle
                // and still not found
                curr = self.rehash(curr);
                if curr == pos {
```

```rust
                    stop = true;
                }
            }
        }

        curr
    }

    // Get a reference and a mutable reference to val
    fn get(&self, key: usize) -> Option<&T> {
        let curr = self.get_pos(key);
        self.data.get(curr)
    }

    fn get_mut(&mut self, key: usize) -> Option<&mut T> {
        let curr = self.get_pos(key);
        self.data.get_mut(curr)
    }

    fn contains(&self, key: usize) -> bool {
        if 0 == key {
            panic!("Error: key must > 0");
        }
        self.slot.contains(&key)
    }

    // Implement iteration and mutable iteration for hashmap
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

// Implementation of iteration
struct Iter<'a, T: 'a> { stack: Vec<&'a T>, }
impl<'a, T> Iterator for Iter<'a, T> {
    type Item = &'a T;
    fn next(&mut self) -> Option<Self::Item> {
        self.stack.pop()
    }
}
```

```rust
struct IterMut<'a, T: 'a> { stack: Vec<&'a mut T>, }
impl<'a, T> Iterator for IterMut<'a, T> {
    type Item = &'a mut T;
    fn next(&mut self) -> Option<Self::Item> {
        self.stack.pop()
    }
}

fn main() {
    basic();
    iter();

    fn basic() {
        let mut hmap = HashMap::new(11);
        hmap.insert(2,"dog");
        hmap.insert(3,"tiger");
        hmap.insert(10,"cat");

        println!("empty: {}, size: {:?}",
                    hmap.is_empty(), hmap.len());
        println!("contains key 2: {}", hmap.contains(2));

        println!("key 3: {:?}", hmap.get(3));
        let val_ptr = hmap.get_mut(3).unwrap();
        *val_ptr = "fish";
        println!("key 3: {:?}", hmap.get(3));
        println!("remove key 3: {:?}", hmap.remove(3));
        println!("remove key 3: {:?}", hmap.remove(3));

        hmap.clear();
        println!("empty: {}, size: {:?}",
                    hmap.is_empty(), hmap.len());
    }

    fn iter() {
        let mut hmap = HashMap::new(11);
        hmap.insert(2,"dog");
        hmap.insert(3,"tiger");
        hmap.insert(10,"cat");

        for item in hmap.iter() {
            println!("val: {item}");
        }

        for item in hmap.iter_mut() {
            *item = "fish";
        }

        for item in hmap.iter() {
            println!("val: {item}");
        }
```

```text
    }
}
```

Here is the code execution output.

```text
empty: false, size: 3
contains key 2: true
key 3: Some("tiger")
key 3: Some("fish")
remove key 3: Some("fish")
remove key 3: None
empty: true, size: 0
val: cat
val:
val:
val:
val:
val:
val:
val: tiger
val: dog
val:
val:
val: fish
val: fish
val: fish
val: fish
val: fish
val: fish
val: fish
val: fish
val: fish
val: fish
val: fish
```

### 6.5.4 Analysis of HashMap

A hash table provides a lookup complexity of O(1) in the best case. However, due to collisions, the number of comparisons during the lookup process can vary. The severity of collisions affects the performance of the hash table, and a good evaluation metric is the load factor λ. A small load factor means the chance of collisions is low, and items are more likely to be in their corresponding slot. A large load factor means the table is filling up quickly, and there are more collisions, leading to a more complex conflict resolution process. The result of each search is either success or failure. For searches performed using linear probing

1 1+ 1−λ

open addressing, the average number of comparisons for success is about

, and for failure, it is 2 1−λ )2 1 1+( . Even when using chaining, the average number of comparisons for success is 1 + λ/2,

about

2

and for failure, it is λ. Overall, the lookup complexity of a hash table is around O(λ). When using the chaining method in a hash table, an increase in collisions results in more items being added to the same chain. As a result, searching for a specific item in the chain takes longer, making it the main contributor to the search time.

## 6.6 Summary

This chapter covers several search algorithms, namely sequential search, binary search, interpolation search, exponential search and hash search. Sequential search is a straightforward algorithm that has a complexity of O(n). Binary search, on the other hand, is a fast algorithm that cuts the data set in half each time, but it requires the data to be sorted, with a complexity of O(log2(n)). Other search algorithms, such as interpolation search and exponential search, build on binary search and are suitable for different types of data distribution. Hash search is a highly efficient O(1) search algorithm that uses a HashMap. However, it is crucial to consider that hash tables are prone to collisions and need appropriate measures, such as open addressing and chaining, to resolve them. Sorting is a helpful technique that speeds up search algorithms, and in the next chapter, we will delve into sorting algorithms.
