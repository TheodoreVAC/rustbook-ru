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
