# Databases & Storage: SQL, NoSQL & How Disks Actually Work

---

## Mental Model: The Library vs. The Quick Notebook

Choosing a database isn't about what's trendy. It comes down to **how you plan to read and write your data on physical disks**.

There are two main ways storage engines organize data on hard drives:

### 1. B+ Trees (Traditional SQL: Postgres, MySQL)
* **Analogy:** A giant public library where every single book is kept in strict alphabetical order on the shelves.
* **Reading is fast ($O(\log N)$):** You want the book *"Harry Potter"*? You walk straight to the 'H' aisle, find the shelf, and grab it. Point lookups and range scans (`WHERE age BETWEEN 20 AND 30`) are super fast.
* **Writing is slow:** What happens when a new book arrives and the shelf is full? The librarian has to physically shift books across 5 shelves to make room (**Random Disk I/O & Page Splits**).

### 2. LSM-Trees (Write-Heavy NoSQL: Cassandra, ScyllaDB, RocksDB)
* **Analogy:** A busy doctor scribbling notes on a desk pad.
* **Writing is blazing fast:** When a patient arrives, the doctor just writes on the next blank line of the notepad in front of them (**Append-Only Sequential Write**). They don't walk over to the filing cabinet every second.
* **Cleaning up in the background:** When the desk pad fills up, an assistant copies the notes neatly into sorted folders in the filing cabinet (**Compaction**).
* **Reading takes a bit more work:** To find a patient's history, you might have to check the active desk pad, then check the latest folder, and maybe an older folder.

```
+-------------------------------------------------------------------------------+
|                      HOW DISKS ACTUALLY PREFER TO WORK                        |
+-------------------------------------------------------------------------------+
|  B+ Trees (SQL)           : Great for Reads & Complex Joins.                  |
|                             Slower for massive write floods.                  |
+-------------------------------------------------------------------------------+
|  LSM-Trees (Append NoSQL) : Blazing fast for Writes (IoT, Logs, Sensor data). |
|                             Reads have to check multiple files on disk.       |
+-------------------------------------------------------------------------------+
```

---

## The Big Four NoSQL Flavors Explained Simply

If you don't use relational SQL, you usually pick one of these 4 tools based on your access pattern:

1. **Key-Value (Redis, DynamoDB):**
   * *Mental Model:* A giant wall of hotel room lockboxes. You give the key number (`user:101`), you get the box.
   * *Best For:* User sessions, shopping carts, caching. Sub-millisecond lookups.
2. **Document Store (MongoDB, Couchbase):**
   * *Mental Model:* A folder of paper resumes or JSON files. Each person's folder can have different information inside (some have degrees, some have certifications).
   * *Best For:* Product catalogs, blog posts, user profiles where each item has different attributes.
3. **Wide-Column Store (Cassandra, ScyllaDB):**
   * *Mental Model:* A giant spreadsheet partitioned by row key and sorted by timestamp.
   * *Best For:* IoT sensor pings, financial tick trades, chat message history. Absorbs 100,000 writes/sec without breaking a sweat.
4. **Graph Database (Neo4j):**
   * *Mental Model:* A corkboard with pushpins connected by strings.
   * *Best For:* Social networks (*"Friends of friends who like this movie"*), fraud rings.

---

## Replication vs. Partitioning (Never Confuse These Two!)

This is the #1 question senior interviewers use to test candidates:

| Concept | The Everyday Analogy | Why Do We Do It? | Does it help with Writes? |
|---|---|---|---|
| **Replication** | Photocopying the entire phonebook 3 times and giving copies to 3 coworkers. | **Safety & High Availability.** If one copy gets wet, you have 2 backups. Also, 3 people can look up numbers at the same time. | **NO!** In primary-replica setups, all writes still hit the primary copy. |
| **Partitioning (Sharding)** | Tearing the phonebook in half: A–M in Volume 1, N–Z in Volume 2. | **Scale.** The book is too heavy for one shelf, or too many people are trying to write in it at once. | **YES!** Writes for 'Alice' go to Volume 1, writes for 'Zack' go to Volume 2. |

```
REPLICATION (Same data copied):          SHARDING (Data split into chunks):
[ Server 1 ] holds [ A, B, C, D ]        [ Shard 1 ] holds [ A, B ]
[ Server 2 ] holds [ A, B, C, D ]        [ Shard 2 ] holds [ C, D ]
```

---

## The Sharding Pitfall: The Celebrity (Hot Shard) Problem

When you shard a database, you pick a **Shard Key** to decide which server holds which data:
$$\text{Server Number} = \text{Hash}(\text{Shard Key}) \pmod{\text{Total Servers}}$$

* **A Good Shard Key:** High cardinality, evenly distributed (e.g., random `UUID` or `account_id`).
* **A Bad Shard Key:**
  * If you shard an e-commerce database by `country_code`, the `US` shard gets 75% of all traffic and melts, while the `Iceland` shard sits at 0.1% CPU.
  * If you shard a social network by `user_id`, a celebrity with 80 million followers lives on Server #3. Whenever that celebrity posts a picture, Server #3's CPU and disk IOPS spike to 100%, taking down Server #3 while the other 30 shards are bored.

---

## Replication Lag: The "Where Did My Profile Picture Go?" Bug

In a database with Read Replicas:
1. You change your profile picture to a cute cat photo.
2. The browser sends `POST /profile`, which writes to the **Primary Database**.
3. The Primary commits the change and responds *"Saved!"*
4. Your browser instantly reloads the page.
5. The read request hits a **Read Replica** that is 500 milliseconds behind in copying the Primary's log.
6. The replica returns your old photo. You think the website is broken and click Save 5 more times.

### The Fix: Read-Your-Own-Writes
For 5 seconds after a user updates their data, route that specific user's read queries directly to the **Primary Database** (or return the data from local memory). Let all other users read from the replicas.

---

## When To Choose What

* **Default to PostgreSQL / MySQL when:**
  * You need transactions (e-commerce checkout, financial balances).
  * You need relational joins and clean schemas.
  * Total database size is under 2–3 Terabytes (a modern SSD handles this effortlessly on a single server with read replicas).
* **Choose NoSQL when:**
  * Your write volume exceeds 5,000–10,000 writes/second.
  * Your dataset is tens of terabytes or petabytes (exceeds single disk limits).
  * Your query pattern is simple: you always look up data by the same primary key.

---

## Common Traps to Avoid

* ❌ **"We'll use Mongo because we don't know our schema yet."** (You still have a schema; you just pushed the job of checking it into messy application code!).
* ❌ **Doing JOINs across sharded databases.** (Joining two tables that live on physically different machines over a network takes seconds and kills performance).
* ❌ **Adding Read Replicas when writes are the problem.** (Replicas only help with read queries; every replica actually increases write replication traffic!).

---

## Practice: Which Database Would You Pick?

> **For each scenario, pick one:** `Relational SQL`, `Key-Value (Redis)`, `Document (Mongo)`, `Wide-Column (Cassandra)`, or `Graph (Neo4j)`. Explain your choice in 2 simple sentences!

### Workload 1: User Wallet & Bank Balance
Users deposit money, transfer funds to friends, and withdraw to bank accounts. Zero balance mistakes allowed.

### Workload 2: Electric Scooter GPS Telemetry
50,000 electric rental scooters stream their GPS coordinates, battery level, and speed every 3 seconds ($16,000\text{ writes/sec}$). Queries are always: *"Show ride history for Scooter X between 2:00 PM and 2:30 PM."*

### Workload 3: E-Commerce Product Catalog
10 million items for sale. Shoes have sizes and colors; laptops have RAM and CPU specs; books have authors and page counts. When a shopper opens a product page, the entire product description is displayed at once.

### Workload 4: Session Tokens
You need to verify user login tokens on 50,000 API calls per second. The operation is: given a random 64-character token, return the `user_id` in under 1 millisecond.

### Workload 5: Fraud Detection in Banking
Analyzing financial transactions across thousands of shell companies to detect loops where Company A sends money to B, B sends to C, and C sends it back to A.

---

## 60-Second Summary

> "Databases are designed around physical disk storage and access patterns. Relational SQL databases use B+ Trees to deliver safe ACID transactions and flexible multi-table joins, but hit limits when write volume saturates disk IOPS. NoSQL engines trade relational joins for scale: Key-Value stores offer sub-millisecond point lookups, Document stores group related nested data into cohesive JSON documents, and Wide-Column stores use append-only LSM-Trees to absorb massive write floods. Remember: replication gives you backup copies and read capacity; sharding splits your dataset when it's too big for one box."
