·

# System Design Mental Model: How to Think Like an Architect

---

## Mental Model: The Coffee Shop Analogy

System design isn't about memorizing fancy diagrams or drawing 20 boxes with arrows.

At its heart, **system design is just smart budgeting**. You have a problem to solve, but you have limits: limited money, limited time, and the laws of physics.

Think of designing a software system like running a busy coffee shop:

* If you only have **10 customers a day**, one barista with a home espresso machine can take orders, make coffee, and swipe credit cards. Life is simple.
* What happens when **5,000 customers show up every morning**?
  * If one person tries to do everything, the line wraps around the block and people leave angry (**High Latency / Bottleneck**).
  * So you split the work: one cashier takes orders and hands out order tickets (**Decoupling / Queue**), while three baristas make drinks from the tickets (**Worker Fleet**).
  * What if an espresso machine breaks? You need a backup machine ready to go (**Redundancy / High Availability**).
  * What if a customer asks for cold brew? Instead of brewing it on the spot (takes 18 hours!), you poured a big pitcher this morning and keep it in the fridge ready to pour in 2 seconds (**Caching**).

```
  [ Customer Orders ]
          |
          v
  [ Cashier / Ticket Printer ] ----(Takes order in 5 seconds & gives you ticket #42)
          |
          v
  [ Order Board (Queue) ] ---------(Buffer so baristas don't get yelled at)
          |
   +------+------+
   |             |
   v             v
[ Barista 1 ] [ Barista 2 ] ------(Fulfill drinks at a steady, reliable pace)
```

Every decision in high-level design is just this:

$$
\text{Problem} \longrightarrow \text{What's stopping us? (Constraint)} \longrightarrow \text{What do we change?} \longrightarrow \text{What's the catch? (Trade-off)}
$$

---

## Why It Exists

On your laptop, code is easy. Your CPU, RAM, and SSD are connected by high-speed copper pins on a single motherboard. Things happen in nanoseconds. If something crashes, your program just stops.

As soon as your app gets popular and outgrows one computer:

1. **Computers must talk over a network:** A cable between two datacenters is millions of times slower than your laptop's memory bus.
2. **Things fail partially:** In a single computer, either it works or it's turned off. In a system of 50 servers, one server is slow, another crashed, a third lost Wi-Fi, and the other 47 are working fine. How do they agree on anything?
3. **Physical limits hit fast:** No matter how much money you have, you cannot buy a computer with infinite CPU or infinite disk speed.

System design exists because **one machine isn't enough, and coordinating multiple machines over a network is messy.**

---

## How It Works: The 11 Forces That Pull Against Each Other

When designing any system, these 11 words describe what you're balancing. Let's make them crystal clear:

### 1. The Speed Forces

* **Latency:** *"How long do I wait for my single request?"*
  * *Real-life:* You order a burger at a drive-thru. It takes 3 minutes to get your food. Latency = 3 minutes.
* **Throughput:** *"How much work can the whole system do at once?"*
  * *Real-life:* The kitchen can make 200 burgers an hour. Throughput = 200 burgers/hour.
  * *Note:* You can have great throughput with bad latency (e.g., shipping a freight train full of hard drives across the country has massive throughput, but terrible latency).

### 2. The Safety Forces

* **Durability:** *"Once you say 'saved', will my data survive if the server catches fire?"*
  * *Real-life:* Storing a family photo in AWS S3. Even if a tornado hits an Amazon warehouse, your photo is saved across other buildings.
* **Consistency:** *"Does everyone see the exact same information right now?"*
  * *Real-life:* You withdraw $100 from an ATM. If your partner checks your bank balance on their phone 1 second later, does it show the $100 gone, or the old balance?
* **Availability:** *"Is the front door open when I knock?"*
  * *Real-life:* If you visit google.com, does the page load, or do you get an error screen?
* **Reliability:** *"Does it do the right job without messing up?"*
  * *Real-life:* The train arrives on time and doesn't derail. An API that quickly returns an empty screen is 100% available, but 0% reliable.
* **Security:** *"Are only the right people allowed in, and is data safe from prying eyes?"*

### 3. The Scale & Cost Forces

* **Scalability:** *"When 10x more users show up, can we just add more machines and keep running smoothly?"*
* **Performance:** *"Are we using our CPU and RAM smartly, or wasting it?"*
* **Cost:** *"How much is AWS going to bill us at the end of the month?"*
* **Complexity:** *"Can an engineer on call at 2:00 AM understand how this works, or is it a tangled mess?"*

---

## The Catch: Why You Can Never Have Everything

In software architecture, **every dial you turn up pushes another dial down**.

### Tension 1: Safety vs. Speed (Durability vs. Latency)

* If you want a write to be **100% durable**, the server has to write it to disk, replicate it over the network to 2 other machines in different cities, and wait for them to confirm. That takes **15 milliseconds**.
* If you want it **lightning fast (sub-millisecond)**, you write it to RAM and return immediately. But if the power cord gets pulled that second, that data is gone forever.

### Tension 2: Accuracy vs. Uptime (Consistency vs. Availability — The CAP Principle)

* Imagine an ocean cable between New York and London gets cut.
* A user in New York tries to buy the last pair of sneakers.
* **Option A (Pick Consistency):** London doesn't know if New York sold the shoes. So London refuses to sell anything until the cable is fixed. (Consistent, but London users see an error screen $\to$ Lower Availability).
* **Option B (Pick Availability):** London lets people keep buying. Everyone is happy, but you might sell the same pair of sneakers twice! (High Availability, but messy inconsistencies).

### Tension 3: Scale vs. Simplicity

* Running a single Postgres database on one good server is simple. One database to back up, one place to query, zero network splits.
* Splitting your database across 20 shards means you now need cluster managers, distributed keys, and complex re-indexing. You only pay that complexity tax when one machine physically cannot keep up anymore.

---

## When To Use It

* **Whenever you start a new feature or service:** Ask: *"Who is going to use this, how many requests will it get, and what happens if it goes down for 10 minutes?"*
* **In System Design Interviews:** The interviewer doesn't care if you know what Redis is. They care if you can say: *"Since this is an e-commerce checkout, we care much more about not double-selling items (Consistency) than shaving 5 milliseconds off the response time."*

---

## When Not To Use It

* **For your hackathon project or internal tool:** If only 15 people in your company use an internal dashboard, don't set up Kafka, Redis, and Kubernetes. A simple monolithic app on a $10 virtual server will run for years without issues.
* **Before you have users:** Don't build for 100 million users when you currently have zero. Build things clean and modular so you *can* scale later, but don't buy the factory before you sell the first cookie.

---

## Alternatives: How People Design (Good vs. Bad)

| Approach                                      | How it Works                                                                                                  | What Happens in Real Life                                                                                                      |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **"Vibes-based" Design**                | Use whatever tech was trending on Hacker News or YouTube this week.                                           | You spend 6 months setting up Kafka and Cassandra for an app that gets 3 visits a day.                                         |
| **Monolith Until it Breaks**            | Keep everything on one simple server until metrics prove a specific bottleneck.                               | You ship in 2 weeks, make money, and only scale the specific parts that need it. (How Shopify, GitHub, and Basecamp started!). |
| **Constraint-Driven Design (Our Goal)** | Look at your non-negotiables first, pick the right tool for that exact job, and state the trade-offs upfront. | Clean, defensible systems that don't melt in production.                                                                       |

---

## Common Ways Systems Break (Failure Modes)

1. **The "It worked on my laptop" Trap:** Forgetting that network calls can hang forever. Always set a timeout!
2. **Confusing Availability with Reliability:** Thinking your API is healthy because it returns `200 OK`, while ignoring that it's returning empty data because a backend query crashed silently.
3. **Premature Sharding:** Splitting a database into 10 shards when the whole database was only 20 GB. Modern NVMe SSDs can read 20 GB in a few seconds. You added 10x headache for no reason.

---

## How Systems Grow Up (The Scaling Stages)

```
Stage 1: Day 1 (1 - 1,000 users)
[ User ] ---> [ One Box: Web App + Database together ]
              Simple, fast to build, cheap ($10/month).

Stage 2: Growing (10,000 users)
[ User ] ---> [ Web App Server ]
                     |
              [ Separate Database Server ]
              Now they aren't fighting for the same CPU and RAM.

Stage 3: Hitting Traffic (100,000 users)
                +---> [ Web App Server 1 ] ---+
[ Load Balancer]|                             |---> [ Primary DB (Writes) ]
                +---> [ Web App Server 2 ] ---+            |
                     |                        |     (Copies changes)
                     +---> [ Redis Cache ]    +---> [ Read Replica (Reads) ]
              Web apps are now disposable. Redis handles popular reads.

Stage 4: Big League (1,000,000+ users)
Add Message Queues (Kafka/SQS) for background jobs, split databases into shards,
put a CDN (Cloudflare) in front of everything.
```

---

## Real-World Example: Instagram Feed vs. Bank Transfer

| Feature                          | Instagram Home Feed                                         | Bank Account Transfer                                                    |
| -------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------ |
| **What matters most?**     | **Speed & Uptime** (Latency & Availability)           | **Zero Data Loss & Accuracy** (Durability & Consistency)           |
| **What if a server dies?** | If you see a post 3 seconds late, nobody cares.             | If $50 disappears from your account, everyone panics.                    |
| **The Choice:**            | Use fast in-memory caches, eventual consistency, fail open. | Use strict database transactions, write-ahead logs on disk, fail closed. |

---

## How to Sound Like a Senior Engineer in an Interview

1. **Don't touch the pen for the first 3 minutes.** When the interviewer says *"Design Twitter"*, don't start drawing boxes. Say:
   > *"Before we jump into architecture, let me clarify the core requirements. Are we focusing on the read-heavy home timeline, or the tweet posting flow? And what scale are we designing for?"*
   >
2. **Always state the catch:**
   > *"I'm going to put Redis in front of our product database. That will drop read latency to under 2ms. The trade-off is that if a price changes in the database, users might see the old cached price for up to 30 seconds until the cache expires."*
   >

---

## 10 Common Mistakes People Make

* ❌ Starting with tech names: *"I'll use Kafka and Mongo"* instead of *"We need an async queue and a document store"*.
* ❌ Forgetting that networks are unreliable.
* ❌ Not asking how many reads vs. how many writes happen.
* ❌ Trying to make every single part of the system 100% strongly consistent.
* ❌ Designing for millions of users without calculating if a single machine could handle it.

---

## Self-Check: Can You Answer These?

1. If your API is slow, but CPU and RAM are both under 20%, what are three possible things the server is waiting for?
   The 3 most common culprits in production:
   1. Database Lock Contention / Connection Pool Starvation: The app server is ready, but all 50 database connections are busy, or
      queries are waiting for an exclusive row lock.
   2. Waiting on a Slow Third-Party Network Call: Your code is synchronously calling Stripe, Twilio, or an internal microservice,
      and blocking on the network socket.
   3. Disk I/O / Thread Deadlock: Threads are stuck in a waiting state (blocked on a mutex lock or reading from a slow network
      drive).
2. Why is it dangerous to promise "100% Consistency and 100% Availability across multiple cities"? --- ANS: CAP theorem will be violated in case of network partition
3. What is the difference between how long one request takes (Latency) and how many requests the server can complete in a second (Throughput)?
   Latency is time per single unit of work (e.g., "This API takes 30ms").
   • Throughput is units of work per unit of time (e.g., "This cluster can process 5,000 requests per second").
   • The Highway Analogy: A Ferrari driving 120 mph on an empty 1-lane road has ultra-low latency, but low throughput (only 1 car
   fits). A massive freight train moving at 30 mph has terrible latency, but insane throughput (moves 10,000 tons of cargo at once)
4. If you have an e-commerce flash sale, which force is more important: stopping people from buying out-of-stock items (Consistency) or letting everyone click around fast (Availability)? --- ANS: Consistency is important

---

## Practice: 10 Real Scenarios ("What Matters Most Here?")

> **How to do this:** For each scenario below, imagine you are the lead engineer.Ask yourself:
>
> 1. **What are the top 2 things we CANNOT mess up?** (e.g., Latency, Consistency, Durability, Availability, etc.)
> 2. **What can we afford to relax or let slide?**
> 3. **Why?** (Explain in 2 simple sentences).

### Scenario 1: Stock Brokerage Order Execution (Robinhood / E*Trade)

A user clicks "Buy 10 shares of Apple at Market Price".

My Ans:

cannot mess up: consistency, durabilty, reliability, security
can afford or relax: avaliablity, latency

• Top 2 Non-Negotiables: Consistency & Durability. Every trade must be legally recorded to the cent. If money or share counts get
      corrupted, your brokerage loses its license.
      • The Nuance on Latency: While high-frequency hedge funds care about microseconds, for a retail app, you can afford ~100–300ms
      execution latency.
      • What we relax: Availability. If the stock exchange link is acting unstable, you Fail Closed (refuse to place orders) rather
      than executing invalid market orders!

### Scenario 2: Video Streaming (Netflix Movie Playback)

A user presses Play on *Stranger Things* on their living room TV on a Friday night.

My Ans:
cannot messup: latency, availablity, security
can relax: consistency,

### Scenario 3: Real-Time Collaborative Document (Google Docs)

Three coworkers are editing the same meeting notes at the exact same second from different laptops.

My ans:
cannot messup: latency, durability, reliability, availablity
can relax: consistency (eventual is fine)

Top 2 Non-Negotiables: Latency (local responsiveness) & Durability (never lose my typed words). If pressing a key on your
      keyboard took 1 second to appear on screen, you'd close the app in frustration.
      • What we relax: Immediate Strong Consistency. Google Docs famously uses Operational Transformation (OT) / CRDTs. If Alice and
      Bob type at the exact same millisecond, their laptops show their own local edits first, and the system merges them eventually
      over the next 100 milliseconds.

### Scenario 4: Hospital ICU Patient Vital Signs

A bedside monitor tracks a heart attack patient's pulse and sends it to the central nurses' station.

ans: cannot messup: consistency, latency, reliability --- can relax:

• Top 2 Non-Negotiables: Low Latency & High Reliability. A flatline alarm must reach the nurses' desk in under 1 second. A
      dropped alert can cost a life.
      • What can we relax? Cost and Global Geographic Availability. ICU monitors run on a local hospital LAN. You do not need multi-
      region global replication to AWS Tokyo, nor do you need to store full 60Hz raw ECG waves on expensive SSDs forever (you can
      compress or aggregate after 24 hours).

### Scenario 5: Concert Ticket Flash Sale (Ticketmaster / Taylor Swift)

100,000 stadium seats go on sale at 10:00 AM. 3 million fans are refreshing the screen trying to claim the same front-row seats.

ans: cannot messup: consistency, durability --- can relax: availablity, latency

### Scenario 6: Ride-Share Driver Location Updates (Uber Driver App)

5 million active drivers transmit their current GPS coordinates every 4 seconds.

• Top 2 Non-Negotiables: High Throughput & Low Latency (Freshness). We need the latest location in memory right now.
      • What we relax: Durability (keep it in RAM, don't write every 4-second ping to hard drives) and Strict Consistency.

### Scenario 7: Bank Transaction Audit Log

A regulatory legal compliance vault that records every bank deposit, wire, and withdrawal for the next 7 years.

ans; cannot messup: durability, reliability, consistency -- can relax: latency, availablity

Top 2 Non-Negotiables: Durability & Consistency. If a bank auditor asks for wire transfers from 2021, those records must exist
      byte-for-byte without alteration.
      • What we relax: Latency. Nobody cares if an audit report takes 2 minutes or 2 hours to generate from cold S3 Glacier storage.

### Scenario 8: 1-on-1 Direct Chat (WhatsApp / Signal)

You send your friend a text message: *"Hey, are you free for lunch?"*

ans; cannot messup: availablity, latency, durability -- can relax: consistency

Top 2 Non-Negotiables: Low Latency (instant delivery when online) and Reliability/Durability (the message must never disappear).
      • What we relax: Global Consistency across chats. WhatsApp does not need Chat A and Chat B to be synchronized against each other
      globally. If a user is offline on an airplane, we use store-and-forward.

### Scenario 9: Competitive First-Person Shooter Game (Valorant / Call of Duty)

Two players turn a corner and shoot at each other at almost the exact same millisecond.

ans; cannot messup: latency and ? -- can relax: durability?

What can we relax? Durability! In a 60-tick game, player coordinates update 60 times a second. Those packets are sent over UDP
      and live only in server RAM. Nobody writes player mouse movements to a hard drive!
      • Top 2 Non-Negotiables: Ultra-Low Latency (< 20ms) and Real-Time Consistency (Fairness / Hit Registration). If two players shoot
      each other, the server's physics engine must resolve who fired first accurately.

### Scenario 10: Web Search Engine (Google Search)

A user types `"weather today"` into the search bar.

Top 2 Non-Negotiables: High Availability & Ultra-Low Latency.
      • What CAN Google Search relax? Consistency!
          • If someone published a blog post 30 seconds ago, does it have to appear in your search results right now? No!
          • If you and your friend search "best coffee" and get slightly different ranked lists or cached snippets, does anything
          break? No! Eventual consistency is 100% fine.

## 60-Second Summary

> "System design is just the art of smart compromises. We can't have infinite speed, zero cost, and 100% perfection all at once. When we build a system, we first find out what's non-negotiable: does this need to be 100% accurate like a bank transfer, or blazing fast like a video stream? Once we know what matters most, we pick the simplest building blocks that solve that constraint, and we always plan for what happens when a machine crashes."
