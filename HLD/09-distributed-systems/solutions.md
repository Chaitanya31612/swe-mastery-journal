# Distributed Systems & Consensus: Comprehensive Solutions & Failure Scenarios (Phase 8)

This document provides rigorous mathematical explanations and architectural mitigations for the Practice Failure Scenarios in [`01-distributed-fundamentals-and-consensus.md`](./01-distributed-fundamentals-and-consensus.md).

---

## Scenario 1: The Cascading Timeout (Thread Exhaustion & The Domino Effect)

### 1. The Scenario Parameters
* **Service A Capacity:** Fixed worker pool of **100 threads**.
* **Communication:** Synchronous HTTP/gRPC call to Service B.
* **Service B Latency:** Spikes from **20ms** to **15,000ms (15 seconds)**.
* **Incoming Ingress Traffic:** **50 requests per second** continuous.

### 2. Math & Physics: What Happens to Service A Within 3 Seconds?

Applying **Little's Law** from queuing theory:
$$\mathbf{L = \lambda \times W}$$
*(Where $L$ is the number of concurrent requests in the system, $\lambda$ is arrival rate, and $W$ is average processing time).*

* **Under Normal Operation ($W = 20\text{ms} = 0.02\text{s}$):**
  $$L = 50\text{ req/sec} \times 0.02\text{s} = 1\text{ thread in use}$$
  Service A is relaxed; 99 threads sit idle ready to serve traffic.

* **During the Service B Outage ($W = 15\text{ seconds}$):**
  * **Second 1:** 50 new requests arrive. All 50 threads call Service B and block on socket reads. Threads in use: **50 / 100**.
  * **Second 2:** Another 50 new requests arrive. All 50 remaining threads call Service B and block. Threads in use: **100 / 100**.
  * **Second 3:** Another 50 new requests arrive. Service A has **zero available threads**.
* **The Catastrophic Outcome within 3 Seconds:**
  * **Total Thread Starvation:** Every single worker thread is frozen waiting on Service B.
  * **Socket Backlog Overflows:** Incoming TCP connections queue up in the OS `listen` backlog until the queue overflows, at which point the OS kernel sends `TCP RST` (Connection Refused).
  * **Cascading Upstream Collapse:** Upstream API Gateways or clients calling Service A experience timeouts and fail. Service A is now completely dead, even though its CPU utilization is $< 5\%$!

### 3. The Two Safety Valves That Stop the Collapse

#### Safety Valve 1: Strict Request Timeouts & Deadlines
* **Never make an unbounded network call!**
* Configure a tight timeout on the Service B client (e.g., `timeout = 500ms`):
  * Instead of waiting 15 seconds, threads wait at most 500ms before abandoning the call and throwing a `TimeoutException`.
  * Threads are recycled back to the pool $30\times$ faster:
    $$L = 50\text{ req/sec} \times 0.5\text{s} = 25\text{ threads}$$
  * Service A uses only 25 threads, leaving 75 threads completely free to handle other traffic.

#### Safety Valve 2: The Circuit Breaker Pattern (e.g., Resilience4j, Envoy)
* A circuit breaker monitors error/timeout rates to Service B over a rolling window.
* **Tripping the Circuit:** If $> 50\%$ of calls to Service B time out over a 10-second period, the breaker switches from **CLOSED** to **OPEN**.
* **Failing Fast ($< 1\text{ms}$):**
  * When OPEN, Service A **does not make any network calls to Service B**.
  * It immediately fails fast or returns a graceful degraded response (e.g., fallback cached data or default payload).
  * Thread consumption drops to near zero, completely shielding Service A from Service B's death.
* **Half-Open Recovery:** After a sleep window (e.g., 30s), the breaker lets a single trial request pass through. If Service B responds quickly, the breaker resets to CLOSED.

```
[ Normal: CLOSED ] ----(Failures > 50%)----> [ Outage: OPEN (Fail Fast) ]
        ^                                                    |
        |                                             (Wait 30 seconds)
        |                                                    |
        +-------(Success)------ [ HALF-OPEN ] <--------------+
```

---

## Scenario 2: The Two Roommates and the Milk (The Concurrency Race Condition)

### 1. The Scenario
* Both Roommates (Server 1 and Server 2) receive a trigger:
  $$\text{"If milk quantity is 0, buy 1 gallon of milk."}$$
* Both servers check the database at the exact same millisecond: both read `quantity = 0`.
* Both order milk. Result: 2 gallons of milk delivered (wasted money).
* **The Questions:**
  * What is this bug called?
  * How do you fix it?

### 2. The Name of the Bug
This bug is officially called a **Race Condition**, specifically the classic **"Check-Then-Act" (Time-of-Check to Time-of-Use — TOCTOU)** anti-pattern.

* **Why it happens:** The verification step (checking if quantity is 0) and the execution step (ordering milk / setting quantity to 1) are executed as separate, non-atomic operations. Between the check and the act, another concurrent process intervenes and mutates the shared state.

```
Time   Server 1 (Roommate 1)               Server 2 (Roommate 2)
 |
 |--- Read DB: quantity == 0 (True)
 |                                          Read DB: quantity == 0 (True)
 |--- Order 1 Gallon of Milk ($$)
 |                                          Order 1 Gallon of Milk ($$)  <-- DUPLICATE!
 v--- Write DB: quantity = 1                Write DB: quantity = 1
```

### 3. How to Fix It (3 Production Patterns)

#### Fix 1: Atomic Database Conditional Update (Compare-And-Swap — CAS)
Push the decision directly into the single source of truth—the database storage engine:
```sql
UPDATE inventory 
SET quantity = 1, ordered_by = 'Server_1'
WHERE item = 'milk' AND quantity = 0;
```
* **Why this works:** The database evaluates the `WHERE` clause and applies the `UPDATE` while holding an internal row-level lock.
* Only the first server's query updates 1 row (`Rows Affected: 1`) $\to$ Server 1 buys milk.
* The second server's query finds `quantity = 1` and updates 0 rows (`Rows Affected: 0`) $\to$ Server 2 aborts without buying milk!

#### Fix 2: Explicit Row-Level Pessimistic Locking (`SELECT FOR UPDATE`)
In an ACID relational database:
```sql
BEGIN;
SELECT quantity FROM inventory WHERE item = 'milk' FOR UPDATE;
-- Server 1 acquires exclusive lock; Server 2 blocks until Server 1 commits!
IF quantity == 0 THEN
    UPDATE inventory SET quantity = 1 WHERE item = 'milk';
    -- Trigger purchase
END IF;
COMMIT;
```

#### Fix 3: Distributed Mutual Exclusion Lock (e.g., Redis Redlock / etcd)
If the coordination spans multiple non-database systems or external APIs:
1. Server 1 attempts to acquire an atomic distributed lock:
   ```bash
   SET lock:buy_milk "server_1_id" NX PX 5000
   ```
   *(The `NX` flag means: Only set if the key does NOT already exist; `PX 5000` sets a 5-second automatic lease expiration).*
2. Server 1 acquires the lock (`OK`), checks the inventory, orders milk, and releases the lock.
3. Server 2's `SETNX` call returns `nil` (lock already held). Server 2 backs off and skips the purchase.
