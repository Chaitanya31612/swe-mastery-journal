# Databases & Data Modeling: Comprehensive Solutions & Technology Selection (Phase 5)

This document provides deep technical rationales, data storage engine mechanics, and architectural trade-offs for the 5 Workload Scenarios in [`01-data-modeling-relational-and-nosql.md`](./01-data-modeling-relational-and-nosql.md).

---

## Workload 1: User Wallet & Bank Balance

### 1. Selected Database
**Relational SQL Database (e.g., PostgreSQL, CockroachDB, MySQL InnoDB)**

### 2. Technical Explanation & Architectural Rationale
* **Non-Negotiable Requirement:** Strict ACID Transactions & Zero Balance Drift.
* **Why Relational SQL is the Perfect Fit:**
  * When User A transfers \$50 to User B, two separate account balances must update atomically inside an explicit database transaction (`BEGIN ... COMMIT`).
  * If the server crashes or the network drops after deducting \$50 from User A, the transaction must automatically roll back so the \$50 does not vanish.
  * Relational SQL engines provide **Strong Isolation (Serializable / Read Committed)** and row-level locking (`SELECT ... FOR UPDATE`), preventing concurrent double-spend race conditions.
  * Schema constraints (`CHECK (balance >= 0)`) provide native database-level guarantees against negative balances regardless of application code bugs.
* **Why NoSQL is Dangerous Here:**
  * Most NoSQL databases (like Cassandra or MongoDB without multi-document transactions) provide only single-row/single-document atomicity.
  * Coordinating multi-party fund transfers across distributed NoSQL shards requires complex distributed two-phase locking in application code, which introduces deadlocks, partial failure states, and audit nightmares.

---

## Workload 2: Electric Scooter GPS Telemetry

### 1. Selected Database
**Wide-Column / Time-Series NoSQL Database (e.g., Apache Cassandra, ScyllaDB, TimescaleDB, ClickHouse)**

### 2. Technical Explanation & Architectural Rationale
* **The Scale:** 50,000 scooters $\times$ write every 3 seconds $\approx \mathbf{16,666\text{ writes/second}}$ continuous ($24\times7$).
* **The Query Pattern:** Strictly range-bound: *"Fetch points for `scooter_id = X` between `start_time` and `end_time`"*.
* **Why Wide-Column (LSM-Tree) is the Perfect Fit:**
  * Standard B-Tree SQL databases choke on 16,000 writes/sec because every insert requires random disk I/O to locate and balance B-Tree leaf pages on disk.
  * Cassandra and ScyllaDB use **Log-Structured Merge-Trees (LSM-Trees)**. Incoming telemetry is written sequentially into an in-memory buffer (MemTable) and an append-only commit log with zero disk seek penalty, easily absorbing 100,000+ writes/sec.
  * **Data Modeling:** The table schema uses `scooter_id` as the **Partition Key** and `timestamp` as the **Clustering Key**:
    ```sql
    CREATE TABLE scooter_telemetry (
        scooter_id UUID,
        recorded_at TIMESTAMP,
        latitude DOUBLE,
        longitude DOUBLE,
        battery_pct INT,
        speed FLOAT,
        PRIMARY KEY ((scooter_id), recorded_at)
    ) WITH CLUSTERING ORDER BY (recorded_at ASC);
    ```
  * All points for a specific ride are stored physically contiguous on disk in sorted chronological order. Range queries between 2:00 PM and 2:30 PM execute as a blazing fast single sequential disk read.

---

## Workload 3: E-Commerce Product Catalog

### 1. Selected Database
**Document Store (e.g., MongoDB, AWS DynamoDB) or Relational PostgreSQL with JSONB**

### 2. Technical Explanation & Architectural Rationale
* **The Business Challenge:** Extreme Schema Heterogeneity (Polymorphism).
  * 10 million items with completely different attributes (Shoes have shoe size and sole material; laptops have RAM, CPU, and screen refresh rate; books have ISBN, author, and page count).
* **Why Document Store is the Perfect Fit:**
  * In traditional normalized SQL, modeling 500 different product categories requires either hundreds of sparse columns with 90% NULLs, or an anti-pattern like Entity-Attribute-Value (EAV) tables requiring 15 joins to view a single laptop.
  * In a Document Database, each product is stored as a self-contained, schema-flexible JSON/BSON document:
    ```json
    {
      "_id": "prod_laptop_99",
      "title": "MacBook Pro 16",
      "price": 2499.00,
      "specs": {
        "cpu": "M3 Max",
        "ram_gb": 64,
        "storage_tb": 2
      }
    }
    ```
  * When a customer opens the product page, the entire product payload is retrieved in a single point-read lookup (`_id = prod_laptop_99`) without a single database `JOIN`.
  * *Staff Nuance:* Modern PostgreSQL with `JSONB` columns and GIN indexing can also handle this pattern exceptionally well up to hundreds of gigabytes.

---

## Workload 4: Session Tokens

### 1. Selected Database
**In-Memory Key-Value Store (e.g., Redis, AWS MemoryDB, Memcached)**

### 2. Technical Explanation & Architectural Rationale
* **The Performance SLA:** 50,000 queries per second with $< 1\text{ millisecond}$ response time.
* **The Operation:** Simple Point Lookup: Given a 64-character token string, return the associated `user_id` and role permissions.
* **Why In-Memory Key-Value is the Perfect Fit:**
  * Redis stores its entire dataset in volatile RAM, bypassing physical disk I/O entirely. A primary key point lookup operates in $O(1)$ constant time, taking **100 to 300 microseconds**.
  * Disk-based databases (SQL or Document) would suffer disk read queue congestion trying to serve 50,000 random I/O operations per second.
  * **Native TTL Expiration:** Session tokens expire after a fixed duration (e.g., 24 hours). Redis has native Time-To-Live (TTL) key expiration:
    ```bash
    SET session:a8f93b7c4e... '{"user_id": 42, "role": "admin"}' EX 86400
    ```
  * Redis automatically purges expired tokens in memory, eliminating the need for periodic cleanup cron jobs that lock production database tables.

---

## Workload 5: Fraud Detection in Banking

### 1. Selected Database
**Graph Database (e.g., Neo4j, Amazon Neptune, Memgraph)**

### 2. Technical Explanation & Architectural Rationale
* **The Problem:** Detecting Deep Cyclic Relationships & Multi-Hop Traversal across Shell Companies.
  * Company A sends money to Company B $\to$ Company B sends to Company C $\to$ Company C sends to Company D $\to$ Company D routes funds back to Company A (Money Laundering Round-Tripping).
* **Why Relational SQL and NoSQL Collapse Here:**
  * In SQL, finding a 5-hop relationship requires joining the `transactions` table against itself 5 times (`JOIN ... JOIN ... JOIN ... JOIN ... JOIN`).
  * Self-joins on a table with 500 million transactions cause combinatorial explosion of intermediate results; queries take minutes or hours and crash database memory.
  * In NoSQL key-value or document stores, graph traversal is unsupported and requires fetching thousands of records over the network to reconstruct in application code.
* **Why Graph Databases Excel:**
  * Graph databases implement **Index-Free Adjacency**: each node (Account/Company) holds direct memory pointers to its adjacent edges (Transactions/Transfers).
  * Traversal time is proportional to the size of the immediate subgraph, **not the total size of the database**.
  * Detecting a cycle in Cypher takes milliseconds:
    ```cypher
    MATCH path = (a:Account)-[:TRANSFERRED*3..6]->(a:Account)
    RETURN path LIMIT 10;
    ```
  * Graph algorithms (PageRank, cycle detection, community clustering) run natively in the storage engine, identifying money laundering rings in real time.

---

## Summary Comparison Table

| Workload | Recommended Database | Core Storage Engine | Primary Architectural Reason |
|---|---|---|---|
| **1. User Wallet & Balance** | Relational SQL (Postgres) | B+ Tree | ACID guarantees, row-level locks, zero balance drift |
| **2. Scooter Telemetry** | Wide-Column (Cassandra/Scylla) | LSM-Tree | Ingests 16k+ writes/sec sequentially; fast range scans |
| **3. Product Catalog** | Document (Mongo / DynamoDB) | JSON / BSON Store | Polymorphic schema; atomic single-read document retrieval |
| **4. Session Tokens** | In-Memory Key-Value (Redis) | In-Memory Hash Map | Sub-millisecond $O(1)$ lookups; native TTL expiration |
| **5. Banking Fraud Detection** | Graph Database (Neo4j) | Adjacency List Pointers | Multi-hop cyclic graph traversal; zero relational joins |
