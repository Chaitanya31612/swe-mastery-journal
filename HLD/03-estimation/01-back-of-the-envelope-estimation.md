# Back-of-the-Envelope Estimation: The Engineer's Reality Check

---

## Mental Model: Packing a Suitcase

Imagine you're packing for a 4-day trip:

* Do you weigh every sock on a scientific laboratory scale down to the milligram? **Of course not.**
* You just ask: *"Will this fit in a carry-on backpack, or do I need to check a 50-pound giant suitcase?"*

Back-of-the-envelope estimation is **packing for your software system**:

* You don't care whether you need 41.3 servers or 42.1 servers.
* You only care about the big question: **"Can one normal server handle this, or will we need a cluster of 50 machines?"**
* If you have 200 requests a day, one tiny $5 server will sleep 99% of the time.
* If you have 500 million requests a day, a single machine will catch fire in 2 seconds.

```
                  [ The Golden Question ]
                             |
             "Can ONE normal machine handle this?"
                            / \
                          /     \
                       (YES)    (NO)
                        /         \
                       v           v
           [ Keep it simple! ]   [ Okay, where does it break first? ]
           - 1 App Server        - CPU? (Too many calculations)
           - 1 Postgres DB       - RAM? (Dataset too big for memory)
           - Done for today!     - Disk? (Running out of hard drive space)
                                 - Network? (Saturating the bandwidth pipe)
```

---

## Why It Exists

Engineers without estimation skills do one of two silly things:

1. **Under-engineering (The Crash):** They build a photo upload service using a single Postgres database. 100,000 users upload photos on launch day. The database hard drive fills up in 3 hours, and the app crashes.
2. **Over-engineering (The Money Pit):** They spend 4 months setting up Kubernetes, Kafka, Cassandra, and Redis for a service that gets 10 requests a minute. They burn $2,000 a month on cloud bills to do the work a 2012 MacBook could do in its sleep.

Estimation takes **2 minutes with a pencil** and saves you months of wasted engineering.

---

## How It Works: The 3 Magic Numbers You Need to Remember

Forget memorizing complex formulas. You only need these three quick tricks in your head:

### 1. The "Seconds in a Day" Trick

There are 24 hours in a day $\times$ 60 minutes $\times$ 60 seconds = **86,400 seconds**.

* In an interview or on a napkin, round 86,400 to **100,000** ($10^5$). It makes mental division effortless!

$$
\mathbf{1\text{ Million requests per day} \approx \frac{1,000,000}{100,000} \approx 10\text{ to }12\text{ requests per second (QPS)}}
$$

Keep this tiny table in your head:

* **1 Million / day** $\approx$ **12 QPS**
* **10 Million / day** $\approx$ **120 QPS**
* **100 Million / day** $\approx$ **1,200 QPS**
* **1 Billion / day** $\approx$ **12,000 QPS**

> 💡 **Aha Moment!** A standard web framework (Go, Node.js, Java) can easily handle **1,000 to 5,000 simple requests per second on a single machine**. That means if your app gets 10 million requests a day (120 QPS), a single decent server can handle the traffic!

---

### 2. Peak Traffic: The "Lunchtime Rush" Rule

People don't use apps evenly at 3:00 AM and 1:00 PM. Traffic comes in waves.

* **Rule of thumb:** Multiply average traffic by **2x to 3x** to find your peak.
* *Example:* If average traffic is 1,000 QPS, design your system to handle **2,500 to 3,000 QPS** so it doesn't crash when everyone opens the app during lunch.

---

### 3. Data Sizes: How Big is a Thing?

| Thing                    | Approximate Size        | How to Picture It                |
| ------------------------ | ----------------------- | -------------------------------- |
| User ID (UUID) or number | ~8 to 36 bytes          | A postage stamp                  |
| One line of text / tweet | ~200 to 500 bytes       | A sticky note                    |
| User Profile row in SQL  | ~1 KB ($1,000$ bytes) | A single sheet of paper          |
| Compressed Web Image     | ~200 KB to 1 MB         | A Polaroid photo                 |
| 1 Minute of 1080p Video  | ~20 MB to 50 MB         | A small video clip on your phone |

And how the units stack up (each step is 1,000x bigger):

* **1,000 Bytes** = **1 KB** (Kilobyte)
* **1,000 KB** = **1 MB** (Megabyte)
* **1,000 MB** = **1 GB** (Gigabyte — a stick of RAM)
* **1,000 GB** = **1 TB** (Terabyte — a laptop hard drive)
* **1,000 TB** = **1 PB** (Petabyte — a room full of server racks)

---

## Step-by-Step Example: Let's Estimate a Photo App (Like Instagram)

Let's do a real calculation together without sweating:

* **Scale:** 10 Million Daily Active Users (DAU).
* Each user views **20 photos a day**.
* Each user uploads **1 photo a day**.
* Photo size = **500 KB**.

### Step 1: How many requests per second (QPS)?

* **Writes (Uploads):**

  * $10\text{ Million photos/day} \div 86,400 \approx \mathbf{120\text{ uploads/second}}$.
  * Peak ($3\times$): $\mathbf{360\text{ uploads/second}}$.
* **Reads (Views):**

  * $10\text{M users} \times 20\text{ views} = 200\text{ Million views/day}$.
  * $200\text{ Million} \div 86,400 \approx \mathbf{2,400\text{ views/second}}$.
  * Peak ($3\times$): $\mathbf{7,200\text{ views/second}}$.
* **What this tells us:** Our system is **20x more read-heavy than write-heavy**! We should focus heavily on caching reads.

### Step 2: How much disk space do we need?

* 10 Million photos uploaded per day $\times$ 500 KB per photo = **5,000,000 MB per day**.
* Convert to GB: $5,000,000 \text{ MB} \div 1,000 = \mathbf{5,000\text{ GB (5 TB) per day}}$.
* Over 1 year: $5\text{ TB} \times 365 \approx \mathbf{1,800\text{ TB (1.8 Petabytes) a year}}$.
* With 3 copies for safety (Replication): $1.8\text{ PB} \times 3 \approx \mathbf{5.4\text{ PB a year}}$.
* **What this tells us:** We CANNOT store these photos in a regular database! A database holding 5 Petabytes will collapse. We **must** store photos in Cloud Object Storage (like AWS S3) and only keep the short URL in our database.

### Step 3: Network Pipe (Bandwidth)

* Viewers fetch 2,400 photos every second.
* $2,400 \text{ photos/sec} \times 500 \text{ KB} = 1,200,000 \text{ KB/sec} \approx \mathbf{1.2\text{ GB per second}}$.
* Convert Bytes to bits ($1\text{ Byte} = 8\text{ bits}$): $1.2 \times 8 \approx \mathbf{9.6\text{ Gigabits per second (Gbps)}}$.
* **What this tells us:** A single datacenter network card (usually 1 Gbps to 10 Gbps) would be maxed out just serving photos! We **must** put a Content Delivery Network (CDN) in front to serve photos from edge servers near users.

Look at what we learned in 3 minutes:

1. We need caching for the 20:1 read ratio.
2. We need S3 for the 5 Petabytes of storage.
3. We need a CDN so our origin servers don't choke on bandwidth.

---

## When To Use It

* **In the first 5 minutes of any system design interview:** It shows the interviewer you build things based on reality, not guesswork.
* **Before signing cloud infrastructure contracts:** Knowing your storage and egress upfront prevents a $50,000 surprise bill from Amazon.

---

## When Not To Use It

* **Don't do long division on a whiteboard:** Nobody cares if the answer is 11.57 QPS or 12 QPS. Round to 12. If an interviewer stops you to correct a decimal point, they are missing the point of engineering.

---

## Common Traps to Avoid

* ❌ **The "Bits vs. Bytes" Trap:** Storage is measured in **Bytes** (Capital B), but network speed is measured in **bits** (lowercase b). Remember: $8\text{ bits} = 1\text{ Byte}$. (A 1 Gbps network can only move 125 MB per second!).
* ❌ **Designing for Average and Crashing at Peak:** If an average is 500 QPS, but peak is 2,500 QPS, your app will crash every day at 12:30 PM.
* ❌ **Forgetting Copies (Replication):** If you calculate 10 TB of data, remember you need at least 3 copies across different datacenters, so you're buying 30 TB.

---

## Practice: 7 Progressively Harder Exercises

> **Try these out on a piece of paper!**For each one, figure out:
>
> 1. Average QPS & Peak QPS
> 2. Daily & 3-Year Storage
> 3. Network Bandwidth (Ingress/Egress)
> 4. Where will it break first? (CPU, RAM, Disk, or Network?)

### Exercise 1: Basic SaaS Web App (1M DAU)

* 1 Million daily users.
* Each user does 30 reads (10 KB each) and 2 writes (2 KB each) per day.
* Keep data for 3 years.

### Exercise 2: Medium Social Feed (10M DAU)

* 10 Million daily users.
* Each user loads their feed 15 times/day (50 KB per load) and posts 2 times/day (1 KB text).
* Keep data for 5 years.

### Exercise 3: Microblogging Platform (100M DAU)

* 100 Million daily users.
* Each user reads 40 posts/day and writes 1 post/day (500 bytes).
* Keep data for 5 years.

### Exercise 4: Photo Portfolio Site (Unsplash Clone)

* 5 Million daily users.
* 1 Million new photos uploaded per day (average 2 MB).
* 50 Million photo views per day.

### Exercise 5: Short-Form Video App (TikTok Clone)

* 25 Million daily users.
* 500,000 video clips uploaded per day (average 15 MB).
* Each user watches 40 clips per day.

### Exercise 6: 1-on-1 Chat App (WhatsApp Clone)

* 50 Million daily users.
* Each user sends 40 messages per day (100 bytes text).
* 10% of messages include a picture (300 KB).

### Exercise 7: Centralized Server Log Tracker

* 5,000 servers in your fleet.
* Each server generates 50 log lines every second ($24\times7$).
* Each log line is 500 bytes.
* Keep logs in search index for 30 days, and archive in cold storage for 1 year.

---

## 60-Second Summary

> "Back-of-the-envelope estimation is not a math test; it's a reality check. By turning user numbers into requests per second, storage gigabytes, and network bandwidth, we instantly see whether our system can live on a single server or needs a distributed cluster. We round numbers aggressively—remembering that 1 million requests a day is about 12 per second—because our only goal is order-of-magnitude clarity: finding what breaks first so we can pick the right tools before writing any code."
