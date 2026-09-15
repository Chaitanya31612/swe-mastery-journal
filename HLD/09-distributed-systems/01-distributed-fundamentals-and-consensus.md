# Distributed Systems: Committees, Broken Walkie-Talkies & Fuse Boxes

---

## Mental Model: The Committee in Different Buildings

A distributed system is just **a bunch of separate computers trying to work together by sending letters to each other over an unreliable postal service**.

In a single computer:
* You have one clock, one memory chip, and everything happens cleanly.

In a distributed system:
* You have 5 computers in different cities.
* There is **no shared clock**: computer clocks drift apart by milliseconds every day.
* Messages get delayed or lost: A server might not reply because it crashed, or because a construction worker cut a fiber cable, or simply because it's running a slow 3-second garbage collection pause! You can never be sure which!

```
                  [ A MESSAGE IS SENT OVER THE INTERNET ]
                                     |
               +---------------------+---------------------+
               |                     |                     |
               v                     v                     v
       (Packet is lost)      (Server crashed)       (Server is just slow)
       "Did they die?"       "They're dead."        "I'm still thinking!"
```

The golden rule of distributed systems: **You cannot prevent network glitches. You have to design your system so that when glitches happen, your cluster reaches agreement anyway.**

---

## Quorums: The 5-Person Committee Rule ($W + R > N$)

How do multiple servers agree on what the current data is without waiting for every single server in the world to answer?

Think of a **5-person company board ($N = 5$)**:
* To pass a new rule, you need **3 votes ($W = 3$)**.
* Later, someone asks: *"What is the latest rule?"* They ask any **3 board members ($R = 3$)**.
* Because $3 + 3 = 6$, which is greater than the total board size of 5:
  $$\mathbf{W + R > N \implies \text{Guaranteed to overlap!}}$$
* There is **mathematically guaranteed to be at least ONE person** in the second meeting who was present in the first meeting and knows the newest rule!

```
Total Nodes: 5
Write Quorum (W = 3): Nodes [ 1, 2, 3 ] vote "YES" on Value B
Read Quorum  (R = 3): You ask Nodes [ 3, 4, 5 ]
* Node 3 overlaps! Node 3 says: "The latest value is B!"
```

* **Want fast writes?** Make $W = 1$ and $R = 5$ (writes are instant, but reads must check everyone).
* **Want fast reads?** Make $W = 5$ and $R = 1$ (reads are instant, but writes take longer).
* **Want balanced safety?** Make $W = 3$ and $R = 3$ (can survive 2 servers catching fire with zero data loss).

---

## Leader Election & Split-Brain: Why Clusters Love Odd Numbers

In systems like etcd, ZooKeeper, or Raft, one machine is the **Leader (The Boss)** and the others are **Followers**.

What happens if the network cable between two datacenters gets cut?

```
[ 4-NODE CLUSTER GETS CUT IN HALF ]
Datacenter A: [ Node 1, Node 2 ]    <--- CABLE CUT --->    Datacenter B: [ Node 3, Node 4 ]
Both sides have 2 nodes!
Both sides think the other died!
Both sides elect a new Leader!
-> SPLIT-BRAIN! Users in Datacenter A write conflicting data to Users in Datacenter B!
```

### The Fix: Strict Majority with Odd Numbers (3, 5, or 7)
Clusters require a **strict majority ($\lfloor N/2 \rfloor + 1$)** to make any decision:
* In a **5-node cluster**, majority is **3**.
* If the network splits the cluster into 3 nodes and 2 nodes:
  * The side with **3 nodes** has a majority $\to$ Continues working!
  * The side with **2 nodes** knows it does NOT have a majority $\to$ Freezes itself and refuses writes!
* **Split-brain is impossible!** (This is why you never run a cluster with an even number of nodes).

---

## Circuit Breakers: The Electrical Fuse Box

Think of the electrical panel in your house:
* If a toaster starts sparking and drawing dangerous current, the **circuit breaker trips open** and cuts off the electricity.
* Why? So your entire house doesn't burn down!

In software architecture, **Service A calls Service B**:
* If Service B gets overwhelmed and starts taking 30 seconds to answer:
  * Service A's threads get stuck waiting.
  * Soon, Service A runs out of threads and crashes too!
* **The Circuit Breaker:**
  * Sits between Service A and Service B.
  * If Service B fails more than 50% of the time, the breaker **trips OPEN**.
  * For the next 30 seconds, Service A **doesn't even try to call Service B**. It immediately fails fast or returns a backup cached response in 1 millisecond.
  * Service B gets 30 seconds of peace and quiet to recover from its traffic jam!

---

## Retry Storms & Jitter: The Revolving Door Jam

Imagine 50 people trying to push through a revolving door at the exact same second. The door jams.
* If everyone counts to 3 and pushes again simultaneously, the door jams again!
* **The Fix: Exponential Backoff with JITTER (Randomness)!**
  * Don't just double your wait time (1s, 2s, 4s, 8s).
  * Add a **random number of milliseconds** to every client's timer:
    $$\text{Wait} = 2^{\text{Attempt}} \pm \text{Random}(0\text{ to }500\text{ms})$$
  * Now, Person 1 tries after 1.2s, Person 2 tries after 1.7s, Person 3 tries after 2.1s. The crowd spreads out smoothly, and the door spins freely!

---

## Practice: Failure Scenarios

### Scenario 1: The Cascading Timeout
Service A has 100 worker threads. It calls Service B synchronously.
Service B's response time suddenly spikes from 20ms to **15 seconds**.
Incoming user traffic is 50 requests every second.
* **What happens to Service A within 3 seconds?**
* **What two safety valves stop this from taking down Service A?**

### Scenario 2: The Two Roommates and the Milk
Two servers both receive a request: *"If milk quantity is 0, buy 1 gallon of milk."*
Both servers check the database at the exact same millisecond: both see quantity is 0. Both order milk.
* **What is this bug called?**
* **How do you fix it?**

---

## 60-Second Summary

> "Distributed systems operate across an untrusted network where partial failures, packet drops, and clock drifts are normal everyday events. We reach safe agreement using quorums ($W + R > N$) and odd-numbered clusters (3 or 5 nodes) to prevent split-brain disasters. To prevent one slow dependency from crashing our entire microservice fleet, we protect network calls with aggressive timeouts, circuit breakers that fail fast during outages, and exponential backoff with random jitter to spread out retries."
