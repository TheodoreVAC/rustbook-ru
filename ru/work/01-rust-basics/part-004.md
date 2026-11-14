## 1.4 Review

Similar to C/C++, Rust is a systems programming language. This means that concepts learned in those languages can be applied to understand Rust better. However, Rust introduces unique concepts like mutability, ownership, borrowing, and lifetimes, which can be both advantages and challenges.

### 1.4.1 The History of Rust

Rust is a highly efficient and reliable general-purpose compiled language that utilizes LLVM as its backend. It offers a balance between development efficiency and execution efficiency, making it a popular language among developers. The language has consistently been ranked as the most loved language by developers on Stack Overflow for many years. In 2021, Google, Amazon, Huawei, Microsoft, and Mozilla established a foundation for Rust, and Google even funded the rewriting of the Internet infrastructure Apache httpd and OpenSSL in Rust. Rust also has its own mascot, a red crab named Ferris. Rust was originally a personal project of Mozilla employee Graydon Hoare, and it received support from the Mozilla Research Institute starting in 2009. Rust was released to the public in 2010. Mozilla supported Rust because the Firefox Gecko engine was behind the times due to various vulnerabilities, historical baggage, and performance bottlenecks. Rust replaced the OCaml-written compiler implementation for self-hosting in 2010-2011 and released version 1.0 in 2015. Rust has a strong and active community, and a stable and testing version are released every six weeks, with a major edition released every three years. Rust employs modern engineering management tool Cargo and has over 100,000 packages published on crates.io. In addition to development efficiency, Rust also exhibits excellent performance. In 2017, a team of six Portuguese researchers conducted a survey [8] on the performance of various programming languages, and Rust was found to be highly performant. They wrote solutions to ten problems based on 27 languages using the same algorithm, and then ran these solutions, recording the electricity consumption, speed, and memory usage of each language.

The figure above provides readers with a clear understanding of the resource usage of various programming languages. Rust’s energy consumption, time consumption, and memory consumption indicators are all very favorable. While this comparison may not be completely accurate, the overall trend is clear: Rust is energy-saving and efficient. Considering the critical point of climate change we currently face, the use of energy-saving and efficient languages like Rust to develop software is in line with the trend of Carbon Peaking and Carbon Neutrality Goals. I believe that it can be an important tool for enterprise transformation and look forward to the industry and society reaching a consensus. Rust has a wide range of applications that extends to command-line tools, DevOps tools, audio and video processing, game engines, search engines, blockchain, the Internet of Things, browsers, cloudnative, network servers, databases, and operating systems. Many universities and enterprises at home and abroad are using Rust extensively. For example, Tsinghua University uses Rust in its new students’ rCore and zCore operating systems, ByteDance’s Feishu, remote desktop software RustDesk, PingCap’s TiDB database, js/ts runtime Deno, and Google’s Fuchsia operating system.

### 1.4.2 Keywords, Comments, Naming conventions

Rust uses 39 keywords (which may increase in the future), and some of these keywords, such as Self and self, can be challenging to learn.

```text
Self
          enum
                   match
                             super
as
          extern
                   mod
                             trait
async
          false
                   move
                             true
await
          fn
                   mut
                             type
break
          for
                   pub
                             union
const
          if
                   ref
                             unsafe
continue
          impl
                   return
                             use
crate
          in
                   self
                             where
dyn
          let
                   static
                             while
else
          loop
                   struct
```

Keywords are crucial to programming languages and reflect the designers’ thought process behind program design. Different keywords indicate different trade-offs and considerations for various tasks. For instance, Rust’s match is powerful, while C’s similar switch functionality is less so, resulting in different coding styles and ways of thinking. To facilitate code understanding and explain complex logic, appropriate explanations must be provided within the program. Comments serve as a useful place for these explanations. Rust supports two types of comments: regular comments and documentation comments. Regular comments have three comment formats.

```text
// comment style 1

/* comment style 2 */

/*
 * comment style 3
 * multi-line-comments
 * multi-line-comments
 * multi-line-comments
 */
```

Documentation and testing are highly emphasized in Rust, which is why it features a special documentation comment feature. This feature enables the writing of documentation and test code within comments, allowing code testing through cargo test and document generation through cargo doc.

```text
//! This symbol placed at the top of a module file to control
//! the generation of library documentation and to describe
//! the functionality of the entire module.
/// This symbol is placed above the object being described to
/// control the generation of library documentation and to
/// describe functions or structures.
```

Rust’s documentation uses Markdown syntax, so using the # symbol is essential.

```rust
//! Math mod
               <-- doc comment, describe mode
//!
/// # Add <-- doc comment, discribe function, test case
/// This function sum the inputs
///
/// # Example <-- test code, use case
/// use math::add;
/// assert_eq!(3, add(1, 2));
fn add(x: i32, y: i32) -> i32 {
    // sum <-- regular comment
    x + y
}
```

Naming conventions have been a topic of interest in programming, and Rust has its recommended practices. Rust suggests using UpperCamelCase for class-level content and snake_case for value-level content.

```text
Item
                Convention
Crate
                snake_case
Type
                UpperCamelCase
Trait
                UpperCamelCase
Enum
                UpperCamelCase
Function
                snake_case
Method
                snake_case
Constructor
                new / with_more_details
Converter
                from_other_type
Macros
                snake_case!
Local variable
                snake_case
Static variable SCREAMING_SNAKE_CASE
Constants
                SCREAMING_SNAKE_CASE
Type Param
                The alphabeta of UpperCamelCase, like T, U, K
Lifetime
                lowercase,such as 'a, 'src, 'dest
```

In UpperCamelCase, initialisms and abbreviations of compound words count as one word. For example, Usize should be used instead of USize. In snake_case or SCREAMING_SNAKE_CASE, words should not be composed of single letters unless it is the last word. Therefore, btree_map should be used instead of b_tree_map, and PI_2 instead of PI2. The following code exemplifies Rust’s naming conventions, which this book follows, and readers are encouraged to follow as well.

```rust
// Enum
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

```rust
// Trait
pub trait From<T> {
    fn from<T> -> Self;
}

// Struct
struct Rectangle {
    height: i32,
    width: i32,
}
impl Rectangle {
    // constructor
    fn new(height: i32, width: i32) -> Self {
        Self { height, width }
    }

    // function
    fn calc_area(&self) -> i32 {
        self.height * self.width
    }
}

// static and constant variables
static NAME: &str = "kew";
const AGE: i32 = 25;

// Macro definition
macro_rules! add {
    ($a:expr, $b:expr) => {
        {
            $a + $b
        }
    }
}

// variable and macro call
let sum_of_nums = add!(1, 2);
```

As Rust’s popularity grows and its usage expands, a unified coding standard becomes necessary. Currently, Professor Zhang Handong leads a good Rust Coding Standard, which readers can refer to.

### 1.4.3 Constants, Variables, Data Type

Variables and constants are fundamental concepts in programming, and Rust is no exception. However, Rust introduces mutability and immutability, which can be confusing, especially for beginners transitioning from other programming languages. In Rust, there are three types of values: constants, variables, and static variables. Novices may face difficulties when dealing with mutability and immutability, and they may have to struggle with the compiler to get their code to compile. By understanding the differences between constants, variables, and static variables, Rust programmers can write more concise and efficient code. Constants are defined using const and are bound to a name that cannot be changed or reassigned.

```text
// define constant(like #define used in C/C++)
const AGE: i32 = 1984;
// AGE = 1995; error, mutation not allowed

const NUM: f64 = 233.0;
// const NUM: f64 = 211.0; error, defined
```

Variables are defined using let and can have a value that is mutable or immutable depending on whether mut is used during its definition.

```rust
let x: f64 = 3.14; // let defines x which can be reassigned
                   // but not mutated.
// x = 6.28; error, x is unmutable
let x: f64 = 2.71 // reassign x

let mut y = 985; // let mut defines y which can be reassigned
                 // and mutated.
y = 996; // y is mutable
let y = 2019; // reassign y
```

Finally, static variables are defined using static and can be mutable or immutable depending on whether mut is used during its definition.

```rust
static NAME: &str = "shieber" // static variable which can be
                              // used as a constant
// NAME = "kew"; error,NAME is unmutable

static mut NUM: i32 = 100; // static mutable variable
unsafe {
    NUM += 1; // NUM is mutable
    println!("Num:{}",NUM);
}
```

The ”mut” keyword is a constraint in Rust programming, restricting variables from being changed unless ”mut” is added in front of it. Otherwise, the variable is immutable. This differs from other programming languages. Although static variables and constants have similarities, they’re different in reality. Constants are replaced inline as many times as they’re used, while static variables are referenced, with only one global instance. Static variables defined with ”static mut” are wrapped in ”unsafe” to indicate that they’re not safe. It’s recommended to use constants and variables instead, forget about static variables, and avoid coding errors. Data types are the building blocks of a language, and Rust’s data types are similar to C, while some are similar to Go. There are two types of basic data types in Rust: scalar and compound. Scalar types represent a single value, such as integers, floating-point numbers, Boolean types, and character types. Compound types combine multiple values into one, such as tuples and arrays, which are Rust’s two native compound types. Integers in Rust are numbers without a decimal part, classified into 12 types based on whether they’re signed or unsigned and their length, denoted by ”i” for signed types and ”u” for unsigned types. A 64-bit machine can handle a 128-bit number by storing it in segments and processing it using multiple registers. ”isize” and ”usize” are integer types that match the machine architecture. So on a 64-bit machine, ”isize” and ”usize” represent ”i64” and ”u64,” respectively. On a 32-bit machine, they represent ”i32” and ”u32.”

```text
Size
        Signed
                  Unsigned
8
        i8
                  u8
```

```text
16
        i16
                  u16
32
        i32
                  u32
64
        i64
                  u64
128
        i128
                  u128
arch
        isize
                  usize
```

Floating-point numbers in Rust are numbers with a decimal part, having two types: ”f32” and ”f64,” with the default type being ”f64,” and both types being signed.

```text
Size
         Signed
32
         f32
64
         f64
               (default)
```

The boolean type in Rust is represented by ”bool” and has only two values: true and false, consistent with other programming languages. The character type ”char” in Rust is the most primitive type, similar to the C language. Characters are declared using single quotes, while string literals are declared using double quotes. The variables ”c” and ”c_str” are completely different types, with characters being four-byte Unicode scalar values, and strings represented as arrays.

```rust
// unicode scalar value
let c = 's';

// dynamic arrays
let c_str = "s";
```

Tuples are a type of composite value that combines multiple values of other types. Once declared, the length of a tuple cannot be increased or decreased. Tuples use parentheses to enclose the values, separated by commas. To retrieve values from a tuple, pattern matching and dot notation can be used, with indices starting at 0.

```rust
let tup1: (i8, f32, i64) = (-1, 2.33, 8000_0000);
// pattern match
let (x, y, z) = tup1;

let tup2 = (0, 100, 2.4);
let zero = tup2.0; // use symbol . to get value
let one_hundred = tup2.1;
```

In Rust, the let keyword is not just used to define variables, but can also destructure values through pattern matching. For example, x, y, and z can each obtain the values of -1, 2.33, and 80000000, respectively, through pattern matching. Defining variables is also a form of pattern matching, as let is essentially a pattern matching operation. The unit type in Rust is represented by an empty tuple (), and when there is only one value, it is written as (). The unit value is a special value of this type, and is implicitly returned when an expression does not return any value. Unlike tuples, arrays in Rust must have elements of the same type, and the length cannot be changed once declared. If a mutable collection is needed, Vec can be used instead. It allows for dynamic resizing and is the preferred option in most situations.

```rust
// define arrays
let genders = ["Female", "Male", "Bigender"];
let gender_f = genders[0]; // indice element

// [type; num] define an array
```

```rust
let digits: [i32; 5] = [0, 1, 2, 3, 4];
let zeros = [0; 10]; // define an array which holds ten '0'
```

Rust allows for explicit type conversion between data types using the as keyword, but does not provide implicit type conversion between primitive types. Integer conversions in Rust follow the conventions of the C language, and all integer conversions are well-defined. For instance, converting i8 to i32 is a reasonable conversion that can be done explicitly.

```bash
// type_transfer.rs
#![allow(overflowing_literals)] // Ignore overflow warnings
                                   // for type conversion.
fn main() {
    let decimal = 61.3214_f32;
    // let integer: u8 = decimal; // Error, f32 cannot be
                                   // converted to u8.
    let integer = decimal as u8; // Correct, use as
    let character = integer as char;
    println!("1000 as a u16: {}", 1000 as u16);
    println!("1000 as a u8: {}", 1000 as u8);
}
```

For some complex types, Rust also provides two traits, From and Into, for conversion.

```rust
pub trait From<T> {
    fn from<T> -> Self;
}
pub trait Into<T> {
    fn into<T> -> T;
}
```

With these two traits, you can provide conversion functionality for various types.

```rust
// integer_to_complex.rs
#[derive(Debug)]
struct Complex {
    real: i32, // real quantity
    imag: i32 // imaginary quantity
}

// Implement a conversion from i32 to a complex number, where
// the i32 is converted to the real part and the imaginary
// part is set to 0.
impl From<i32> for Complex {
    fn from(real: i32) -> Self {
        Self { real, imag: 0 }
    }
}

fn main() {
    let c1: Complex = Complex::from(2_i32);
    // implemented Into by default
    let c2: Complex = 2_i32.into();
    println!("c1: {:?}, c2: {:?}", c1, c2);
}
```

### 1.4.4 Statement, Expression, Computors and Flow Control

In Rust, there are two basic syntax categories: Statements and Expressions. Statements refer to operations to be executed, while expressions are simply used to evaluate values. Rust statements include declaration statements and expression statements. Declaration statements are used to declare variables, static variables, constants, structs, functions, external packages, and external modules. Statements that end with a semicolon are expression statements.

```rust
// Declaration statement for function
fn sum_of_nums(nums: &[i32]) -> i32{
    nums.iter().sum::<i32>()
}

let x = 5; // The entire line is a statement, x = 5 is an
               // expression that calculates the value of x
x + 1; // The entire line is an expression
let y = x + 1; // The entire line is a statement, y = x + 1
               // is an expression
println!("{y}");

let z = [1,2,3];
println!("sum is {:?}", sum_of_nums(&z));
```

Operators are symbols used to specify the type of calculation performed by an expression. Rust supports common types of operators including arithmetic, relational, logical, assignment, and reference operators. Here are some Rust operators and their functions:

```rust
Operator
          Example
                                    Explanation
+
          expr + expr
                                    addition
+
          trait + trait, 'a + trait compound type constraint
-
          expr - expr
                                    subtraction
-
          - expr
                                    negation
*
          expr * expr
                                    multiply
*
          *expr
                                    dereference
*
          *const type, *mut type
                                    raw pointer
/
          expr / expr
                                    division
%
          expr % expr
                                    remainder
=
          var = expr, ident = type
                                    asignmen/equality
+=
          var += expr
                                    addition and assignment
-=
          var -= expr
                                    subtraction and assignment
*=
          var *= expr
                                    multiply and assignment
/=
          var /= expr
                                    division and assignment
%=
          var %= expr
                                    remainder and assignment
==
          expr == expr
                                    equality comparison
!=
          var != expr
                                    inequality comparison
>
          expr > expr
                                    greater-than comparison
<
          expr < expr
                                    less-than comparison
>=
          expr >= expr
                                    >= comparison
<=
          expr <= expr
                                    <= comparison
&&
          expr && expr
                                    logical AND
||
          expr || expr
                                    logical OR
!
          !expr
                                    bitwise NOT or logical NOT
```

```rust
&
          expr & expr
                                    bitwise AND
&
          &expr, &mut expr
                                    borrow
&
          &type, &mut type,
                                    pointer/reference
|
          pat | pat
                                    pattern matching
|
          expr | expr
                                    bitwise OR
^
          expr ^ expr
                                    bitwise XOR
<<
          expr << expr
                                    left shift
>>
          expr >> expr
                                    right shift
&=
          var &= expr
                                    bitwise AND and assignment
|=
          var |= expr
                                    bitwise OR and assignment
^=
          var ^= expr
                                    bitwise XOR and assignment
<<=
          var <<= expr
                                    left shift and assignment
>>=
          var >>= expr
                                    right shift and assignment
.
          expr.ident
                                    member access
..
          .., expr..,
          ..expr, expr..expr
                                    right-exclusive range
..
          ..expr
                                    struct update syntax
..=
          ..=expr, expr..=expr
                                    right-inclusive range
:
          pat: type, ident: type
                                    type constraint
:
          ident: expr
                                    struct field initialization
:
          'a: loop {...}
                                    loop label
;
          [type; len]
                                    fixed-size array type
=>
          pat => expr
                                    match arm
@
          ident @ pat
                                    pattern binding
?
          expr?
                                    error propagation
->
          fn(...) -> type,
          |...| -> type
                                    function or closure
                                    return type
```

The ability to decide whether to execute a piece of code based on a condition or to repeatedly run a piece of code depending on whether a condition is satisfied is a feature found in most programming languages. In Rust, if expressions and loops are the most common structures used to control execution flow.

```rust
let a = 3;

if a > 5 {
    println!("Greater than 5");
} else if a > 3 {
    println!("Greater than 3");
} else {
    println!("less or equal to 3");
}
```

if and let can also be combined to control code execution. One way to do this is with a let if statement, which returns the result to the let section if the condition is met. Note that there is a semicolon at the end because let c = ..; is a statement.

```rust
let a = 3; let b = 2;
let c = if a > b {
            true
```

```text
        } else {
            false
        };
```

Another way is with an if let statement, which executes code by pattern matching the value on the right.

```rust
let some_value = Some(100);
if let Some(value) = some_value {
    println!("value: {value}");
} else {
    println!("no value");
}
```

In addition to the if let matching statement, match can also be used to control code execution.

```rust
let a = 10;
match a {
    0 => println!("0 == a"),
    1..=9 => println!("1 <= a <= 9"),
    _ => println!("10 <= a"),
}
```

Rust provides various loop types, including loop, while, and for in. Using the continue and break keywords, you can jump and stop code execution on demand. The loop keyword controls repeated code execution until a condition is met.

```rust
let mut val = 10;
let res = loop {
    // break loop and return value
    if val < 0 {
        break val;
    }

    val -= 1;
    if 0 == val % 2 {
        continue;
    }

    println!("val = {val}");
}; // a semi-colon here

// dead loop
loop {
    if res > 0 { break; }

    println!("{res}");
} // no semi-colon here
```

In contrast, a while loop computes the loop condition externally.

```rust
let num = 10;
while num > 0 {
    println!("{}", num);
    num -= 1;
```

```rust
}

let nums = [1,2,3,4,5,6];
let mut index = 0;
while index < 6 {
    println!("val: {}", nums[index]);
    index += 1;
}
```

Iterating through an array in Rust can be achieved through the for in loop, which is more convenient than using index and length.

```rust
let nums = [1,2,3,4,5,6];

// iterate over array
for num in nums {
    println!("val: {num}");
}

// iterate over array in reverse order
for num in nums.iter().rev() {
    println!("val: {num}");
}
```

This approach is not only concise, but also reduces the chance of errors, as it avoids specifying the array length explicitly. Additionally, iter().rev() can be used to traverse the array in reverse order. The combination of while and let can be used to form a pattern match, eliminating the need to write a stop condition. The let syntax automatically determines when the condition is met before continuing while.

```rust
let mut v = vec![1,2,3,4,5,6];
while let Some(x) = v.pop() {
    println!("{x}");
}
```

Overall, Rust provides many useful methods to control code flow, including match, if let, let if, while let, which align with Rust’s coding specifications and are recommended.

### 1.4.5 Function, Program Structure

Functions are a crucial building block in programming languages, and in Rust, they are defined using the fn keyword followed by a snake-case function name. Function arguments are enclosed in parentheses and written as val: type, for example, x: i32. The return value is specified using -> res and may or may not have a value. The function implementation is wrapped in curly braces. Like C, Rust has a main function.

```rust
// define a function
fn func_name(parameters) -> return_types {
    code_body;
                // code body
    return_value // return value, no semi-colon here
}
```

Define a summation function.

```rust
// main function
fn main() {
    let res = add(1, 2);
    println!("1 + 2 = {res}");
}

fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

It is important to note that function definitions can be written before or after the main function, and the return value can be written directly on the value line without adding a semicolon, although this syntax is unique to Rust and adding a semicolon is not recommended. Functions in Rust modules are private by default and require the pub keyword to export them to other programs. In Rust, a program is composed of several parts.

```text
package/lib/crate/mod
variable
statement/expression
function
trait
label
comment
```

The following example shows the various elements of a program.

```rust
// rust_example.rs

// import module from standard library
use std::cmp::max;

// public module
pub mod math {
    // public function
    pub fn add(x: i32, y: i32) -> i32 { x + y }

    // private function
    fn is_zero(num: i32) -> bool { 0 == num }
}

// struct
#[derive(Debug)]
struct Circle { radius: f32, // radius }

// implement a converter to convert f32 to Circle
impl From<f32> for Circle {
    fn from(radius: f32) -> Self {
        Self { radius }
    }
}

// comment: custom function
```

```rust
fn calc_func(num1:i32, num2:i32) -> i32 {
    let x = 5;
    let y = {
        let x = 3;
        x + 1 // expression
    }; // statement

    max(x, y)
}

// use function from math module
use math::add;

// main function
fn main() {
    let num1 = 1; let num2 = 2;

    // call function
    println!("num1 + num2 = {}", add(num1, num2));
    println!("res = {}", calc_func(num1, num2));

    let f: f32 = 9.85;
    let c: Circle = Circle::from(f);
    println!("{:?}", c);
}
```

### 1.4.6 Ownership, Scope, Lifetime

Rust’s ownership system is a crucial concept that deals with resource management, dangling references, and other complexities in the type system. It introduces the concepts of ownership, borrowing, and lifetime to restrict the state and scope of various quantities. The scope rules in Rust are the strictest among all programming languages. In Rust, memory is managed through the ownership system, which is unlike garbage collection or manual memory release in other languages. The compiler checks a set of ownership rules at compile time, and if any rule is violated, the program doesn’t even compile. The ownership rules are simple:

- Each value has an owner (variable).
- Values have only one owner at any given time.
- When the owner leaves the scope, the value is discarded.

This means that values in Rust are managed by a unique object, and memory is released as soon as they are no longer in use. Rust’s ownership rules make it more memory efficient because it releases unused memory as soon as it is no longer needed, which can then be reused by later variables. In contrast, languages that use garbage collection, such as in Go, which reclaims memory through the tricolor method and could lead to stop the world problems and program lag, or manual memory release may cause memory leaks as unused memory may not be released. The ownership mechanism is achieved through the automatic call of the drop method when the variable leaves the scope.

```rust
fn main() {
    let long = 10; <--- long enters scope (main)

    { // this is a new temp scope
        let short = 5; <--- short enters scope (temp)
```

```rust
        println!("inner short: {}", short);

        let long = 3.14; <--- long enters scope (temp)
        println!("inner long: {}", long);
    } <--- long and short leave scope (temp)

    let long = 'a'; <--- long reassigns to a char
    println!("outer long: {}", long);
} <--- long leaves scope (main)
```

The above shows the scope of each variable. The ownership mechanism is achieved by automatically calling the drop method of the variable when it leaves the scope (e.g. } in this case). Note that the internal long and the external long are two different variables, and the internal long does not override the external long. To illustrate Rust’s ownership mechanism, we can compare it to human society. For example, when a reader buys a book, they own it. If a friend borrows the book, the ownership still belongs to the reader. However, if the reader gives the book to the friend, the ownership transfers to the friend. Rust also has the concepts of ”borrow” and ”move,” which are illustrated in the below example.

```rust
fn main() {
    let x = "Shieber".to_string(); // create a string
    let y = x; // move ownership of x to y
    // println!("{x}"); // x is no longer valid
} <--- y calls drop
```

Let y = x; make a move, which transfers ownership of x to y. Some readers may wonder, ”Isn’t it released only when you leave the scope?”, x and y are still in the main scope, how can it report an error? Actually, the second rule of ownership mechanism is very clear: a value can have only one owner at any time. So after the variable x is moved, it is immediately released and cannot be used later. Its scope only goes to the line let y = x; and not to the line }. In addition, this mechanism ensures that only y, not x, is freed at }, avoiding the memory safety problem of secondary freeing. To use both x and y, you can do something like the following.

```rust
fn main() {
    let x = "Shieber".to_string(); // create a string
    let y = &x; // borrow x
    println!("{x}"); // x is still valid
} <--- y calls drop
```

let y = &x; is called a borrowing, &x is a reference to x. A reference is like a pointer (address) from which you can access data stored at that address that belongs to another variable, and a reference is created to be borrowed by someone else. The book we borrowed cannot, by definition, be altered in any way, i.e. it is immutable. However, there’s nothing wrong with a friend sketching over it. Similarly, there are mutable and immutable variables borrowed from Rust, and the let y = &x; above shows that y is just a non-variable borrowed from x. If you want mutable, you need to add the mut modifier.

```rust
fn main() {
    let x = "Shieber".to_string(); // create a string
    let y = &mut x; // borrow x mutably
    y.push_str(", handsome!");
    // let z = &mut x; // cannot borrow x mutably twice
    println!("{x}"); // x is still valid
}
```

On line: let z = &mut x;, an error is reported, indicating that there can be only one variable borrow. This is done to avoid data competition, such as writing data at the same time. More than one immutable reference can exist at the same time, because multiple immutable references do not affect the variable; only multiple mutable references cause errors. Now look at another situation. If the reader buys an electronic version of this book, then you can give a copy to your friend by copying it (Please follow the intellectual property laws), so you both have a copy of the book, and both have ownership of the book. Extending this concept in Rust gives us ”copy”, ”clone”.

```rust
fn main() {
    let x = "Shieber".to_string(); // create a string
    let y = x.clone(); // clone x
    println!("{x}, {y}"); // x and y both are valid
}
```

The clone function, as the word literally implies, makes a deep copy of the data to y. Borrowing is just getting a valid pointer, which is fast, while cloning requires copying the data, which is less efficient and doubles the memory consumption. If the reader tries to write the following without the clone function, and finds that it compiles and runs without errors, does it not satisfy the ownership rule?

```rust
fn main() {
    let x = 10; // create an integer on the stack
    let y = x;
    println!("{x}, {y}"); // x and y both are valid. paradox?
}
```

In fact, let y = x; does not give 10 to y, but automatically copies a new 10 to y, so that x and y each have a 10, so there is no conflict with the ownership rule. Because these simple variables are on the stack, Rust implements a uniform trait for this kind of data called Copy, which allows for fast copying without releasing the old variable x. In Rust, values, booleans, characters, etc. all implement the Copy trait, so moving such variables is equivalent to copying. Here you can call clone as well, but it’s not necessary. As mentioned earlier, a reference is a valid pointer. However, invalid pointers are often found, similar to the invalid dangling pointers in other programming languages.

```rust
fn dangle() -> &String {
    let s = "Shieber".to_string();
    &s
}

fn main() {
    let ref_to_nothing = dangle();
}
```

The above code will compile with an error message similar to the following (with deletions).

```rust
error[E0106]: missing lifetime specifier
 --> dangle.rs:1:16
1 | fn dangle() -> &String {
  |
                   ^ expected named lifetime parameter
  | help: function's return type contains a borrowed value,
  | but there is no value for it to be borrowed from
  | help: consider using the 'static lifetime
1 | fn dangle() -> &'static String {
  |
                   ~~~~~~~~
```

In fact, the problem can be found by analyzing the code or the error message, the function returned an invalid reference.

```rust
fn dangle() -> &String { <--- return a reference to a String
    let s = "Shieber".to_string();
    &s <---- return a reference to s
} <---- s is dropped here, and it's memory goes away
```

According to the ownership analysis, s release is satisfied, &s is a pointer, returned, and seems to be fine, at most the pointer position is invalid. s and &s are two different things, the ownership system can only check the data according to the three rules, but it is impossible to know that the address &s points to is actually invalid. So why does the compilation error? The error message indicates that the lifetime specifier is missing. You can see that the suspension reference and the lifetime are in conflict, and that’s why the error is reported. This means that even if your ownership system passes, but the lifetime does not, the error will be reported. In fact, every reference in Rust has its own lifetime, i.e., the scope for which the reference remains valid. The ownership system does not guarantee that the data is absolutely valid, and requires a lifetime to ensure validity. Most of the time the lifetime is implicit and can be inferred, just as most of the time the type can be automatically inferred. When there is a reference in the scope, it is necessary to indicate the lifetime to show the interrelationship, so that the reference actually used at runtime is absolutely valid.

```rust
fn main() {
    let a; // ----------+'a, a lifetime begins
                          // |
    { // |
        let b = 10; // --+'b | b lifetime begins
                          // | |
        a = &b; // -+ | b lifetime ends
    } // |
                          // |
    println!("a: {}", a); // ----------+ a lifetime ends
}
```

a references b, and a’s lifetime ’a is longer than b’s lifetime ’b, so the compiler compiles with an error. For a to reference b properly, then b’s lifetime must be at least as long as the end of a’s lifetime. By comparing lifetimes, Rust can find references that don’t make sense and thus avoid dangling reference problems. To use variables legally, Rust requires that all data carry a lifetime specifier. Lifetimes are indicated by single quotes ’ followed by a letter, such as &’a, &mut ’t. References in functions also require lifetime markers.

```rust
fn longest<'a>(x: &'a String, y: &'a String) -> &'a String {
    if x.len() < y.len() {
        y
    } else {
        x
    }
}
```

The pointed brackets are lifecycle arguments, which are generic arguments that need to be declared in the pointed brackets of the function name and argument list to indicate that both arguments and the returned reference will live as long as they do. Because Rust automatically infers the lifetime, it is recommended to omit the lifetime specifier.

```rust
fn main() {
    // static lifetime, lives for the entire duration
    let s: &' static str = "Shieber";

    let x = 10;
    let y = &x; // can rewrite as let y = &'a x;
    println!("y: {}", y);
}
```

In this section, we learn about ownership system, borrowing, cloning, scope rules, lifetime. The ownership system is a memory management mechanism, borrowing and cloning are ways of using variables that extend the ownership system, and the lifetime is a complement to the ownership system, used to solve problems such as dangling references that the ownership system cannot handle.

### 1.4.7 Generic, Trait

To add two i64s, you can implement an add function of type i64 called add_i64.

```rust
fn add_i64(x: i64, y: i64) -> i64 {
    x + y
}
```

However, if you were to implement add functions for all numeric types, the code would become lengthy and the naming of functions would become cumbersome, leading to function names like add_i8, add_i16, and so on. The addition operation should be universal for any numeric type, and writing multiple sets of code is unnecessary. To tackle this problem, Rust uses generics. Generics are abstract substitutes for concrete types or properties, allowing developers to express the properties of the generic type without knowing its actual type when writing code.

```rust
// generic function: add
fn add<T>(x: T, y: T) -> T {
    x + y
}
```

The add function uses a generic type, and the generic parameter T is placed inside the parentheses immediately after add in the function declaration to indicate that this is a generic function. The generic parameter T represents any numeric type, and the return value type and the type of arguments involved in the function are both T, allowing it to handle all numeric types. In addition to functions, generics can be used for other program components, such as enums. The Result in Rust ia an enum type, which handles errors, uses the generic parameters T and E, where T represents the return value type on success and E represents the return value type on error.

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

Generic types can also be used for commonly used structs

```rust
struct Point<T> {
    x: T,
    y: T,
}
```

```rust
let point_i = Point { x: 3, y: 4 };
let point_f = Point { x: 2.1, y: 3.2 };
// let point_m = Point { x: 2_i32, y: 3.2_f32 }; Error
```

The generic parameter T is used to constrain the input parameters, ensuring that both parameters are of the same type. For instance, for the Point struct, it would be incorrect if x used i32 and y used f32. Although a generic set of code has been implemented for the add function using generics, there are still some issues. The T parameter is not guaranteed to be a numeric type, so calling add on a type that does not support addition would be incorrect. It would be preferable to restrict the generic argument type of add to only numeric types. A trait in Rust is a way to define and restrict the behavior of a generic type, encapsulating the functionality shared by each type. Using traits, the behavior of each type can be well-controlled, and a trait can consist of three parts: method, type, and constant. It defines an abstract interface that can be implemented by a type or directly inherited from its default implementation. For example, if you have two types, teacher and student, and both have a greeting behavior, you can implement the following trait:

```rust
trait Greete {
    // default implementation
    fn say_hello(&self) {
        println!("Hello!");
    }
}

// contains different properties
struct Student {
    education: i32, // education years
}
struct Teacher {
    education: i32, // education years
    teaching: i32, // teaching years
}

impl Greete for Student {}

impl Greete for Teacher {
    // override default implementation
    fn say_hello(&self) {
        println!("Hello, I am teacher Zhang!");
    }
}

// generic constraint
fn outer_say_hello<T: Greete>(t: &T) {
    t.say_hello();
}

fn main() {
    let s = Student{ education: 3 };
    s.say_hello();

    let t = Teacher{ education: 20, teaching: 2 };
    outer_say_hello(&t);
}
```

The outer_say_hello function above adds the generic constraint T: Greete, known as trait bound, indicating that only a type T that implements Greete can call the say_hello function. the previous add function can rewrite as below.

```rust
fn add<T: Addable>(x: T, y: T) -> T {
    x + y
}
```

The Addable trait is a constraint that ensures that only types implementing the Addable trait can be added together. This allows any type that doesn’t meet the constraint to be reported as an error at compile time rather than waiting until runtime. Another way to write the trait constraint is by using the impl keyword, as shown in the following example. Here, t must be a reference implementing the Greete trait.

```rust
fn outer_say_hello(t: &impl Greete) {
    t.say_hello();
}
```

Multiple trait bounds and multiple argument types can be combined using a comma and a plus sign.

```rust
fn some_func<T: trait1 + trait2, U: trait1> (x: T, y: U) {
    do_some_work();
}
```

To avoid using multiple trait bounds in parentheses, Rust has introduced a where syntax that separates the trait bound from the parentheses.

```rust
// where clause
fn some_func<T, U> (x: T, y: U)
    where T: trait1 + trait2,
          U: trait1,
{
    do_some_work();
}
```

The implementation of the say_hello method in Greete for Student and Teacher allows each type to encapsulate its own unique properties. While Student is more like a direct inheritance from Greete, Teacher overrides Greete. Although they use the same say_hello method, Student and Teacher display different states. The concepts of encapsulation, inheritance, and polymorphism are present here, which seems to imply that the concept of classes has been implemented through impl, trait, and thus objectoriented programming.
