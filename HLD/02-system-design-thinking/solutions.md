# System Design Mental Model: Comprehensive Solutions & Explanations (Phase 1)

This document provides in-depth architectural solutions and trade-off analyses for the Self-Check and 10 Real Scenarios in [`01-system-design-mental-model.md`](./01-system-design-mental-model.md).

---

## Part A: Self-Check Solutions

### 1. The Low-CPU Slow-API Mystery
**Question:** If your API is slow (e.g., taking 3,000ms), but CPU and RAM are both under 20%, what are three possible things the server is waiting for?

**Solutions & Explanations:**
1. **Database Lock Contention & Connection Pool Starvation:**
   * The application thread has been scheduled by the OS, but it is stuck in a blocked state waiting for a database connection from a saturated pool (e.g., HikariCP or SQLAlchemy connection pool at 100% utilization).
   * Alternatively, the SQL query has executed, but is waiting to acquire an exclusive row-level lock (`SELECT ... FOR UPDATE`) held by another long-running transaction. The CPU does zero work while blocked on I/O.
2. **Blocking Synchronous Third-Party Network Calls:**
   * The application code is making an outbound HTTP/gRPC request to an external payment provider, fraud service, or shipping API (e.g., Stripe, Twilio, or internal microservices). If the remote endpoint takes 2,800ms to respond, your server thread sits idle in a network socket `read()` system call.
3. **Thread Synchronization / Distributed Mutex Contention:**
   * Multiple worker threads are serialized behind an internal application lock (e.g., synchronized block, thread mutex, or distributed Redis lock). Threads spend 99% of their lifespan waiting for lock acquisition rather than executing machine instructions.

---

### 2. The Danger of "100% Consistency and 100% Availability Across Cities"
**Question:** Why is it dangerous to promise "100% Consistency and 100% Availability across multiple cities"?

**Solutions & Explanations:**
* **The Physics Constraint (CAP Theorem & Network Partitions):**
  * Multiple cities are connected by public internet backbones or undersea fiber. Inevitably, backhoes cut fiber cables, routers misconfigure BGP routes, or trans-oceanic cables suffer packet loss. A **network partition ($P$) is a physical certainty**, not an optional configuration.
* **The Inescapable Dilemma:**
  * When the network partition occurs between City A (New York) and City B (London), a user in London attempts to write new data.
  * If you choose **Consistency ($C$)**, City B must wait for City A to acknowledge the write. Since the network link is severed, City B cannot reach City A and must reject or fail the request $\to$ **You lose Availability ($A$)**.
  * If you choose **Availability ($A$)**, City B accepts the write locally and acknowledges success to the user. But now City A does not have this data, and clients reading in City A will see stale or conflicting data $\to$ **You lose Consistency ($C$)**.
  * Anyone promising 100% of both is ignoring the speed of light and physical networking failure modes.

---

### 3. Latency vs. Throughput
**Question:** What is the difference between how long one request takes (Latency) and how many requests the server can complete in a second (Throughput)?

**Solutions & Explanations:**
* **Latency:** The elapsed wall-clock duration required to complete a single unit of work from the perspective of the requester (measured in milliseconds or microseconds). Formula:
  $$\text{Latency} = T_{\text{finish}} - T_{\text{start}}$$
* **Throughput:** The total volume of completed work units processed by the system per unit of time (measured in Requests Per Second [RPS] or Queries Per Second [QPS]). Formula:
  $$\text{Throughput} = \frac{\text{Completed Work Units}}{\Delta t}$$
* **The Analogy:**
  * A Formula 1 race car travels at 220 mph (ultra-low latency), but only transports 1 passenger (low throughput).
  * A 100-car freight train moves at 35 mph (high latency), but transports 10,000 tons of cargo simultaneously (astronomical throughput). In system design, batching increases throughput at the expense of per-request latency.

---

### 4. E-Commerce Flash Sale: Consistency vs. Availability
**Question:** If you have an e-commerce flash sale, which force is more important: stopping people from buying out-of-stock items (Consistency) or letting everyone click around fast (Availability)?

**Solutions & Explanations:**
* **Decision:** **Strict Consistency** on the final inventory deduction; high availability on product viewing.
* **Explanation:**
  * If you prioritize Availability for checkout, multiple nodes accept "Buy" requests for items that do not exist, causing massive **overselling**. Overselling 10,000 PlayStation 5 consoles during a flash sale triggers legal liability, payment gateway refund fees, customer outrage, and customer service gridlock.
  * For checkout, systems must **Fail Closed** using atomic inventory locks or single-partition event streams. It is acceptable for 95% of users to receive an explicit "Sorry, item is in another cart / Sold out" message (controlled unavailability) rather than silently corrupting inventory.

---

## Part B: Practice — 10 Real Scenarios ("What Matters Most Here?")

### Scenario 1: Stock Brokerage Order Execution (Robinhood / E*Trade)
*A user clicks "Buy 10 shares of Apple at Market Price".*

1. **Top 2 Non-Negotiables:**
   * **Durability:** Every accepted order must be immutably recorded to non-volatile storage. Lost orders mean regulatory fines and direct financial liability.
   * **Consistency (ACID & Correctness):** Account cash balances and stock holdings must reconcile to the penny. No double-spending or phantom shares allowed.
2. **What We Can Relax:**
   * **Availability (Fail Closed):** If the connection to the clearinghouse or market maker is degraded, the brokerage must halt trading and reject orders rather than execute market orders with uncertain prices.
   * **Sub-Millisecond Latency:** While high-frequency trading (HFT) firms operate in microseconds, retail investors are fully served by 100ms–300ms execution latency.
3. **Architecture Implications:**
   * Relational SQL engine with strict ACID transactions (PostgreSQL / CockroachDB).
   * Double-entry bookkeeping ledger architecture.
   * Message streaming with idempotent consumers to prevent duplicate executions.

---

### Scenario 2: Video Streaming (Netflix Movie Playback)
*A user presses Play on Stranger Things on their TV on a Friday night.*

1. **Top 2 Non-Negotiables:**
   * **Availability:** If a user clicks play and receives an error screen on Friday night, they cancel their subscription and switch to YouTube or HBO.
   * **Low Latency (Time-To-First-Frame):** Video playback must start in $< 500\text{ms}$ with zero mid-stream buffering.
2. **What We Can Relax:**
   * **Strong Consistency:** If the subtitle sync metadata or view-progress bookmark lags by 5 seconds, nobody cares.
   * **Durability of Analytics:** If one heartbeat tracking that the user reached minute 42:15 is lost over UDP, the user experience is unharmed.
3. **Architecture Implications:**
   * Content Delivery Networks (CDNs) deployed at ISP edge locations (Netflix Open Connect).
   * Adaptive Bitrate Streaming (HLS/DASH) chunking video into 2–4 second immutable static TS/MP4 files.
   * Eventual consistency for bookmarking and watch histories.

---

### Scenario 3: Real-Time Collaborative Document (Google Docs)
*Three coworkers are editing the same meeting notes at the exact same second from different laptops.*

1. **Top 2 Non-Negotiables:**
   * **Local Responsiveness (Ultra-Low Latency):** When typing a character, it must appear on the local screen immediately ($< 10\text{ms}$). Any input lag makes typing impossible.
   * **Durability:** Typed words and revision history must never be lost once acknowledged.
2. **What We Can Relax:**
   * **Immediate Global Strong Consistency:** Collaborators do not need to see each other's keystrokes in identical lock-step order instantaneously.
3. **Architecture Implications:**
   * **Conflict-Free Replicated Data Types (CRDTs)** or **Operational Transformation (OT)**.
   * Edits are applied immediately to local client state and broadcast asynchronously over WebSockets to peers for convergence.

---

### Scenario 4: Hospital ICU Patient Vital Signs
*A bedside monitor tracks a heart attack patient's pulse and sends it to the central nurses' station.*

1. **Top 2 Non-Negotiables:**
   * **High Reliability / Fault Tolerance:** The communication path cannot drop critical cardiac arrest or flatline alarms.
   * **Bounded Low Latency:** Vital metric telemetry and anomaly alarms must reach medical personnel in $< 1\text{ second}$.
2. **What We Can Relax:**
   * **Global Multi-Region Cloud Replication:** ICU telemetry is confined to the local hospital building network (LAN). There is zero need to replicate high-frequency raw ECG waves across continents.
   * **Long-Term Full-Fidelity Durability:** 60Hz raw waveforms can be aggregated or discarded after 24–48 hours; only clinical summaries and critical alarm events need 7-year storage.
3. **Architecture Implications:**
   * Local edge gateways running on redundant, on-premise industrial hardware.
   * Dedicated isolated VLANs with QoS priority for medical telemetry.
   * Fail-safe audible alarms directly at the physical bedside monitor if network connectivity drops.

---

### Scenario 5: Concert Ticket Flash Sale (Ticketmaster / Taylor Swift)
*100,000 stadium seats go on sale at 10:00 AM. 3 million fans are refreshing the screen trying to claim the same front-row seats.*

1. **Top 2 Non-Negotiables:**
   * **Consistency (Zero Double-Booking):** Under no circumstances can two fans receive confirmed tickets for Seat Section 101, Row A, Seat 4.
   * **Durability:** Once payment clears and the reservation is locked, the ticket ownership must be permanently committed.
2. **What We Can Relax:**
   * **General Availability:** 97% of fans will not get a ticket. Placing incoming users into a virtual waiting room (queueing) and rejecting excess write requests is the correct architectural choice.
3. **Architecture Implications:**
   * Virtual Waiting Room / Token Bucket queue (e.g., Cloudflare Waiting Room) to throttle ingress traffic to match database capacity.
   * Distributed reservation locks with a 5-minute lease (e.g., Redis Redlock or database row locks).
   * Strict relational transaction boundaries on seat reservation tables.

---

### Scenario 6: Ride-Share Driver Location Updates (Uber Driver App)
*5 million active drivers transmit their current GPS coordinates every 4 seconds.*

1. **Top 2 Non-Negotiables:**
   * **High Ingestion Throughput:** The system must comfortably ingest and process $> 1.25\text{ Million}$ GPS pings per second continuous.
   * **Low Latency / Freshness:** The rider matching engine requires the driver's location from the last few seconds, not 2 minutes ago.
2. **What We Can Relax:**
   * **Durability of Intermediate Points:** If a driver's GPS ping from 8 seconds ago is lost in transit, it is immediately superseded by the fresh ping arriving now. Writing every single 4-second ping to persistent disk is an expensive anti-pattern.
   * **Global Strong Consistency:** Drivers in London do not interact with riders in San Francisco; spatial sharding eliminates cross-region coordination.
3. **Architecture Implications:**
   * In-memory geospatial indexing (e.g., Uber H3, Redis Geospatial `GEOADD`, or specialized in-memory spatial indexes).
   * Append-only streaming ingress (Kafka) for billing and route reconstruction, separated from real-time dispatch state.

---

### Scenario 7: Bank Transaction Audit Log
*A regulatory legal compliance vault that records every bank deposit, wire, and withdrawal for the next 7 years.*

1. **Top 2 Non-Negotiables:**
   * **Durability (WORM — Write Once, Read Many):** Data must be tamper-proof, immutable, and preserved across hardware failures, natural disasters, and software bugs for the statutory retention period.
   * **Strict Consistency:** Audited transactions must be cryptographically verifiable and match ledger balance movements.
2. **What We Can Relax:**
   * **Read Latency:** Compliance auditors run queries infrequently. Waiting 5 minutes or 2 hours for a historical audit report to query cold storage is completely acceptable.
   * **Immediate Availability:** If the audit archival pipeline lags by 30 minutes, it creates zero operational impact on customer-facing banking.
3. **Architecture Implications:**
   * Immutable append-only audit tables with cryptographic hash chaining (Merkle trees or ledger databases like Amazon QLDB).
   * Lifecycle policies streaming settled records to AWS S3 Glacier Deep Archive with Object Lock (compliance retention mode).

---

### Scenario 8: 1-on-1 Direct Chat (WhatsApp / Signal)
*You send your friend a text message: "Hey, are you free for lunch?"*

1. **Top 2 Non-Negotiables:**
   * **Low Latency (Interactive Real-Time Delivery):** When both users are online, messages must be delivered and displayed in $< 100\text{ms}$.
   * **Reliability / Durability:** Messages must never vanish into thin air. If the recipient is offline, the message must be stored safely until they reconnect.
2. **What We Can Relax:**
   * **Global Consistency Across Chats:** Chat #1 between Alice and Bob has zero dependency on Chat #2 between Charlie and Dave. There is no global order needed across different conversations.
3. **Architecture Implications:**
   * Persistent bi-directional connections (WebSockets or long-lived TCP sockets managed by Erlang/Elixir or Go connection gateways).
   * **Store-and-Forward Pattern:** If the recipient connection is dead, store the encrypted payload in a persistent queue/database; push to Apple APNs/FCM and deliver on reconnection.

---

### Scenario 9: Competitive First-Person Shooter Game (Valorant / Call of Duty)
*Two players turn a corner and shoot at each other at almost the exact same millisecond.*

1. **Top 2 Non-Negotiables:**
   * **Ultra-Low Latency ($< 20\text{ms}$):** In a 64-tick or 128-tick game engine, packet delivery and processing must be deterministic and instantaneous.
   * **Real-Time Consistency & Fairness (Authoritative State):** The server must be the single source of truth for collision detection and hit registration to prevent cheating and desync.
2. **What We Can Relax:**
   * **Durability:** Player positional packets update 60–128 times every second. They exist purely in server RAM. Writing mouse movements to disk or database would immediately collapse the game engine.
   * **TCP Reliability:** Packets use UDP. If an individual positional update packet is dropped, retransmitting it is useless because the player has already moved; the next packet contains newer coordinates.
3. **Architecture Implications:**
   * Dedicated game server instances running in memory.
   * Low-overhead UDP packet protocols with client-side prediction and server-side lag compensation.

---

### Scenario 10: Web Search Engine (Google Search)
*A user types "weather today" into the search bar.*

1. **Top 2 Non-Negotiables:**
   * **Ultra-Low Latency ($< 200\text{ms}$):** Users treat search as an extension of their train of thought; any perceptible delay degrades engagement.
   * **High Availability ($99.999\%$):** Search must always return a result page, even under datacenter failures or traffic spikes.
2. **What We Can Relax:**
   * **Strong Consistency:** If a new webpage was published 20 seconds ago, it does not need to appear in search results immediately.
   * **Uniformity Across Users:** If Alice and Bob see slightly different rankings or snippet summaries due to localized index caches, system correctness is preserved. Eventual consistency is the core design principle of web search.
3. **Architecture Implications:**
   * Pre-computed inverted indexes partitioned across massive distributed clusters.
   * Multi-tiered caching (result cache, snippet cache, posting list cache).
   * Asynchronous web crawlers and index pipelines decoupled from query-serving clusters.
