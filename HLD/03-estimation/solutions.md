# Back-of-the-Envelope Estimation: Comprehensive Solutions & Step-by-Step Calculations (Phase 2)

This document provides rigorous, step-by-step mathematical solutions and hardware bottleneck analyses for the 7 exercises in [`01-back-of-the-envelope-estimation.md`](./01-back-of-the-envelope-estimation.md).

---

## 🧮 Standard Estimation Constants

* **Seconds in a Day:** $86,400\text{ s} \approx 10^5\text{ s}$ (100,000 seconds for rapid estimation).
* **The Golden Rule of Scale:**
  $$\mathbf{1\text{ Million requests per day} \approx \frac{1,000,000}{86,400} \approx 11.6 \approx 12\text{ QPS}}$$
* **Peak Traffic Multiplier:** Standard peak is typically assumed to be $2\times$ to $3\times$ average QPS.
* **Storage Units:**
  * $1\text{ KB} = 10^3\text{ bytes}$
  * $1\text{ MB} = 10^6\text{ bytes}$
  * $1\text{ GB} = 10^9\text{ bytes}$
  * $1\text{ TB} = 10^{12}\text{ bytes}$
  * $1\text{ PB} = 10^{15}\text{ bytes}$
* **Network Units:** Bandwidth is measured in **Bits per second** ($1\text{ Byte} = 8\text{ bits}$).

---

## Exercise 1: Basic SaaS Web App (1M DAU)

### 1. Requirements & Parameters
* **DAU:** 1 Million active users.
* **Reads:** 30 reads/day per user, 10 KB per response.
* **Writes:** 2 writes/day per user, 2 KB payload.
* **Retention:** 3 years ($3 \times 365 \approx 1,100\text{ days}$).

### 2. Step-by-Step Math

#### A. Queries Per Second (QPS)
* **Total Daily Reads:** $1\text{M} \times 30 = 30\text{ Million reads/day}$.
  $$\text{Average Read QPS} = \frac{30,000,000}{86,400} \approx 347\text{ QPS (Quick estimate: } 30 \times 12 \approx 360\text{ QPS)}$$
  $$\text{Peak Read QPS } (2.5\times) \approx 350 \times 2.5 \approx 875\text{ QPS}$$
* **Total Daily Writes:** $1\text{M} \times 2 = 2\text{ Million writes/day}$.
  $$\text{Average Write QPS} = \frac{2,000,000}{86,400} \approx 23\text{ QPS (Quick: } 2 \times 12 \approx 24\text{ QPS)}$$
  $$\text{Peak Write QPS } (2.5\times) \approx 24 \times 2.5 \approx 60\text{ QPS}$$

#### B. Storage Volume
* **Daily Write Volume:**
  $$\text{Daily Storage} = 2\text{M writes} \times 2\text{ KB} = 4\text{ GB/day}$$
* **3-Year Storage:**
  $$\text{3-Year Storage} = 4\text{ GB/day} \times 365 \times 3 \approx 4\text{ GB} \times 1,100 \approx 4.4\text{ TB}$$
* With index overhead ($1.5\times$) and replication ($2\times$ replica copies): $\approx 4.4\text{ TB} \times 3 \approx 13.2\text{ TB}$.

#### C. Network Bandwidth
* **Ingress (Incoming writes):**
  $$23\text{ writes/sec} \times 2\text{ KB} = 46\text{ KB/sec} = 368\text{ Kbps (negligible)}$$
* **Egress (Outgoing reads):**
  $$350\text{ reads/sec} \times 10\text{ KB} = 3,500\text{ KB/sec} = 3.5\text{ MB/sec} \times 8 \approx 28\text{ Mbps}$$

#### D. Architectural Bottleneck
* **Verdict:** This entire system comfortably lives on a **single relational database** (e.g., PostgreSQL or MySQL) with 1 primary and 1 standby replica.
* 350 read QPS and 23 write QPS can easily be handled by a modern 8-core CPU server without sharding or complex caching. 4.4 TB of storage over 3 years easily fits on standard NVMe EBS volumes.

---

## Exercise 2: Medium Social Feed (10M DAU)

### 1. Requirements & Parameters
* **DAU:** 10 Million active users.
* **Reads:** 15 feed loads/day per user, 50 KB per load.
* **Writes:** 2 posts/day per user, 1 KB text.
* **Retention:** 5 years ($5 \times 365 \approx 1,825\text{ days}$).

### 2. Step-by-Step Math

#### A. Queries Per Second (QPS)
* **Total Daily Reads:** $10\text{M} \times 15 = 150\text{ Million feed loads/day}$.
  $$\text{Average Read QPS} = \frac{150,000,000}{86,400} \approx 1,736\text{ QPS (Quick: } 150 \times 12 \approx 1,800\text{ QPS)}$$
  $$\text{Peak Read QPS } (2.5\times) \approx 1,736 \times 2.5 \approx 4,340\text{ QPS}$$
* **Total Daily Writes:** $10\text{M} \times 2 = 20\text{ Million posts/day}$.
  $$\text{Average Write QPS} = \frac{20,000,000}{86,400} \approx 231\text{ QPS (Quick: } 20 \times 12 \approx 240\text{ QPS)}$$
  $$\text{Peak Write QPS } (2.5\times) \approx 231 \times 2.5 \approx 578\text{ QPS}$$

#### B. Storage Volume
* **Daily Write Volume:**
  $$\text{Daily Storage} = 20\text{M posts} \times 1\text{ KB} = 20\text{ GB/day}$$
* **5-Year Storage:**
  $$\text{5-Year Storage} = 20\text{ GB/day} \times 1,825\text{ days} \approx 36.5\text{ TB}$$

#### C. Network Bandwidth
* **Ingress:**
  $$231\text{ writes/sec} \times 1\text{ KB} = 231\text{ KB/sec} \approx 1.85\text{ Mbps}$$
* **Egress:**
  $$1,736\text{ reads/sec} \times 50\text{ KB} \approx 86.8\text{ MB/sec} \times 8 \approx 695\text{ Mbps} \approx 0.7\text{ Gbps}$$

#### D. Architectural Bottleneck
* **Where It Breaks First:** **Database CPU & Disk Read IOPS** generating feed lists.
* Generating a feed requires joining followers and fetching posts. Running complex feed queries at 4,340 peak QPS directly on a relational database will crash it.
* **The Fix:** Introduce a **Redis Cache tier** (Cache-Aside or Fan-out home timeline caches) to absorb feed reads in RAM, and add 2–3 **Read Replicas** to offload user profile queries.

---

## Exercise 3: Microblogging Platform (100M DAU)

### 1. Requirements & Parameters
* **DAU:** 100 Million active users.
* **Reads:** 40 posts read/day per user.
* **Writes:** 1 post written/day per user (500 bytes text).
* **Retention:** 5 years ($1,825\text{ days}$).

### 2. Step-by-Step Math

#### A. Queries Per Second (QPS)
* **Total Daily Reads:** $100\text{M} \times 40 = 4\text{ Billion reads/day}$.
  $$\text{Average Read QPS} = \frac{4,000,000,000}{86,400} \approx 46,300\text{ QPS}$$
  $$\text{Peak Read QPS } (2\times) \approx 92,600\text{ QPS} \approx 100,000\text{ QPS}$$
* **Total Daily Writes:** $100\text{M} \times 1 = 100\text{ Million writes/day}$.
  $$\text{Average Write QPS} = \frac{100,000,000}{86,400} \approx 1,157\text{ QPS (Quick: } 100 \times 12 \approx 1,200\text{ QPS)}$$
  $$\text{Peak Write QPS } (2.5\times) \approx 1,157 \times 2.5 \approx 2,900\text{ QPS}$$

#### B. Storage Volume
* **Daily Write Volume:**
  $$\text{Daily Storage} = 100\text{M posts} \times 500\text{ bytes} = 50\text{ GB/day}$$
* **5-Year Storage:**
  $$\text{5-Year Storage} = 50\text{ GB/day} \times 1,825\text{ days} \approx 91.25\text{ TB}$$
* With metadata and indexing overhead: $\approx 150\text{ TB}$.

#### C. Network Bandwidth
* **Ingress:**
  $$1,157\text{ writes/sec} \times 500\text{ bytes} \approx 578.5\text{ KB/sec} \approx 4.6\text{ Mbps}$$
* **Egress (assuming 500 bytes per post returned):**
  $$46,300\text{ reads/sec} \times 500\text{ bytes} \approx 23.15\text{ MB/sec} \times 8 \approx 185\text{ Mbps}$$
  *(Note: If returning batches of 10 posts with author metadata, egress scales to $\sim 2\text{ Gbps}$).*

#### D. Architectural Bottleneck
* **Where It Breaks First:** **Read Fan-Out & Redis Memory Saturation**.
* Serving 100,000 read QPS cannot be done by querying disk. A clustered Redis cache fleet is mandatory.
* At 100M DAU, **Celebrity Fan-Out on Write** will choke message workers if a user with 50M followers posts. A hybrid fan-out model (push for regular users, pull on read for celebrities) is required.

---

## Exercise 4: Photo Portfolio Site (Unsplash Clone)

### 1. Requirements & Parameters
* **DAU:** 5 Million active users.
* **Uploads:** 1 Million new photos/day (average 2 MB each).
* **Views:** 50 Million photo views/day.

### 2. Step-by-Step Math

#### A. Queries Per Second (QPS)
* **Upload QPS:**
  $$\text{Average Upload QPS} = \frac{1,000,000}{86,400} \approx 11.6 \approx 12\text{ QPS}$$
  $$\text{Peak Upload QPS } (3\times) \approx 36\text{ QPS}$$
* **View QPS:**
  $$\text{Average View QPS} = \frac{50,000,000}{86,400} \approx 578\text{ QPS}$$
  $$\text{Peak View QPS } (3\times) \approx 1,736\text{ QPS}$$

#### B. Storage Growth
* **Daily Photo Storage:**
  $$1,000,000\text{ photos} \times 2\text{ MB} = 2,000,000\text{ MB} = 2\text{ TB/day!}$$
* **Annual Storage:**
  $$2\text{ TB/day} \times 365\text{ days} = 730\text{ TB/year}$$

#### C. Network Bandwidth
* **Ingress (Upload bandwidth):**
  $$12\text{ uploads/sec} \times 2\text{ MB} = 24\text{ MB/sec} \times 8 \approx 192\text{ Mbps}$$
* **Egress (Photo viewing bandwidth):**
  $$578\text{ views/sec} \times 2\text{ MB} = 1,156\text{ MB/sec} = 1.15\text{ GB/sec}!$$
  $$\text{Egress Bandwidth in Gbps} = 1.156 \times 8 \approx \mathbf{9.25\text{ Gbps}}$$
  $$\text{Peak Egress Bandwidth } (3\times) \approx 9.25 \times 3 \approx \mathbf{27.7\text{ Gbps}}$$

#### D. Architectural Bottleneck
* **Where It Breaks First:** **Network Egress Bandwidth & App Server Saturation**.
* Streaming nearly 10 Gbps average (28 Gbps peak) will completely saturate standard application server network interfaces and incur enormous cloud bandwidth costs.
* Storing 730 TB/year in an operational database will destroy it.
* **The Architecture:**
  1. **Object Storage (AWS S3):** Never store raw photos in PostgreSQL.
  2. **Direct-to-S3 Pre-signed Uploads:** Client streams 2 MB images directly to S3.
  3. **Global CDN (Cloudflare / CloudFront):** CDN edge caches absorb $> 95\%$ of image views close to users, cutting origin egress from 28 Gbps down to $< 1.4\text{ Gbps}$.

---

## Exercise 5: Short-Form Video App (TikTok Clone)

### 1. Requirements & Parameters
* **DAU:** 25 Million active users.
* **Uploads:** 500,000 video clips/day (average 15 MB each).
* **Views:** Each user watches 40 clips/day ($25\text{M} \times 40 = 1\text{ Billion video views/day}$).

### 2. Step-by-Step Math

#### A. Queries Per Second (QPS)
* **Upload QPS:**
  $$\text{Average Upload QPS} = \frac{500,000}{86,400} \approx 5.8 \approx 6\text{ QPS}$$
* **View / Stream QPS:**
  $$\text{Average View QPS} = \frac{1,000,000,000}{86,400} \approx 11,574\text{ QPS}$$
  $$\text{Peak View QPS } (2.5\times) \approx 28,935\text{ QPS}$$

#### B. Storage Growth
* **Daily Raw Video Storage:**
  $$500,000\text{ videos} \times 15\text{ MB} = 7,500,000\text{ MB} = 7.5\text{ TB/day}$$
* With multi-bitrate transcoding (1080p, 720p, 480p, 360p adds $\sim 1.5\times$ storage):
  $$\text{Daily Total Transcoded Storage} = 7.5\text{ TB} \times 2.5 \approx 18.75\text{ TB/day}$$
* **Annual Storage:**
  $$18.75\text{ TB/day} \times 365 \approx 6.84\text{ PB/year (Petabytes!)}$$

#### C. Network Bandwidth
* **Ingress (Video Uploads):**
  $$6\text{ uploads/sec} \times 15\text{ MB} = 90\text{ MB/sec} \times 8 \approx 720\text{ Mbps}$$
* **Egress (Assuming users watch 5 MB of each 15 MB video):**
  $$11,574\text{ views/sec} \times 5\text{ MB} = 57,870\text{ MB/sec} \approx 57.87\text{ GB/sec}!$$
  $$\text{Egress Bandwidth in Gbps} = 57.87 \times 8 \approx \mathbf{463\text{ Gbps}}$$
  $$\text{Peak Egress Bandwidth } (2.5\times) \approx 463 \times 2.5 \approx \mathbf{1,157\text{ Gbps} (1.15\text{ Tbps!})}$$

#### D. Architectural Bottleneck
* **Where It Breaks First:** **Global Network Egress & Worker Transcoding CPU**.
* Terabits-per-second egress makes direct datacenter streaming physically and financially impossible.
* **The Architecture:**
  1. Multi-CDN edge strategy (Akamai, Fastly, Cloudflare) with byte-range chunk caching.
  2. Asynchronous transcoding pipelines using GPU/ASIC worker fleets managed by message queues.
  3. Tiered storage: push videos older than 60 days to Infrequent Access / Glacier.

---

## Exercise 6: 1-on-1 Chat App (WhatsApp Clone)

### 1. Requirements & Parameters
* **DAU:** 50 Million active users.
* **Activity:** 40 messages/day per user ($50\text{M} \times 40 = 2\text{ Billion messages/day}$).
* **Text Size:** 100 bytes per message.
* **Media:** 10% of messages include a photo ($300\text{ KB}$).

### 2. Step-by-Step Math

#### A. Queries Per Second (QPS)
* **Daily Total Messages:** 2 Billion messages/day.
  $$\text{Average Message Ingestion QPS} = \frac{2,000,000,000}{86,400} \approx 23,148\text{ QPS}$$
  $$\text{Peak Ingestion QPS } (2.5\times) \approx 57,870\text{ QPS}$$
* Since every 1-on-1 message must be delivered to the recipient, delivery QPS equals ingestion QPS ($\approx 23,150\text{ QPS}$).

#### B. Storage Growth
* **Text Storage:**
  $$2\text{ Billion} \times 100\text{ bytes} = 200\text{ GB/day}$$
* **Media Storage (10% of 2 Billion = 200 Million images):**
  $$200\text{ Million} \times 300\text{ KB} = 60,000,000\text{ KB} = 60\text{ TB/day}$$
* **Annual Storage:**
  $$\text{Text} = 200\text{ GB} \times 365 \approx 73\text{ TB/year}$$
  $$\text{Media} = 60\text{ TB} \times 365 \approx 21.9\text{ PB/year}$$

#### C. Network Bandwidth
* **Text Bandwidth:**
  $$23,148\text{ msgs/sec} \times 100\text{ bytes} \approx 2.31\text{ MB/sec} \times 8 \approx 18.5\text{ Mbps}$$
* **Media Bandwidth (Ingress & Egress):**
  $$2,315\text{ media msgs/sec} \times 300\text{ KB} \approx 694.5\text{ MB/sec} \times 8 \approx \mathbf{5.55\text{ Gbps}}$$

#### D. Architectural Bottleneck
* **Where It Breaks First:** **Open TCP/WebSocket Connections & RAM on Gateway Servers**.
* 50 Million DAU means at peak hours, **15 to 20 Million users are simultaneously connected**.
* If each TCP socket consumes 10 KB of operating system memory:
  $$20,000,000 \times 10\text{ KB} \approx 200\text{ GB of RAM}$$
* **The Architecture:**
  1. Epoll-based connection gateway servers (e.g., Erlang/Elixir, Go, or Netty) holding millions of open WebSockets.
  2. Redis presence cluster mapping `user_id -> gateway_server_id`.
  3. Ephemeral store-and-forward queue: once a message is acknowledged by the recipient device, delete it from the server to keep disk usage near zero (WhatsApp model).

---

## Exercise 7: Centralized Server Log Tracker

### 1. Requirements & Parameters
* **Server Fleet:** 5,000 servers.
* **Log Rate:** 50 log lines/second per server ($24 \times 7$).
* **Line Size:** 500 bytes per log line.
* **Retention:** 30 days in search index; 1 year in cold archive.

### 2. Step-by-Step Math

#### A. Ingestion Rate (QPS & Throughput)
* **Total Continuous Log QPS:**
  $$\text{Ingestion QPS} = 5,000\text{ servers} \times 50\text{ lines/sec} = \mathbf{250,000\text{ lines/second}}$$
* **Continuous Ingress Data Rate:**
  $$250,000\text{ lines/sec} \times 500\text{ bytes} = 125,000,000\text{ bytes/sec} = \mathbf{125\text{ MB/sec}}$$
  $$\text{Network Bandwidth} = 125\text{ MB/sec} \times 8 = \mathbf{1\text{ Gbps (continuous)}}$$

#### B. Storage Calculations
* **Daily Ingestion Volume:**
  $$\text{Daily Volume} = 125\text{ MB/sec} \times 86,400\text{ sec} \approx 10,800,000\text{ MB} \approx \mathbf{10.8\text{ TB/day}}$$
* **30-Day Search Index (Hot Tier):**
  $$10.8\text{ TB/day} \times 30\text{ days} = 324\text{ TB (raw text)}$$
  * Inverted indexes (Lucene / Elasticsearch) have an expansion factor of $1.3\times$ to $1.5\times$, plus $1\times$ replica copy for HA:
    $$\text{Hot Search Tier Disk Needed} \approx 324\text{ TB} \times 1.4 \times 2 \approx \mathbf{907\text{ TB of fast NVMe SSD!}}$$
* **1-Year Cold Archival Storage:**
  $$10.8\text{ TB/day} \times 365\text{ days} \approx 3,942\text{ TB} \approx 3.94\text{ PB (raw)}$$
  * Compressed with Zstandard / Gzip ($5\times$ compression on structured JSON text):
    $$\text{Cold Tier S3 Storage} \approx \frac{3.94\text{ PB}}{5} \approx \mathbf{788\text{ TB in AWS S3 Glacier}}$$

#### C. Architectural Bottleneck
* **Where It Breaks First:** **Elasticsearch Cluster Write Saturation & Node GC Freezes**.
* Indexing 250,000 documents per second directly into an Elasticsearch cluster will trigger constant Lucene segment merges and garbage collection pauses, collapsing nodes.
* **The Architecture:**
  1. **Local Agent Buffering (Vector / Fluentbit):** Batch log lines on the host before sending.
  2. **Kafka Message Bus:** Buffer the 125 MB/sec stream across 30–50 Kafka partitions to absorb index backpressure.
  3. **Tiered Indexing:** Micro-batch into ClickHouse or OpenSearch, and stream Parquet files directly to S3 for Athena queries.
