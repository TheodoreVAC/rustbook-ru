## 10.5 Алгоритм LRU (наименее недавно использованный)

Алгоритм вытеснения из кеша, или алгоритм замещения страниц, — широко применяемый приём управления памятью в системе виртуальной памяти и при кэшировании данных. Его принцип основан на предположении, что если к данным недавно обращались, то скорее всего к ним будут обращаться и в будущем. Поэтому блоки данных, находящиеся в памяти, но не используемые, удаляются в зависимости от того, какие данные были использованы реже всего, освобождая место и экономя память. LRU (Least Recently Used) — популярный алгоритм вытеснения, применяемый для удаления данных по журналу обращений, когда объём хранилища ограничен. Предположим, что для кэширования пользовательской информации используется хеш-связный список с ёмкостью 5, а сейчас в кэше хранится информация о 4 пользователях, как показано на рисунке.

001 002 003 004 Info a Info b Info c Info d

Когда клиент запрашивает пользователя 5, данных нет в хеш-связном списке, поэтому их нужно прочитать из базы данных и вставить в кэш. В этот момент крайний правый узел связного списка представляет

недавно использованного пользователя 5, а крайний левый — пользователя 1, использованного реже всего.

001 002 003 004 005 Info a Info b Info c Info d Info e

Далее, когда другой клиент обращается к пользователю 2, данные обнаруживаются в хеш-связном списке, поэтому пользователь 2 просто извлекается со своего места и вставляется в крайний правый конец связного списка.

001 003 004 005 Info a Info c Info d Info e 002 Info b

После этих обращений хеш-связный список выглядит так, как показано на рисунке.

001 003 004 005 002 Info a Info c Info d Info e Info b

Позже клиент обращается к пользователю 6, но его данных нет в кэше, поэтому их тоже необходимо вставить.

001 003 004 005 002 006 Info a Info c Info d Info e Info b Info f

Однако поскольку кэш достиг предельного размера, сначала необходимо удалить данные, использованные реже всего, — пользователя 1. После этого пользователя 6 можно вставить в крайний правый конец хеш-связного списка.

003 004 005 002 006 Info c Info d Info e Info b Info f

Алгоритм LRU — распространённый алгоритм вытеснения из кеша, освобождающий память за счёт удаления наименее недавно использованных данных. Для реализации этого алгоритма необходимо определить структуру данных и операции, абстрагированные от графа. Сюда входят управление ключами, записями, а также указателями на начало и конец. Необходимые функции операций: insert, remove, contains и вспомогательные функции.

```rust
// lru.rs
use std::collections::HashMap;

// Definition for entry of LRU
struct Entry<K, V> {
    key: K,
    val: Option<V>,
```

```rust
    next: Option<usize>,
    prev: Option<usize>,
}

struct LRUCache<K, V> {
    cap: usize,
    head: Option<usize>,
    tail: Option<usize>,
    map: HashMap<K, usize>,
    entries: Vec<Entry<K, V>>,
}
```

Для хранения ключей используем HashMap, а для хранения записей — Vec. Указатели head и tail можно упростить до индексов в Vec. Чтобы настроить ёмкость кеша, реализуем функцию with_capacity, а new по умолчанию задаёт ёмкость, равную 100.

```rust
// lru.rs
use std::hash::Hash;

const CACHE_SIZE: usize = 100;

impl<K: Clone + Hash + Eq, V> LRUCache<K, V> {
    fn new() -> Self {
        Self::with_capacity(CACHE_SIZE)
    }

    fn len(&self) -> usize {
        self.map.len()
    }

    fn is_empty(&self) -> bool {
        self.map.is_empty()
    }

    fn is_full(&self) -> bool {
        self.map.len() == self.cap
    }

    fn with_capacity(cap: usize) -> Self {
        LRUCache {
            cap: cap,
            head: None,
            tail: None,
            map: HashMap::with_capacity(cap),
            entries: Vec::with_capacity(cap),
        }
    }
}
```

При вставке данных, если ключ уже существует, значение обновляется напрямую, а прежнее значение возвращается. Если вставляемого значения нет, возвращаемое значение должно быть None — отсюда использование Option в качестве типа возврата. Метод access используется для удаления прежнего значения и обновления, а ensure_room — для удаления наименее недавно использованных данных, когда кеш достигает предельной ёмкости.

```rust
// lru.rs

impl<K: Clone + Hash + Eq, V> LRUCache<K, V> {
    fn insert(&mut self, key: K, val: V) -> Option<V> {
        if self.map.contains_key(&key) {
            // Update if key exists
            self.access(&key);
            let entry = &mut self.entries[self.head.unwrap()];
            let old_val = entry.val.take();
            entry.val = Some(val);
            old_val
        } else {
            // insert if key not exists
            self.ensure_room();

            // Update the original head pointer
            let index = self.entries.len();
            self.head.map(|e| {
                self.entries[e].prev = Some(index);
            });

            // The new head node
            self.entries.push(Entry {
                key: key.clone(),
                val: Some(val),
                prev: None,
                next: self.head,
            });

            self.head = Some(index);
            self.tail = self.tail.or(self.head);
            self.map.insert(key, index);

            None
        }
    }

    fn get(&mut self, key: &K) -> Option<&V> {
        if self.contains(key) { self.access(key); }

        let entries = &self.entries;
        self.map.get(key).and_then(move |&i| {
            entries[i].val.as_ref()
        })
    }

    fn get_mut(&mut self, key: &K) -> Option<&mut V> {
        if self.contains(key) { self.access(key); }

        let entries = &mut self.entries;
        self.map.get(key).and_then(move |&i| {
```

```rust
            entries[i].val.as_mut()
        })
    }

    fn contains(&mut self, key: &K) -> bool {
        self.map.contains_key(key)
    }

    // Ensure there is enough capacity, remove the
    // least recently used item if full
    fn ensure_room(&mut self) {
        if self.cap == self.len() {
            self.remove_tail();
        }
    }

    fn remove_tail(&mut self) {
        if let Some(index) = self.tail {
            self.remove_from_list(index);
            let key = &self.entries[index].key;
            self.map.remove(key);
        }
        if self.tail.is_none() {
            self.head = None;
        }
    }

    // Get the value of a key, remove the
    // old position and add to the head
    fn access(&mut self, key: &K) {
        let i = *self.map.get(key).unwrap();
        self.remove_from_list(i);
        self.head = Some(i);
    }

    fn remove(&mut self, key: &K) -> Option<V> {
        self.map.remove(&key).map(|index| {
                self.remove_from_list(index);
                self.entries[index].val.take().unwrap()
            })
    }

    fn remove_from_list(&mut self, i: usize) {
        let (prev, next) = {
            let entry = self.entries.get_mut(i).unwrap();
            (entry.prev, entry.next)
        };

        match (prev, next) {
            // The data item is in the middle of the cache
            (Some(j), Some(k)) => {
                let head = &mut self.entries[j];
```

```rust
                head.next = next;
                let next = &mut self.entries[k];
                next.prev = prev;
            },
            // The data item is at the end of the cache
            (Some(j), None) => {
                let head = &mut self.entries[j];
                head.next = None;
                self.tail = prev;
            },
            // The data item is at the head of the cache
            _ => {
                if self.len() > 1 {
                    let head = &mut self.entries[0];
                    head.next = None;
                    let next = &mut self.entries[1];
                    next.prev = None;
                }
            },
        }
    }
}
```

Ниже приведён пример использования LRU.

```rust
// lru.rs

fn main() {
    let mut cache = LRUCache::with_capacity(2);
    cache.insert("foo", 1);
    cache.insert("bar", 2);
    cache.insert("baz", 3);
    cache.insert("tik", 4);
    cache.insert("tok", 5);

    assert!(!cache.contains(&"foo"));
    assert!(!cache.contains(&"bar"));
    assert!(cache.contains(&"baz"));
    assert!(cache.contains(&"tik"));

    cache.insert("qux", 6);
    assert!(cache.contains(&"qux"));
}
```
