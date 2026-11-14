## 10.3 Бор (trie)

Бор (trie), также известный как дерево сжатых префиксов (radix tree) или префиксное дерево (prefix tree), — это древовидная структура данных, предназначенная для поиска слов или префиксов. Он имеет широкий спектр применений, включая автодополнение, проверку орфографии, предсказание при наборе текста и многое другое. Хотя сбалансированные деревья и хеш-таблицы также можно использовать для поиска слов, они не позволяют быстро найти все слова с одинаковым префиксом или перечислить все сохранённые слова в лексикографическом порядке. Хеш-таблица может найти слово за время O(1), но по мере роста количества слов она может стать слишком большой и из-за коллизий увеличить временную сложность до O(n). Напротив, бор использует меньше пространства для хранения множества слов с одинаковым префиксом, а его временная сложность составляет всего O(m), где m — длина слова. Временная сложность поиска слова в сбалансированном дереве равна O(mlog(n)). Структура бора показана на рисунке ниже. Для хранения слов достаточно обрабатывать 26 букв, а слова с одинаковым префиксом разделяют этот префикс, что экономит память. Например, «apple» и «appeal» имеют общий префикс «app», а «boom» и «box» — общий префикс «bo».

root a b p u m o y p o x t d e m l e a l

Чтобы реализовать бор, сначала нужно абстрагировать узел — аналогично узлу на рисунке выше. Узел хранит ссылки на свои дочерние узлы и состояние текущего узла. Состояние указывает, является ли этот узел концом слова («end»), что позволяет определить при поиске, заканчивается ли на нём слово. Кроме того, корневой узел является входом в бор и используется для представления всего бора.

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

Ниже приведены результаты выполнения.

```text
word 'apple' in Trie: true
word 'apples' in Trie: false
prefix 'ins' in Trie: true
prefix 'ina' in Trie: false
Some(Node { end: true, children: [None, ..., None] })
```
