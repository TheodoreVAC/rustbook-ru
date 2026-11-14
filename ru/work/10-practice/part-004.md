## 10.4 Filters

In many software projects, determining whether an element exists in a collection is a common task. For instance, in word processing software, it is essential to verify if an English word is spelled correctly by checking if it exists in a known dictionary. Similarly, in the FBI, it is necessary to determine if a suspect’s name appears on the suspect list to issue an FBI Warning. Likewise, in a web crawler, it is crucial to determine if a URL has been visited. To achieve this, the most straightforward approach is to store all the elements in the collection in the computer and compare them directly with the new element encountered. Usually, computer sets use a hash table to store the collection, which is fast and accurate but consumes more space. For small data collections, this approach is adequate. However, when the collection is extensive, the low storage efficiency of hash tables becomes apparent. For example, email providers such as Yahoo or Gmail need to filter spam regularly. One way to accomplish this is to keep a record of the email addresses of those who send spam. However, since spammers keep registering new addresses, storing all of them would require numerous network servers. Storing 100 million email addresses in a hash table requires about 1.6 GB of memory, which is a considerable amount. Furthermore, hash tables have a load factor that may not allow the full utilization of space. Additionally, if the data set is stored on a remote server and input is accepted locally, it may not be feasible to construct a hash table since the dataset is too large to read into memory at once.

### 10.4.1 The Bloom Filter

When dealing with problems of identifying elements in a set or collection, Bloom Filters are a useful data structure to consider. These probabilistic data structures were introduced by Burton Howard Bloom in 1970 and consist of a long binary vector and random mapping functions. They are particularly useful in terms of space and query efficiency, although they do have a certain error rate and deleting elements can be challenging. A Bloom Filter, shown below , is composed of a binary vector (bit array) that can store n data elements and k hash functions. Two basic operations are supported: insert and query. However, the number of values that can be inserted is fixed at design time, so the size of the Bloom Filter must be specifically designed for the problem at hand.

x,y 0 1 0 1 1 0 0 1 0 1 0 1 z

Initially, all positions in the Bloom Filter are set to 0. When data is inserted, k hash functions are used to determine the position of the data in the filter and set the corresponding positions to 1. For instance, when k = 3, three hash values are calculated as indices, and their corresponding positions are set to 1. When querying, k hash functions are also used to generate k hash values as indices. If all indices correspond to values that are 1, then the element may exist in the set. In the given figure, x and y are stored in the Bloom Filter, but the last hash value for z is 0, so it definitely does not exist in the filter. To experience a Bloom Filter, visit bloomfilter. To determine the optimal number of elements m to be stored in a Bloom filter of length n with a tolerable error rate of ϵ, use the formula: m = −nlnϵ

(10.3) (ln2)2

To calculate the required number of hash functions k, use the formula:

k = −lnϵ

ln2 = −log2ϵ

(10.4)

For example, if the tolerable error rate ϵ is 8%, then k would be 3, and a larger k value would indicate a higher error rate. It is possible to simulate k hash functions by combining two basic hash functions and the number of iterations, without changing the fault-tolerance rate, using the following formula: gi(x) = h1(x) + ih2(x)

(10.5)

To implement a Bloom filter, a struct can be used to encapsulate all the necessary information, including the set of storage bits and hash functions. Since Bloom filter only determines the existence of a value and not the value itself, it must be able to accommodate data of any type using generics. The Boolean values of 1 and 0 can be used to represent the storage bits, and they can be saved to a Vec for easy implementation. During the judgment process, the Boolean value can indicate whether the value exists or not.

```rust
// bloom_filter.rs

use std::collections::hash_map::DefaultHasher;

// Definition of bloom filter
struct BloomFilter<T> {
    bits: Vec<bool>, // Bit bucket
    hash_fn_count: usize, // Number of hash functions
    hashers: [DefaultHasher; 2], // Two hash functions
}
```

The code above cannot compile since the generic type T is not used by any field, which violates Rust’s rules. To make it compile, we can use Rust’s phantom data to occupy the space of T. Phantom data can pretend to use T without actually using it, deceiving the compiler into passing the code. Additionally, to support data with an undefined size at compile time, we add the ?Sized trait to make the filter work with such data types. We prefix the unused field with _phantom to indicate that it is not used and occupies 0 bytes. However, it includes T to deceive the compiler. We also simulate k hash functions using two random hash functions.

```rust
// bloom_filter.rs

use std::collections::hash_map::DefaultHasher;
use std::marker::PhantomData;

// Definition of a new bloom filter
struct BloomFilter<T: ?Sized> {
    bits: Vec<bool>,
    hash_fn_count: usize,
    hashers: [DefaultHasher; 2],
    _phantom: PhantomData<T>,
    // T is a placeholder
    // for deceiving the compiler
}
```

To implement the filter’s functionality, we need to implement three functions: the initialization function new, the function to add elements insert, and the function to check contains. We also need auxiliary functions to implement the first three functions. The new function calculates the size of m based on the fault tolerance rate and the approximate storage scale, and initializes the filter.

```rust
// bloom_filter.rs

use std::hash::{BuildHasher, Hash, Hasher};
use std::collections::hash_map::RandomState;

impl<T: ?Sized + Hash> BloomFilter<T> {
    fn new(cap: usize, ert: f64) -> Self {
        let ln22 = std::f64::consts::LN_2.powf(2f64);

        // Calculate the size of the bit bucket and
        // the number of hash functions
        let bits_count = -1f64 * cap as f64 * ert.ln() / ln22;
        let hash_fn_count = -1f64 * ert.log2();

        // Random hash function
        let hashers = [
            RandomState::new().build_hasher(),
            RandomState::new().build_hasher(),
        ];

        Self {
            bits: vec![false; bits_count.ceil() as usize],
            hash_fn_count: hash_fn_count.ceil() as usize,
            hashers: hashers,
            _phantom: PhantomData,
```

```rust
        }
    }

    // Set the corresponding bit of the bit bucket to true
    // according to hash_fn_count
    fn insert(&mut self, elem: &T) {
        let hashes = self.make_hash(elem);
        for fn_i in 0..self.hash_fn_count {
            let index = self.get_index(hashes, fn_i as u64);
            self.bits[index] = true;
        }
    }

    // Data query
    fn contains(&self, elem: &T) -> bool {
        let hashes = self.make_hash(elem);
        (0..self.hash_fn_count).all(|fn_i| {
            let index = self.get_index(hashes, fn_i as u64);
            self.bits[index]
        })
    }

    // Calculate hash value
    fn make_hash(&self, elem: &T) -> (u64, u64) {
        let hasher1 = &mut self.hashers[0].clone();
        let hasher2 = &mut self.hashers[1].clone();
        elem.hash(hasher1);
        elem.hash(hasher2);

        (hasher1.finish(), hasher2.finish())
    }

    // Get the index of a certain bit in the bit bucket
    fn get_index(&self, (h1,h2):(u64,u64),fn_i:u64) -> usize {
        let ih2 = fn_i.wrapping_mul(h2);
        let h1pih2 = h1.wrapping_add(ih2);
        ( h1pih2 % self.bits.len() as u64) as usize
    }
}
fn main() {
    let mut bf = BloomFilter::new(100, 0.08);
    (0..20).for_each(|i| bf.insert(&i));
    let res1 = bf.contains(&2);
    let res2 = bf.contains(&200);
    println!("2 in bf: {res1}, 200 in bf: {res2}");
    // 2 in bf: true, 200 in bf: false
}
```

By analyzing the Bloom filter, we can conclude that its space complexity is O(m), while the time complexity of insert and contains is O(k). However, k is typically small, so we can consider the time complexity as O(1).

### 10.4.2 The Cuckoo Filter

The Bloom filter, as discussed earlier, is relatively easy to implement, but it has a couple of disadvantages. Firstly, as more data is inserted, the error rate increases. Secondly, it does not support the deletion of data. Lastly, it uses random access memory, which does not perform well on CPUs with cache, as stated in CloudFlare’s article ”When Bloom filters don’t bloom”. To overcome these issues, the Cuckoo filter [18] was developed as an improved version of the Bloom filter. The Cuckoo filter uses paired hash functions to map data to two positions: one is the saved position and the other is the alternate position, used to handle collisions. The Cuckoo filter uses paired hash functions to map data to two positions: one is the saved position, and the other is the alternate position, which is used to handle collisions. It is named after the cuckoo bird, which lays its eggs in other birds’ nests and lets them hatch and raise its offspring. The cuckoo chick hatches earlier than the other chicks and pushes the other eggs out of the nest to monopolize the food from its foster parents. Inspired by this biological phenomenon, the Cuckoo filter also kicks out the original element at the collided position and replaces it with the new element. If the alternate position is also occupied, it repeats this process until it reaches a predefined limit and confirms that the hash table is full. Unlike the Bloom filter, the Cuckoo filter stores not only 0s and 1s but also a fixed number of bits of data, known as fingerprints. The length of the fingerprint is determined by the false positive rate ϵ, with smaller ϵ requiring longer fingerprints. The Cuckoo filter is based on the Cuckoo hash table, which is extended into a two-dimensional matrix to store multiple fingerprints in each bucket.

0 0 0 c 1 1 1 2 b 2 b 2 h1(x) h1(x) relocate 3 3 3 c a 4 4 4 x x 5 5 5 relocate h2(x) a x h2(x) 6 6 6 7 7 7

When inserting an element into the Cuckoo filter, if two buckets are already occupied, the filter randomly chooses one of the elements to be kicked out to an alternate position, and the previously kickedout element takes the newly emptied spot. This filter supports insertion, deletion, and lookup operations. In the standard Cuckoo hash table shown in the left diagram, inserting a new item into the existing hash table requires accessing the original item to determine its position and make room for the new item. However, since the Cuckoo filter only stores fingerprints, there is no way to rehash the original item to find its alternate position. To overcome this limitation, a technique called partial-key Cuckoo hashing can be used to obtain an item’s alternate position based on its fingerprint. For item x, the two candidate bucket indices are calculated using the same hashing function as follows:

h1(x) = hash(x) (10.6)

h2(x) = h1(x) ⊕hash(fingureprint(x)) The XOR operation ⊕ensures that h1(x) and h2(x) can be calculated using the same formula, so it is not necessary to know the value of x to determine the position of the alternate bucket using Equation (10.7). j = i ⊕hash(fingureprint(x))

(10.7)

The lookup method is straightforward: first use Equation (10.6) to calculate the fingerprint of the item to be searched and the positions of the two alternate buckets, then read the values in those buckets. If any of the buckets contains a value that matches the fingerprint of the item being searched, then it exists

in the filter. The deletion method is similarly simple: check the values in the two alternate buckets, and if there is a match, delete the copy of the fingerprint in that bucket. It is important to ensure that the item is inserted before attempting to delete it, otherwise it may accidentally delete other values with the same fingerprint. After extensive experimentation and testing, a bucket size of 4 was found to provide excellent performance, even the best performance. The Cuckoo filter boasts four main advantages over Bloom filters: (1) Supports dynamic addition and deletion of items. (2) Higher lookup performance than Bloom filters, even when approaching full capacity. (3) Easier to implement than other Bloom filter alternatives, such as quotient filters. (4) In practical applications, it uses less space than Bloom filters if the false positive rate ϵ is less than 3%. In addition to Bloom filters and Cuckoo filters, there are many other filters with various characteristics that interested readers can search for and refer to.

**Table 10.1: Comparison of Various Filters**

| Filter Type | Space Usage | Hash Function | Deletion |
| --- | --- | --- | --- |
| Bloom Filter | 1 | k | no |
| Blocked Bloom Filter | 1x | 1 | no |
| Couting Bloom Filter | 3x-4x | k | yes |
| D-left Counting Bloom Filter | 1.5x-2x | d | yes |
| Quotient Filter | 1x-1.2x | ≥1 | yes |
| Cuckoo Filter | ≤1x | 2 | yes |

To implement the Cuckoo Filter, we need to extend the Bloom Filter to two dimensions. This requires us to create two new data structures: FingerPrint to store the fingerprints, and Bucket to store the FingerPrints. Since the implementation involves random access and hashing operations, we utilize libraries such as Rng and Serde in the code. We implement the Cuckoo Filter as a Rust library, where bucket.rs includes the definitions and operations of FingerPrint and Bucket, and util.rs includes the struct FaI for calculating fingerprints and bucket indexes. The code structure is as follows.

```text
shieber@Kew:cuckoofilter/ tree
 /Cargo.toml
 /src
    |- bucket.rs
    |- lib.rs
    |- util.rs
```

The Cuckoo Filter code is quite lengthy, so we will only list the lib.rs file here. For the remaining code, please refer to the source code provided with the book.

```rust
// lib.rs
mod bucket;
mod util;

use std::fmt;
use std::cmp::max;
use std::iter::repeat;
use std::error::Error;
use std::hash::{Hash, Hasher};
use std::marker::PhantomData;
use std::collections::hash_map::DefaultHasher;
```

```rust
// Support serialization
use rand::Rng;
#[cfg(feature = "serde_support")]
use serde_derive::{Serialize, Deserialize};

use crate::util::FaI;
use crate::bucket::{Bucket, FingerPrint,
                    BUCKET_SIZE, FIGERPRINT_SIZE};

const MAX_RELOCATION: u32 = 100;
const DEFAULT_CAPACITY: usize = (1 << 20) - 1;

// Error handling
#[derive(Debug)]
enum CuckooError {
    NotEnoughSpace,
}

// add print function
impl fmt::Display for CuckooError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        f.write_str("NotEnoughSpace")
    }
}

impl Error for CuckooError {
    fn description(&self) -> &str {
        "Not enough space to save element, operation failed!"
    }
}

// Definition of cuckoo filter
struct CuckooFilter<H> {
    buckets: Box<[Bucket]>, // Bucket
    len: usize, // length
    _phantom: PhantomData<H>,
}

// add default value
impl Default for CuckooFilter<DefaultHasher> {
    fn default() -> Self {
        Self::new()
    }
}

impl CuckooFilter<DefaultHasher> {
    fn new() -> Self {
        Self::with_capacity(DEFAULT_CAPACITY)
    }
}

impl<H: Hasher + Default> CuckooFilter<H> {
```

```rust
    fn with_capacity(cap: usize) -> Self {
        let capacity = max(1, cap.next_power_of_two()
                           / BUCKET_SIZE);
        Self {
            // build a CuckooFilter with capacity buckets
            buckets: repeat(Bucket::new())
                    .take(capacity)
                    .collect::<Vec<_>>(),
                    .into_boxed_slice(),
            len: 0,
            _phantom: PhantomData,
        }
    }

    fn try_insert<T: ?Sized + Hash>(&mut self, elem: &T)
        -> Result<bool, CuckooError> {
        if self.contains(elem) {
            Ok(false)
        } else {
            self.insert(elem).map(|_| true)
        }
    }

    fn insert<T: ?Sized + Hash>(&mut self, elem: &T)
        -> Result<(), CuckooError> {
        let fai = FaI::from_data::<_, H>(elem)
        if self.put(fai.fp, fai.i1)
            || self.put(fai.fp, fai.i2) {
            return Ok(());
        }

        // collision, relocate
        let mut rng = rand::thread_rng();
        let mut i = fai.random_index(&mut rng);
        let mut fp = fai.fp;
        for _ in 0..MAX_RELOCATION {
            let other_fp;
            {
                let loc = &mut self.buckets[i % self.len]
                                   .buffer[rng.gen_range(0,
                                           BUCKET_SIZE)];
                other_fp = *loc;
                *loc = fp;
                i = FaI::get_alt_index::<H>(other_fp, i);
            }
            if self.put(other_fp, i) {
                return Ok(());
            }
            fp = other_fp;
        }
        Err(CuckooError::NotEnoughSpace)
    }
```

```rust
    // add fingerprint
    fn put(&mut self, fp: FingerPrint, i: usize) -> bool {
        if self.buckets[i % self.len].insert(fp) {
            self.len += 1;
            true
        } else {
            false
        }
    }

    fn remove(&mut self, fp: FingerPrint, i: usize) -> bool {
        if self.buckets[i % self.len].delete(fp) {
            self.len -= 1;
            true
        } else {
            false
        }
    }

    fn contains<T: ?Sized + Hash>(&self, elem: &T) -> bool {
        let FaI { fp, i1, i2 } = FaI::from_data::<_, H>(elem);
        self.buckets[i1 % self.len]
            .get_fp_index(fp)
            .or_else(|| {
                self.buckets[i2 % self.len]
                    .get_fp_index(fp)
             })
            .is_some()
    }
}
```

As we can see from the code, the Cuckoo Filter supports insertion, deletion, and querying operations.
