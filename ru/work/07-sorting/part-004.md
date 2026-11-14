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
