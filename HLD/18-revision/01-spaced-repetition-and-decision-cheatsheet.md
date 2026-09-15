# The Pocket Cheatsheet: If-This-Then-That Architecture Rules

> **Purpose:** Keep this page bookmarked. When you have a system design interview or an architecture review in 15 minutes, read this single page.  
> **Rule:** Zero fluff, zero academic lectures. Pure practical engineering intuition.

---

## 1. The 7 Golden Rules of Architecture

1. **The Ingress Rule:** The fastest request is the one that never leaves the user's phone (browser cache); the second fastest is the one served from the nearest city kiosk (CDN edge).
2. **The Rental Car Rule:** Treat servers like rental cars, not family pets. Never save session state or files on a web server's local hard drive. Keep compute stateless!
3. **The Storage Rule:** Never store images, videos, or big PDFs in an expensive SQL database. Heavy files go to S3; only the short URL string goes in the database!
4. **The Index Rule:** Databases map Rows $\to$ Words. Search engines invert that and map Words $\to$ Rows. Never use `LIKE '%term%'` in SQL for user search bars!
5. **The Walkie-Talkie Rule:** Every synchronous HTTP call between microservices multiplies your chance of failure. Use asynchronous message queues to absorb spikes and decouple systems.
6. **The Elevator Rule:** Every async consumer and retry loop MUST be idempotent. Tapping the button 10 times should never charge a customer 10 times!
7. **The Lake Depth Rule:** Never look at "average" latency. A man can drown in a lake with an average depth of 3 feet. Always design for the **p99 tail**!

---

## 2. The Universal If-This-Then-That Decision Table

| IF your system has this problem... | THEN choose this tool... | BECAUSE... |
|---|---|---|
| Database CPU is at 90% due to read queries | **Read Replicas** + **Redis Cache** | Offloads reads from the primary DB; keeps the top 20% hot data in RAM. |
| Write volume exceeds 5,000–10,000 writes/sec | **Cassandra / ScyllaDB** or **Sharding** | Append-only LSM-Trees turn random writes into fast sequential disk appends. |
| Users need to upload 500MB videos | **Direct-to-S3 Pre-Signed URLs** | Files stream directly from browser to S3; your app server CPU/RAM is never touched! |
| Complex multi-service transaction (Flight + Hotel) | **Saga with Compensating Actions** | Distributed 2-Phase Commit freezes under network lag; Sagas undo steps gracefully. |
| A downstream service is slow or timing out | **Circuit Breaker** + **Jittered Backoff** | Fails fast to save caller threads; jittered retries prevent thundering herd retry storms. |
| Users need fuzzy text search with typos | **CDC (Debezium) $\to$ Kafka $\to$ Elasticsearch** | Postgres remains the transactional source of truth; Elasticsearch does inverted index search. |
| User updates profile but sees old picture on reload | **Read-Your-Own-Writes Routing** | Routes that specific user to read from the Primary DB for 5 seconds after a write. |
| A viral product page cache expires (Stampede) | **Distributed Mutex Lock (`SETNX`)** | Only 1 worker queries the database to warm the cache; everyone else waits 50ms. |
| Background workers can't keep up with Kafka | **Add Partitions to Topic**, then scale pods | Active workers in a group cannot exceed partition count; more partitions = more workers! |
| Database connection pool is maxed out at 100% | **Connection Pooler (PgBouncer)** | Keeps a fixed warm pool of DB connections and multiplexes thousands of app threads. |

---

## 3. The 5-Minute Spaced Recall Quiz

Can you answer these 6 questions without peeking?
1. *How many requests per second is 10 Million requests per day?*  
   $\to$ **~120 QPS** (Remember: $1\text{M/day} \approx 12\text{ QPS}$).
2. *Why do we DELETE a cache key on write instead of updating it?*  
   $\to$ **To avoid concurrency race conditions where an older update overwrites a newer one.**
3. *What is the difference between Replication and Sharding?*  
   $\to$ **Replication copies the same data for safety and read capacity; Sharding splits data into pieces across machines for write capacity.**
4. *What happens if you have 30 Kafka consumer pods on a topic with only 10 partitions?*  
   $\to$ **10 pods read; 20 pods sit completely idle!**
5. *What is a Circuit Breaker?*  
   $\to$ **A safety fuse that stops calling a dying dependency so it can recover, failing fast upstream.**
6. *Why do we add random Jitter to cache TTLs?*  
   $\to$ **To prevent a Cache Avalanche where thousands of keys expire at the exact same midnight second.**
