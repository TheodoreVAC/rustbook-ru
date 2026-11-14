## 4.3 Stack

A stack is a linear data structure that has numerous applications, such as in function calls and webpage data recording. It is an ordered collection of data items where new items are added or removed from

the top, while the bottom refers to the opposite end. The bottom is significant because the items closest to it have been stored for the longest time, and the most recently added item will be the first one to be removed. This is known as the Last In First Out (LIFO) or First In Last Out (FILO) principle, which means that newer items are closer to the top, while older items are closer to the bottom. Stacks are ubiquitous in everyday life, like bricks on a construction site, books on a desk, and plates in a restaurant. To access the bottom brick, book, or plate, we need to remove the items on top first. The schematic diagram of a stack is shown below with some conceptual names.

![Figure 4.1: Stack](images/fig-4.1.png)

*Figure 4.1: Stack*

To understand the function of stacks, it is best to observe how they are formed and emptied. Suppose we stack books on a clean desktop one by one; we are creating a stack. Now, if we remove a book, the order of removal is opposite to the order in which the books were placed. The significance of stacks lies in their ability to reverse the order of items, inserting and deleting in the opposite order. The following diagram shows the process of creating and deleting data objects, with particular attention to the order of the data.

![Figure 4.2: Stack reverse order](images/fig-4.2.png)

*Figure 4.2: Stack reverse order*

The ability to reverse the order of items makes the reversal property of stacks particularly useful, as demonstrated in various computer applications. For instance, when browsing news on a web browser, the back function is implemented using a stack. As the user browses web pages, they are stacked, with the current page at the top and the first page at the bottom. Pressing the back button takes the user to the previous page in the opposite order. Without the power of stacks, designing this back function would be nearly impossible. This example highlights the importance of data structures in simplifying certain functions, as choosing the right data structure can make a significant difference.

### 4.3.1 The Stack Abstract Data Type

A stack is an abstract data type (ADT) that is defined by its structure and operations. It is an ordered collection of items where new items are added and removed from the top. The following operations can be performed on a stack:

- new(): creates an empty stack with no arguments and returns an empty stack.
- push(item): adds the data item ’item’ to the top of the stack, taking ’item’ as an argument and returning nothing.
- pop(): removes the top data item from the stack, taking no arguments and returning the data item. The stack is modified.
- peek(): returns the top data item from the stack without removing it, taking no arguments and not modifying the stack.
- is_empty(): tests if the stack is empty, taking no arguments and returning a Boolean value.
- size(): returns the number of data items in the stack as a ’usize’ integer, taking no arguments.
- iter(): returns an immutable iteration form of the stack, where the stack is not modified and takes no arguments.
- iter_mut(): returns a mutable iteration form of the stack, where the stack can be modified and takes no arguments.
- into_iter(): changes the stack into an iterable form, consuming the stack and taking no arguments.

To illustrate the stack operations, assume that ’s’ is an already created empty stack (represented as ’[]’ here), and the table below shows the results of stack operations, with the stack top on the right.

**Table 4.1: Stack Operations**

| Operation | Value | Return Value |
| --- | --- | --- |
| s.is_empty() | [] | true |
| s.push(1) | [1] |  |
| s.push(2) | [1,2] |  |
| s.peek() | [1,2] | 2 |
| s.push(3) | [1,2,3] |  |
| s.size() | [1,2,3] | 3 |
| s.is_empty() | [1,2,3] | false |
| s.push(4) | [1,2,3,4] |  |
| s.push(5) | [1,2,3,4,5] |  |
| s.size() | [1,2,3,4,5] | 5 |
| s.pop() | [1,2,3,4] | 5 |
| s.push(6) | [1,2,3,4,6] |  |
| s.peek() | [1,2,3,4,6] | 6 |

### 4.3.2 Implemeting a Stack in Rust

The abstract data type of a stack has been defined above, and now we will use Rust to implement it as a data structure. In Rust, abstract data types are implemented by creating a new struct and implementing the operations as functions of the struct. Using the basic data structures provided by Rust to implement a stack and its operations is very helpful. We will use the Vec collection container as the underlying implementation of the stack because it provides an ordered collection mechanism and a set of operation methods. To implement other operations, we only need to choose which end of the Vec is the top of the stack. The implementation assumes that the tail of Vec will save the top element, and as the stack grows, new items will be added to the end of Vec. Since the type of data to be inserted is unknown, we use the generic data type T. We have also added three structs, IntoIter, Iter, and IterMut, to complete the three types of iteration.

```rust
// stack.rs

#[derive(Debug)]
struct Stack<T> {
    size: usize, // stack size
    data: Vec<T>, // stack data
}

impl<T> Stack<T> {
    // initialize a stack
    fn new() -> Self {
        Self {
            size: 0,
            data: Vec::new()
        }
    }

    fn is_empty(&self) -> bool {
        0 == self.size
    }

    fn len(&self) -> usize {
        self.size
    }

    // clear stack
    fn clear(&mut self) {
        self.size = 0;
        self.data.clear();
    }

    // put the item into the tail of Vec
    fn push(&mut self, val: T) {
        self.data.push(val);
        self.size += 1;
    }

    // size decrease by 1 and then return the value
    fn pop(&mut self) -> Option<T> {
        if 0 == self.size {
            return None;
        }
        self.size -= 1;
        self.data.pop()
    }

    // return reference to the top value
    fn peek(&self) -> Option<&T> {
        if 0 == self.size {
            return None;
        }
```

```rust
        self.data.get(self.size - 1)
    }

    fn peek_mut(&mut self) -> Option<&mut T> {
        if 0 == self.size {
            return None;
        }

        self.data.get_mut(self.size - 1)
    }

    // Implementing iteration for stack
    // into_iter: stack modified and becomes a iterator
    // iter: stack unmodified and get a unmutable iterator
    // iter_mut: stack unmodified and get a mutable iterator
    fn into_iter(self) -> IntoIter<T> {
        IntoIter(self)
    }

    fn iter(&self) -> Iter<T> {
        let mut iterator = Iter { stack: Vec::new() };
        for item in self.data.iter() {
            iterator.stack.push(item);
        }

        iterator
    }

    fn iter_mut(&mut self) -> IterMut<T> {
        let mut iterator = IterMut { stack: Vec::new() };
        for item in self.data.iter_mut() {
            iterator.stack.push(item);
        }

        iterator
    }
}

// Implementation of 3 iterations
struct IntoIter<T>(Stack<T>);
impl<T: Clone> Iterator for IntoIter<T> {
    type Item = T;
    fn next(&mut self) -> Option<Self::Item> {
        if !self.0.is_empty() {
            self.0.size -= 1;
            self.0.data.pop()
        } else {
            None
        }
    }
}
```

```rust
struct Iter<'a, T: 'a> { stack: Vec<&'a T>, }
impl<'a, T> Iterator for Iter<'a, T> {
    type Item = &'a T;
    fn next(&mut self) -> Option<Self::Item> {
        self.stack.pop()
    }
}

struct IterMut<'a, T: 'a> { stack: Vec<&'a mut T> }
impl<'a, T> Iterator for IterMut<'a, T> {
    type Item = &'a mut T;
    fn next(&mut self) -> Option<Self::Item> {
        self.stack.pop()
    }
}

fn main() {
    basic();
    peek();
    iter();

    fn basic() {
        let mut s = Stack::new();
        s.push(1); s.push(2); s.push(3);

        println!("size: {}, {:?}", s.len(), s);
        println!("pop {:?}, size {}",s.pop().unwrap(), s.len())
           ; println!("empty: {}, {:?}", s.is_empty(), s);

        s.clear();
        println!("{:?}", s);
    }

    fn peek() {
        let mut s = Stack::new();
        s.push(1); s.push(2); s.push(3);

        println!("{:?}", s);
        let peek_mut = s.peek_mut();
        if let Some(top) = peek_mut {
            *top = 4;
        }

        println!("top {:?}", s.peek().unwrap());
        println!("{:?}", s);
    }

    fn iter() {
        let mut s = Stack::new();
        s.push(1); s.push(2); s.push(3);
```

```rust
        let sum1 = s.iter().sum::<i32>();
        let mut addend = 0;
        for item in s.iter_mut() {
            *item += 1;
            addend += 1;
        }

        let sum2 = s.iter().sum::<i32>();
        println!("{sum1} + {addend} = {sum2}");
        assert_eq!(9, s.into_iter().sum::<i32>());
    }
}
```

After executing the code, we obtain the following results.

```text
size: 3, Stack { size: 3, data: [1, 2, 3] }
pop 3, size 2
empty: false, Stack { size: 2, data: [1, 2] }
Stack { size: 0, data: [] }
Stack { size: 3, data: [1, 2, 3] }
top 4
Stack { size: 3, data: [1, 2, 4] }
6 + 3 = 9
```

### 4.3.3 Simple Balanced Parentheses

Previously, we implemented the stack data structure and now we will use it to solve the parenthesis matching problem. Arithmetic expressions that evaluate values contain parentheses as shown below. (5 + 6) × (7 + 8)/(4 + 3) Similarly, in the Lisp language, the multiply function shown below also has parentheses.

```text
(defun multiply(n)
    (* n n))
```

The focus here is on parentheses, as they alter the order of operations and constrain the language semantics. It is essential to ensure that the parentheses are complete; otherwise, the entire expression will be incorrect. Humans can quickly identify incomplete parenthesis, but how can a computer do this? Clearly, the computer must verify whether the parentheses match and report an error if they don’t. In both the examples above, the parentheses must appear in pairs. Parenthesis matching means that each opening symbol has a corresponding closing symbol, and the parentheses are correctly nested so that the computer can process them correctly. Consider the following correctly matched parenthesis strings and these mismatched parenthesis.

```text
(()()()())
(((())))
(()((())()))
((((((())
()))
(()()(()
```

To solve the parenthesis matching problem, a deeper understanding of brackets and their matching is needed. When processing symbols from left to right, the nearest left starting bracket ’(’ must match the next right closing symbol ’)’ (as shown in Figure 4.3). In addition, the first left starting bracket processed must wait until it matches the last right closing bracket. Ending brackets match starting brackets in the opposite order, from inside to outside. This is a problem that can be solved using a stack.

![Figure 4.3: Parenthesis matching](images/fig-4.3.png)

*Figure 4.3: Parenthesis matching*

Matching parenthesis is crucial in computer programs since it determines the next operation. The challenge is to write an algorithm that can read a string of symbols from left to right and determine whether the brackets match. Parenthesis and their matching are essential for computer programs since bracket and nesting are prevalent in programs. The implementation of the algorithm for matching parentheses using a stack is quite simple since it only involves push, pop, and judgment operations on the stack. To start, process the bracket string from left to right with an empty stack. If the symbol is a left starting symbol, push it onto the stack; if it is an ending symbol, pop the top element of the stack and match these two symbols. If they match, continue to process the next bracket until the string is completely processed. At the end of the processing, the stack should be empty; if not, it indicates that there are unmatched brackets. Here is a Rust implementation of the bracket matching program.

```rust
// par_checker1.rs

fn par_checker1(par: &str) -> bool {
    // adding characters into Vec
    let mut char_list = Vec::new();
    for c in par.chars() {
        char_list.push(c);
    }

    let mut index = 0;
    let mut balance = true; // determine if balanced
    let mut stack = Stack::new();
    while index < char_list.len() && balance {
        let c = char_list[index];

        if '(' == c { // if is '(', put data into stack
            stack.push(c);
        } else { // if is ')', determine if stack is empty
            if stack.is_empty() { // empty stack, matched
                balance = false;
            } else {
                let _r = stack.pop();
            }
        }

        index += 1;
    }
```

```rust
    // parenthesis matched: balanced and empty stack
    balance && stack.is_empty()
}

fn main() {
    let sa = "()(())";
    let sb = "()((()";
    let res1 = par_checker1(sa);
    let res2 = par_checker1(sb);
    println!("{sa} balanced:{res1}, {sb} balanced:{res2}");
    // ()(()) balanced:true, ()((() balanced:false
}
```

While the above example only involves matching the parentheses ’()’, there are actually three commonly used types of parentheses: ’()’, ’[]’, and ’{}’. These different types of left and right parentheses are often nested together, as shown in Rust, where square brackets ’[]’ are used for indexing, curly brackets ’{}’ are used for formatting output, and parentheses ’()’ are used for function parameters, tuples, mathematical expressions, and more. As long as each symbol maintains its own left starting and right ending relationship, mixed nesting symbols can be used.

```text
{ { ( [ ] [ ] ) } ( ) }
[ [ { { ( ( ) ) } } ] ]
[ ] [ ] [ ] ( ) { }
```

All of the parentheses shown above are matched. On the contrary, the following expression is not matched.

```text
( } [ ]
( ( ( ) ] ) )
[ { ( ) ]
```

To handle three types of parentheses, the previous parentheses checking program, par_checker1(only able to detect ’()’ parentheses), needs to be extended. However, the algorithm process remains the same. Each left starting parenthesis is pushed onto the stack, waiting for the matching right ending parenthesis to appear. When an ending parenthesis appears, the program checks whether the types of parentheses match. If the two parentheses do not match, then the string does not match. If the entire string has been processed and the stack is empty, then the parentheses expression matches. To detect whether the types of parentheses match, a new function called par_match() has been added. This function can detect the three commonly used types of parentheses. The detection principle is very simple: the program arranges the parentheses in order and checks whether their indices match.

```rust
// par_checker2.rs

// check if parentheses match of various symbols
fn par_match(open: char, close: char) -> bool {
    let opens = "([{";
    let closers = ")]}";
    opens.find(open) == closers.find(close)
}

fn par_checker2(par: &str) -> bool {
    let mut char_list = Vec::new();
```

```rust
    for c in par.chars() {
        char_list.push(c);
    }

    let mut index = 0;
    let mut balance = true;
    let mut stack = Stack::new();
    while index < char_list.len() && balance {
        let c = char_list[index];
        // check 3 open symbols simultaneously
        if '(' == c || '[' == c || '{' == c {
            stack.push(c);
        } else {
            if stack.is_empty() {
                balance = false;
            } else {
                // determine if match
                let top = stack.pop().unwrap();
                if !par_match(top, c) {
                    balance = false;
                }
            }
        }
        index += 1;
    }
    balance && stack.is_empty()
}

fn main() {
    let sa = "(){}[]";
    let sb = "(){)[}";
    let res1 = par_checker2(sa);
    let res2 = par_checker2(sb);
    println!("sa balanced:{res1}, sb balanced:{res2}");
    // (){}[] balanced:true, (){)[} balanced:false
}
```

The current implementation can handle different types of bracket matching problems. However, if the input expression contains non-bracket characters, the program will fail to work properly.

```text
(a+b)(c*d)func()
```

The apparent complexity of the problem can be deceiving because the actual issue is still related to detecting matching brackets. Hence, non-bracket characters can be skipped during processing. In the case of the given example, the non-bracket characters can be ignored, leaving only the brackets, resulting in the string: ()(){}(). The problem remains the same as before, and the code can be modified to detect matching brackets even in strings containing non-bracket characters. The following implementation is the modified code based on par_checker2.rs.

```rust
// par_checker3.rs

fn par_checker3(par: &str) -> bool {
    let mut char_list = Vec::new();
```

```rust
    for c in par.chars() { char_list.push(c); }

    let mut index = 0;
    let mut balance = true;
    let mut stack = Stack::new();
    while index < char_list.len() && balance {
        let c = char_list[index];
        // open mark, push
        if '(' == c || '[' == c || '{' == c {
            stack.push(c);
        }
        // close mark, determine if balanced
        if ')' == c || ']' == c || '}' == c {
            if stack.is_empty() {
                balance = false;
            } else {
                let top = stack.pop().unwrap();
                if !par_match(top, c) { balance = false; }
            }
        }
        // skip if not the bracket
        index += 1;
    }
    balance && stack.is_empty()
}

fn main() {
    let sa = "(2+3){func}[abc]"; let sb = "(2+3)*(3-1";
    let res1 = par_checker3(sa); let res2 = par_checker3(sb);
    println!("sa balanced:{res1}, sb balanced:{res2}");
 // (2+3){func}[abc] balanced:true, (2+3)*(3-1 balanced:false
}
```

### 4.3.4 Converting Decimal Numbers to Binary Numbers

Binary is a fundamental concept in the computer world, as it is the universal data format at the low-level of computing. All values stored in computers are in the form of 0s and 1s, making it critical to convert between binary numbers and ordinary characters for successful interaction with computers. Integer values are commonly used in computer programs and calculations, but we typically learn them in decimal form. For instance, decimal 233(10) can also be represented in binary as 11101001(2).

2 × 102 + 3 × 101 + 3 × 100 = 233 (4.1)

1 × 27 + 1 × 26 + 1 × 25 + 0 × 24 + 1 × 23 + 0 × 22 + 0 × 21 + 1 × 20 = 233 To convert an integer to binary, the ”divide by 2” algorithm (as shown in Figure 4.4) is a simple and effective method that involves using a stack to track the binary result’s digits. Starting with a positive integer greater than 0, the algorithm iteratively divides the decimal number by 2, keeping track of the remainders. The first remainder after dividing by 2 determines whether the value is even or odd, with an even number producing a remainder of 0 and an odd number resulting in a remainder of 1. By recording these remainders during the iteration and reversing the sequence, the binary digit sequence is obtained, with the first remainder (i.e., the last digit in the sequence) placed at the bottom of the stack. Popping all the digits from the stack results in the binary representation of the original decimal number.

![Figure 4.4: Divided by 2](images/fig-4.4.png)

*Figure 4.4: Divided by 2*

The function shown below takes a decimal parameter and uses Rust’s modulus operator (%) to extract the remainder, which is then pushed onto a stack. The parameter is repeatedly divided by 2 until it reaches 0, and the program constructs the binary representation of the original value.

```rust
// divide_by_two.rs

fn divide_by_two(mut dec_num: u32) -> String {
    // save the remainder in a stack
    let mut rem_stack = Stack::new();

    // push rem into the stack
    while dec_num > 0 {
        let rem = dec_num % 2;
        rem_stack.push(rem);
        dec_num /= 2;
    }

    // pop out elems from the stack to form a string
    let mut bin_str = "".to_string();
    while !rem_stack.is_empty() {
        let rem = rem_stack.pop().unwrap().to_string();
        bin_str += &rem;
    }
    bin_str
}

fn main() {
    let num = 10;
    let bin_str: String = divided_by_two(num);
    println!("{num} = b{bin_str}");
    // 10 = b1010
}
```

This algorithm for converting from decimal to binary can be extended to perform conversions between any two bases commonly used in computer science, such as binary, octal, and hexadecimal. For example, the decimal number 233(10) corresponds to 351(8) in octal and e9(16) in hexadecimal. To make the function more general, it can be modified to accept a predetermined conversion base,

replacing the concept of dividing by 2 with dividing by the conversion base. The remainders are still pushed onto a stack until the value being converted reaches 0. However, for bases greater than 10, remainders greater than 10 will inevitably occur, so it is best to represent them as a single character. In the base_converter function, we choose to use A-F to represent 10-15, but lowercase letters such as a-f or other character sequences can also be used.

```rust
// base_converter.rs

fn base_converter(mut dec_num: u32, base: u32) -> String {
    // digits is the string form of integers(especially for 10
       -15) let digits = ['0', '1', '2', '3', '4', '5', '6', '7',
                 '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'];
    let mut rem_stack = Stack::new();

    // push rem into the stack
    while dec_num > 0 {
        let rem = dec_num % base;
        rem_stack.push(rem);
        dec_num /= base;
    }

    // pop out elems from the stack to form a string
    let mut base_str = "".to_string();
    while !rem_stack.is_empty() {
        let rem = rem_stack.pop().unwrap() as usize;
        base_str += &digits[rem].to_string();
    }
    base_str
}

fn main() {
    let num1 = 10;
    let num2 = 43;
    let bin_str: String = base_converter(num1, 2);
    let hex_str: String = base_converter(num2, 16);
    println!("{num1} = b{bin_str}, {num2} = x{hex_str}");
    // 10 = b1010, 43 = x2B
}
```

### 4.3.5 Prefix, Infix, Postfix Expressions

In mathematics, an arithmetic expression, like B * C, has a specific format that makes it easy to understand. For instance, B multiplied by C, with the multiplication operator ”*” in between two operands, forms an infix expression. This type of expression is naturally easy to read and follow since it maintains the order of the expression. However, an infix expression like A + B * C, with the ”+” and ”*” operators sandwiched between operands, requires an understanding of operator priority to determine the order of operations. When operators of equal priority are present, they evaluate from left to right. Parentheses can alter the order of the operation, and arithmetic operator priority places multiplication and division before addition and subtraction. While humans can easily solve such expressions by mentally adding parentheses, computers require

specific algorithms to perform the same task. A computer can avoid confusion by using fully parenthesized expressions, where each operator has a pair of parentheses, indicating the order of the operation. However, processing these expressions can be difficult since computers work from left to right. Therefore, even simple tasks that seem easy for humans can be complex for computers, as they lack intelligence and the ability to understand expressions intuitively. To ensure that computers do not confuse the order of operations, a fully parenthesized expression can be used, where each operator is enclosed in a pair of parentheses indicating the order of operations. However, since computers process data from left to right, they may have difficulty jumping between inner and outer parentheses to calculate expressions like (A + (B * C)). While humans can do this intuitively, it is challenging for computers since they are rigid and require explicit instructions. A more intuitive method for computers is to separate the operator and operands by moving the operator outside the parentheses. This creates prefix and postfix expressions, which can be distinguished from the original infix expression. In prefix expressions, operators come before the operands, and in postfix expressions, operators come after the corresponding operands. Calculations are performed by taking the operator and operands, calculating the result as the current value, and then proceeding to subsequent operations until the expression is fully calculated. For example, the infix expression A + B can be written as + A B in prefix notation or A B + in postfix notation. By following the rules for each notation, readers can calculate more complex expressions in prefix or postfix notation and confirm the correct result.

**Table 4.2: Prefix-Infix-Postfix Expression**

| prefix | infix | postfix |
| --- | --- | --- |
| A + B | + A B | A B + |
| A + B * C | + A * B C | A B C * + |
| (A + B) * C | * + A B C | A B + C * |
| A + B - C | - + A B C | A B + C - |
| A * B + C | + * A B C | A B * C + |
| A * B / C | / * A B C | A B * C / |

To analyze complex expressions, readers must understand the importance of parentheses in expressing the order of operations. Even small changes in the placement of parentheses can result in vastly different expressions. While infix expressions require parentheses to disambiguate the order of operations, prefix and postfix expressions do not need them. This is because the order of operations is entirely determined by the position of operators in these notations. As a result, prefix and postfix expressions can clearly express the calculation logic without ambiguity, ensuring that calculations based on them are error-free. The table below shows some examples of complex expressions in different notations.

**Table 4.3: Complex Pre-In-Postfix Expressions**

| infix | prefix | postfix |
| --- | --- | --- |
| A + B * C - D | - + A * B C D | A B C * + D - |
| A * B - C / D | - * A B / C D | A B * C D / - |
| A + B + C + D | + + + A B C D | A B + C + D + |
| (A + B) * (C - D) | * + A B - C D | A B + C D - * |

Prefix and postfix expressions may appear more complicated to compute at first. For instance, the prefix expression ”+ A * B C” for ”A + B * C” requires calculating ”B * C” before adding it to A. However, the multiplication sign is still inside the addition operator, making it impossible to calculate. To resolve this issue, stacks can be used to reverse the order of operations. By pushing the operands and operators onto separate stacks from left to right, the order of operations can be reversed, as shown in Figure (4.5). This approach enables prefix and postfix expressions to be computed efficiently and accurately.

![Figure 4.5: Expressions on a stack](images/fig-4.5.png)

*Figure 4.5: Expressions on a stack*

To calculate expressions in prefix notation, the operator and operands are pushed onto separate stacks from left to right. To compute the expression, the top operator is popped from the operator stack, and the two top operands are popped from the operand stack. The operator is applied to these operands to obtain a result, which is then pushed back onto the operand stack. This process is repeated until the operator stack is empty. Finally, the top value in the operand stack is the result of the expression. This method is as efficient as fully bracketed expressions since the computer only needs to push and pop from the stacks, and does not need to handle parentheses, as shown in Figure (4.6).

![Figure 4.6: calculating expression by the stack](images/fig-4.6.png)

*Figure 4.6: calculating expression by the stack*

Similarly, postfix expressions can also be calculated using stacks. Only one stack is required to perform the calculation. For example, the postfix expression for A + B * C, which is A B C * +, is calculated by pushing A, B, and C onto the stack. When the * operator is encountered, the top two operands, B and C, are popped, multiplied, and pushed back onto the stack. Then, when the + operator is encountered, the top two operands, A and BC, are popped, added, and pushed back onto the stack, resulting in the final result of A + BC. This approach demonstrates the efficiency of stack-based computations, which can handle expressions in any notation without the need for parentheses.

### 4.3.6 Conversion of Infix Expressions to Prefix and Postfix

The calculation process demonstrated that converting infix expressions into prefix or postfix expressions is necessary to achieve efficiency. The first step in this process is to obtain prefix or postfix expressions, and a method to achieve this is through the use of fully bracketed expressions.

![Figure 4.7: infix to prefix and postfix](images/fig-4.7.png)

*Figure 4.7: infix to prefix and postfix*

For instance, A + B * C can be expressed as (A + (B * C)) to indicate that multiplication has a higher priority than addition. It is noteworthy that each pair of brackets represent the start and end of

an operand pair. The internal expression of (A + (B * C)) is (B * C), and by moving the multiplication symbol to the left bracket position and deleting the left and matching right brackets, the subexpression can be converted to a prefix expression. Similarly, by moving the addition operator to its corresponding left bracket position and deleting the matching right bracket, the complete prefix expression + A * B C can be obtained. By repeating this operation for all operators, the complete postfix expression can be obtained. To convert an expression, regardless of whether it is a prefix or postfix expression, the expression must first be converted into a fully bracketed expression based on the order of operations. Once the expression is fully bracketed, the operator inside the brackets can be moved to the position of the left or right bracket to achieve the desired notation. For example, the more complex expression (A + B) * C - (D + E) / (F + G) can be converted to a prefix or postfix expression using this method. Although the result may be complex for humans, computers can handle this process with ease.

![Figure 4.8: Infix to Prefix and Postfix](images/fig-4.8.png)

*Figure 4.8: Infix to Prefix and Postfix*

Obtaining a fully parenthesized expression is a difficult task, and it requires modifying the string by moving and deleting characters. Therefore, this method is not universal enough. A more convenient approach is to handle operators separately. When converting an infix expression, if the operands are not considered, they maintain their original relative positions, and only the operators change position. Therefore, it is not necessary to change the position of operands when encountering them; instead, only operators need to be handled when they are encountered. However, operators have priorities and often reverse the order. The characteristic of reversing the order is inherent to the stack data structure, which can be used to store operators. To convert an infix expression to a postfix expression, we can use a stack to store operators while scanning the expression from left to right. When an operand is encountered, it is added to the postfix expression. If an operator is encountered, we compare its priority with the operator at the top of the stack. If the current operator has higher priority, it is pushed onto the stack. If the current operator has lower or equal priority, we pop operators from the stack and add them to the postfix expression until we reach an operator with lower priority or an opening parenthesis. When we encounter a closing parenthesis, we pop operators from the stack and add them to the postfix expression until we reach the corresponding opening parenthesis, which is then discarded. The result is a postfix expression that can be evaluated efficiently. For example, to convert the infix expression (A + B) * C, we scan it from left to right. We first encounter the operand A, which is added to the postfix expression. Next, we encounter the operator +, which has lower priority than the opening parenthesis, so we push it onto the stack. We then encounter the operand B, which is added to the postfix expression. Finally, we encounter the closing parenthesis, so we pop the operator + from the stack and add it to the postfix expression, followed by the operator *. The resulting postfix expression is A B + C *. In the same way, we can convert the infix expression A * B + C * D to the postfix expression A B * C D * +, as shown in the figure below.

![Figure 4.9: Postfix expression by a stack](images/fig-4.9.png)

*Figure 4.9: Postfix expression by a stack*

To convert an infix expression to postfix notation, follow these steps: 1. Create an empty stack op_stack to hold operators, an empty list postfix to store the output. 2. Split the input infix string into tokens and store them in a list called src_str. 3. Iterate through the tokens in src_str from left to right: If the token is an operand, append it to the end of the postfix list. If the token is a left parenthesis, push it onto the op_stack. If the token is a right parenthesis, pop operators from op_stack and append them to postfix until the corresponding left parenthesis is removed. If the token is an operator (+, -, *, or /), push it onto the op_stack. However, first pop any higher or equal priority operators from op_stack and append them to postfix. 4. After processing the input, check the op_stack. Pop any remaining operators from the op_stack and append them to postfix. The final postfix list is the result of the conversion.

Algorithm 4.1: Algorithm: expression conversion from infix to postfix Input: infix expression

Output: postfix expression

1 Create an empty stack op_stack, an empty list postfix 2 Convert the input infix expression into a token list(src_str) 3 for c ∈src_str do if c ∈‘A −Z’ then 4 postfix.append(c) 5 else if c == ‘(’ then 6 op_stack.push(c) 7 else if c ∈‘ + −∗/’ then 8 while op_stack.peek() prior to c do 9 postfix.append(op_stack.pop()) 10 end 11 op_stack.push(c) 12 else if c == ‘)’ then 13 while op_stack.peek() != ‘(’ do 14 postfix.append(op_stack.pop()) 15 end 16 end 17 18 end 19 while !op_stack.is_empty() do postfix.append(op_stack.pop()) 20 21 end 22 return ‘ ’.join(postfix)

To convert an infix expression to postfix expression, we can use a HashMap named ”prec” to store the priority of operators. This HashMap maps each operator to an integer that is used to compare the priority of operators. The priority of parentheses is assigned the lowest value so that any operator compared with them has higher priority. Operators are limited to ”+-*/”, while operands are defined as uppercase letters A −Z or digits 0 −9.

```rust
// infix_to_postfix.rs
use std::collections::HashMap;

fn infix_to_postfix(infix: &str) -> Option<String> {
    // check parenthesis
    if !par_checker3(infix) {
        return None;
    }

    // set priority of all symbols
    let mut prec = HashMap::new();
    prec.insert("(", 1); prec.insert(")", 1);
    prec.insert("+", 2); prec.insert("-", 2);
    prec.insert("*", 3); prec.insert("/", 3);

    // ops: svae operators, postfix: svae postfix expression
    let mut ops = Stack::new();
    let mut postfix = Vec::new();
    for token in infix.split_whitespace() {
        // characters range from 0 - 9 and A-Z can
        // be pushed onto the stack
        if ("A" <= token && token <= "Z") ||
            ("0" <= token && token <= "9") {
            postfix.push(token);
        } else if "(" == token {
            // open mark, push onto the stack
            ops.push(token);
        } else if ")" == token {
            // close mark, pop out from stack
            let mut top = ops.pop().unwrap();
            while top != "(" {
                postfix.push(top);
                top = ops.pop().unwrap();
            }
        } else {
            // check the priority of operators
            while (!ops.is_empty()) &&
                (prec[ops.peek().unwrap()]
                                    >= prec[token]) {
                postfix.push(ops.pop().unwrap());
            }
            ops.push(token);
        }
    }

    // push the remaining operators onto the stack
```

```rust
    while !ops.is_empty() {
        postfix.push(ops.pop().unwrap())
    }
    // pop out operators and create the postfix expression
    let mut postfix_str = "".to_string();
    for c in postfix {
        postfix_str += &c.to_string();
        postfix_str += " ";
    }

    Some(postfix_str)
}

fn main() {
    let infix = "( A + B ) * ( C + D )";
    let postfix = infix_to_postfix(infix);
    match postfix {
        Some(val) => { println!("{infix} -> {val}"); },
        None => {
            println!("{infix} isn't a correct infix string");
        },
    }
    // ( A + B ) * ( C + D ) -> A B + C D + *
}
```

When calculating postfix expressions, special attention must be given to the ”-” and ”/” operators. Unlike the ”+” and ”*” operators, the order of operands matters for ”-” and ”/”. For example, A / B and B / A, A - B and B - A are completely different and cannot be handled like ”+”, and ”*”. Assuming the postfix expression is a space-separated string with operators ”+-*/” and operands as integers, the output is also an integer. The following are the algorithm steps for calculating postfix expressions: 1. Create an empty stack named op_stack. 2. Split the string into a list of symbols. 3. Scan the symbol list from left to right. If the symbol is an operand, convert it from a character to an integer and push the value onto op_stack. If the symbol is an operator, pop op_stack twice. The second pop is the first operand, and the first pop is the second operand. Perform the arithmetic operation and push the result back onto the operand stack. 4. When the entire input expression has been processed, the result is on the stack. Pop op_stack to get the final result of the operation.

![Figure 4.10: Evaluation of Postfix Expression](images/fig-4.10.png)

*Figure 4.10: Evaluation of Postfix Expression*

The specific steps for evaluating postfix expressions are shown in the above figure, and below is the implementation code.

```rust
// postfix_eval.rs

fn postfix_eval(postfix: &str) -> Option<i32> {
    // the expression needs at least two operands and
    // one operator, and two spaces to separate them.
    if postfix.len() < 5 { return None; }

    let mut ops = Stack::new();
    for token in postfix.split_whitespace() {
        // Strings can be compared directly
        if "0" <= token && token <= "9" {
            ops.push(token.parse::<i32>().unwrap());
        } else {
            // For subtraction and division, the order matters
            let op2 = ops.pop().unwrap();
            let op1 = ops.pop().unwrap();
            let res = do_calc(token, op1, op2);
            ops.push(res);
        }
    }
    // The value remained in the stack is the result
    Some(ops.pop().unwrap())
}

// Perform arithmetic operations
fn do_calc(op: &str, op1: i32, op2: i32) -> i32 {
    if "+" == op {
        op1 + op2
    } else if "-" == op {
        op1 - op2
    } else if "*" == op {
        op1 * op2
    } else if "/" == op {
        if 0 == op2 {
            panic!("ZeroDivisionError: Invalid operation!");
        }
        op1 / op2
    } else {
        panic!("OperatorError: Invalid operator: {:?}", op);
    }
}

fn main() {
    let postfix = "1 2 + 1 2 + *";
    let res = postfix_eval(postfix);
    match res {
        Some(val) => println!("res = {val}"),
        None => println!("{postfix} isn't a valid postfix"),
    }
    // res = 9
}
```
