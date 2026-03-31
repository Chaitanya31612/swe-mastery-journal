# 🚗 Problem 10: Ride Sharing System (Uber/Ola)

> **Frequency:** 🟢 P2 | **Time:** 90 min | **Difficulty:** ⭐⭐⭐⭐

---

## 📋 Requirements

### Must-Have (Core)
1. **Riders** request rides with pickup and drop-off locations
2. **Drivers** can go online/offline and accept/reject rides
3. **Match** rider with nearest available driver
4. Ride has states: **REQUESTED → ACCEPTED → IN_PROGRESS → COMPLETED**
5. **Fare calculation** based on distance (base fare + per-km rate)
6. Track ride status updates

### Nice-to-Have
- Multiple vehicle types (Auto, Mini, Sedan, SUV) with different pricing
- Surge pricing during peak demand
- Driver rating system
- Ride history

---

## 🧩 Key Entities

```
Rider, Driver, Ride, RideStatus, Location, RideManager,
MatchingStrategy, PricingStrategy
```

## 🎯 Patterns Used

| Pattern | Where | Why |
|---|---|---|
| **Strategy** | MatchingStrategy (nearest, highest-rated) | Swap matching logic |
| **Strategy** | PricingStrategy (flat, distance-based, surge) | Swap pricing logic |
| **Observer** | Ride status updates | Notify rider/driver of changes |
| **State** | RideStatus transitions | Behavior per ride state |

## 📁 Code Structure
```
src/
├── model/
│   ├── Rider.java
│   ├── Driver.java
│   ├── Ride.java
│   ├── RideStatus.java
│   ├── Location.java
│   └── VehicleType.java
├── strategy/
│   ├── MatchingStrategy.java
│   ├── NearestDriverStrategy.java
│   ├── PricingStrategy.java
│   └── DistancePricingStrategy.java
├── service/
│   └── RideManager.java
└── RideSharingDemo.java
```
