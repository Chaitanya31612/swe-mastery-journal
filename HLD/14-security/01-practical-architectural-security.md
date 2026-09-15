# Practical Security: Keycard Badges, Token Buckets & Zero Trust

---

## Mental Model: The Castle Moat vs. Keycard Office Badges

For decades, software security followed the **"Castle-and-Moat"** model:
* Build a huge stone wall and a deep moat around your company network (**The Firewall**).
* Once an employee or packet crosses the drawbridge into the private internal network, **everything inside is trusted 100%**.
* **The Catastrophe:** If an attacker gets into one tiny, non-critical marketing printer on the Wi-Fi, they can walk straight into the bank ledger database without anyone stopping them!

Modern architecture enforces **Zero Trust ("Never Trust, Always Verify")**:
* Think of a secure government laboratory or modern tech office:
* There are no open doors. **Every single doorway requires swiping your badge**, even when walking between two adjacent desks inside the building.
* When Service A calls Service B inside your own private cloud, Service B checks Service A's cryptographic badge (**mTLS: Mutual TLS**) before sharing any data.

```
                    [ HOSTILE PUBLIC INTERNET ]
                                 |
                          [ HTTPS / TLS 1.3 ]
                                 |
                                 v
               +------------------------------------+
               | API GATEWAY (Front Door Security)  |
               | - Token Bucket Rate Limiting       |
               | - Blocks SQL Injection / Bad Bots  |
               | - Validates User Login Token       |
               +------------------------------------+
                                 |
               [ INTERNAL PRIVATE VPC (Zero Trust!) ]
                                 |
                   (mTLS: Encrypted Badge Swipes)
                                 |
         +-----------------------+-----------------------+
         |                                               |
         v                                               v
+------------------------+                     +------------------------+
| Order Service          | --(mTLS Badge Check)->| Payment Service        |
| - Can only touch orders|                     | - Only accepts calls   |
|   database             |                     |   from authorized pods |
+------------------------+                     +------------------------+
```

---

## Stateless JWTs vs. Stateful Sessions: The Concert Wristband

How does a website remember who you are when you click from page to page?

### 1. Stateless JWT (The Holographic Wristband)
* You buy a VIP ticket at a music festival. The guard puts a tamper-proof plastic wristband on your arm stamped with: *"Name: Alice, VIP Area Access, Valid until 11:00 PM"*.
* Every time you walk past a stage guard, they glance at the holographic stamp. It's legitimate, so they let you in immediately!
* **Superpower:** The guard **does not need to call headquarters or check a database**! Any server can verify the digital signature in 0.1ms using pure math.
* **The Catch (Revocation is Hard):** What if you start causing a fight inside the festival? The guard can't "un-stamp" your wristband unless they post your photo on a physical blacklist board at every tent. A stolen JWT remains valid until its expiration timer runs out!

### 2. Stateful Session (The Hotel Room Keycard)
* You get an unlabelled plastic card with a random number.
* Every single time you swipe it at your door, the lock calls the central front desk computer: *"Is Card #412 valid for Room 204 right now?"*
* **Superpower (Instant Revocation):** If you lose your card, the front desk cancels it on the computer, and it instantly stops working everywhere.
* **The Catch:** Every single click on your website must make a network call to your Redis session database.

### The Production Sweet Spot:
Use **short-lived JWTs (15-minute expiration)** for fast, database-free API calls, paired with a **long-lived Refresh Token in Redis** that can be canceled whenever a user logs out!

---

## Token Bucket Rate Limiting: The Arcade Game Dispenser

How do you stop bots from hammering your login page 10,000 times a second?

Think of a **Token Bucket**:
* You have a bucket that holds up to **10 tokens**.
* Every second, the system drops **2 new tokens** into the bucket.
* When a user makes an API call, it takes **1 token** out of the bucket.
* **If tokens are available:** The request goes through!
* **If the bucket is empty:** The user made too many requests too fast! The system immediately returns `429 Too Many Requests` (*"Please wait 5 seconds"*).

```
[ Incoming Requests ] ---> Takes 1 token ---> [ Bucket (Max 10) ]
                                                     |
                                            Are tokens left?
                                            /              \
                                         (YES)             (NO)
                                          /                  \
                                   [ Allow API call ]   [ Return 429 Error ]
```

* **Why it's awesome:** It naturally allows brief bursts of activity (like a user rapidly clicking 5 items into their cart), while strictly preventing sustained, automated abuse!

---

## The #1 API Security Bug: BOLA / IDOR Explained

What is **Broken Object-Level Authorization (BOLA)**, and why does it cause 80% of data leaks?

Imagine you are logged into your bank account:
* You click "View Statement" and the URL is:  
  `GET /api/statements?id=1001`
* You wonder what happens if you change the number in the browser URL to:  
  `GET /api/statements?id=1002`
* **The Disaster:** The backend server checks: *"Is this user logged in? Yes, valid JWT!"* But it **forgets to check if Statement 1002 actually belongs to you!**
* The server sends you someone else's private bank statement. A hacker writes a 5-line script looping from `id=1` to `id=1000000` and steals every bank statement in the company!

### The Fix in Code:
Always enforce ownership in your database query:
```sql
-- WRONG:
SELECT * FROM statements WHERE id = :statement_id;

-- RIGHT:
SELECT * FROM statements 
WHERE id = :statement_id AND user_id = :authenticated_user_id;
```

---

## Practice: Spot the Security Hole

### Scenario: The Anonymous Discount Code Loop
An e-commerce site has an endpoint `POST /apply-promo {"code": "FREESHIP"}`.
A user writes a bot that tries 500,000 random letter combinations a minute to discover unannounced secret discount codes.
* **Where should you block this bot? (In the database, in the app code, or at the API Gateway/Cloudflare?)**
* **What specific technique stops this in 2 seconds?**

---

## 60-Second Summary

> "Practical security is built on Zero Trust: never assume internal traffic is safe, and verify identity at every boundary using mutual TLS. We protect our APIs at the front door using Token Bucket rate limiting to stop volumetric scrapers, authenticate users via short-lived cryptographic tokens, and always enforce strict object-level authorization so users can only ever access their own data. By giving every service only the bare minimum permissions it needs (Least Privilege), we ensure that if any single container is compromised, the blast radius is tightly locked down."
