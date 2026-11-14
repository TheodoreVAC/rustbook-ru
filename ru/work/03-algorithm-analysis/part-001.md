# Algorithm Analysis

## 3.1 Objectives

- Understanding the Importance of Algorithm Analysis.
- Learning to perform performance benchmark tests on Rust programs.
- Being able to use the Big O notation to analyze the complexity of algorithms.
- Understanding the Big O analysis results for Rust data structures such as arrays.
- Understanding how Rust data structure implementations affect algorithm analysis.

## 3.2 What is Algorithm Analysis?

In Chapter 2, we defined an algorithm as a set of instructions that solves a specific problem by producing an expected result given a specific input. A program is an algorithm written in a programming language. As programmers use different programming languages and have varying levels of knowledge, different programs may describe the same algorithm. New computer science students may compare their programs with others. To explore the differences between programs that solve the same problem, let’s consider the functions ”sum_of_n” and ”tik_tok,” which both calculate the sum of the first n integers. The first function uses an accumulator variable initialized to 0 and iterates over the n integers, adding each value to the accumulator. The ”tik_tok” function does the same thing but uses unclear identifier names and an unnecessary assignment.

```rust
// sum_of_n.rs
fn sum_of_n(n: i32) -> i32 {
    let mut sum: i32 = 0;
    for i in 1..=n { sum += i; }
    sum
}

// tiktok.rs
fn tiktok(tik: i32) -> i32 {
    let mut tok = 0;
    for k in 1..=tik {
        let ggg = k;
        tok = tok + ggg;
    }
    tok
}
```

When evaluating the two functions, the answer depends on the reader’s criteria. If readability is the concern, then ”sum_of_n” is better. However, in this book, we focus more on the statements of the algorithms themselves, and clean coding is not part of the discussion. Algorithm analysis compares the amount of resources used by algorithms. An algorithm is better than another algorithm if it uses fewer resources or is more efficient in using resources. When comparing the ”sum_of_n” and ”tik_tok” functions, they appear very similar in terms of resource usage. Identifying the resources used for computation is crucial and requires considering both time and space perspectives.

- The space used by an algorithm is determined by its memory consumption, which is typically influenced by the size and nature of the problem. However, some algorithms have special space requirements.
- Algorithm execution time refers to the time it takes for an algorithm to execute all its steps.

For instance, the execution time of the ”sum_of_n” function can be analyzed through benchmark testing. In Rust, the execution time of code can be calculated by recording the system time before and after function execution. The SystemTime function, which is available in std::time, returns the system time when called and gives the elapsed time afterward. By calling this function at the beginning and end of function execution, we can obtain the function execution time.

```rust
// static_func_call.rs

use std::time::SystemTime;

fn sum_of_n(n: i64) -> i64 {
    let mut sum: i64 = 0;
    for i in 1..=n {
        sum += i;
    }
    sum
}

fn main() {
    for _i in 0..5 {
        let now = SystemTime::now();
        let _sum = sum_of_n(500000);
        let duration = now.elapsed().unwrap();
        let time = duration.as_millis();
        println!("func used {time} ms");
    }
}
```

To illustrate this, we executed the ”sum_of_n” function five times, each time calculating the sum of the first 500,000 integers and 1000,000 integers. The results were as follows:

```text
func used 10 ms
func used 6 ms
func used 6 ms
func used 6 ms
func used 6 ms
func used 17 ms
func used 12 ms
func used 12 ms
func used 12 ms
func used 12 ms
```

After comparing the results of two executions, it was found that the time taken by the function to execute is basically the same. On average, the function takes 6 milliseconds to execute. The first execution takes longer at 10 milliseconds because the function requires initialization and preparation. The subsequent four executions do not require initialization, and their times are more accurate, hence why multiple executions are necessary. When calculating the sum of the first 1,000,000 integers, it can be observed that the first execution takes longer, and the subsequent executions take exactly twice the time taken to calculate the sum of the first 500,000 integers. This indicates that the execution time of the algorithm is proportional to the size of the calculation. To further explore this idea, consider the following function, which also calculates the sum of the first n integers, but uses the mathematical formula ∑n i=0 = n(n+1)

to compute it. 2

```rust
// static_func_call2.rs
fn sum_of_n2(n: i64) -> i64 {
    n * (n + 1) / 2
}
```

The sum_of_n function in static_func_call.rs is modified to use this formula, and a benchmark test is performed using three different values of n (100,000, 500,000, 1,000,000). Each calculation is repeated five times, and the average execution time is recorded. The results are as follows:

```text
func used 1396 ns
func used 1313 ns
func used 1341 ns
```

There are two important points to note in the output. First, the recorded execution time is in nanoseconds, which is significantly shorter than the previous examples. The execution times for all three calculations are approximately 0.0013 milliseconds, which is orders of magnitude shorter than the previous 6 milliseconds. Second, the execution time is independent of n. As n increases, the calculation time remains the same, indicating that the calculation is almost unaffected by n. This benchmark test indicates that the iterative solution sum_of_n performs more work because some program steps are repeated, which is why it takes longer. Moreover, the execution time of the iterative solution increases with n. Additionally, it should be noted that running similar functions on different computers or using different programming languages may yield different results. The calculated value of 1341 nanoseconds mentioned in the text refers to the computer used in this study, which is Lenovo Legion R7000P with a 16-core AMD R7-4800H CPU. Older computers may take longer to execute sum_of_n2. It is necessary to find a better way to describe the execution time of algorithms. Although benchmark tests measure the actual time taken by a program to execute, they do not provide a useful measure because the execution time depends on the specific machine, and there are also magnitude conversions between milliseconds and nanoseconds. We require a measure that is independent of the program or computer used, and can be used to compare the efficiency of different algorithm implementations. Big O notation is a good method for measuring algorithmic efficiency in the field of algorithm analysis, analogous to acceleration measuring the change in speed per second.

## 3.3 Big-O Notation Analysis

To evaluate the performance of an algorithm, we need to quantify the number of operation steps and storage space required independently of any specific program or computer. For the summing algorithm, counting the execution statements is a good measure. In the function sum_of_n, there is one assignment statement (the_sum = 0), and n addition statements (the_sum += i), making the statement count for the function equal to n + 1. The storage space used is two variables, n and sum, so the count is 2.

We use the function T to represent the total number of executions to measure the algorithm’s time complexity, where T(n) = 1 + n. The parameter n represents the problem size, and T(n) is the time spent solving a problem with a size greater than or equal to n. Using n to represent the problem size makes sense for the summing function, as summing 100,000 integers is a larger problem than summing 1000 integers, and thus takes longer. Our goal is to demonstrate how the algorithm’s execution time changes relative to the problem size. For measuring the algorithm’s space complexity, we use the function S to represent the total memory consumption, where S(n) = 2. The parameter n still represents the problem size, but S(n) is independent of n. To analyze the performance of an algorithm, it is crucial to determine the primary components of its time complexity function T(n) and space complexity function S(n), rather than merely counting the number of operation steps and space usage. As the problem size grows, some components of these functions become dominant. The fastest-growing parts of these functions with n are represented by the big O notation, denoted as O(f(n)). The function f(n) signifies the primary part of T(n) or S(n). For instance, T(n) = n + 1 in the previous example. As n increases, the constant 1 becomes less significant. Thus, we can approximate the running time of T(n) as O(T(n)) = O(n + 1) = O(n). While the constant 1 is undoubtedly important for T(n), its contribution becomes negligible when n is large. However, when T(n) = n3 + 1, (n = 1), discarding the constant 1 is unreasonable since it would mean discarding a significant portion of the running time. In this case, using O(T(n)) = O(n3 + 1) is appropriate for small values of n. But as n increases, the 1 becomes less significant, and we can approximate T(n) as O(T(n)) = O(n3). For S(n), since it is a constant, O(S(n)) = O(2) = O(1). The big O notation only represents the order of magnitude. Therefore, although the actual complexity of S(n) is O(2), we use O(1) instead. Assuming an algorithm has a number of operational steps determined by T(n) = 6n2 + 37n + 996. When n is small, such as 1 or 2, the constant term 996 may seem to be the main part of the function. However, as n grows larger, the significance of the n2 term increases. In fact, as n becomes very large, the other two terms become negligible in the final result. Thus, we can approximate T(n) by ignoring the other terms and focusing only on 6n2. Moreover, the coefficient 6 also becomes insignificant as n grows larger. Thus, we say that T(n) has a complexity order of n2, or O(n2). However, the complexity of some algorithms depends on the exact values of the data, rather than the size of the problem. For such algorithms, their performance needs to be characterized based on best case, worst case, or average case scenarios. Worst case refers to a specific dataset that leads to particularly poor algorithm performance, while the same algorithm may have significantly different performance under different datasets. In most cases, the efficiency of algorithm execution lies between the two extremes of worst and best cases, i.e., the average case. Thus, it is important for programmers to understand these differences and avoid being misled by a particular case. In the study of algorithms, some common order functions appear repeatedly, as shown in the table and figure below. To determine which of these functions is the main part, we need to observe how they relate to each other as n grows larger.

**Table 3.1: Complexity functions**

| O(1) | O(logn) | O(n) | O(nlogn) | O(n2) | O(n3) | O(2n) |
| --- | --- | --- | --- | --- | --- | --- |
| constants | logarithmic | linear | linear logarithmic | quadratic | cubic | power exponential. |

The figure below illustrates the growth of various functions. At small values of n, it can be difficult to discern which function dominates the others. However, as n increases, the relative sizes of the functions become clear. It is worth noting that at n = 10, 2n exceeds n3, though this case is not shown on the graph. The figure also highlights the differences between different orders of magnitude. Generally, for n > 10, we have O(2n) > O(n3) > O(n2) > O(n log n) > O(n) > O(log n) > O(1). This information is useful in algorithm design, as it allows us to calculate the complexity of an algorithm. If we determine that an algorithm has a complexity similar to O(2n), for example, we know that it is not practical and can look to optimize it for better performance.

![Figure 3.1: Complexity curve](images/fig-3.1.png)

*Figure 3.1: Complexity curve*

The above analysis examines time and space complexity, but often time complexity is the primary concern because space is typically difficult to optimize. For example, the space complexity of an input array is limited from the outset, but different algorithms can result in significant differences in the time required to run on the array. Moreover, as storage becomes cheaper and more abundant, time becomes the most important factor because it cannot be increased. Therefore, most of the complexity analysis in this book focuses on time complexity, unless otherwise specified. The following code only employs addition, subtraction, multiplication, and division. We can use it to apply our newly acquired understanding of algorithm complexity analysis.

```rust
// big_o_analysis.rs
fn main() {
    let a = 1; let b = 2;
    let c = 3; let n = 1000000;

    for i in 0..n {
        for j in 0..n {
            let x = i * i;
            let y = j * j;
            let z = i * j;
         }
    }

    for k in 0..n {
        let w = a*b + 45;
        let v = b*b;
    }

    let d = 996;
}
```

The code above has a time complexity of O(n2), which can be obtained by analyzing the code. Firstly, the time to allocate operations a, b, c, and n is a constant 4. Then, the second term is 3n2, which comes from the execution of three statements n2 times due to nested iteration. The third term is 2n, as two statements are iteratively executed n times. Finally, the fourth term is a constant 1, representing the final assignment statement d = 996. Thus, the function that determines the number of operational steps is T(n) = 4 + 3n2 + 2n + 1 = 3n2 + 2n + 5. By examining the exponent, we can see that the n2 term is the most significant, indicating that the time complexity of this code is O(n2).

## 3.4 Anagram Detection

The problem of checking if two strings are permutations of each other serves as an example to demonstrate different levels of complexity. A permutation is defined as one string, s1, being a rearrangement of another string, s2. For instance, ”heart” and ”earth” are permutations of each other, as are ”rust” and ”trus”. Let us assume that both strings have the same length and consist only of 26 lowercase letters. Our goal is to write a function that takes two strings as inputs and returns whether or not they are permutations of each other.

### 3.4.1 Brute Force

The most naive solution to this problem is to use brute force and check all possible permutations of s1. This method is highly resource-intensive, consuming both time and memory. When generating all possible strings of s1, there are n possibilities for the first position, n-1 for the second position, n-2 for the third position, and so on, resulting in n! = n × (n −1) × (n −2) × ... × 3 × 2 × 1 total possibilities. Although some strings may be duplicates, the program cannot know this in advance, and thus it will generate n! strings. For example, if s1 has a length of 20, there will be 20! = 2,432,902,008,176,640,000 possible strings. If we process one possible string per second, it would take 77,146,816,596 years to exhaust the entire list. In fact, n! grows even faster than n2, making brute force an infeasible solution for any learning or real software project. Nonetheless, being aware of its existence and making an effort to avoid such situations is essential.

### 3.4.2 Checking Off

A more efficient solution to the problem involves checking if each character in the first string is present in the second string. If all characters are found, then the two strings are permutations of each other. We can use the ’ ’ character to replace a character once it has been checked.

```rust
// anagram_solution2.rs

fn anagram_solution2(s1: &str, s2: &str) -> bool {
    if s1.len() != s2.len() {
        return false;
    }

    // put the characters of s1 and s2 into
    // vec_a and vec_b respectively
    let mut vec_a = Vec::new();
    let mut vec_b = Vec::new();
    for c in s1.chars() {
        vec_a.push(c);
    }
    for c in s2.chars() {
```

```rust
        vec_b.push(c);
    }

    // index: pos1, pos2
    let mut pos1: usize = 0;
    let mut pos2: usize;

    // loop controlling
    let mut is_anagram = true;
    let mut found: bool;
    while pos1 < s1.len() && is_anagram {
        pos2 = 0;
        found = false;
        while pos2 < vec_b.len() && !found {
            if vec_a[pos1] == vec_b[pos2] {
                found = true;
            } else {
                pos2 += 1;
            }
        }

        // replace a character with ' '
        if found {
            vec_b[pos2]= ' ';
        } else {
            is_anagram = false;
        }

        // tackle the next character of s1
        pos1 += 1;
    }

    is_anagram
}

fn main() {
    let s1 = "rust";
    let s2 = "trus";
    let result = anagram_solution2(s1, s2);
    println!("s1 and s2 is anagram: {result}");
    // s1 and s2 is anagram: true
}
```

Upon analyzing this algorithm, we observe that each character in s1 is compared to all characters in s2, which leads to a maximum of n comparisons for each character in s1. As a result, the n positions in blist will be visited once to match the characters from s1. The total number of visits can be expressed as the sum of integers from 1 to n.

n ∑

i = n(n + 1)

= 1 2n2 + 1 1 + 2 + · · · + n = 2n (3.1) 2 i=1

The time complexity of this algorithm is O(n2), as the term n2 dominates as n grows. This is much better than the brute force algorithm that has a complexity of O(n!).

### 3.4.3 Sort and Compare

An alternative solution for scrambled strings is to take advantage of the fact that even if s1 and s2 are different, they consist of exactly the same characters. Therefore, we can sort each string in alphabetical order from a to z, and if the two sorted strings are the same, then they are scrambled strings.

```rust
// anagram_solution3.rs

fn anagram_solution3(s1: &str, s2: &str) -> bool {
    if s1.len() != s2.len() {
        return false;
    }

    // put the characters of s1 and s2 into
    // vec_a and vec_b respectively then sorting
    let mut vec_a = Vec::new();
    let mut vec_b = Vec::new();
    for c in s1.chars() {
        vec_a.push(c);
    }
    for c in s2.chars() {
        vec_b.push(c);
    }
    vec_a.sort();
    vec_b.sort();

    // compare vec_a and vec_b, if thers is any mismatch of
    // any character then break the loop
    let mut pos: usize = 0;
    let mut is_anagram = true;
    while pos < vec_a.len() && is_anagram {
        if vec_a[pos] == vec_b[pos] {
            pos += 1;
        } else {
            is_anagram = false;
        }
    }

    is_anagram
}

fn main() {
    let s1 = "rust";
    let s2 = "trus";
    let result = anagram_solution3(s1, s2);
    println!("s1 and s2 is anagram: {result}");
    // s1 and s2 is anagram: true
}
```

At first glance, the time complexity of the algorithm that checks for scrambled strings seems to be O(n) because it has only one while loop. However, the complexity of calling the sort() function is not negligible, and it is usually O(n2) or O(n log n), which makes the algorithm’s complexity of the same order of magnitude as sorting algorithms.

### 3.4.4 Count and Compare

The previous methods always create vec_a and vec_b, which can be memory-intensive when s1 and s2 are long. To solve this problem, we can use two lists with a length of 26 to count the frequency of each character in s1 and s2. This approach involves multiple iterations, but the iterations are non-nested. Moreover, the third iteration that compares the two frequency lists only needs 26 iterations because there are only 26 lowercase letters. Thus, the time complexity of this algorithm is O(n), where n is the length of s1 or s2. This is a linear time complexity algorithm, and both its space and time complexities are relatively efficient.

```rust
// anagram_solution4.rs

fn anagram_solution4(s1: &str, s2: &str) -> bool {
    if s1.len() != s2.len() { return false; }

    // with the size of 26, c1 and c2 are storage
    // for saving ASCII charaters
    let mut c1 = [0; 26];
    let mut c2 = [0; 26];
    for c in s1.chars() {
        let pos = (c as usize) - 97; // 97: ASCII value of a
        c1[pos] += 1;
    }
    for c in s2.chars() {
        let pos = (c as usize) - 97;
        c2[pos] += 1;
    }

    // compare the value of ASCII
    let mut pos = 0;
    let mut is_anagram = true;
    while pos < 26 && is_anagram {
        if c1[pos] == c2[pos] {
            pos += 1;
        } else {
            is_anagram = false;
        }
    }

    is_anagram
}

fn main() {
    let s1 = "rust";
    let s2 = "trus";
    let result = anagram_solution4(s1, s2);
    println!("s1 and s2 is anagram: {result}");
    // s1 and s2 is anagram: true
}
```

However, if s1 and s2 are short and do not use all 26 characters, this algorithm sacrifices some storage space. When deciding which algorithm to use, it is essential to make a trade-off between space and time and consider the real scenarios that your algorithm will face.

## 3.5 Performance of Rust Data Structures

### 3.5.1 Scalar and Complex Data Structures

In this section, we will explore the big O performance of Rust’s basic data types. Understanding the performance of these data structures is crucial because they are the core building blocks in Rust, and more complex data structures are constructed from them. Rust’s basic data types are divided into two major categories: scalar and composite types. Scalar types represent a single value, while composite types are combinations of scalar types. Rust has four basic scalar types: integer, floating-point, boolean, and character. On the other hand, Rust has two composite types: tuple and array. Scalar types are the most basic and memory-coupled primitive types, with computational efficiency that is typically O(1). Meanwhile, composite types are more complex, and their complexity varies with their data scale. Let’s take a look at some examples of using basic data types.

```rust
let a: i8 = -2;
let b: f32 = 2.34;
let c: bool = true;
let d: char = 'a';

// tuple with various types
let x: (i32, f64, u8) = (200, 5.32, 1);
let xi32 = x.0;
let xf64 = x.1;
let xu8 = x.2;
```

The tuple is a composite data structure that combines multiple values of various types, with a fixed length. Once declared, its length cannot be increased or decreased. Tuple indexing starts from 0, and its values can be directly accessed using the ”.”(dot notation). Arrays, on the other hand, must have the same type for each element, and once declared, their length cannot be increased or decreased.

```rust
let months = ["January","February","March","April",
              "May","June","July","August","September",
              "October","November","December"
             ];

let first_month = months[0]
let halfyear = &months[..6];

let mut monthsv = Vec::new();
for month in months { monthsv.push(month); }
```

Rust offers various data types, composed of scalar and composite types, such as Vec and HashMap. Vec is a collection type similar to an array, which allows for adding, shrinking, and limiting its length. It provides greater scalability and can be used wherever an array can be used.

### 3.5.2 Collection Data Structures

Rust’s collection types are divided into linear and non-linear types, constructed based on scalar and composite types. The linear collection types include String, Vec, VecDeque, and LinkedList, while the non-linear collection types include HashMap, BTreeMap, HashSet, BTreeSet, and BinaryHeap. These collection types involve indexing, adding, and deleting operations, and their respective complexities are often O(1), O(n), etc.

Rust’s String type is based on Vec, which allows String to be modified like Vec. To use a portion of the String, one can use &str, which is a slice of the String type that is easy to index. However, since &str is based on String, it cannot be changed because modifying the slice would change the data in String, which may be used elsewhere. In Rust, mutable strings use String, while immutable strings use &str. Vec is similar to lists in other languages, and VecDeque extends Vec to support inserting data at both ends of the sequence, making it a double-ended queue. LinkedList is a linked list and can be used when an unknown size Vec is desired. The HashMap in Rust is similar to dictionaries in other languages, while BTreeMap is a B-tree whose nodes contain data and pointers. It is often used to implement databases, file systems, and other content storage applications. The HashSet and BTreeSet in Rust are similar to the Set collection in other languages, which are used to record a single value that has appeared once. HashSet is implemented using HashMap as its underlying data structure, while BTreeSet is implemented using BTreeMap. BinaryHeap is a priority queue, storing a set of elements that can extract the maximum value at any time. Rust’s collection data types are highly efficient, as can be seen from the tables below that show the performance of various data structures. The highest complexity of these data structures is O(n).

**Table 3.2: Time complexity of linear composite types**

| Type | get | insert | remove | append | split_off |
| --- | --- | --- | --- | --- | --- |
| Vec | O(1) | O(n −i) | O(n −i) | O(m) | O(n −i) |
| VecDeque | O(1) | O(min(i, n −i)) | O(min(i, n −i)) | O(m) | O(min(i, n −i)) |
| LinkedList | O(min(i, n −i)) | O(min(i, n −i)) | O(min(i, n −i)) | O(1) | O(min(i, n −i)) |

**Table 3.3: Time complexity of non-linear composite types**

| Type | get | insert | remove | predecessor | append |
| --- | --- | --- | --- | --- | --- |
| HashMap | O(1) | O(1) | O(1) | N/A | N/A |
| HashSet | O(1) | O(1) | O(1) | N/A | N/A |
| BTreeMap | O(logn) | O(logn) | O(logn) | O(logn) | O(n + m) |
| BTreeSet | O(logn) | O(logn) | O(logn) | O(logn) | O(n + m) |
| Type | push | pop | peek | peek_mut | append |
| BinaryHeap | O(1) | O(1ogn) | O(1) | O(1) | O(n + m) |

## 3.6 Summary

This chapter introduced the big O notation analysis method for evaluating algorithm complexity, which involves calculating the number of code execution steps and determining the maximum quantity level. We then examined the complexity of Rust’s basic data types and collection data types. Upon comparison and analysis, it becomes clear that Rust’s built-in scalar, composite, and collection data types are highly efficient. Additionally, custom data structures implemented based on these collection types can also achieve efficient.
