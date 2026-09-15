# Core Architectural Patterns: The 16 LEGO Blocks of System Design

---

## Mental Model: The Architect's LEGO Box

Nobody designs a massive distributed system completely from scratch. 

Master architects assemble systems out of **proven, standardized building blocks**. Just like building a house with bricks, beams, and windows, you solve distributed constraints by snapping together these 16 core blueprints:

$$\mathbf{\text{Specific Headache} \longrightarrow \text{Proven Blueprint} \longrightarrow \text{Predictable Trade-off}}$$

Let's break down all 16 patterns with zero academic fluff:

---

### 1. Layered (N-Tier) Architecture
* **The Headache:** Spaghetti code where your HTML templates are running raw SQL queries directly.
* **The Blueprint:** Divide your code into clean floors: Presentation (UI) $\to$ Business Logic $\to$ Database Access.
* **The Catch:** Adds a bit of boilerplate code for simple operations.
* **Everyday Example:** Traditional Spring Boot, Django, or Rails apps.

---

### 2. Stateless Compute Fleet
* **The Headache:** You can't add more web servers because user sessions are saved on Server 1's local hard drive.
* **The Blueprint:** Treat servers like rental cars. Move all sessions to Redis and all files to S3. Any server can crash without affecting any user.
* **The Catch:** Adds a tiny 1ms network hop to fetch the session from Redis on each click.
* **Everyday Example:** Containerized web apps on Kubernetes or AWS ECS.

---

### 3. Cache-Aside (Lazy Loading)
* **The Headache:** Read queries are melting your database disk.
* **The Blueprint:** Keep the 20% most popular data in Redis (on your desk). If it's not on your desk, fetch it from the database and copy it over. On database write, delete the cache key.
* **The Catch:** The very first read takes an extra millisecond (cache miss).
* **Everyday Example:** Twitter/X profile and tweet caching.

---

### 4. Read Replicas (Primary-Replica DB)
* **The Headache:** 95% of your database traffic is read queries, pushing CPU to 90%.
* **The Blueprint:** All writes go to the Primary DB. Replicate data asynchronously to 3 Read Replicas. Route all user read queries to the replicas.
* **The Catch:** Replication Lag: a user updates their name and might see their old name for 500ms on a lagging replica.
* **Everyday Example:** GitHub's massive MySQL database fleet.

---

### 5. Database Sharding (Horizontal Partitioning)
* **The Headache:** Your dataset is 10 Terabytes, which is too big for a single machine's disk, or write volume exceeds single-disk write IOPS.
* **The Blueprint:** Split the dataset into pieces across 10 separate database servers using a Shard Key (e.g., `user_id % 10`).
* **The Catch:** You can no longer easily do SQL `JOIN`s across tables on different shards!
* **Everyday Example:** Slack sharding data by Workspace/Team ID.

---

### 6. Event-Driven Architecture (EDA)
* **The Headache:** Service A calls Service B, which calls Service C. If Service C is slow, the entire website freezes.
* **The Blueprint:** Services don't call each other directly; they announce events over a message bus: *"Order #101 was placed!"*. Other services listen and react on their own time.
* **The Catch:** Tracing bugs across multiple decoupled services requires good distributed tracing.
* **Everyday Example:** Uber ride events: `DriverDispatched`, `RideStarted`, `RideCompleted`.

---

### 7. Asynchronous Worker Queue
* **The Headache:** Generating a monthly PDF invoice takes 15 seconds. If done inside an HTTP handler, the user's browser times out.
* **The Blueprint:** The web server writes an order ticket to a queue (like SQS) and immediately tells the browser *"Working on it!"*. Dedicated background workers pull and process tasks.
* **The Catch:** The user interface needs to show a spinner or send a push notification when the job finishes.
* **Everyday Example:** YouTube processing video resolutions after an upload.

---

### 8. Pub/Sub (Publish / Subscribe) Fan-Out
* **The Headache:** When an order is placed, 5 different services (Shipping, Billing, Inventory, Fraud, Marketing) all need to know about it.
* **The Blueprint:** The publisher broadcasts one message to a Topic. The broker automatically duplicates and delivers a copy to every subscriber's private queue.
* **The Catch:** Multiplies message storage and network traffic by the number of subscribers.
* **Everyday Example:** Amazon checkout notifying Shipping, Inventory, and Billing simultaneously.

---

### 9. CQRS (Command Query Responsibility Segregation)
* **The Headache:** Your write model needs strict normalized tables for financial safety, but your search screen needs messy denormalized views across 6 tables.
* **The Blueprint:** Split the Write Model (Commands $\to$ PostgreSQL) from the Read Model (Queries $\to$ Elasticsearch). Asynchronously sync changes between them.
* **The Catch:** High complexity; read models lag behind writes by a few hundred milliseconds.
* **Everyday Example:** Airbnb: hosts write listing updates to SQL; guests search listings from an optimized search index.

---

### 10. Event Sourcing
* **The Headache:** Traditional databases overwrite data (`UPDATE account SET balance = 50`). If a bug happens, you have no record of how the balance got there.
* **The Blueprint:** Never update or delete rows. Record every state change as an immutable history: `Deposited $100`, `Withdrew $50`. The current balance is calculated by adding up the history.
* **The Catch:** Replaying 100,000 events to find current state is slow; requires periodic **Snapshots**.
* **Everyday Example:** Banking ledgers, Git commit history.

---

### 11. Saga Pattern (Distributed Transactions)
* **The Headache:** A booking spans 3 independent microservices: Flight, Hotel, and Car Rental. You cannot use a database transaction across 3 separate company databases.
* **The Blueprint:** Execute a chain of local transactions. If Step 3 (Car Rental) fails, the Saga runs **Compensating Transactions** backwards to undo the Hotel and Flight reservations!
* **The Catch:** Writing compensation logic for every step takes time and careful testing.
* **Everyday Example:** Vacation booking packages (Expedia / Booking.com).

---

### 12. API Gateway Pattern
* **The Headache:** A mobile app has to make 20 separate network calls to 20 different microservices, draining the phone battery over slow mobile networks.
* **The Blueprint:** Place a single receptionist at the front door. The mobile app makes one call to the API Gateway; the Gateway fans out internal calls over high-speed datacenter fiber and returns a clean combined response.
* **The Catch:** The Gateway can become a bottleneck if not scaled properly.
* **Everyday Example:** Netflix Zuul / Envoy routing millions of smart TV devices.

---

### 13. CDN Edge Architecture
* **The Headache:** Users in Australia trying to load images from a server in Virginia wait 400ms on every picture.
* **The Blueprint:** Put edge servers in Sydney, Tokyo, London, and New York that cache static assets within 5 miles of users.
* **The Catch:** Invalidation delay: when you update a website CSS file, you need to use cache-busting hashes (`style.a8f2.css`) so users don't see old designs.
* **Everyday Example:** Cloudflare / CloudFront serving static media for Reddit, Discord, and Spotify.

---

### 14. Object-Storage Media Architecture
* **The Headache:** Uploading 500MB video files through Python/Node.js web servers exhausts server memory and connections.
* **The Blueprint:** Give the user a temporary **Pre-Signed S3 URL**. The user's browser streams the file directly to Amazon S3. The app server only saves the URL in the database.
* **The Catch:** S3 is eventually consistent on bucket listings; files cannot be modified in place.
* **Everyday Example:** Instagram photo uploads, Google Drive file uploads.

---

### 15. Search Indexing Pipeline
* **The Headache:** SQL queries with `LIKE '%term%'` cause full table scans that freeze your database.
* **The Blueprint:** Write to PostgreSQL as your transactional source of truth. Use Change Data Capture (CDC via Debezium) to stream updates through Kafka into Elasticsearch for instant full-text search.
* **The Catch:** Newly added items appear in search results with a ~500ms delay.
* **Everyday Example:** Amazon product catalog search.

---

### 16. Fan-Out on Write (Push) vs. Fan-Out on Read (Pull)
* **The Headache:** Generating a personalized social media home feed for users who follow hundreds of accounts.
* **The Blueprint (The Hybrid Fix):**
  * **Push for normal users:** When someone with 200 followers posts, background workers push the post directly into their 200 followers' pre-baked feed caches (Instant reads!).
  * **Pull for celebrities:** When a celebrity with 80 million followers posts, do NOT push to 80 million feeds! Keep their post in a separate box and merge it dynamically when a follower opens their app.
* **The Catch:** Requires maintaining two separate feed generation codepaths.
* **Everyday Example:** The Twitter / X Home Timeline.

---

## 60-Second Summary

> "Architectural patterns are standardized solutions to recurring distributed systems challenges. We use Cache-Aside and Read Replicas to scale read-heavy databases, and Sharding when a single disk cannot hold the volume. In microservices, we eliminate brittle synchronous calls by using Event-Driven Pub/Sub with worker queues, coordinate multi-service flows using Sagas with compensating actions, and protect our perimeter using API Gateways and Edge CDNs. You don't need to invent new architectures; you just need to know which of these 16 proven blueprints solves your exact bottleneck."
