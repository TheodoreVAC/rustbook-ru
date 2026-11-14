# Basic Data Structures

## 4.1 Objectives

- Understanding Abstract Data Types Vec, Stack, Queue, Deque, Linked List
- Being able to implement stack, queue, deque, and linked list using Rust
- Understanding the performance (complexity) of basic linear data structures
- Understanding prefix, infix, and postfix expression formats
- Using a stack to implement postfix expression and calculate the value
- Using a stack to convert infix expressions to postfix expressions
- Being able to identify whether to use a stack, queue, deque, or linked list for a given problem
- Being able to implement abstract data types as linked lists using nodes and references
- Being able to compare the performance of self-implemented Vec with Rust’s built-in Vec.

## 4.2 Linear Structures

Data structures are used to store data in a container, and there are several types of data structures available such as arrays, stacks, queues, dequeues, and linked lists. These data structures are called linear data structures because they maintain the order in which the data items are added or removed. Linear data structures have two ends, which can be named as the left and right or the front and back. The names are not important, but they indicate that the organization of data is linear, and this linear characteristic is related to memory, which is linear hardware. This relationship between software and hardware is important to understand. It is important to note that the term ”linear” in linear data structures does not refer to the way data is stored but rather to the way it is accessed. In a linked list, for example, data items may not be adjacent in memory, but the access is still linear. To differentiate between linear data structures, we need to look at the way items are added and removed, particularly their positions. Some data structures only allow adding items from one end, while others only allow removing items from the other end. Some data structures allow manipulation of data items from both ends. These variations and combinations have led to the creation of many useful data structures in computer science, which are used in various algorithms to perform important and practical tasks.

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

## 4.4 Queue

A queue is an ordered collection of items that has a front and a rear end. New items are added at the rear, and items are removed from the front. Each element added to the queue moves towards the front until it becomes the next item to be removed. This type of ordering is known as First In First Out (FIFO). A stack, in contrast, uses Last In First Out (LIFO) ordering. Queues are commonly used in everyday situations such as long lines of people waiting to board a train or bus, or at self-service restaurants. Queues have limited behavior because they have only one entrance and one exit. It is not possible to cut in line or leave early; one must wait for their turn. While it is true that real-life queues and queue data structures may allow cutting in line, this discussion does not consider that possibility. Operating systems use queues as a data structure to control processes. Multiple different queues are used in scheduling algorithms to prioritize executing programs as quickly as possible and service as many users as possible. When typing on a keyboard, a delay may occur before characters appear on the screen. This is because the keystrokes are placed in a buffer similar to a queue.

![Figure 4.11: Queue](images/fig-4.11.png)

*Figure 4.11: Queue*

### 4.4.1 The Queue Abstract Data Type

A queue is a data structure that maintains the FIFO sorting property. It is defined by the following structure and operations:

- new() creates a new queue, takes no parameters, and returns an empty queue.
- enqueue(item) adds a new item to the end of the queue, takes item as a parameter, no return.
- dequeue() removes an item from the front of the queue, takes no parameters, returns the removed item, and modifies the queue.
- is_empty() checks whether the queue is empty, takes no parameters, and returns a Boolean value.
- size() returns the number of items in the queue, takes no parameters, and returns a usize integer.
- iter() returns an immutable iteration of the queue, the queue remains unchanged, and takes no parameters.
- iter_mut() returns a mutable iteration of the queue, the queue is mutable, and takes no parameters.
- into_iter() changes the queue into an iteration, consumes the queue, and takes no parameters.

Assuming an empty queue q has already been created, the table below shows the expected results of various queue operations, with the front of the queue on the left:

**Table 4.4: Queue Operations**

| operation | value | return |
| --- | --- | --- |
| q.is_empty() | [] | true |
| q.enqueue(1) | [1] |  |
| q.enqueue(2) | [1,2] |  |
| q.enqueue(3) | [1,2,3] |  |
| q.dequeue() | [2,3] | 1 |
| q.enqueue(4) | [2,3,4] |  |
| q.enqueue(5) | [2,3,4,5] |  |
| q.deque() | [3,4,5] | 2 |
| q.size() | [3,4,5] | 3 |
| q.is_empty() | [3,4,5] | false |

### 4.4.2 Implementing a Queue in Rust

To implement a queue in Rust, we can use a Vec with the left end as the rear end of the queue and the right end as the front end. Adding an element to the queue has a complexity of O(n), while removing an element has a complexity of O(1). To prevent the queue from growing infinitely, we can set a cap parameter to limit its length.

```rust
// queue.rs

#[derive(Debug)]
struct Queue<T> {
    cap: usize, // capacity
    data: Vec<T>, // store elements
}

impl<T> Queue<T> {
    fn new(size: usize) -> Self {
        Self { cap: size, data: Vec::with_capacity(size) }
    }

    fn is_empty(&self) -> bool { 0 == Self::len(&self) }

    fn is_full(&self) -> bool { self.len() == self.cap }

    fn len(&self) -> usize { self.data.len() }

    fn clear(&mut self) {
        self.data = Vec::with_capacity(self.cap);
    }

    fn enqueue(&mut self, val: T) -> Result<(), String> {
        if self.len() == self.cap { // check left space
            return Err("No space available".to_string());
        }
        self.data.insert(0, val);
        Ok(())
    }

    // pop out values
    fn dequeue(&mut self) -> Option<T> {
        if self.len() > 0 {
            self.data.pop()
        } else {
            None
        }
    }

    // Implemntion of iterations for a queue
    // into_iter: queue modified and became a iterator
    // iter: queue unmodified and get a unmutable iterator
    // iter_mut: queue unmodified and get a mutable iterator
    fn into_iter(self) -> IntoIter<T> {
        IntoIter(self)
```

```rust
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

// Implemention of 3 iterations
struct IntoIter<T>(Queue<T>);
impl<T: Clone> Iterator for IntoIter<T> {
    type Item = T;
    fn next(&mut self) -> Option<Self::Item> {
        if !self.0.is_empty() {
            Some(self.0.data.remove(0))
        } else {
            None
        }
    }
}

struct Iter<'a, T: 'a> { stack: Vec<&'a T>, }
impl<'a, T> Iterator for Iter<'a, T> {
    type Item = &'a T;
    fn next(&mut self) -> Option<Self::Item> {
        if 0 != self.stack.len() {
            Some(self.stack.remove(0))
        } else {
            None
        }
    }
}

struct IterMut<'a, T: 'a> { stack: Vec<&'a mut T> }
impl<'a, T> Iterator for IterMut<'a, T> {
    type Item = &'a mut T;
    fn next(&mut self) -> Option<Self::Item> {
        if 0 != self.stack.len() {
            Some(self.stack.remove(0))
        } else {
            None
```

```rust
        }
    }
}
fn main() {
    basic();
    iter();
    fn basic() {
        let mut q = Queue::new(4);
        let _r1 = q.enqueue(1); let _r2 = q.enqueue(2);
        let _r3 = q.enqueue(3); let _r4 = q.enqueue(4);
        if let Err(error) = q.enqueue(5) {
            println!("Enqueue error: {error}");
        }
        if let Some(data) = q.dequeue() {
            println!("dequeue data: {data}");
        } else {
            println!("empty queue");
        }
        println!("empty: {}, len: {}", q.is_empty(), q.len());
        println!("full: {}", q.is_full());
        println!("q: {:?}", q);
        q.clear();
        println!("{:?}", q);
    }

    fn iter() {
        let mut q = Queue::new(4);
        let _r1 = q.enqueue(1); let _r2 = q.enqueue(2);
        let _r3 = q.enqueue(3); let _r4 = q.enqueue(4);
        let sum1 = q.iter().sum::<i32>();
        let mut addend = 0;
        for item in q.iter_mut() {
            *item += 1;
            addend += 1;
        }
        let sum2 = q.iter().sum::<i32>();
        println!("{sum1} + {addend} = {sum2}");
        println!("sum = {}", q.into_iter().sum::<i32>());
    }
}
```

Here is the result of the execution.

```text
Enqueue error: No space available
dequeue data: 1
empty: false, len: 3
full: false
q: Queue { cap: 4, data: [4, 3, 2] }
Queue { cap: 4, data: [] }
10 + 4 = 14
sum = 14
```

### 4.4.3 Hot Potato

A queue is commonly used to simulate real-world scenarios where data is processed in a FIFO (firstin, first-out) manner. For instance, the game of hot potato involves children forming a circle and passing a potato quickly to the child next to them, with the objective of keeping the potato moving as if it were hot (see Figure 4.12). When the passing action stops, the child holding the potato is removed from the circle. The game continues until only one child remains. The game is similar to musical chairs, where people perform an action such as speaking, dancing, or leaving their seat when the music stops.

![Figure 4.12: hot potato](images/fig-4.12.png)

*Figure 4.12: hot potato*

The game of hot potato is comparable to the Josephus problem, a legendary story recounted by the historian Flavius Josephus. Josephus and his comrades were trapped by the Roman army in a cave and chose to die instead of becoming Roman slaves. They formed a circle and counted clockwise to the eighth person, who was then killed. This continued until only one person was left alive. As a mathematician, Josephus figured out where he should sit to be the last person alive and ultimately joined the Roman side. While there are variations of this story, the fundamental ideas of both the hot potato game and the Josephus problem can be simulated using a queue.

![Figure 4.13: Simulation of game of hot potato](images/fig-4.13.png)

*Figure 4.13: Simulation of game of hot potato*

To implement the hot potato game, the program accepts multiple names of children and a constant num to set the count of how many children to skip before removing one. Assuming the child holding the hot potato is always at the front of the queue, they leave the queue and re-enter at the back, effectively passing the potato to the next child who must be at the front of the queue. After num rounds of dequeuing

and enqueuing, the child at the front of the queue is permanently removed. The process repeats until only one name remains. The queue model for the Hot Potato game is clearly illustrated in the two figures above. Here is the implementation of the game based on this model.

```rust
// hot_potato.rs

fn hot_potato(names: Vec<&str>, num: usize) -> &str {
    // Initialize the queue and enqueue the names
    let mut q = Queue::new(names.len());
    for name in names {
        let _nm = q.enqueue(name);
    }

    while q.size() > 1 {
        // Dequeue and enqueue the names,
        // which simulates passing the potato
        for _i in 0..num {
            let name = q.dequeue().unwrap();
            let _rm = q.enqueue(name);
        }

        // After num dequeue/enqueue cycles
        // remove one person
        let _rm = q.dequeue();
    }

    q.dequeue().unwrap()
}
fn main() {
    let name = vec!["Mon","Tom","Kew","Lisa","Marry","Bob"];
    let survivor = hot_potato(name, 8);
    println!("The survival person is {survivor}");
    // The survival person is Marry
}
```

It is worth noting that the counting value used in the implementation is 8, which is greater than the number of people in the queue (which is 6). However, this is not a problem because the queue functions like a circle that returns to the head after reaching the tail, and continues until the count is reached. Therefore, there will always be someone dequeued in the end.

## 4.5 Deque

A deque also is a linear data structure with two ends: the front and the rear. Unlike a queue, a deque allows items to be added and removed from both ends. This flexibility makes it a hybrid linear structure that can function as both a stack and a queue. Although a deque shares similarities with both a stack and a queue, it does not enforce LIFO or FIFO ordering. The order of adding and removing data determines whether it acts like a stack or a queue. It is important to note that a deque should not be used as a replacement for either a stack or a queue, as each data structure has its own unique properties and is designed for specific computational purposes. The image below provides an example of Deque.

![Figure 4.14: Deque](images/fig-4.14.png)

*Figure 4.14: Deque*

### 4.5.1 The Deque Abstract Data Type

The deque data structure is an ordered collection of items that allows adding and removing items from either end. It is defined by the following operations:

- new() creates a new deque with no arguments and returns an empty deque.
- add_front(item) adds item to the front of the deque, requiring item as a parameter, and does not return any content.
- add_rear(item) adds item to the back of the deque, requiring item as a parameter, and does not return any content.
- remove_front() removes the front item from the deque, requiring no arguments, returns item, and modifies the deque.
- remove_rear() removes the rear item from the deque, requiring no arguments, returns item, and modifies the deque.
- is_empty() tests whether the deque is empty, requires no arguments, and returns a boolean value.
- size() returns the number of items in the deque, requires no arguments, and returns a usize integer.
- iter() returns an immutable iteration form of the deque, with the deque unchanged and no arguments required.
- iter_mut() returns a mutable iteration form of the deque, with the deque mutable and no arguments required.
- into_iter() changes the deque into an iterable form, with the deque consumed and no arguments required.

Assuming that d is an already created empty deque, the following table shows the results of a series of operations. Note that the front is on the right-hand side. When moving items in and out, it is important to keep track of the front and back contents, as modifying both ends can make the result look somewhat messy.

**Table 4.5: Deque Operations**

| operations | value | return |
| --- | --- | --- |
| d.is_empty() | [] | true |
| d.add_rear(1) | [1] |  |
| d.add_rear(2) | [2,1] |  |
| d.add_front(3) | [2,1,3] |  |
| d.add_front(4) | [2,1,3,4] |  |
| d.remove_rear() | [1,3,4] | 2 |
| d.remove_front() | [1,3] | 4 |
| d.size() | [1,3] | 2 |
| d.is_empty() | [1,3] | false |
| d.add_front(2) | [1,3,2] |  |
| d.add_rear(4) | [4,1,3,2] |  |
| d.size() | [4,1,3,2] | 4 |
| d.is_empty() | [4,1,3,2] | false |
| d.add_rear(5) | [5,4,1,3,2] |  |
| d.add_front(10) | [5,4,1,3,2,10] |  |

### 4.5.2 Implementing a Deque in Rust

To implement the deque abstract data type in Rust, we can use a Vec as the underlying data structure. The left end of the Vec serves as the rear of the deque, while the right end serves as the front. To prevent the deque from growing indefinitely, a capacity parameter is added to control the maximum length of the deque.

```rust
// deque.rs

// deque definition
#[derive(Debug)]
struct Deque<T> {
    cap: usize, // capacity
    data: Vec<T>, // save elements in data
}

impl<T> Deque<T> {
    fn new(cap: usize) -> Self {
        Self {
            cap: cap,
            data: Vec::with_capacity(cap),
        }
    }

    fn is_empty(&self) -> bool {
        0 == self.len()
    }

    fn is_full(&self) -> bool {
        self.len() == self.cap
    }

    fn len(&self) -> usize {
        self.data.len()
    }

    fn clear(&mut self) {
        self.data = Vec::with_capacity(self.cap);
    }

    // use the tail of a Vec as the start of the deque
    fn add_front(&mut self, val: T) -> Result<(), String> {
        if self.len() == self.cap {
            return Err("No space avaliable".to_string());
        }
        self.data.push(val);

        Ok(())
    }

    // the head of the Vec is the tail of the deque
    fn add_rear(&mut self, val: T) -> Result<(), String> {
        if self.len() == self.cap {
```

```rust
            return Err("No space avaliabl".to_string());
        }
        self.data.insert(0, val);

        Ok(())
    }

    // remove data from queue head
    fn remove_front(&mut self) -> Option<T> {
        if self.len() > 0 {
            self.data.pop()
        } else {
            None
        }
    }

    // remove data from queue tail
    fn remove_rear(&mut self) -> Option<T> {
        if self.len() > 0 {
            Some(self.data.remove(0))
        } else {
            None
        }
    }

    // Implemention of iteration for the deque
    // into_iter: deque modified and became a iterator
    // iter: deque unmodified and get a unmutable iterator
    // iter_mut: deque unmodified and get a mutable iterator
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
```

```rust
// Implementing 3 iterations
struct IntoIter<T>(Deque<T>);
impl<T: Clone> Iterator for IntoIter<T> {
    type Item = T;
    fn next(&mut self) -> Option<Self::Item> {
        // first element of a tuple is not empty
        if !self.0.is_empty() {
            Some(self.0.data.remove(0))
        } else {
            None
        }
    }
}

struct Iter<'a, T: 'a> { stack: Vec<&'a T>, }
impl<'a, T> Iterator for Iter<'a, T> {
    type Item = &'a T;
    fn next(&mut self) -> Option<Self::Item> {
        if 0 != self.stack.len() {
            Some(self.stack.remove(0))
        } else {
            None
        }
    }
}

struct IterMut<'a, T: 'a> { stack: Vec<&'a mut T> }
impl<'a, T> Iterator for IterMut<'a, T> {
    type Item = &'a mut T;
    fn next(&mut self) -> Option<Self::Item> {
        if 0 != self.stack.len() {
            Some(self.stack.remove(0))
        } else {
            None
        }
    }
}

fn main() {
    basic();
    iter();

    fn basic() {
        let mut d = Deque::new(4);
        let _r1 = d.add_front(1);
        let _r2 = d.add_front(2);
        let _r3 = d.add_rear(3);
        let _r4 = d.add_rear(4);

        if let Err(error) = d.add_front(5) {
            println!("add_front error: {error}");
        }
```

```rust
        println!("{:?}", d);

        match d.remove_rear() {
            Some(data) => println!("remove rear data {data}"),
            None => println!("empty deque"),
        }

        match d.remove_front() {
            Some(data) => println!("remove front data {data}"),
            None => println!("empty deque"),
        }
        println!("empty: {}, len: {}", d.is_empty(), d.len());
        println!("full: {}, {:?}", d.is_full(), d);

        d.clear();
        println!("{:?}", d);
    }

    fn iter() {
        let mut d = Deque::new(4);
        let _r1 = d.add_front(1);
        let _r2 = d.add_front(2);
        let _r3 = d.add_rear(3);
        let _r4 = d.add_rear(4);

        let sum1 = d.iter().sum::<i32>();
        let mut addend = 0;
        for item in d.iter_mut() {
            *item += 1;
            addend += 1;
        }

        let sum2 = d.iter().sum::<i32>();
        println!("{sum1} + {addend} = {sum2}");
        assert_eq!(14, d.into_iter().sum::<i32>());
    }
}
```

Here is an example output of an execution.

```text
add_front error: No space avaliable
Deque { cap: 4, data: [4, 3, 1, 2] }
remove rear data 4
remove front data 2
empty: false, len: 2
full: false, Deque { cap: 4, data: [3, 1] }
Deque { cap: 4, data: [] }
10 + 4 = 14
```

As we can see from the output, a deque has similarities to both a queue and a stack, and can be thought of as a combination of the two. The specific implementation of a deque can vary depending on the situation, and which end is considered the front and which end is considered the rear should be determined based on the context.

### 4.5.3 Palindrome Checker

Palindromes are strings in which the characters at the same position from both ends are the same, such as ”radar”, ”sos”, and ”rustsur”. In this section, we will present an algorithm for checking whether a given string is a palindrome. One approach is to use a queue to enqueue the characters of the string and then dequeue the characters to compare them with the reversed original string. This method is simple, but it requires a lot of memory. A more efficient approach is to use a deque.

![Figure 4.15: Palindrome Checker](images/fig-4.15.png)

*Figure 4.15: Palindrome Checker*

To check for palindromes using a deque, we start by processing the input string from left to right and adding each character to the rear of the deque. At this point, the front of the deque holds the first character of the string, while the rear holds the last character. We can then use the deque’s feature of dequeuing from both ends to compare the front and rear characters. If they match, we continue dequeuing the front and rear characters until either all the characters are used up, leaving an empty deque, or a deque of size 1 is left. In both cases, the string is a palindrome. Any other situation indicates that the string is not a palindrome. Below is the code implementaion of palindrome detection using a deque.

```rust
// palindrome_checker.rs
fn palindrome_checker(pal: &str) -> bool {
    let mut d = Deque::new(pal.len());
    for c in pal.chars() {
        let _r = d.add_rear(c);
    }

    let mut is_pal = true;
    while d.size() > 1 && is_pal {
        let head = d.remove_front();
        let tail = d.remove_rear();
        if head != tail {
            is_pal = false;
        }
    }
    is_pal
}

fn main() {
    let pal = "rustsur";
    let is_pal = palindrome_checker(pal);
    println!("{pal} is palindrome string: {is_pal}");
    // rustsur is palindrome string: true

    let pal = "panda";
    let is_pal = palindrome_checker(pal);
    println!("{pal} is palindrome string: {is_pal}");
    // panda is palindrome string: false
}
```

## 4.6 LinkedList

An ordered collection of data items is important to maintain the relative position of data and efficient indexing. Arrays and linked lists both allow data to be collected in an ordered manner and saved in relative positions, making them suitable for implementing ordered data types. For example, Rust’s default implementation of Vec uses an array. This section focuses on linked lists, which offer some unique advantages. Unlike arrays, linked lists do not require elements to be stored in contiguous memory. Each item in the collection has a reference to the next item, so the items can be randomly placed without the need to allocate a block of memory, resulting in higher efficiency. To use a linked list, we need to specify the position of the first item explicitly. Once we know the position of the first item, we can determine the position of the second item and so on until the end of the entire linked list.

![Figure 4.16: Linked list](images/fig-4.16.png)

*Figure 4.16: Linked list*

Usually, linked lists provide a reference to the head of the list, and the last item must be set to null or an empty next item, also known as the tail. With this setup, we can easily traverse the linked list from the head to the tail, or vice versa, by following the references between items. This makes linked lists an efficient data structure for implementing other ordered data types.

### 4.6.1 The LinkedList Abstract Data Type

The abstract data type of a linked list consists of its structure and operations. As previously mentioned, a linked list is an ordered collection of nodes, and the entire list can be traversed from the head node. The structure of a linked list is simple, with each node containing an element and a reference to the next node. The following definitions and operations apply to a linked list:

- new(): Creates a new head node that points to a Node, takes no arguments, and returns a pointer.
- push(item): Adds a new Node, takes an item parameter, and returns None.
- pop(): Deletes the head node of the linked list, takes no arguments, and returns a Node.
- peek(): Returns a referent to the head node of the linked list, takes no arguments.
- peek_mut(): Returns the head node of the linked list, takes no arguments, and returns a mutable reference to the node.
- is_empty(): Returns a Boolean value indicating whether the current linked list is empty, takes no arguments.
- size(): Returns the length of the linked list as a usize integer value, takes no arguments.
- iter(): Returns an immutable iteration of the linked list without modifying the linked list, takes no arguments.
- iter_mut(): Returns a mutable iteration of the linked list with the linked list mutable, takes no arguments.
- into_iter(): Consumes the linked list and returns an iterable form of the linked list, takes no arguments.

Assuming that l is an empty linked list, the table below shows the result of a sequence of linked list operations, with Link<num> representing the address pointing to the node containing num, and the left end of the list being the head node.

**Table 4.6: LinkedList Operations**

| Operation | Value | Return |
| --- | --- | --- |
| l.is_empty() | [None->None] | true |
| l.push(1) | [1->None] |  |
| l.push(2) | [2->1->None] |  |
| l.push(3) | [3->2->1->None] |  |
| l.peek() | [3->2->1->None] | Link<3> |
| l.pop() | [2->1->None] | 3 |
| l.size() | [2->1->None] | 2 |
| l.push(4) | [4->2->1->None] |  |
| l.peek_mut() | [4->2->1->None] | mut Link<4> |
| l.iter() | [4->2->1->None] | [4,2,1] |
| l.is_empty() | [4->2->1->None] | false |
| l.size() | [4->2->1->None] | 3 |
| l.into_iter() | [None->None] | [4,2,1] |

### 4.6.2 Implementing a LinkedList in Rust

To represent an item in a linked list, we use a node abstraction that includes the data item and the address of the next item. The node also provides methods to access and modify the data item. As shown in the figure below, a Node consists of data and the address of the next node.

![Figure 4.17: Node](images/fig-4.17.png)

*Figure 4.17: Node*

In Rust, None is used to represent the absence of a next node in both the Node and the linked list. The new function initializes a grounded node with its next field set to None. Explicitly assigning None to the next field is a good practice that helps avoid dangling pointers, a common issue in languages like C/C++.

![Figure 4.18: LinkedList](images/fig-4.18.png)

*Figure 4.18: LinkedList*

The following code shows the implementation of the linked list, with the node link defined as Link for code clarity.

```rust
// linked_list.rs

// The node link uses a Box pointer (size determined),
// because only with a determined size can memory be allocated.
type Link<T> = Option<Box<Node<T>>>;
```

```rust
// Linked list definition
struct List<T> {
    size: usize, // Number of nodes in the linked list
    head: Link<T>, // Head node
}

// Linked list node
struct Node<T> {
    elem: T, // data
    next: Link<T>, // Link to the next node
}

impl<T> List <T> {
    fn new() -> Self {
        Self {
            size: 0,
            head: None
        }
    }

    fn is_empty(&self) -> bool { 0 == self.size }

    fn len(&self) -> usize { self.size }

    fn clear(&mut self) {
        self.size = 0;
        self.head = None;
    }

    // add a new node ahead of the head node
    fn push(&mut self, elem: T) {
        let node = Box::new(Node {
            elem: elem,
            next: self.head.take(),
        });
        self.head = Some(node);
        self.size += 1;
    }

    // take will move data out from node and left a vaccum
    fn pop(&mut self) -> Option<T> {
        self.head.take().map(|node| {
            self.head = node.next;
            self.size -= 1;
            node.elem
        })
    }

    // peek get a unmutable reference
    fn peek(&self) -> Option<&T> {
        self.head.as_ref().map(|node| &node.elem )
    }
```

```rust
    // peek_mut get a mutable reference
    fn peek_mut(&mut self) -> Option<&mut T> {
        self.head.as_mut().map(|node| &mut node.elem )
    }

    // Implementation of iteration for the linked list.
    // into_iter: makes the linked list an iterator
    // by consuming it
    // iter: returns an immutable iterator without modifying
    // the linked list
    // iter_mut: returns a mutable iterator without modifying
    // the linked list
    fn into_iter(self) -> IntoIter<T> {
        IntoIter(self)
    }

    fn iter(&self) -> Iter<T> {
        Iter { next: self.head.as_deref() }
    }

    fn iter_mut(&mut self) -> IterMut<T> {
        IterMut { next: self.head.as_deref_mut() }
    }
}

// Implementation of three iterations
struct IntoIter<T>(List<T>);
impl<T> Iterator for IntoIter<T> {
    type Item = T;
    fn next(&mut self) -> Option<Self::Item> {
        // (List<T>) tuple's 0th item
        self.0.pop()
    }
}

struct Iter<'a, T: 'a> { next: Option<&'a Node<T>> }
impl<'a, T> Iterator for Iter<'a, T> {
    type Item = &'a T;
    fn next(&mut self) -> Option<Self::Item> {
        self.next.map(|node| {
            self.next = node.next.as_deref();
            &node.elem
        })
    }
}

struct IterMut<'a, T: 'a> { next: Option<&'a mut Node<T>> }
impl<'a, T> Iterator for IterMut<'a, T> {
    type Item = &'a mut T;
    fn next(&mut self) -> Option<Self::Item> {
        self.next.take().map(|node| {
```

```rust
            self.next = node.next.as_deref_mut();
            &mut node.elem
        })
    }
}

// Custom implementation of Drop for the linked list
impl<T> Drop for List<T> {
    fn drop(&mut self) {
        let mut link = self.head.take();
        while let Some(mut node) = link {
            link = node.next.take();
        }
    }
}

fn main() {
    basic_test();
    into_iter_test();
    iter_test();
    iter_mut_test();

    fn basic_test() {
        let mut list = List::new();
        list.push(1); list.push(2); list.push(3);

        assert_eq!(list.len(), 3);
        assert_eq!(list.is_empty(), false);
        assert_eq!(list.pop(), Some(3));
        assert_eq!(list.peek(), Some(&2));
        assert_eq!(list.peek_mut(), Some(&mut 2));

        list.peek_mut().map(|val| {
            *val = 4;
        });

        assert_eq!(list.peek(), Some(&4));
        list.clear();
        println!("basics test Ok!");
    }

    fn into_iter_test() {
        let mut list = List::new();
        list.push(1); list.push(2); list.push(3);

        let mut iter = list.into_iter();
        assert_eq!(iter.next(), Some(3));
        assert_eq!(iter.next(), Some(2));
        assert_eq!(iter.next(), Some(1));
        assert_eq!(iter.next(), None);

        println!("into_iter test Ok!");
```

```rust
    }

    fn iter_test() {
        let mut list = List::new();
        list.push(1); list.push(2); list.push(3);

        let mut iter = list.iter();
        assert_eq!(iter.next(), Some(&3));
        assert_eq!(iter.next(), Some(&2));
        assert_eq!(iter.next(), Some(&1));
        assert_eq!(iter.next(), None);
        println!("iter test Ok!");
    }

    fn iter_mut_test() {
        let mut list = List::new();
        list.push(1); list.push(2); list.push(3);

        let mut iter = list.iter_mut();
        assert_eq!(iter.next(), Some(&mut 3));
        assert_eq!(iter.next(), Some(&mut 2));
        assert_eq!(iter.next(), Some(&mut 1));
        assert_eq!(iter.next(), None);
        println!("iter_mut test Ok!");
    }
}
```

### 4.6.3 LinkedList Stack

To implement a stack, we can also use a linked list, which is another type of linear data structure. In this case, we can use the head of the linked list to store the top element of the stack. As new items are added to the stack, they will be inserted at the head of the linked list. The implementation for this approach is shown below. Note that since the push and pop functions modify the linked list nodes, we use the take function to extract the node value.

```rust
// list_stack.rs

// Linked List Node
#[derive(Debug, Clone)]
struct Node<T> {
    data: T,
    next: Link<T>,
}

// Node Self-contained Reference
type Link<T> = Option<Box<Node<T>>>;

impl<T> Node<T> {
    fn new(data: T) -> Self {
        Self {
            data: data,
            next: None // No next link when initialized
```

```rust
        }
    }
}

// Linked list stack
#[derive(Debug, Clone)]
struct LStack<T> {
    size: usize,
    top: Link<T>, // Top controls the entire stack
}

impl<T: Clone> LStack<T> {
    fn new() -> Self {
        Self {
            size: 0,
            top: None
        }
    }

    fn is_empty(&self) -> bool {
        0 == self.size
    }

    fn len(&self) -> usize {
        self.size
    }

    fn clear(&mut self) {
        self.size = 0;
        self.top = None;
    }

    // take out the node on the top, leaving an empty space
    // that could be filled later
    fn push(&mut self, val: T) {
        let mut node = Node::new(val);
        node.next = self.top.take();
        self.top = Some(Box::new(node));
        self.size += 1;
    }

    fn pop(&mut self) -> Option<T> {
        self.top.take().map(|node| {
            let node = *node;
            self.top = node.next;
            self.size -= 1;
            node.data
        })
    }

    // Return a reference to the data in the linked list stack
    fn peek(&self) -> Option<&T> {
```

```rust
        self.top.as_ref().map(|node| &node.data)
    }

    fn peek_mut(&mut self) -> Option<&mut T> {
        self.top.as_deref_mut().map(|node| &mut node.data)
    }

    // into_iter: the linked list stack changes
    // iter: the linked list stack remains unchanged
    // iter_mut: the linked list stack remains unchanged
    fn into_iter(self) -> IntoIter<T> {
        IntoIter(self)
    }

    fn iter(&self) -> Iter<T> {
        Iter { next: self.top.as_deref() }
    }

    fn iter_mut(&mut self) -> IterMut<T> {
        IterMut { next: self.top.as_deref_mut() }
    }
}

// Implement three iterations
struct IntoIter<T: Clone>(LStack<T>);
impl<T: Clone> Iterator for IntoIter<T> {
    type Item = T;
    fn next(&mut self) -> Option<Self::Item> {
        self.0.pop()
    }
}

struct Iter<'a, T: 'a> { next: Option<&'a Node<T>> }
impl<'a, T> Iterator for Iter<'a, T> {
    type Item = &'a T;
    fn next(&mut self) -> Option<Self::Item> {
        self.next.map(|node| {
            self.next = node.next.as_deref();
            &node.data
        })
    }
}

struct IterMut<'a, T: 'a> { next: Option<&'a mut Node<T>> }
impl<'a, T> Iterator for IterMut<'a, T> {
    type Item = &'a mut T;
    fn next(&mut self) -> Option<Self::Item> {
        self.next.take().map(|node| {
            self.next = node.next.as_deref_mut();
            &mut node.data
        })
    }
```

```rust
}

fn main() {
    basic();
    iter();

    fn basic() {
        let mut s = LStack::new();
        s.push(1); s.push(2); s.push(3);

        println!("empty: {:?}", s.is_empty());
        println!("top: {:?}, size: {}", s.peek(), s.len());
        println!("pop: {:?}, size: {}", s.pop(), s.len());

        let peek_mut = s.peek_mut();
        if let Some(data) = peek_mut {
            *data = 4
        }
        println!("top {:?}, size {}", s.peek(), s.len());

        println!("{:?}", s);
        s.clear();
        println!("{:?}", s);
    }

    fn iter() {
        let mut s = LStack::new();
        s.push(1); s.push(2); s.push(3);

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

The output of the code will depend on how the stack is used and what functions are called.

```text
empty: false
top: Some(3), size: 3
pop: Some(3), size: 2
top Some(4), size 2
LStack { size: 2, top: Some(Node { data: 4,
         next: Some(Node { data: 1, next: None }) }) }
LStack { size: 0, top: None }
6 + 3 = 9
```

## 4.7 Vec

In this chapter, we have demonstrated how the basic data type Vec can be used to implement various abstract data types, including stacks, queues, deques, and linked lists. Vec is a powerful yet simple data container that offers mechanisms for data collection and various operations, which is why we repeatedly use it as the underlying data structure for implementing other data types. It is similar to Python’s List and is very convenient to use. However, not all programming languages include Vec, or not all data types may be suitable for it. In some cases, Vec or similar data containers must be implemented separately by programmers.

### 4.7.1 The Vec Abstract Data Type

Vec is a collection of items that maintain a relative position to other items. Here are the various operations of the Vec abstract data type:

- new(): Creates a new empty Vec, takes no arguments.
- push(item): Adds the item to the end of the Vec, takes item as a parameter.
- pop(): Deletes the last item in the Vec and returns it, take no arguments.
- insert(pos, item): Inserts the item at position pos in the Vec, takes pos and item parameters.
- remove(idx): Removes the item at index idx from the Vec and returns it, takes a parameter.
- find(item): Checks if the item exists in the Vec and returns a boolean value, takes an item parameter.
- is_empty(): Checks if the Vec is empty and returns a boolean value, takes no arguments.
- size(): Calculates the number of items in the Vec and returns a usize integer, takes no arguments.
- iter(): Returns an immutable iteration form of the Vec.
- iter_mut(): Returns a mutable iteration form of the Vec, takes no arguments.
- into_iter(): Consumes the Vec and returns an iterable form of the Vec, takes no arguments.

Assuming v is an empty Vec that has been created, the table below shows the Vec after different operations, with the left side being the head.

**Table 4.7: Operations on a Vec**

| operation | value | return |
| --- | --- | --- |
| v.is_empty() | [] | true |
| v.push(1) | [1] |  |
| v.push(2) | [1,2] |  |
| v.push(3) | [1,2,3] |  |
| v.size() | [1,2,3] | 3 |
| v.pop() | [1,2] | 3 |
| v.push(5) | [1,2,5] |  |
| v.find(4) | [1,2,5] | false |
| v.insert(0,8) | [8,1,2,5] |  |
| v.pop() | [8,1,2] | 5 |
| v.remove(0) | [1,2] | 8 |
| v.size() | [1,2] | 2 |

Finally, it is worth noting that while Vec is a powerful data structure, it may not always be the best choice for a particular use case. Programmers should carefully consider the requirements of their project and choose the appropriate data structure accordingly.

### 4.7.2 Implementing a Vec in Rust

Vec is composed of linked list nodes, where each node contains a data item and an explicit reference to the next node. Given the location of the first node, subsequent items can be accessed by following the next link.

Since references play a crucial role in Vec, it is necessary to maintain a reference to the first node. The linked list is created with None indicating that the list does not reference any content, as shown in Figure (4.19). The head of the linked list refers to the first node of the list, which stores the address of the next node. It is important to note that the Vec itself does not contain any node objects but only a reference to the first node in the linked list structure.

![Figure 4.19: LinkedList Formed Vec](images/fig-4.19.png)

*Figure 4.19: LinkedList Formed Vec*

To add a new item to the linked list, the only entry point is through the head of the list. As all other nodes can only be accessed by following the next link from the first node, the most efficient way to add a new node is to add it to the head of the linked list. This approach adds the new item as the first element, with the existing items linked to it. While the implementation of Vec presented here is unordered, it is possible to implement an ordered Vec using a data comparison function with total or partial orders. The following LVec provides only a portion of the functionality of the standard library Vec, and print_lvec is used to print its data items.

```rust
// lvec.rs

use std::fmt::Debug;

#[derive(Debug)]
struct Node<T> {
    elem: T,
    next: Link<T>,
}

type Link<T> = Option<Box<Node<T>>>;

impl<T> Node<T> {
    fn new(elem: T) -> Self {
        Self {
            elem: elem,
            next: None
        }
    }
}

// LinkedList Vec definition
#[derive(Debug)]
struct LVec<T> {
    size: usize,
    head: Link<T>,
}

impl<T: Copy + Debug> LVec<T> {
    fn new() -> Self {
        Self { size: 0, head: None }
```

```rust
    }

    fn is_empty(&self) -> bool {
        0 == self.size
    }

    fn len(&self) -> usize {
        self.size
    }

    fn clear(&mut self) {
        self.size = 0;
        self.head = None;
    }

    fn push(&mut self, elem: T) {
        let node = Node::new(elem);
        if self.is_empty() {
            self.head = Some(Box::new(node));
        } else {
            let mut curr = self.head.as_mut().unwrap();

            // find the last node in the list
            for _i in 0..self.size-1 {
                curr = curr.next.as_mut().unwrap();
            }

            // insert the new data after the last node
            curr.next = Some(Box::new(node));
        }
        self.size += 1;
    }

    // add a new LVec to the end of the stack
    fn append(&mut self, other: &mut Self) {
        while let Some(node) = other.head.as_mut().take() {
            self.push(node.elem);
            other.head = node.next.take();
        }
        other.clear();
    }

    fn insert(&mut self, mut index: usize, elem: T) {
        if index >= self.size { index = self.size; }

        // three cases for inserting a new node
        let mut node = Node::new(elem);
        if self.is_empty() { // LVec is empty
            self.head = Some(Box::new(node));
        } else if index == 0 { // insert at the beginning of
           the list node.next = self.head.take();
```

```rust
            self.head = Some(Box::new(node));
        } else { // insert int the middle of the list
            let mut curr = self.head.as_mut().unwrap();
            for _i in 0..index - 1 { // find the right insert
               position curr = curr.next.as_mut().unwrap();
            }
            node.next = curr.next.take();
            curr.next = Some(Box::new(node));
        }
        self.size += 1;
    }

    fn pop(&mut self) -> Option<T> {
        if self.size < 1 {
            return None;
        } else {
            self.remove(self.size - 1)
        }
    }

    fn remove(&mut self, index: usize) -> Option<T> {
        if index >= self.size { return None; }

        // two cases for deleting a node
        let mut node;
        if 0 == index {
            node = self.head.take().unwrap();
            self.head = node.next.take();
        } else { // find the position which will be deleteed
           and arrange the links properly let mut curr = self.head.as_mut().unwrap();
            for _i in 0..index - 1 {
                curr = curr.next.as_mut().unwrap();
            }
            node = curr.next.take().unwrap();
            curr.next = node.next.take();
        }
        self.size -= 1;

        Some(node.elem)
    }

   fn into_iter(self) -> IntoIter<T> {
        IntoIter(self)
    }

    fn iter(&self) -> Iter<T> {
        Iter { next: self.head.as_deref() }
    }

    fn iter_mut(&mut self) -> IterMut<T> {
```

```rust
        IterMut { next: self.head.as_deref_mut() }
    }

    // print LVec
    fn print_lvec(&self) {
        if 0 == self.size {
            println!("Empty lvec");
        }
        for item in self.iter() {
            println!("{:?}", item);
        }
    }
}

// Implemtion of three iterations
struct IntoIter<T: Copy + Debug >(LVec<T>);
impl<T: Copy + Debug> Iterator for IntoIter<T> {
    type Item = T;
    fn next(&mut self) -> Option<Self::Item> {
        self.0.pop()
    }
}

struct Iter<'a, T: 'a> { next: Option<&'a Node<T>> }
impl<'a, T> Iterator for Iter<'a, T> {
    type Item = &'a T;
    fn next(&mut self) -> Option<Self::Item> {
        self.next.map(|node| {
            self.next = node.next.as_deref();
            &node.elem
        })
    }
}

struct IterMut<'a, T: 'a> { next: Option<&'a mut Node<T>> }
impl<'a, T> Iterator for IterMut<'a, T> {
    type Item = &'a mut T;
    fn next(&mut self) -> Option<Self::Item> {
        self.next.take().map(|node| {
            self.next = node.next.as_deref_mut();
            &mut node.elem
        })
    }
}

fn main() {
    basic();
    iter();

    fn basic() {
        let mut lvec1: LVec<i32> = LVec::new();
        lvec1.push(10); lvec1.push(11);
```

```rust
        lvec1.push(12); lvec1.push(13);
        lvec1.insert(0,9);

        lvec1.print_lvec();

        let mut lvec2: LVec<i32> = LVec::new();
        lvec2.insert(0, 8);
        lvec2.append(&mut lvec1);

        println!("len: {}", lvec2.len());
        println!("pop {:?}", lvec2.pop().unwrap());
        println!("remove {:?}", lvec2.remove(0).unwrap());

        lvec2.print_lvec();
        lvec2.clear();
        lvec2.print_lvec();
    }

    fn iter() {
        let mut lvec: LVec<i32> = LVec::new();
        lvec.push(10); lvec.push(11);
        lvec.push(12); lvec.push(13);

        let sum1 = lvec.iter().sum::<i32>();
        let mut addend = 0;
        for item in lvec.iter_mut() {
            *item += 1;
            addend += 1;
        }
        let sum2 = lvec.iter().sum::<i32>();
        println!("{sum1} + {addend} = {sum2}");

        assert_eq!(50, lvec.into_iter().sum::<i32>());
    }
}
```

Here is the execution result.

```text
9
10
11
12
13
len: 6
pop 13
remove 8
9
10
11
12
Empty lvec
46 + 4 = 50
```

It’s important to note that LVec is a linked list with n nodes, and any method that requires traversing nodes, such as insert, push, pop, remove, etc., has a time complexity of O(n). Although on average it may only require traversing half as many nodes, in the worst case, every node in the list must be processed.

## 4.8 Summary

This chapter focuses on several linear data structures, including stack, queue, double-ended queue, linkedList, and Vec. A stack is a type of data structure that maintains last-in-first-out (LIFO) ordering and has basic operations such as push, pop, and is_empty. Stacks are useful for designing algorithms that compute parsed expressions and can provide inversion properties that are useful in implementing operating system function calls, website save functions, and more. Prefix, infix, and postfix expressions can all be handled with a stack, but computers do not typically use infix expressions. A queue is a simple data structure that maintains a first-in-first-out (FIFO) sorting property and has basic operations such as enqueue, dequeue, and is_empty. Queues are very useful in scheduling system tasks and can help build timed task emulations. A double-ended queue(Deque) is a data structure that allows a mixed behavior of stack and queue. Its basic operations include is_empty, add_front, add_rear, remove_front, and remove_rear. Although a double-ended queue can be used as a stack or a queue, it is recommended to use it only as a double-ended queue. A linkedList is a collection of items, each of which is stored in a relative position in the list. The implementation of a linked list itself maintains logical order and does not need to be stored in physical order. Modifying the head of a linked list is a special case. Vec is a data container that comes with Rust, and the default implementation uses dynamic arrays. In this chapter, however, we use a linked list for this purpose.
