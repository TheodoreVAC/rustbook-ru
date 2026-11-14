## 4.5 Дек

Дек — это тоже линейная структура данных с двумя концами: передним и задним. В отличие от очереди, дек позволяет добавлять и удалять элементы с обоих концов. Такая гибкость делает его гибридной линейной структурой, способной работать и как стек, и как очередь. Хотя дек имеет сходство и со стеком, и с очередью, он не навязывает ни порядка LIFO, ни порядка FIFO. Порядок добавления и удаления данных определяет, будет ли дек вести себя как стек или как очередь. Важно отметить, что дек не следует использовать вместо стека или очереди, поскольку у каждой структуры данных есть свои уникальные свойства и она проектировалась для определённых вычислительных задач. Пример дека приведён на рисунке ниже.

![Рисунок 4.14: Дек](images/fig-4.14.png)

*Рисунок 4.14: Дек*

### 4.5.1 Абстрактный тип данных «дек»

Структура данных «дек» представляет собой упорядоченную коллекцию элементов, допускающую добавление и удаление элементов с любого из концов. Она определяется следующими операциями:

- new() создаёт новый дек без аргументов и возвращает пустой дек.
- add_front(item) добавляет элемент item на передний конец дека, требуя item в качестве параметра и не возвращая никакого значения.
- add_rear(item) добавляет элемент item на задний конец дека, требуя item в качестве параметра и не возвращая никакого значения.
- remove_front() удаляет передний элемент из дека, не принимая аргументов, возвращает удалённый элемент и при этом изменяет дек.
- remove_rear() удаляет задний элемент из дека, не принимая аргументов, возвращает удалённый элемент и при этом изменяет дек.
- is_empty() проверяет, пуст ли дек, не принимая аргументов и возвращая логическое значение.
- size() возвращает число элементов в деке, не принимая аргументов и возвращая целое число типа `usize`.
- iter() возвращает неизменяемую форму итерации по деку; дек при этом остаётся неизменным, аргументы не требуются.
- iter_mut() возвращает изменяемую форму итерации по деку; дек при этом изменяем, аргументы не требуются.
- into_iter() превращает дек в итерируемую форму; дек при этом потребляется, аргументы не требуются.

Предположим, что `d` — это уже созданный пустой дек; в таблице ниже показаны результаты серии операций. Обратите внимание, что передний конец находится с правой стороны. При добавлении и извлечении элементов важно отслеживать содержимое переднего и заднего концов, поскольку изменение обоих концов может сделать результат несколько запутанным.

**Таблица 4.5: Операции над деком**

| операции | значение | возвращаемое значение |
| --- | --- | --- |
| d.is_empty() | [] | true |
| d.add_rear(1) | [1] | |
| d.add_rear(2) | [2,1] | |
| d.add_front(3) | [2,1,3] | |
| d.add_front(4) | [2,1,3,4] | |
| d.remove_rear() | [1,3,4] | 2 |
| d.remove_front() | [1,3] | 4 |
| d.size() | [1,3] | 2 |
| d.is_empty() | [1,3] | false |
| d.add_front(2) | [1,3,2] | |
| d.add_rear(4) | [4,1,3,2] | |
| d.size() | [4,1,3,2] | 4 |
| d.is_empty() | [4,1,3,2] | false |
| d.add_rear(5) | [5,4,1,3,2] | |
| d.add_front(10) | [5,4,1,3,2,10] | |

### 4.5.2 Реализация дека на Rust

Чтобы реализовать абстрактный тип данных «дек» на Rust, можно использовать `Vec` в качестве базовой структуры данных. Левый конец `Vec` служит задним концом дека, а правый — передним. Чтобы дек не рос бесконечно, добавлен параметр ёмкости, управляющий максимальной длиной дека.

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

Ниже приведён пример вывода программы.

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

Как видно из приведённого вывода, дек имеет сходство и с очередью, и со стеком, и его можно рассматривать как их сочетание. Конкретная реализация дека может различаться в зависимости от ситуации, а то, какой конец считается передним и какой — задним, следует определять исходя из контекста.

### 4.5.3 Проверка палиндрома

Палиндромы — это строки, в которых символы на одинаковых позициях от обоих концов совпадают, например «radar», «sos» и «rustsur». В этом разделе мы рассмотрим алгоритм, позволяющий проверить, является ли заданная строка палиндромом. Один из подходов заключается в том, чтобы с помощью очереди поместить символы строки в очередь, а затем извлекать их оттуда и сравнивать с перевёрнутой исходной строкой. Этот метод прост, но требует много памяти. Более эффективный подход — использовать дек.

![Рисунок 4.15: Проверка палиндрома](images/fig-4.15.png)

*Рисунок 4.15: Проверка палиндрома*

Чтобы проверять палиндромы с помощью дека, мы сначала обрабатываем входную строку слева направо, добавляя каждый её символ на задний конец дека. На этом этапе передний конец дека содержит первый символ строки, а задний — последний. Затем мы можем воспользоваться особенностью дека извлекать элементы с обоих концов, чтобы сравнивать символы, находящиеся на переднем и заднем концах. Если они совпадают, мы продолжаем извлекать символы с переднего и заднего концов, пока либо все символы не будут использованы и дек не опустеет, либо не останется дек размером 1. В обоих случаях строка является палиндромом. Любая другая ситуация означает, что строка не является палиндромом. Ниже приведён код реализации определения палиндрома с помощью дека.

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
