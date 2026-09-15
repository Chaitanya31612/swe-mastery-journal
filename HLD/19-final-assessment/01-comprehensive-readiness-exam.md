# The Capstone Readiness Exam: Are You Ready for Alex Xu? (Phase 18)

> **Welcome to the Capstone Challenge!**  
> This isn't a stressful university exam; think of this like a scrimmage game before the championship.  
> **Goal:** Test your intuitive mental model across all the core concepts we've built together. If you can answer these conversationally, you are 100% ready to master Alex Xu's *System Design Interview* books and walk into senior interviews with swagger.

---

## Part A: Rapid-Fire Recall (20 Questions)

*Answer in 1 or 2 quick sentences off the top of your head:*
1. What is the difference between latency (how long you wait) and throughput (how much work gets done)?
2. What is the simple formula for a quorum committee ($W, R, N$)?
3. Why does 1 Million requests per day equal about 12 QPS?
4. What does a Layer 4 load balancer look at vs. a Layer 7 load balancer?
5. Why should you always DELETE a cache key on write instead of updating it?
6. Can you have 20 active consumer workers reading from a Kafka topic with 8 partitions? What happens to the other 12 workers?
7. In simple words, what is the difference between Replication and Sharding?
8. Why are LSM-Trees so much faster at writes than B+ Trees?
9. What is a Dead-Letter Queue (DLQ), and what kind of messages get sent there?
10. What is an Error Budget, and what happens when your team burns through all of it?
11. Why is checking average latency dangerous for finding slow user experiences?
12. What is a Cache Stampede, and what stops 50,000 requests from hitting the database at once?
13. How does the Token Bucket algorithm allow bursts while still capping average rate?
14. What is the Outbox Pattern, and why do we use it instead of writing to Postgres and Kafka in the same API handler?
15. What is the difference between a Kubernetes Liveness probe and a Readiness probe?
16. Why can an API call from New York to Tokyo never take less than ~70 milliseconds, no matter how much money you spend?
17. What is an Inverted Index, and how is it like the index at the back of a textbook?
18. What is the difference between At-Least-Once delivery and At-Most-Once delivery?
19. What is the Bulkhead pattern, and how is it like watertight doors on a submarine?
20. Why should users upload large video files directly to S3 using pre-signed URLs instead of through your web servers?

---

## Part B: Concept Showdown (10 Quick Comparisons)

*Explain the fundamental difference and trade-off in 2 sentences for each pair:*
1. **Redis vs. PostgreSQL**
2. **SQL (Relational) vs. NoSQL (Wide-Column / Key-Value)**
3. **Point-to-Point Queue (SQS) vs. Publish/Subscribe (SNS)**
4. **Database Replication vs. Database Sharding**
5. **Synchronous REST vs. Asynchronous Event-Driven Queues**
6. **In-Memory Cache (Redis) vs. Content Delivery Network (CDN Edge)**
7. **Stateless Compute vs. Stateful Sticky Sessions**
8. **Fan-Out on Write (Push) vs. Fan-Out on Read (Pull)**
9. **Two-Phase Commit (2PC) vs. Saga with Compensating Actions**
10. **p50 Latency vs. p99 Latency**

---

## Part C: Napkin Math (5 Real Calculations)

*Grab a scratchpad and do the quick math:*

1. **Daily QPS:** A photo app has 30 Million daily users. Each user views 40 photos and uploads 2 photos per day. Calculate average Read QPS, peak Read QPS ($3\times$), average Write QPS, and peak Write QPS.
2. **Storage Growth:** An IoT fleet ingests 100 Million sensor pings a day. Each ping is 200 bytes. With $3\times$ replication copies, how much disk space is consumed in 1 year?
3. **Network Pipe:** A streaming app serves 50 Million video segments a day. Each segment is 4 MB. Calculate the outbound network bandwidth needed in Gigabits per second (Gbps).
4. **Cache Sizing:** You get 200 GB of read queries per day. Applying the 80/20 rule, how much RAM do you need in your Redis cluster?
5. **Autoscaling Pods:** One container pod can comfortably handle 250 requests/sec. If peak traffic hits 8,000 QPS, how many pods should your cluster run?

---

## Part D: Production Firefighting (5 Scenarios)

*You are the lead on-call engineer. What happened, and how do you stop the bleeding?*

1. **The Domino Crash:** Service A calls Service B with a 30-second timeout. Service B slows down to 25 seconds. What happens to Service A's worker threads? What safety fuse halts the cascade?
2. **The 4-Node Split-Brain:** A 4-node database cluster is split evenly across two datacenters (2 nodes in NY, 2 nodes in London). The ocean cable cuts. Both sides elect a leader and accept customer writes. What went wrong, and how does an odd-numbered quorum prevent it?
3. **The Midnight Avalanche:** Exactly at midnight, 500,000 product cache keys expire simultaneously. The database CPU spikes to 100% and stays there. What caused this, and what simple trick fixes it forever?
4. **The Deadlock Kafka Topic:** 10 worker pods are reading from a Kafka topic with 10 partitions. Messages are piling up by 50,000 a minute. You scale the worker fleet to 50 pods, but queue lag keeps growing just as fast. Why?
5. **The Unindexed Big Delete:** An engineer runs `DELETE FROM audit_logs WHERE date < '2025-01-01'` on a 100-million row table in the middle of Tuesday afternoon. All production API calls grind to a halt. What happened physically inside the database?

---

## Part E: Mini-Designs (3 Quick Napkin Sketches)

*Outline a quick 5-bullet design for each (FR, NFR, Data Model, Core Path, Scaling):*

1. **One-Time Secret Sharing (Privnote Clone):** A user enters an API key or password and generates a secret link. Once opened, the secret is permanently erased from memory and disk forever.
2. **Live Sports Scoreboard:** Push live World Cup soccer scores to 10 million concurrent mobile app users with $< 1\text{ second}$ latency.
3. **Webhook Dispatcher:** Take internal order events and reliably deliver them to third-party merchant URLs with automatic retries, exponential backoff, and deduplication.

---

## Part F: 60-Second Verbal Elevator Pitches (10 Concepts)

*In 2–3 crisp, confident sentences, explain each concept as if answering an engineering director:*
1. What is System Design?
2. Why do we need Cache-Aside?
3. What is Backpressure?
4. What is Idempotency?
5. Why are Averages misleading in monitoring?
6. What is the difference between Availability and Durability?
7. What is Database Sharding?
8. What is a Circuit Breaker?
9. What is Zero Trust security?
10. What is the Saga pattern?

---

## The Verdict: When Are You Ready for Alex Xu?

Once you work through these questions, we will evaluate your responses:
* **Score $\ge 85\%$:** 🟢 **READY FOR ALEX XU & INTERVIEWS.** You have an intuitive, defensible mental model. You can open Alex Xu's books and breeze through the case studies with genuine understanding.
* **Score $< 85\%$:** 🟡 **QUICK GAP REFRESH.** We'll target the 1 or 2 specific building blocks that feel fuzzy and sharpen them together!
