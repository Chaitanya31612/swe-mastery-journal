# Practical Architectural Security: Comprehensive Solutions & Mitigation (Phase 13)

This document provides detailed defense-in-depth solutions and edge security architectures for the Practice Promo Code Loop Scenario in [`01-practical-architectural-security.md`](./01-practical-architectural-security.md).

---

## Scenario: The Anonymous Discount Code Loop (Promo Code Brute-Force Bot)

### 1. The Threat Model & Attack Vector
* **The Endpoint:** `POST /apply-promo {"code": "FREESHIP"}`.
* **The Attack:** A volumetric brute-force bot tests **500,000 randomized 6-character strings per minute** ($\approx 8,333\text{ requests/second}$) to discover unpublished promotional codes (e.g., employee discounts, influencer VIP codes).
* **The Vulnerability:** High volumetric resource exhaustion and automated coupon enumeration.

---

## Question 1: Where Should You Block This Bot?

### 1. The Architectural Verdict
**At the Edge / API Gateway / Cloudflare Web Application Firewall (WAF) — The Outer Perimeter.**

### 2. Deep Defense-in-Depth Comparison

| Layer | Viability | Architectural Impact |
|---|---|---|
| **❌ The Database** | **CATASTROPHIC** | If 8,333 queries/sec reach the database to execute `SELECT * FROM promo_codes WHERE code = :code`, the database CPU hits 100%, saturates the connection pool, and knocks down the entire e-commerce store. Using the database as a security firewall is a critical anti-pattern. |
| **❌ The Application Code** | **POOR** | Letting 500,000 HTTP requests/min hit Python/Node.js/Ruby application pods forces the OS to handle TLS handshakes, allocate request memory buffers, and consume worker threads, slowing down legitimate checkout traffic. |
| **✅ The Edge / API Gateway / WAF** | **OPTIMAL** | Blocking traffic at the Cloudflare edge or API Gateway (Envoy/Kong) drops packets **before they ever touch your private VPC or compute servers**. The attack is absorbed on the cloud provider's global network backbone ($0\text{ backend CPU}$ consumed). |

```
[ Attacker Bot: 8,333 req/sec ]
               |
               v
+----------------------------------------------------+
|  EDGE WAF / API GATEWAY (Cloudflare / Envoy)       |
|                                                    |
|  * Token Bucket Rate Limiting (Blocked in 2s!)     |
|  * TLS / IP Reputation / Bot Fingerprinting        |
|  * Managed Challenge / CAPTCHA                     |
|                                                    |
|  Status: HTTP 429 Too Many Requests                |
+----------------------------------------------------+
               | (Only legitimate, throttled traffic passes)
               v
     [ Internal Backend Fleet & Database: 100% Protected ]
```

---

## Question 2: What Specific Technique Stops This in 2 Seconds?

Stopping a distributed brute-force attack in seconds requires a combination of **algorithmic rate limiting and behavioral challenges**:

### 1. Edge-Based Token Bucket Rate Limiting with IP & Session Keys
* Configure a strict rate limit on the `/apply-promo` path at the API Gateway / Cloudflare WAF:
  * **Threshold:** Allow a maximum burst of **5 attempts per minute** per client IP / authenticated session:
    $$\text{Rate Limit} = 5\text{ requests} / 60\text{ seconds}$$
  * After 5 failed attempts, immediately return `HTTP 429 Too Many Requests` with a `Retry-After: 60` header.
* **Why it works in 2 seconds:**
  * The bot sends requests at 8,333 req/sec.
  * Within the first **2 milliseconds**, the bot consumes all 5 tokens in its bucket.
  * The remaining 499,995 requests over the minute are instantly rejected at the CDN edge without touching origin servers.

### 2. Cloudflare Turnstile / Managed CAPTCHA Challenge
* If the bot distributes requests across 50,000 residential proxy IPs (bypassing simple per-IP rate limits):
  * Trigger an automated **JavaScript cryptographic proof-of-work (Cloudflare Turnstile / Managed Challenge)** after any client fails 2 promo code lookups consecutively.
  * Legitimate humans solve the invisible browser challenge in 100ms; automated headless curl/Python scripts cannot execute browser JavaScript and are permanently blocked.

### 3. Progressive Delays (Exponential Backoff Penalty)
* Track failed code attempts in an in-memory Redis counter:
  * Attempt 1 failed: Delay response by 0ms.
  * Attempt 2 failed: Delay response by 500ms.
  * Attempt 3 failed: Delay response by 2,000ms.
  * Attempt 5+ failed: Lock the user's promo code submission form for 15 minutes.
* This dramatically destroys the economic viability of brute-force dictionary attacks.

### 4. Code Entropy Best Practice
* As an additional architectural defense, avoid short 6-letter promo codes like `VIP101` for high-value promotions. Use high-entropy keys (e.g., `SAVE-9F8A-32BC-7E11`) with $62^8$ combinations, rendering random guessing mathematically futile.
