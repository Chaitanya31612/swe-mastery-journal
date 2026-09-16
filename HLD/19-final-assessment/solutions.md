# Capstone Readiness Exam: Master Solutions & Answer Key (Phase 18)

This document provides complete, definitive, Staff-engineer-level solutions for all sections (Parts A through F) of the Capstone Readiness Exam in [`01-comprehensive-readiness-exam.md`](./01-comprehensive-readiness-exam.md).

---

## 🎯 Part A: Rapid-Fire Recall (20 Questions)

1. **Latency vs. Throughput:**
   * **Latency** is the time taken to complete a single unit of work (e.g., 20ms per API call).
   * **Throughput** is the total volume of work completed per unit of time (e.g., 5,000 requests per second).
2. **Quorum Formula:**
   * For a cluster of $N$ nodes, read quorum $R$ and write quorum $W$ must satisfy:
     $$\mathbf{W + R > N}$$
   * Ensuring that any read quorum intersects with the write quorum by at least one overlapping node that holds the latest committed state.
3. **1M Requests/Day to QPS:**
   * A day has $86,400\text{ seconds} \approx 100,000\text{ seconds}$.
   * $\frac{1,000,000}{86,400} \approx \mathbf{11.6 \approx 12\text{ QPS}}$ (Peak $\approx 24\text{–}36\text{ QPS}$).
4. **Layer 4 vs. Layer 7 Load Balancing:**
   * **Layer 4 (Transport):** Routes packets based purely on IP address and TCP/UDP port without inspecting the packet payload; faster and handles higher throughput.
   * **Layer 7 (Application):** Decrypts TLS and inspects HTTP headers, cookies, and URL paths (`/api/v1/checkout`); allows content-based routing at the cost of higher CPU overhead.
5. **Why DELETE Cache Key on Write (Never Update):**
   * Updating the cache creates a concurrency race condition where an older write can overwrite a newer write. Deleting the key forces the next read to fetch the fresh single source of truth from the database.
6. **20 Workers on a 10-Partition Kafka Topic:**
   * Exactly **10 workers** are assigned 1 partition each and read actively; the remaining **10 workers sit completely idle**, because Kafka allows at most one consumer per partition within a consumer group.
7. **Replication vs. Sharding:**
   * **Replication** copies the *same* data to multiple machines for fault tolerance and read throughput.
   * **Sharding** splits a large dataset into *mutually exclusive slices* across machines to scale writes and storage capacity.
8. **Why LSM-Trees Write Faster than B+ Trees:**
   * B+ Trees require in-place random disk writes to update tree pages, which suffers from disk seek and write amplification penalties.
   * LSM-Trees write sequentially into an in-memory buffer (MemTable) and an append-only commit log on disk with zero random disk seeks.
9. **Dead-Letter Queue (DLQ):**
   * A secondary queue where messages that fail processing repeatedly (e.g., after 3 or 5 retries due to malformed payloads or "poison pills") are moved so they do not block the main processing queue.
10. **Error Budget & What Happens When Burned:**
    * The allowable margin of downtime/unreliability defined by an SLO ($100\% - \text{SLO}$, e.g., 0.1% downtime for a 99.9% SLO).
    * When burned completely, feature deployments are frozen, and engineering focus shifts 100% to stability, bug fixes, and reliability engineering.
11. **Why Averages Lie:**
    * Arithmetic means hide extreme outliers in skewed distributions. A system can have an average latency of 25ms while the 99th percentile (p99) suffers a 5-second freeze.
12. **Cache Stampede & Mitigation:**
    * When a high-traffic cached key expires, thousands of concurrent requests miss the cache simultaneously and slam the database.
    * Stopped using a **Distributed Mutex (`SETNX`)** or single-flight loader so only 1 thread queries the database while others wait.
13. **Token Bucket Burst Handling:**
    * Tokens are added to the bucket at a constant rate up to a max bucket capacity. A burst of requests can consume all available tokens instantly down to zero, after which traffic is strictly throttled to the token refill rate.
14. **The Outbox Pattern:**
    * Writing business data and outgoing domain events into the same relational database inside a single local ACID transaction. A CDC worker streams the events to Kafka, guaranteeing dual writes never diverge.
15. **Kubernetes Liveness vs. Readiness Probes:**
    * **Liveness Probe:** Checks if the container is alive; if it fails, Kubernetes restarts the pod.
    * **Readiness Probe:** Checks if the container is ready to accept incoming traffic; if it fails, Kubernetes temporarily removes the pod from load balancer endpoints.
16. **Why New York to Tokyo Takes $\ge 70\text{ms}$:**
    * The physical distance is $\approx 11,000\text{ km}$. The speed of light in fiber optic glass is $\approx 200,000\text{ km/s}$ ($5\text{ }\mu\text{s/km}$). A round trip of $22,000\text{ km}$ physically requires a minimum of $110\text{ms}$ in fiber.
17. **Inverted Index:**
    * A data structure that maps words/tokens to the list of document IDs in which they appear (like the index at the back of a textbook mapping keywords to page numbers), enabling instant full-text search.
18. **At-Least-Once vs. At-Most-Once Delivery:**
    * **At-Least-Once:** Messages are retried until acknowledged; guarantees no message is lost, but duplicates may occur (requires idempotent consumers).
    * **At-Most-Once:** Messages are never retried; messages may be lost, but duplicates never occur.
19. **Bulkhead Pattern:**
    * Partitioning resources (thread pools, memory, server pods) into isolated pools so that a failure or runaway load in one non-critical feature cannot exhaust resources and crash critical core features.
20. **Direct-to-S3 Pre-Signed Uploads:**
    * Client browsers stream large binary files directly to Amazon S3 over S3 pre-signed URLs, preventing gigabytes of file data from consuming application server RAM, worker threads, and bandwidth.

---

## 🥊 Part B: Concept Showdown (10 Quick Comparisons)

1. **Redis vs. PostgreSQL:**
   * Redis is an in-memory key-value data store optimized for sub-millisecond ephemeral operations and caching.
   * PostgreSQL is a disk-based relational database providing ACID transactions, relational integrity, and durable long-term storage.
2. **SQL vs. NoSQL:**
   * SQL enforces fixed schemas, B-Tree indexes, and strong ACID relational joins across normalized tables.
   * NoSQL trades multi-table joins and ACID transactions for horizontal partitioning, schema flexibility, and massive write throughput.
3. **Queue (SQS) vs. Pub/Sub (SNS):**
   * SQS is point-to-point where competing workers share a queue and each message is consumed by exactly one worker.
   * SNS is a broadcast topic where published messages are fanned out to all subscribed queues simultaneously.
4. **Replication vs. Sharding:**
   * Replication clones identical copies of data to scale read throughput and survive hardware crashes.
   * Sharding divides a dataset across machines by a shard key to overcome single-node disk capacity and write IOPS limits.
5. **Synchronous REST vs. Asynchronous Queues:**
   * Synchronous REST holds open network sockets while waiting for immediate responses, coupling caller and receiver availability.
   * Asynchronous Queues decouple systems temporally, allowing producers to enqueue events in $< 2\text{ms}$ and consumers to process at their own pace.
6. **Redis Cache vs. CDN Edge:**
   * Redis caches dynamic database query results and session data in RAM within the backend datacenter.
   * CDNs cache static media and HTML pages on edge servers distributed globally within 5 miles of end users.
7. **Stateless Compute vs. Sticky Sessions:**
   * Stateless compute stores zero session data in local server RAM, allowing any server to handle any request and enabling instant autoscaling.
   * Sticky sessions pin users to specific servers via session cookies, complicating deployments and crashing sessions if a server dies.
8. **Fan-Out on Write (Push) vs. Fan-Out on Read (Pull):**
   * Push pre-computes home feeds into follower inboxes on post creation, giving instant reads ($O(1)$) but choking on celebrity posts.
   * Pull fetches and merges posts dynamically when a user opens the app, making writes fast but making reads heavy.
9. **Two-Phase Commit (2PC) vs. Saga:**
   * 2PC provides distributed ACID transactions by holding database row locks across systems, making it brittle to network lag.
   * Sagas execute local transactions sequentially and recover from partial failures via compensating transactions, trading isolation for availability.
10. **p50 Latency vs. p99 Latency:**
    * p50 represents the median user experience where 50% of requests are faster.
    * p99 represents the worst 1% tail latency, exposing system bottlenecks, garbage collection pauses, and lock contention.

---

## 🧮 Part C: Napkin Math (5 Real Calculations)

### 1. Photo App Daily QPS
* **Inputs:** 30M DAU, 40 photo views/day, 2 photo uploads/day.
* **Reads:**
  $$\text{Daily Reads} = 30\text{M} \times 40 = 1.2\text{ Billion reads/day}$$
  $$\text{Average Read QPS} = \frac{1,200,000,000}{86,400} \approx \mathbf{13,888 \approx 14,000\text{ QPS}}$$
  $$\text{Peak Read QPS } (3\times) \approx 14,000 \times 3 = \mathbf{42,000\text{ QPS}}$$
* **Writes:**
  $$\text{Daily Writes} = 30\text{M} \times 2 = 60\text{ Million uploads/day}$$
  $$\text{Average Write QPS} = \frac{60,000,000}{86,400} \approx \mathbf{694 \approx 700\text{ QPS}}$$
  $$\text{Peak Write QPS } (3\times) \approx 700 \times 3 = \mathbf{2,100\text{ QPS}}$$

---

### 2. IoT Fleet Storage Growth
* **Inputs:** 100M pings/day, 200 bytes/ping, $3\times$ replication copies, 1 year (365 days).
  $$\text{Daily Raw Storage} = 100,000,000 \times 200\text{ bytes} = 20,000,000,000\text{ bytes} = 20\text{ GB/day}$$
  $$\text{1-Year Raw Storage} = 20\text{ GB} \times 365 = 7,300\text{ GB} = 7.3\text{ TB}$$
  $$\text{Total Storage with } 3\times \text{ Replication} = 7.3\text{ TB} \times 3 = \mathbf{21.9\text{ TB/year}}$$

---

### 3. Video Streaming Network Pipe
* **Inputs:** 50M video segments/day, 4 MB per segment.
  $$\text{Daily Data Volume} = 50,000,000 \times 4\text{ MB} = 200,000,000\text{ MB} = 200\text{ TB/day}$$
  $$\text{Data Transfer Rate} = \frac{200\text{ TB}}{86,400\text{ sec}} \approx 2.315\text{ GB/sec}$$
  $$\text{Bandwidth in Gbps} = 2.315\text{ GB/sec} \times 8\text{ bits/byte} \approx \mathbf{18.52\text{ Gbps (continuous)}}$$
  * Peak traffic ($2.5\times$ multiplier) $\approx 18.52 \times 2.5 \approx \mathbf{46.3\text{ Gbps}}$.

---

### 4. Cache Sizing (80/20 Rule)
* **Inputs:** 200 GB of read queries per day.
* Applying the Pareto Principle (80% of traffic hits 20% of data):
  $$\text{Cache Working Set} = 200\text{ GB} \times 0.20 = \mathbf{40\text{ GB}}$$
* Factoring in Redis metadata overhead ($1.25\times$ safety margin):
  $$\text{Recommended Redis RAM} \approx 40\text{ GB} \times 1.25 = \mathbf{50\text{ GB of RAM}}$$

---

### 5. Autoscaling Pod Calculations
* **Inputs:** 1 pod handles 250 req/sec; Peak traffic = 8,000 QPS.
  $$\text{Pods Required} = \frac{8,000\text{ QPS}}{250\text{ QPS/pod}} = 32\text{ pods}$$
* With an $N + 2$ redundancy buffer for rolling deployments and zone resilience ($+25\%$ headroom):
  $$\text{Cluster Target Capacity} = 32 \times 1.25 = \mathbf{40\text{ container pods}}$$

---

## 🚒 Part D: Production Firefighting (5 Scenarios)

### 1. The Domino Crash
* **What Happened:** Service B slowed to 25s. Because Service A had a 30s timeout, Service A's worker threads remained blocked on socket reads for 25s. At incoming traffic of 50 req/sec, all worker threads in Service A were consumed within seconds, causing a cascading outage.
* **The Safety Fuse:**
  1. Reduce request timeout from 30s to **800ms**.
  2. Implement a **Circuit Breaker** (e.g., Resilience4j/Envoy) to trip OPEN after 50% timeouts, failing fast in $< 1\text{ms}$ and preserving Service A's thread pool.

### 2. The 4-Node Split-Brain
* **What Went Wrong:** With 4 nodes (2 in NY, 2 in London), when the network partition severed the ocean link, neither side could form a strict majority ($> \frac{4}{2} = 3$). Because the cluster was improperly configured without strict majority consensus, both 2-node partitions declared themselves leaders and accepted conflicting customer writes.
* **The Fix:** Maintain an **odd number of nodes (3 or 5 nodes)**. In a 5-node cluster (3 in NY, 2 in London), NY holds the strict majority ($3 \ge 3$) and continues serving writes, while London ($2 < 3$) automatically steps down and refuses writes, mathematically preventing split-brain.

### 3. The Midnight Avalanche
* **What Happened:** 500,000 cached product keys were generated with the exact same static TTL (`TTL = 86400`). Exactly at midnight, all 500,000 keys expired at the identical millisecond, sending a massive stampede of cache misses directly to the database disk.
* **The Fix:** Add **TTL Jitter**: `TTL = 86400 + random(-3600, 3600)`. Expirations are smoothed over a 2-hour window, eliminating the midnight spike forever.

### 4. The Deadlock Kafka Topic
* **What Happened:** The Kafka topic has only 10 partitions. Under the Kafka consumer protocol, at most 1 consumer worker within a consumer group can read from a partition. The 40 newly spawned pods sat 100% idle.
* **The Fix:**
  1. Repartition the Kafka topic from 10 to **50 partitions** so all 50 pods can actively consume.
  2. Alternatively, have each worker pod dispatch messages into an internal multi-threaded worker pool.

### 5. The Unindexed Big Delete
* **What Happened:** Executing `DELETE FROM audit_logs WHERE date < '2025-01-01'` on 100M rows forces PostgreSQL/MySQL to acquire exclusive table/row locks, scan millions of pages, and write gigabytes of undo/redo logs in a single massive transaction. All other read/write queries blocked waiting for table locks.
* **The Fix:**
  1. **Batch Deletions:** Delete in small chunks: `DELETE WHERE id IN (SELECT id FROM audit_logs WHERE date < ... LIMIT 1000)` with sleep pauses between batches.
  2. **Table Partitioning (Optimal):** Partition the table by date (`PARTITION BY RANGE (date)`). Deleting an old month becomes a zero-cost instant metadata command: `DROP TABLE audit_logs_2024_12;`.

---

## 📐 Part E: Mini-Designs (3 Quick Napkin Sketches)

### 1. One-Time Secret Sharing (Privnote Clone)
* **FR:** User submits secret string $\to$ returns one-time link. When link is opened, secret is displayed once and destroyed forever.
* **NFR:** Zero residual data on disk, end-to-end encryption, TTL expiration (24 hours).
* **Data Model (Redis In-Memory):** Key: `secret:{token_hash}`, Value: `{encrypted_payload}`, TTL: `86400`.
* **Core Path:**
  1. Client encrypts text in browser with a symmetric key ($K$). The key is placed in the URL hash fragment (`#key123`), which is never sent to the server.
  2. Server receives encrypted ciphertext, stores in Redis with a 24-hour TTL, and returns short link.
  3. When recipient opens link, server executes an **Atomic Get-And-Delete via Lua script**:
     ```lua
     local val = redis.call('get', KEYS[1])
     if val then redis.call('del', KEYS[1]) end
     return val
     ```
  4. Server returns ciphertext; client decrypts locally in browser. Subsequent clicks return 404.

### 2. Live Sports Scoreboard (10M Concurrent Users, $< 1\text{s}$ Latency)
* **FR:** Push World Cup goal alerts and live scores to 10M active mobile apps in $< 1\text{s}$.
* **NFR:** Low origin load, high broadcast fan-out, battery friendly.
* **Data Model:** In-memory match document in Redis: `match:101:score -> {"home": 2, "away": 1, "minute": 88}`.
* **Architecture:**
  1. **Ingestion:** Referee system writes score update to backend API $\to$ published to Redis Pub/Sub topic.
  2. **Fan-Out Edge Fleet:** A cluster of distributed connection gateway pods (Go/Erlang) maintain 10M long-lived **Server-Sent Events (SSE)** or WebSocket connections.
  3. Gateway pods subscribe to the Redis match channel and fan out the score payload down established client sockets within 200ms.

### 3. Resilient Webhook Dispatcher
* **FR:** Ingest internal domain events (`order.paid`) and deliver HTTP POST payloads to third-party merchant URLs.
* **NFR:** At-least-once delivery, exponential backoff retries, protection against slow endpoints.
* **Architecture:**
  1. Microservices publish events to Kafka topic `merchant-webhooks`.
  2. Dispatcher worker pulls event, signs payload with HMAC-SHA256, and makes HTTP POST to merchant URL with a strict 3-second timeout.
  3. **Retry Strategy:** On 5xx or timeout, worker re-enqueues into delayed retry queues using exponential backoff with jitter (1m, 5m, 30m, 2h, 24h).
  4. After 5 failed attempts, message moves to a **Dead-Letter Queue (DLQ)** and notifies the merchant dashboard.

---

## 🎙️ Part F: 60-Second Verbal Elevator Pitches (10 Concepts)

1. **System Design:**
   > *"System design is the discipline of making deliberate engineering trade-offs under physical and computational constraints. It is about understanding what breaks first as data scales, choosing the simplest building blocks that fulfill business requirements, and designing architectures that fail gracefully when hardware inevitably crashes."*
2. **Cache-Aside:**
   > *"Cache-Aside is the pattern where the application orchestrates data flow between cache and database. On read, the app checks Redis first, falling back to the database on a miss and warming the cache. On write, the app updates the database and deletes the cache key, eliminating race conditions while keeping 80% of read traffic in memory."*
3. **Backpressure:**
   > *"Backpressure is a flow-control mechanism where a downstream system under heavy load signals upstream producers to slow down. Instead of accepting requests until memory exhausts and workers crash, the system buffers work in durable queues, rejects excess traffic with HTTP 429, and throttles throughput to a sustainable processing rate."*
4. **Idempotency:**
   > *"Idempotency is the property where performing an operation multiple times produces the exact same result as performing it once. In distributed systems where networks drop packets and retry failed calls, idempotent endpoints ensure that resending an order or payment request never results in duplicate charges or duplicate rows."*
5. **Why Averages Are Misleading:**
   > *"Averages are misleading because they dilute extreme outliers across thousands of fast requests. In production, a 25ms average latency can easily hide a p99 tail where 1% of your customers experience a 4-second freeze. Senior engineers monitor p95 and p99 percentiles to optimize real user experiences."*
6. **Availability vs. Durability:**
   > *"Availability measures whether your service is currently online and responding to user requests without error. Durability measures whether committed data remains safely preserved on non-volatile storage forever. A bank will gladly sacrifice availability by going offline rather than sacrifice durability and lose customer account balances."*
7. **Database Sharding:**
   > *"Database sharding is horizontal partitioning where a massive dataset is divided across separate database nodes using a shard key. We reach for sharding when total data size exceeds single-disk limits or write volume saturates database disk IOPS, trading away cross-shard joins for horizontal write scalability."*
8. **Circuit Breaker:**
   > *"A circuit breaker is an architectural fuse that wraps remote network calls. When a downstream dependency experiences elevated error rates or timeouts, the breaker trips to OPEN and fails fast immediately, shielding upstream caller threads from exhaustion and allowing the downstream service time to recover."*
9. **Zero Trust Security:**
   > *"Zero Trust is the architectural security principle of 'never trust, always verify'. Rather than assuming anything inside the corporate network perimeter is safe, Zero Trust verifies identity, enforces mutual TLS, and requires strict object-level authorization for every single internal service call."*
10. **The Saga Pattern:**
    > *"The Saga pattern is a distributed transaction pattern for microservices that avoids distributed database row locks. It coordinates multi-service workflows through a sequence of local ACID transactions; if any step fails, the saga executes compensating transactions backwards to undo previous steps and restore data consistency."*
