# Search Systems: The Textbook Index & Change Data Capture

---

## Mental Model: The Index at the Back of a Textbook

Imagine you are studying for a biology exam and need to find every mention of the word **"Mitochondria"** in an 800-page textbook:
* **The SQL `LIKE '%mitochondria%'` Way:** You open page 1 and read every single word with your finger. You finish page 1, turn to page 2, and read every word. Doing this for 800 pages takes **6 hours** (**Full Table Scan**).
* **The Inverted Index Way (Elasticsearch / OpenSearch):** You flip to the very back of the textbook to the **Alphabetical Index**:
  * You find **"M"** $\to$ **"Mitochondria"**.
  * It says: `Pages: 14, 82, 305`.
  * You look it up in **3 seconds**!

```
NORMAL DATABASE (Rows -> Words):
Row 101: "The quick brown fox jumps"
Row 102: "A brown dog sits"

INVERTED INDEX (Words -> Rows):
"brown" -> [ Row 101, Row 102 ]
"fox"   -> [ Row 101 ]
"dog"   -> [ Row 102 ]

Search Query: "brown fox"
Just do a quick mathematical intersection:
[ 101, 102 ] ∩ [ 101 ] = [ Row 101 ] (Done in 0.5 milliseconds!)
```

---

## Why Databases Are Terrible at Search

If you try to build a search bar using a relational database with `WHERE description LIKE '%running shoes%'`:
1. **The Leading Wildcard Trap:** Because of the `%` at the beginning, standard B+ Tree database indexes are **completely ignored**. The database must inspect every single byte of text on disk across every row in the table.
2. **Databases don't speak human:** If a user searches for `"run sneaker"`, a database query for `"running shoes"` will return **zero results**! Databases do exact character matching; they don't know that "running" and "run" are the same word.
3. **No Relevance Scoring:** A database gives you a dumb Yes or No. It can't tell you which of 5,000 matching products is the *best* match.

---

## How a Real Search Engine Works: The 3 Steps

Before text goes into an Inverted Index, it passes through an **Analyzer**:

1. **Tokenization:** Breaks the sentence into individual words:  
   `"Apple MacBook Pro!"` $\to$ `["Apple", "MacBook", "Pro"]`
2. **Normalization & Stemming:**
   * Makes everything lowercase (`"apple"`).
   * Strips useless filler words like `"the"`, `"a"`, `"is"` (**Stop Words**).
   * Chops words down to their root form using linguistics (**Stemming**):  
     `"running"`, `"runs"`, `"ran"` $\to$ **`"run"`**
3. **BM25 Relevance Scoring:**
   * If a word is rare across the whole catalog (like `"quantum"`), documents with that word get a huge score boost.
   * If a word matches in the short **Title**, it gets ranked higher than if it was buried on paragraph 12 of the product description.

---

## The Big Architecture Rule: Never "Dual-Write" in Application Code!

When someone adds a new product, how does it get into both Postgres (for money transactions) and Elasticsearch (for search)?

```
THE AMATEUR TRAP (Dual-Writing in Web App):
[ Web App ] ---> (1) Save to Postgres (Success!)
            ---> (2) Save to Elasticsearch (Network drops! Fails!)
* Result: Your database has the product, but search NEVER finds it. They are out of sync forever!

THE PRODUCTION STANDARD (Change Data Capture - CDC):
[ Web App ] ---> (1) Save to PostgreSQL (Single Source of Truth)
                         |
                   (Database WAL Commit Log)
                         v
             [ Debezium / CDC Engine ]
                         |
                         v
             [ Kafka Search Event Topic ]
                         |
                         v
             [ Elasticsearch Indexer Worker ]
                         |
                         v
             [ Elasticsearch Cluster ]
```

* **Why this is bulletproof:** The web app only writes to Postgres. If Elasticsearch is having a bad day or restarting, updates simply wait safely in Kafka. When Elasticsearch comes back, it catches right back up!

---

## Practice: SQL LIKE vs. DB Index vs. Search Engine

> **Which tool is right for the job?**  
> Pick: `SQL Exact Index`, `Postgres Full-Text (tsvector)`, or `Elasticsearch Cluster`.

1. **User Login by Email:** Finding a user record where `email = 'user@gmail.com'`.
2. **E-Commerce Search Bar:** A customer types `"cheep blak runing shoe"` (typos, multiple attributes, sorted by rating).
3. **Company Internal Wiki (20,000 articles):** Searching for article titles starting with a specific department tag.

---

## 60-Second Summary

> "Databases store rows that contain words; search engines invert that relationship, mapping individual words directly to document IDs like the index at the back of a textbook. Through tokenization, stemming (reducing words to roots), and BM25 relevance scoring, search engines deliver instant fuzzy search results. In production, never write to both a database and a search engine from your web servers; write to your primary transactional database as the single source of truth, and stream updates asynchronously to your search cluster using Change Data Capture and Kafka."
