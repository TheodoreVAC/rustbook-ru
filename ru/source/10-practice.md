# Practices

## 10.1 Objectives

- Utilize Rust data structures and algorithms to accomplish diverse practical projects.
- Comprehend and implement data structures and algorithms employed in practical projects.

## 10.2 Edit Distance

The edit distance measures the similarity between two sequences by calculating the minimum number of operations required to transform one word, W1, into another word, W2, through insertion, deletion, or substitution. These operations are commonly used in daily editing, which is why it is called edit distance. Notably, the number of edits performed by a single operation is counted as an edit distance. There are two main types of edit distance: the Hamming distance and the Levenshtein distance. The Hamming distance only considers substitution operations, while the Levenshtein distance simultaneously takes into account insertion, deletion, and substitution operations. Readers may ponder if it is possible to develop an edit distance that involves only two of these operations.

### 10.2.1 The Hammig Distance

The Hamming distance is the number of differing symbols at the same positions between two sequences of equal length or the number of differing bits in a binary sequence. It measures the minimum number of substitution operations required to convert one sequence into another. For instance, in the figure below, converting ”trust” to ”rrost” only requires substituting two characters, resulting in a Hamming distance of 2.

![Figure 10.1: Hamming distance](images/fig-10.1.png)

*Figure 10.1: Hamming distance*

The Hamming distance is commonly used for error correction in coding. In Hamming codes [17], the algorithm for computing the distance is the Hamming distance. To simplify the code, separate algorithms are implemented for calculating the Hamming distance of numbers and characters. Computing the Hamming distance of numbers is straightforward as bitwise operations can compare numbers for similarity and difference. The code for calculating the Hamming distance of numbers is shown below.

```rust
// hamming_distance.rs

fn hamming_distance1(source: u64, target: u64) -> u32 {
    let mut count = 0;
    let mut xor = source ^ target;
    while xor != 0 {
        count += xor & 1;
        xor >>= 1;
    }
    count as u32
}

fn main() {
    let source = 1;
    let target = 2;
    let distance = hamming_distance1(source, target);
    println!("the hamming distance is {distance}");
    // the hamming distance is 2

    let source = 3;
    let target = 4;
    let distance = hamming_distance1(source, target);
    println!("the hamming distance is {distance}");
    // the hamming distance is 3
}
```

The XOR operation sets the same bits in ”source” and ”target” numbers to 0 and different bits to 1. If the result is nonzero, different bits exist. Thus, we calculate the different bits step by step from the last bit using XOR and AND operations with 1. After computing each bit, we remove it to compare the previous bits by adding a right shift operation. Note that the implementation requires manually counting the number of 1’s in the binary system. However, Rust provides a count_ones() function for counting the number of 1’s in its numbers, simplifying the above code to the following concise form.

```rust
// hamming_distance.rs

fn hamming_distance2(source: u64, target: u64) -> u32 {
    (source ^ target).count_ones()
}
```

With this foundation, we now implement the character version of the Hamming distance.

```rust
// hamming_distance.rs

fn hamming_distance_str(source: &str, target: &str) -> u32 {
    let mut count = 0;
    let mut source = source.chars();
    let mut target = target.chars();

    // Compare two strings character by character
    loop {
        match (source.next(), target.next()) {
            // Four situations may arise
            (Some(cs), Some(ct)) if cs != ct => count += 1,
```

```rust
            (Some(_), None) | (None, Some(_)) =>
                    panic!("Must have the same length"),
            (None, None) => break,
            _ => continue,
        }
    }

    count as u32
}

fn main() {
    let source = "abce";
    let target = "edcf";
    let distance = hamming_distance_str(source, target);
    println!("the hamming distance is {distance}");
    // the hamming distance is 3
}
```

The character version of the Hamming distance algorithm takes two parameters, ”source” and ”target”, and compares Unicode characters using the chars method. Unicode is preferred over ASCII because characters may include not only letters but also other characters, such as Chinese, Japanese, and Korean characters, with each character corresponding to multiple ASCII values. The ”if c1 != c2” is an additional condition check outside of the pattern matching. It only enters the matching branch if both ”source” and ”target” have the next character, and the two characters are not equal. If either character is ”None” and the other is ”Some,” it means the input strings have different lengths, and the function can return directly. If there are no more characters left, the comparison ends. In other cases, if the two characters are the same, the function continues to compare the next character. Since the Hamming distance requires calculating all characters, the time complexity is O(n), and the space complexity is O(1).

### 10.2.2 The Levenshtein Distance

The Levenshtein distance, also known as edit distance, is an algorithm used to measure the difference between two strings by representing the minimum number of edit operations required to transform one string into another, including insertion, deletion, and substitution. The concept of edit distance is easy to understand, and the operations involved are simple, making it useful for basic character correction. For instance, calculating the edit distance between the words ”sitting” and ”kitten” using the Levenshtein distance algorithm involves the following steps:

- sitting -> kitting, replace ”s” with ”k”.
- kitting -> kitteng, replace ”i” with ”e”.
- kitteng -> kitten, delete ”g”.

Since it took three operations, making the edit distance three. However, how can we prove that three is the minimum number of edit operations required? This is because there are only three types of operations that can be performed to transform one string to another: deletion, insertion, and substitution. One way to transform an empty string into a string of length s is to insert s characters, making the edit distance between the two strings equal to the length of s. For example, transforming an empty string into ”abc” requires inserting three characters, so the edit distance is 3. The figure (10.2.2) on next page illustrates the extreme cases required to transform ”sitting” into ”kitten”. It also shows that the maximum edit distance is the length of the longer string. This can be expressed mathematically using the formula: edia,b(i, j) = max(i, j)

if min(i, j) = 0 (10.1)

Where i and j are the lengths of the two strings, min(i, j) = 0 means that there is no common substring.

![Figure 10.2: Edit distances (Converting empty string to a string)](images/fig-10.2.png)

*Figure 10.2: Edit distances (Converting empty string to a string)*

Except for cases where the strings have no common substrings, the edit distance can be increased through three types of editing operations, each of which increases the edit distance by 1. Thus, we can calculate the edit distance obtained by each of the three editing operations and then take the minimum value.

edia,b(i, j) = min { edia,b(i −1, j) + 1 edia,b(i, j −1) + 1 edia,b(i −1, j −1) + 1a≠b (10.2)}

The formula edia,b(i −1, j) + 1 means that one character must be deleted to transform string a into string b, increasing the edit distance by 1. The formula edia,b(i, j −1) + 1 means that one character must be inserted to transform string a into string b, also increasing the edit distance by 1. The formula edia,b(i −1, j −1) + 1a≠b means that one character must be replaced to transform string a into string b, increasing the edit distance by 1 only if a and b are not equal. These functions are recursively defined, and their space complexity is O(3m+n−1), where m and n are the lengths of the strings. We have learned that dynamic programing is a good way to solve big problem by split it into several small ones. Therefore, dynamic programming is used to handle recursion in this case. The algorithm works by storing the edit distance in a matrix, which represents the state of the problem after various operations. The most basic case is when an empty string is transformed into a string of varying lengths, as illustrated in the figure (10.2.2) on next page. The edit distance between character k and s is calculated next, which can be divided into three cases:

- The accumulated edit distance of 1 deletion above the red cell, plus a deletion operation, results in an edit distance of 2.
- The accumulated edit distance of 1 insertion to the left of the red cell, plus an insertion operation, results in an edit distance of 2.
- The accumulated edit distance of 0 substitutions along the diagonal of the red cell, plus a substitution operation, results in an edit distance of 1.

All the values being processed in this step are from the yellow region in the diagram. Starting from the top left corner, the edit distance in the red cell is computed by taking the minimum of the three values in the yellow region and adding 1. This yields the new edit distance.

![Figure 10.3: State transition matrix](images/fig-10.3.png)

*Figure 10.3: State transition matrix*

Based on the above description and diagram, we can develop the following algorithm to calculate the edit distance between two strings.

```rust
// edit_distance.rs

use std::cmp::min;

fn edit_distance(source: &str, target: &str) -> usize {
    // Extreme case: transformation from empty string
    // to a non-empty string
    if source.is_empty() {
        return target.len();
    } else if target.is_empty() {
        return source.len();
    }

    // Establish a matrix to store process values
    let source_c = source.chars().count();
    let target_c = target.chars().count();
    let mut distance = vec![vec![0;target_c+1]; source_c+1];
    (1..=source_c).for_each(|i| {
        distance[i][0] = i;
    });
    (1..=target_c).for_each(|j| {
        distance[0][j] = j;
    })

    // Save the minimum number of steps(insert, delete, modify)
    for (i, cs) in source.chars().enumerate() {
        for (j, ct) in target.chars().enumerate() {
```

```rust
            let ins = distance[i+1][j] + 1;
            let del = distance[i][j+1] + 1;
            let sub = distance[i][j] + (cs != ct) as usize;
            distance[i+1][j+1] = min(min(ins, del), sub);
        }
    }

    // Return the value in the last row and last column
    *distance.last().and_then(|d| d.last()).unwrap()
}
fn main() {
    let source = "abce";
    let target = "adcf";
    let dist = edit_distance(source, target);
    println!("distance between {source} and {target}: {dist}");
    // distance between abce and adcf: 2

    let source = "bdfc";
    let target = "adcf";
    let dist = edit_distance(source, target);
    println!("distance between {source} and {target}: {dist}");
    // distance between bdfc and adcf: 3
}
```

To select the three values that need to be calculated, we can gradually move the yellow area. Once we have these values, we take the minimum calculated result and fill it into the lower right corner of the current yellow area. This new value represents the edit distance for that particular section. The final calculation result can be seen in the figure below.

g s n t t i i 5 7 0 3 6 1 2 4 5 7 1 1 2 3 4 6 k 5 3 6 2 2 1 2 4 i t 3 3 3 5 2 1 2 4 t 3 3 4 4 2 1 2 4 e 5 5 3 3 4 2 2 4 n 5 6 6 3 3 3 4 2

The entire edit distance state transition matrix can be used to calculate the value in the last row and last column, which represents the overall edit distance. It is important to note that the matrix is two-

dimensional and requires careful use of subscripts. One approach is to place each row of the matrix in an array, forming a large array with m*n values but smaller dimensions. However, this approach can result in a lot of intermediate values that waste memory. To optimize the algorithm, we can repeatedly use a single array to calculate and save values. This approach reduces the matrix to an array with a length of m + 1 or n + 1. The optimized code for the edit distance algorithm is shown below.

```rust
// edit_distance.rs

fn edit_distance2(source: &str, target: &str) -> usize {
    if source.is_empty() {
        return target.len();
    } else if target.is_empty() {
        return source.len();
    }

    // The "distances" variable stores the edit distances
    // to various strings
    let target_c = target.chars().count();
    let mut distances = (0..=target_c).collect::<Vec<_>>();
    for (i, cs) in source.chars().enumerate() {
        let mut substt = i;
        distances[0] = substt + 1;
        // Combinations are continuously calculated
        // to obtain the distances
        for (j, ct) in target.chars().enumerate() {
            let dist = min(
                        min(distances[j],distances[j+1]) + 1,
                        substt + (cs != ct) as usize);
            substt = distances[j+1];
            distances[j+1] = dist;
        }
    }

    // The last distance value is the answer
    distances.pop().unwrap()
}

fn main() {
    let source = "abced";
    let target = "adcf";
    let dist = edit_distance2(source, target);
    println!("distance between {source} and {target}: {dist}");
    // distance between abced and adcf: 3
}
```

The optimized edit distance algorithm has a worst-case time complexity of O(mn) and a worst-case space complexity that has been reduced from O(mn) for the matrix to O(min(m, n)) for the array. This represents a significant improvement. Microsoft Word software uses a spell check function that does not rely on edit distance. Instead, it uses a hash table to store commonly used words, allowing it to quickly look up each word as it is typed. If the word is not found in the hash table, an error is reported. Because hash tables are very fast, and several hundred thousand words only require a few megabytes of memory, this approach is highly efficient.

## 10.3 Trie

Trie, also known as a radix tree or prefix tree, is a tree data structure used to search for words or prefixes. It has a wide range of applications, including auto-completion, spell checking, typing prediction, and more. While balanced trees and hash tables can also be used to search for words, they cannot quickly find all words with the same prefix or enumerate all stored words in lexicographical order. Hash tables can find a word in O(1) time, but as the number of words grows, the hash table may become too large and increase the time complexity to O(n) due to collisions. In contrast, Trie uses less space to store multiple words with the same prefix, and its time complexity is only O(m), where m is the length of the word. The time complexity of searching for a word in a balanced tree is O(mlog(n)). The structure of Trie is shown in the figure below. Storing words only requires processing 26 letters, and words with the same prefix share the same prefix, which saves storage space. For example, ”apple” and ”appeal” share ”app,” and ”boom” and ”box” share ”bo.”

root a b p u m o y p o x t d e m l e a l

To implement Trie, we first need to abstract the node, similar to the node in the above figure. The node stores the reference to its child nodes and the state of the current node. The state indicates whether this node is the end of a word (”end”), which can be used to determine whether the word ends when searching. In addition, the root node is the entrance to Trie and used to represent the entire Trie.

```rust
// trie.rs

// Definition of Trie
#[derive(Default, Debug)]
struct Trie {
    root: Node,
}

// Definition of Trie node
#[derive(Default)]
struct Node {
    end: bool,
    children: [Option<Box<Node>>; 26], // List of letter nodes
}

impl Trie {
```

```rust
    fn new() -> Self {
        Self::default()
    }

    // Insert word
    fn insert(&mut self, word: &str) {
        let mut node = &mut self.root;

        // Insert character by character
        for c in word.as_bytes() {
            let index = (c - b'a') as usize;
            let next = &mut node.children[index];
            node = next.get_or_insert_with(
                        Box::<Node>::default);
        }

        node.end = true;
    }

    fn contains(&self, word: &str) -> bool {
        self.word_node(word)
            .map_or(false, |n| n.end)
    }

    // Check if there exists a word with a certain prefix
    fn start_with(&self, prefix: &str) -> bool {
        self.word_node(prefix)
            .is_some()
    }

    // Prefix string (wps: word_prefix_string)
    fn word_node(&self, wps: &str) -> Option<&Node> {
        let mut node = &self.root;
        for c in wps.as_bytes() {
            let index = (c - b'a') as usize;
            match &node.children[index] {
                None => return None,
                Some(next) => node = next.as_ref(),
            }
        }

        Some(node)
    }
}

fn main() {
    let mut trie = Trie::new();
    trie.insert("box");
    trie.insert("insert");
    trie.insert("apple");
    trie.insert("appeal");
```

```rust
    let res1 = trie.contains("apple");
    let res2 = trie.contains("apples");
    let res3 = trie.start_with("ins");
    let res4 = trie.start_with("ina");
    let res5 = trie.word_node("box");

    println!("word 'apple' in Trie: {res1}");
    println!("word 'apples' in Trie: {res2}");
    println!("prefix 'ins' in Trie: {res3}");
    println!("prefix 'ina' in Trie: {res4}");
    println!("{:?}", res5);
}
```

The following are outputs after execution.

```text
word 'apple' in Trie: true
word 'apples' in Trie: false
prefix 'ins' in Trie: true
prefix 'ina' in Trie: false
Some(Node { end: true, children: [None, ..., None] })
```

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

## 10.5 Least Recently Used(LRU) Algorithm

The cache eviction algorithm, or page replacement algorithm, is a commonly used memory management technique in virtual paging storage and data caching. Its principle is based on the assumption that if data has been recently accessed, it is more likely to be accessed again in the future. Therefore, data blocks that are in memory but not used will be removed based on which data is the least recently used, freeing up space and saving memory. LRU (Least Recently Used) is a popular eviction algorithm used to eliminate data based on the access record of data when storage is limited. Assuming a hash-linked list is used to cache user information with a capacity of 5, and currently caching 4 user information, as shown in the figure.

001 002 003 004 Info a Info b Info c Info d

When a client queries user 5, the data is not in the hash-linked list, so it needs to be read from the database and inserted into the cache. At this point, the rightmost node of the linked list represents the

most recently accessed user 5, and the leftmost represents the least recently accessed user 1.

001 002 003 004 005 Info a Info b Info c Info d Info e

Next, when another client accesses user 2, the data is found in the hash-linked list, so user 2 is simply removed from its current position and reinserted into the rightmost of the linked list.

001 003 004 005 Info a Info c Info d Info e 002 Info b

After these accesses, the hash-linked list looks like the figure shown.

001 003 004 005 002 Info a Info c Info d Info e Info b

Later, a client accesses user 6, but the data is not in the cache, so it also needs to be inserted.

001 003 004 005 002 006 Info a Info c Info d Info e Info b Info f

However, since the cache has reached its limit, the least recently accessed data, user 1, needs to be deleted first. Then, user 6 can be inserted at the rightmost end of the hash-linked list.

003 004 005 002 006 Info c Info d Info e Info b Info f

The LRU algorithm is a common cache eviction algorithm that frees up memory by removing the least recently used data. To implement this algorithm, we need to define the data structure and operations abstracted from the graph. This includes managing keys, entries, and front and back pointers. The necessary operation functions include insert, remove, contains, and auxiliary functions.

```rust
// lru.rs
use std::collections::HashMap;

// Definition for entry of LRU
struct Entry<K, V> {
    key: K,
    val: Option<V>,
```

```rust
    next: Option<usize>,
    prev: Option<usize>,
}

struct LRUCache<K, V> {
    cap: usize,
    head: Option<usize>,
    tail: Option<usize>,
    map: HashMap<K, usize>,
    entries: Vec<Entry<K, V>>,
}
```

To store the keys, we will use a HashMap, and a Vec to store the entries. The head and tail pointers can be simplified to the index of the Vec. To customize the cache capacity, we can implement a with_capacity function, with new setting the capacity to 100 by default.

```rust
// lru.rs
use std::hash::Hash;

const CACHE_SIZE: usize = 100;

impl<K: Clone + Hash + Eq, V> LRUCache<K, V> {
    fn new() -> Self {
        Self::with_capacity(CACHE_SIZE)
    }

    fn len(&self) -> usize {
        self.map.len()
    }

    fn is_empty(&self) -> bool {
        self.map.is_empty()
    }

    fn is_full(&self) -> bool {
        self.map.len() == self.cap
    }

    fn with_capacity(cap: usize) -> Self {
        LRUCache {
            cap: cap,
            head: None,
            tail: None,
            map: HashMap::with_capacity(cap),
            entries: Vec::with_capacity(cap),
        }
    }
}
```

When inserting data, if the key already exists, the value will be updated directly and the original value will be returned. If the inserted value does not exist, the returned value should be None, hence the use of Option as the return type. The access method is used to remove the original value and update the value, and ensure_room is used to remove the least recently used data when the cache reaches capacity.

```rust
// lru.rs

impl<K: Clone + Hash + Eq, V> LRUCache<K, V> {
    fn insert(&mut self, key: K, val: V) -> Option<V> {
        if self.map.contains_key(&key) {
            // Update if key exists
            self.access(&key);
            let entry = &mut self.entries[self.head.unwrap()];
            let old_val = entry.val.take();
            entry.val = Some(val);
            old_val
        } else {
            // insert if key not exists
            self.ensure_room();

            // Update the original head pointer
            let index = self.entries.len();
            self.head.map(|e| {
                self.entries[e].prev = Some(index);
            });

            // The new head node
            self.entries.push(Entry {
                key: key.clone(),
                val: Some(val),
                prev: None,
                next: self.head,
            });

            self.head = Some(index);
            self.tail = self.tail.or(self.head);
            self.map.insert(key, index);

            None
        }
    }

    fn get(&mut self, key: &K) -> Option<&V> {
        if self.contains(key) { self.access(key); }

        let entries = &self.entries;
        self.map.get(key).and_then(move |&i| {
            entries[i].val.as_ref()
        })
    }

    fn get_mut(&mut self, key: &K) -> Option<&mut V> {
        if self.contains(key) { self.access(key); }

        let entries = &mut self.entries;
        self.map.get(key).and_then(move |&i| {
```

```rust
            entries[i].val.as_mut()
        })
    }

    fn contains(&mut self, key: &K) -> bool {
        self.map.contains_key(key)
    }

    // Ensure there is enough capacity, remove the
    // least recently used item if full
    fn ensure_room(&mut self) {
        if self.cap == self.len() {
            self.remove_tail();
        }
    }

    fn remove_tail(&mut self) {
        if let Some(index) = self.tail {
            self.remove_from_list(index);
            let key = &self.entries[index].key;
            self.map.remove(key);
        }
        if self.tail.is_none() {
            self.head = None;
        }
    }

    // Get the value of a key, remove the
    // old position and add to the head
    fn access(&mut self, key: &K) {
        let i = *self.map.get(key).unwrap();
        self.remove_from_list(i);
        self.head = Some(i);
    }

    fn remove(&mut self, key: &K) -> Option<V> {
        self.map.remove(&key).map(|index| {
                self.remove_from_list(index);
                self.entries[index].val.take().unwrap()
            })
    }

    fn remove_from_list(&mut self, i: usize) {
        let (prev, next) = {
            let entry = self.entries.get_mut(i).unwrap();
            (entry.prev, entry.next)
        };

        match (prev, next) {
            // The data item is in the middle of the cache
            (Some(j), Some(k)) => {
                let head = &mut self.entries[j];
```

```rust
                head.next = next;
                let next = &mut self.entries[k];
                next.prev = prev;
            },
            // The data item is at the end of the cache
            (Some(j), None) => {
                let head = &mut self.entries[j];
                head.next = None;
                self.tail = prev;
            },
            // The data item is at the head of the cache
            _ => {
                if self.len() > 1 {
                    let head = &mut self.entries[0];
                    head.next = None;
                    let next = &mut self.entries[1];
                    next.prev = None;
                }
            },
        }
    }
}
```

The following are use example of LRU.

```rust
// lru.rs

fn main() {
    let mut cache = LRUCache::with_capacity(2);
    cache.insert("foo", 1);
    cache.insert("bar", 2);
    cache.insert("baz", 3);
    cache.insert("tik", 4);
    cache.insert("tok", 5);

    assert!(!cache.contains(&"foo"));
    assert!(!cache.contains(&"bar"));
    assert!(cache.contains(&"baz"));
    assert!(cache.contains(&"tik"));

    cache.insert("qux", 6);
    assert!(cache.contains(&"qux"));
}
```

## 10.6 Consistent Hashing

The Consistent Hashing algorithm was initially proposed by Karger et al. of MIT to address hotspot issues in distributed caching. However, after years of development, it has become a widely applied algorithm. To understand its application, let’s consider caching images in Redis. A single Redis instance can handle small data volumes and low access rates, and a master-slave configuration may be sufficient.

However, when data volumes grow, and access rates increase, a cluster must be created to distribute data across multiple machines. For example, if there are 5 machines, the position index of an image would be index = hash(key) % 5, where key is an index related to the image. However, adding or removing machines changes N, and previously calculated indices will become invalid. This is where consistent hashing comes in. It creates a circle that ranges from 0 to 232 −1, mapping data to a position on the circle.

232 −1 0 Node3 Node1 Node2

To achieve caching, data must be added to a specific segment of the circle based on its hash value. The corresponding node located just clockwise from the segment will store the data.

232 −1 0 Node3 Node1 Node2

Suppose Node3 fails, causing data between Node2 and Node3 to be transferred to Node1.

232 −1 0 Node1 Node2

When a new machine, Node4, is added, the data originally stored on Node3 will now be stored on Node4.

232 −1 0 Node3 Node1 Node4 Node2

The Consistent Hashing algorithm is fault-tolerant and scalable since it only relocates a small portion of the data when nodes are added or removed. This feature enables the algorithm to achieve consistency. To implement Consistent Hashing, a Ring is needed to store nodes representing machines.

```rust
// conshash.rs

use std::fmt::Debug;
use std::string::ToString;
use std::hash::{Hash, Hasher};
use std::collections::{BTreeMap, hash_map::DefaultHasher};

// Ring node definition, used for storing the host, ip and port
#[derive(Clone, Debug)]
struct Node {
    host: &'static str,
    ip: &'static str,
    port: u16,
}

// implement a to_string function
impl ToString for Node {
    fn to_string(&self) -> String {
        self.ip.to_string() + &self.port.to_string()
    }
}

// Definition for the Ring
struct Ring<T: Clone + ToString + Debug> {
    replicas: usize, // partition number
    ring: BTreeMap<u64, T>, // store data
}
```

Replicas in the Ring are utilized to avoid node clustering and ensure even data distribution across nodes. Multiple virtual nodes can be created for each node to solve the node clustering problem. The default hash calculator provided by the standard library, with a default of 10 nodes, can be used for hash calculation, or custom nodes can be created. For the Consistent Hashing algorithm, at least node insertion, node deletion, and query functions must be supported. Additionally, batch versions of insertion and deletion can be implemented for batch processing.

```rust
// conshash.rs

const DEFAULT_REPLICAS: usize = 10;

// Hash calculation function
fn hash<T: Hash>(val: &T) -> u64 {
    let mut hasher = DefaultHasher::new();
    val.hash(&mut hasher);

    hasher.finish()
}

impl<T> Ring<T> where T: Clone + ToString + Debug {
    fn new() -> Self {
        Self::with_capacity(DEFAULT_REPLICAS)
    }

    // new with a replicas parameter
    fn with_capacity(replicas: usize) -> Self {
        Ring {
            replicas: replicas,
            ring: BTreeMap::new()
        }
    }

    // Batch insertion of nodes
    fn add_multi(&mut self, nodes: &[T]) {
        if !nodes.is_empty() {
            for node in nodes.iter() {
                self.add(node);
            }
        }
    }

    fn add(&mut self, node: &T) {
        for i in 0..self.replicas {
            let key = hash(&(node.to_string()
                                + &i.to_string()));
            self.ring.insert(key, node.clone());
        }
    }

    // Batch deletion of nodes
    fn remove_multi(&mut self, nodes: &[T]) {
        if !nodes.is_empty() {
            for node in nodes.iter() {
                self.remove(node);
            }
        }
    }
```

```rust
    fn remove(&mut self, node: &T) {
        // assertion to ensure that the node exists
        assert!(!self.ring.is_empty());

        for i in 0..self.replicas {
            let key = hash(&(node.to_string()
                                + &i.to_string()));
            self.ring.remove(&key);
        }
    }

    // Get nodes
    fn get(&self, key: u64) -> Option<&T> {
        if self.ring.is_empty() {
            return None;
        }

        let mut keys = self.ring.keys();
        keys.find(|&k| k >= &key)
            .and_then(|k| self.ring.get(k))
            .or(keys.nth(0).and_then(|x| self.ring.get(x)))
    }
}

fn main() {
    let replica = 3;
    let mut ring = Ring::with_capacity(replica);
    let node = Node{
        host:"localhost",
        ip:"127.0.0.1",
        port:23
    };
    ring.add(&node);

    for i in 0..replica {
        let key = hash(&(node.to_string() + &i.to_string()));
        let res = ring.get(key);
        assert_eq!(node.host, res.unwrap().host);
    }

    println!("{:?}", &node);
    ring.remove(&node);
    // Node { host: "localhost", ip: "127.0.0.1", port: 23 }
}
```

## 10.7 Base58 Encode and Decode

Base58 is an encoding algorithm that only uses certain characters from the Base64 table, removing the characters highlighted in red. It was originally used to represent Bitcoin wallet addresses and was invented by Satoshi Nakamoto.

**Table 10.2: Base 64 encoding characters**

| ASCII | Char | ASCII | Char | ASCII | Char | ASCII | Char | ASCII | Char |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 13 | D | 26 | Q | 39 | d | 52 | q |
| 1 | 1 | 14 | E | 27 | R | 40 | e | 53 | r |
| 2 | 2 | 15 | F | 28 | S | 41 | f | 54 | s |
| 3 | 3 | 16 | G | 29 | T | 42 | g | 55 | t |
| 4 | 4 | 17 | H | 30 | U | 43 | h | 56 | u |
| 5 | 5 | 18 | I | 31 | V | 44 | i | 57 | v |
| 6 | 6 | 19 | J | 32 | W | 45 | j | 58 | w |
| 7 | 7 | 20 | K | 33 | X | 46 | k | 59 | x |
| 8 | 8 | 21 | L | 34 | Y | 47 | l | 60 | y |
| 9 | 9 | 22 | M | 35 | Z | 48 | m | 61 | z |
| 10 | A | 23 | N | 36 | a | 49 | n | 62 | + |
| 11 | B | 24 | O | 37 | b | 50 | o | 63 | / |
| 12 | C | 25 | P | 38 | c | 51 | p |  |  |

To avoid ambiguous characters, Base58 removes 0 (zero), O (capital O), I (capital i), l (lowercase L), plus sign (+), and slash (/) from the Base64 table. The remaining 58 characters are used as encoding characters. These characters are easily distinguishable and also prevent problems with line breaks when copying the code. Base58 encoding is essentially a conversion from a large number base. First, the character is converted to ASCII and then to decimal, followed by 58 base conversion. Finally, the corresponding character is selected from the encoding table to form the Base58 encoding string. However, due to the need for base conversion, the efficiency of Base58 encoding is relatively low. The encoding algorithm (10.1) illustrates the encoding principle.

Algorithm 10.1: Base58 Encoding Algorithm Data: Original string s

Result: Encoded string b58_str

1 Initialize an empty string b58_str to store the result. 2 for c ∈s do Convert byte c in s to ASCII value (256 base). 3 Convert 256 base number to decimal. 4 Convert decimal number to 58 base number. 5 Convert 58 base number to corresponding character according to the Base58 character 6 table. Append the resulting character to b58_str. 7 8 end 9 Return the encoded string b58_str.

Decoding is the reverse process of encoding and involves converting from a large number base. The characters in the Base58 string are first converted to ASCII values, then to 10 decimal values, followed by conversion to 256 decimal values, and finally to ASCII characters. The decoding process is described in detail in Algorithm (10.2).

Algorithm 10.2: Base58 Decoding Algorithm Data: Encoded string b58

Result: Decoded string new_str

1 Initialize an empty string new_str to store the result 2 for c ∈b58 do Convert byte c in b58 to ASCII value (58 base) 3 Convert 58 base number to 10 decimal value 4 Convert 10 decimal value to 256 decimal value 5 Convert 256 decimal value to corresponding ASCII character 6 Append the resulting character to new_str 7 8 end 9 Return the decoded string new_str

Encoding and decoding are essentially two-way string transformations between different spaces, similar to a mapping in the encoding space. To implement a Base58 encoder and decoder, we first prepare the encoding characters ALPHABET and the encoding conversion table DIGITS_MAP. Additionally, we define the maximum conversion base 58 and substitute 1 for the leading 0 as constants. Using constants for operations is preferable to using magic numbers directly, as it improves code readability.

```text
// base58.rs

// Conversion base 58
const BIG_RADIX: u32 = 58;

// Substitute 1 for the leading 0
const ALPHABET_INDEX_0: char = '1';

// Base58 encoding characters
const ALPHABET: &[u8;58] = b"123456789ABCDEFGHJKLMNPQRSTUVWXYZ
abcdefghijkmnopqrstuvwxyz";

// Mapping relationship between the bases
const DIGITS_MAP: &'static [u8] = &[
  255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
  255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
  255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
  255, 0, 1, 2, 3, 4, 5, 6, 7,
     8,255,255,255,255,255,255, 255, 9, 10, 11, 12, 13, 14, 15, 16,255, 17, 18, 19, 20,
     21,255, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
      32,255,255,255,255,255, 255, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43,255, 44, 45,
     46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56,
      57,255,255,255,255,255, ];
```

To handle potential errors during encoding and decoding, we have implemented a custom error type for Base58 encoding to manage illegal characters, length errors, and other cases. Two traits, Encoder and Decoder, have been created for encoding and decoding, respectively. Encoder and Decoder contain the methods encode_to_base58 and decode_from_base58, respectively.

```rust
// base58.rs

// Decoding error type
#[derive(Debug, PartialEq)]
pub enum DecodeError {
    Invalid,
    InvalidLength,
    InvalidCharacter(char, usize),
}

// Encoding and decoding traits
pub trait Encoder {
    // Encoding method
    fn encode_to_base58(&self) -> String;
}

pub trait Decoder {
    // Decoding method
    fn decode_from_base58(&self) ->Result<String,DecodeError>;
}
```

In the next step, we will implement the methods that correspond to the two traits mentioned earlier. Although these traits are implemented for strings, it is better to use u8 for internal calculations since the characters in the string may contain multiple u8 values.

```rust
// base58.rs

// Implement Base58 encoding
impl Encoder for str {
    fn encode_to_base58(&self) -> String {
        // Convert to bytes for processing
        let str_u8 = self.as_bytes();
        // Count the number of leading zeros
        let zero_count = str_u8.iter()
                               .take_while(|&&x| x == 0)
                               .count();
        // Space required after conversion is log(256)/log(58),
        // which is approximately 1.38 times the original data.
        // We don't need leading zeros
        let size = (str_u8.len() - zero_count) * 138 / 100 + 1;
        // Convert characters from one base to another
        let mut i = zero_count;
        let mut high = size - 1;
        let mut buffer = vec![0u8; size];
        while i < str_u8.len() {
            // j is the decreasing index, corresponding to
            // counting from the back
            let mut j = size - 1;
```

```rust
            // carry is the character read from the front
            let mut carry = str_u8[i] as u32;

            // Store the converted data from back to front
            // in turn
            while j > high || carry != 0 {
                carry += 256 * buffer[j] as u32;
                buffer[j] = (carry % BIG_RADIX) as u8;
                carry /= BIG_RADIX;

                if j > 0 {
                    j -= 1;
                }
            }
            i += 1;
            high = j;
        }

        // Handle multiple leading zeros
        let mut b58_str = String::new();
        for _ in 0..zero_count {
            b58_str.push(ALPHABET_INDEX_0);
        }

        // Get the encoded characters and concatenate
        // them into a string
        let mut j = buffer.iter()
                          .take_while(|&&x| x == 0)
                          .count();
        while j < size {
            b58_str.push(ALPHABET[buffer[j] as usize] as char);
            j += 1;
        }

        // Return the encoded string
        b58_str
    }
}
```

Decoding is the process of converting Base58 encoded data back to its original form, which is essentially a conversion between numeral systems. The specific implementation of the decoding method is as follows:

```rust
// base58.rs

// Implement Base58 decoding
impl Decoder for str {
    fn decode_from_base58(&self) -> Result<String,DecodeError>
{
        // Store conversion characters
        let mut bin = [0u8; 132];
        let mut out = [0u32; (132 + 3) / 4];
```

```rust
        // Number of remaining bits after processing data
        // in units of 4
        let bytes_left = (bin.len() % 4) as u8;
        let zero_mask = match bytes_left {
            0 => 0u32,
            _ => 0xffffffff << (bytes_left * 8),
        };

        // Count leading zeros
        let zero_count = self.chars()
                        .take_while(|&x| x == ALPHABET_INDEX_0)
                        .count();

        let mut i = zero_count;
        let b58: Vec<u8> = self.bytes().collect();
        while i < self.len() {
            // Invalid characters
            if (b58[i] & 0x80) != 0 {
                return Err(DecodeError::InvalidCharacter(
                            b58[i] as char, i));
            }
            if DIGITS_MAP[b58[i] as usize] == 255 {
                return Err(DecodeError::InvalidCharacter(
                            b58[i] as char, i));
            }

            // Number system conversion
            let mut j = out.len();
            let mut c = DIGITS_MAP[b58[i] as usize] as u64;
            while j != 0 {
                j -= 1;
                let t = out[j] as u64 * (BIG_RADIX as u64) + c;
                c = (t & 0x3f00000000) >> 32;
                out[j] = (t & 0xffffffff) as u32;
            }

            // Data is too long
            if c != 0 {
                return Err(DecodeError::InvalidLength);
            }

            if (out[0] & zero_mask) != 0 {
                return Err(DecodeError::InvalidLength);
            }

            i += 1;
        }

        // Handle remaining bits
        let mut i = 1;
        let mut j = 0;
```

```rust
        bin[0] = match bytes_left {
            3 => ((out[0] & 0xff0000) >> 16) as u8,
            2 => ((out[0] & 0xff00) >> 8) as u8,
            1 => {
                j = 1;
                (out[0] & 0xff) as u8
            },
            _ => {
                i = 0;
                bin[0]
            }
        };

        // Process data in units of 4 and
        // use bit shifting for division
        while j < out.len() {
            bin[i] = ((out[j] >> 0x18) & 0xff) as u8;
            bin[i + 1] = ((out[j] >> 0x10) & 0xff) as u8;
            bin[i + 2] = ((out[j] >> 8) & 0xff) as u8;
            bin[i + 3] = ((out[j] >> 0) & 0xff) as u8;
            i += 4;
            j += 1;
        }

        // Get number of leading zeros
        let leading_zeros = bin.iter()
                               .take_while(|&&x| x == 0)
                               .count();

        // Get decoded string
        let new_str = String::from_utf8(
                        bin[leading_zeros - zero_count..]
                        .to_vec());

        // Return valid result
        match new_str {
            Ok(res) => Ok(res),
            Err(_) => Err(DecodeError::Invalid),
        }
    }
}

fn main() {
    println!("{:#?}","abc".encode_to_base58());
    println!("{:#?}","ZiCa".decode_from_base58().unwrap());

    println!("{:#?}","loverust".encode_to_base58());
    println!("{:#?}","K8xdoM2VJtK".decode_from_base58());

    println!("{:#?}","iloveyou".encode_to_base58());
    println!("{:#?}","Jdjxs3pmuK2".decode_from_base58());
}
```

The following are the results after Base58 encoding and decoding.

```text
"ZiCa"
"abc"
"K8xdoM2VJtK"
Ok(
    "loverust",
)
"Jdjxs3pmuK2"
Ok(
    "iloveyou",
)
```

With the completion of the entire Base58 algorithm, similar methods can be used to implement encoding and decoding algorithms for other encoding schemes of interest, such as Base32, Base36, Base62, Base64, Base85, Base92, and so on. In Chapter 1, we used Base64 to create a password generator, but it can also be replaced with Base58. I have already made the replacement and included the specific code in the corresponding repository for this chapter.

## 10.8 Blockchain

Blockchain is a digital technology that has gained significant attention in recent years. This attention has been due, in part, to the rise in the price of Bitcoin, which is closely tied to blockchain technology, as well as other related concepts such as Ethereum, virtual currencies, and the digital economy. The endorsement of virtual currencies by influential figures such as Tesla CEO Elon Musk has further fueled the development of the field. Additionally, governments around the world have been formulating policies related to blockchain technology, adding to the momentum of the industry. Ultimately, blockchain technology is a tool closely tied to economic development and the trade of commodities. Online transactions rely heavily on financial institutions as third-party intermediaries to process payment information. However, this credit-based model has inherent weaknesses that limit the feasibility of small daily payment transactions, increase the cost of transactions, and prevent completely irreversible transactions due to the involvement of financial intermediaries to coordinate disputes. This limits the potential of internet trade as both parties in a transaction must trust each other, and merchants must guard against potential fraud. In contrast, physical cash transactions do not require third-party intermediaries and thus do not face such limitations. To address these issues, we need an electronic payment system based on cryptographic principles that enables two parties to make payments directly without intermediaries. This eliminates the possibility of rolling back payment transactions, protecting sellers from fraud. We propose a method for generating electronic transaction proofs using a peer-to-peer distributed timestamp server that records transactions in chronological order. The system is secure as long as the total computing power controlled by honest nodes exceeds that of cooperating attackers. The passage above is the introduction to the Bitcoin whitepaper(Bitcoin: A Peer-to-Peer Electronic Cash System [19]), written by Satoshi Nakamoto, the inventor of Bitcoin. It outlines the reason for the invention of Bitcoin, which was to address the practical problem of the global financial crisis of 2008, inflation, and its impact on various countries. Nakamoto was dissatisfied with the existing financial environment and used their professional knowledge to invent the blockchain technology to address this problem.

### 10.8.1 The Principles of Blockchain and Bitcoin

Blockchain and Bitcoin are often mentioned together in media reports, but their relationship is not always clear. Blockchain technology is a new decentralized infrastructure and computing paradigm that

uses a chain data structure to store and verify data, distributed node consensus algorithms to generate and update data, cryptography to ensure data security, and smart contracts to program and operate data. In contrast, Bitcoin is a type of digital currency that was invented using blockchain technology. To put it simply, blockchain is a decentralized distributed ledger, where data is not only stored on each node but replicated and shared across the entire network. Blockchain is a ledger that records transactions and consumes a lot of resources to do so. As transactions are recorded, rewards and transaction fees are generated in the form of digital currency, which is used to maintain the system’s operation. Bitcoin is the first digital currency created using blockchain technology and serves as a guarantee of transactions and a type of incentive. In summary, blockchain is a distributed transaction medium, and Bitcoin is a type of digital currency that serves as a guarantee of transactions and an incentive. Blockchain itself consists of components such as blocks, blockchains, transactions, accounts, miners, transaction fees, and rewards. To implement a blockchain system, one must start by implementing these basic components.

### 10.8.2 A Primary Blockchain

The blockchain structure consists of a block header, block body, and block hash. The header contains the hash of the previous block (pre_hash), the current block transaction hash value (tx_hash), and the block packaging time (time). The block body includes all transaction data (transactions), and the block hash (hash) is calculated from the block header and block body. The block and blockchain structures are shown in the following figure.

pre hash|tx hash|time pre hash|tx hash|time pre hash|tx hash|time transaction 1 transaction 1 transaction 1 transaction 2 transaction 2 transaction 2 transaction 3 transaction 3 transaction 3 ... ... ... hash hash hash

Hash values play a vital role in the blockchain, as evident from the structure discussed above. Thus, the initial step is to compute the hash value, and serialization of the block structure is a more efficient approach. The basic blockchain’s first function is to perform serialization and hash value computation, demonstrated in the following code. To handle blocks with varying transaction numbers, we employ the ”Sized” trait. The serialization process utilizes the ”bincode” library, while the ”crypto’s Sha3” library computes the hash. For better readability, we convert all hashes to strings. The serialized data is of type ”&[u8]”, and ”hash_str” retrieves the data and returns it as a string.

```rust
// serializer.rs

use bincode;
use serde::Serialize;
use crypto::digest::Digest;
use crypto::sha3::Sha3;

// Data serialization
pub fn serialize<T: ?Sized>(value: &T) -> Vec<u8>
    where T: Serialize
{
    bincode::serialize(value).unwrap()
}

// calculate the hash value and return it as a string
pub fn hash_str(value: &[u8]) -> String {
```

```rust
    let mut hasher = Sha3::sha3_256();
    hasher.input(value);

    hasher.result_str()
}
```

The hash computation function can calculate the hash values for the block’s hash, pre_hash, and tx_hash, while the time can be obtained by capturing the block’s generation time. Initially, we simplify the problem by using strings to represent transactions and place them in a Vec to simulate multiple transactions. In Rust, we can utilize the struct to represent blocks and block headers.

```rust
// block.rs

// Block structure
pub struct Block {
    pub header: BlockHeader,
    pub tranxs: String,
    pub hash: String,
}

// Block header structure
pub struct BlockHeader {
    pub time: i64,
    pub pre_hash: String,
    pub txs_hash: String,
}
```

Since hash values are crucial in the blockchain, the first step is to calculate the hash. To achieve this, we serialize the block structure before computing the hash value for efficiency purposes.

```rust
// block.rs

use std::thread;
use std::time::Duration;
use chrono::prelude::*;
use utils::serializer::{serialize, hash_str};
use serde::Serialize;

// Definition of block header
#[derive(Serialize, Debug, PartialEq, Eq)]
pub struct BlockHeader {
    pub time: i64,
    pub pre_hash: String,
    pub txs_hash: String,
}

// Definition of block
#[derive(Debug)]
pub struct Block {
    pub header: BlockHeader,
    pub tranxs: String,
    pub hash: String,
}
```

```rust
impl Block {
    pub fn new(txs: String, pre_hash: String) -> Self {
        // Introduce a 3-second delay for mining
        println!("Start mining .... ");
        thread::sleep(Duration::from_secs(3));

        // Prepare timestamp and calculate transaction hash
        let time = Utc::now().timestamp();
        let txs_ser = serialize(&txs);
        let txs_hash = hash_str(&txs_ser);

        let mut block = Block {
            header: BlockHeader {
                time: time,
                txs_hash: txs_hash,
                pre_hash: pre_hash,
            },
            tranxs: txs,
            hash: "".to_string(),
        };

        block.set_hash();
        println!("Produce a new block!\n");

        block
    }

    // Calculate and set block hash value
    fn set_hash(&mut self) {
        let header = serialize(&(self.header));
        self.hash = hash_str(&header);
    }
}
```

To form a blockchain, we must link the created blocks together, which can be accomplished using a Vec to store multiple blocks. The system should enable the generation of the first block (genesis block) and adding new blocks to the chain. Since the genesis block does not have a pre_hash, it needs to be set manually. We will utilize the base64 value of ”Bitcoin hit $60000” as the pre_hash for the genesis block. Lastly, we will require a function to create a new block and update its hash value.

```rust
// blockchain.rs
use crate::block::Block;

// Genesis block pre_hash
const PRE_HASH: &str = "22caaf24ef0aea3522c13d133912d2b7
                        22caaf24ef0aea3522c13d133912d2b7";
pub struct BlockChain {
    pub blocks: Vec<Block>,
}

impl BlockChain {
    pub fn new() -> Self {
```

```rust
        BlockChain { blocks: vec![Self::genesis_block()] }
    }

    // Generate the genesis block
    fn genesis_block() -> Block {
        Block::new("genesis block".to_string(),PRE_HASH.
           to_string()) }

    // Add blocks to form a blockchain
    pub fn add_block(&mut self, data: String) {
        // Get the hash value of the previous block
        let pre_block = &self.blocks[self.blocks.len() - 1];
        let pre_hash = pre_block.hash.clone();
        // Build a new block and add it to the chain
        let new_block = Block::new(data, pre_hash);
        self.blocks.push(new_block);
    }

    // Print block information
    pub fn block_info(&self) {
        for b in self.blocks.iter() { println!("{:#?}", b); }
    }
}
```

To execute a blockchain system, we must generate transactions to create blocks. In the code below, the string ”tx” represents a transaction, and information is printed after the transaction has been packed and finalized.

```rust
// main.rs
use core::blockchain::BlockChain as BC;

fn main() {
    println!("----------------Mine Info-------------------");

    let mut bc = BC::new();
    let tx = "0xabcd -> 0xabce: 5 btc".to_string();
    bc.add_block(tx);
    let tx = "0xabcd -> 0xabcf: 2.5 btc".to_string();
    bc.add_block(String::from(tx));

    println!("----------------Block Info------------------");
    bc.block_info();
}
```

To ensure that these codes work coherently, we need to arrange them logically. Since the hash calculation is not directly related to the blockchain, it should be included in the ”utils” directory as a tool. On the other hand, the ”block” and ”blockchain” should be stored in the ”core” directory. The main function should call the ”core” directory to execute the creation and addition of blocks. To generate the blockchain project, we can use Cargo, as demonstrated in the blockchain1 repository on GitHub. The code above has facilitated the implementation of a basic blockchain project that can create and add blocks. The program’s output, including mining information and block information, is depicted on next page.

Our implementation is a simplified version of a blockchain. A comprehensive blockchain involves various components such as proof of work, transactions, accounts, hashing, miners, mining, bitcoin rewards, block storage, and many others. Readers can gradually incorporate these features on top of the fundamental blockchain implementation.

## 10.9 Summary

In this chapter, we covered a plethora of useful data structures. We began by exploring the implementation of trie, Bloom filter, and cuckoo filter. Next, we delved into Hamming and edit distance, followed by an understanding of LRU cache eviction algorithm and consistent hashing algorithm. Lastly, we learned about the principles of blockchain and implemented a rudimentary blockchain. Throughout this book, we have covered a wide range of data structures and implemented a considerable amount of Rust code. Although some of the codes may not be optimal, they can still be useful references for readers. Any feedback from readers via Github to further improve the content is greatly appreciated. Finally, I hope that this book proves helpful to readers and serves as a valuable resource to explore rust and its applications in data structures.

# Bibliography

[1] The Open Group. Unix. Website, 1995. https://unix.org/what_is_unix.html. [2] Multicians. Multics. Website, 1995. https://www.multicians.org. [3] Linus. Linux kernel. Website, 1991. https://www.kernel.org. [4] GNU. Gnu/linux. Website, 2010. https://www.gnu.org. [5] Wikipedia. Quantum computer. Website, 2022.

```text
                                  https://en.wikipedia.org/wiki/
Quantum_computing.
```

[6] Bradley N. Miller and David L. Ranum. Problem Solving with Algorithms and Data Structures Using Python. Franklin, Beedle & Associates, US, 2011. [7] Rust Foundation. Rust foundation. Website, 2021. https://foundation.rust-lang.

```text
org/members/.
```

[8] Rui Pereira, Marco Couto, Francisco Ribeiro, Rui Rua, Jácome Cunha, João Paulo Fernandes, and João Saraiva. Energy efficiency across programming languages: How do energy, time, and memory relate? In Proceedings of the 10th ACM SIGPLAN International Conference on Software Language Engineering, SLE 2017, page 256–267, New York, NY, USA, 2017. Association for Computing Machinery. [9] Wikipedia. Np-complete problem. Website, 2021. https://zh.wikipedia.org/wiki/

```text
NP%E5%AE%8C%E5%85%A8.
```

[10] Wikipedia. Goldbach’s conjecture. Website, 2021. https://zh.wikipedia.org/zh-cn/

```text
%E5%93%A5%E5%BE%B7%E5%B7%B4%E8%B5%AB%E7%8C%9C%E6%83%B3.
```

[11] Yehoshua Perl, Alon Itai, and Haim Avni. Interpolation search—a log logn search. Commun. ACM,

21(7):550–553, jul 1978.

[12] Stanley P. Y. Fung. Is this the simplest (and most surprising) sorting algorithm ever?, 2021. [13] Wikipedia. Entropy. Website, 2022. https://zh.wikipedia.org/wiki/%E7%86%B5. [14] Wikipedia. Locality of reference. Website, 2022. https://zh.wikipedia.org/wiki/

```text
%E8%AE%BF%E9%97%AE%E5%B1%80%E9%83%A8%E6%80%A7.
```

[15] Wikipedia. Distance vector routing protocol. Website, 2021. https://en.wikipedia.org/

```text
wiki/Distance-vector_routing_protocol.
```

[16] Wikipedia. Link state routing protocol. Website, 2022. https://en.wikipedia.org/

```text
wiki/Link-state_routing_protocol.
```

[17] Wikipedia. Hamming code. Website, 2022. https://zh.wikipedia.org/zh-hans/

```text
%E6%B1%89%E6%98%8E%E7%A0%81.
```

[18] Bin Fan and David G Andarsen. Cuckoo filter: Practically better than bloom. Website, 2014.

```text
https://www.cs.cmu.edu/~dga/papers/cuckoo-conext2014.pdf.
```

[19] Satoshi Nakamoto. Bitcoin: A peer-to-peer electronic cash system. Website, 2008. https:

```text
//bitcoin.org/bitcoin.pdf.
```
