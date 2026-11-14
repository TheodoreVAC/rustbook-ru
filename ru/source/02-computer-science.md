# Computer Science

## 2.1 Objectives

- Understand the ideas of computer science.
- Understand the concept of abstract data types.
- Review the basics of the Rust programming language.

## 2.2 Getting Started

In the realm of computer technology, acquiring a solid understanding of the fundamentals is crucial to effectively solving problems. However, even with this foundation, tackling some problems can still be challenging. The complexity of a problem and its corresponding solution can often obscure the key ideas needed to reach a resolution. Additionally, since problems can have multiple solutions, each with its own constraints and logic, trying to combine the structure of one problem with the solution logic of another can lead to trouble. This chapter focuses on computer science, algorithms, and data structures, specifically examining why studying these topics is essential. By understanding the structure and logic of problem statements, we can better approach solving problems.

## 2.3 What is Computer Science?

Computer science is a challenging field to define, possibly due to the word ”computer” in its name. However, computer science is not limited to the study of computers alone, as it encompasses the study of problems, solutions, and the process of generating solutions. The objective of computer scientists is to create an algorithm, a set of instructions, to solve a given problem instance. Following this algorithm allows similar problems to be solved in a finite amount of time. Although computer science can be regarded as the study of algorithms, it is important to recognize that some problems do not have algorithms to solve them, such as NP-complete problems [9]. Although these problems cannot currently be solved, researching them is essential because solving them could result in technological advancements. Like the ”Goldbach Conjecture [10]”, research into it has developed many tools. Therefore, computer science can be defined as the study of solvable problem solutions and unsolvable problem ideas. When describing problems and solutions, a computable problem is one that has an algorithm to solve it. In contrast, computer science can be defined as ”the study of whether there is a solution to problems that are computable and non-computable.” It is noteworthy that this definition does not mention the word ”computer.” Solutions are independent of the machine and consist of ideas, regardless of whether a computer is employed.

Computer science focuses on the art of problem-solving, which is achieved through abstraction. Abstraction allows us to consider problems and their solutions from a logical perspective, rather than being bogged down by physical details. An everyday example of this is driving a car. As a driver, you interact with the car to reach your destination, using functions provided by the car’s designer, such as the key, engine, gears, brakes, accelerator, and steering wheel. These functions are interfaces that simplify the driving experience. In contrast, a car mechanic has a different perspective. They understand the inner workings of the car, including the engine, transmission, temperature control, and windshield wipers. These details operate at the physical level and happen ”under the hood.” Similarly, users interact with computers from a logical perspective, using programs such as email, document editors, and media players. In contrast, computer scientists, programmers, and system administrators work at a lower level, understanding how the operating system works, how to configure network protocols, and how to write control function scripts. The key concept behind both of these examples is abstraction. By hiding the complex details of the system, an interface simplifies the user’s interaction with the computer. Rust’s mathematical calculation functions are a good example of this.

```rust
// sin_cos_function.rs

fn main() {
    let x: f32 = 1.0;
    let y = x.sin();
    let z = x.cos();
    println!("sin(1) = {y}, cos(1) = {z}");
    // sin(1) = 0.84147096, cos(1) = 0.5403023
}
```

We may not know how to calculate the sine and cosine values, but as long as we understand how to use the function, that’s all we need. Someone has implemented the algorithm for calculating sine and cosine, and we can trust that the function will return the correct result. This is the idea of a ”black box.” The interface describes the function’s input and output, while the details of the algorithm are hidden within.

![Figure 2.1: calculate the sine value](images/fig-2.1.png)

*Figure 2.1: calculate the sine value*

## 2.4 What is Programming?

Programming is the process of converting algorithms into computer instructions. An algorithm is a set of steps that produces a solution based on data and expected results. It is essential to have a solution before writing a program. Although computer science is not solely about programming, programming is a crucial skill for computer scientists. When programming, one organizes the problem statement structure in their mind and expresses it clearly for efficient computer processing. To represent processes and data, programming languages must provide control methods and various data types. Control methods allow for algorithms to be expressed clearly and unambiguously, with sequential processing, selection, and iterative repetition being the minimum requirements. All data items in a computer are represented in binary form, and data types provide an interpretation and presentation of this binary data. Data types are abstractions of the physical world used to represent

entities in the problem, with underlying primitive data types such as integer and floating-point data types being the foundation for algorithm development. The operations that can be performed on data are also described in the data type. For example, the most fundamental operations for numbers are addition, subtraction, multiplication, and division. However, programming languages’ simple structures and data types may not always suffice to represent complex solutions. To control this complexity, more reasonable data management methods (data structures) and operation processes (algorithms) are required.

## 2.5 Why Study Data Structures and Abstract Data Types?

Computer scientists use abstraction to manage the complexity of problems and obtain concrete steps to solve them. Abstraction allows them to focus on the big picture without getting lost in the details. Creating a domain model enables computers to solve problems more effectively, and algorithms can be described in a more consistent manner.

![Figure 2.2: system level diagram](images/fig-2.2.png)

*Figure 2.2: system level diagram*

An Abstract Data Type (ADT) is a logical description of how to view and operate on data. It provides a level of abstraction where only the meaning of the data is of concern, not its final storage form. By wrapping the data in this way, implementation details can be hidden. The user’s interaction with the interface is an abstract operation, while the user and shell are abstract data types. Although the specific operations are not known, understanding their interaction mechanism is still possible. This is the benefit of abstract data types for algorithm design. To implement abstract data types, primitive data types are used to build new data types from a physical view, known as data structures. There are usually many different ways to implement abstract data types, but different implementations should have the same physical view. This allows programmers to change implementation details without altering the interaction method, and users to continue to focus on the problem. The common logic for abstract data types includes creating new data types, retrieving data, adding, deleting, searching, modifying, checking for empty data, and computing size. For example, to implement a queue, its abstract data type logic should include at least: new(), is_empty(), len(), clear(), enqueue(), and dequeue(). Once the specific operational logic is known, implementation becomes simple, and there are various ways to implement it as long as these abstract logic exists.

## 2.6 Why Study Algorithms?

In the computer world, the goal is to use algorithms that are efficient in terms of speed and memory usage. However, some problems may be difficult to handle, and no algorithm can provide an answer within an expected time frame. In such cases, it is important to distinguish between problems that have

solutions and those that do not, as well as problems that have solutions but require significant time or resources. As computer scientists, we need to evaluate and compare different solutions to determine the most appropriate one. Learning from the problem-solving approaches of others is an efficient way to develop our skills. By examining different solutions, we can gain insights into how various algorithm designs help us tackle challenging problems. By studying various algorithms, we can uncover their core principles and develop a universal algorithm that can be applied to similar problems in the future. However, for the same problem, different people may provide different algorithm implementations. As we saw earlier in the example of computing sine and cosine, there can be many different implementation versions. If one algorithm can achieve the same result as another algorithm in less time, it is obviously the better option.

## 2.7 Summary

This chapter delves into the concepts of computer science thinking and abstract data types, providing clear definitions and highlighting the roles of algorithms and data structures. By abstracting data types, specific implementation and operation logic is removed, which clarifies the boundaries between data structures and algorithms and significantly simplifies the process of algorithm design. In the forthcoming chapters, we will continue to utilize abstract data types to design various data structures.
