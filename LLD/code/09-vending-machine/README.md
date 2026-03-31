# 🥤 Problem 09: Vending Machine

> **Frequency:** 🟢 P2 | **Time:** 90 min | **Difficulty:** ⭐⭐

---

## 📋 Requirements

### Must-Have (Core)
1. Machine holds **inventory** of products with quantities and prices
2. Accept **coins** (1, 5, 10, 25 denominations)
3. User flow: **Insert Coins → Select Product → Dispense + Change**
4. Machine states: **IDLE**, **HAS_MONEY**, **DISPENSING**
5. Handle: insufficient funds, out of stock, return change
6. **State transitions** — behavior changes based on current state

### Nice-to-Have
- Admin operations: refill, collect money, change prices
- Card payment
- Display current balance and product list

---

## 🧩 Key Entities

```
VendingMachine, Product, Inventory, Coin (Enum),
VendingMachineState (interface), IdleState, HasMoneyState, DispensingState
```

## 🏗️ Class Diagram (State Pattern)

```
┌──────────────────┐      ┌─────────────────────┐
│  VendingMachine  │─────>│   <<interface>>     │
├──────────────────┤      │VendingMachineState  │
│ -state           │      ├─────────────────────┤
│ -inventory       │      │+insertCoin()        │
│ -balance         │      │+selectProduct()     │
│ -selectedProduct │      │+dispense()          │
├──────────────────┤      │+returnChange()      │
│ +setState()      │      └──────────▲──────────┘
│ +insertCoin()    │                 ┊
│ +selectProduct() │        ┌────────┼────────┐
│ +dispense()      │        ┊        ┊        ┊
└──────────────────┘  ┌─────┴──┐ ┌───┴────┐ ┌─┴────────┐
                      │  Idle  │ │HasMoney│ │Dispensing│
                      │  State │ │ State  │ │ State    │
                      └────────┘ └────────┘ └──────────┘

State Transitions:
  IDLE ──(insertCoin)──> HAS_MONEY
  HAS_MONEY ──(insertCoin)──> HAS_MONEY (add balance)
  HAS_MONEY ──(selectProduct + sufficient)──> DISPENSING
  HAS_MONEY ──(returnChange)──> IDLE
  DISPENSING ──(dispense)──> IDLE
```

## 🎯 Patterns Used

| Pattern | Where | Why |
|---|---|---|
| **State** | VendingMachineState | Core pattern — behavior changes per state |
| **Singleton** | VendingMachine instance | One physical machine |
| **Chain of Responsibility** | Coin change calculation | Dispense change in optimal denominations |

## 📁 Code Structure
```
src/
├── model/
│   ├── Product.java
│   ├── Coin.java
│   └── Inventory.java
├── state/
│   ├── VendingMachineState.java
│   ├── IdleState.java
│   ├── HasMoneyState.java
│   └── DispensingState.java
├── VendingMachine.java
└── VendingMachineDemo.java
```
