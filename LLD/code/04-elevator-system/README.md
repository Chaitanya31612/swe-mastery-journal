# 🛗 Problem 04: Elevator System

> **Frequency:** 🔴 P0 | **Time:** 90 min | **Difficulty:** ⭐⭐⭐⭐

---

## 📋 Requirements

### Must-Have (Core)
1. Building with **N floors** and **M elevators**
2. Handle **external requests** (from floor buttons: UP/DOWN)
3. Handle **internal requests** (from inside elevator: go to floor X)
4. Elevator has states: **IDLE**, **MOVING_UP**, **MOVING_DOWN**, **DOOR_OPEN**
5. **Scheduling algorithm** to assign requests to optimal elevator
6. Elevator moves floor by floor and stops where it has requests

### Nice-to-Have (Extensions)
- Different scheduling algorithms (FCFS, SSTF, SCAN/Elevator algorithm)
- Weight/capacity limits
- Priority floors (VIP, emergency)
- Display panels showing current floor

---

## 🧩 Key Entities

```
Building, Elevator, Floor, Request, Direction (Enum),
ElevatorState (Enum), ElevatorController, SchedulingStrategy
```

## 🏗️ Class Diagram

```
┌──────────────────┐     ┌───────────┐
│ElevatorController│1──*│ Elevator  │
├──────────────────┤     ├───────────┤
│ -elevators       │     │ -id       │
│ -strategy        │     │ -curFloor │
│ -pendingRequests │     │ -state    │
├──────────────────┤     │ -direction│
│ +submitRequest() │     │ -requests │
│ +step()          │     ├───────────┤
└──────────────────┘     │ +move()   │
                         │ +stop()   │
┌────────────────┐       │ +openDoor │
│  <<interface>> │       └───────────┘
│ScheduleStrategy│
├────────────────┤       ┌───────────┐
│+selectElevator │       │  Request  │
│  (request)     │       ├───────────┤
└───────▲────────┘       │ -floor    │
        ┊                │ -direction│
   ┌────┴────┐           │ -type     │
   │         │           └───────────┘
┌──┴───┐ ┌──┴────┐
│ FCFS │ │ SSTF  │
└──────┘ └───────┘
```

## 🎯 Patterns Used

| Pattern | Where | Why |
|---|---|---|
| **State** | Elevator states (Idle, Moving, DoorOpen) | Behavior changes per state |
| **Strategy** | Scheduling algorithm | Swap FCFS/SSTF/SCAN |
| **Observer** | Display panels, logging | React to floor changes |
| **Command** | Requests as objects | Queue and process requests |

## 🔑 Key Design Decisions
- **State machine** — Elevator transitions: IDLE → MOVING_UP → DOOR_OPEN → MOVING_UP → IDLE
- **Request types** — External (floor button) vs Internal (inside elevator)
- **Scheduling** — FCFS is simplest, SCAN is most realistic (elevator algorithm)
- **Step-based simulation** — Each `step()` call moves elevators one floor

## 📁 Code Structure
```
src/
├── model/
│   ├── Elevator.java
│   ├── Floor.java
│   ├── Request.java
│   ├── Direction.java
│   └── ElevatorState.java
├── controller/
│   └── ElevatorController.java
├── strategy/
│   ├── SchedulingStrategy.java
│   ├── FCFSStrategy.java
│   └── SSTFStrategy.java
├── observer/
│   ├── ElevatorObserver.java
│   └── DisplayPanel.java
└── ElevatorDemo.java
```
