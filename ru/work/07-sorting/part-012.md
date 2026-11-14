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
