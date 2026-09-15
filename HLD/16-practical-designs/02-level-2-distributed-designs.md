# Practical System Designs: Level 2 Distributed Infrastructure

> **Level 2 Philosophy:** Now we step up to **asynchronous event pipelines, high-throughput ingestion, and distributed coordination**.  
> Approach each design using the **13-Step Architectural Recipe**. Focus on failure modes, consumer lag, and high availability.

---

## Challenge 6: The City Megaphone (Universal Notification Platform)

### The Real-World Scenario
You are building the centralized notification engine for an Uber or Amazon. Multiple internal services call your API to send Push Notifications (iOS APNs, Android FCM), SMS texts, and in-app alerts to users worldwide.

### The Numbers:
* **Scale:** 50 Million notifications per day (~600/sec average; peak 5,000/sec during breaking news).
* **Two Classes of Traffic:**
  * **Critical:** Two-Factor Auth (2FA) SMS codes and fraud alerts (Must arrive in $< 5\text{ seconds}$).
  * **Bulk:** Promotional marketing sales (Can wait up to 2 hours).

### The Big Decisions You Must Make:
* **The Priority Lane:** If an e-commerce marketing campaign blasts 10 million promotional push notifications at 10:00 AM, how do you make sure a user waiting for a 2FA login text isn't stuck behind 10 million marketing messages?
* **User Preferences & Rate Limiting:** Where do you check: *"Does User A have Push Notifications turned off?"* and *"Don't send more than 3 marketing messages per day to any single user"*?
* **Vendor Flakiness:** Third-party telecom providers (Twilio, Vonage, Apple APNs) go down or rate-limit you. How do you automatically fail over to an alternate SMS provider?

---

## Challenge 7: The Digital Post Office (High-Scale Transactional Email)

### The Real-World Scenario
You are building a SendGrid or Mailgun clone. Businesses send order receipts, password resets, and account updates through your API. You must deliver millions of emails to Gmail, Yahoo, and Outlook without getting marked as spam.

### The Numbers:
* **Scale:** 100 Million emails per day (~1,200/sec average; peak 10,000/sec).
* **The Spam Trap:** If one scammer signs up and sends 50,000 phishing emails from your server's IP address, Gmail will blacklist your entire IP pool, and legitimate password reset emails for millions of other customers will go straight to the Spam folder!

### The Big Decisions You Must Make:
* **IP Pool Isolation (Bulkhead):** How do you physically separate the IP addresses used for high-risk promotional marketing from the clean, dedicated IP addresses used for mission-critical password resets?
* **Bounce & Unsubscribe Feedback Loops:** How do you asynchronously process bounce-back emails and automatically blacklist dead email addresses to keep your sender reputation high?

---

## Challenge 8: The Alarm Clock for Code (Delayed Distributed Job Queue)

### The Real-World Scenario
Design an asynchronous background task scheduler. Developers submit tasks with execution instructions:
* *"Run this immediately."*
* *"Run this in exactly 4 hours."* (e.g., Send abandoned cart reminder email).
* *"Run this every Monday at 9:00 AM."* (Recurring cron).

### The Numbers:
* **Scale:** 50 Million tasks scheduled per day.
* **Accuracy:** Delayed jobs must fire within **1 second** of their scheduled time.
* **Worker Crashes:** If a worker machine running Job #101 crashes halfway through execution, the job must not vanish into thin air; another healthy worker must pick it up and retry it.

### The Big Decisions You Must Make:
* **How to implement the delay?** Do you poll a database table `WHERE run_at <= NOW()` (which melts the database at scale!), or use a **Redis Sorted Set (`ZADD`)** ordered by Unix timestamp, or a **Timing Wheel**?
* **Visibility Timeouts:** When Worker A picks up a job, how long does the broker hide that job from other workers? What happens if the job takes longer than expected?

---

## Challenge 9: The Mind Reader (Real-Time Search Autocomplete)

### The Real-World Scenario
As a user types into a search box, the system returns the top 5 most popular search suggestions matching that prefix within **15 milliseconds** (e.g., typing `"lap"` suggests: `"laptop"`, `"laptop stand"`, `"laptop bag"`).

### The Numbers:
* **Query Traffic:** 500 Million searches a day $\times$ 4 keystrokes per search = **2 Billion autocomplete requests per day** (~23,000 QPS average; peak **80,000 QPS**).
* **Latency SLA:** Suggestions must return in $< 15\text{ms}$!

### The Big Decisions You Must Make:
* **Which Data Structure?** An in-memory **Trie (Prefix Tree)** vs. an Inverted Index Prefix (Edge N-gram) vs. a Redis Sorted Set.
* **Pre-Computing the Top 5:** Calculating the top 5 most popular completions at runtime while the user types is too slow. Can you store the pre-computed Top 5 suggestions directly inside each Trie node?
* **The Offline Rebuild Pipeline:** How do you update search popularity? Do you update the live Trie on every keystroke (which will crash your memory!), or do you aggregate search counts with Kafka/MapReduce and rebuild the Trie offline every night?

---

## Challenge 10: The Flight Black Box (Centralized Logging & Telemetry)

### The Real-World Scenario
10,000 microservice containers emit continuous streams of structured JSON logs and metrics. Engineers must search, filter, and alert on error stack traces in real time.

### The Numbers:
* **Fleet:** 10,000 container instances.
* **Ingestion:** 20 log lines per second per container = **200,000 logs every second** continuous ($100\text{ MB/sec}$ continuous ingress $\approx 800\text{ Mbps}$).
* **Retention:** Hot search tier = 7 days; Cold compressed archival tier = 1 year.

### The Big Decisions You Must Make:
* **Getting logs off the box:** Should the application code send HTTP calls to an external logging service (blocking request threads!), or write to standard stdout where a lightweight local agent (Fluentbit/Vector) picks it up asynchronously?
* **Backpressure when the search cluster is full:** If the central Elasticsearch cluster slows down, how do you prevent log buffering from running out of RAM and crashing your production web apps?
* **Storage Tiering:** How do you move 100 Terabytes of logs from expensive NVMe SSD search clusters to dirt-cheap S3 Parquet files after 7 days?

---

## 60-Second Summary

> "Level 2 systems are the backbone of distributed infrastructure. Universal Notifications teach priority queuing and external vendor failover. Transactional Email teaches IP reputation isolation and bounce processing. The Delayed Job Queue teaches timing wheels and visibility leasing. Search Autocomplete teaches in-memory Tries and offline batch pre-computation. And Centralized Logging teaches high-throughput telemetry ingestion, buffering, and tiered storage lifecycles. Once you can architect these five systems, you are ready for any Staff-level interview scenario."
