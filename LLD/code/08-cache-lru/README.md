# 🗄️ Problem 08: LRU Cache

> **Frequency:** 🟡 P1 | **Time:** 90 min | **Difficulty:** ⭐⭐⭐

---

## 📋 Requirements

### Must-Have (Core)
1. Fixed **capacity** cache
2. **get(key)** — return value if exists, mark as recently used
3. **put(key, value)** — add/update entry, evict LRU if at capacity
4. Both operations in **O(1)** time complexity
5. **Eviction policy**: Least Recently Used item removed first

### Nice-to-Have
- TTL (Time-To-Live) per entry
- Thread-safe implementation
- Multiple eviction policies (LFU, FIFO)
- Cache statistics (hits, misses, evictions)

---

## 🧩 Key Entities

```
Cache, CacheNode, DoublyLinkedList, EvictionPolicy
```

## 🏗️ Implementation Design

```
Data Structures:
┌────────────────────────────────────────────────┐
│  HashMap<Key, Node>  →  O(1) lookup            │
│  DoublyLinkedList    →  O(1) insert/remove      │
│                                                │
│  HashMap:     key1 → Node1                     │
│               key2 → Node2                     │
│               key3 → Node3                     │
│                                                │
│  DLL:  HEAD ↔ Node3 ↔ Node1 ↔ Node2 ↔ TAIL    │
│        (most recent)          (least recent)   │
│                                                │
│  On get(key1):  Move Node1 to HEAD             │
│  On put(new):   Add to HEAD, if full → remove  │
│                 node before TAIL                │
└────────────────────────────────────────────────┘
```

## 🎯 Patterns Used

| Pattern | Where | Why |
|---|---|---|
| **Strategy** | EvictionPolicy (LRU, LFU, FIFO) | Swap eviction algorithms |
| **Singleton** | CacheManager | Single cache instance |
| **Observer** | Cache events (eviction, hit, miss) | Statistics tracking |

## 🔑 Key Design Decisions
- **HashMap + Doubly Linked List** — Classic O(1) solution
- **Sentinel nodes** — Use dummy HEAD and TAIL for cleaner insert/remove
- **Thread safety** — Use `ReentrantReadWriteLock` for concurrent access
- **Generic types** — `Cache<K, V>` to support any key-value type

## 📁 Code Structure
```
src/
├── model/
│   └── CacheNode.java
├── datastructure/
│   └── DoublyLinkedList.java
├── policy/
│   ├── EvictionPolicy.java
│   └── LRUEvictionPolicy.java
├── Cache.java
└── CacheDemo.java
```
