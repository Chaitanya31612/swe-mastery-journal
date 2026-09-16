# Caching Strategies & Invalidation: Comprehensive Solutions & System Designs (Phase 6)

This document provides complete architectural specifications, invalidation mechanisms, and edge-caching designs for the 3 Practice Scenarios in [`01-caching-strategies-and-invalidation.md`](./01-caching-strategies-and-invalidation.md).

---

## Scenario 1: Breaking News Headline Banner

### 1. The Scenario
* A major news platform publishes an urgent banner: *"Earthquake in Tokyo"*.
* **The Traffic:** 20 Million users reload the homepage in the next 15 minutes ($\approx 22,000\text{ QPS}$ surging to $60,000\text{ QPS}$).
* **The Constraint:** Editors may correct a typo in the headline within 3 minutes.

### 2. Comprehensive Caching Architecture

| Dimension | Architectural Decision |
|---|---|
| **1. Should we cache this?** | **YES, ABSOLUTELY.** Uncached traffic would hit origin servers at 60,000 QPS and immediately collapse the database. |
| **2. Where should it live?** | **Two-Tier Cache: CDN Edge (Cloudflare/Fastly) + Application Reverse Proxy (Varnish/Envoy in front of web pods).** Minimal/no browser cache! |
| **3. What should the TTL be?** | **Short Edge TTL: 15 to 30 Seconds** with `stale-while-revalidate=60`. |
| **4. Invalidation Method:** | **Surrogate-Key / Cache-Tag Purge via Webhook (Event-Driven Edge Invalidation).** |

### 3. Detailed Engineering Rationale
* **Why NOT the Browser Cache?**
  * If you set `Cache-Control: max-age=3600` on 20 million client browsers, and an editor fixes a typo 2 minutes later, you **cannot invalidate client browser caches**! Those 20 million users will see the embarrassing typo for an hour until their local timers expire. Browser caching for live news banners must be set to `Cache-Control: no-cache, must-revalidate` or `max-age=5`.
* **The Power of CDN Edge Caching:**
  * Placing the headline on CDN edge servers in Tokyo, London, and New York collapses 60,000 QPS down to $< 10\text{ QPS}$ at your origin database ($99.98\%$ Cache Hit Ratio).
* **The Invalidation Flow (Instant CMS Purge):**
  1. The CMS attaches a Cache-Tag / Surrogate-Key header when publishing:
     ```http
     Surrogate-Key: breaking-banner news-urgent-101
     Cache-Control: public, s-maxage=300, stale-while-revalidate=60
     ```
  2. When the editor clicks "Save Typo Correction" in the CMS, a webhook sends an instantaneous API purge call to the CDN API:
     ```bash
     curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
          -H "Authorization: Bearer $API_TOKEN" \
          -d '{"tags": ["breaking-banner"]}'
     ```
  3. The CDN flushes the cached object worldwide in **under 150 milliseconds**. The very next edge request pulls the updated text.

---

## Scenario 2: User Shopping Cart

### 1. The Scenario
* A customer browses an online clothing store, adding, updating, and removing shirts over a 30-minute shopping session.

### 2. Comprehensive Caching Architecture

| Dimension | Architectural Decision |
|---|---|
| **1. Should we cache this?** | **YES.** But strictly scoped per user session; never shared publicly. |
| **2. Where should it live?** | **Distributed In-Memory Cache (Redis Cluster) + Local Client State (React/Redux/Mobile Memory).** NEVER on a CDN! |
| **3. What should the TTL be?** | **Rolling TTL of 7 to 30 Days** (or 2 hours of inactivity; refreshed on every cart interaction). |
| **4. Invalidation Method:** | **Write-Through Invalidation / Direct Key Mutation (Never stale-read cart contents).** |

### 3. Detailed Engineering Rationale
* **Why NEVER on a CDN?**
  * A CDN is a public shared proxy. If a developer accidentally caches `GET /api/cart` on a CDN without proper `Vary: Authorization` or `Cache-Control: private`, Customer B will see Customer A's shopping cart, names, and delivery addresses (a catastrophic GDPR / security breach).
* **The Redis Key-Value Design:**
  * Cart state is keyed by authenticated `user_id` or anonymous session cookie:
    ```bash
    cart:user_83921 -> JSON blob [{"item_id": 101, "qty": 2, "price": 29.99}]
    ```
* **The Mutation Flow:**
  * When the user clicks "Add to Cart":
    1. Update the cart in Redis:
       ```bash
       SET cart:user_83921 "<json_payload>" EX 604800
       ```
    2. Asynchronously stream cart state changes to an underlying persistent database (e.g., PostgreSQL or DynamoDB) using the **Write-Behind** pattern or write to both in a transactional boundary.
    3. If the user clears their cart or finishes checkout, explicitly run `DEL cart:user_83921`.

---

## Scenario 3: Live Currency Exchange Rates (USD to EUR)

### 1. The Scenario
* Forex market rates that fluctuate every **250 milliseconds**, used by currency traders to execute live financial trades.

### 2. Comprehensive Caching Architecture

| Dimension | Architectural Decision |
|---|---|
| **1. Should we cache this?** | **FOR READS/UI DISPLAY: YES (Micro-Cache). FOR TRADE EXECUTION: NO (Zero Cache / Strict Source of Truth).** |
| **2. Where should it live?** | **In-Memory Local Server RAM / WebSockets / Redis Pub/Sub stream.** NEVER in traditional HTTP caches with long TTLs. |
| **3. What should the TTL be?** | **Sub-Second Micro-Cache: 100ms to 250ms (or continuous push via WebSocket/SSE).** |
| **4. Invalidation Method:** | **Continuous Stream Replacement (Event Stream from Market Ticker).** |

### 3. Detailed Engineering Rationale
* **The Critical Separation of Concerns:**
  * **The UI / Chart Display Flow (Micro-Caching):**
    * Millions of users watching market tickers on their phones do not need to query the clearinghouse database on every tick.
    * Ingest the live Forex feed into an in-memory Redis cluster or memory buffer. Micro-cache the price for **250 milliseconds**.
    * Push updates to client applications over persistent **WebSockets or Server-Sent Events (SSE)**.
  * **The Trade Execution Flow (ZERO Caching):**
    * When a trader clicks *"Exchange \$1,000,000 USD to EUR"*, you **MUST NOT use a cached price**!
    * If you use a 3-second-old cached exchange rate of `1.0850` while the live market has moved to `1.0820`, the brokerage incurs an immediate massive financial loss (arbitrage exploitation).
    * Trade execution endpoints must bypass all caches, acquire an exclusive market lock or order book snapshot, validate the quote with the central matching engine, and commit the transaction atomically.

---

## Summary Strategy Matrix

| Scenario | Cacheable? | Target Location | TTL | Invalidation Protocol |
|---|---|---|---|---|
| **1. Breaking News Banner** | Yes (High value) | CDN Edge (Cloudflare) | 15–30s (`s-maxage`) | Webhook Cache-Tag Purge |
| **2. User Shopping Cart** | Yes (Per user) | Redis In-Memory Store | 7–30 Days (Rolling) | Explicit `DEL` or `SET` on mutation |
| **3. Live Forex Rates (Display)** | Yes (Micro-cache) | WebSocket / Redis RAM | 100–250ms | Stream tick replacement |
| **3. Live Forex Rates (Trade)** | **NO** | Origin Matching Engine | **0s (No Cache)** | Direct transactional execution |
