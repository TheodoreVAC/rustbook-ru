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
