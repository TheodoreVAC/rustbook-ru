## 4.7 Vec

В этой главе мы продемонстрировали, каким образом базовый тип данных Vec может использоваться для реализации различных абстрактных типов данных, включая стек, очередь, дек и связные списки. Vec — мощный, но вместе с тем простой контейнер данных, предоставляющий механизмы сбора данных и выполнения разнообразных операций, поэтому мы постоянно используем его как базовую структуру данных при реализации других типов данных. Он похож на List из Python и очень удобен в применении. Однако далеко не во всех языках программирования есть Vec, да и не всякий тип данных подходит для него. В некоторых случаях Vec или аналогичные контейнеры данных программистам приходится реализовывать самостоятельно.

### 4.7.1 Абстрактный тип данных Vec

Vec представляет собой коллекцию элементов, сохраняющих взаимное относительное положение. Ниже перечислены различные операции абстрактного типа данных Vec:

- new(): создаёт новый пустой Vec, аргументов не принимает.
- push(item): добавляет элемент в конец Vec, принимает параметр item.
- pop(): удаляет последний элемент Vec и возвращает его, аргументов не принимает.
- insert(pos, item): вставляет элемент в позицию pos вектора Vec, принимает параметры pos и item.
- remove(idx): удаляет элемент с индексом idx из Vec и возвращает его, принимает один параметр.
- find(item): проверяет, присутствует ли элемент в Vec, и возвращает логическое значение, принимает параметр item.
- is_empty(): проверяет, пуст ли Vec, и возвращает логическое значение, аргументов не принимает.
- size(): вычисляет количество элементов в Vec и возвращает целое число типа usize, аргументов не принимает.
- iter(): возвращает неизменяемую итерацию по Vec.
- iter_mut(): возвращает изменяемую итерацию по Vec, аргументов не принимает.
- into_iter(): поглощает Vec и возвращает итерируемую форму Vec, аргументов не принимает.

Предположим, что v — это созданный пустой Vec. В таблице ниже показан вид Vec после выполнения различных операций, причём левая сторона соответствует голове списка.

**Таблица 4.7: Операции над Vec**

| операция | значение | результат |
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

Наконец, стоит отметить, что, хотя Vec является мощной структурой данных, для конкретного варианта использования она не всегда окажется лучшим выбором. Программистам следует тщательно учитывать требования своего проекта и соответственно выбирать подходящую структуру данных.

### 4.7.2 Реализация Vec на Rust

Vec состоит из узлов связного списка, каждый из которых содержит элемент данных и явную ссылку на следующий узел. Зная местоположение первого узла, к последующим элементам можно получить доступ, переходя по ссылке next.

Поскольку ссылки играют ключевую роль в Vec, необходимо поддерживать ссылку на первый узел. Связный список создаётся со значением None, означающим, что список не ссылается ни на какое содержимое, как показано на рисунке (4.19). Голова связного списка ссылается на первый узел списка, в котором хранится адрес следующего узла. Важно отметить, что сам Vec не содержит объектов-узлов, а хранит лишь ссылку на первый узел структуры связного списка.

![Рисунок 4.19: Vec на основе связного списка](images/fig-4.19.png)

*Рисунок 4.19: Vec на основе связного списка*

Чтобы добавить новый элемент в связный список, единственная точка входа — это голова списка. Поскольку все остальные узлы доступны только переходом по ссылке next от первого узла, наиболее эффективный способ добавить новый узел — вставить его в голову связного списка. При таком подходе новый элемент становится первым элементом, а уже существовавшие элементы связываются с ним. Хотя приведённая здесь реализация Vec не является упорядоченной, упорядоченный Vec можно реализовать, используя функцию сравнения данных, задающую полный или частичный порядок. Приведённый ниже LVec обеспечивает лишь часть возможностей Vec из стандартной библиотеки, а функция print_lvec используется для вывода его элементов данных.

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

Вот результат выполнения.

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

Важно отметить, что LVec представляет собой связный список из n узлов, и любой метод, требующий обхода узлов, например insert, push, pop, remove и тому подобные, имеет временную сложность O(n). Хотя в среднем случае может потребоваться обход лишь половины узлов, в худшем случае придётся обработать каждый узел списка.
