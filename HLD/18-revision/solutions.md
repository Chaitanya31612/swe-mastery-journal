# Revision & Decision Cheatsheet: Comprehensive Solutions & Deep Recall (Phase 17)

This document provides deep technical explanations, concurrency sequence diagrams, and mathematical derivations for the 5-Minute Spaced Recall Quiz and advanced architectural decision rules in [`01-spaced-repetition-and-decision-cheatsheet.md`](./01-spaced-repetition-and-decision-cheatsheet.md).

---

## 🧠 Part A: The 5-Minute Spaced Recall Quiz — Deep Solutions

---

### Question 1: How many requests per second is 10 Million requests per day?
* **Quick Answer:** **~120 QPS** (Peak: ~250–360 QPS).
* **Deep Derivation:**
  * Exact calculation:
    $$\text{Average QPS} = \frac{10,000,000\text{ requests}}{86,400\text{ seconds}} \approx 115.74 \approx \mathbf{116\text{ QPS}}$$
  * The Mental Shortcut:
    $$\mathbf{1\text{ Million requests/day} \approx 11.6 \approx 12\text{ QPS}}$$
    $$10 \times 12\text{ QPS} \approx \mathbf{120\text{ QPS}}$$
  * Peak Traffic Multiplier: Traffic is never uniformly distributed throughout the 24-hour day. During peak evening hours, traffic typically surges to $2\times$ to $3\times$ the daily average:
    $$\text{Peak QPS} = 120 \times 2.5 \approx \mathbf{300\text{ QPS}}$$

---

### Question 2: Why do we DELETE a cache key on write instead of updating it?
* **Quick Answer:** **To eliminate concurrency race conditions where an older update overwrites a newer update in the cache.**
* **The Fatal Race Condition Flow (If You Update the Cache):**

```
Time   Thread 1 (Writes "Alice")           Thread 2 (Writes "Bob")
 |
 1     Updates DB: name = "Alice"
 2                                         Updates DB: name = "Bob"
 3                                         Updates Cache: name = "Bob" (Correct!)
 4     Updates Cache: name = "Alice" <--- DISASTER! Race condition overwrites newer value!
 v
State: Database has "Bob", but Cache has "Alice" indefinitely!
```

* **Why Deletion Fixes This:**
  * When Thread 1 and Thread 2 both simply `DEL user:42:profile`, the order does not matter! The key is removed from Redis.
  * The next user read experiences a clean cache miss, reads the single source of truth from the database (which contains "Bob"), and repopulates the cache with fresh data.

---

### Question 3: What is the difference between Replication and Sharding?
* **Quick Answer:** **Replication copies the exact same dataset across multiple machines for durability and read capacity; Sharding splits a huge dataset into distinct pieces across machines for write capacity and storage limits.**
* **Deep Comparison:**

| Dimension | Database Replication | Database Sharding (Partitioning) |
|---|---|---|
| **What It Does** | Clones identical data to multiple nodes ($N$ copies) | Distributes mutually exclusive slices of data |
| **Solves This Bottleneck** | Read CPU saturation and hardware disaster recovery | Disk storage exhaustion and write IOPS limits |
| **Write Impact** | Does NOT scale writes (writes must replicate to all nodes) | Scales writes linearly across multiple shard primaries |
| **Query Complexity** | Simple; any replica can execute full SQL joins | Complex; cross-shard joins are slow or impossible |

---

### Question 4: What happens if you have 30 Kafka consumer pods on a topic with only 10 partitions?
* **Quick Answer:** **10 pods read from the 10 partitions; the other 20 pods sit completely idle doing zero work!**
* **Deep Architectural Reason:**
  * The Kafka consumer group protocol enforces a fundamental concurrency invariant: **within a single consumer group, a partition can be assigned to at most ONE consumer thread at any given time**.
  * This rule exists to guarantee strict message ordering within each partition without requiring expensive distributed locks.
  * To utilize 30 active consumer pods, you **must first repartition the Kafka topic to have at least 30 partitions**.

---

### Question 5: What is a Circuit Breaker?
* **Quick Answer:** **A safety fuse in software that monitors remote dependency failures; when failures cross a threshold, it trips to OPEN and fails fast upstream without making network calls, allowing the downstream system to recover.**
* **The 3 Operational States:**
  1. **CLOSED (Normal):** All requests pass through to the downstream service. Failures and timeouts are measured.
  2. **OPEN (Outage / Tripped):** Failure rate exceeded threshold (e.g., $> 50\%$). The breaker immediately returns a fallback or error in $< 1\text{ms}$ without touching the network, preserving caller threads.
  3. **HALF-OPEN (Trial Probe):** After a cooldown window (e.g., 30 seconds), the breaker allows a single trial request through. If it succeeds, it resets to CLOSED; if it fails, it returns to OPEN.

---

### Question 6: Why do we add random Jitter to cache TTLs?
* **Quick Answer:** **To prevent a Cache Avalanche where thousands of keys expire at the exact same second, causing a thundering herd that crashes the database.**
* **The Math of Jitter:**
  * Without Jitter: 100,000 product pages are warmed at 12:00:00 with `TTL = 86400` (exactly 24 hours). At 12:00:00 the next day, all 100,000 keys expire at the exact same millisecond. The database CPU instantly spikes to 100%.
  * With Jitter:
    $$\text{TTL} = 86,400\text{ seconds} \pm \text{Random}(0, 3,600\text{ seconds})$$
  * Expirations are smoothly spread over a 2-hour window. The database absorbs a tiny trickle of cache misses with zero performance degradation.

---

## 🚀 Part B: Advanced Architectural Decision Drills

### Drill 1: The Transactional Outbox Pattern
* **The Problem:** You must write an order to PostgreSQL and emit an `OrderCreated` event to Kafka. If you write to Postgres first, and the server crashes before sending to Kafka, the message is lost. If you write to Kafka first, and Postgres fails, you emitted a ghost event.
* **The Solution:** In the exact same SQL transaction, insert the event into an `outbox` table. A CDC worker (Debezium) tailing the PostgreSQL Write-Ahead Log (WAL) streams the event reliably to Kafka (**Guaranteed At-Least-Once Delivery**).

### Drill 2: Read-Your-Own-Writes Consistency
* **The Problem:** A user updates their profile picture, redirects to their profile page, but sees their old picture because their read hit an asynchronous read replica with 500ms replication lag.
* **The Solution:** When a user commits a write, set a temporary cookie or Redis token (`user:42:recent_write = 1` with TTL = 5 seconds). If this token exists, route all read queries for that specific user directly to the **Primary Database**. Route all other users to read replicas.

### Drill 3: Connection Multiplexing (PgBouncer)
* **The Problem:** 500 microservice pods each hold 20 open database connections ($10,000$ total connections). PostgreSQL consumes 10 MB RAM per connection and crashes due to process context-switching overhead.
* **The Solution:** Place **PgBouncer** in front of PostgreSQL in `transaction pooling` mode. PgBouncer keeps a warm pool of only 100 physical connections to PostgreSQL, multiplexing thousands of incoming application queries over those 100 connections seamlessly.
