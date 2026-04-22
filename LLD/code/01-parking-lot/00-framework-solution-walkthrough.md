# The "40-Year Coach" LLD Interview Framework: Parking Lot

Welcome, engineer. I've conducted and designed coding interviews at top tech companies for decades. Your goal here isn't just to write code that compiles; it's to demonstrate **architectural forethought, clarity in communication, and mastery of extensibility**. 

This document mirrors the scratchpad or IDE you'd share with an interviewer. Walk through it linearly. Remember, you have 40-60 minutes.

---

## 🛠️ The 5-Step LLD Framework

1. **Clarify (5-10m):** Establish bounds. Separate P0 (Must-haves) from P1 (Nice-to-haves).
2. **Model Entities & Relationships (10m):** Nouns become classes; verbs become methods. Sketch out the class diagram mentally or in text.
3. **Design Contracts First (5-10m):** Build Interfaces and Abstract classes. Show you think in abstractions, not just implementations.
4. **Implementation (25-30m):** Build the core components. Hardcode or simplify the non-critical parts, focus on the complex logic.
5. **Review & Edge Cases (5 m):** Dry run, discuss concurrency, and explain design pattern tradeoffs.

---

## 🅿️ Step 1: Clarifying Requirements (What to say)

**Interviewer:** "Design a Parking Lot System."

**You (The Candidate):** 
*“Before I jump into the class design, I want to clarify the constraints to ensure we build exactly what’s needed within the time limit. Let me list out my assumptions, please tell me if I should adjust any.”*

**Requirements Documented on Scratchpad:**
*   **Must-Haves (P0):**
    *   Multiple floors, multiple spots per floor.
    *   Spot types: Small (Bike), Medium (Car), Large (Truck).
    *   A vehicle can only park in a spot that fits it (or larger? *Assumption: exact fit or larger. Let's assume strict fit for simplicity unless dictated otherwise.*)
    *   Entry: Issue a Ticket with an entry time.
    *   Exit: Calculate price and free the spot.
*   **Out of Scope (For now):** Payment processing, multi-gate concurrency (assuming a single thread for core logic, but will design thread-safely where obvious).
*   **Scale:** In-memory, single application instance.

> **Coach's Tip:** Clarifying scale and scope buys you time and restricts the problem bounds. It turns a massive system into a solvable 40-minute chunk.

---

## 🧩 Step 2: Entities & Relationships

**You:** *“Based on the requirements, I’ll extract the key nouns to form my entities.”*

**Scratchpad Notes:**
*   **Enums:** `VehicleType` (BIKE, CAR, TRUCK), `SpotType` (SMALL, MEDIUM, LARGE), `TicketStatus` (ACTIVE, PAID).
*   **Entities:**
    *   `Vehicle`: `licensePlate`, `VehicleType`.
    *   `ParkingSpot`: `spotNumber`, `SpotType`, `isFree`, `Vehicle`.
    *   `Floor`: `floorNumber`, `List<ParkingSpot>`.
    *   `Ticket`: `ticketId`, `Vehicle`, `ParkingSpot`, `entryTime`.
    *   `ParkingLot`: `List<Floor>`.
*   **Relationships:**
    *   ParkingLot *has-many* Floors.
    *   Floor *has-many* ParkingSpots.

> **Coach's Tip:** Talk while you type. "I'm making `ParkingSpot` hold a reference to `Vehicle` so we know who is parked where in constant time."

---

## 📜 Step 3: Design Contracts First (Abstractions)

**You:** *“I’ll design the interfaces first. This ensures the system is closed for modification but open for extension (Open/Closed Principle). The two most volatile parts of a parking lot are HOW we find a spot, and HOW we calculate the price.”*

**Scratchpad / Pseudo-Code:**

```java
// Strategy Pattern for Allocation
interface ParkingStrategy {
    ParkingSpot findSpot(VehicleType type, List<Floor> floors);
}

// Strategy Pattern for Pricing
interface PricingStrategy {
    double calculatePrice(Ticket ticket);
}

// Core Operations Interface
interface IParkingLot {
    Ticket parkVehicle(Vehicle vehicle);
    double unparkVehicle(String ticketId);
}
```

> **Coach's Tip:** Interviewers love this. By introducing `ParkingStrategy` and `PricingStrategy`, you instantly demonstrate the Strategy pattern without them having to ask. It screams "Senior Engineer".

---

## 🏗️ Step 4: Core Implementation (Pseudo-Code)

**You:** *“I’ll now build the core entities. Let’s focus on the `ParkingLot` which acts as our facade, and the actual strategy implementations.”*

**Scratchpad / Pseudo-Code:**

```java
class ParkingSpot {
    SpotType type;
    Vehicle vehicle;
    boolean isFree;
    
    void park(Vehicle v) {
        this.vehicle = v;
        this.isFree = false;
    }
    
    void vacate() {
        this.vehicle = null;
        this.isFree = true;
    }
}

class NearestFirstStrategy implements ParkingStrategy {
    public ParkingSpot findSpot(VehicleType vType, List<Floor> floors) {
        SpotType requiredType = mapVehicleToSpotType(vType);
        for(Floor f : floors) {
            for(ParkingSpot s : f.spots) {
                if(s.isFree() && s.getType() == requiredType) return s;
            }
        }
        throw new ParkingFullException();
    }
}

// The Singleton Facade
class ParkingLot {
    List<Floor> floors;
    ParkingStrategy parkingStrategy;
    PricingStrategy pricingStrategy;
    Map<String, Ticket> activeTickets; // Fast lookup on unpark

    public Ticket parkVehicle(Vehicle v) {
        ParkingSpot spot = parkingStrategy.findSpot(v.getType(), floors);
        spot.park(v);
        Ticket t = new Ticket(v, spot, Time.now());
        activeTickets.put(t.id, t);
        return t;
    }

    public double unparkVehicle(String ticketId) {
        Ticket t = activeTickets.get(ticketId);
        ParkingSpot spot = t.getSpot();
        spot.vacate();
        double price = pricingStrategy.calculatePrice(t);
        activeTickets.remove(ticketId);
        return price;
    }
}
```

> **Coach's Tip:** Always use a simple dictionary/hashmap for fast lookups (like `activeTickets`). It shows you think about performance (O(1) lookups) rather than iterating through all floors and spots to find a car.

---

## 🔍 Step 5: Review & Edge Cases (Discussion)

**You:** *“The core flow is complete. Let’s dry-run what happens when a CAR enters...”* (Briefly walk through `parkVehicle`).

*“Before we wrap up, I want to highlight some trade-offs and how we’d handle scale:”*

1.  **Concurrency / Thread Safety:** "If two cars enter different gates simultaneously, they might be assigned the same `ParkingSpot`. To fix this, I would use a `ConcurrentHashMap` for active tickets and add a `ReentrantLock` or simply use the `synchronized` keyword on the `parkVehicle` method. Even better, synchronize on the specific `Floor` or `ParkingSpot`."
2.  **Performance Optimization:** "Currently, `findSpot` is O(N) where N is all spots. In a production system, I'd maintain a `Queue` or `MinHeap` of available spots per `SpotType` to make `findSpot` O(1) or O(log N)."
3.  **Extensibility:** "If we wanted to add a 'Handicapped' spot or 'EV Charging', we just add elements to `SpotType`. We can implement a new `EvPricingStrategy` without touching the core `ParkingLot` code."

> **Coach's Conclusion:** You've just guided the interviewer through a masterclass. You hit SOLID principles, optimization, and edge cases before they even had to prompt you.
