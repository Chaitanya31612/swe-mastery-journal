# 🅿️ Problem 01: Parking Lot System

> **Frequency:** 🔴 #1 Most Asked | **Time:** 90 min | **Difficulty:** ⭐⭐⭐

---

## 📋 Requirements

### Must-Have (Core)
1. Parking lot has multiple **floors**, each floor has multiple **parking spots**
2. Three types of spots: **Small**, **Medium**, **Large**
3. Three types of vehicles: **Bike**, **Car**, **Truck**
4. Vehicle can only park in a spot that fits it (Bike → Small, Car → Medium, Truck → Large)
5. On parking → generate a **Ticket** with entry time
6. On unparking → calculate **price** based on duration
7. Display **availability** per floor and spot type

### Nice-to-Have (Extensions)
- Multiple entry/exit gates
- Different pricing strategies (hourly, daily, flat-rate)
- Electric vehicle spots with charging
- Handicapped spots priority

---

## 🧩 Key Entities

```
ParkingLot, Floor, ParkingSpot, Vehicle (Car, Truck, Bike),
Ticket, ParkingStrategy, PricingStrategy
```

## 🏗️ Class Diagram

```
┌──────────────┐     ┌───────────┐     ┌──────────────┐
│  ParkingLot  │1──*│   Floor   │1──*│ ParkingSpot  │
├──────────────┤     ├───────────┤     ├──────────────┤
│ -floors      │     │ -floorNo  │     │ -spotNumber  │
│ -strategy    │     │ -spots    │     │ -type: Enum  │
│ -pricing     │     ├───────────┤     │ -vehicle     │
├──────────────┤     │+getAvail()│     ├──────────────┤
│ +park()      │     └───────────┘     │ +canFit()    │
│ +unpark()    │                       │ +occupy()    │
│ +display()   │                       │ +vacate()    │
└──────────────┘                       └──────────────┘

┌────────────────┐    ┌─────────────────┐
│  <<interface>> │    │   <<interface>> │
│ParkingStrategy │    │PricingStrategy  │
├────────────────┤    ├─────────────────┤
│+findSpot()     │    │+calculate()     │
└───────▲────────┘    └────────▲────────┘
        ┊                      ┊
  ┌─────┴──────┐         ┌────┴─────┐
  │NearestFirst│         │ Hourly   │
  │Strategy    │         │ Pricing  │
  └────────────┘         └──────────┘
```

## 🎯 Patterns Used

| Pattern | Where | Why |
|---|---|---|
| **Strategy** | ParkingStrategy, PricingStrategy | Swap allocation/pricing algorithms |
| **Factory** | VehicleFactory | Create vehicles by type |
| **Singleton** | ParkingLot | Only one parking lot instance |
| **Builder** | ParkingLot construction | Complex configuration |

## 📁 Code Structure
```
src/
├── model/
│   ├── Vehicle.java
│   ├── VehicleType.java
│   ├── ParkingSpot.java
│   ├── SpotType.java
│   ├── Floor.java
│   ├── Ticket.java
│   └── ParkingLot.java
├── strategy/
│   ├── ParkingStrategy.java
│   ├── NearestFirstStrategy.java
│   ├── PricingStrategy.java
│   └── HourlyPricingStrategy.java
├── exception/
│   ├── ParkingLotFullException.java
│   └── InvalidTicketException.java
└── ParkingLotDemo.java
```
