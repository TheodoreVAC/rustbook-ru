## 10.3 Trie

Trie, also known as a radix tree or prefix tree, is a tree data structure used to search for words or prefixes. It has a wide range of applications, including auto-completion, spell checking, typing prediction, and more. While balanced trees and hash tables can also be used to search for words, they cannot quickly find all words with the same prefix or enumerate all stored words in lexicographical order. Hash tables can find a word in O(1) time, but as the number of words grows, the hash table may become too large and increase the time complexity to O(n) due to collisions. In contrast, Trie uses less space to store multiple words with the same prefix, and its time complexity is only O(m), where m is the length of the word. The time complexity of searching for a word in a balanced tree is O(mlog(n)). The structure of Trie is shown in the figure below. Storing words only requires processing 26 letters, and words with the same prefix share the same prefix, which saves storage space. For example, ”apple” and ”appeal” share ”app,” and ”boom” and ”box” share ”bo.”

root a b p u m o y p o x t d e m l e a l

To implement Trie, we first need to abstract the node, similar to the node in the above figure. The node stores the reference to its child nodes and the state of the current node. The state indicates whether this node is the end of a word (”end”), which can be used to determine whether the word ends when searching. In addition, the root node is the entrance to Trie and used to represent the entire Trie.

```rust
// trie.rs

// Definition of Trie
#[derive(Default, Debug)]
struct Trie {
    root: Node,
}

// Definition of Trie node
#[derive(Default)]
struct Node {
    end: bool,
    children: [Option<Box<Node>>; 26], // List of letter nodes
}

impl Trie {
```

```rust
    fn new() -> Self {
        Self::default()
    }

    // Insert word
    fn insert(&mut self, word: &str) {
        let mut node = &mut self.root;

        // Insert character by character
        for c in word.as_bytes() {
            let index = (c - b'a') as usize;
            let next = &mut node.children[index];
            node = next.get_or_insert_with(
                        Box::<Node>::default);
        }

        node.end = true;
    }

    fn contains(&self, word: &str) -> bool {
        self.word_node(word)
            .map_or(false, |n| n.end)
    }

    // Check if there exists a word with a certain prefix
    fn start_with(&self, prefix: &str) -> bool {
        self.word_node(prefix)
            .is_some()
    }

    // Prefix string (wps: word_prefix_string)
    fn word_node(&self, wps: &str) -> Option<&Node> {
        let mut node = &self.root;
        for c in wps.as_bytes() {
            let index = (c - b'a') as usize;
            match &node.children[index] {
                None => return None,
                Some(next) => node = next.as_ref(),
            }
        }

        Some(node)
    }
}

fn main() {
    let mut trie = Trie::new();
    trie.insert("box");
    trie.insert("insert");
    trie.insert("apple");
    trie.insert("appeal");
```

```rust
    let res1 = trie.contains("apple");
    let res2 = trie.contains("apples");
    let res3 = trie.start_with("ins");
    let res4 = trie.start_with("ina");
    let res5 = trie.word_node("box");

    println!("word 'apple' in Trie: {res1}");
    println!("word 'apples' in Trie: {res2}");
    println!("prefix 'ins' in Trie: {res3}");
    println!("prefix 'ina' in Trie: {res4}");
    println!("{:?}", res5);
}
```

The following are outputs after execution.

```text
word 'apple' in Trie: true
word 'apples' in Trie: false
prefix 'ins' in Trie: true
prefix 'ina' in Trie: false
Some(Node { end: true, children: [None, ..., None] })
```
