# Search Systems & Indexing: Comprehensive Solutions & Technology Selection (Phase 10)

This document provides deep technical rationales, data structure evaluations, and architectural trade-offs for the 3 Practice Scenarios in [`01-search-systems-and-indexing-pipelines.md`](./01-search-systems-and-indexing-pipelines.md).

---

## Decision Matrix: SQL Index vs. Postgres Full-Text vs. Elasticsearch

| Scenario | Recommended Tool | Core Data Structure | Why This Specific Tool |
|---|---|---|---|
| **1. User Login by Email** | **SQL Exact Index (B-Tree)** | B+ Tree | Exact point lookup; $O(\log N)$ time; sub-millisecond execution; enforces uniqueness |
| **2. E-Commerce Search Bar** | **Elasticsearch / OpenSearch Cluster** | Inverted Index + FST (Finite State Transducers) | Fuzzy typo tolerance, BM25 relevance scoring, multi-attribute filtering at scale |
| **3. Company Internal Wiki** | **Postgres Full-Text (`tsvector` + GIN)** | Generalized Inverted Index (GIN) | Modest scale (20k docs); zero extra infrastructure; ACID consistency with wiki edits |

---

## Detailed Technical Rationales

### 1. User Login by Email (`WHERE email = 'user@gmail.com'`)
* **Selected Tool:** **SQL Exact Index (Standard B-Tree Index).**
* **Why B-Tree Index is the Perfect Fit:**
  * Authentication requires an exact, binary byte-for-byte match on a string.
  * In PostgreSQL or MySQL:
    ```sql
    CREATE UNIQUE INDEX idx_users_email ON users(email);
    ```
  * A B-Tree index keeps keys in balanced sorted order. Finding `user@gmail.com` in a table of 100 million users takes $\approx 3\text{ to }4$ disk page reads:
    $$O(\log_B N) < 1\text{ millisecond}$$
* **Why Elasticsearch is an Anti-Pattern Here:**
  * Elasticsearch analyzes strings by breaking them into lowercase tokens. An email string would be tokenized into `["user", "gmail", "com"]`, creating unnecessary indexing overhead.
  * More dangerously, search clusters are **eventually consistent** (with a default 1-second refresh interval). If a user registers their account and immediately tries to log in, querying Elasticsearch might fail to find the user due to indexing lag.

---

### 2. E-Commerce Search Bar ("cheep blak runing shoe")
* **Selected Tool:** **Elasticsearch / OpenSearch Cluster.**
* **Why Traditional SQL (Even with Indexes) Fails:**
  * **The Query:** The customer entered multiple misspellings (`cheep` instead of cheap, `blak` instead of black, `runing` instead of running).
  * Running a SQL `WHERE description LIKE '%cheep%'` requires a **full-table scan** over 10 million products, running for 15 seconds and melting the database.
  * Even if the SQL query did run, it would return **0 results** because neither "cheep" nor "blak" exists verbatim in the product catalog!
* **Why Elasticsearch Excels:**
  1. **Fuzzy String Matching (Levenshtein Edit Distance):**
     * Automatically corrects `blak` $\to$ `black` (edit distance 1) and `runing` $\to$ `running` (edit distance 1).
  2. **Stemming & Lemmatization (Snowball / Porter Stemmer):**
     * Reduces words to linguistic roots: `running`, `runs`, `runner` all map to the root token `run`.
  3. **BM25 Relevance Scoring:**
     * Evaluates term frequency and inverse document frequency. Products where "running" and "shoe" both appear in the title score higher than products where they appear in fine-print warranties.
  4. **Multi-Field Boosting:**
     * Boosts results where matched terms match the `title` field by $3\times$ compared to the `description` field.
* **The Architecture:**
  * PostgreSQL remains the single source of truth.
  * Database changes are streamed asynchronously into Elasticsearch via **Change Data Capture (Debezium + Kafka)**, preserving database performance while keeping search results fresh within 500ms.

---

### 3. Company Internal Wiki (20,000 Articles with Department Tags)
* **Selected Tool:** **PostgreSQL Full-Text Search (`tsvector` + GIN Index).**
* **Why Postgres Full-Text is the Ideal Pragmatic Choice:**
  * **The Scale:** 20,000 documents is a **tiny dataset** in system design terms. 20,000 articles of text easily fit into a few hundred megabytes of RAM.
  * **Zero Operational Overhead:**
    * Spinning up an Elasticsearch cluster requires dedicated JVM tuning, master node election, memory management, and cross-system sync pipelines (Kafka + CDC).
    * For 20,000 internal articles, managing a separate search infrastructure is massive over-engineering.
  * **How It Works in Postgres:**
    1. Create a generated column with language tokenization and a Generalized Inverted Index (GIN):
       ```sql
       ALTER TABLE wiki_articles 
       ADD COLUMN text_search tsvector 
       GENERATED ALWAYS AS (to_tsvector('english', title || ' ' || body)) STORED;

       CREATE INDEX idx_wiki_search ON wiki_articles USING GIN(text_search);
       ```
    2. Query with prefix and Boolean matching:
       ```sql
       SELECT title, ts_rank(text_search, query) AS rank
       FROM wiki_articles, to_tsquery('english', 'engineering:* & deployment') query
       WHERE text_search @@ query
       ORDER BY rank DESC;
       ```
  * **The Huge Benefit:** Immediate Strong Consistency! The moment an engineer edits a wiki page and clicks "Save", their changes are searchable **0 milliseconds later** within the same database transaction.
