# Core Architectural Patterns: Comprehensive Solutions & Design Decision Drills (Phase 14)

This document provides detailed architectural solutions, trade-off evaluations, and decision matrices for real-world scenarios applying the 16 core patterns in [`01-core-architectural-patterns.md`](./01-core-architectural-patterns.md).

---

## 🎯 Part A: 5 High-Stakes Architectural Pattern Drills & Solutions

### Drill 1: The Multi-Service Vacation Package (Flight + Hotel + Car)
**The Challenge:** A customer books a vacation package spanning three independent microservices: Flight Booking, Hotel Reservation, and Car Rental. Each service owns its own private database. How do you coordinate this multi-service transaction without locking distributed databases?

#### Architectural Solution: The Orchestrated Saga Pattern with Compensating Transactions
* **Why NOT Two-Phase Commit (2PC):**
  * 2PC requires distributed transactions holding database row locks across all three company databases while waiting for external confirmation.
  * If the Car Rental service experiences network lag, locks in the Flight and Hotel databases remain open indefinitely, blocking thousands of unrelated bookings and triggering catastrophic thread pool starvation.
* **The Saga Blueprint:**
  1. An **Orchestrator Service** executes local ACID transactions sequentially across each service:
     * Step 1: Reserve Flight $\to$ Success!
     * Step 2: Reserve Hotel $\to$ Success!
     * Step 3: Reserve Car $\to$ **Failed (Sold Out)!**
  2. The orchestrator catches the failure and immediately triggers **Compensating Transactions** in reverse order:
     * Compensate Step 2: Call Hotel Service to cancel reservation and refund hold.
     * Compensate Step 1: Call Flight Service to release seat reservation and refund hold.
  3. The customer is notified: *"Car was unavailable; no charges were made."*
* **Trade-off:** We sacrifice immediate isolation (a user might see a temporarily reserved flight for 2 seconds while the saga unwinds) in exchange for high availability, zero distributed database locks, and fault isolation.

---

### Drill 2: The High-Scale Social Media Home Timeline
**The Challenge:** Users follow hundreds of accounts. When a user opens the app, they expect their personalized feed in $< 50\text{ms}$. How do you architect feed generation when 99.9% of users have under 500 followers, but a few celebrities have 80 million followers?

#### Architectural Solution: Hybrid Fan-Out Architecture (Pattern 16)
* **The Push-Only Trap (Fan-Out on Write):**
  * When a user posts, background workers push the post to every follower's pre-computed feed cache in Redis.
  * If a normal user with 200 followers posts, writing 200 Redis list entries takes 5ms.
  * But when a celebrity with 80 million followers posts, writing to 80 million feeds requires hours of worker queue time, saturating Redis network cards and delaying feeds for everyone.
* **The Pull-Only Trap (Fan-Out on Read):**
  * If you generate the feed on-demand whenever a user opens the app by querying the posts of everyone they follow (`WHERE user_id IN (1, 2, ... 500)`), the SQL query takes 800ms and crashes the database during peak hours.
* **The Production Hybrid Fix (The Twitter / X Pattern):**
  1. **Push for Normal Users ($< 25,000$ followers):** On post creation, push the post ID into followers' Redis home timeline lists. When they open the app, reads are instantaneous ($O(1)$ in $< 5\text{ms}$).
  2. **Pull for Celebrities ($> 25,000$ followers):** Never fan out celebrity posts to millions of inboxes! Store the celebrity's post in a dedicated celebrity post list.
  3. **Read-Time Merge:** When a user opens their app, fetch their pre-computed feed from Redis, pull the latest posts from the few celebrities they follow, and merge-sort them in application RAM in $< 10\text{ms}$.

---

### Drill 3: The Financial Audit Ledger & Account Balance
**The Challenge:** A digital bank must record customer deposits, withdrawals, and transfers. Auditors require a mathematically verifiable history of every balance change over 10 years. Meanwhile, mobile banking apps demand sub-millisecond account balance checks.

#### Architectural Solution: Event Sourcing + CQRS (Patterns 9 & 10)
* **Why Traditional CRUD Fails:**
  * In standard CRUD (`UPDATE accounts SET balance = balance + 100`), past state is overwritten. If a database glitch or concurrency bug sets balance to \$500, there is zero historical trace of who made the change or why.
* **The Event Sourcing Write Model:**
  * Account balances are **never updated directly**.
  * The Write database (PostgreSQL) is an append-only log of immutable business events:
    ```json
    [
      {"event": "AccountOpened", "amount": 0, "ts": 1},
      {"event": "FundsDeposited", "amount": 500, "ts": 2},
      {"event": "CardPayment", "amount": -45, "ts": 3}
    ]
    ```
* **The CQRS Read Model (Materialized Views):**
  * Replaying 10,000 events to compute balance on every login is too slow.
  * A projection worker listens to the append-only event stream and continuously updates an in-memory **Materialized View** in Redis:
    ```bash
    SET account:42:balance 455.00
    ```
  * Mobile apps query the read model in 1ms; auditors query the immutable event log for compliance.

---

### Drill 4: High-Scale 4K Video Ingestion
**The Challenge:** Users upload 5 GB raw video files from mobile and desktop clients. How do you ingest 100,000 video files per day without crashing your application servers or exhausting bandwidth?

#### Architectural Solution: Direct-to-Storage Pre-Signed S3 Uploads (Pattern 14)
* **The Anti-Pattern (Proxying Through App Servers):**
  * Client streams 5 GB through web servers. Web server thread and memory buffers remain occupied for 10 minutes. A burst of 100 uploads saturates network interfaces and crashes the compute tier.
* **The Blueprint:**
  1. Client sends a tiny JSON request: `POST /api/videos/upload-intent {"filename": "vacation.mp4", "size": 5368709120}`.
  2. Web server validates permissions, generates an **AWS S3 Pre-Signed Multi-Part Upload URL**, and returns it in $< 10\text{ms}$.
  3. Client's browser/app slices the 5 GB file into 10 MB chunks and streams chunks directly to Amazon S3 concurrently.
  4. S3 confirms upload completion; client notifies backend to save the video metadata.
  5. The application compute servers **never touch a single byte of video data**!

---

### Drill 5: Scaling Read-Heavy Databases (The Scaling Progression)
**The Challenge:** Your startup's database CPU is climbing: 60% $\to$ 85% $\to$ 98%. What is the exact architectural progression to scale the database sustainably without premature complexity?

#### Architectural Solution: The 4-Stage Database Scaling Progression
1. **Stage 1: Hardware & Query Optimization (Day 1):**
   * Inspect slow query logs (`EXPLAIN ANALYZE`).
   * Add covering B-Tree indexes on foreign keys and search columns.
   * Vertical scale (upgrade instance CPU/RAM) to buy time.
2. **Stage 2: Cache-Aside with Redis (Day 30):**
   * Keep the 20% most popular queries in Redis RAM.
   * Absorbs 80–90% of repeated `SELECT` queries, dropping database CPU to $< 30\%$.
3. **Stage 3: Read Replicas (Day 90):**
   * Set up 2–3 asynchronous PostgreSQL read replicas.
   * Route all remaining `SELECT` queries to replicas; reserve Primary exclusively for writes.
   * Implement "Read-Your-Own-Writes" to avoid replication lag bugs.
4. **Stage 4: Sharding / Horizontal Partitioning (Year 2+):**
   * When total dataset exceeds single-disk capacity ($> 5\text{ TB}$) or write volume exceeds 10,000 writes/sec, shard data horizontally by a uniform Shard Key (e.g., `hash(user_id) % num_shards`).

---

## 🗺️ Master 16-Pattern Architectural Reference Table

| Pattern | Solves This Bottleneck | What You Gain | What You Sacrifice (The Trade-Off) | Production Failure Mode |
|---|---|---|---|---|
| **1. Layered (N-Tier)** | Spaghetti code | Separation of concerns | Minor boilerplate | Monolithic lock-in |
| **2. Stateless Compute** | Can't autoscale servers | Elastic scaling behind LB | 1ms hop to fetch session | Session store becomes SPOF |
| **3. Cache-Aside** | DB read saturation | Sub-millisecond reads | Eventual consistency; cold misses | Cache stampede / avalanche |
| **4. Read Replicas** | DB CPU high on reads | Scales read throughput | Asynchronous replication lag | Reading stale data |
| **5. DB Sharding** | Write IOPS & disk limits | Unlimited scale horizontally | Cross-shard JOINs impossible | Hot shards (celebrity key) |
| **6. Event-Driven** | Brittle synchronous calls | Decoupled services | Eventual consistency | Hard to debug without tracing |
| **7. Worker Queue** | Slow tasks blocking HTTP | Fast $< 20\text{ms}$ user APIs | User must wait/poll for job | Consumer lag; unhandled retries |
| **8. Pub/Sub Fan-Out** | 1-to-many service updates | Decouples publishers | Multiplies network & broker load | Broker saturation on big fan-out |
| **9. CQRS** | Write vs read model tension | Optimized reads & writes | Complex dual data models | Read model sync lag |
| **10. Event Sourcing** | Overwriting audit history | 100% immutable audit trail | Replaying events is slow | High disk growth; needs snapshots |
| **11. Saga Pattern** | Multi-service transactions | No distributed DB locks | Eventual isolation | Complex compensation logic |
| **12. API Gateway** | Mobile making 20 calls | Single front-door entry | Centralized routing | Gateway becomes bottleneck |
| **13. CDN Edge** | High latency across oceans | Assets cached $< 5\text{ms}$ away | Invalidation delays | Stale CSS/JS bugs |
| **14. Object Pre-Signed** | App servers choked on files | Files stream directly to S3 | S3 eventual consistency | Upload timeout handling |
| **15. Search Pipeline** | Slow SQL `LIKE` queries | Typo tolerance & BM25 rank | 500ms sync delay to index | Sync pipeline lag/desync |
| **16. Hybrid Fan-Out** | Celebrity post storms | Instant reads & fast writes | Two separate code paths | Edge-case ranking bugs |
