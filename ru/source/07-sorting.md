# Sorting

## 7.1 Objectives

- Learn sorting algorithms.
- Be able to implement the ten basic sorting algorithms in Rust.

## 7.2 What is Sorting?

Sorting involves arranging elements in a specific order in a collection. For example, playing cards are shuffled and arranged by suit or order to play effectively, and words can be sorted alphabetically or by length. Similarly, Chinese cities can be sorted by population, ethnicity, or region. Orderliness is a crucial skill for humans as it enables smooth progress in various areas. Sorting is an important field in computer science, and many pioneers have contributed to the development of sorting algorithms. Various algorithms, including sequential search and binary search, benefit from sorting datasets. Sorting algorithm efficiency is dependent on the number of items being processed, and complex sorting methods are too expensive for small collections while simple algorithms are not suitable for large datasets. In this chapter, we will explore different sorting algorithms and compare their performance. Comparison is the core operation in sorting, as it determines sequence, order, and orderliness. Comparison involves looking at which element is larger or smaller based on a criterion, which can be simple (numerical size) or abstract (health index). If the comparison shows that the order is incorrect, data positions need to be exchanged. However, exchanging data positions is an expensive operation in computer science, and the total number of exchanges is crucial for evaluating the efficiency of algorithms. In this chapter, we will analyze various sorting algorithms using the Big O analysis method, which is the most intuitive indicator for evaluating their efficiency. Apart from efficiency, sorting also has the issue of stability. For instance, in a list like [1,4,9,8,5,5,2,3,7,6], there are two 5s, and different sorts may swap the order of the two 5s. Although they are adjacent in the end, the original order relationship has been destroyed. For numeric data, this may not matter, but for data structures containing keys like personal information, rash sorting may change the order, which is not desirable.

```text
person {
                   person {
    amount: 5,
                       amount: 5,
    name: Shieber,
                       name: Kew,
    phone: 133xx,
                       phone: 133xx,
    age: 20,
                       age: 24,
}
                   }
```

To ensure that the order of the elements in a sorted collection remains stable, it is important to consider stability when evaluating sorting algorithms. Stability refers to whether the relative order of equal elements in the original collection is maintained in the sorted collection. For example, if the amount: 5 appears twice in a collection and sorting changes the order of the two occurrences, this can cause issues for algorithms that rely on the stability of the sequence, such as deduction operations. There are numerous sorting algorithms available for collections, but there are ten basic types of sorting algorithms that serve as the foundation for most of them. These include bubble sort, quick sort, selection sort, heap sort, insertion sort, shell sort, merge sort, counting sort, bucket sort, and radix sort. Many improved algorithms have been derived from these ten basic algorithms. In this article, we will explain several of these improved algorithms, including new bubble sort, cocktail sort, comb sort, binary insertion sort, flash sort, and Tim sort.

## 7.3 The Bubble Sort

Bubble sort is a simple sorting algorithm that requires multiple iterations through the collection, comparing adjacent items and swapping those that are unordered. Each iteration places the largest value in its correct position. The algorithm gets its name from the similarity of the sorting process to bubbles rising to the top of a pot of boiling water. In the first pass, the algorithm compares adjacent items and swaps them if they are in the wrong order. If there are n items in the list, there will be n-1 comparisons in the first pass. In the second pass, the largest value in the data set is already in the correct position, and the remaining n-1 items need to be sorted, which means there will be n-2 comparisons. The algorithm requires n-1 iterations to place the next largest value in its proper position. After completing n-1 rounds of iteration and comparison, the smallest item will definitely be in the correct position, and no further processing is needed.

![Figure 7.1: Bubble sort](images/fig-7.1.png)

*Figure 7.1: Bubble sort*

The diagonal line in the figure above represents the maximum value, and it keeps moving towards the right, just like bubbles rising to the top. Bubble sort involves frequent swap operations, which are com-

monly used auxiliary operations in comparisons. In Rust, the Vec data structure defaults to implementing the swap() function, but you can also implement the following swap operation.

```rust
// swap
let temp = data[i];
data[i] = data[j];
data[j] = temp;
```

Some programming languages provide a convenient way to swap values without using temporary variables, such as: data[i], data[j] = data[j], data[i]. Although this feature still uses variables internally, it operates on two variables simultaneously, as shown in the figure below.

47 84

In this chapter, we only deal with sets of numbers to simplify the algorithm design. Therefore, we can use a Vec to implement bubble sort.

```rust
// bubble_sort.rs

fn bubble_sort1(nums: &mut [i32]) {
    if nums.len() < 2 {
        return;
    }

    for i in 1..nums.len() {
        for j in 0..nums.len()-i {
            if nums[j] > nums[j+1] {
                nums.swap(j, j+1);
            }
        }
    }
}
```

Here is an example of bubble sort.

```rust
fn main() {
    let mut nums = [54,26,93,17,77,31,44,55,20];
    bubble_sort1(&mut nums);
    println!("sorted nums: {:?}", nums);
    // sorted nums: [17, 20, 26, 31, 44, 54, 55, 77, 93]
}
```

It is worth noting that to avoid a double for-loop, we can also use a while-loop to implement bubble sort.

```rust
// bubble_sort.rs

fn bubble_sort2(nums: &mut [i32]) {
    let mut len = nums.len() - 1;

    while len > 0 {
        for i in 0..len {
```

```rust
            if nums[i] > nums[i+1] {
                nums.swap(i, i+1);
            }
        }

        len -= 1;
    }
}

fn main() {
    let mut nums = [54,26,93,17,77,31,44,55,20];
    bubble_sort2(&mut nums);
    println!("sorted nums: {:?}", nums);
    // sorted nums: [17, 20, 26, 31, 44, 54, 55, 77, 93]
}
```

Bubble sort involves comparing adjacent items and swapping those that are unordered, which repeats until the largest item is in its correct position. The algorithm performs n - 1 rounds of traversal to sort n numbers, regardless of the initial arrangement. During the first round, n - 1 comparisons are required, followed by n - 2 comparisons in the second round, and so on, until only one comparison is needed. The total number of comparisons can be calculated using the formula: 1 + 2 + ..., +n −1 = n2

2 + n (7.1) 2

This means that the time complexity of bubble sort is O( n2

2 + n 2 ) = O(n2).

Although both bubble sort algorithms presented above achieve sorting, even a sorted set requires continuous comparisons and swapping of data items. To optimize the algorithm, we can add a variable to control whether comparisons should continue and exit directly when encountering a sorted set.

```rust
// bubble_sort.rs

fn bubble_sort3(nums: &mut [i32]) {
    // compare controls whether to continue comparing
    let mut compare = true;
    let mut len = nums.len() - 1;

    while len > 0 && compare {
        compare = false;
        for i in 0..len {
            if nums[i] > nums[i+1] {
                // Data is unordered and need to compare
                nums.swap(i, i+1);
                compare = true;
            }
        }

        len -= 1;
    }
}

fn main() {
    let mut nums = [54,26,93,17,77,31,44,55,20];
```

```rust
    bubble_sort3(&mut nums);
    println!("sorted nums: {:?}", nums);
    // sorted nums: [17, 20, 26, 31, 44, 54, 55, 77, 93]
}
```

Bubble sort is a sorting algorithm that compares adjacent elements in an array, starting from the first number and exchanging positions based on their relative size. Elements are only swapped from left to right. However, can we perform bubble sort from right to left? Yes, we can, and this bidirectional sorting method is called cocktail sort. Cocktail sort is a variant of bubble sort that sorts in descending order when sorting from right to left. While it slightly optimizes bubble sort, its time complexity is still O(n2), but it approaches O(n) if the sequence is already sorted.

```rust
// cocktail_sort.rs

fn cocktail_sort(nums: &mut [i32]) {
    if nums.len() <= 1 { return; }

    // bubble controls the sort process
    let mut bubble = true;
    let len = nums.len();
    for i in 0..(len >> 1) {
        if bubble {
            bubble = false;
            // bubble from left to right
            for j in i..(len - i - 1) {
                if nums[j] > nums[j+1] {
                    nums.swap(j, j+1);
                    bubble = true
                }
            }
            // bubble from right to left
            for j in (i+1..=(len - i - 1)).rev() {
                if nums[j] < nums[j-1] {
                    nums.swap(j-1, j);
                    bubble = true
                }
            }
        } else {
            break;
        }
    }
}

fn main() {
    let mut nums = [1,3,2,8,3,6,4,9,5,10,6,7];
    cocktail_sort(&mut nums);
    println!("sorted nums {:?}", nums);
    // sorted nums [1, 2, 3, 3, 4, 5, 6, 6, 7, 8, 9, 10]
}
```

In contrast to bubble sort, comb sort can compare items with a distance greater than 1. Comb sort starts by setting the gap to the length of the array and decreasing it by a fixed ratio in each iteration of the loop, typically by multiplying it by 0.8, which is the most effective ratio determined by the original

author through experimentation. When the gap is 1, comb sort degenerates into bubble sort. Comb sort aims to move inverted numbers forward as much as possible and ensure that the numbers in the current gap are sorted, similar to combing hair with a comb, where the gap is similar to the gap between the teeth of the comb. Comb sort has a time complexity of O(nlogn), with a space complexity of O(1), and it is an unstable sorting algorithm.

```rust
// comb_sort.rs

fn comb_sort(nums: &mut [i32]) {
    if nums.len() <= 1 { return; }
    let mut i;
    let mut gap: usize = nums.len();

    // ordered basicly
    while gap > 0 {
        gap = (gap as f32 * 0.8) as usize;
        i = gap;
        while i < nums.len() {
            if nums[i-gap] > nums[i] {
                nums.swap(i-gap, i);
            }
            i += 1;
        }
    }

    // rearrange the element properly.
    // exchange controls the process
    let mut exchange = true;
    while exchange {
        exchange = false;
        i = 0;
        while i < nums.len() - 1 {
            if nums[i] > nums[i+1] {
                nums.swap(i, i+1);
                exchange = true;
            }
            i += 1;
        }
    }
}
fn main() {
    let mut nums = [1,2,8,3,4,9,5,6,7];
    comb_sort(&mut nums);
    println!("sorted nums {:?}", nums);
    // sorted nums [1, 2, 3, 4, 5, 6, 7, 8, 9]
}
```

Bubble sort suffers from the problem that the boundary index, such as i, j, i+1, j+1, must be arranged properly and cannot be wrong. In 2021, a new sorting algorithm [12] was published that does not require handling boundary index values. It is intuitive and resembles bubble sort at first glance, but it is actually similar to insertion sort. Although it looks like a descending sort, it is actually an ascending sort.

```rust
// CantBelieveItCanSort.rs

fn cbic_sort1(nums: &mut [i32]) {
    for i in 0..nums.len() {
        for j in 0..nums.len() {
            if nums[i] < nums[j] { nums.swap(i, j); }
        }
    }
}

fn main() {
    let mut nums = [54,32,99,18,75,31,43,56,21,22];
    cbic_sort1(&mut nums);
    println!("sorted nums {:?}", nums);
    // sorted nums [18, 21, 22, 31, 32, 43, 54, 56, 75, 99]
}
```

Of course, it can also be implemented as a descending sort by changing the less than symbol to a greater than symbol.

```rust
// CantBelieveItCanSort.rs

fn cbic_sort2(nums: &mut [i32]) {
    for i in 0..nums.len() {
        for j in 0..nums.len() {
            if nums[i] > nums[j] {
                nums.swap(i, j);
            }
        }
    }
}
fn main() {
    let mut nums = [54,32,99,18,75,31,43,56,21,22];
    cbic_sort2(&mut nums);
    println!("sorted nums {:?}", nums);
    // sorted nums [99, 75, 56, 54, 43, 32, 31, 22, 21, 18]
}
```

This algorithm uses only two for loops, and the index values do not need to be handled separately. While it resembles the definition of bubble sort, it is not actually a bubble sort algorithm.

## 7.4 The Quick Sort

Quicksort and bubble sort do have some similarities, but it is not accurate to say that quicksort is an upgraded version of bubble sort. Quicksort is a completely different algorithm that uses the divide-andconquer strategy to speed up the sorting process. The quicksort algorithm involves two main steps: selecting a pivot value and partitioning the set. The pivot value can be any value in the collection, but it is typically chosen to be a value that is close to the middle of the final sorted collection for the fastest sorting speed. There are many different methods for selecting a pivot value, but this article only explains the principle and does not consider algorithm optimization.

In the following figure, the pivot value of 84 is not necessarily at the middle of the sorted collection, and it would be more efficient to choose a value closer to the middle, such as 56, as the pivot value. However, choose a correct pivot value is not the focus of this article.

84 92 66 56 31 72 19 44 24

To implement quicksort, two markers need to be set for comparison after selecting the pivot value (the dark gray value). The left and right markers should be located at the far left and far right extremes of the collection, except for the pivot value.

84 92 66 56 31 72 19 44 24 leftmark rightmark 84 92 66 56 31 72 19 44 24 leftmark rightmark

The goal of partitioning is to move the items that are misaligned with respect to the pivot value. By comparing the values at the left and right markers with the pivot value and swapping the smaller value to the left marker and the larger value to the right marker, a basicly sorted collection can be achieved quickly through repeated swaps.

92 66 56 31 72 19 84 24 44 leftmark rightmark 92 66 56 31 72 19 84 24 44 leftmark rightmark 92 66 56 31 72 19 84 24 44 leftmark rightmark

To begin partitioning, right shift the left index until a value greater than or equal to the pivot value is found. Then left shift the decreasing right index until a value less than or equal to the pivot value is found. If the value of the left index is greater than the right index, swap the values. In this case, 84 and 24 satisfy this condition, so the values are directly swapped. Repeat this process until the left and right indices cross each other. After crossing, compare the values of the left and right indices. If the right is less than the left, swap the right index value with the pivot value. Otherwise, swap the left index value with the pivot value. The right index value serves as the splitting point, dividing the set into two intervals. Recursively call quicksort on the left and right intervals until the sorting is completed. It is important to note that the pivot value does not necessarily have to be the value in the middle of the collection but

should be a value that is in the middle or close to the middle of the final sorted collection for the fastest sorting speed.

24 19 31 44 56 66 72 92 84 leftmark rightmark <56 >56 19 31 56 66 72 92 84 24 44 leftmark rightmark leftmark rightmark

Once quicksort is executed on both the left and right sides, the sorting process is completed. If the set’s length is less than or equal to one, it’s already sorted, and the program can exit directly. To implement quicksort, we have a dedicated partition function that selects the first item(or selects a random value in the data set) as the pivot value.

```rust
// quick_sort.rs

fn quick_sort1(nums: &mut [i32], low: usize, high: usize) {
    if low < high {
        let split = partition(nums, low, high);

        // avoid out of range (split <= 1) and syntax error
        if split > 1 {
            quick_sort1(nums, low, split - 1);
        }

        quick_sort1(nums, split + 1, high);
    }
}

fn partition(nums:&mut[i32], low:usize,high:usize) -> usize {
    // left marker and right marker
    let mut lm = low;
    let mut rm = high;

    loop {
        // left mark move to right gradually
        while lm <= rm && nums[lm] <= nums[low] {
            lm += 1;
        }

        // right mark move to left gradually
        while lm <= rm && nums[rm] >= nums[low] {
            rm -= 1;
        }
```

```rust
        // once lm > rm, return and exchange data between
        // postion lm and rm
        if lm > rm {
            break;
        } else {
            nums.swap(lm, rm);
        }
    }

    nums.swap(low, rm);

    rm
}

fn main() {
    let mut nums = [54,26,93,17,77,31,44,55,20];
    let high = nums.len() - 1;
    quick_sort1(&mut nums, 0, high);
    println!("sorted nums: {:?}", nums);
    // sorted nums: [17, 20, 26, 31, 44, 54, 55, 77, 93]
}
```

However, it’s also possible to implement quicksort directly through the recursive method without using the partition function.

```rust
// quick_sort.rs

fn quick_sort2(nums: &mut [i32], low: usize, high: usize) {
    if low >= high {
        return;
    }

    // left marker and right marker
    let mut lm = low;
    let mut rm = high;
    while lm < rm {
        // right marker move to left gradually
        while lm < rm && nums[low] <= nums[rm] {
            rm -= 1;
        }

        // left marker move to right gradually
        while lm < rm && nums[lm] <= nums[low] {
            lm += 1;
        }

        // exchange data between position lm and rm
        nums.swap(lm, rm);
    }

    // exchange data between position low and lm
    nums.swap(low, lm);
```

```rust
    if lm > 1 {
        quick_sort2(nums, low, lm - 1);
    }

    quick_sort2(nums, rm + 1, high);
}

fn main() {
    let mut nums = [54,26,93,17,77,31,44,55,20];
    let high = nums.len() - 1;
    quick_sort2(&mut nums, 0, high);
    println!("sorted nums: {:?}", nums);
    // sorted nums: [17, 20, 26, 31, 44, 54, 55, 77, 93]

    let mut nums = [1000,-1,2,-20,89,64,0,99,73];
    let high = nums.len() - 1;
    quick_sort2(&mut nums, 0, high);
    println!("sorted nums: {:?}", nums);
    // sorted nums: [-20, -1, 0, 2, 64, 73, 89, 99, 1000]
}
```

To partition a set of length n in quicksort, there will be log(n) partitions if the partition is always in the middle. However, finding the splitting point requires checking the pivot value against each of the n items, resulting in a complexity of nlog(n). In the worst case, when the splitting point is far from the middle, sorting of items 1 and n - 1 will be repeated n times, leading to a complexity of O(n2). Quicksort relies on recursion, but excessive depth can decrease its performance. To overcome this limitation, introsort switches to heap sort after the recursion depth exceeds log(n). For small numbers (n < 20), introsort switches to insertion sort. This mixed sorting algorithm can achieve the high performance of quicksort on regular datasets and maintain a performance of O(nlog(n)) in the worst case. Introsort is a built-in sorting algorithm in C++. Quicksort divides the array to be sorted into two areas for sorting. However, if there are a large number of duplicate elements, quicksort will repeatedly compare them, resulting in wasted performance. To address this issue, the array can be divided into three areas for sorting(three-area quicksort). Duplicate elements are placed in the third area, and only the other two areas are sorted. The repeated data is chosen as the pivot value, and the less-than pivot value is put into the left area, the greater-than pivot value into the right area, and the equal pivot value into the middle area. Then, three-area quicksort is recursively called on the left and right areas.

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

## 7.10 The Bucket Sort

The previously discussed different sorting techniques, including comparison-based algorithms. However, there are also sorting algorithms that do not involve comparisons, such as bucket sort, counting sort, and radix sort. Non-comparison sorting works by determining the number of elements that come before each element in the sorted set. For example, given a set of numbers ”nums”, calculating the number of elements before ”nums[i]” uniquely determines its position in the sorted set. Non-comparison sorting can be completed in a single pass with a time complexity of O(n), as it only requires counting the number of elements before each element. Although non-comparison sorting has a low time complexity, it requires additional space to determine the position, making it suitable for specific data sizes and distributions(especially numbers). Noncomparison sorting requires indexable information within the data to determine the position. In contrast, comparison sorting is suitable for data of different sizes and distributions, making it applicable in various sorting situations. Bucket sorting is one type of non-comparison sorting, where buckets are similar to slots in a hash table, but can hold multiple elements. The basic idea of bucket sorting are:

- Step 1: Divide the elements into different buckets, setting the number of buckets to k after finding maxV and minV, and dividing the interval [minV, maxV] into k equal intervals. Elements in the sequence are hashed to each bucket using a hash function (such as taking the remainder).
- Step 2: Sort the elements in each bucket with any available sorting algorithm.
- Step 3: Merge the ordered elements in each bucket into a large ordered set.

In Rust, a bucket can be defined as a structure that contains a hash function named hasher and a dataset named values.

```rust
// bucket_sort.rs

struct Bucket<H, T> {
    hasher: H, // hasher: a function, recieved when called
    values: Vec<T>, // values: a container for data
}
```

To help readers understand bucket sort, the figure below illustrates the process of hashing data into buckets, sorting within each bucket, and merging the sorted data to obtain the final ordered set.

92 70 80 66 56 44 31 20 24 5 7 0 1 2 3 4 6 8 80 70 20 66 56 31 92 44 24 20 70 80 31 56 66 92 24 44 20 24 31 44 56 66 70 80 92

Here is an implementation of bucket sort.

```rust
// bucket_sort.rs

use std::fmt::Debug;

impl<H, T> Bucket<H, T> {
    fn new(hasher: H, value: T) -> Bucket<H, T> {
        Bucket {
            hasher: hasher,
            values: vec![value]
        }
    }
}

// Bucket sort, Debug feature is used for printing T
fn bucket_sort<H, T, F>(nums: &mut [T], hasher: F)
    where H: Ord,
          T: Ord + Clone + Debug,
          F: Fn(&T) -> H,
{
    let mut buckets: Vec<Bucket<H, T>> = Vec::new();
```

```rust
    for val in nums.iter() {
        let hasher = hasher(&val);

        // Binary search and sort bucket data
        match buckets.binary_search_by(|bct|
                bct.hasher.cmp(&hasher)) {
            Ok(idx) => buckets[idx].values.push(val.clone()),
            Err(idx) => buckets.insert(idx,
                        Bucket::new(hasher, val.clone())),
        }
    }

    // Split the buckets and merge them into a single Vec
    let ret = buckets.into_iter().flat_map(|mut bucket| {
        bucket.values.sort();
        bucket.values
    }).collect::<Vec<T>>();

    nums.clone_from_slice(&ret);
}

fn main() {
    let mut nums = [0,54,32,99,18,75,31,43,4,56,21,22,1,100];
    bucket_sort(&mut nums, |t| t / 5);
    println!("{:?}", nums);
    // [0, 1, 4, 18, 21, 22, 31, 32, 43, 54, 56, 75, 99, 100]
}
```

Implementing bucket sort is more complex than comparison-based sorting algorithms because it involves creating a bucket structure and implementing a sorting algorithm that operates on this structure. In this implementation, the data is distributed into buckets using division by 5. If another value is used, the number of buckets needs to be adjusted accordingly. Bucket sort has a time complexity of O(n + nlogn −nlogk), where n is the number of elements to be sorted and k is the number of buckets used. Assuming the data is uniformly distributed, the average number of elements in each bucket is n/k. If quicksort is used to sort each bucket, the time complexity of each sorting operation is O(n/klog(n/k)). Therefore, the total time complexity can be expressed as O(n) + kO(n/klog(n/k)) = O(n + nlog(n/k)). When k is close to n, bucket sorting can be regarded as having a time complexity of O(n). One drawback of bucket sort is that it may create too many unnecessary buckets, resulting in wasted space. To address this issue, FlashSort is an optimized bucket sorting algorithm that estimates the number of buckets needed based on the number of elements to be sorted. If the number of buckets is greater than the number of elements, the number of buckets can be calculated by m = f ∗n, where f is a decimal such as 0.2. The rule for placing elements into buckets is defined by equation shown below, where K(Ai) denotes the bucket index of element Ai. K(Ai) = 1 + int((m −1) Ai −Amin

) (7.2) Amax −Amin

Assuming each bucket has an average of n/m elements, using insertion sort for each bucket results in a total time complexity of O(n2/m). Experimental results show that FlashSort performs optimally at O(n) when m = 0.42n. Moreover, when m = 0.1n, FlashSort is faster than quicksort as long as n > 80, and when n = 10000, it is twice as fast. Additionally, when m = 0.2n, it is 15% faster than when m = 0.1n. Even when m is as low as 0.05n, FlashSort is still significantly faster than quicksort when n > 200.

## 7.11 The Counting Sort

Another type of non-comparison sorting is counting sort, which is a special case of bucket sort that only handles data of the same type, and therefore requires more space. The basic idea of counting sort is as follows:

- First, initialize a counter set of length maxV - minV + 1, where maxV is the maximum value in the set to be sorted, and minV is the minimum value. Set all values in the counter set to 0.
- Second, scan the set to be sorted and use the current value minus minV as the index in the counter set, and increment the counter at this index.
- Third, scan the counter set and write the values back to the original set in order to complete the sorting.

For example, given nums=[0,7,1,7,3,1,5,8,4,4,5], first traverse nums to obtain the minimum and maximum values, maxV=8, minV=0, and then initialize a counter set of length 8 - 0 + 1. counter = [0, 0, 0, 0, 0, 0, 0, 0, 0] Then scan nums and calculate the index by subtracting minV from the current value. For example, when scanning 0, the index is 0 - 0 = 0, so the value at index 0 of counter is incremented by 1. At this point, counter is [1,0,0,0,0,0,0,0,0]. Continue scanning until the final value of counter is obtained. [1, 2, 0, 1, 2, 2, 0, 2, 1] When traversing the counter set, if a value at a certain index is not 0, write the corresponding index value into nums, and decrement the value in counter. For example, if the value at the first position 0 of counter is 1, indicating that there is one 0 in nums, write it into nums. Continuing, the value at index 1 is 2, indicating that there are two 1s in nums, write them into nums. Finally, nums is sorted as: [0, 1, 1, 3, 4, 4, 5, 5, 7, 7, 8] The sorting process is completed by scanning the counter set, and the sorting process does not involve comparison, exchange, or other operations, making it very fast. Here is an implementation of counting sort:

```rust
// counting_sort.rs

fn counting_sort(nums: &mut [usize]) {
    if nums.len() <= 1 {
        return;
    }

    // bucket number is the maximum value in nums plus 1
    let max_bkt_num = 1 + nums.iter().max().unwrap();

    // save the number of each value in nums
    let mut counter = vec![0; max_bkt_num];
    for &v in nums.iter() {
        counter[v] += 1;
    }

    // write data back to original nums slice
    let mut j = 0;
    for i in 0..max_bkt_num {
        while counter[i] > 0 {
            nums[j] = i;
```

```rust
            counter[i] -= 1;
            j += 1;
        }
    }
}

fn main() {
    let mut nums = [54,32,99,18,75,31,43,56,21,22];
    counting_sort(&mut nums);
    println!("sorted nums: {:?}", nums);
    // sorted nums: [18, 21, 22, 31, 32, 43, 54, 56, 75, 99]
}
```

## 7.12 The Radix Sort

The third type of non-comparison sorting is radix sort, which uses the radix rule of positive numbers to sort. The sorting process involves collecting and distributing data, and the specific steps are as follows:

- Step 1: Find the maximum value in the given set of integers, and determine the number of digits in it. Then, pad zeros to the left of the numbers to unify the number of digits.
- Step 2: Starting from the lowest digit, perform stable sorting, collect the numbers according to their digits, and then sort the numbers according to the next higher digit until the sorting is complete.

For instance, consider an integer sequence [1, 134, 532, 45, 36, 346, 999, 102]. The maximum value in the set is 999, which has three digits. Therefore, three rounds of sorting are required for the ones, tens, and hundreds digits. Firstly, pad zeros to the left of the numbers to make all numbers have three digits, as shown in the second column of the figure. Then, sort the numbers according to their ones digit, tens digit, and hundreds digit in order. After three rounds of sorting, the data is sorted. The red digit in the figure represents the digit being sorted in the current round, and it is apparent that the numbers are sorted based on their corresponding digit at each iteration.

![Figure 7.10: Radix sort](images/fig-7.10.png)

*Figure 7.10: Radix sort*

```rust
// radix_sort.rs

fn radix_sort(nums: &mut [usize]) {
    if nums.len() <= 1 { return; }

    // Find the largest number, which has the most digits.
    let max_num = match nums.iter().max() {
        Some(&x) => x,
        None => return,
    };

    // Find the power of 2 that is greater than or equals to
    // the length of nums as the bucket size. For example,
    // the closest and greater power of 2 to 10 is 2^4 = 16,
    // the closest and greater power of 2 to 17 is 2^5 = 32.
    let radix = nums.len().next_power_of_two();

    // The variable 'digit' represents the count of numbers
    // in a bucket that are less than a certain digit.
    // The ones, tens, hundreds, and thousands digits
    // correspond to positions 1, 2, 3, and 4, respectively.
    // The counting starts from the ones digit, so it is 1.
    let mut digit = 1;
    while digit <= max_num {
        // Calculate the position of the data in the bucket.
        let index_of = |x| x / digit % radix;
        let mut counter = vec![0; radix];
        for &x in nums.iter() {
            counter[index_of(x)] += 1;
        }
        for i in 1..radix {
            counter[i] += counter[i-1];
        }

        // sorting
        for &x in nums.to_owned().iter().rev() {
            counter[index_of(x)] -= 1;
            nums[counter[index_of(x)]] = x;
        }

        // process next bucket
        digit *= radix;
    }
}

fn main() {
    let mut nums = [0,54,32,99,18,75,31,43,56,21,22,100];
    radix_sort(&mut nums);
    println!("sorted nums: {:?}", nums);
    // sorted nums: [18, 21, 22, 31, 32, 43, 54, 56, 75, 99]
}
```

To sort by the same digit, stable sorting is used because it preserves the previous sorting result. For instance, sorting the tens digit preserves the sorting result of the ones digit, and sorting the hundreds digit preserves the sorting result of the tens digit. Binary can also be used to solve any non-negative integer sequence with the radix sorting algorithm. The time complexity is O(64n) assuming the maximum integer in the sequence is 64 bits. Although comparison-based sorting algorithms have a time complexity of O(nlog(n)), they are still faster than radix sorting since the coefficient of 64 is too large to be practical. To use binary, k=2 is the smallest and the number of digits is the largest, so the time complexity becomes O(nd) and the space complexity becomes O(n + k), which is smaller. Conversely, when using the maximum value as the radix, k=maxV is the largest and the number of digits is the smallest, resulting in a smaller time complexity of O(nd) but an increased space complexity of O(n + k), leading to radix sorting degenerating into counting sorting. In summary, these three non-comparison sorting methods (counting sorting, bucket sorting, and radix sorting) are interconnected. Counting sorting is a specific case of bucket sorting, and radix sorting degenerates into counting sorting if it uses the minimum number of digits to sort. Bucket sorting is suitable for evenly distributed elements, counting sorting requires a small difference between maxV and minV, and radix sorting can only handle positive numbers with maxV and minV being as close as possible. Therefore, these three sorting methods are only applicable for sorting small amounts of data, ideally less than 10000.

## 7.13 The Tim Sort

The TimSort hybrid sorting algorithm, proposed by Tim Peters in 2002, combines multiple sorting methods to address the limitations of individual algorithms. TimSort is efficient, stable, and adaptive to data distribution, making it superior to most sorting algorithms. It is currently the default sorting algorithm in many programming languages and platforms, including Java, Python, Rust etc. TimSort is a hybrid stable sorting algorithm that uses merge and insertion sorts. When the number of elements to be sorted is less than 64, TimSort calls insertion sort directly. However, when the number of elements is greater than 64, TimSort combines insertion and merge sorts. In practice, the data to be sorted often contains partially ordered blocks, where some parts of the data are already sorted in ascending or descending order, as shown in the figure below. TimSort leverages this characteristic of the data to sort it, and the existence of partially ordered blocks is the core of TimSort.

![Figure 7.11: Partially ordered data](images/fig-7.11.png)

*Figure 7.11: Partially ordered data*

To sort the set of elements, TimSort divides them into runs or partitions. These runs can be seen as individual computational units. TimSort iterates through the elements and places them in different runs while merging the runs according to certain rules. This merging continues until only one run remains, which is the sorted result. To set the appropriate partition size, TimSort sets the minrun parameter. Each partition cannot have fewer elements than minrun. If a partition has fewer elements than minrun, the number of runs is expanded to minrun using insertion sort and then merged.

![Figure 7.12: Data Runs](images/fig-7.12.png)

*Figure 7.12: Data Runs*

The approximate process of TimSort is as follows:

- Scan the set to be sorted to determine whether the number of elements is greater than 64.
- If it is less than or equal to 64, use the insertion sort algorithm to sort the data and return.
- If it is greater than 64, scan the set, calculate the minrun, and find various ordered blocks.
- Merge the blocks in pairs. If an individual block has fewer elements than minrun, use insertion sort to expand it.
- Repeat this process until only one block remains, which is the sorted set.

TimSort is a sorting algorithm that can be completed by addressing three important points: determining the minrun value, finding ordered blocks, and expanding and merging small blocks. The first point is to determine the value of minrun. TimSort selects the first six binary digits of the length n of the collection to be sorted as the minrun. If the remaining digits are not 0, then minrun is incremented by 1. The range of minrun is from 32 to 64.

- For a collection of length n = 189, its binary representation is: 10111101. The first six digits, 101111, equal 47, and the remaining digits, 01, lead to a minrun value of 48.
- For a collection of length n = 976, its binary representation is: 1111010000. The first six digits, 111101, equal 61, and the remaining digits, 0000, lead to a minrun value of 61.

In fact, the maximum value of the first six binary digits is 111111 = 63, and the minimum is 100000 = 32. Therefore, the minrun value ranges from 32 to 64. The second point is to find ordered blocks. TimSort finds ordered blocks by identifying increasing or decreasing sequences in the collection. This is achieved by an algorithm that only needs to judge the compare relationship of consecutive data to determine whether it is a block. The third point is to expand and merge small blocks. Once the minrun value is calculated, TimSort adjusts any blocks that are in reverse order in place to be in the correct order. If the block has fewer elements than minrun, insertion sort is used to expand the block until it reaches minrun. The algorithm then checks the relationship between the current block and the previous two blocks. If the length of the three blocks does not satisfy A > B + C, B > C, then A and B or B and C are merged using insertion sort depending on the situation. If not, the algorithm continues to find the next block and repeat the block expansion and merging. Finally, the collection becomes several ordered blocks, and these merged blocks have lengths from longest to shortest. After the block division is completed, the small blocks are merged in pairs from the end of the collection to the beginning, and the collection becomes a large block, indicating that the sorting is completed. The first two points are clear, but the third point may require further explanation. Reversing the order of a block is a simple process. To expand a block, new elements are inserted into the current block. However, merging blocks can be complicated as there are six possible scenarios. When there are only two blocks, the algorithm only needs to consider the condition of A > B. When there are three blocks, the algorithm checks whether A > B + C and B > C. Here are the illustrations of the six cases, where A is at the bottom of the stack, and B or C is at the top:

- A > B: Do not merge.
- A < B: Merge run A with B.
- A > B + C and B > C: Do not merge.
- A > B + C and B < C: Merge run B with C.
- A < B + C and A > C: Merge run B with C. • A < B + C and A < C: Merge run A with B.

```rust
1: A > B, no merge
                              2: A < B,B merges A
     |
                       |
                                   |
                                                     |
B -> |
         [xxxxxxxxx]
                       |
                              B -> | [xxxxxxxxxxxxx] |
     |
                       |
                                   |
                                                     |
A -> | [xxxxxxxxxxxxx] |
                              A -> |
                                       [xxxxxxxxx]
                                                     |
     |
                       |
                                   |
                                                     |
3: A > B + C; B > C, no merge 4: A > B + C; B < C, B merges C
     |
                       |
                                   |
                                                     |
C -> |
           [xxx]
                       |
                              C -> |
                                       [xxxxxxx]
                                                     |
     |
                       |
                                   |
                                                     |
B -> |
         [xxxxxxxx]
                       |
                              B -> |
                                         [xxx]
                                                     |
```

```rust
     |
                       |
                                   |
                                                     |
A -> | [xxxxxxxxxxxxx] |
                              A -> | [xxxxxxxxxxxxx] |
     |
                       |
                                   |
                                                     |
5: A < B + C; A > C, B merges C 6: A < B + C; C > A, B merges A
     |
                       |
                                   |
                                                     |
C -> |
          [xxxxxx]
                       |
                              C -> |
                                      [xxxxxxxxxxx]
                                                     |
     |
                       |
                                   |
                                                     |
B -> |
         [xxxxxxxx]
                       |
                              B -> | [xxxxxxxxxxxxx] |
     |
                       |
                                   |
                                                     |
A -> | [xxxxxxxxxxxxx] |
                              A -> |
                                       [xxxxxxxxx]
                                                     |
     |
                       |
                                   |
                                                     |
```

The figure depicts the merging of three ordered blocks with a minimum run of 3. The characters A, B, and C represent the run blocks [xx], while the vertical lines represent a temporary stack used to merge these blocks. To determine whether and how to merge the blocks, the lengths of the three blocks are compared. The ideal merged state is shown in cases 1 and 3, while the other four merging scenarios are used to approximate these two cases. The condition that A > B + C, B > C is necessary to ensure efficient merging. For example, merging the block [6,7,8] directly with [0,1,2,3,4,9,5] would result in two remaining blocks with a large difference in length, making insertion sort inefficient. In contrast, when the blocks have similar lengths, merging them is very fast. Therefore, in this case, the blocks are not merged and are processed separately before being merged in reverse order at the end: [6,7,8] and [5], followed by [0,1,2,3,4,9] and [5,6,7,8].

7 5 0 3 9 6 8 1 2 4

To simplify the sorting process, a minimum run length is set, below which binary insertion sort is used. If the run length equals 64, minrun is also set to 64. Otherwise, a value between 32-64 is chosen

n

for minrun such that k =

minrun is less than or equal to a power of 2. k represents the number of

remaining blocks after scanning and processing, and their lengths must be sorted from largest to smallest. This enables merging from the tail, resulting in longer blocks and faster merging, akin to binary search. Hence, k is required to be less than or equal to a power of 2.

![Figure 7.13: TimSort](images/fig-7.13.png)

*Figure 7.13: TimSort*

To illustrate the block expansion and merging mechanism, diagrams are presented above. For this example, minrun = 5, and each row represents an operation cycle. The leftmost column indicates the cycle number, and the square box contains the elements to be sorted. The TimSort algorithm consists of several rounds of processing to sort a given set of data. In the first round, the algorithm obtains the data to be sorted from its parameters. In the second round, it searches for partitions and identifies a partition of length equal to the minimum run value, which is a predetermined set of values [2,4,7,8,23]. In the third round, it searches for the next partition and finds an inversion [19,16,14,13,12,10], which is then corrected to be in order as values [10,12,13,14,16,19]in the fourth round. In the fifth round, the algorithm compares the length of the current partition to that of the previous partition and merges them using insertion sort if the current partition is longer. The result is [2,4,7,8,10,12,13,14,16,19,23], a new partition that is a combination of the two previous partitions. In the sixth round, it finds the next partition [20,18,17,15,11,9], detects an inversion, and corrects it to be in order in the seventh round. It then compares its length to the previous partition and continues searching for the next partition since it is shorter. In the eighth round, the algorithm finds a new partition [0,5,6] that is shorter than the minimum run value and expands it using insertion sort. It then compares its length to the previous two partitions and determines that they satisfy certain conditions, which means that they do not need to be merged. This process continues until all the partitions are complete, which occurs after ten rounds. In the eleventh round, the algorithm starts merging the smaller partitions from the end to the beginning([0,1,3,5,6] and [21, 22]). In the twelfth round, it merges the two remaining partitions [9,11,15,17,18,20] and [0,1,3,5,6,21,22], which are of similar length. Finally, in the thirteenth round, the algorithm performs the final merge to obtain the sorted output. To implement TimSort, the process can be broken down into several steps. Firstly, the original data list and the minimum number of elements required for merging (MIN_MERGE) need to be prepared. Next, the starting position of each run and its corresponding run can be obtained through the partition process. After that, since merge sorting involves temporary stacks and processing of two runs, these data related to sorting tasks can be implemented in a structure. Finally, the actual merging process can be performed from the small partitions at the end to the beginning, with longer partitions merged with shorter ones and the partitions of decreasing length for easier merging.

```rust
// tim_sort_without_gallop.rs

// The minimum length of a sequence involved in merging,
// shorter than which insertion sort is used.
const MIN_MERGE: usize = 64;

// Sorting state structure
struct SortState<'a> {
    list: &'a mut [i32],
    runs: Vec<Run>, // store all run(s)
    pos: usize,
}

// Define the Run entity to save the starting index and
// interval length of the run in the list.
#[derive(Debug, Copy, Clone)]
struct Run {
    pos: usize,
    len: usize,
}
```

```rust
// merge_lo: a sorting state structure, used for merging
// sorting A and B.
struct MergeLo<'a> {
    list_len: usize, // The length of the data
    first_pos: usize, // first position of run1
    first_len: usize, // length of run1
    second_pos: usize, // first position of run2
    dest_pos: usize, // index of the sorted result.
    list: &'a mut [i32], // partial interval of the data
                         // to be sorted
    temp: Vec<i32>, // with a length set as the minimum
                         // value between the lengths of
                         // run1 and run2.
}

// merge_hi: a sorting state structure, used for merging
// sorting B and C.
struct MergeHi<'a> {
    first_pos: isize,
    second_pos: isize,
    dest_pos: isize,
    list: &'a mut [i32],
    temp: Vec<i32>, // used for memory alignment
}
```

For blocks with less than MIN_MERGE elements, binary insertion sort can be used to speed up the sorting process. This method has already been implemented in the previous section, so no further code will be provided. When using TimSort, the first step is to calculate the minrun value and identify the sorted runs (including reverse runs). If necessary, the reverse runs should be converted to regular runs.

```rust
// tim_sort_without_gallop.rs

// Calculate minrun, actual range is [32, 64]
fn calc_minrun(len: usize) -> usize {
    // If any bit in the low bits of len is 1, r is set to 1
    let mut r = 0;
    let mut new_len = len;
    while new_len >= MIN_MERGE {
        r |= new_len & 1;
        new_len >>= 1;
    }

    new_len + r
}

// Calculate the starting index of the run and convert
// the reverse run to a forward run
fn count_run(list: &mut [i32]) -> usize {
    let (ord, pos) = find_run(list);
    if ord { // convert reverse run to a forward run
        list.split_at_mut(pos).0.reverse();
    }
```

```rust
    pos
}

// Determine whether the relationship between list[i]
// and list[i+1] is ascending or descending and
// return the inflection point index
fn find_run(list: &[i32]) -> (bool, usize) {
    let len = list.len();
    if len < 2 {
        return (false, len);
    }

    let mut pos = 1;
    if list[1] < list[0] {
        // descending: list[i+1] < list[i]
        while pos < len - 1 && list[pos + 1] < list[pos] {
            pos += 1;
        }
        (true, pos + 1)
    } else {
        // ascending: list[i+1] >= list[i]
        while pos < len - 1 && list[pos + 1] >= list[pos] {
            pos += 1;
        }
        (false, pos + 1)
    }
}
```

Next, to sort the SortState, you will need to implement a constructor and a sort function. Finally, when the length of the partitions does not meet the requirements, partition merging needs to be performed using merge sort.

```rust
// tim_sort_without_gallop.rs

impl<'a> SortState<'a> {
    fn new(list: &'a mut [i32]) -> Self {
        SortState {
            list: list,
            runs: Vec::new(),
            pos: 0,
        }
    }

    fn sort(&mut self) {
        let len = self.list.len();
        // calculate the minrun
        let minrun = calc_minrun(len);

        while self.pos < len {
            let pos = self.pos;
            let mut run_len = count_run(self.list
                                            .split_at_mut(pos)
```

```rust
                                            .1);

            // check if the remaining number of elements is
            // less than minrun, if so,
            // let run_minlen = len - pos
            let run_minlen = if minrun > len - pos {
                len - pos
            } else {
                minrun
            };

            // If the run is very short, extend its length
            // to run_minlen, and the extended run needs to
            // be sorted, so use binary insertion sort
            if run_len < run_minlen {
                run_len = run_minlen;
                let left = self.list
                               .split_at_mut(pos).1
                               .split_at_mut(run_len).0;
                binary_insertion_sort(left);
            }

            // Stack the runs, with each run having a
            // different length
            self.runs.push(Run {
                pos: pos,
                len: run_len,
            });

            // Find the next run position
            self.pos += run_len;

            // Merge runs that do not conform to the
            // A > B + C and B > C rules
            self.merge_collapse();
        }

        // Forcefully merge all remaining runs from the top
        // of the stack until only one run remains,
        // completing the tim_sort sort
        self.merge_force_collapse();
    }

    // Merge runs to satisfy A > B + C and B > C
    // If A <= B + C, merge B with the shorter of A and C
    // If only A and B, and A <= B, merge A and B
    fn merge_collapse(&mut self) {
        let runs = &mut self.runs;
        while runs.len() > 1 {
            let n = runs.len() - 2;
```

```rust
            // check the relationships between A, B, C, and D
            // with D to prevent special cases of bugs
            // A <= B + C || D <= A + B
            if (n >= 1 && runs[n - 1].len
                <= runs[n].len + runs[n + 1].len)
                || (n >= 2 && runs[n - 2].len
                    <= runs[n].len + runs[n - 1].len)
            {
                // Determine the length relationship between
                // three consecutive runs A, B, and C,
                // and merge n-1 corresponding to A,
                // n corresponding to B, and n+1
                // corresponding to C
                let (pos1, pos2) = if runs[n-1].len
                                        < runs[n+1].len {
                    (n - 1, n) // merge A and B
                } else {
                    (n, n + 1) // merge B and C
                };

                // Take out run1 and run2 to be merged
                let (run1, run2) = (runs[pos1], runs[pos2]);
                debug_assert_eq!(run1.pos+run1.len, run2.pos);

                // Merge run to run1, i.e., update run1
                // and delete run2,
                // run1 index remains unchanged, and length
                // becomes the len(run1) + len(run2)
                runs.remove(pos2);
                runs[pos1] = Run {
                    pos: run1.pos,
                    len: run1.len + run2.len,
                };

                // Take the merged run1 for merge sort
                let new_list = self.list
                    .split_at_mut(run1.pos).1
                    .split_at_mut(run1.len + run2.len).0;
                merge_sort(new_list, run1.len, run2.len);
            } else {
                break;
            }
        }
    }

    // Forcefully merge any remaining runs until
    // only one run remains
    fn merge_force_collapse(&mut self) {
        let runs = &mut self.runs;
        while runs.len() > 1 {
            let n = runs.len() - 2;
```

```rust
            // Check the length relationship between three
            // consecutive runs A, B, and C,
            // and merge n-1 corresponding to A,
            // n corresponding to B, n+1 corresponding to C
            let (pos1, pos2) = if n > 0
                   && runs[n - 1].len < runs[n + 1].len {
                (n - 1, n)
            } else {
                (n, n + 1)
            };

            // Take out run1 and run2 to be merged
            let (run1, run2) = (runs[pos1], runs[pos2]);
            debug_assert_eq!(run1.len, run2.pos);

            // Merge run to run1, i.e., update run1
            // and delete run2,
            // run1 index remains unchanged, and length
            // becomes the sum of the lengths of run1 and run2
            runs.remove(pos2);
            runs[pos1] = Run {
                pos: run1.pos,
                len: run1.len + run2.len,
            };

            // Take the merged run1 for merge sort
            let new_list = self.list
                .split_at_mut(run1.pos).1
                .split_at_mut(run1.len + run2.len).0;
            merge_sort(new_list, run1.len, run2.len);
        }
    }
}
```

There are six cases of partitioning, which may require merging A and B or merging B and C. Since A, B, and C are contiguous in memory, merging A and B can be implemented separately from merging B and C, taking advantage of their relative positions.

```rust
// tim_sort_without_gallop.rs

// merge sort for A, B and C
fn merge_sort(
    list: &mut [i32],
    first_len: usize,
    second_len: usize)
{
    if 0 == first_len || 0 == second_len { return; }

    if first_len > second_len {
        // Merge B and C, and merge from the end
        // of the list using temp
        merge_hi(list, first_len, second_len);
    } else {
```

```rust
        // Merge B and A, and merge from the beginning
        // of the list using temp
        merge_lo(list, first_len);
    }
}

// merge A and B to a single run
fn merge_lo(list: &mut [i32], first_len: usize) {
    unsafe {
        let mut state = MergeLo::new(list, first_len);
        state.merge();
    }
}

impl<'a> MergeLo<'a> {
    unsafe fn new(list: &'a mut [i32], first_len: usize) ->
       Self { let mut ret_val = MergeLo {
            list_len: list.len(),
            first_pos: 0,
            first_len: first_len,
            second_pos: first_len, // run1 close to run2,
                                   // the start index of run2
                                   // is exactly equals the
                                   // length of run1
            dest_pos: 0, // write the sorted data
                                   // back to run1
            list: list,
            temp: Vec::with_capacity(first_len),
        };

        // copy run1 to temp
        ret_val.temp.set_len(first_len);
        for i in 0..first_len {
            ret_val.temp[i] = ret_val.list[i];
        }

        ret_val
    }

    // merge sort
    fn merge(&mut self) {
        while self.second_pos > self.dest_pos
             && self.second_pos < self.list_len {
            debug_assert!((self.second_pos - self.first_len) +
                self.first_pos == self.dest_pos);

            if self.temp[self.first_pos]
                    > self.list[self.second_pos] {
                self.list[self.dest_pos]
                    = self.list[self.second_pos];
                self.second_pos += 1;
```

```rust
            } else {
                self.list[self.dest_pos]
                    = self.temp[self.first_pos];
                self.first_pos += 1;
            }
            self.dest_pos += 1;
        }
    }
}

// clear temp stack
impl<'a> Drop for MergeLo<'a> {
    fn drop(&mut self) {
        unsafe {
            // put left date of temp into list(high digit)
            if self.first_pos < self.first_len {
                for i in 0..(self.first_len - self.first_pos) {
                    self.list[self.dest_pos + i]
                        = self.temp[self.first_pos + i];
                }
            }

            // set the lenght of temp to 0
            self.temp.set_len(0);
        }
    }
}

// merge B and C as a new run block
fn merge_hi(
    list: &mut [i32],
    first_len: usize,
    second_len: usize)
{
    unsafe {
        let mut state = MergeHi::new(list,
                                     first_len,
                                     second_len);
        state.merge();
    }
}

impl<'a> MergeHi<'a> {
    unsafe fn new(
        list: &'a mut [i32],
        first_len: usize,
        second_len: usize) -> Self
    {
        let mut ret_val = MergeHi {
            first_pos: first_len as isize - 1,
            second_pos: second_len as isize - 1,
            dest_pos: list.len() as isize - 1,// from the tail
```

```rust
            list: list,
            temp: Vec::with_capacity(second_len),
        };

        // copy run2 to temp
        ret_val.temp.set_len(second_len);
        for i in 0..second_len {
            ret_val.temp[i] = ret_val.list[i + first_len];

        }

        ret_val
    }

    // merge sort
    fn merge(&mut self) {
        while self.first_pos < self.dest_pos
             && self.first_pos >= 0 {
            debug_assert!(self.first_pos + self.second_pos + 1
                == self.dest_pos);
            if self.temp[self.second_pos as usize]
                >= self.list[self.first_pos as usize] {
                self.list[self.dest_pos as usize]
                    = self.temp[self.second_pos as usize];
                self.second_pos -= 1;
            } else {
                self.list[self.dest_pos as usize]
                    = self.list[self.first_pos as usize];
                self.first_pos -= 1;
            }
            self.dest_pos -= 1;
        }
    }
}

// clear temp stack
impl<'a> Drop for MergeHi<'a> {
    fn drop(&mut self) {
        unsafe {
            // put left date of temp into list(low digit)
            if self.second_pos >= 0 {
                let size = self.second_pos + 1;
                let src = 0;
                let dest = self.dest_pos - size;
                for i in 0..size {
                    self.list[(dest + i) as usize]
                        = self.temp[(src + i) as usize];
                }
            }

            // set the length of temp stack to 0
            self.temp.set_len(0);
```

```text
        }
    }
}
```

Here is the main function of TimSort.

```rust
// timSort entry point

fn tim_sort(list: &mut [i32]) {
    if list.len() < MIN_MERGE {
       binary_insertion_sort(list);
    } else {
       let mut sort_state = SortState::new(list);
       sort_state.sort();
    }
}
```

Here is an example of TimSort.

```rust
fn main() {
    let mut nums: Vec<i32> = vec![
         2, 4, 7, 8, 23, 19, 16, 14, 13, 12, 10, 20,
        18, 17, 15, 11, 9, -1, 5, 6, 1, 3, 21, 40,
        22, 39, 38, 37, 36, 35, 34, 33, 24, 30, 31, 32,
        25, 26, 27, 28, 29, 41, 42, 43, 44, 45, 46, 47,
        48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
        60, 80, 79, 78, 77, 76, 75, 74, 73, 72, 71, 70,
        61, 62, 63, 64, 65, 66, 67, 68, 69, 95, 94, 93,
        92, 91, 90, 85, 82, 83, 84, 81, 86, 87, 88, 89,
    ];
    tim_sort(&mut nums);
    println!("sorted nums: {:?}", nums);
}
sorted nums: [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95]
```

The implemented TimSort algorithm only works for i32 type numbers, but it can be extended to support sorting algorithms for various types of numbers through the use of generics. Additionally, during merging, some data may already be sorted, but the implemented TimSort algorithm still goes through each comparison one by one. However, merging can be accelerated through a strategy called galloping. The TimSort implementation in this book’s source code in tim_sort_without_gallop.rs is the nonaccelerated version, but an accelerated version of Timsort has also been implemented in tim_sort.rs. Interested readers can refer to and compare the differences between the two algorithms. Some readers may wonder how TimSort determines if the data to be sorted is block-sorted originally. In reality, the algorithm cannot determine this; it is a property of the partially ordered data that the author discovered. In physics, there is a concept of entropy [13] that refers to the degree of disorder in a physical

system. The more disorderly a system is, the greater the entropy, and conversely, the more ordered it is, the smaller the entropy. In most cases, things have a certain degree of order. For example, humans are ordered animals in reverse entropy, and only become disordered with death. Another example is the principle of locality of reference [14], where when accessing data on a hard drive, the CPU will read the data around it into memory because it is likely to be accessed next. These two phenomena are natural laws that are consistent with statistical principles, and Tim wrote TimSort based on these laws. This illustrates the importance of data structures and how different understandings can lead to very different algorithms.

## 7.14 Summary

In this chapter, we learned about ten different types of sorting algorithms. Bubble sort, selection sort, and insertion sort are O(n2) algorithms, while most other sorting algorithms have a complexity of O(nlog2(n)). Selection sort is an improvement on bubble sort, shell sort improves on insertion sort, heap sort improves on selection sort, and quicksort and merge sort both use the divide-and-conquer approach. All of these sorts are based on comparison, but there are also non-comparison sorts that rely solely on numerical patterns for sorting, such as bucket sort, counting sort, and radix sort. These sorts have a complexity of approximately O(n) and are suitable for sorting small amounts of data. Counting sort is a special case of bucket sort, and radix sort is a multi-round bucket sort that can degrade into counting sort. In addition to the basic sorting algorithms, we also learned about improved versions of some algorithms, particularly the TimSort algorithm, which is an efficient and stable hybrid sorting algorithm. Its improved version is already the default sorting algorithm for many languages and platforms. The table below summarizes the various sorting algorithms, which readers can compare and understand on their own to deepen their understanding.

**Table 7.1: Time and space complexity of various sorting algorithms**

| No | Algorithm | Time-worst | Time-best | Time-average | Space | Stability |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Bubble sort | O(n2) | O(n) | O(n2) | O(1) | stable |
| 2 | Quick sort | O(n2) | O(nlog(n)) | O(nlog(n)) | O(nlog(n)) | unstable |
| 3 | Selection sort | O(n2) | O(n2) | O(n2) | O(1) | unstable |
| 4 | Heap sort | O(nlog(n)) | O(nlog(n)) | O(nlog(n)) | O(1) | unstable |
| 5 | Insertion sort | O(n2) | O(n) | O(n2) | O(1) | stable |
| 6 | Shell sort | O(n2) | O(n) | O(n1.3) | O(1) | unstable |
| 7 | Merge sort | O(nlog(n)) | O(nlog(n)) | O(nlog(n)) | O(n) | stable |
| 8 | Counting sort | O(n + k) | O(n + k) | O(n + k) | O(n + k) | stable |
| 9 | Bucket sort | O(n2) | O(n) | O(n + k) | O(n + k) | stable |
| 10 | Radix sort | O(nk) | O(nk) | O(nk) | O(n + k) | stable |
| 11 | Tim sort | O(nlog(n)) | O(n) | O(nlong(n)) | O(n) | stable |
