# Asynchronous Systems: Comprehensive Solutions & Flow Architecture (Phase 7)

This document provides architectural analyses, execution path designs, and trade-off rationales for the 4 Practice Flows in [`01-queues-pubsub-and-event-driven.md`](./01-queues-pubsub-and-event-driven.md).

---

## Flow 1: Clicking "Forgot Password"

### 1. Architectural Verdict
**Hybrid Pattern: Synchronous Validation $\longrightarrow$ Asynchronous Email Delivery**

### 2. Deep Technical Breakdown & Explanation
* **The Synchronous Step ($< 20\text{ms}$):**
  * When the user clicks "Send Reset Link", the web server synchronously validates the email format, looks up the user account, generates a cryptographically secure, time-limited reset token (UUIDv4/HMAC), and saves the token hash and expiration timestamp into the database.
  * The HTTP response immediately returns `HTTP 200 OK` with: *"If an account exists with this email, a password reset link has been sent."* (Preserving user privacy against account enumeration attacks).
* **The Asynchronous Step (Background Queue):**
  * Actually transmitting the email over SMTP via SendGrid, Mailgun, or AWS SES must be **Asynchronous via a Message Queue (AWS SQS / RabbitMQ)**.
  * **Why It Must Be Async:** Third-party email APIs frequently take 1,000ms to 4,000ms to process an SMTP handshake. If the email provider suffers an outage or rate-limits your API, holding the user's browser in a synchronous HTTP wait state will cause user-facing timeouts.
  * Placing the email job on a persistent queue decouples user feedback from email network flakiness. If SendGrid is down, the message retries safely in the background with exponential backoff until delivered.

---

## Flow 2: ATM Cash Withdrawal

### 1. Architectural Verdict
**Strictly Synchronous (Atomic Transaction with Physical Confirmation)**

### 2. Deep Technical Breakdown & Explanation
* **Why It Must Be Synchronous:**
  * An ATM withdrawal involves a physical interaction with real currency in the real world. You cannot give the user a background promise ticket: *"Thanks! We've queued your withdrawal. Come back in 10 minutes to see if cash dispenses."*
  * The system must verify the PIN, confirm sufficient account balance, and acquire an exclusive row lock on the customer's ledger **in real time**.
* **The Two-Phase Physical Handshake:**
  1. **Step 1 (Sync DB Lock):** The central core banking system locks the funds:
     ```sql
     UPDATE accounts SET balance = balance - 100 WHERE id = 42 AND balance >= 100;
     ```
  2. **Step 2 (Sync Hardware Dispense):** The ATM machine dispenses the 5 physical \$20 bills into the customer's hands.
  3. **Step 3 (Sync Confirmation):** Only after the ATM optical sensors confirm the cash was physically pulled from the slot does the system commit the transaction.
  * If the ATM runs out of bills or jams, the transaction rolls back immediately and credits the account back in the same synchronous session. Asynchronous processing here would create massive financial fraud risks and customer disputes.

---

## Flow 3: Uploading a YouTube Video

### 1. Architectural Verdict
**Asynchronous Event Pipeline (Worker Queues & Directed Acyclic Graph - DAG)**

### 2. Deep Technical Breakdown & Explanation
* **Why Synchronous Processing Collapses:**
  * Transcoding a 2 GB 4K video file into multiple resolutions (1080p, 720p, 480p, 360p), extracting audio tracks, generating preview GIF thumbnails, and running copyright content-ID scans requires **billions of CPU cycles and takes anywhere from 2 to 30 minutes**.
  * No HTTP connection can stay open for 30 minutes; browsers, mobile networks, and reverse proxies (Nginx/ALB) will terminate the socket with `504 Gateway Timeout`.
* **The Production Asynchronous Flow:**
  1. **Direct Upload:** Client streams the raw video file directly into an Amazon S3 bucket via an S3 Pre-Signed URL ($0\text{ app server CPU}$).
  2. **Event Notification:** Upon upload completion, S3 emits an `s3:ObjectCreated` event to an SNS topic / SQS queue.
  3. **DAG Worker Fleet (Temporal / Celery / AWS Batch):** A fleet of GPU-accelerated video worker pods pull jobs from the queue. They download the raw file, process encodings in parallel, and store chunked HLS segments back to S3.
  4. **Client Notification:** The user's creator studio dashboard polls or listens to a WebSocket: *"Processing: 45% complete..."*. The user can close their laptop and walk away; the job safely completes in the cloud.

---

## Flow 4: Reserving a Hotel Room

### 1. Architectural Verdict
**Strictly Synchronous Reservation Lock (Preventing Double-Booking)**

### 2. Deep Technical Breakdown & Explanation
* **The High-Contention Constraint:**
  * There is only **one physical Room 204**. Two other users are currently on the payment screen looking at the same room for the same date.
* **Why It Must Be Synchronous:**
  * If you push reservation requests to an asynchronous queue and return a cheerful *"We are processing your reservation!"* to all three users, all three will enter credit card information.
  * When the asynchronous worker finally processes the queue 5 seconds later, it discovers User 1 took the room, forcing the system to apologize and process refunds for Users 2 and 3. This destroys customer trust.
* **The Production Pattern (Synchronous Short-Term Hold):**
  1. The moment the user clicks "Reserve", make a **synchronous database call** to acquire an exclusive temporary hold:
     ```sql
     UPDATE rooms 
     SET status = 'HELD', held_until = NOW() + INTERVAL '10 MINUTES', held_by_user = 'u101'
     WHERE room_id = 204 AND date = '2026-10-01' AND (status = 'AVAILABLE' OR held_until < NOW());
     ```
  2. If the row update succeeds (1 row affected), return `HTTP 200 OK` and start a 10-minute checkout timer.
  3. If another user was faster, the query affects 0 rows; immediately inform the user synchronously: *"Sorry, someone just reserved this room 2 seconds ago!"*.
  4. Only non-essential post-booking steps (sending the confirmation email, updating marketing analytics) are offloaded to asynchronous queues.

---

## Summary Decision Matrix

| Flow | Execution Mode | User Latency Expectation | Failure Mode / Blast Radius If Misconfigured |
|---|---|---|---|
| **1. Forgot Password** | Sync token gen $\to$ Async email | $< 100\text{ms}$ UI response | If fully sync: third-party email outage breaks user login portal |
| **2. ATM Cash Dispense** | Strictly Synchronous | $< 3\text{ seconds}$ | If async: customer leaves ATM before cash dispenses or double-spends |
| **3. YouTube Transcoding** | Strictly Asynchronous | Minutes to hours | If sync: HTTP timeout after 60s; web server RAM/CPU exhaustion |
| **4. Hotel Room Booking** | Strictly Synchronous Lock | $< 500\text{ms}$ | If async: catastrophic double-booking of physical hotel rooms |
