# Rust Basic

## 1.1 Objectives

- Install Rust and learn its toolchain
- Explore learning resources for Rust in various areas
- Review the fundamentals of the Rust programming language

## 1.2 Install Rust and its Toolchain

Ubuntu 22.04 and later versions come with pre-installed Rust, so you can start using it right away. If you’re using other Unix-like systems, use the command below to install Rust. For Windows, refer to the official website. As the code in this book is written in Linux, we recommend readers use Linux or Mac OS to avoid any inconsistencies and errors caused by different environments.

```bash
$ curl --proto '=https' --tlsv1.2 \
    -sSf https://sh.rustup.rs | sh
```

After installing Rust on Linux, you need to set environment variables to enable the system to locate Rust tools like the rustc compiler. Add the following three lines to the end of ~/.bashrc.

```bash
# Rust env-path variables
export RUSTPATH=$HOME/.cargo/bin
export PATH=$PATH:$RUSTPATH
```

Then, save and execute source ~/.bashrc. If you find this process cumbersome, you can download the install_rust.sh script from the first chapter of the source code of this book and run it to complete the Rust toolchain installation. The instructions above will install the rustup tool, which manages and installs the Rust toolchain, including the rustc compiler, cargo project management tool, rustup toolchain management tool, rustdoc documentation tool, rustfmt formatting tool, and rust-gdb debugging tool. For simple projects, you can use the rustc compiler for compilation. However, for larger projects, you need the cargo tool for management, which internally calls rustc for compilation. Cargo is an excellent tool that handles project building, testing, compilation, and publishing, making it highly efficient. Programmers who have worked with C/C++ projects will appreciate the cargo tool’s greatness in handling various libraries and dependencies. Most of the time, we use the rustc compiler instead of the cargo tool, as the projects in this book are not too complex. Rustup manages the installation, upgrade, and uninstallation of Rust tools. Note that the Rust language includes stable and nightly versions, both of which can coexist. You can install Nightly using the following command.

```bash
$ rustup default nightly
```

After installation, you can use rustup to check the current version in use.

```bash
$ rustup toolchain list
    stable-x86_64-unknown-linux-gnu
    nightly-x86_64-unknown-linux-gnu (default)
```

To switch between stable and nightly versions, please use the following command.

```bash
$ rustup default stable # nightly
```

## 1.3 Learning Resources

Rust is a systems programming language and has a certain level of difficulty. It is impossible to learn Rust without good resources. Below is a collection of learning materials in various fields of Rust compiled by the author. It may not be complete, but most fields are covered.

### 1.3.1 Books and Documents

Basic: The Rust Programming Language, Easy to Understand Rust, Rustlings, Rust by Example, Rust Primer, Rust Cookbook, Rust in Action, Rust Course Advanced: Cargo Documentation, The Tao of Rust Programming, Learn Rust With Entirely Too Many Linked Lists, Rust Design Patterns High-level: rustc book, The Little Book of Rust Macros, The Rustonomicon, Asynchronous Programming in Rust

### 1.3.2 Related Topics

Wasm: https://wasmer.io, https://wasmtime.dev, https://wasmedge.org HTTP/3: https://github.com/cloudflare/quiche Algorithms: https://github.com/TheAlgorithms/Rust Games: https://github.com/bevyengine/bevy Tools: https://github.com/rustdesk/rustdesk, https://github.com/uutils/coreutils Blockchain: https://github.com/w3f/polkadot Databases: https://github.com/tikv, https://github.com/tensorbase/tensorbase Compilers: https://github.com/rust-lang/rustc_codegen_gcc Operating Systems: https://github.com/Rust-for-Linux, https://github.com/rcore-os Web Front-end: https://github.com/yewstack/yew, https://github.com/denoland/deno Web Back-end: https://actix.rs/, https://github.com/tokio-rs/axum, https://github.com/poem-web/poem

### 1.3.3 Community and Blogs

Rust Official: https://www.rust-lang.org Rust Source Code: https://github.com/rust-lang/rust Rust Documentation: https://doc.rust-lang.org/stable Rust Reference: https://doc.rust-lang.org/reference Awesome Rust: https://github.com/rust-unofficial/awesome-rust Rust lib/crate: https://crates.io, https://lib.rs Rust Sources: https://www.yuque.com/zhoujiping/programming/rust-materials Rust Cheat Sheet: https://cheats.rs

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

### 1.4.8 Enum and Match

When designing a questionnaire that requires multiple choice answers for gender, education, marital status, and other options, it is necessary to provide a variety of choices for participants to select. Enumerations in programming languages allow you to define a type by listing all possible members, similar to defining a structure. For instance, you can use an enumeration to represent gender.

```rust
enum Gender {
    Male,
    Female,
    TransGender,
}
```

To use an enumeration in Rust, simply use ”enum type::enum name”.

```rust
let male = Gender::Male;
```

A common enumeration type in Rust is Option, where Some represents a value and None indicates no value.

```rust
enum Option<T> {
    Some(T),
    None
}
```

Enumerations can also be combined with match for process control. A match expression compares a value to a series of patterns and executes the corresponding code based on the matching pattern. The patterns can include literal values, variables, wildcards, and other content. The matched values pass through each pattern of the match, and when the first matching pattern is encountered, it enters the associated block of code. Match expressions are like a classifier or sieve that filters values based on patterns. In Rust, the matched values can be filtered into more fine-grained classes. For example, an enumeration could represent the different denominations of currency values.

```rust
enum Cash { // US dollar($)
    One,
    Two,
    Five,
    Ten,
    Twenty,
    Fifty,
    Hundred,
}

fn cash_value(cash: Cash) -> u8 {
    match cash {
        Cash::One => 1,
        Cash::Two => 2,
        Cash::Five => 5,
        Cash::Ten => 10,
        Cash::Twenty => 20,
        Cash::Fifty => 50,
        Cash::Hundred => 100,
    }
}
```

Additionally, match supports wildcard and _ placeholder matches.

```rust
match cash {
    Cash::One => 1,
    Cash::Two => 2,
    Cash::Five => 5,
    Cash::Ten => 10,
    other => 0, // _ => 0,
}
```

For instance, ”other” can be replaced with _ if you don’t need to use the value directly. Here other is used instead of all denominations greater than 10.

The match expression must be exhaustive, which means it should cover all possible matching patterns. However, if you only need to match a specific pattern, using match can be cumbersome. Fortunately, Rust generalizes the matching pattern of match and introduces the if let matching pattern. The if let match counts all bills larger than $1.

```rust
let mut greater_than_one = 0;
if let Cash::One = cash { // only match Cash::One
    println!("cash is one");
} else {
    greater_than_one += 1;
}
```

### 1.4.9 Functional Programming

Rust prioritizes functional programming instead of class-based problem-solving methods used in object-oriented languages. This programming paradigm involves using functions as parameter values or returning them as the result of other functions. The key components of functional programming are closures and iterators. Closures are anonymous functions that can be passed as parameters to other functions and capture variables. They can be created in one location and executed in different contexts. Closures allow the capturing of values in the caller’s scope, making them particularly useful for defining functions that are only used once.

```rust
// define a function
fn function_name(parameters) -> return_types {
    code_body;
    return_value
}

// define closure
|parameters| {
    cody_body;
    return_value
}
```

Closures can be parameterless and may or may not return values. Rust infers closure parameter and return value types, eliminating the need to specify them explicitly. To use a closure, it must be assigned to a variable and called like a function. For instance, a closure function that determines odd or even numbers can be defined.

```rust
let is_even = |x| { 0 == x % 2 };

let num = 10;
println!("{num} is even: {}", is_even(num));
```

It’s also possible to use external variables in closures.

```rust
let val = 2;
let add_val = |x| { x + val };

let num = 2;
let res = add_val(num);
println!("{num} + {val} = {res}")
```

The add_val function captures the external variable val. Closures can capture external variables by taking ownership, reference, or mutable reference, which Rust defines using three function traits: FnOnce, FnMut, Fn.

- The FnOnce trait consumes the captured variable from the surrounding scope and moves it into the closure when it is defined. This trait indicates that the closure can only be called once.
- The FnMut trait obtains a mutable borrowed value, allowing it to change the external variable.
- The Fn trait obtains an immutable borrowed value from its environment.

These traits correspond to the move, mutable reference, and reference implementation of the ownership system. All closures can be called at least once, making them implement the FnOnce trait. Closures that use mutable references but do not move variable ownership into the closure implement the FnMut trait, while those that do not require mutable access to the variables implement Fn. The move keyword is used to force the ownership of an external variable to be moved into a closure.

```rust
let val = 2;
let add_val = move |x| { x + val };
// println!("{val}"); error: use of moved value: val
```

In Rust, the ”for in” loop is used to iterate through an array, which is an iterator that implements the iteration functionality by default. Iterators pass each element in a collection to a processing logic in sequence, allowing specific operations to be performed on the items in a sequence. They are responsible for iterating through each item in the sequence and determining when to stop. By default, iterators must implement the Iterator trait, which has two methods: iter() and next().

```text
iter(), return a iterator
next(), return the next element
```

The iter() method can be divided into three types depending on whether the data can be modified during iteration.

```rust
method
                  return type
iter()
                  return a immutable iterator
                  whose element type is &T
iter_mut()
                  return a mutable iterator
                  whose element type is &mut T
into_iter()
                  return a immutable iterator
                  whose element type is T, original data
                     consummed
```

In Rust, iterators can be classified into ”reentrant” and ”non-reentrant” types based on their behavior towards the original data after iteration. A ”reentrant” iterator allows the original data to be used again after iteration, while a ”non-reentrant” iterator consumes the original data. The iter(), iter_mut(), and into_iter() methods are used to implement iterators for reading values, changing values, and taking ownership of the original data, respectively.

```rust
let nums = vec![1,2,3,4,5,6];

// 1.iter immutable
for num in nums.iter() {
    println!("num: {num}")
};
println!("{:?}", nums); // use nums after iter

// 2.iter_mut mutable
for num in nums.iter_mut() {
```

```rust
    *num += 1;
}
println!("{:?}", nums); // use nums after iter_mut

// 3.into_iter transfer nums into iterator and consume nums
for num in nums.into_iter() {
    println!("num: {num}");
}
// println!("{:?}", nums); error: use of moved value "nums"
```

In addition to transferring ownership of the original data, iterators can also be consumed or regenerated. Consumers are special operations on an iterator that convert the iterator into a value of another type. Examples of consumers include sum, collect, nth, find, next, and fold. They perform operations on the iterator to obtain the final value. Producers, on the other hand, are adapters that traverse the iterator and generate another iterator. Examples of adapters include take, skip, rev, filter, map, zip, and enumerate. In Rust, an iterator itself is considered an adapter.

```rust
// adapter_consumer.rs

fn main() {
    let nums = vec![1,2,3,4,5,6];
    let nums_iter = nums.iter();
    let total = nums_iter.sum::<i32>(); // sum is a consumer

    let new_nums: Vec<i32> = (0..100).filter(|&n| 0 == n % 2)
                                     .collect(); // Adapter
    println!("{:?}", new_nums);

    // calculate the sum of all numbers less than 1000
    // that are divisible by 3 or 5
    let sum = (1..1000).filter(|n| n % 3 == 0 || n % 5 == 0)
                       .sum::<u32>();
                       // conbine adapter and consumer
    println!("{sum}");
}
```

The following code combines adapters, closures, and consumers to find the sum of all integers less than 1000 that are divisible by 3 or 5, showcasing the power of functional programming. This approach allows for complex calculations to be performed in a concise and efficient manner. In comparison, imperative programming may result in lengthy and difficult-to-understand code. Therefore, it is recommended to use closures with iterators, adapters, and consumers for functional programming.

```rust
fn main() {
    let mut nums: Vec<u32> = Vec::new();
    for i in 1..1000 {
        if i % 3 == 0 || i % 5 == 0 {
            nums.push(i);
        }
    }

    let sum = nums.iter().sum::<u32>();
    println!("{sum}");
}
```

Functional programming is a programming paradigm that is distinct from other paradigms such as imperative programming and declarative programming. Imperative programming is an abstraction of computer hardware, involving variables, assignment statements, expressions, control statements, etc. Structured programming and object-oriented programming, which are commonly used, fall under this paradigm. The main focus is on the steps that the computer executes, instructing it on what to do step by step. In contrast, declarative programming expresses program logic as data structures, concentrating on what to do rather than how to do it. SQL statements are an example of declarative programming. While functional programming and declarative programming share a common idea of focusing on what to do, functional programming is not limited to declarative programming. It is an abstraction of mathematics, describing computation as the evaluation of expressions. In other words, a functional program is a mathematical expression. The functions in functional programming refer to mathematical functions, which map the independent variable to the dependent variable y = f(x). The output of a function solely depends on the input parameter value, not on any other state. For instance, the sin() function in mathematics calculates the sine value of x. As long as x remains unchanged, the final result will always be the same, no matter how or when it is called.

### 1.4.10 Smart Pointer

Rust, being a systems language, still requires the use of pointers. Pointers refer to or point to other data by containing a memory address. The most common pointer in Rust is a reference, which is similar to C’s concept of pointers but has no other functionality besides referencing data. On the other hand, smart pointers are data structures that behave like pointers and contain metadata. They provide additional functions such as memory management or binding checks, like managing file handles and network connections. In Rust, Vec and String can be considered smart pointers. Smart pointers were first introduced in C++ and later adopted by Rust. Rust encapsulates two major traits for smart pointers: Deref and Drop. When a variable implements Deref and Drop, it becomes more than an ordinary variable. After implementing Deref, the variable overloads the dereference operator ”*”, which can be used as an ordinary reference and can be automatically or manually dereferenced when necessary. After implementing Drop, the variable is automatically released from the heap when it goes out of scope. Other functions can also be customized, such as releasing files or network connections, similar to some languages’ destructor functions. The following are the main features of smart pointers: 1. Smart pointers usually own the data they point to. 2. Smart pointers are data structures that are typically implemented using structures. 3. Smart pointers implement two major traits: Deref and Drop. Many common smart pointers are available, and users can also implement the smart pointers they need. The following are frequently used smart pointers or data structures. Note that although Cell and RefCell share similarities with smart pointers, they are not considered smart pointers according to the above characteristics.

- Box<T>: A unique ownership smart pointer that points to data of type T stored on the heap.
- Rc<T>: A reference counting smart pointer that shares ownership and is used to track the number of references to a value stored on the heap.
- Arc<T>: A thread-safe reference counting smart pointer that shares ownership and can be used for multi-threading.
- Cell<T>: A container that provides interior mutability and is not a smart pointer. It allows for borrowed mutable data with compile-time checks, requiring T to implement the Copy trait.
- RefCell<T>: A container that provides interior mutability and is not a smart pointer. It allows for borrowed mutable data with run-time checks, with no requirement for T to implement the Copy trait.
- Weak<T>: A weak reference type that corresponds to Rc and is used to solve the problem of circular references in RefCell.
- Cow<T>: A copy-on-write enumerated smart pointer that is primarily used to reduce memory allocation and copying. It is suitable for scenarios with frequent reads and infrequent writes.

In Rust, Deref and Drop are the two most important traits for smart pointers. By implementing Deref and Drop for a custom data type similar to Box, we can better understand the difference between references and smart pointers.

```rust
// define tuple struct
struct SBox<T>(T);
impl<T> SBox<T> {
    fn new(x: T) -> Self {
        Self(x)
    }
}

fn main() {
    let x = 10;
    let y = SBox::new(x);
    println!("x = {x}");
    // println!("y = {}", *y); cannot dereference a raw pointer
} <--- x, y call drop
```

Here is an example of implementation of Deref and Drop for SBox.

```rust
use std::ops::Deref;

// implement Deref for SBox
impl<T> Deref for SBox<T> {
    type Target = T; // define associated type,
                     // which is the type that Deref is
                        targeting to fn deref(&sefl) -> &Self::Target {
        &self.0 // .0 means the first element of tuple struct
    }
}

// implement Drop for SBox
impl<T> Drop for SBox<T> {
    fn drop(&mut self) {
        println("SBox drop itself!"); // just print a message
    }
}
```

If Deref is not implemented, a variable of our custom data type cannot be dereferenced. On the other hand, if Drop is not implemented, the variable will be released from the heap only when it goes out of scope. However, if the variable contains other references or smart pointers, they will not be released until the program exits, resulting in a memory leak. Therefore, it is crucial to implement Drop correctly to avoid memory leaks.

```rust
fn main() {
    let x = 10;
    let y = SBox::new(x);
    println!("x = {x}");
    println!("y = {}", *y); // *y equals *(y.deref())
    // y.drop(); error: drop twice
} <--- x, y call drop and y prints "SBox drop itself!"
```

Box stores its data on the heap, and after implementing Deref, it can be automatically dereferenced.

```rust
fn main() {
    let num = 10; // num stored in stack
    let n_box = Box::new(num); // n_box stored in heap
    println!("n_box = {}", n_box); // n_box deref to num
                                   // automatically
    println!("{}", 10 == *n_box); // n_box deref to num
                                   // manually
}
```

The ownership system rules state that a value can only have one owner at any given time, but in some scenarios, we need values to have multiple owners. To address this, Rust provides the Rc smart pointer. Rc is a shareable reference counting smart pointer that can produce multiple ownership values. Reference counting means that it determines whether a value is still in use by keeping track of the number of references to it, and if the reference count is zero, the value can be cleaned up. Rust’s ownership system mandates that a value can have only one owner at any given time. However, in some cases, multiple ownership is necessary. To solve this problem, Rust provides the Rc smart pointer, which is a reference counting smart pointer that can produce multiple ownership values. It tracks whether a value is still in use by counting the number of references to it. Once the reference count drops to zero, the value can be cleaned up.

b 2 None 3 4 a 1

In the example shown, 3 is shared by variables a(1) and b(2), and cloning an Rc increases the reference count. Sharing is like turning off the lights in a classroom, only the last person leaving needs to turn off the lights. Similarly, each user of Rc will only clear the data on the last use. Cloning an Rc will increase the reference count, just like when a new person enters a classroom.

```rust
use std::rc::Rc;
fn main() {
    let one = Rc::new(1);
    // increase reference count
    let one_1 = one.clone();
    // display reference count
    println!("sc:{}", Rc::strong_count(one_1));
}
```

Rc can be used for shared ownership in single-threaded environments only. For multithreaded environments, Rust provides Arc (atomic reference counting), a thread-safe version of Rc. It allocates a T type value with shared ownership on the heap. Cloning an Arc increases the reference count while producing a new Arc instance pointing to the same heap as the source Arc. Arc is immutable by default and requires locking mechanisms like Mutex to modify it between multiple threads. By default, Rc and Arc do not allow internal data modification. Rust provides two containers with internal mutability, Cell and RefCell, for scenarios where modifying internal values is necessary. Internal mutability is a Rust design pattern that allows data modification while having immutable references. Cell provides methods for getting and changing internal values. For data types that implement Copy, the get method is used to view the internal value, while the take method replaces the internal value with the

default value and returns the replaced value. For all data types, the replace method replaces and returns the replaced value, while the into_inner method consumes Cell and returns the internal value.

```rust
// use_cell.rs

use std::cell::Cell;

struct Fields {
    regular_field: u8,
    special_field: Cell<u8>,
}

fn main() {
    let fields = Fields {
        regular_field: 0,
        special_field: Cell::new(1),
    };

    let value = 10;
    // fields.regular_field = value;
    // error[E0594]: cannot assign to immutable field

    fields.special_field.set(value);
    // although fields is immutable,
    // we can still change the value of special_field

    println!("special: {}", fields.special_field.get());
}
```

To enable modification of certain fields internally, Cell provides a backdoor to immutable struct Fields. RefCell has similar characteristics to Cell, but instead of using get and set methods to modify internal data, it directly obtains a mutable reference to the data. For example, RefMut<_> can be used to modify HashMap through RefCell. Here, shared_map obtains a RefMut<_> type map directly through borrow_mut(), and then adds an element to the map through insert, which modifies shared_map.

```rust
// use_refcell.rs

use std::cell::{RefCell, RefMut};
use std::collections::HashMap;
use std::rc::Rc;

fn main() {
    let shared_map: Rc<RefCell<_>> =
        Rc::new(RefCell::new(HashMap::new()));
    {
        let mut map: RefMut<_> = shared_map.borrow_mut();
        map.insert("kew", 1);
        map.insert("shieber", 2);
        map.insert("mon", 3);
        map.insert("hon", 4);
    }
```

```rust
    let total: i32 = shared_map.borrow().values().sum();
    println!("{}", total);
}
```

While both Cell and RefCell can modify internal values, they do so differently. Cell replaces values directly, while RefCell modifies them through mutable references. Since Cell needs to replace and move values, it must implement Copy, while RefCell is suitable for data types that do not implement Copy. Cell is checked at compile time, while RefCell is checked at runtime, and misuse can lead to panics. Although Rust provides memory safety guarantees, RefCell may still cause circular references and memory leaks. To prevent this, Rust provides the Weak smart pointer, which allows for the value to be cleared even when there are circular references. The upgrade method can be used to check if the referenced value is still valid. Each time Rc is cloned, the strong reference count strong_count of the instance is increased, and the instance is only cleared when strong_count is 0. strong_count will never be 0 in circular references. When using the Weak smart pointer, the value of strong_count is not increased, but the value of weak_count does. weak_count can be cleared without being 0, which solves the problem of circular references. As Weak smart pointer, to ensure that the referenced value is still valid, its upgrade method can be called, which returns Option<Rc<T». If the Rc<T> value has not been dropped, the result is Some. If dropped, the result is None. The following is an example of using Weak to solve circular references. Car and Wheel have mutual references, and circular references will occur if they are both used with Rc.

```rust
// use_weak.rs
use std::cell::RefCell;
use std::rc::{Rc, Weak};

struct Car {
    name: String,
    wheels: RefCell<Vec<Weak<Wheel>>>,
}
struct Wheel {
    id: i32,
    car: Weak<Car>, // Weak ref Car
}

fn main() {
    let car: Rc<Car> = Rc::new(
        Car { name: "Tesla".to_string(),
                wheels: RefCell::new(vec![]),
        }
    );
    let wl1 = Rc::new(Wheel{ id:1, car: Rc::downgrade(&car) });
    let wl2 = Rc::new(Wheel{ id:2, car: Rc::downgrade(&car) });

    {
        let mut wheels = car.wheels.borrow_mut();
        wheels.push(Rc::downgrade(&wl1)); // downgrade to Weak
        wheels.push(Rc::downgrade(&wl2));
    } // make sure ref is ended

    for wheel_weak in car.wheels.borrow().iter() {
        if let Some(wl) = wheel_weak.upgrade() {
            println!("wheel {} owned by {}", wl.id,
                wl.car.upgrade().unwrap().name);
```

```rust
        } else {
            println!("wheel weak reference has been dropped");
        }
    }
}
```

Now, let’s take a look at Cow (Copy on Write) Smart Pointer.

```rust
pub enum Cow<'a, B>
    where B: 'a + ToOwned + 'a + ?Sized {
    Borrowed(&'a B), // wrap a reference
    Owned(<B as ToOwned>::Owned), // wrap a onwed value
}
```

The concept of borrowing involves accessing borrowed content in an immutable way, while ownership means cloning the data when mutable borrowing is needed. To filter out all spaces in a string, we can use the following code.

```rust
// use_cow.rs
fn delete_spaces(src: &str) -> String {
    let mut dest = String::with_capacity(src.len());
    for c in src.chars() {
        if ' ' != c {
            dest.push(c);
        }
    }
    dest
}
```

While this code works, its efficiency is not optimal. First, we need to decide whether to use &str or String for the parameter. If we use String but input &str, we need to clone it before calling the function. If we use String, the string will be moved to the interior after the call, and the external cannot use it anymore. In either case, a string generation and copy are performed in the function. If the string does not contain whitespace characters, it is best to return it as is without copying. This is where Cow comes in handy as it reduces copying and improves efficiency.

```rust
// use_cow.rs
use std::borrow::Cow;
fn delete_spaces2<'a>(src: &'a str) -> Cow<'a, str> {
    if src.contains(' ') {
        let mut dest = String::with_capacity(src.len());
        for c in src.chars() {
            if ' ' != c { dest.push(c); }
        }
        // capture the ownership and drop dest
        return Cow::Owned(dest);
    }
    return Cow::Borrowed(src); // borrow the src
}
```

Here is an example that utilizes Cow.

```rust
// use_cow.rs
fn main() {
    let s = "i love you";
```

```rust
    let res1 = delete_spaces(s);
    let res2 = delete_spaces2(s);
    println!("{res1}, {res2}");
}
```

When there are no whitespace characters, the function returns directly, avoiding copying and improving efficiency.

```rust
// more_cow_usage.rs

use std::borrow::Cow;
fn abs_all(input: &mut Cow<[i32]>) {
    for i in 0..input.len() {
        let v = input[i];
        if v < 0 { input.to_mut()[i] = -v; }
    }
}
fn main() {
    // read only, no write, no copy
    let a = [0, 1, 2];
    let mut input = Cow::from(&a[..]);
    abs_all(&mut input);
    assert_eq!(input, Cow::Borrowed(a.as_ref()));
    // copy on write, copy when read -1
    let b = [0, -1, -2];
    let mut input = Cow::from(&b[..]);
    abs_all(&mut input);
    assert_eq!(input, Cow::Owned(vec![0,1,2]) as Cow<[i32]>);
    // no copy on write, because already owned
    let mut c = Cow::from(vec![0, -1, -2]);
    abs_all(&mut c);
    assert_eq!(c, Cow::Owned(vec![0,1,2]) as Cow<[i32]>);
}
```

This section contains a lot of diverse content, and readers are encouraged to study it further in conjunction with other dedicated books. The information provided here is only brief and not deeply discussed.

### 1.4.11 Exception

Rust provides a unique exception handling mechanism as it does not have try-catch blocks like other languages. This section is titled ”Exceptions,” but the author has used the term to refer to failures, errors, and exceptions collectively. There are four types of exceptions in Rust: Option, Result, Panic, and Abort. Option is used to handle possible failure cases, indicating whether the operation succeeded or failed with Some and None. For instance, when getting a value that may not exist, the result may be None, which should not cause an error but needs to be handled appropriately. Failure is different from error, as it is an anticipated outcome that will not cause problems for the program. The definition of Option, which we have already learned, is provided below.

```rust
enum Option<T> {
    Some(T),
    None,
}
```

Result is used to handle recoverable errors and represents success and failure. An error may not necessarily cause the program to crash, but it needs to be specifically handled to allow the program to continue executing. The definition of Result is as follows:

```rust
enum Result<T,E> {
    Ok(T),
    Err(E),
}
```

Opening a file that does not exist, accessing a file without permission, or attempting to convert a non-numeric string to a number will result in Err(E).

```rust
use std::fs::File;
use std::io::ErrorKind;

let f = File::open("kw.txt");
let f = match f {
    Ok(file) => file,
    Err(err) => match err.kind() {
    ErrorKind::NotFound => match File::create("kw.txt"){
        Ok(fc) => fc,
        Err(e) => panic("Error while creating file!"),
    }
    ErrorKind::PermissionDenied => panic("No permission!"),
    other => panic!("Error while openning file"),
}
```

In Rust, handling errors is crucial, and there are various mechanisms to achieve it. One of them is the panic mechanism, which should only be used when no other solution is available. When encountering an unrecoverable error, panic will immediately stop the program’s execution to allow the programmer to identify the problem. This mechanism is also useful for cleaning up memory. However, if you do not want to use panic to clean up when encountering such errors, you can use the abort mechanism to let the operating system handle it instead. Although error handling in Rust may look verbose when using match, there are more concise options available. For example, you can use the unwrap or expect methods to handle errors.

```rust
use std::fs::File;
use std::io;
use std::io::Read;

fn main() {
   let f = File::open("kew.txt").unwrap();
   let f = File::open("mon.txt").expect("Open file failed!");
   // expect gives more specific error message than unwrap
}
```

If you only want to propagate the error and not handle it, you can use the ”?” operator. In this case, the return type is Result, which returns String on success and io::Error on failure.

```rust
fn main() {
    let s = read_from_file();
    match s {
        Err(e) => println!("{}", e),
        Ok(s) => println!("{}", s),
    }
```

```rust
}

fn read_from_file() -> Result<String, io::Error> {
    let f = File::open("kew.txt")?; // if error, throw it
    let mut s = String::new();
    f.read_to_string(&mut s);

    Ok(s)
}
```

When working with errors in Rust, you have to choose between using Option or Result depending on the type of failure or error you are handling. Option is used for handling possible failures and represents success or failure with Some or None. On the other hand, Result is used for handling recoverable errors and represents success and failure with Ok or Err. It is essential to handle errors appropriately to avoid program crashes. Finally, note that Option and Result are very similar, as Option<T> can be seen as Result<T, ()>.

### 1.4.12 Macro

Rust does not have built-in library functions, meaning that programmers must define everything themselves. However, Rust offers a set of powerful macros, including declarative and procedural macros, that can accomplish many tasks. Unlike C macros, Rust macros are more powerful and widely used. For instance, using the ”derive” macro, new functionality can be added to structures, and commonly used methods like ”println!”, ”vec!”, and ”panic!” are also macros. There are two main categories of macros in Rust: declarative macros declared using ”macro_rules!” and procedural macros, further divided into custom derive macros, function-like macros, and attribute macros. We’ve already covered declarative and custom derive macros, so this section will still focus on those. Readers can refer to related materials for other macro types. The format of a declarative macro is ”macro_name!()”, ”macro_name![]”, or ”macro_name!”. These macros all use a macro name followed by an exclamation mark, which is of one of these bracket types (), [], {}. Different macro purposes require different brackets, with ”vec![]” not being the same as ”vec!()”. The latter looks more like a function and is the reason ”println!()” uses parentheses. However, any of these brackets can be used and different brackets are just to satisfy the unity of meaning and form.

```text
macro_rules! macro_name {
    ($matcher) => {
        $code_body;
        return_value
    };
}
```

In the macro definition, ”$matcher” marks syntax elements like empty, identifiers, literals, keywords, symbols, patterns, and regular expressions. The ”$” symbol captures values, which are then used in ”$code_body” to process and potentially return a value. For example, the following macro can be used to calculate the left and right child nodes of a binary tree parent node ”p”, with the left and right child node indices being ”2p” and ”2p+1”, respectively.

```text
macro_rules! left_child {
    ($parent:ident) => {
        $parent << 1
    };
}
macro_rules! right_child {
```

```text
    ($parent:ident) => {
        ($parent << 1) + 1
    };
}
```

When calculating left and right child nodes, macros such as ”left_child!(p)” and ”right_child!(p)” can be used instead of expressions like ”2 * p” and ”2 * p + 1”. This simplifies the code and clarifies its meaning. The ”indent” and colon in the macro are metavariable specifiers. ”Indent” is an attribute of ”parent”, indicating that ”parent” is a value. Rust’s macros rely on these specifiers to function correctly. The second form of macros is called procedural macros because they are more like a process or function. They take code as input and produce other code as output. Derive macros, a type of procedural macro, add new functionality to code directly. The following example uses the ”derive” macro to add the ”Clone” method to ”Student”, so that ”Student” can directly call ”clone()” to achieve copying. This is a simplified writing of ”impl Clone for Student”.

```rust
#[derive(Clone)]
struct Student;
```

Multiple traits can also be placed in ”derive” simultaneously, allowing for implementation of various functions.

```rust
#[derive(Debug, Clone, Copy)]
struct Student;
```

Macros are a complex topic and should only be used when necessary and when they simplify the code. It’s not recommended to use macros for their own sake.

### 1.4.13 Code Organization and Dependency

In Rust, there are several concepts to understand for organizing code, including packages, crates, libraries, and modules. When using the ”cargo new” command, Rust generates a package that contains multiple directories, each of which is a crate. After compilation, a crate can either be a binary executable or a library that can be used by other functions. Within a crate, there are typically multiple .rs files, which are called modules and are accessed using the ”use” keyword. The table below provides a detailed overview of these concepts and their corresponding terms in Rust.

```rust
package --> crates
                    (dirs)
                               a package have multiple crates
crate
        --> modules (lib/EFL)
                               a crate have multiple modules
                               which can be compiled into a
                               library or executable file
module
        --> file.rs (file)
                               a module can contain one or
                               more .rs files
package
                   <-- package name
|-- Cargo.toml
|-- src
                   <-- crate
|
     |-- main.rs
                   <-- main module
|
     |-- lib.rs
                   <-- module, library module
|
     |-- math
                   <-- module, math module
|
         |- mod.rs <-- module, import add/sub from modules
|
         |- add.rs <-- module, implement add of math module
|
         |- sub.rs <-- module, implement sub of math module
|-- file
                   <-- crate
     |-- core
                   <-- module, file operation module
     |-- clear
                   <-- module, clear module
```

To organize a large project, it is recommended to follow this approach when using Rust libraries. The Tikv codebase is a good example to follow. Rust also offers many standard libraries for solving general programming tasks. By studying these libraries, developers can deepen their understanding of Rust and find inspiration for solving real-world problems. The standard libraries in Rust include:

```text
alloc
             env
                       i64
                                 pin
                                             task
any
             error
                       i128
                                 prelude
                                             thread
array
             f32
                       io
                                 primitive
                                             time
ascii
             f64
                       isize
                                 process
                                             u8
borrow
             ffi
                       iter
                                 raw
                                             u16
boxed
             fmt
                       marker
                                 mem
                                             u32
cell
             fs
                       net
                                 ptr
                                             u64
char
             future
                       num
                                 rc
                                             u128
clone
             hash
                       ops
                                 result
                                             usize
cmp
             hint
                       option
                                 slice
                                             vec
collections
             i8
                       os
                                 str
                                             backtrace
convert
             i16
                       panic
                                 string
                                             intrinsics
default
             i32
                       path
                                 sync
                                             lazy
```

![Figure 1.1: Rust package dependency](images/fig-1.1.png)

*Figure 1.1: Rust package dependency*

The image shown here is a simplified dependency graph of Rust libraries. It was created to illustrate how Rust as a language is built and how the language’s libraries are interrelated. These libraries are considered the de facto standards of Rust, with some being fundamental and serving as dependencies for other libraries.

An analysis of Rust’s standard libraries revealed that they can be divided into three layers: core, alloc, and std. Each layer builds upon the previous one, with std being the top layer, alloc in the middle, and core serving as the most critical layer. Core is responsible for defining and implementing various core concepts in Rust’s basic syntax, such as variables, numbers, characters, and Boolean types. These are the foundational concepts that beginners learn when studying Rust’s basics.

### 1.4.14 Project: a password generator

In the previous sections, we covered many basic Rust concepts. Now, let’s apply them to a comprehensive project. In this project, readers will learn how to organize Rust project code, import modules, use various annotations, write tests, and build command-line tools. In the age of the internet, people have numerous accounts and passwords to remember. Unfortunately, it’s challenging to remember unique passwords for each account, and people often set similar or identical passwords, leaving themselves vulnerable to hacking. Although password management software can help, relying on someone else’s software to manage your own passwords can make you uneasy. To solve this problem, the author created PasswdGenerator, a command-line tool that generates passwords that are at least 16 characters long and appear like random strings, such as 9KbAM4QWMCcyXAar. PasswdGenerator can generate complex passwords of default length 16 by controlling the seed parameter, and the length parameter can adjust password length. This tool makes generating different passwords for all kinds of accounts easy, allowing users to input a digit or character that only they know to generate complex passwords. Using PasswdGenerator, the author generated different passwords for all his accounts and, because he thought of the seed himselve, he didn’t have to worry about forgetting it. PasswdGenerator has been used for several years, and the author doesn’t even know his passwords for WeChat, Alipay, Twitter, Youtube, Github accounts etc. PasswdGenerator is a command-line tool, and its usage method is similar to that of command-line tools in Unix-like systems. Therefore, its first usage is ”PasswdGenerator -h” or ”PasswdGenerator –help”.

```text
shieber@kew $ PasswdGenerator -h
PasswdGenerator 0.1.0
A simple password generator for any account
USAGE:
    PasswdGenerator [OPTIONS] --seed <SEED>
OPTIONS:
    -h, --help
                             Prints help information
    -l, --length <LENGTH>
                             Length of password [default: 16]
    -s, --seed <SEED>
                             Seed to generate password
    -V, --version
                             Prints version information
```

The USAGE section provides instructions on how to use the tool, while the OPTIONS section displays the control parameters.

```text
shieber@kew $ PasswdGenerator -s wechat
wechat: GQnaoXobRwrgW21A
```

The output of the PasswdGenerator tool begins with a short seed, such as ”wechat,” which can be customized with prefixes or suffixes to associate it with a specific account. The seed serves to indicate that the password was generated specifically for that account.

```text
shieber@kew $ PasswdGenerator -s wechat -l 20
wechat: GQnaoXobRwrgW21Ac2Pb
```

The length of the password is controlled by the ”-l” parameter. If this parameter is not included, the password defaults to a length of 16, which is sufficient in the vast majority of cases. To handle command-line arguments, the clap library can be used, as shown below.

```rust
use clap::Parser;
/// A simple password generator for any account
#[derive(Parser, Debug)]
#[clap(version, about, long_about= None)]
struct Args {
    /// Seed to generate password
    #[clap(short, long)]
    seed: String,
    /// Length of password
    #[clap(short, long, default_value_t = 16)]
    length: usize,
}
```

The ”seed” and ”length” are the two command-line arguments, including their short and long forms, with ”length” having a default value of 16. The command-line arguments can be obtained by calling Args::parse(). Once the command-line arguments are obtained, the next step is to generate the password. My approach was to use a combination of a hash algorithm and base64 encoding. While there are many types of hash algorithms and various libraries available for generating hashes, it is practical to write a hash algorithm oneself. Here, I chose to use Mersenne primes to generate hash values. To generate the hash value, the ASCII value of each character in the seed is multiplied by its corresponding index value, and the result is taken modulo the Mersenne prime 127. The remainder is then raised to the third power to obtain the hash value of the seed. Mersenne primes are prime numbers of the form Mn = 2n −1, where n is also a prime number. While 2n−1 may not always be a prime number, as in the case of primes such as 11, 23, and 29, Mersenne primes have the property that both n and Mn must be prime, making them suitable for calculating the hash value here. Some examples of Mersenne primes include 3, 7, 31, and 127 are shown below, in which 127 is the fourth Mersenne prime.

```text
No
         n
                 Mn
1
         2
                 3
2
         3
                 7
3
         5
                 31
4
         7
                 127
5
         13
                 8191
6
         17
                 131071
7
         19
                 524287
8
         31
                 2147483647
9
         61
                 2305843009213693951
10
         89
                 618970019642690137449562111
```

One method to convert a hash value to a string is by character replacement. The hash value is first modulo-ed with a fixed-length string (password), which results in a remainder used as an index to obtain a character. Repeating this process cyclically generates a string of characters that can be concatenated to form the password. For more complexity, the seed can be split and concatenated with the generated password.

```rust
// conbine seed and passwd
let interval = passwd.clone();
for c in seed.chars() {
    passwd.push(c);
    passwd += &interval;
}
```

To make the password suitable for use, any unsuitable characters in the password string can be converted to Base64 encoding, which uses 64 visible characters. Additionally, ”+” and ”/” in Base64 can be replaced with ”*” in the password.

```text
// encode passwd (base64)
passwd = encode(passwd);
passwd = passwd.replace("+", "*").replace("/", "*");
```

If the password is still not long enough, it can be cyclically written into itself and wrapped with the seed and password using format, then returned.

```rust
let interval = passwd.clone();
while passwd.len() < length {
    passwd += &interval;
}
format!("{}: {}", seed, &passwd[..length])
```

The tool uses three functions: ”hash” crate to calculate the Mersenne hash value, ”encryptor” crate to generate the password, and the main module to obtain command-line arguments. The main module calls the ”generate_password” function from ”encryptor” crate, which in turn calls ”mersenne_hash” function from ”hash” crate to calculate the hash value. To organize the code, we can use Cargo’s workspace mechanism to generate corresponding crates by specifying their names. The first step is to create and enter a directory.

```text
shieber@kew $ mkdir PasswdGenerator && cd PasswdGenerator
```

Then, we need to write a ”Cargo.toml” file that defines the names of the crates we want to generate.

```text
[workspace]
members = [
    "hash",
    "encryptor",
    "main",
]
```

After that, we can use ”cargo” to generate the three crates. Note that different parameters should be used to generate the library and the main program.

```text
shieber@kew $ cargo new hash --lib
    Created library hash package
shieber@kew $ cargo new encryptor --lib
    Created library encryptor package
shieber@kew $ cargo new main
    Created binary (application) main package
```

Once generated, the directory structure should look like the following table.

```text
.
|-- Cargo.toml
|-- encryptor
|   |-- Cargo.toml
|   |-- src
|
        |-- lib.rs
|-- hash
|   |-- Cargo.toml
|   |-- src
|
        |-- lib.rs
|-- main
    |-- Cargo.toml
    |-- src
        |-- main.rs
6 directories, 7 files
```

In each crate, the modules need to be exported for use by the main program. For example, in the ”hash” library, we can implement the ”mersenne_hash” function in ”merhash.rs” and export it in ”lib.rs”. Similarly, in the ”encryptor” library, we can implement the function for generating passwords in ”password.rs” and export it in ”lib.rs”. The ”lib.rs” files of each crate should only be used to export functions. For mersenne_hash, it can be encapsulated in merhash.rs, while the function for generating passwords can be encapsulated in password.rs. The final directory looks like this:

```text
|-- Cargo.toml
|-- encryptor
|   |-- Cargo.toml
|   |-- src
|
        |-- lib.rs
|
        |-- password.rs
|-- hash
|   |-- Cargo.toml
|   |-- src
|
        |-- lib.rs
|
        |-- merhash.rs
|-- main
    |-- Cargo.toml
    |-- src
        |-- main.rs
6 directories, 9 files
```

It is important to note that the ”hash” library does not depend on the external libraries and can be implemented first.

```rust
// hash/src/lib.rs

pub mod merhash; // export module merhash

#[cft(test)] // test module
mod tests {
```

```rust
    use crate::merhash::mersenne_hash;

    #[test]
    fn mersenne_hash_works() {
        let seed = String::from("jdxjp");
        let hash = mersenne_hash(&seed);
        assert_eq!(2000375, hash);
    }
}
```

Then, we implement merhash.

```rust
// hash/src/merhash.rs

//! Mersenne Hash
//!
/// calculate hash value with mersenne prime 127
///
/// # Example
/// use hash::merhash::mersenne_hash;
///
/// let seed = "jdxjp";
/// let hash = mersenne_hash(&seed);
/// assert_eq!(2000375, hash);
pub fn mersenne_hash(seed: &str) -> usize {
    let mut hash: usize = 0;

    for (i, c) in seed.chars().enumerate() {
        hash += (i + 1) * (c as usize);
    }

    (hash % 127).pow(3) - 1
}
```

To ensure the code is well-documented and easy to maintain, document comments and module comments are used throughout the project. Tests are also included in the document comments, which is very convenient for testing and subsequent document maintenance. To complete the ”encryptor” library, we need to rely only on the external ”base64” library. In addition, to handle error situations, the ”anyhow” library is also introduced. To do this, we open the ”Cargo.toml” file under the ”encryptor” directory and add the necessary dependencies under the ”[dependencies]” section, including the ”anyhow” and ”base64” libraries, as well as the ”hash” library that was previously written.

```text
[package]
name = "encryptor"
authors = ["shieber"]
version = "0.1.0"
edition = "2021"

[dependencies]
anyhow = "1.0.56"
base64 = "0.13.0"
hash = { path = "../hash" }
```

The implementation of the ”password.rs” module is shown below.

```rust
// encryptor/src/lib.rs

pub mod password; // export module password

// encryptor/src/password.rs
use anyhow::{bail, Error, Result};
use base64::encode;
use hash::merhash::mersenne_hash;

/// crypto(length=100), you can exchange/add/delete characters
const CRYPTO: &str = "!pqHr$*+ST1Vst_uv:?wWS%X&Y-/Z01_2.34<ABl
9ECo|x#yDE^F{GHEI[]JK>LM#NOBWPQ:RaKU@}cde56R7=8f/9gIhi,jkzmn";

/// Password generator with hash value, use hash value's high
/// power to get character from CRYPTO
///
/// #Example
/// use encryptor::password::generate_password;
/// let seed = "jdwnp";
/// let length = 16;
/// let passwd = generate_password(seed, length);
/// match passwd {
/// Ok(val) => println!("{:#?}", val),
/// Err(err) => println!("{:#?}", err),
/// }
pub fn generate_password(seed: &str, length: usize)
    -> Result<String, Error>
{
    // check password length
    if length < 6 {
        bail!("length must >= 6"); // return error
    }

    // calculate mer_hash
    let p = match length {
        6..=10 => 1,
        11..=15 => 2,
        16..=20 => 3,
        _ => 3,
    };
    let mut mer_hash = mersenne_hash(seed).pow(p);

    // calculate password by mer_hash
    let mut passwd = String::new();
    let crypto_len = CRYPTO.len();
    while mer_hash > 9 {
        let loc = mer_hash % crypto_len;
        let nthc = CRYPTO.chars()
                         .nth(loc)
                         .expect("Error while getting char!");
```

```rust
        passwd.push(nthc);
        mer_hash /= crypto_len;
    }

    // combine seed and passwd
    let interval = passwd.clone();
    for c in seed.chars() {
        passwd.push(c);
        passwd += &interval;
    }

    // encode passwd to base64
    passwd = encode(passwd);
    passwd = passwd.replace("+", "*").replace("/", "*");

    // length is not enough, use interval to fill
    let interval = passwd.clone();
    while passwd.len() < length {
        passwd += &interval;
    }

    // return first length characters as password
    Ok(format!("{}: {}", seed, &passwd[..length]))
}
```

In the ”Cargo.toml” of the main module, we introduce the necessary libraries, and note that the name is ”PasswdGenerator”.

```text
[package]
name = "PasswdGenerator"
authors = ["shieber"]
version = "0.1.0"
edition = "2021"

[dependencies]
anyhow = "1.0.56"
clap = { version= "3.1.6", features= ["derive"] }
encryptor = { path = "../encryptor"}
```

Finally, in the main function, we call the ”encryptor” and command line structure to generate passwords and return them.

```rust
// passwdgenerate/src/main.rs

use anyhow::{bail, Result};
use clap::Parser;
use encryptor::password::generate_password;

/// A simple password generator for any account
#[derive(Parser, Debug)]
#[clap(version, about, long_about= None)]
struct Args {
    /// Seed to generate password
```

```rust
    #[clap(short, long)]
    seed: String,

    /// Length of password
    #[clap(short, long, default_value_t = 16)]
    length: usize,
}

fn main() -> Result<()> {
    let args = Args::parse();

    // seed must be longer than 4 characters
    if args.seed.len() < 4 {
        bail!("seed {} length must >= 4", &args.seed);
    }

    let (seed, length) = (args.seed, args.length);
    let passwd = generate_password(&seed[..], length);
    match passwd {
        Ok(val) => println!("{}", val),
        Err(err) => println!("{}", err),
    }

    Ok(())
}
```

Once the program is complete, compile it with ”cargo build –release” to get the ”PasswdGenerator” command line tool in the ”target/release/” directory. You can put it in the ”/usr/local/bin” directory so that you can use it anywhere on the system. Of course, using ”cargo doc” can also generate a ”doc” directory, which contains detailed documentation about the project. Through this small project, readers have become familiar with Rust code organization, module usage, testing methods, and coding styles. Although this password generator is simple, it is completely sufficient for personal use.

## 1.5 Summary

In this chapter, we provide an overview of Rust fundamentals. Firstly, we begin by introducing the installation of the Rust toolchain and summarizing some learning resources. We then review Rust basics, covering variables, functions, ownership, lifetimes, generics, traits, smart pointers, error handling, and macro systems. After that, we present a comprehensive project that implements a command-line tool using Rust. Although the content of this chapter is relatively basic, it is essential to understand these concepts to build more complex projects in Rust. Readers who need further clarification are recommended to refer to the Rust documentation. By the end of this chapter, readers will have a general understanding of Rust. In the following chapters, we will delve into learning data structures and algorithms.
