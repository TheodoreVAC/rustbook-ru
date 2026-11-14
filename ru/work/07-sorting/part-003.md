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
