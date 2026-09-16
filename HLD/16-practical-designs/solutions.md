# Practical System Designs: Comprehensive Architectural Solutions (Phase 15)

This document provides complete, interview-grade architectural solutions for all 10 System Design Challenges across Level 1 and Level 2 in [`01-level-1-foundational-designs.md`](./01-level-1-foundational-designs.md) and [`02-level-2-distributed-designs.md`](./02-level-2-distributed-designs.md).

---

# 🧱 Level 1: Foundational Designs

---

## Challenge 1: The Short Link Machine (TinyURL / Bitly)

### 1. Requirements & Scale Math
* **Traffic:** 100M writes/month ($\approx 40\text{ writes/sec}$ avg; $150\text{ peak}$); 10B reads/month ($\approx 4,000\text{ QPS}$ avg; $15,000\text{ peak}$).
* **Retention:** 5 years $\implies 100\text{M} \times 12 \times 5 = 6\text{ Billion records}$.
* **Storage:** Each record $\approx 500\text{ bytes}$ (ID + short_code + long_url + user_id + created_at):
  $$\text{5-Year Storage} = 6\text{B} \times 500\text{ bytes} = 3\text{ TB}$$

### 2. The Big Architectural Decisions

#### Decision A: 7-Character Short Code Generation (Base62 vs. Hashing)
* **Option 1 (Hash + Truncate):** Taking MD5/SHA256 of `long_url` and taking first 7 characters causes **hash collisions** requiring iterative probing (`hash + salt`), adding database round-trips.
* **Option 2 (Distributed Unique ID Generator + Base62 Encoding — RECOMMENDED):**
  * Use 64-bit integer auto-increment IDs generated via Snowflake IDs or a distributed counter service.
  * Convert integer ID to Base62 (`[a-z, A-Z, 0-9]`).
  * 7 Base62 characters yield $62^7 \approx \mathbf{3.5\text{ Trillion unique URLs}}$, far exceeding our 6 billion requirement.
  * **Zero collisions mathematically guaranteed.**

#### Decision B: HTTP 301 vs. HTTP 302
* `HTTP 301 (Moved Permanently)`: The user's browser caches the target URL forever. Fast for the user, but the browser never calls your server again, resulting in **zero click analytics**.
* `HTTP 302 (Found / Temporary Redirect) — RECOMMENDED`: Every click hits your service first before redirecting. Adds a tiny $< 10\text{ms}$ hop, but enables complete analytics tracking (geographic location, referrers, click counts).

#### Decision C: Redis Cache Sizing (80/20 Rule)
* Daily reads: $\frac{10\text{ Billion}}{30} \approx 333\text{ Million clicks/day}$.
* 20% hot URLs account for 80% of clicks: $333\text{M} \times 0.20 \approx 66.6\text{ Million hot links}$.
* Daily RAM needed: $66.6\text{M} \times 500\text{ bytes} \approx \mathbf{33.3\text{ GB of Redis RAM}}$.
* Easily hosted on a small 3-node Redis cluster with LRU eviction.

### 3. Architecture & Data Flow
```
[ Client Browser ] ----(1) GET /a8F3k9 --------------------> [ CDN Edge ]
                                                                 | (Cache Miss)
                                                                 v
                                                        [ Load Balancer ]
                                                                 |
                                                                 v
                                                        [ TinyURL Service ]
                                                                 |
                           +-------------------------------------+-----------------------+
                           | (Check Cache)                                               | (Async Event)
                           v                                                             v
                    [ Redis Cluster ] <--(Cache Miss)--> [ PostgreSQL / DynamoDB ]   [ Kafka: Click Events ]
                           |                                                             |
                           +---------(HTTP 302: Location: https://amazon.com/...)        v
                                                                                   [ ClickHouse Analytics ]
```

---

## Challenge 2: The Digital Scratchpad (Pastebin)

### 1. Requirements & Scale Math
* **Traffic:** 2M writes/day ($\approx 24\text{ writes/sec}$); 20M reads/day ($\approx 240\text{ QPS}$).
* **Payload:** Average 10 KB; Maximum 10 MB.
* **Daily Storage:** $2\text{M} \times 10\text{ KB} = 20\text{ GB/day} \implies 7.3\text{ TB/year}$.

### 2. The Big Architectural Decisions

#### Decision A: Where Does the Text Blob Live?
* **Relational DB BLOB (Anti-Pattern):** Storing 10 MB text files in PostgreSQL database rows causes table bloat, degrades index scans, and makes backups painful.
* **Object Store (AWS S3) + Relational Metadata (RECOMMENDED):**
  * Store the raw paste body as an immutable text file in Amazon S3 (`s3://pastes/{paste_id}.txt`).
  * Store metadata (id, user_id, title, s3_path, expires_at, created_at) in PostgreSQL or DynamoDB.

#### Decision B: Expired Paste Cleanup (Handling Expiration)
* **The Cron Job Trap:** Running `DELETE FROM pastes WHERE expires_at < NOW()` locks database tables and degrades production queries.
* **The 2-Pronged Production Strategy:**
  1. **Lazy Deletion on Read:** When a user requests a paste, check `expires_at`. If expired, return `HTTP 404 Not Found` and emit an asynchronous deletion event.
  2. **S3 Object Lifecycle Rules:** Configure S3 bucket lifecycle rules to automatically purge raw files after 30 days ($0\text{ compute overhead}$).
  3. **Low-Priority Nightly Reaper:** A background worker deletes expired database metadata rows in small throttled batches of 500 during off-peak hours.

---

## Challenge 3: The Front Door Bouncer (Distributed Rate Limiter)

### 1. Requirements & Scale Math
* **Traffic:** Evaluate **100,000 incoming requests per second** across 200 web servers with $< 2\text{ms}$ latency overhead.
* **Policy:** 100 requests per minute per client IP / API key.

### 2. The Big Architectural Decisions

#### Decision A: Algorithm (Token Bucket vs. Sliding Window Counter)
* **Sliding Window Log:** Stores timestamps of every request in Redis sorted sets; memory overhead is high ($100\text{ bytes} \times 100 = 10\text{ KB}$ per user).
* **Token Bucket (RECOMMENDED):**
  * Each bucket has `capacity = 100` and `refill_rate = 100 tokens / 60 seconds`.
  * Stored in Redis as a simple hash with only 2 fields: `tokens_left` and `last_refreshed_at` ($\approx 20\text{ bytes}$ per user). Extremely memory efficient.

#### Decision B: Distributed Counter Coordination
* **Atomic Redis Lua Script:**
  * To avoid race conditions between 200 web servers, run token calculation atomically inside Redis:
  ```lua
  local key = KEYS[1]
  local limit = tonumber(ARGV[1])
  local current = tonumber(redis.call('get', key) or "0")
  if current + 1 > limit then
      return 0
  else
      redis.call("INCRBY", key, 1)
      if current == 0 then redis.call("EXPIRE", key, 60) end
      return 1
  end
  ```

#### Decision C: Fail Open vs. Fail Closed
* **Verdict: Fail Open!**
  * If the Redis rate limiter cluster crashes or network partitions, the rate limiter **fails open** (allows traffic through) while alerting engineering.
  * Blocking 100% of legitimate paying customers because a security counter crashed is an unacceptable business failure.

---

## Challenge 4: The Freight Delivery System (High-Scale File Upload)

### 1. Requirements & Scale Math
* **Traffic:** 5 Million files/day (sizes from 50 MB to 10 GB).
* **Constraint:** Flaky mobile connections, pause/resume support, zero web server memory exhaustion.

### 2. The Big Architectural Decisions

#### Decision A: Direct-to-S3 Pre-Signed Multi-Part Upload Architecture
```
[ Client ] ----(1) POST /initiate-upload {filename, size, chunks: 500} ----> [ Web Server ]
   |                                                                                |
   | <---(2) Returns UploadID + 500 Pre-Signed S3 Part URLs ------------------------+
   |
   +-----(3) PUT Part #1 (10 MB) directly to S3 ---------> [ Amazon S3 Bucket ]
   +-----(4) PUT Part #2 (10 MB) directly to S3 ---------> [ Amazon S3 Bucket ]
   +-----(5) PUT Part #N (10 MB) directly to S3 ---------> [ Amazon S3 Bucket ]
   |
   +-----(6) POST /complete-upload {UploadID, part_etags} ---------------> [ Web Server ]
                                                                                |
                                                                          (Calls S3 Complete)
```
* **Why this is resilient:**
  * Application servers handle only lightweight JSON tokens.
  * The client browser chops the 5 GB file into 10 MB chunks.
  * Each chunk is uploaded independently with its own S3 Pre-Signed URL.
  * If the connection drops at 90%, the client simply resumes uploading chunks 91–100. It never restarts from 0%!

---

## Challenge 5: The Instant Photo Studio (Image Hosting & Resizing)

### 1. Requirements & Scale Math
* **Traffic:** 5M uploads/day ($\approx 60/\text{sec}$); 500M views/day ($\approx 6,000\text{ QPS}$ avg; $20,000\text{ peak}$).
* **Images:** Average 3 MB original photo.

### 2. The Big Architectural Decisions

#### Decision A: Eager vs. Lazy (On-Demand) Resizing
* **Eager (Anti-Pattern):** Pre-generating 15 different image formats/dimensions on upload wastes $15\times$ storage on sizes that may never be viewed.
* **Lazy On-Demand Resizing (RECOMMENDED):**
  * Store only the original high-resolution master photo in S3.
  * Generate resized dimensions on-the-fly the first time a user requests that specific dimension, and cache the result permanently on the CDN edge.

#### Decision B: Where Does Resizing Compute Live?
* **Edge Compute (Cloudflare Workers / AWS Lambda@Edge):**
  * Incoming URL: `https://images.site.com/p101.jpg?w=300&h=200&fmt=webp`.
  * **CDN Cache Hit:** Returns cached image from edge in $< 10\text{ms}$.
  * **CDN Cache Miss:** Edge function fetches original photo from S3, executes WebP resize in memory ($< 80\text{ms}$), stores the resized file back to S3/CDN cache, and returns it to the client. Subsequent users get instant edge hits.

---

# 🚀 Level 2: Distributed Infrastructure Designs

---

## Challenge 6: The City Megaphone (Universal Notification Platform)

### 1. Requirements & Scale Math
* **Traffic:** 50M notifications/day ($\approx 600/\text{sec}$ avg; $5,000/\text{sec}$ peak).
* **Classes:** Critical ($< 5\text{s}$ SLA: 2FA/fraud) vs. Bulk (2-hour SLA: marketing blasts).

### 2. The Big Architectural Decisions

#### Decision A: Priority Lane Isolation (Bulkheads)
* Never mix 2FA traffic and marketing traffic in the same queue!
* **Dedicated Queues:**
  * `priority-high-queue` (2FA, Fraud): Consumed by dedicated workers with zero queue backlog.
  * `priority-bulk-queue` (Promotions): Throttled and rate-limited.
* Even if marketing publishes 10 million push alerts, the high-priority queue remains completely empty and processes 2FA codes in $< 1\text{ second}$.

#### Decision B: User Preferences & Global Rate Limiting
* Before enqueuing notifications, query Redis:
  * Check opt-outs: `user:preferences:push_enabled == false`.
  * Check fatigue limits: `INCR user:42:notifications_sent_today EX 86400`. If counter $> 3$, drop the bulk notification.

#### Decision C: Third-Party Telecom Failover
* Wrap third-party SMS/Push providers (Twilio, Vonage, FCM) with **Circuit Breakers**.
* If Twilio failure rate $> 20\%$, route traffic automatically to secondary provider (AWS SNS).

---

## Challenge 7: The Digital Post Office (High-Scale Transactional Email)

### 1. Requirements & Scale Math
* **Traffic:** 100M emails/day ($\approx 1,200/\text{sec}$ avg; $10,000/\text{sec}$ peak).
* **Core Problem:** Protecting IP reputation from spam blacklisting.

### 2. The Big Architectural Decisions

#### Decision A: IP Pool Bulkhead Isolation
* Split outbound SMTP traffic across physically isolated IP pools:
  * **Transactional IP Pool:** Dedicated, warmed IPs strictly reserved for password resets, order receipts, and 2FA emails. High sender reputation ($> 99\%$).
  * **Marketing IP Pool:** Separate shared IP pools for promotional newsletters. If a customer sends spam, only the marketing IP gets blacklisted; password reset emails continue arriving in inboxes reliably.

#### Decision B: Asynchronous Bounce & Feedback Loops
* Ingest SMTP delivery status events asynchronously via webhooks from receiving mail servers (Gmail, Outlook).
* Process hard bounces (invalid email addresses) and spam complaints through Kafka.
* Instantly write offending emails to a global **Suppression List** table; all future outgoing emails to those addresses are automatically blocked before calling SMTP.

---

## Challenge 8: The Alarm Clock for Code (Delayed Distributed Job Queue)

### 1. Requirements & Scale Math
* **Traffic:** 50M tasks/day; 1-second firing accuracy; crash resilience.

### 2. The Big Architectural Decisions

#### Decision A: Delay Mechanism (Redis Sorted Set vs. DB Polling)
* **DB Polling (`WHERE run_at <= NOW()`):** Degrades disk IOPS under frequent polling.
* **Redis Sorted Set (`ZADD` / `ZRANGEBYSCORE`) — RECOMMENDED:**
  * Schedule job: `ZADD delayed_jobs <execution_unix_timestamp> <job_id>`.
  * Dispatcher poll loop: Every 500ms, run:
    ```bash
    ZRANGEBYSCORE delayed_jobs -inf <current_unix_timestamp> LIMIT 0 100
    ```
  * Atomic Pop via Lua script moves jobs from the Sorted Set to active execution queues (AWS SQS / RabbitMQ).

#### Decision B: Worker Crash Recovery (Visibility Timeouts)
* When Worker A picks up a job, the broker sets a **Visibility Timeout** (e.g., 30 seconds).
* If Worker A processes the job successfully, it sends an explicit `ACK` to delete the job.
* If Worker A crashes or freezes, the visibility timer expires; the job becomes visible again and another healthy worker automatically picks it up and retries.

---

## Challenge 9: The Mind Reader (Real-Time Search Autocomplete)

### 1. Requirements & Scale Math
* **Traffic:** 2 Billion autocomplete requests/day ($23,000\text{ QPS}$ avg; $80,000\text{ QPS}$ peak).
* **Latency SLA:** $< 15\text{ milliseconds}$.

### 2. The Big Architectural Decisions

#### Decision A: Core Data Structure (In-Memory Trie with Pre-Computed Top 5)
* A standard prefix tree (Trie) requires traversing child nodes and ranking completions at runtime, which is too slow ($> 50\text{ms}$).
* **The Optimization:** Store the **Top 5 most popular completions directly inside each Trie node**:
  ```
  Node ['l']   -> top_5: ["laptop", "lego", "login", "linkedin", "lamps"]
    |
  Node ['a'] -> top_5: ["laptop", "lamps", "lava", "laser", "laptop stand"]
    |
  Node ['p'] -> top_5: ["laptop", "laptop stand", "laptop bag", "laptop case"]
  ```
* When the user types `"lap"`, locate the `'p'` node in $O(L)$ time ($3\text{ hops} \approx 0.05\text{ms}$) and return the pre-stored list immediately!

#### Decision B: Offline Rebuild Pipeline
* Never update the live Trie in RAM on every individual search!
* **Offline Aggregation:** Stream search queries into Kafka. Run an hourly Spark/MapReduce job to aggregate search term frequency.
* Build a fresh Trie snapshot in batch, serialize it, and hot-swap it into serving memory without interrupting live traffic.

---

## Challenge 10: The Flight Black Box (Centralized Logging & Telemetry)

### 1. Requirements & Scale Math
* **Fleet:** 10,000 container pods emitting 200,000 logs/sec continuous ($100\text{ MB/sec} = 800\text{ Mbps}$).
* **Retention:** Hot search = 7 days; Cold archive = 1 year.

### 2. The Big Architectural Decisions

#### Decision A: Zero Application Overhead Logging
* Application code writes structured JSON logs strictly to **standard output (`stdout`)**.
* A lightweight host daemon (e.g., **Vector or Fluentbit**) reads from the local container socket asynchronously, batches logs in memory, and compresses them.
* Application worker threads never make remote HTTP calls and are never blocked by logging infrastructure.

#### Decision B: Backpressure Absorption (Kafka Buffer)
* Fluentbit streams logs to a distributed **Apache Kafka cluster** (30–50 partitions).
* If the search indexing cluster (OpenSearch/Elasticsearch) slows down during high load, logs accumulate safely on Kafka's sequential disk buffers without crashing web applications.

#### Decision C: Storage Lifecycle Tiering
* **Hot Tier (Days 0–7):** OpenSearch cluster with NVMe SSDs for instant grep and stack trace searches.
* **Cold Tier (Days 8–365):** Ingest workers micro-batch logs from Kafka, convert them to compressed columnar **Apache Parquet files**, and write directly to **Amazon S3**.
* Engineers query cold historical logs using **AWS Athena / Presto** with zero cluster maintenance costs.
