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
