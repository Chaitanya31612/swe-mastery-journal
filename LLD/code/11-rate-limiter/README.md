# 🚦 Problem 11: Rate Limiter

> **Frequency:** 🟢 P2 | **Time:** 90 min | **Difficulty:** ⭐⭐⭐

---

## 📋 Requirements

### Must-Have (Core)
1. Limit number of **requests per user** in a **time window**
2. **Token Bucket** algorithm: fixed capacity, tokens refill at constant rate
3. **allowRequest(userId)** → returns `true` if allowed, `false` if rate-limited
4. Configurable **capacity** and **refill rate**
5. Per-user rate limiting

### Nice-to-Have
- Sliding Window Log algorithm (alternative)
- Sliding Window Counter (hybrid)
- Different limits per API endpoint
- Distributed rate limiting
- Rate limit headers (remaining, reset time)

---

## 🧩 Key Entities

```
RateLimiter (interface), TokenBucketLimiter, SlidingWindowLimiter,
UserBucket, RateLimiterConfig
```

## 🎯 Patterns Used

| Pattern | Where | Why |
|---|---|---|
| **Strategy** | RateLimiter implementations | Swap algorithms |
| **Factory** | RateLimiterFactory | Create limiter by algorithm type |

## 🔑 Token Bucket Algorithm
```
Bucket capacity = 10 tokens
Refill rate = 1 token/second

Timeline:
t=0:  [10 tokens] → Request → [9 tokens] ✅ ALLOWED
t=0:  [9 tokens]  → Request → [8 tokens] ✅ ALLOWED
...
t=0:  [1 token]   → Request → [0 tokens] ✅ ALLOWED
t=0:  [0 tokens]  → Request → [0 tokens] ❌ RATE LIMITED
t=1:  [1 token]   → (refilled) → Request → [0 tokens] ✅ ALLOWED
```

## 📁 Code Structure
```
src/
├── model/
│   ├── UserBucket.java
│   └── RateLimiterConfig.java
├── limiter/
│   ├── RateLimiter.java
│   ├── TokenBucketLimiter.java
│   └── SlidingWindowLimiter.java
├── factory/
│   └── RateLimiterFactory.java
└── RateLimiterDemo.java
```
