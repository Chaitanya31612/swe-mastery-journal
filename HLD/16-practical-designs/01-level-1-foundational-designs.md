# Practical System Designs: Level 1 Foundational Systems

> **The Rule:** Don't start with Uber or Netflix! First, master the 5 core building-block systems that appear inside every major company.  
> Approach each design using the **13-Step Architectural Recipe**. Keep your explanations simple, conversational, and focused on trade-offs.

---

## The 13-Step Architectural Recipe

Whenever you design any system (in an interview or on the job), follow this natural flow:
1. **Clarify the Problem:** Who is using it? What are the edge cases?
2. **Functional Requirements (FR):** What 2 or 3 things must the system do?
3. **Non-Functional Requirements (NFR):** What cannot fail? (Speed, 100% accuracy, high uptime?)
4. **Napkin Math (Scale):** How many QPS? How much disk space per year?
5. **API Design:** What do the endpoints look like? (`POST /shorten`, `GET /{id}`)
6. **Data Model:** What tables/keys do we need, and which database holds them?
7. **High-Level Diagram:** Draw the boxes from phone to database.
8. **The Happy Request Path:** Trace a normal user click step-by-step.
9. **The Background Flow:** What runs asynchronously behind the scenes?
10. **How to Scale 10x:** Adding caches, replicas, or shards when traffic surges.
11. **How It Can Break:** What happens when a machine dies?
12. **The True Bottleneck:** What physical resource (CPU, disk IOPS, network) maxes out first?
13. **The Trade-offs Summary:** What did we deliberately sacrifice?

---

## Challenge 1: The Short Link Machine (TinyURL / Bitly)

### The Real-World Scenario
You enter a 200-character long URL:
`https://amazon.com/products/electronics/laptops/2026/deal?ref=campaign123&track=xyz`  
The service returns a tiny 7-character link:  
`https://tiny.url/a8F3k9`  
When anyone in the world clicks that short link, they get redirected to the long Amazon page in under **20 milliseconds**.

### The Numbers:
* **Writes:** 100 Million new links created per month (~40 writes/sec average; peak 150/sec).
* **Reads:** 10 Billion clicks per month (100:1 read-to-write ratio; ~4,000 QPS average; peak 15,000 QPS).
* **Retention:** Keep links for 5 years.

### The Big Decisions You Must Make:
* **How do you generate the 7 characters?** Do you hash the URL (MD5/SHA256) and deal with collisions, or use a distributed counter converted to Base62?
* **HTTP 301 vs. 302:** Which status code do you return?
  * `301 Permanent Redirect`: The user's browser caches the redirect forever. Great for speed, but you get **zero click analytics**!
  * `302 Temporary Redirect`: Every single click hits your server so you can track analytics, but it adds a tiny network hop.
* **How much Redis RAM do you need to cache the top 20% links?**

---

## Challenge 2: The Digital Scratchpad (Pastebin)

### The Real-World Scenario
Users paste code snippets, error logs, or text notes (up to 10MB each) and receive a shareable link. They can set an expiration time: *"Delete this paste in 1 hour"*, *"1 day"*, or *"Never"*.

### The Numbers:
* **Writes:** 2 Million pastes created per day (~24 writes/sec).
* **Reads:** 20 Million views per day (~240 QPS).
* **Payload:** Average paste is 10 KB; maximum is 10 MB.
* **Storage:** 70% of pastes expire within 30 days.

### The Big Decisions You Must Make:
* **Where does the text live?** Do you store 10MB text snippets inside PostgreSQL, or do you store the text in Amazon S3 and only keep metadata in the database?
* **How do you clean up expired pastes?** Do you run a heavy cron job running `DELETE FROM pastes WHERE expires_at < NOW()` (which locks the database!), or do you delete lazily when someone tries to read an expired link?

---

## Challenge 3: The Front Door Bouncer (Distributed Rate Limiter)

### The Real-World Scenario
Protect an API from bots, scrapers, and denial-of-service attacks. If a client exceeds 100 requests per minute, immediately slam the door in their face with `HTTP 429 Too Many Requests`.

### The Numbers:
* **Scale:** Must evaluate **100,000 incoming requests per second** across 200 web servers with $< 2\text{ms}$ added latency.
* **Distributed Challenge:** Client A might hit Server #1 on click 1, and Server #45 on click 2. How do all 200 servers know how many requests Client A has made?

### The Big Decisions You Must Make:
* **Which algorithm?** Token Bucket vs. Sliding Window Counter.
* **Where do the counters live?** A centralized Redis cluster running atomic Lua scripts, or local in-memory counters that sync periodically?
* **Fail Open or Fail Closed?** If the Redis rate-limiter cluster catches fire, do you let all traffic through (Fail Open) or block all users (Fail Closed)?

---

## Challenge 4: The Freight Delivery System (High-Scale File Upload)

### The Real-World Scenario
Users upload large files (from 50MB PDFs to 10GB 4K raw videos) over flaky mobile connections. The upload must support pause, resume, and chunking without crashing web servers.

### The Numbers:
* **Scale:** 5 Million files uploaded per day.
* **The Physics Problem:** A user uploads a 5GB video on a train with spotty cellular connection. The connection drops at 90%. They should NOT have to start over from 0%!

### The Big Decisions You Must Make:
* **Direct-to-Storage:** How do you use the **S3 Pre-Signed URL** pattern so that 10GB files flow directly from the client's browser into S3, completely bypassing your web servers?
* **Multi-Part Chunking:** How does the browser chop a 5GB file into 10MB pieces, upload chunks concurrently, and tell S3 to sew them back together?

---

## Challenge 5: The Instant Photo Studio (Image Hosting & Resizing)

### The Real-World Scenario
Users upload full-resolution photos. Viewers request images dynamically resized to fit their exact device screen:  
`https://images.site.com/photo101.jpg?width=300&height=200&format=webp`

### The Numbers:
* **Uploads:** 5 Million images per day (~60/sec).
* **Views:** 500 Million image views per day (~6,000 QPS average; peak 20,000 QPS).
* **Raw Image Size:** Average 3 MB original photo.

### The Big Decisions You Must Make:
* **Eager vs. Lazy Resizing:** Do you pre-generate 15 different thumbnail sizes the second an image is uploaded (wasting disk space on sizes nobody ever views?), or do you resize on-demand the first time someone requests that size and cache it on a CDN?
* **Where does resizing compute happen?** On backend worker servers, or directly at the edge using Cloudflare Workers / Lambda@Edge?

---

## 60-Second Summary

> "Level 1 designs teach the fundamental building blocks of system architecture. TinyURL teaches URL encoding and caching ratios. Pastebin teaches how to separate text blobs from metadata and handle data expiration. The Rate Limiter teaches token buckets and distributed atomic counters. File Upload teaches multi-part chunking and direct-to-S3 pre-signed uploads. And Image Hosting teaches edge compute and dynamic on-demand transformation. Master these five, and you have the foundation to tackle any system design problem."
