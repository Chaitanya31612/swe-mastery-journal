# LRU Cache LLD Evaluation & Code Review

This document provides a senior engineer's review of the LRU Cache Low-Level Design (LLD) and its implementation, highlighting strong points, weak points, code bugs, concurrency flaws, and suggestions for improvement.

---

## 1. High-Level Design & Diagram Analysis

### Strengths
- **Decoupled Facade**: The separation of `Cache` (the public facade) and `CacheManager` (the internal orchestrator) is a good choice. It encapsulates the map and linked-list logic away from the public API.
- **Double-Linked List with Dummy Nodes**: Using dummy `head` and `tail` nodes simplifies boundary checks (adding/removing nodes) and avoids repetitive `null` pointer handling.

### Weaknesses & Inconsistencies
- **Naming Inconsistency**: In the `Cache` class diagram, the member field is named `manager: CacheNodeManager`, but the actual class is named `CacheManager`.
- **Encapsulation Violation**: The diagram lists node fields (`key`, `value`, `next`, `prev`) as private (`-`) and provides getters/setters. In the implementation, however, they are package-private and accessed directly.
- **Missing Interface/Contract**: The diagram shows `clearAll()`, which is missing from both the `Cache` and `CacheManager` code.

---

## 2. Compilation and Runtime Bugs

The current implementation will not compile or run due to several syntax and reference errors:

1. **Incomplete Statement**:
   - **Line 104**: `throw new IllegalStateException("Cache needs to be initialized first.")` is missing a semicolon.
2. **Missing Symbol (`cache` in `Cache` class)**:
   - **Line 116 & 120**: `Cache.isFull()` and `Cache.isEmpty()` reference `cache.size()` and `cache.isEmpty()`. However, `cache` (the Map) is defined in `CacheManager`, not in `Cache`.
3. **Invalid Method Signature Call**:
   - **Line 39**: `Cache.getInstance(5)` is called in `CacheDemo`. However, `getInstance()` accepts no arguments, and the private `initialize(int size)` is never called. This leads to a compilation error and would throw an `IllegalStateException` even if compiled.
4. **Missing Delegate Method**:
   - **Line 76**: `cache.exists("name")` is called, but the `Cache` class does not define or delegate the `exists` method.

---

## 3. Concurrency & Thread-Safety Critique

### The "Check-Then-Act" Race Condition
In `CacheManager.get()`, the code checks key existence before acquiring the write lock:
```java
public Object get(Object key) {
  if (!exists(key)) { // 1. Acquires and releases read lock
    return null;
  }
  lock.writeLock().lock(); // 2. Acquires write lock
  try {
    CacheNode cachedNode = cache.get(key);
    markMostRecent(cachedNode); // 3. Modifies linked list pointers
    return cachedNode.value;
  } finally {
    lock.writeLock().unlock();
  }
}
```
> [!WARNING]
> **Race Condition**: Under high concurrent access, another thread could evict the node between step 1 and step 2. When step 3 runs, `cache.get(key)` will return `null`. Passing `null` to `markMostRecent` will throw a `NullPointerException` (NPE) at `node.prev.next = node.next`, causing the thread to crash.

### Performance Overhead
- Every successful read request performs **two lock acquisitions** (one read lock inside `exists()`, followed by one write lock). In high-throughput cache environments, reducing synchronization overhead is critical.

### Misleading Thread-Safety Claim
- The design document states: *"use ConcurrentHashMap to be thread-safe"*. However, the code uses standard `HashMap`.
- **Design Note**: Using `HashMap` here is actually correct because modifying the map and the doubly-linked list must be performed atomically. If you used `ConcurrentHashMap` without locking the list operations, the list structure would quickly become corrupt due to race conditions.

---

## 4. Design & Clean Code Improvements

### Use Java Generics
Using `Object` keys and values strips away compile-time type safety. It should be refactored to `Cache<K, V>`.

### Singleton Initialization with Parameters
Initializing a Singleton with a variable parameter (like size) via `initialize(size)` can lead to runtime issues if different parts of the code try to initialize it with different configurations. A clean approach:
- Inject the `Cache` configuration via constructor/dependency injection, OR
- If sticking to a Singleton, use a Thread-safe Double-Checked Locking initialization pattern that supports a one-time configuration parameters step.

---

## 5. Refactored Implementation

Here is the clean, thread-safe, compile-ready, and generic implementation:

```java
import java.util.HashMap;
import java.util.Map;
import java.util.NoSuchElementException;
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

public class Cache<K, V> {
    private static Cache<?, ?> instance;
    private final CacheManager<K, V> manager;

    private Cache(int capacity) {
        this.manager = new CacheManager<>(capacity);
    }

    @SuppressWarnings("unchecked")
    public static synchronized <K, V> void initialize(int capacity) {
        if (instance != null) {
            throw new IllegalStateException("Cache is already initialized");
        }
        instance = new Cache<>(capacity);
    }

    @SuppressWarnings("unchecked")
    public static <K, V> Cache<K, V> getInstance() {
        if (instance == null) {
            throw new IllegalStateException("Cache needs to be initialized first.");
        }
        return (Cache<K, V>) instance;
    }

    public int capacity() {
        return manager.getCapacity();
    }

    public int size() {
        return manager.size();
    }

    public boolean isFull() {
        return manager.isFull();
    }

    public boolean isEmpty() {
        return manager.isEmpty();
    }

    public boolean exists(K key) {
        return manager.exists(key);
    }

    public void put(K key, V value) {
        manager.put(key, value);
    }

    public V get(K key) {
        return manager.get(key);
    }

    public void clearAll() {
        manager.clearAll();
    }
}

class CacheManager<K, V> {
    private final int capacity;
    private final Map<K, CacheNode<K, V>> cacheMap;
    private final CacheNode<K, V> head;
    private final CacheNode<K, V> tail;
    private final ReadWriteLock lock = new ReentrantReadWriteLock();

    public CacheManager(int capacity) {
        this.capacity = capacity;
        this.cacheMap = new HashMap<>();
        this.head = new CacheNode<>(null, null);
        this.tail = new CacheNode<>(null, null);
        this.head.next = this.tail;
        this.tail.prev = this.head;
    }

    public void put(K key, V value) {
        lock.writeLock().lock();
        try {
            if (cacheMap.containsKey(key)) {
                CacheNode<K, V> node = cacheMap.get(key);
                node.value = value;
                markMostRecent(node);
            } else {
                if (cacheMap.size() >= capacity) {
                    evictLRU();
                }
                CacheNode<K, V> newNode = new CacheNode<>(key, value);
                cacheMap.put(key, newNode);
                addNodeToHead(newNode);
            }
        } finally {
            lock.writeLock().unlock();
        }
    }

    public V get(K key) {
        lock.writeLock().lock();
        try {
            CacheNode<K, V> node = cacheMap.get(key);
            if (node == null) {
                throw new NoSuchElementException("Key not found in cache: " + key);
            }
            markMostRecent(node);
            return node.value;
        } finally {
            lock.writeLock().unlock();
        }
    }

    public boolean exists(K key) {
        lock.readLock().lock();
        try {
            return cacheMap.containsKey(key);
        } finally {
            lock.readLock().unlock();
        }
    }

    public int getCapacity() {
        return this.capacity;
    }

    public int size() {
        lock.readLock().lock();
        try {
            return cacheMap.size();
        } finally {
            lock.readLock().unlock();
        }
    }

    public boolean isFull() {
        lock.readLock().lock();
        try {
            return cacheMap.size() >= capacity;
        } finally {
            lock.readLock().unlock();
        }
    }

    public boolean isEmpty() {
        lock.readLock().lock();
        try {
            return cacheMap.isEmpty();
        } finally {
            lock.readLock().unlock();
        }
    }

    public void clearAll() {
        lock.writeLock().lock();
        try {
            cacheMap.clear();
            head.next = tail;
            tail.prev = head;
        } finally {
            lock.writeLock().unlock();
        }
    }

    // Helper methods (must be called within a write lock)
    private void markMostRecent(CacheNode<K, V> node) {
        removeNode(node);
        addNodeToHead(node);
    }

    private void evictLRU() {
        CacheNode<K, V> lruNode = tail.prev;
        if (lruNode != head) { // Ensure cache is not empty
            removeNode(lruNode);
            cacheMap.remove(lruNode.key);
        }
    }

    private void addNodeToHead(CacheNode<K, V> node) {
        node.next = head.next;
        node.prev = head;
        head.next.prev = node;
        head.next = node;
    }

    private void removeNode(CacheNode<K, V> node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }
}

class CacheNode<K, V> {
    final K key; // Key remains immutable
    V value;
    CacheNode<K, V> prev;
    CacheNode<K, V> next;

    public CacheNode(K key, V value) {
        this.key = key;
        this.value = value;
    }
}
```

---

## 6. Discussion in a Real Interview Setting

When presenting this LLD in an interview, structure your explanation around design choices and tradeoffs:

1. **Why standard `HashMap` + custom locks instead of `ConcurrentHashMap`?**
   - *Explanation*: "A common trap is using `ConcurrentHashMap` thinking it solves thread-safety. But an LRU cache operations (`get` and `put`) require update to both a Map and a Doubly-Linked List. These two updates must be atomic. If we locked them separately, the list structure could get corrupted. Hence, we serialize the compound operations using a `ReentrantReadWriteLock` on a standard `HashMap`."
2. **ReadWriteLock performance vs. eviction lock requirement:**
   - *Explanation*: "In a read-heavy system, a `ReadWriteLock` is usually preferred. However, in an LRU Cache, even a `get()` operation modifies the internal state (re-ordering the nodes to the head). This means `get()` requires a **write lock**, limiting concurrent read performance. If this is a bottleneck, we could discuss alternative concurrent structures like using a separate read queue, thread-local buffers (similar to Caffeine Cache), or segmenting the cache (striped locking)."
3. **Handling Eviction Policy extensibility:**
   - *Explanation*: "Right now, LRU is hardcoded in the list operations. If the interviewer asks to support multiple policies (FIFO, LFU, TTL-based), we can decouple the eviction policy into a strategy pattern (e.g., an `EvictionPolicy` interface), where `CacheManager` triggers callbacks on cache hits, misses, and insertions."
