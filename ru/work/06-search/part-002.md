## 6.2 What is Searching?

In this chapter, we will use the data structures we have previously implemented (stacks, queues, and linked lists) to solve practical search and sort problems. Search and sort are fundamental tasks in computer science, and many software applications and algorithms are developed around them. You are likely familiar with the search function in various software applications you have used, such as finding specific characters in a Word document or using the search bar in Goolge browser to find information. Search and lookup mean the same thing, and this book does not distinguish between the two. Searching is the process of finding a specific item within a set of items. Search algorithms typically return either true or false to indicate whether the item exists in the set, and sometimes they also return the position of the item. In Rust, we can use the contains() function to query whether an item is in a set. This function checks whether the data contains a certain value and performs a search for us.

```rust
fn main() {
    let data = vec![1,2,3,4,5];
    if data.contains(&3) {
        println!("Yes");
    } else {
        println!("No");
    }
}
```

While contains() is a simple search algorithm, there are many different search methods available, including sequential search, binary search, and hash search. We will explore how these different algorithms work and what their complexities are.
