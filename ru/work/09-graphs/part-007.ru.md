## 9.7 Depth First Search(DFS)

Задача о маршруте коня — это частный случай алгоритма поиска в глубину, который направлен на создание максимально глубокого дерева. Поиск в глубину обычно используется для обхода графов с множеством ветвей: его цель — проникать как можно глубже, связывать как можно больше узлов и ветвиться при необходимости. В некоторых случаях поиск в глубину может создавать несколько деревьев, которые называются лесом поиска в глубину. Как и поиск в ширину, поиск в глубину использует ссылки на предшественников для построения деревьев. Чтобы лучше понять поиск в глубину, класс вершины можно расширить двумя переменными, указывающими время начала и окончания поиска узла: время начала также указывает количество шагов до встречи с вершиной, а время окончания — количество шагов до того, как вершина окрашивается в чёрный цвет. На следующем рисунке показан небольшой граф и применённый к нему алгоритм поиска в глубину. Толстые линии обозначают проверенные рёбра, причём узел на другом конце ребра уже добавлен в дерево поиска в глубину. Поиск начинается с вершины A, и поскольку в начале поиска все вершины окрашены, алгоритм случайным образом начинает обход с вершины A. При посещении вершины первым шагом её цвет устанавливается в серый, что указывает на то, что вершина исследуется, а время обнаружения — в 1. Поскольку у вершины A две смежные вершины (B и D), каждую вершину необходимо посетить, причём смежные вершины посещаются в алфавитном порядке.

A1/ B C D E F

Далее мы посещаем вершину B, которая смежна с вершинами C и D. Вершина C приводит нас к концу ветви, поэтому её можно окрасить в чёрный цвет и установить время окончания равным 4. Теперь возвращаемся к вершине B и продолжаем исследовать D, которая приводит нас к вершине E. У вершины E две смежные вершины — B и F. Поскольку B уже окрашена в чёрный цвет, её можно пропустить и посетить вершину F.

C3/ A1/ B2/ A1/ B2/ C D E F D E F C C A1/ B2/ A1/ B2/ 3/4 3/4 D5/ D5/ E6/ F7/ E F

У вершины F есть только одна смежная вершина — C, уже окрашенная в чёрный цвет, поэтому алгоритм достиг конца ветви. Следовательно, алгоритм должен выполнять обратный поиск с откатами (бэктрекинг) и продолжать поиск до тех пор, пока не встретит серую вершину или не завершится.

C C3/ A1/ B2/ A1/ B2/ 3/4 D5/ E6/ F D5/ E F D E F 7/8 6/9 7/8 C C A1/ B2/ A1/ B 3/4 2/11 3/4 D E F D E F 5/10 6/9 7/8 5/10 6/9 7/8

В итоге алгоритм возвращается к исходной вершине и завершает поиск, получая пройденный путь: A → B → D → E → F.

C A B 1/12 2/11 3/4 D E F 5/10 6/9 7/8

### 9.7.1 Implementing a DFS

Основываясь на предыдущем обсуждении и иллюстрации, можно представить базовую реализацию алгоритма поиска в глубину, которая не включает цветовые пометки, но реализует основной функционал исследования.

```rust
// dfs.rs
use std::rc::Rc;
use std::cell::RefCell;

// Node link
type Link = Option<Rc<RefCell<Node>>>;

struct Node {
    data: usize,
    next: Link,
}

impl Node {
    fn new(data: usize) -> Self {
        Self {
            data: data,
            next: None
        }
    }
}

// Definition of Graph
struct Graph {
    first: Link,
    last: Link,
}

impl Graph {
    fn new() -> Self {
        Self { first: None, last: None }
    }

    fn is_empty(&self) -> bool {
        self.first.is_none()
    }

    fn get_first(&self) -> Link {
        self.first.clone()
    }

    fn print_node(&self) {
        let mut curr = self.first.clone();
        while let Some(val) = curr {
            print!("[{}]", &val.borrow().data);
            curr = val.borrow().next.clone();
        }
        print!("\n");
```

```rust
    }

    // insert data
    fn insert(&mut self, data: usize) {
        let node = Rc::new(RefCell::new(Node::new(data)));
        if self.is_empty() {
            self.first = Some(node.clone());
            self.last = Some(node);
        } else {
            self.last.as_mut()
                     .unwrap()
                     .borrow_mut()
                     .next = Some(node.clone());
            self.last = Some(node);
        }
    }
}

// build a graph
fn build_graph(data: [[usize;2];20]) -> Vec<(Graph, usize)> {
    let mut graphsVec<(Graph, usize)> = Vec::new();
    for _ in 0..9 {
      graphs.push((Graph::new(), 0));
    }

    for i in 1..9 {
        for j in 0..data.len() {
            if data[j][0] == i {
              graphs[i].0.insert(data[j][1]);
            }
        }

        print!("[{i}]->");
        graphs[i].0.print_node();
    }

    graphs
}

fn dfs(graph: Vec<(Graph, usize)>) {
    let mut gp = graph;
    let mut nodes: Vec<usize> = Vec::new();
    let mut temp: Vec<usize> = Vec::new();

    gp[1].1 = 1;
    let mut curr = gp[1].0.get_first().clone();

    // print graph
    print!("{1}->");
    while let Some(val) = curr {
        nodes.insert(0,val.borrow().data);
        curr = val.borrow().next.clone();
```

```rust
    }

    // print dfs graph
    loop{
        if 0 == nodes.len() {
            break;
        }else{
            let data = nodes.pop().unwrap();
            if 0 == gp[data].1 { // Unvisited
                // Change state to visited
                gp[data].1 = 1;
                print!("{data}->");

                // Add node to temp and perform depth-first
                // search on it
                let mut curr = gp[data].0.get_first().clone();
                while let Some(val) = curr {
                    temp.push(val.borrow().data);
                    curr = val.borrow().next.clone();
                }

                while !temp.is_empty(){
                    nodes.push(temp.pop().unwrap());
                }
            }
        }
    }

    println!("");
}

fn main() {
    let data = [
      [1,2],[2,1],[1,3],[3,1],[2,4],[4,2],[2,5],
      [5,2],[3,6],[6,3],[3,7],[7,3],[4,5],[5,4],
      [6,7],[7,6],[5,8],[8,5],[6,8],[8,6]
    ];
    let gp = build_graph(data);
    dfs(gp);
}
```

Ниже приведён вывод, отображающий смежные узлы каждой вершины и самый глубокий путь.

```rust
[1]->[2][3]
[2]->[1][4][5]
[3]->[1][6][7]
[4]->[2][5]
[5]->[2][4][8]
[6]->[3][7][8]
[7]->[3][6]
[8]->[5][6]
1->2->4->5->8->6->3->7->
```

### 9.7.2 Analysis of DFS

Временная сложность поиска в глубину (DFS) может быть вычислена как с точки зрения вершин, так и с точки зрения рёбер. В `build_graph` каждая вершина должна быть обработана один раз для построения графа, что даёт сложность O(V). Во время поиска DFS начинается с некоторой вершины и исследует все смежные вершины как можно глубже, обрабатывая каждое ребро с временной сложностью O(E). Следовательно, общая временная сложность DFS равна O(V + E). Если во время DFS все вершины образуют цепочку, то самый глубокий поиск будет включать все узлы, что даёт пространственную сложность O(V). Важно отметить, что деревья являются частным случаем графов. Поэтому алгоритмы поиска в глубину и поиска в ширину для графов могут также использоваться для поиска в деревьях. Поиск в ширину, который был рассмотрен в главе о деревьях, на самом деле представляет собой обход по уровням. DFS и BFS являются основой для многих других важных алгоритмов обработки графов, что делает их необходимыми для поиска в графах. В следующих разделах будут использоваться BFS и DFS графа для решения практических задач, чтобы углубить понимание.

### 9.7.3 Topological Sorting

Задачи реального мира часто могут быть смоделированы в виде графов и решены с помощью алгоритмов обработки графов. Например, рассмотрим задачу составления четырёхлетнего учебного плана для специальности, которая включает обеспечение правильных зависимостей между курсами и допустимой последовательности курсов. Эта задача может быть сложной, но с использованием структуры данных «граф» её можно решить с помощью алгоритмов обработки графов. Предположим, у нас есть четыре курса с зависимостями, показанными на графе; допустимый порядок изучения курсов — [functions, derivatives, systems of equations, calculus, linear algebra, probability theory, convolutional neural networks]. Чтобы определить порядок курсов, можно использовать алгоритм сортировки зависимостей между курсами, который известен как топологическая сортировка.

![Figure 9.5: Courses Topological Relationship](images/fig-9.5.png)

*Figure 9.5: Courses Topological Relationship*

Топологическая сортировка — это вариант поиска в глубину, который создаёт линейное упорядочение всех вершин ориентированного ациклического графа (DAG). Полученный порядок может использоваться для указания приоритетов событий, составления расписаний проектов, генерации графов приоритетов для запросов к базе данных и так далее. Основные идеи топологической сортировки заключаются в следующем:

- Вызвать `dfs()` для графа g с использованием поиска в глубину, чтобы найти подходящие вершины.
- Сохранить вершины в стеке так, чтобы последняя из них оказалась на дне.
- Вернуть данные из стека как результат топологической сортировки.

Следуя этим шагам, можно преобразовать граф в линейное отношение, например упомянутый выше учебный план, который может быть преобразован в топологическую последовательность.

![Figure 9.6: Course sheduling](images/fig-9.6.png)

*Figure 9.6: Course sheduling*

Итоговый результат топологической сортировки представлен ниже. Курсы одного цвета можно проходить в любом порядке, а курсы разных цветов — только в порядке, заданном топологической сортировкой.

![Figure 9.7: Topological sequence of course sheduling](images/fig-9.7.png)

*Figure 9.7: Topological sequence of course sheduling*

Для реализации алгоритма обработки графа для составления расписания курсов сначала определим перечисление цветов, представляющее состояние исследования узла.

```rust
// course_topological_sort.rs
use std::collections::HashMap;
use std::hash::Hash;
use std::fmt::Display;

// Color enum used to determine if a node has been searched
#[derive(Debug, Clone, PartialEq)]
enum Color {
    White, // White: not yet explored
    Gray, // Gray: currently being explored
    Black, // Black: exploration complete
}
```

Затем определяются узел и граф, как это уже не раз делалось ранее.

```rust
// course_topological_sort.rs

// course vertex definition
#[derive(Debug, Clone)]
struct Vertex<T> {
    key: T,
    color: Color,
    neighbors: Vec<T>,
}
```

```rust
impl<T: PartialEq + Clone> Vertex<T> {
    fn new(key: T) -> Self {
        Self {
            key: key,
            color: Color::White,
            neighbors: Vec::new(),
        }
    }

    fn add_neighbor(&mut self, nbr: T) {
        self.neighbors.push(nbr);
    }
}

// couses relation graph definition
#[derive(Debug, Clone)]
struct Graph<T> {
    vertnums: u32,
    edgenums: u32,
    vertices: HashMap<T, Vertex<T>>, // all vertex
    edges: HashMap<T, Vec<T>>, // all edges
}

impl<T: Eq + PartialEq + Clone + Hash> Graph<T> {
    fn new() -> Self {
        Self {
            vertnums: 0,
            edgenums: 0,
            vertices: HashMap::<T, Vertex<T>>::new(),
            edges: HashMap::<T, Vec<T>>::new(),
        }
    }

    fn add_vertex(&mut self, key: &T) -> Option<Vertex<T>> {
        let vertex = Vertex::new(key.clone());
        self.vertnums += 1;
        self.vertices.insert(key.clone(), vertex)
    }

    fn add_edge(&mut self, src: &T, des: &T) {
        if !self.vertices.contains_key(src) {
          let _sv = self.add_vertex(src);
        }

        if !self.vertices.contains_key(des) {
          let _dv = self.add_vertex(des);
        }

        // add vertex
        self.edgenums += 1;
        self.vertices.get_mut(src)
                     .unwrap()
```

```rust
                     .add_neighbor(des.clone());

        // add edge
        if !self.edges.contains_key(src) {
            let _eg = self.edges
                          .insert(src.clone(), Vec::new());
        }

        self.edges.get_mut(src).unwrap().push(des.clone());
    }
}
```

Когда граф построен, можно приступать к созданию графа зависимостей курсов. При исследовании всех узлов-курсов в графе используется атрибут цвета, чтобы указать, был ли узел посещён. Переменная schedule хранит результат топологической сортировки курсов. Чтобы предотвратить ошибки планирования, такие как циклические зависимости, здесь добавлена переменная "has_circle" для управления процессом поиска. При обнаружении цикла программа завершается, указывая на то, что входные данные некорректны.

```rust
// course_topological_sort.rs

// Build the course dependency graph.
fn build_course_graph<T>(pre_requisites:Vec<Vec<T>>)->Graph<T>
    where T: Eq + PartialEq + Clone + Hash
{
    // Create edge relationships for dependent courses.
    let mut course_graph = Graph::new();
    for v in pre_requisites.iter() {
        let prev = v.first().unwrap();
        let last = v.last().unwrap();
        course_graph.add_edge(prev, last);
    }

    course_graph
}

// Course scheduling.
fn course_scheduling<T>(
    cg: &mut Graph<T>,
    course: Vertex<T>,
    schedule: &mut Vec<String>,
    mut has_circle: bool)
where T: Eq + PartialEq + Clone + Hash + Display
{
    // Clone to prevent conflicts with mutable references.
    let edges = cg.edges.clone();

    // Explore dependent courses.
    let dependencies = edges.get(&course.key);

    if !dependencies.is_none() {
        for dep in dependencies.unwrap().iter() {
            let course = cg.vertices.get(dep)
                                    .unwrap().clone();
```

```rust
            if Color::White == course.color {
                cg.vertices.get_mut(dep)
                           .unwrap()
                           .color = Color::Gray;

                course_scheduling(cg, course,
                                  schedule, has_circle);

                // Exit when encountering a cycle.
                if has_circle {
                    return;
                }
            } else if Color::Gray == course.color {
                has_circle = true;
                return;
            }
        }
    }

    // Change node color and add to schedule.
    cg.vertices.get_mut(&course.key)
               .unwrap()
               .color = Color::Black;
    schedule.push(course.key.to_string());
}

fn find_topological_order<T>(
    course_num: usize,
    pre_requisites: Vec<Vec<T>>)
where T: Eq + PartialEq + Clone + Hash + Display
{
    // Build the course dependency graph.
    let mut cg = build_course_graph(pre_requisites);

    // Get all course nodes into "courses".
    let vertices = cg.vertices.clone();
    let mut courses = Vec::new();
    for key in vertices.keys() {
        courses.push(key);
    }

    // Save feasible course schedules.
    let mut schedule = Vec::new();

    // Determine if there is a cycle.
    let has_circle = false;

    // Perform topological sorting of courses.
    for i in 0..course_num {
        let course = cg.vertices.get(&courses[i])
                                .unwrap()
                                .clone();
```

```rust
        // Only explore courses that are not explored
        // and do not have cycles.
        if !has_circle && Color::White == course.color {
            // Change the color of the course node to indicate
            // that it is currently being explored.
            cg.vertices.get_mut(&courses[i])
                       .unwrap()
                       .color = Color::Gray;

            course_scheduling(&mut cg, course,
                              &mut schedule, has_circle);
        }
    }

    if !has_circle {
        println!("{:#?}", schedule);
    }
}

fn main() {
    let course_num = 7;

    // Build course dependency relationships.
    let mut pre_requisites = Vec::<Vec<&str>>::new();
    pre_requisites.push(vec!["calculus", "function"]);
    pre_requisites.push(vec!["calculus", "derivation"]);
    pre_requisites.push(vec!["linear algebra", "equation"]);
    pre_requisites.push(vec!["CNN", "calculus"]);
    pre_requisites.push(vec!["CNN", "probalility thery"]);
    pre_requisites.push(vec!["CNN", "linear algebra"]);

    // Find the topological sorting result, which is a
    // reasonable course learning order.
    find_topological_order(course_num, pre_requisites);
}
```

Here is a feasible course learning order.

```text
[
    "function",
    "derivation",
    "calculus",
    "equation",
    "linear algebra",
    "probability theory",
    "CNN",
]
```

Помимо выбора курсов, приготовление пищи также можно абстрагировать как топологическую сортировку. Например, рассмотрим приготовление блинов, как показано на рисунке ниже. Рецепт прост: 1 яйцо, 1 чашка блинной смеси, 1 столовая ложка масла и 3/4 чашки молока. Чтобы приготовить блины, сначала необходимо включить плиту и разогреть сковороду. Затем ложкой смешать все ингредиенты и вылить смесь на сковороду. Когда

начинают образовываться пузырьки, перевернуть блин и обжарить его с обеих сторон до золотистой корочки. Перед едой можно добавить соус.

![Figure 9.8: Pancake Cooking](images/fig-9.8.png)

*Figure 9.8: Pancake Cooking*

С помощью алгоритма топологической сортировки приведённый выше рисунок можно упростить до стандартной схемы этапов приготовления. На этой схеме этапы одного цвета можно выполнять в любом порядке. Такая схема этапов может помочь начинающим кулинарам успешно приготовить блины. Однако сделать их вкусными — это уже совсем другое дело.

![Figure 9.9: Pancake cooking process topological relationship](images/fig-9.9.png)

*Figure 9.9: Pancake cooking process topological relationship*

И приготовление пищи, и выбор курсов могут быть абстрагированы как организация процессов, и поэтому теоретически один и тот же код может использоваться для работы с ними. Реализация алгоритма топологической сортировки процесса приготовления пищи совпадает с алгоритмом топологической сортировки для планирования курсов. Поэтому большая часть кода здесь приводиться не будет, но её можно найти в файлах исходного кода этой книги.

```rust
// cooking_topological_sort.rs

// Implementation omitted as it is identical to
// course_topological_sort
fn main() {
    let operation_num = 9;
```

```rust
    // constructe a cooking process dependency relationship
    let mut pre_requisites = Vec::<Vec<&str>>::new();
    pre_requisites.push(vec!["Mix", "3/4 cup of milk"]);
    pre_requisites.push(vec!["Mix", "1 egg"]);
    pre_requisites.push(vec!["Mix", "1 tablespoon olive oil"]);
    pre_requisites.push(vec!["Pour in 1/4 cup", "Mix"]);
    pre_requisites.push(vec!["Pour in 1/4 cup",
                             "Heat the pan"]);
    pre_requisites.push(vec!["Flip the bottom until golden",
                             "Pour in 1/4 cup"]);
    pre_requisites.push(vec!["Enjoy",
                             "Flip the bottom until golden"]);
    pre_requisites.push(vec!["Enjoy", "Heat the sauce"]);

    // Find a feasible topological result
    // which is a reasonable cooking order
    find_topological_order(operation_num, pre_requisites);
}
```

Here are two feasible cooking sequences.

```text
[
    "3/4 cup of milk",
    "1 egg",
    "1 tablespoon olive oil",
    "Mix",
    "Heat the pan",
    "Pour in 1/4 cup",
    "Flip the bottom until golden",
    "Heat the sauce",
    "Enjoy",
]
[
    "Heat the pan",
    "3/4 cup of milk",
    "1 egg",
    "1 tablespoon olive oil",
    "Mix",
    "Pour in 1/4 cup",
    "Flip the bottom until golden",
    "Heat the sauce",
    "Enjoy",
]
```


