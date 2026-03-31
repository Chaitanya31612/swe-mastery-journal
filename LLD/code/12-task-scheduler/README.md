# ⏰ Problem 12: Task Scheduler (Cron-like)

> **Frequency:** 🟢 P2 | **Time:** 90 min | **Difficulty:** ⭐⭐⭐

---

## 📋 Requirements

### Must-Have (Core)
1. Schedule **tasks** to run at specific intervals or times
2. Task types: **ONE_TIME**, **RECURRING** (every N seconds/minutes)
3. Tasks have a **priority** — higher priority tasks execute first
4. **Execute** tasks when their scheduled time arrives
5. Support **cancel** and **update** tasks
6. Handle task **dependencies** (task B runs after task A completes)

### Nice-to-Have
- Thread pool for concurrent task execution
- Retry on failure with exponential backoff
- Task chaining (pipeline)
- Cron expression support

---

## 🧩 Key Entities

```
Task, TaskScheduler, TaskStatus, TaskType, TaskExecutor, PriorityQueue
```

## 🎯 Patterns Used

| Pattern | Where | Why |
|---|---|---|
| **Command** | Task as command object | Encapsulate task execution |
| **Strategy** | Execution strategy (sequential, parallel) | Swap execution modes |
| **Observer** | Task completion events | Trigger dependent tasks |
| **Singleton** | TaskScheduler | Central scheduling |

## 🔑 Key Design Decisions
- **PriorityQueue (min-heap)** — Tasks ordered by next execution time
- **Command pattern** — Each Task wraps a `Runnable` with metadata
- **Recurring tasks** — After execution, re-schedule with updated next execution time
- **Thread pool** — Use `ScheduledExecutorService` for actual execution

## 📁 Code Structure
```
src/
├── model/
│   ├── Task.java
│   ├── TaskType.java
│   └── TaskStatus.java
├── scheduler/
│   ├── TaskScheduler.java
│   └── TaskExecutor.java
├── command/
│   ├── TaskCommand.java
│   └── PrintTaskCommand.java
└── TaskSchedulerDemo.java
```
