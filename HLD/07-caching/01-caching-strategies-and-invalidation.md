# Caching: Keeping Popular Data on Your Desk

---

## Mental Model: Your Desk vs. The Basement Archive

Imagine you're an accountant working in a high-rise office:
* There's a filing cabinet in the **basement** with 500,000 customer folders (**The Database on Disk**).
* Walking down to the basement, unlocking the door, finding the drawer, and carrying the folder upstairs takes **10 minutes** (**Slow Disk & Query Latency**).
* Instead, you keep the **20 folders you use every single day right on your desk** (**The Cache in RAM**).
* When someone asks for Alice's file, you reach over and grab it in **2 seconds** (**Cache Hit**).
* If someone asks for a file you don't have on your desk (**Cache Miss**), you walk down to the basement, fetch it, copy it to your desk, and answer them.

```
                  [ USER READ REQUEST ]
                            |
                            v
              +---------------------------+
              | Is it on your desk (RAM)? |
              +---------------------------+
                     /             \
             (YES: Cache Hit)   (NO: Cache Miss)
                   /                 \
                  v                   v
           [ Done in 1ms! ]   [ Walk to Basement DB (15ms) ]
                                      |
                              [ Copy to your desk ]
                                      |
                              [ Return to user ]
```

The golden rule of caching: **The 80/20 Rule (Pareto Principle). In almost every app, 80% of user traffic views the same 20% of popular items. You don't need to put the whole database in RAM—just the hot 20%!**

---

## Why It Exists

Computer memory speeds have massive differences:
* **Reading from RAM (Redis/Memcached):** ~100 nanoseconds ($< 1\text{ms}$).
* **Reading from a Database SSD:** ~5 to 15 milliseconds (**10,000x slower**).

A single PostgreSQL database server can handle maybe **5,000 to 10,000 queries a second** before its CPU and disk choke.
A single Redis instance can easily handle **100,000 queries a second** per core because it lives entirely in RAM and does no SQL parsing.

Caching protects your database from drowning in repetitive read queries.

---

## The Core Caching Patterns Explained

### 1. Cache-Aside (Lazy Loading) — *The Industry Standard*
1. Your app checks the cache (Redis).
2. If found $\to$ Return data immediately (**Cache Hit**).
3. If not found $\to$ Read from SQL database, write the result into Redis with an expiration timer (TTL), and return to user (**Cache Miss**).
4. **On Write:** When data changes in the database, **delete the key from Redis**.

### 2. Write-Through
The app writes data to the cache, and the cache immediately writes it to the database before telling the user *"Saved!"*.
* *Good:* Cache is never out-of-date.
* *Bad:* Writes are slower because you wait for both cache and database to save.

### 3. Write-Behind (Write-Back) — *Fast but Dangerous!*
The app writes only to the cache and responds *"Saved!"* in 1 millisecond. The cache batches writes and updates the database later in the background.
* *Good:* Blazing fast write speeds.
* *The Danger:* If the server loses power before flushing to the database, **that data is permanently gone!** (Never use this for bank accounts or orders!).

---

## The #1 Caching Secret: Why You DELETE the Cache on Write (Never Update It!)

When someone updates their profile, should your code **Update the cache with the new name**, or **Delete the cache key**?

$$\mathbf{\text{Always DELETE the key. Never update it!}}$$

### Why? The Race Condition Trap:
Imagine two requests happen at the same millisecond:
1. Thread 1 wants to change name to `"Alice"`.
2. Thread 2 wants to change name to `"Bob"`.

* **If you UPDATE the cache:**
  * Thread 1 updates the Database to `"Alice"`.
  * Thread 2 updates the Database to `"Bob"`. (Database correctly says Bob is the winner).
  * But due to network lag, Thread 1's cache update arrives *after* Thread 2's cache update.
  * Now the **Cache says Alice**, but the **Database says Bob**! Your cache is now permanently out-of-sync until someone notices!
* **If you DELETE the cache:**
  * Both Thread 1 and Thread 2 just delete the key.
  * The next time anyone visits the profile, it forces a fresh read from the database, which returns the true winner: `"Bob"`. Problem solved!

---

## The 3 Classic Cache Disasters (And How to Stop Them)

```
[ 1. THE FAKE ID ATTACK ]       [ 2. THE VIRAL EXPOSURE ]       [ 3. MIDNIGHT COLLAPSE ]
Cache Penetration               Cache Stampede / Breakdown      Cache Avalanche
-------------------------       --------------------------      ------------------------
Attacker queries random         A viral product page with       500,000 product keys were
fake IDs: user_id = -9999       100k viewers expires at         written at midnight with
                                12:00:00                        identical 24-hour TTLs
         |                                   |                              |
Every request misses cache!     100,000 queries miss at once!   At 24:00:00, ALL 500k
         |                                   |                  keys expire at once!
All 100k queries hit DB!        All 100k queries hammer DB!     100% of read traffic dumps
Database crashes.               Database CPU hits 100%.         onto the database.
         |                                   |                              |
[ FIX: Bloom Filter or ]        [ FIX: Mutex Lock (`SETNX`) ]   [ FIX: Jitter (Add random ]
[ Cache the "null" result ]     [ Only 1 query allowed to DB ]  [ ±5 min offset to TTLs) ]
```

### 1. Cache Penetration (The Fake ID Attack)
* A hacker writes a script querying non-existent IDs (`/users/-1`, `/users/fake999`).
* The cache doesn't have it, so every single request punches through the cache and forces a full scan on your SQL database.
* **The Fix:**
  * **Cache Null:** If a user ID doesn't exist in the database, save `user:-1 = NULL` in Redis with a 60-second TTL. The next request hits the cache and returns 404 in 1ms!
  * **Bloom Filter:** A tiny bouncer in front of your cache that can instantly tell you: *"This key definitely does not exist in our database, don't even bother looking."*

### 2. Cache Stampede / Thundering Herd (The Viral Product)
* 50,000 people are watching a live flash sale product page.
* The cache key expires at 12:00:00.
* In that exact millisecond, all 50,000 requests get a cache miss and all 50,000 fire the exact same SQL query at the database at the same instant!
* **The Fix: Mutex Lock (`SETNX`):**
  * When a cache miss happens, the first request acquires a temporary lock: *"I'm going to the database to fetch this, everyone else wait 50ms or use the slightly older data."* Only **one** query hits the database.

### 3. Cache Avalanche (The Midnight Crash)
* You cache 100,000 products at midnight with a strict `TTL = 86400 seconds` (24 hours).
* Exactly 24 hours later, all 100,000 keys expire at the exact same second. The cache suddenly empties, and 100% of your site's traffic floods the database.
* **The Fix: Add Jitter!**
  * Never use a flat expiration time. Always add random noise:
    $$\text{TTL} = 24\text{ hours} \pm \text{Random}(1\text{ to }10\text{ minutes})$$
  * Keys will expire gradually across a 20-minute window instead of all at once.

---

## When To Cache

* Read-heavy data (read 10x more than written).
* Heavy, slow calculations (e.g., aggregating monthly spending or user rankings).
* Static data (country lists, store locations, site settings).

---

## When NOT To Cache

* Write-heavy logs or sensor streams where each record is written once and rarely read again. (You'll just waste expensive RAM constantly evicting data).
* Real-time bank balances during a money transfer where reading even a 1-second stale balance could allow an overdraft.

---

## Practice: What's Your Caching Strategy?

> **For each scenario, tell me:**
> 1. Should we cache this?
> 2. Where should it live (Browser, CDN, Redis, or nowhere)?
> 3. What should the TTL be?
> 4. How would you invalidate it?

### Scenario 1: Breaking News Headline Banner
A major news website posts: *"Earthquake in Tokyo"*. 20 million users reload the homepage in the next 15 minutes. Editors might edit the typo in the headline in 3 minutes.

### Scenario 2: User Shopping Cart
A customer is browsing an online clothing store, adding and removing shirts over a 30-minute shopping session.

### Scenario 3: Live Currency Exchange Rates (USD to EUR)
Forex market rates that fluctuate every 250 milliseconds and are used by currency traders to make live financial trades.

---

## 60-Second Summary

> "Caching is keeping popular data on your desk in RAM so you don't have to walk down to the basement database on every single request. Using the 80/20 rule, we cache the top 20% most popular items to absorb over 80% of read traffic. In production, always delete cache keys on write instead of updating them to avoid race conditions. And protect against the big three caching traps: use Bloom filters or null caching for Penetration, mutex locks for Stampedes, and randomized TTL jitter to prevent Avalanches."
