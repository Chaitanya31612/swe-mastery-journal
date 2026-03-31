# 🎬 Problem 06: Movie Ticket Booking System (BookMyShow)

> **Frequency:** 🟡 P1 | **Time:** 90 min | **Difficulty:** ⭐⭐⭐⭐

---

## 📋 Requirements

### Must-Have (Core)
1. Multiple **theatres**, each with multiple **screens**
2. Each screen has multiple **shows** per day
3. Shows have a **seat map** with different categories (Silver, Gold, Platinum)
4. Users can **search** shows by movie, city, theatre
5. Users can **select seats** and **book** tickets
6. Handle **concurrent bookings** — two users shouldn't book same seat
7. Generate **booking confirmation** with ticket details

### Nice-to-Have
- Payment processing
- Cancellation with refund
- Offers/discounts
- Waitlist for sold-out shows

---

## 🧩 Key Entities

```
Theatre, Screen, Show, Movie, Seat, SeatType, Booking,
BookingStatus, Payment, User, ShowManager
```

## 🏗️ Class Diagram

```
┌─────────┐    ┌────────┐    ┌──────┐    ┌──────┐
│ Theatre │1─*│ Screen │1─*│ Show │*─1│ Movie│
├─────────┤    ├────────┤    ├──────┤    ├──────┤
│ -name   │    │ -seats │    │ -time│    │-title│
│ -city   │    │ -id    │    │ -date│    │-genre│
│ -screens│    └────────┘    │-movie│    └──────┘
└─────────┘                  │-seats│
                             └──────┘
┌──────────┐                           ┌──────────┐
│  Booking │*────────────────────────1│   User   │
├──────────┤                           ├──────────┤
│ -show    │                           │ -name    │
│ -seats   │  ┌──────────────────┐     │ -email   │
│ -status  │  │  <<interface>>   │     └──────────┘
│ -amount  │  │ BookingService   │
│ -user    │  ├──────────────────┤
└──────────┘  │ +bookSeats()     │
              │ +cancelBooking() │
              └──────────────────┘
```

## 🎯 Patterns Used

| Pattern | Where | Why |
|---|---|---|
| **State** | BookingStatus (Pending → Confirmed → Cancelled) | Status transitions |
| **Strategy** | Pricing (by seat type, time of day) | Different pricing rules |
| **Singleton** | BookingService | Centralized booking management |
| **Observer** | Notifications on booking confirmation | Email/SMS alerts |

## 🔑 Key Design Decisions
- **Concurrency** — Use `synchronized` on seat selection or `ConcurrentHashMap` for seat locks
- **Seat locking** — Temporarily lock seats during booking flow (with timeout)
- **Separation** — Search logic separate from booking logic
- **Idempotency** — Same booking request shouldn't create duplicate bookings

## 📁 Code Structure
```
src/
├── model/
│   ├── Theatre.java
│   ├── Screen.java
│   ├── Show.java
│   ├── Movie.java
│   ├── Seat.java
│   ├── SeatType.java
│   ├── Booking.java
│   ├── BookingStatus.java
│   └── User.java
├── service/
│   ├── BookingService.java
│   ├── SearchService.java
│   └── PricingService.java
├── exception/
│   ├── SeatAlreadyBookedException.java
│   └── ShowFullException.java
└── BookingDemo.java
```
