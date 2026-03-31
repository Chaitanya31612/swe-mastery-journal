# 🎯 Machine Coding Playbook — The 90-Minute Battle Plan

> This is the exact framework to follow during a machine coding round.
> Print this. Memorize this. This is your SOP.

---

## ⏱️ Time Allocation

```
┌────────────────────────────────────────────────────────────┐
│  0        10        20        30        60        80   90  │
│  ├─────────┼─────────┼─────────┼─────────┼─────────┼───┤  │
│  │ CLARIFY │ MODEL   │ DESIGN  │    IMPLEMENT      │ ✓ │  │
│  │ 5-10min │ 10min   │ 5-10min │    45-55min       │5m │  │
│  └─────────┴─────────┴─────────┴─────────────────────┴──┘  │
└────────────────────────────────────────────────────────────┘
```

---

## Step 1: Clarify Requirements (5-10 min)

### What to Do
- **Read the problem statement twice** — don't skim
- **Ask clarifying questions** — this shows maturity
- **Separate Must-haves from Nice-to-haves**
- **Document your assumptions** in code comments

### Questions to Ask
```
✅ "Should the system support multiple [X] simultaneously?"
✅ "Do we need to handle concurrent access?"
✅ "What are the constraints on [capacity/time/users]?"
✅ "Should I focus on a working solution or cover all edge cases?"
✅ "Is there a specific design pattern you'd like me to explore?"
```

### What to Write Down
```
REQUIREMENTS:
- Must-have: [list core features]
- Nice-to-have: [list extensions]
- Out of scope: [explicitly exclude]

ASSUMPTIONS:
- Single-threaded unless stated otherwise
- In-memory storage (no DB)
- [Any other assumptions]
```

---

## Step 2: Identify Entities & Relationships (10 min)

### The Noun-Verb Technique
1. **Underline all nouns** in requirements → These are your **classes/entities**
2. **Underline all verbs** → These are your **methods**
3. **Identify relationships** → has-a, is-a, uses-a

### Example: Parking Lot
```
"A parking lot has multiple floors. Each floor has parking spots.
 Spots can be small, medium, or large. Vehicles can be parked and unparked."

Nouns (Entities):  ParkingLot, Floor, ParkingSpot, Vehicle
Verbs (Methods):   park(), unpark()
Relationships:     ParkingLot HAS-A List<Floor>
                   Floor HAS-A List<ParkingSpot>
                   Vehicle IS-A (Car, Truck, Bike)
                   ParkingSpot HAS-A Vehicle (when occupied)
```

### Quick Class Diagram (sketch on paper/whiteboard)
```
┌──────────────┐       ┌───────────┐       ┌──────────────┐
│  ParkingLot  │1────*│   Floor   │1────*│ ParkingSpot  │
├──────────────┤       ├───────────┤       ├──────────────┤
│ -floors      │       │ -spots    │       │ -type        │
│ -name        │       │ -floorNo  │       │ -vehicle     │
├──────────────┤       ├───────────┤       │ -isAvailable │
│ +park()      │       │ +getAvail │       ├──────────────┤
│ +unpark()    │       │  Spot()   │       │ +canFit()    │
└──────────────┘       └───────────┘       │ +occupy()    │
                                           │ +vacate()    │
                                           └──────────────┘
```

---

## Step 3: Design Interfaces & Contracts (5-10 min)

### Think in Interfaces First
Before writing any implementation, define what each component **promises** to do.

```java
// GOOD: Define contracts first
public interface ParkingStrategy {
    ParkingSpot findSpot(Vehicle vehicle, List<Floor> floors);
}

public interface PricingStrategy {
    double calculatePrice(Ticket ticket);
}

// Then implement
public class NearestFirstStrategy implements ParkingStrategy { ... }
public class HourlyPricingStrategy implements PricingStrategy { ... }
```

### Why This Matters
- Shows you think about **abstraction** before implementation
- Makes your code **extensible** (can swap strategies)
- Demonstrates **Dependency Inversion** (depend on abstractions)
- Easy to explain trade-offs to interviewer

---

## Step 4: Implement Core Logic (45-55 min)

### Order of Implementation
```
1. Enums & Constants          (2 min)  — VehicleType, SpotType, etc.
2. Model/Entity Classes       (10 min) — The data holders
3. Core Business Logic        (20 min) — The "brain" of the system
4. Service/Manager Layer      (10 min) — Orchestration
5. Driver/Main Class          (5 min)  — Demo that it works
```

### Golden Rules While Coding
```
✅ DO                              ❌ DON'T
──────────────────────────         ──────────────────────────
Use meaningful names               Use single-letter variables
Keep methods < 15 lines            Write God classes
Use enums for fixed types          Use string constants
Handle null/edge cases             Assume happy path
Use composition over inherit.      Create deep class hierarchies
Make fields private                Make everything public
Use final where possible           Leave things mutable
```

### The "Is It Extensible?" Test
After writing your core code, mentally check:
> "If the interviewer says 'now add support for electric vehicles with charging spots',
>  how much code do I need to change?"

- **Good answer:** "I add a new VehicleType enum and a new SpotType, maybe a new Strategy"
- **Bad answer:** "I need to modify my core ParkingLot class and add if-else blocks"

---

## Step 5: Review & Edge Cases (5 min)

### Quick Checklist
- [ ] Does the code compile?
- [ ] Can I demo the happy path?
- [ ] Are there any obvious NullPointerExceptions?
- [ ] Did I handle "not found" / "full capacity" cases?
- [ ] Are variable/method names self-explanatory?
- [ ] Can I explain every design decision if asked?

### Bonus Points (if time permits)
- Add basic exception handling with custom exceptions
- Show thread-safety awareness (mention `synchronized` or `ConcurrentHashMap`)
- Add a simple `toString()` for debugging output

---

## 🧠 Mindset During the Round

```
┌────────────────────────────────────────────────────┐
│                                                    │
│   "I am not writing production code.                │
│    I am demonstrating my DESIGN THINKING           │
│    through clean, extensible code."                │
│                                                    │
│   → Think out loud                                 │
│   → Explain trade-offs                             │
│   → It's OK to simplify — just call it out         │
│   → A working simple design > broken complex one   │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

## 🔥 Emergency Shortcuts

If you're running out of time:

1. **Skip implementation details** — Write method signatures + comments
   ```java
   // TODO: Implement using BFS to find nearest available spot
   public ParkingSpot findNearestSpot(Vehicle v) { return null; }
   ```

2. **Use in-memory collections** — Don't build anything fancy
   ```java
   private Map<String, Ticket> activeTickets = new HashMap<>();
   ```

3. **Hardcode configurations** — You can mention "this would be configurable"
   ```java
   private static final int MAX_FLOORS = 5; // Configurable in production
   ```

4. **Explain what you'd do differently** — Verbal extensibility counts
   > "In production, I'd use a database for persistence and add an Observer
   >  pattern for notifications, but for now I'll keep it in-memory."
