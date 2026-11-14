## 10.6 Согласованное хеширование

Алгоритм согласованного хеширования был изначально предложен Кэнгером и др. из MIT для решения проблем с горячими точками в распределённом кэшировании. Однако после нескольких лет разработки он стал широко применяемым алгоритмом. Чтобы понять его применение, рассмотрим кэширование изображений в Redis. Один экземпляр Redis может справляться с малыми объёмами данных и низкими скоростями доступа, и для таких объёмов может быть достаточно конфигурации «мастер-реплика».

Однако когда объёмы данных растут, а скорости доступа увеличиваются, необходимо создать кластер, чтобы распределить данные между несколькими машинами. Например, если существует пять машин, позиция индекса изображения была бы равна index = hash(key) % 5, где key — это индекс, связанный с изображением. Однако добавление или удаление машин изменяет N, и ранее вычисленные индексы становятся недействительными. Именно здесь применяется согласованное хеширование. Оно создаёт круг, диапазон которого составляет 0 до 232 −1, сопоставляя данные с позицией на этом круге.

232 −1 0 Node3 Node1 Node2

Для достижения кэширования данные должны быть добавлены в определённый сегмент круга на основе их хеш-значения. Соответствующий узел, находящийся чуть выше по часовой стрелке от сегмента, будет хранить данные.

232 −1 0 Node3 Node1 Node2

Предположим, что Node3 отказывает, и данные между Node2 и Node3 передаются Node1.

232 −1 0 Node1 Node2

Когда новый узел Node4 добавляется, данные, изначально хранившиеся на Node3, теперь будут храниться на Node4.

232 −1 0 Node3 Node1 Node4 Node2

Алгоритм согласованного хеширования устойчив к сбоям и способен масштабироваться, поскольку при добавлении или удалении узлов перемещается лишь небольшая часть данных. Эта возможность позволяет алгоритму достигать согласованности. Для реализации согласованного хеширования требуется создать Ring, который будет хранить узлы, представляющие машины.

```rust
// conshash.rs

use std::fmt::Debug;
use std::string::ToString;
use std::hash::{Hash, Hasher};
use std::collections::{BTreeMap, hash_map::DefaultHasher};

// Ring node definition, used for storing the host, ip and port
#[derive(Clone, Debug)]
struct Node {
    host: &'static str,
    ip: &'static str,
    port: u16,
}

// implement a to_string function
impl ToString for Node {
    fn to_string(&self) -> String {
        self.ip.to_string() + &self.port.to_string()
    }
}

// Definition for the Ring
struct Ring<T: Clone + ToString + Debug> {
    replicas: usize, // partition number
    ring: BTreeMap<u64, T>, // store data
}
```

В Ring используются реплики, чтобы избежать кластеризации узлов и обеспечить равномерное распределение данных между узлами. Для решения проблемы кластеризации узлов можно создать несколько виртуальных узлов для каждого узла. Вычислитель хеша, предоставляемый стандартной библиотекой, со значением по умолчанию, равным десяти узлам, можно использовать для вычисления хеша, либо можно создать собственные узлы. Для алгоритма согласованного хеширования должны быть реализованы как минимум функции вставки узла, удаления узла и запросов. Кроме того, для пакетной обработки можно реализовать пакетные версии функций вставки и удаления.

```rust
// conshash.rs

const DEFAULT_REPLICAS: usize = 10;

// Hash calculation function
fn hash<T: Hash>(val: &T) -> u64 {
    let mut hasher = DefaultHasher::new();
    val.hash(&mut hasher);

    hasher.finish()
}

impl<T> Ring<T> where T: Clone + ToString + Debug {
    fn new() -> Self {
        Self::with_capacity(DEFAULT_REPLICAS)
    }

    // new with a replicas parameter
    fn with_capacity(replicas: usize) -> Self {
        Ring {
            replicas: replicas,
            ring: BTreeMap::new()
        }
    }

    // Batch insertion of nodes
    fn add_multi(&mut self, nodes: &[T]) {
        if !nodes.is_empty() {
            for node in nodes.iter() {
                self.add(node);
            }
        }
    }

    fn add(&mut self, node: &T) {
        for i in 0..self.replicas {
            let key = hash(&(node.to_string()
                                + &i.to_string()));
            self.ring.insert(key, node.clone());
        }
    }

    // Batch deletion of nodes
    fn remove_multi(&mut self, nodes: &[T]) {
        if !nodes.is_empty() {
            for node in nodes.iter() {
                self.remove(node);
            }
        }
    }
```

```rust
    fn remove(&mut self, node: &T) {
        // assertion to ensure that the node exists
        assert!(!self.ring.is_empty());

        for i in 0..self.replicas {
            let key = hash(&(node.to_string()
                                + &i.to_string()));
            self.ring.remove(&key);
        }
    }

    // Get nodes
    fn get(&self, key: u64) -> Option<&T> {
        if self.ring.is_empty() {
            return None;
        }

        let mut keys = self.ring.keys();
        keys.find(|&k| k >= &key)
            .and_then(|k| self.ring.get(k))
            .or(keys.nth(0).and_then(|x| self.ring.get(x)))
    }
}

fn main() {
    let replica = 3;
    let mut ring = Ring::with_capacity(replica);
    let node = Node{
        host:"localhost",
        ip:"127.0.0.1",
        port:23
    };
    ring.add(&node);

    for i in 0..replica {
        let key = hash(&(node.to_string() + &i.to_string()));
        let res = ring.get(key);
        assert_eq!(node.host, res.unwrap().host);
    }

    println!("{:?}", &node);
    ring.remove(&node);
    // Node { host: "localhost", ip: "127.0.0.1", port: 23 }
}
```
