## 7.13 Сортировка Тимсорт (TimSort)

Гибридный алгоритм сортировки Тимсорт (TimSort), предложенный Тимом Питерсом в 2002 году, объединяет несколько методов сортировки, чтобы преодолеть ограничения отдельных алгоритмов. Тимсорт эффективен, стабилен и адаптируется к распределению данных, что делает его превосходящим большинство алгоритмов сортировки. В настоящее время он является алгоритмом сортировки по умолчанию во многих языках программирования и платформах, включая Java, Python, Rust и другие. Тимсорт — это гибридный стабильный алгоритм сортировки, использующий сортировку слиянием и сортировку вставками. Когда количество сортируемых элементов меньше 64, Тимсорт напрямую вызывает сортировку вставками. Однако когда количество элементов больше 64, Тимсорт комбинирует сортировку вставками и сортировку слиянием. На практике сортируемые данные часто содержат частично упорядоченные блоки, в которых некоторые части данных уже отсортированы по возрастанию или убыванию, как показано на рисунке ниже. Тимсорт использует эту особенность данных при их сортировке, и наличие частично упорядоченных блоков является ключевой идеей алгоритма.

![Рисунок 7.11: Частично упорядоченные данные](images/fig-7.11.png)

*Рисунок 7.11: Частично упорядоченные данные*

Для сортировки набора элементов Тимсорт делит их на серии (runs), или разделы. Эти серии можно рассматривать как отдельные вычислительные единицы. Тимсорт проходит по элементам и размещает их в разных сериях, одновременно сливая серии в соответствии с определёнными правилами. Это слияние продолжается до тех пор, пока не останется только одна серия, которая и является отсортированным результатом. Чтобы задать подходящий размер раздела, Тимсорт использует параметр minrun. Каждый раздел не может содержать меньше элементов, чем minrun. Если в разделе меньше элементов, чем minrun, количество серий расширяется до minrun с помощью сортировки вставками, после чего выполняется слияние.

![Рисунок 7.12: Серии данных](images/fig-7.12.png)

*Рисунок 7.12: Серии данных*

Приблизительный процесс работы Тимсорт выглядит следующим образом:

- Просканировать набор, который требуется отсортировать, чтобы определить, больше ли 64 количество элементов.
- Если оно меньше или равно 64, использовать алгоритм сортировки вставками для сортировки данных и вернуть результат.
- Если оно больше 64, просканировать набор, вычислить minrun и найти различные упорядоченные блоки.
- Сливать блоки попарно. Если в отдельном блоке меньше элементов, чем minrun, использовать сортировку вставками для его расширения.
- Повторять этот процесс, пока не останется только один блок, который и будет отсортированным набором.

Тимсорт — это алгоритм сортировки, который можно реализовать, решив три важные задачи: определение значения minrun, поиск упорядоченных блоков, а также расширение и слияние маленьких блоков. Первая задача — определить значение minrun. Тимсорт выбирает первые шесть двоичных разрядов длины n сортируемой коллекции в качестве minrun. Если оставшиеся разряды не равны 0, то minrun увеличивается на 1. Диапазон значений minrun — от 32 до 64.

- Для коллекции длины n = 189 её двоичное представление: 10111101. Первые шесть разрядов, 101111, равны 47, а оставшиеся разряды, 01, приводят к значению minrun, равному 48.
- Для коллекции длины n = 976 её двоичное представление: 1111010000. Первые шесть разрядов, 111101, равны 61, а оставшиеся разряды, 0000, приводят к значению minrun, равному 61.

Фактически максимальное значение первых шести двоичных разрядов равно 111111 = 63, а минимальное — 100000 = 32. Поэтому значение minrun находится в диапазоне от 32 до 64. Вторая задача — найти упорядоченные блоки. Тимсорт находит упорядоченные блоки, выявляя возрастающие или убывающие последовательности в коллекции. Это достигается алгоритмом, которому достаточно сравнивать соседние элементы, чтобы определить, образуют ли они блок. Третья задача — расширение и слияние маленьких блоков. После вычисления значения minrun Тимсорт на месте преобразует любые блоки, расположенные в обратном порядке, в правильный порядок. Если в блоке меньше элементов, чем minrun, используется сортировка вставками для расширения блока до достижения значения minrun. Затем алгоритм проверяет соотношение между текущим блоком и двумя предыдущими блоками. Если длины трёх блоков не удовлетворяют условиям A > B + C, B > C, то в зависимости от ситуации выполняется слияние A и B или B и C с использованием сортировки вставками. В противном случае алгоритм продолжает поиск следующего блока и повторяет расширение и слияние блоков. В итоге коллекция превращается в несколько упорядоченных блоков, причём длины этих слитых блоков располагаются от наибольшей к наименьшей. После завершения разбиения на блоки маленькие блоки попарно сливаются с конца коллекции к началу, и коллекция превращается в один большой блок, что означает завершение сортировки. Первые две задачи понятны, но третья может требовать дополнительных пояснений. Обращение порядка блока — простая операция. Для расширения блока в текущий блок вставляются новые элементы. Однако слияние блоков может быть сложным, поскольку возможны шесть различных сценариев. Когда есть только два блока, алгоритму достаточно учитывать условие A > B. Когда есть три блока, алгоритм проверяет, выполняются ли условия A > B + C и B > C. Ниже приведены иллюстрации шести случаев, где A находится внизу стека, а B или C — наверху:

- A > B: слияние не выполняется.
- A < B: слить серию A с B.
- A > B + C и B > C: слияние не выполняется.
- A > B + C и B < C: слить серию B с C.
- A < B + C и A > C: слить серию B с C. • A < B + C и A < C: слить серию A с B.

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

На рисунке показано слияние трёх упорядоченных блоков с минимальной длиной серии, равной 3. Символы A, B и C обозначают серии [xx], а вертикальные линии — временный стек, используемый для слияния этих блоков. Чтобы определить, нужно ли выполнять слияние и как именно, сравниваются длины трёх блоков. Идеальное состояние после слияния показано в случаях 1 и 3, тогда как остальные четыре сценария слияния используются для приближения к этим двум случаям. Условие A > B + C, B > C необходимо для обеспечения эффективного слияния. Например, прямое слияние блока [6,7,8] с [0,1,2,3,4,9,5] привело бы к двум оставшимся блокам с большой разницей в длине, из-за чего сортировка вставками стала бы неэффективной. Напротив, когда блоки имеют схожие длины, их слияние выполняется очень быстро. Поэтому в этом случае блоки не сливаются, а обрабатываются отдельно, после чего сливаются в обратном порядке в конце: [6,7,8] и [5], затем [0,1,2,3,4,9] и [5,6,7,8].

7 5 0 3 9 6 8 1 2 4

Чтобы упростить процесс сортировки, задаётся минимальная длина серии, ниже которой используется двоичная сортировка вставками. Если длина серии равна 64, minrun также устанавливается равным 64. В противном случае для minrun выбирается значение в диапазоне от 32 до 64

n

for minrun such that k =

minrun не превосходит степени двойки. k представляет собой количество

оставшихся блоков после сканирования и обработки, и их длины должны быть упорядочены от наибольшей к наименьшей. Это позволяет выполнять слияние с конца, в результате чего получаются более длинные блоки и более быстрое слияние, подобно двоичному поиску. Следовательно, требуется, чтобы k было меньше или равно степени двойки.

![Рисунок 7.13: Тимсорт](images/fig-7.13.png)

*Рисунок 7.13: Тимсорт*

Для иллюстрации механизма расширения и слияния блоков выше приведены схемы. В этом примере minrun = 5, и каждая строка представляет собой один цикл операций. В крайнем левом столбце указан номер цикла, а в квадратных рамках показаны элементы, которые нужно отсортировать. Алгоритм Тимсорт состоит из нескольких раундов обработки для сортировки заданного набора данных. В первом раунде алгоритм получает данные для сортировки из своих параметров. Во втором раунде он ищет разделы и находит раздел длиной, равной значению минимальной серии, который представляет собой заранее определённый набор значений [2,4,7,8,23]. В третьем раунде он ищет следующий раздел и обнаруживает инверсию [19,16,14,13,12,10], которая затем в четвёртом раунде приводится к упорядоченному виду [10,12,13,14,16,19]. В пятом раунде алгоритм сравнивает длину текущего раздела с длиной предыдущего раздела и, если текущий раздел длиннее, сливает их с помощью сортировки вставками. Результатом является [2,4,7,8,10,12,13,14,16,19,23] — новый раздел, представляющий собой объединение двух предыдущих разделов. В шестом раунде он находит следующий раздел [20,18,17,15,11,9], обнаруживает инверсию и в седьмом раунде приводит его к упорядоченному виду. Затем он сравнивает его длину с длиной предыдущего раздела и, поскольку он короче, продолжает поиск следующего раздела. В восьмом раунде алгоритм находит новый раздел [0,5,6], который короче минимальной длины серии, и расширяет его с помощью сортировки вставками. Затем он сравнивает его длину с длинами двух предыдущих разделов и определяет, что они удовлетворяют определённым условиям, а значит, слияние не требуется. Этот процесс продолжается до тех пор, пока все разделы не будут сформированы, что происходит после десяти раундов. В одиннадцатом раунде алгоритм начинает сливать меньшие разделы с конца к началу ([0,1,3,5,6] и [21,22]). В двенадцатом раунде он сливает два оставшихся раздела [9,11,15,17,18,20] и [0,1,3,5,6,21,22], в результате чего получается один упорядоченный набор.

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

Для блоков, содержащих менее MIN_MERGE элементов, можно использовать двоичную сортировку вставками, чтобы ускорить процесс сортировки. Этот метод уже был реализован в предыдущем разделе, поэтому дополнительный код здесь не приводится. При использовании Тимсорт первым шагом является вычисление значения minrun и выявление отсортированных серий (включая обратные серии). При необходимости обратные серии следует преобразовать в обычные.

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

Далее для сортировки SortState необходимо реализовать конструктор и функцию sort. Наконец, когда длины разделов не удовлетворяют требованиям, необходимо выполнить слияние разделов с использованием сортировки слиянием.

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

Существует шесть случаев разбиения, при которых может потребоваться слияние A и B или слияние B и C. Поскольку A, B и C расположены в памяти непрерывно, слияние A и B можно реализовать отдельно от слияния B и C, используя их относительное расположение.

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

Ниже приведена основная функция Тимсорт.

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

Ниже приведён пример использования Тимсорт.

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

Реализованный алгоритм Тимсорт работает только для чисел типа i32, но его можно расширить для поддержки сортировки значений различных типов с помощью обобщённых типов. Кроме того, при слиянии некоторые данные могут быть уже отсортированы, однако реализованный алгоритм Тимсорт всё равно выполняет сравнения по одному. Тем не менее слияние можно ускорить с помощью стратегии, называемой галопированием (galloping). Реализация Тимсорт в исходном коде этой книги в файле tim_sort_without_gallop.rs является неускоренной версией, но в файле tim_sort.rs также реализована ускоренная версия Тимсорт. Заинтересованные читатели могут обратиться к этим реализациям и сравнить различия между двумя алгоритмами. Некоторые читатели могут задаться вопросом, как Тимсорт определяет, являются ли сортируемые данные изначально блочно упорядоченными. На самом деле алгоритм не может этого определить — это свойство частично упорядоченных данных, которое обнаружил автор. В физике существует понятие энтропии [13], обозначающее степень беспорядка в физической

системе. Чем более неупорядочена система, тем больше энтропия, и наоборот, чем более упорядочена система, тем меньше энтропия. В большинстве случаев вещи обладают определённой степенью упорядоченности. Например, люди — это упорядоченные существа, существующие вопреки энтропии, и становятся неупорядоченными только со смертью. Другой пример — принцип локальности обращений [14]: при доступе к данным на жёстком диске процессор считывает в память также данные, расположенные рядом, поскольку к ним, вероятно, будет обращение в ближайшее время. Эти два явления являются законами природы, согласующимися со статистическими принципами, и Тим разработал Тимсорт на основе этих законов. Это показывает важность структур данных и то, как различное понимание может привести к совершенно разным алгоритмам.