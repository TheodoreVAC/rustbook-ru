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
