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
