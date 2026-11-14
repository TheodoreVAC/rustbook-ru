# Recursion

## 5.1 Objectives

- Understanding simple recursive solutions
- Learning how to write programs using recursion
- Understanding and applying the three laws of recursion
- Understanding recursion as a form of iteration
- Formulating problems into recursive solutions
- Understanding how computers implement recursion

## 5.2 What is Recursion?

Recursion is a problem-solving method that involves breaking down a complex problem into smaller sub-problems until a simple base case is reached. By solving the base case and combining the results, the solution to the original problem can be obtained. Recursion is particularly useful for solving difficult problems elegantly. For instance, consider the task of computing the sum of an integer array like [2, 1, 7, 4, 5]. The most straightforward way to do it is by using an accumulator to add each value iteratively.

```rust
// iterative sum

fn nums_sum(nums: Vec<i32>) -> i32 {
    // use sum as accumulator
    let mut sum = 0;

    for num in nums {
        sum += num;
    }

    sum
}
```

However, if a programming language lacks for or while loops, the above sum code won’t work. In such cases, one can still compute the sum by using recursion to solve smaller problems. To solve the sum problem recursively, you can break down the array into smaller additions, which can be constructed using the basic problem of addition. By recursively solving these smaller problems, you can eventually solve the original sum problem without loops.

The process of constructing small additions can be done using elementary school-level knowledge of constructing fully parenthesized expressions, of which there are of course two forms as shown below. 2 + 1 + 7 + 4 + 5 = 2 + 1 + 7 + 4 + 5 sum = ((((2 + 1) + 7) + 4) + 5) sum = (((3 + 7) + 4) + 5) sum = (10 + 4) + 5) sum = (14 + 5)

sum = 19 (5.1)

= 2 + 1 + 7 + 4 + 5 sum = (2 + (1 + (7 + (4 + 5)))) sum = (2 + (1 + (7 + 9))) sum = (2 + (1 + 16)) sum = (2 + 17)

sum = 19

Overall, recursion provides an elegant and effective solution to seemingly difficult problems, allowing for efficient computation and solving programming challenges even in languages with limited capabilities. The given expression can be correctly parenthesized using either form of parentheses on the righthand side. By following the rule of parentheses precedence and internal priority, we can treat the parenthesized expression as a sequence of small additions. The pattern of both parts and the entire expression is entirely recursive, and we can simulate it without using While or For loops. If we observe the calculation starting with ”sum” and read it from bottom to top, we can see that the first term is 19, followed by (2 + 17), and then (2 + (1 + 16)). The total sum is the sum of the first term and the remaining terms on the right-hand side. We can further decompose it into the sum of its first term and the remaining terms on the right-hand side. Therefore, we can express this mathematically as follows: Sum(nums) = First(nums) + Sum(restR(nums))

(5.2)

This is the calculation method for the second form of parenthesized expressions. Similarly, we also have a calculation method for the first form of parenthesized expressions. Sum(nums) = Last(nums) + Sum(restL(nums))

(5.3)

The equation defines various functions such as First(nums), restR(nums), Last(nums), and restL(nums) that return the required elements from the array. We can implement two recursive methods to calculate expressions in Rust. The nums_sum1 function sums the remaining terms after nums[0], while the nums_sum2 function sums the last term and all the terms before it. Both implementations have the same time and space complexities and do not differ from each other.

```rust
// nums_sum12.rs

// Form : Sum(nums) = First(nums) + Sum(restR(nums))
fn nums_sum1(nums: &[i32]) -> i32 {
    if 1 == nums.len() {
        nums[0]
    } else {
        let first = nums[0];
        first + nums_sum1(&nums[1..])
    }
```

```rust
}

// Form : Sum(nums) = Last(nums) + Sum(restL(nums))
fn nums_sum2(nums: &[i32]) -> i32 {
    if 1 == nums.len() {
        nums[0]
    } else {
        let last = nums[nums.len() - 1];
        nums_sum2(&nums[..nums.len() - 1]) + last
    }
}

fn main() {
    let nums = [2,1,7,4,5];
    let sum1 = nums_sum1(&nums);
    let sum2 = nums_sum2(&nums);
    println!("sum1 = {sum1}, sum2 = {sum2}");
    // sum1 = 19, sum2 = 19

    let nums = [-1,7,1,2,5,4,10,100];
    let sum1 = nums_sum1(&nums);
    let sum2 = nums_sum2(&nums);
    println!("sum1 = {sum1}, sum2 = {sum2}");
    // sum1 = 128, sum2 = 128
}
```

The crucial part of the code is the if and else statements and their respective forms. The condition of if 1 == nums.len() is crucial as it marks the turning point of the function. At this point, the numerical value is directly returned without any further mathematical calculation. In the else statement, the function calls itself, achieving the effect of solving parentheses layer by layer and calculating their values. This is the essence of recursion, where a function calls itself until it reaches a base case.

### 5.2.1 The Three Laws of Recursion

By analyzing the above code, we can see that all recursive algorithms must follow these three basic laws:

```text
Recursive algorithms must have a base case
Recursive algorithms must move towards the base case
Recursive algorithms must call themselves in a recursive manner
```

The first law is the base case, which is when the algorithm stops, in this case, 1 == nums.len(). The second law involves the decomposition of the problem, where we return the number in the else clause and then calculate it again using the set of elements except for the returned number. This reduces the number of elements in the original array nums that need to be calculated. It is evident that the else clause moves towards the base case(nums.len == 1), which occurs when nums.len() > 1. The third law involves calling itself, which is implemented in the else clause. It is important to note that calling itself is not a loop, and there are no while or for statements here. In summary, our recursive sum algorithm satisfies these three laws. The recursive function call process can be visualized using a series of boxes representing the function call graph. Each recursion solves a small problem until the problem reaches the base case, where it can no longer be further decomposed. Finally, these intermediate calculated values are used to solve the larger problem.

![Figure 5.1: caculation by iteration](images/fig-5.1.png)

*Figure 5.1: caculation by iteration*

### 5.2.2 Converting an Integer to a String in Any Base

In the previous section, we discussed implementing algorithms for converting integers into binary and hexadecimal strings using stacks. However, recursive methods can also be used for base conversion. To design a recursive algorithm for base conversion, we must adhere to the three laws of recursion.

```text
The recursive algorithm must have a base case
The recursive algorithm must move towards the base case
The recursive algorithm must call itself
```

The algorithm for base conversion can be derived as follows:

```text
Simplify the original number into a series of individual digits
Use a lookup method to convert each digit into a character
Concatenate the individual characters to form the final result
```

To move towards the base case, we use division to change the number state. We divide the number by the base and obtain a remainder and a quotient. If the quotient is less than the base, we stop the operation and return the result. For instance, consider the decimal number 996 and converting it into a base-10 string. We divide 996 by 10, and the remainder is 6, and the quotient is 99. Since the remainder is less than 10, we can obtain the character ’6’. The quotient 99 is less than 996, which moves us closer to the base case. We then recursively call the function with 99 as the input. We divide 99 by 10, and the remainder is 9, and the quotient is 9. Since the remainder is less than 10, we can obtain the character ’9’. Finally, we get the decimal string ’996’. Once we can solve base-10 conversion, we can easily handle base-2 to base-16 conversion. Here’s an algorithm for converting integers to any base (base-2 to base-16) string. The variable BASESTR holds the character representation for different digits, with digits greater than 10 represented by characters A-F.

```text
// num2str_rec.rs

//Character table for various digits
const BASESTR: [&str; 16] = ["0","1","2","3","4","5","6","7",
                             "8","9","A","B","C","D","E","F"];
```

```rust
fn num2str_rec(num: i32, base: i32) -> String {
    if num < base {
        BASESTR[num as usize].to_string()
    } else {
        // Append remainder to the end of the string
        num2str_rec(num/base, base) +
            BASESTR[(num % base) as usize]
    }
}

fn main() {
    let num = 100;
    let sb = num2str_rec(num,2); // sb = str_binary
    let so = num2str_rec(num,8); // so = str_octal
    let sh = num2str_rec(num,16); // sh = str_hexdecimal
    println!("{num} = b{sb}, o{so}, x{sh}");
    // 100 = b1100100, o144, x64

    let num = 1000;
    let so = num2str_rec(num,8);
    let sh = num2str_rec(num,16);
    println!("{num} = o{so}, x{sh}");
    // 1000 = o1750, x3E8
}
```

In the previous section, we utilized a stack to convert numbers to any base. Now, we still achieve similar functionality using recursion, indicating a relationship between stacks and recursion. Recursion can be viewed as a stack, but the stack is implicitly called by the compiler. The code only uses recursion, but the compiler employs a stack to save data. If we were to implement the following recursive code using a stack, the structure would be very similar.

```rust
// num2str_stk.rs

fn num2str_stk(mut num: i32, base: i32) -> String {
    let digits: [&str; 16] = ["0","1","2","3","4","5","6","7",
                             "8","9","A","B","C","D","E","F"];

    let mut rem_stack = Stack::new();
    while num > 0 {
        if num < base {
            // Push directly to stack if not exceeding the base
            rem_stack.push(num);
        } else {
            // Push remainder to stack if exceeding the base
            rem_stack.push(num % base);
        }
        num /= base;
    }

    // Pop remainder from stack and form a string
    let mut numstr = "".to_string();
    while !rem_stack.is_empty() {
        numstr += digits[rem_stack.pop().unwrap() as usize];
```

```rust
    }

    numstr
}

fn main() {
    let num = 100;
    let sb = num2str_stk(100, 2);
    let so = num2str_stk(100, 8);
    let sh = num2str_stk(100, 16);
    println!("{num} = b{sb}, o{so}, x{sh}");
    // 100 = b1100100, o144, x64
}
```

### 5.2.3 Tower of Hanoi

The Tower of Hanoi puzzle was invented by French mathematician Edouard Lucas in 1883. The puzzle involves moving 64 gold discs of decreasing size from one of three poles to another, one disc at a time, with the constraint that a larger disc cannot be placed on a smaller one. The inspiration for this puzzle came from a legend about a puzzle given to young priests by the abbot of an Indian Hindu temple. In reality, moving all 64 discs would take 5.85 trillion years, longer than the known age of the universe. Figure (5.2) illustrates the process of moving disks from the first peg to the third peg, which resembles a stack. If you haven’t played this before, you can try it now. You don’t need disks, a pile of bricks, books, or paper will do, and you don’t need 64, 10 is enough. See if it really takes that long.

![Figure 5.2: Hanoi](images/fig-5.2.png)

*Figure 5.2: Hanoi*

To solve this problem recursively, we need to determine the base case. Suppose there is a tower of Hanoi with three pegs: left, middle, and right, and five disks on the left peg. We can assume that we know how to move one disk to the right. This is the base case. If we know how to move n-1 disks to the middle peg, we can easily move the bottom disk to the right peg and then move the n-1 disks from the middle peg to the right peg. If we don’t know how to move n-1 disks to the middle peg, we can assume that we know how to move n-2 disks to the middle peg, then move the n-1th disk to the right peg, and then move the n-2 disks from the middle peg to the top of the n-1th disk on the right peg. This process is an abstraction of the disk movement process. In summary, we can organize the above operation process into the following algorithm to solve the Tower of Hanoi puzzle recursively.

```text
Move height-1 disks to the middle peg using the target peg as a
    helper. Move the last disk to the target peg.
Move height-1 disks from the middle peg to the target peg using
    the starting peg as a helper.
```

To solve the Towers of Hanoi problem, the recursive three laws must be followed to ensure that larger discs remain at the bottom of the stack. The base case is when there is only one disc, which can be moved to its final destination. The algorithm then reduces the height of the Towers of Hanoi through steps 1 and 3, moving towards the base case. The solution can be implemented in a few lines of Rust code using recursion, as shown below.

```rust
// hanoi.rs

// p: pole
fn hanoi(height:u32, src_p:&str, des_p:&str, mid_p:&str) {
    if height >= 1 {
        hanoi(height - 1, src_p, mid_p, des_p);
        println!("move disk[{height}] from
                    {src_p} to {des_p}");
        hanoi(height - 1, mid_p, des_p, src_p);
    }
}

fn main() {
    hanoi(1, "A", "B", "C");
    hanoi(2, "A", "B", "C");
    hanoi(3, "A", "B", "C");
    hanoi(4, "A", "B", "C");
    hanoi(5, "A", "B", "C");
    hanoi(6, "A", "B", "C");
}
```

To simulate the problem, one can use three pens and paper to move the discs according to the output of the hanoi function for heights 1, 2, 3, and 4.

## 5.3 Tail Recursion

The aforementioned recursive computation is called regular recursion, which involves saving values during the computation process. This can lead to stack overflow if there are too many recursive calls and memory becomes limited. To avoid this, tail recursion can be used. Tail recursion processes the current result of the operation as a parameter for the next recursive function call, which reduces the memory consumption on the stack and makes the code more concise. Tail recursion optimization is particularly useful when dealing with subproblems that need to be summed. It reduces the problem size by calculating the sum of the parameters beforehand, which optimizes the algorithm. However, tail-recursive code may be more difficult to understand since the results of subproblems are directly used as parameters for the next recursive call. The regular recursive version of the code for summing the numbers can be converted into a more concise tail-recursive form.

```rust
// nums_sum34.rs

fn nums_sum3(sum: i32, nums: &[i32]) -> i32 {
    if 1 == nums.len() {
        sum + nums[0]
    } else {
        nums_sum3(sum + nums[0], &nums[1..])
    }
```

```rust
}

fn nums_sum4(sum: i32, nums: &[i32]) -> i32 {
    if 1 == nums.len() {
        sum + nums[0]
    } else {
        nums_sum4(sum + nums[nums.len() - 1],
                  &nums[..nums.len() - 1])
    }
}

fn main() {
    let nums = [2,1,7,4,5];
    let sum1 = nums_sum3(0, &nums);
    let sum2 = nums_sum4(0, &nums);
    println!("sum1 is {sum1}, sum2 is {sum2}");
    // sum1 is 19, sum2 is 19
}
```

Ultimately, the implementation of recursive programs depends on the programmer’s ability to write clear and efficient code. If tail recursion does not cause stack overflow and is easy to understand, it can be a useful tool in algorithm optimization.

### 5.3.1 Recursion VS Iteration

To compute the array [2, 1, 7, 4, 5], we employed three methods: loop iteration, recursion, and tail recursion. These methods demonstrate that recursion and iteration can accomplish the same goal. So, what is the relationship between recursion and iteration?

- Recursion refers to a process of repeating a transaction in a self-similar way. In mathematics and computer science, it involves using the function itself in its definition. When recursion is unfolded, it creates a tree-like structure. This can be thought of as a process of repetitive recursion and backtracking. Once the recursion reaches the bottom, backtracking begins, which is equivalent to a depth-first traversal of the tree.
- On the other hand, iteration involves repeating a feedback process, where the outcome of each iteration becomes the starting point for the next iteration. Iteration is a loop structure, starting from the initial state, where each iteration traverses the loop and updates the state. Multiple iterations continue until the end state is reached.

While all iterations can be converted into recursion, converting recursion to iteration is not always possible because changing a tree into a loop is not always feasible. Therefore, it is essential to choose the appropriate method for a given problem, taking into account its complexity, readability, and efficiency.

![Figure 5.3: Recursion VS Iteration](images/fig-5.3.png)

*Figure 5.3: Recursion VS Iteration*

## 5.4 Dynamic Programming

In computer science, optimization problems that involve finding the maximum or minimum value of a function are common. These problems are crucial for achieving carbon neutrality, saving energy, and improving the passenger experience. This section aims to demonstrate different solutions to optimization problems and highlight dynamic programming as an effective approach for solving such problems. A typical example of an optimization problem is the ”minimum number of bills/coins to make change” problem, commonly seen in subway ticketing and vending machines. The objective is to minimize the number of bills/coins returned for a single transaction. For example, returning two bills (a five and a one) for a six dollars transaction, instead of six one-dollar bills. The problem is how to plan the return of different denominations of bills/coins from a total task, such as making change for six dollars. The most intuitive approach is the greedy method, which starts with the largest denomination of bills/coins and uses as many of them as possible, then moves on to the next smaller denomination and repeats the process until the change is complete. However, the greedy method may not always yield the optimal solution. For instance, if a country has a complex currency system that includes not only the usual 1, 5, 10, and 25 dollar bills/coins, but also a 22 dollar bill/coin, the greedy method cannot find the best solution for making change for 66 dollars. Even with the addition of the 22 dollars bill/coin, the greedy method still finds a solution, but it requires five bills (two 25 dollar bills, one 10 dollar bill, one 5 dollar bill, and one 1 dollar bill), while the optimal answer is three 22 dollar bills. To solve the change-making problem, recursion is an effective method. The first step is to identify the basic problem, which is to make change for one bill/coin with an unspecified denomination but equal to the total amount needed. This is because making change with only one bill/coin represents the minimum number of bills/coins required except when the amount is zero. Assuming US dollars bills with denominations of 1, 5, 10, 20, and 50 dollar are used, the number of bills needed to make change for the original amount can be calculated by adding one to the number of bills needed for the remaining amount after subtracting the denomination from the total amount. Therefore, the formula for calculating the number of bills needed is straightforward.

numBills(amount) = { 1 + numBills(amount −1) 1 + numBills(amount −5) 1 + numBills(amount −10) 1 + numBills(amount −20) 1 + numBills(amount −50) (5.4)}

To implement this approach, the numBills function is used to calculate the number of bills required for a given amount of change. The function considers five cases, where the change can be made up of different denominations of bills. The algorithm checks if the change amount is equal to a denomination of bill on line 8, which serves as a base case. If not, the function recursively calls itself with a reduced change amount and the next smallest denomination of bill. The count of bills used is incremented before each recursive call to keep track of the total number of bills used in the final solution

```rust
// rec_mc1.rs

fn rec_mc1(cashes: &[u32], amount: u32) -> u32 {
    // Calculates the minimum number of coins required for
    // change when using only 1-yuan bills.
    let mut min_cashes = amount;

    if cashes.contains(&amount) {
        return 1;
    } else {
```

```rust
        // Extracts valid denominations (denominations must
        // be smaller than the change amount).
        for c in cashes.iter()
                       .filter(|&&c| c <= amount)
                       .collect::<Vec<&u32>>() {
            // Subtracts c from amount to indicate that a bill
            // of denomination c has been used,
            // and increments num_cashes by 1.
            let num_cashes = 1 + rec_mc1(&cashes, amount - c);

            // If num_cashes is smaller than min_cashes,
            // update min_cashes.
            if num_cashes < min_cashes {
                min_cashes = num_cashes;
            }
        }
    }

    min_cashes
}

fn main() {
    // cashes stores denominations of bills.
    let cashes = [1,5,10,20,50];
    let amount = 31u32;
    let cashes_num = rec_mc1(&cashes, amount);
    println!("need refund {cashes_num} cashes");
    // need refund 3 cashes
}
```

To avoid lengthy wait times for the program to return a result, it is important to optimize the code by reducing redundant calculations. In the given code, changing the amount to 90 results in a long wait time because the program needs to make a large number of recursive calls to find the combination of three bills: [50, 20, 20].

![Figure 5.4: solve the task by recursion](images/fig-5.4.png)

*Figure 5.4: solve the task by recursion*

To address this issue, one solution is to store previously calculated results to avoid redundant calculations. One approach is to store the current minimum number of bills in a list and check this list before calculating a new minimum value. If the result already exists, use the stored value instead of recalculating it. This technique is an example of trading space for time in algorithm design.

```rust
// rc_mc2.rs

fn rec_mc2(cashes: &[u32], amount: u32,
           min_cashes: &mut [u32]) -> u32
{
    // Calculates the minimum number of coins required for
    // change when using only 1-yuan bills.
    let mut min_cashe_num = amount;

    if cashes.contains(&amount) {
        // Collects denominations that match the
        // current change value.
        min_cashes[amount as usize] = 1;
        return 1;
    } else if min_cashes[amount as usize] > 0 {
        // If the change amount already has the minimum number
        // of coins required for change, return directly.
        return min_cashes[amount as usize];
    } else {
        for c in cashes.iter()
                       .filter(|&&c| c <= amount)
                       .collect::<Vec<&u32>>() {

            let cashe_num = 1 + rec_mc2(cashes,
                                        amount - c,
                                        min_cashes);

            // Updates the minimum number of coins
            // required for change.
            if cashe_num < min_cashe_num {
                min_cashe_num = cashe_num;
                min_cashes[amount as usize] = min_cashe_num;
            }
        }
    }

    min_cashe_num
}

fn main() {
    let amount = 90u32;
    let cashes: [u32; 5] = [1,5,10,20,50];
    let mut min_cashes: [u32; 91] = [0; 91];
    let cashe_num = rec_mc2(&cashes, amount, &mut min_cashes);
    println!("need refund {cashe_num} cashes");
    // need refund 3 cashes
}
```

The rec_mc2 is less time-consuming because it uses the variable min_cashes to store intermediate values. It is important to note that although this section discusses dynamic programming, both programs presented are recursive rather than dynamic programming. The second program only saves intermediate values during recursion, using a memory or cache technique to reduce the time required for calculations.

### 5.4.1 What is Dynamic Programming?

Dynamic programming(DP) is a mathematical technique for solving optimization problems in decisionmaking processes. The change-making problem described above is an optimization problem that seeks to minimize the number of bills/coins used, and this is the optimization objective. The key to dynamic programming is identifying whether a problem can be solved by this technique and expressing the problem as a state that can be transitioned between. The state is critical to the calculation and is used to derive the next step in the problem-solving process. Unlike the previous greedy algorithm, which goes from large to small denominations, dynamic programming assumes that the current best result has been obtained and deduces the next step based on this result. The technique decomposes a large problem into smaller sub-problems and deduces from small to large problems. The intermediate values of the deducing process are cached, and this process is known as state transition. For the change-making problem, three parameters are required for dynamic programming: a list of available bills, the amount to be changed, and a list that contains the minimum number of bills needed for each amount. The algorithm saves the calculated values to the list, starting from the smallest amount and gradually building up to the desired change amount. The implementation of the algorithm uses iteration. By using dynamic programming, redundant calculations can be avoided, and a significant improvement in efficiency can be achieved. The program caches previously calculated results, which reduces the workload and processing time.

```rust
// dp_rec_mc.rs

fn dp_rec_mc(cashes: &[u32], amount: u32,
             min_cashes: &mut [u32]) -> u32 {
    // Collect the minimum number of coins required to
    // make change from 1 to amount, and then reconstructs
    for denm in 1..=amount {
        let mut min_cashe_num = denm;
        for c in cashes.iter()
                       .filter(|&&c| c <= denm)
                       .collect::<Vec<&u32>>() {
            let index = (denm - c) as usize;
            let cashe_num = 1 + min_cashes[index];
            if cashe_num < min_cashe_num {
                min_cashe_num = cashe_num;
            }
        }
        min_cashes[denm as usize] = min_cashe_num;
    }
    // directly return the result
    min_cashes[amount as usize]
}

fn main() {
    let amount = 90u32;
    let cashes = [1,5,10,20,50];
    let mut min_cashes: [u32; 91] = [0; 91];
    let cash_num = dp_rec_mc(&cashes,amount,&mut min_cashes);
    println!("Refund for ${amount} need {cash_num} cashes");
    // Refund for $90 need 3 cashes
}
```

The iterative dynamic programming code is much more concise than the previous recursive versions and reduces the use of the stack. However, it is important to note that just because a problem can be solved using recursion does not mean it is the best solution. While the dynamic programming algorithm finds the minimum number of bills required, it does not indicate which denominations of bills are used. To obtain this information, a table, cashes_used, can be added to record the denominations and quantities of bills used. The algorithm can be extended by adding the denomination of the last bill used for each amount to the cashes_used table and then continuously finding the last bill used for the previous amount until the end.

```rust
// dp_rc_mc_show.rs

// The algorithm uses cashes_used to collect
// the denominations of coins used,
fn dp_rec_mc_show(cashes: &[u32], amount: u32,
                  min_cashes: &mut [u32],
                  cashes_used: &mut [u32]) -> u32 {
    for denm in 1..=amount {
        let mut min_cashe_num = denm ;
        // With a minimum denomination of 1 yuan
        let mut used_cashe = 1;
        for c in cashes.iter()
                       .filter(|&c| *c <= denm)
                       .collect::<Vec<&u32>>() {
            let index = (denm - c) as usize;
            let cashe_num = 1 + min_cashes[index];
            if cashe_num < min_cashe_num {
                min_cashe_num = cashe_num;
                used_cashe = *c;
            }
        }
        // update the minimum number of coins
        // required for each amount
        min_cashes[denm as usize] = min_cashe_num;
        cashes_used[denm as usize] = used_cashe;
    }

    min_cashes[amount as usize]
}

// prints the denominations of coins used
fn print_cashes(cashes_used: &[u32], mut amount: u32) {
    while amount > 0 {
        let curr = cashes_used[amount as usize];
        println!("${curr}");
        amount -= curr;
    }
}

fn main() {
    let amount = 81u32; let cashes = [1,5,10,20,50];
    let mut min_cashes: [u32; 82] = [0; 82];
    let mut cashes_used: [u32; 82] = [0; 82];
```

```rust
    let cs_num = dp_rec_mc_show(&cashes, amount,
                                &mut min_cashes,
                                &mut cashes_used);
    println!("Refund for ${amount} need {cs_num} cashes:");
    print_cashes(&cashes_used, amount);
}
```

For instance, when making change for 90 dollars, only three bills ([50, 20, 20]) are needed.

```text
Refund for $90 requires 3 cashes:
$20
$20
$50
```

### 5.4.2 Dynamic Programming VS Recursion

Recursion and dynamic programming are two different techniques used to solve problems. Recursion breaks down a large problem into smaller ones and solves them by calling itself, while dynamic programming solves large problems using solutions to smaller problems. Recursion can be memoryintensive and lead to stack overflow, while dynamic programming requires determining transition rules and initial conditions, but has simple code and a steep learning curve. Although both techniques can solve the same problems, such as the Fibonacci sequence problem.

```rust
// fibnacci_dp_rec.rs

fn fibnacci_dp(n: u32) -> u32 {
    // Using only two positions to store values can save memory
    let mut dp = [1, 1];
    for i in 2..=n {
        let idx1 = (i % 2) as usize;
        let idx2 = ((i - 1) % 2) as usize;
        let idx3 = ((i - 2) % 2) as usize;
        dp[idx1] = dp[idx2] + dp[idx3];
    }

    dp[((n-1) % 2) as usize]
}

fn fibnacci_rec(n: u32) -> u32 {
    if n == 1 || n == 2 {
        return 1;
    } else {
        fibnacci_rec(n-1) + fibnacci_rec(n-2)
    }
}

fn main() {
    println!("fib(10): {}", fibnacci_dp(10));
    println!("fib(10): {}", fibnacci_rec(10));
    // fib(10): 55
    // fib(10): 55
}
```

It is important to note that a problem that can be solved with dynamic programming may not necessarily be solvable with recursion as they have different requirements.

## 5.5 Summary

In this chapter, we covered both recursive and iterative algorithms. Recursive algorithms must satisfy three laws, and while recursion can sometimes replace iteration, it is not always the optimal solution. Recursion can be a natural way to express a problem, but tail recursion is an optimization technique that can reduce stack usage. Dynamic programming is a useful approach for solving optimization problems by breaking down large problems into smaller ones and gradually constructing larger solutions. While recursion solves problems by breaking them down, dynamic programming works by building up from small to large problems.
