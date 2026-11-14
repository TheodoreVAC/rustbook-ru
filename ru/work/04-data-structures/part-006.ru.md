## 4.6 Связный список

Упорядоченная коллекция элементов данных важна для сохранения относительного положения данных и для обеспечения эффективного индексирования. И массивы, и связные списки позволяют собирать данные в упорядоченном виде и хранить их в относительных позициях, что делает их подходящими для реализации упорядоченных типов данных. Например, стандартная реализация Vec в Rust использует массив. В этом разделе рассматриваются связные списки, которые обладают рядом уникальных преимуществ. В отличие от массивов, связные списки не требуют размещения элементов в непрерывной памяти. Каждый элемент коллекции содержит ссылку на следующий элемент, поэтому элементы могут располагаться произвольно, без необходимости выделять целый блок памяти, что повышает эффективность работы. Для работы со связным списком необходимо явно указать положение первого элемента. Зная положение первого элемента, мы можем определить положение второго и так далее до самого конца связного списка.

![Рисунок 4.16: Связный список](images/fig-4.16.png)

*Рисунок 4.16: Связный список*

Обычно связный список предоставляет ссылку на голову списка, а последний элемент должен быть установлен в null или в пустой следующий элемент, который также называется хвостом списка. При такой организации связный список можно легко обходить от головы к хвосту или в обратном направлении, переходя по ссылкам между элементами. Благодаря этому связные списки являются эффективной структурой данных для реализации других упорядоченных типов данных.

### 4.6.1 Абстрактный тип данных «связный список»

Абстрактный тип данных связного списка состоит из его структуры и набора операций. Как отмечалось выше, связный список представляет собой упорядоченную коллекцию узлов, причём весь список можно обойти, начиная с головного узла. Структура связного списка довольно проста: каждый узел содержит один элемент и ссылку на следующий узел. Для связного списка определены следующие операции:

- new(): создаёт новый головной узел, указывающий на Node, не принимает аргументов и возвращает указатель.
- push(item): добавляет новый Node, принимает параметр item и возвращает None.
- pop(): удаляет головной узел связного списка, не принимает аргументов и возвращает этот узел типа Node.
- peek(): возвращает ссылку на головной узел связного списка, не принимает аргументов.
- peek_mut(): возвращает головной узел связного списка, не принимает аргументов и возвращает изменяемую ссылку на этот узел.
- is_empty(): возвращает логическое значение, указывающее, пуст ли текущий связный список, и не принимает аргументов.
- size(): возвращает длину связного списка в виде целого числа типа usize, не принимает аргументов.
- iter(): возвращает неизменяемую итерацию по связному списку, не изменяя при этом сам связный список, и не принимает аргументов.
- iter_mut(): возвращает изменяемую итерацию по связному списку, причём сам список должен быть изменяемым, и не принимает аргументов.
- into_iter(): потребляет связный список и возвращает его в итерируемой форме, не принимая аргументов.

Предположим, что l — пустой связный список; в таблице ниже показан результат последовательности операций над связным списком, где Link<num> обозначает адрес, указывающий на узел, содержащий num, а левый конец списка является головным узлом.

**Таблица 4.6: Операции над связным списком**

| Операция | Значение | Возвращаемое значение |
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

### 4.6.2 Реализация связного списка на Rust

Для представления элемента связного списка мы используем абстракцию узла, которая включает сам элемент данных и адрес следующего элемента. Узел также предоставляет методы для доступа к элементу данных и его изменения. Как показано на рисунке ниже, Node состоит из данных и адреса следующего узла.

![Рисунок 4.17: Узел](images/fig-4.17.png)

*Рисунок 4.17: Узел*

В Rust значение None используется для обозначения отсутствия следующего узла как в Node, так и в самом связном списке. Функция new инициализирует узел, устанавливая его поле next в None. Явное присваивание None полю next — хорошая практика, помогающая избежать висячих указателей, распространённой проблемы в таких языках, как C/C++.

![Рисунок 4.18: Связный список](images/fig-4.18.png)

*Рисунок 4.18: Связный список*

Приведённый ниже код показывает реализацию связного списка; для читаемости кода ссылка на узел определена с помощью псевдонима Link.

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

### 4.6.3 Стек на основе связного списка

Для реализации стека также можно использовать связный список — ещё одну разновидность линейных структур данных. В этом случае для хранения вершины стека можно использовать голову связного списка. По мере добавления новых элементов в стек они вставляются в начало связного списка. Реализация такого подхода приведена ниже. Обратите внимание, что, поскольку функции push и pop изменяют узлы связного списка, для извлечения значения узла используется функция take, которая забирает содержимое узла, оставляя на его месте пустое значение.

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

Вывод программы будет зависеть от того, как именно используется стек и какие функции вызываются.

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
