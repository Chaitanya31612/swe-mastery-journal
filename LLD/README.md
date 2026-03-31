# 🏗️ Low Level Design (LLD) — Machine Coding Round Preparation

> **Goal:** Crack machine coding rounds at top tech companies in the shortest time possible.
> **Strategy:** Pattern-first approach → Solve the top 12 most-asked problems → Build muscle memory.

---

## 📁 Folder Structure

```
LLD/
├── README.md                          ← You are here (Roadmap + Strategy)
├── docs/
│   ├── 00-machine-coding-playbook.md  ← The 90-minute framework for the actual round
│   ├── 01-solid-principles.md         ← SOLID with real LLD examples
│   ├── 02-design-patterns-cheatsheet.md ← Only the patterns that matter for LLD
│   ├── 03-uml-quick-reference.md      ← Class diagram essentials
│   └── 04-common-mistakes.md          ← What experienced devs get wrong
├── code/
│   ├── 01-parking-lot/                ← #1 most asked
│   ├── 02-snake-and-ladder/           ← Classic game design
│   ├── 03-tic-tac-toe/               ← Clean OOP showcase
│   ├── 04-elevator-system/           ← State + Strategy patterns
│   ├── 05-splitwise/                 ← Debt simplification
│   ├── 06-booking-system/            ← Movie ticket / BookMyShow
│   ├── 07-logging-framework/         ← Chain of Responsibility
│   ├── 08-cache-lru/                 ← LRU Cache design
│   ├── 09-vending-machine/           ← State pattern classic
│   ├── 10-ride-sharing/              ← Uber/Ola matching
│   ├── 11-rate-limiter/              ← Token bucket + sliding window
│   └── 12-task-scheduler/            ← Cron-like scheduler
└── .gitkeep
```

---

## 🚀 The Fastest Preparation Strategy

### Why Design Patterns Alone Aren't Enough

You already know design patterns — great. But machine coding rounds test something different:

| Design Patterns Knowledge | Machine Coding Skill |
|---|---|
| Know *what* Strategy pattern is | Know *when* to apply it in a parking lot |
| Can explain Observer | Can model an event-driven elevator system |
| Memorized UML for Factory | Can design a vehicle hierarchy under pressure |

**The gap = applied problem-solving under time constraints.**

---

### 🗺️ The 3-Phase Roadmap

#### Phase 1: Foundation Refresh (Day 1-2) 📖
> Read the docs, internalize the framework

- [ ] Read [Machine Coding Playbook](docs/00-machine-coding-playbook.md) — your 90-min battle plan
- [ ] Skim [SOLID Principles](docs/01-solid-principles.md) — focus on *violations* you'd make
- [ ] Review [Design Patterns Cheatsheet](docs/02-design-patterns-cheatsheet.md) — only the 8 that matter
- [ ] Glance at [UML Quick Reference](docs/03-uml-quick-reference.md) — class diagrams only
- [ ] Read [Common Mistakes](docs/04-common-mistakes.md) — avoid what others get wrong

#### Phase 2: Core Problems (Day 3-8) 🔥
> Solve 2 problems per day, timed at 90 minutes each

| Priority | Problem | Key Pattern | Difficulty |
|---|---|---|---|
| 🔴 P0 | Parking Lot | Strategy, Factory, Singleton | ⭐⭐⭐ |
| 🔴 P0 | Snake & Ladder | Entities + Game Loop | ⭐⭐ |
| 🔴 P0 | Tic Tac Toe | Strategy, Clean OOP | ⭐⭐ |
| 🔴 P0 | Elevator System | State, Strategy, Observer | ⭐⭐⭐⭐ |
| 🟡 P1 | Splitwise | Graph/Debt Simplification | ⭐⭐⭐ |
| 🟡 P1 | Booking System | Concurrency, State Machine | ⭐⭐⭐⭐ |
| 🟡 P1 | Logging Framework | Chain of Responsibility | ⭐⭐ |
| 🟡 P1 | LRU Cache | HashMap + DLL | ⭐⭐⭐ |
| 🟢 P2 | Vending Machine | State Pattern | ⭐⭐ |
| 🟢 P2 | Ride Sharing | Strategy, Observer | ⭐⭐⭐⭐ |
| 🟢 P2 | Rate Limiter | Token Bucket Algorithm | ⭐⭐⭐ |
| 🟢 P2 | Task Scheduler | Priority Queue, Command | ⭐⭐⭐ |

#### Phase 3: Mock Drills (Day 9-10) ⚡
> Simulate real interview conditions

- [ ] Pick any 2 problems you haven't revisited
- [ ] Set a **strict 90-minute timer**
- [ ] No looking at solutions, no internet
- [ ] Write on a fresh file from scratch
- [ ] Review your own code for SOLID violations after

---

## 🎯 What Interviewers Actually Evaluate

```
┌─────────────────────────────────────────────────────┐
│                  EVALUATION MATRIX                   │
├──────────────────────┬──────────────────────────────┤
│ Code Completeness    │ Does it compile & run?       │
│ Object Modeling      │ Right entities & relations?  │
│ Design Patterns      │ Applied where appropriate?   │
│ SOLID Adherence      │ Extensible without breakage? │
│ Clean Code           │ Readable, well-named?        │
│ Edge Cases           │ Error handling, boundaries?  │
│ Extensibility        │ Easy to add new features?    │
└──────────────────────┴──────────────────────────────┘
```

---

## 📚 Quick References

- **Language:** All code examples are in **Java** (most expected in LLD rounds)
- **Each problem folder contains:**
  - `README.md` — Requirements, entities, class diagram
  - `src/` — Clean implementation
  - `PATTERNS_USED.md` — Which patterns and why

---

*Last updated: March 30, 2026*
