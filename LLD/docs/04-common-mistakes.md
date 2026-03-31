# ⚠️ Common Mistakes — What Experienced Devs Get Wrong in Machine Coding Rounds

> Having years of experience can actually be a disadvantage if you bring
> production habits into a timed interview. Here's what to avoid.

---

## Mistake 1: Over-Engineering 🏗️

### The Problem
Experienced devs build for scale during a 90-minute round.

```java
// ❌ You built an entire event-driven microservice architecture
// for what should be a simple in-memory parking lot

public class ParkingEventBus {
    private final ExecutorService executor = Executors.newFixedThreadPool(10);
    private final ConcurrentHashMap<String, List<EventHandler>> handlers = ...
}

public class ParkingCommandHandler implements CommandHandler<ParkCommand> { ... }
public class ParkingQueryHandler implements QueryHandler<AvailabilityQuery> { ... }
```

### The Fix
```java
// ✅ Simple, clean, in-memory — extensible but not over-architected
public class ParkingLot {
    private List<Floor> floors;
    private ParkingStrategy strategy;
    
    public Ticket park(Vehicle vehicle) {
        ParkingSpot spot = strategy.findSpot(vehicle, floors);
        spot.occupy(vehicle);
        return new Ticket(vehicle, spot);
    }
}
```

### Rule of Thumb
> If the interviewer didn't ask for it, don't build it.
> Show you *know* about it by *mentioning* it verbally.

---

## Mistake 2: Jumping Straight to Code 💻

### The Problem
You're confident from years of coding, so you skip design and start typing immediately.

### What Happens
- 30 minutes in, you realize entity relationships are wrong
- Massive refactoring under time pressure
- Interviewer sees you didn't plan

### The Fix
**Always spend 15-20 minutes on design before writing a single line.**
- List entities
- Draw relationships (even as comments)
- Define interfaces
- THEN implement

---

## Mistake 3: God Classes 👑

### The Problem
One class does everything because "it's faster."

```java
// ❌ ParkingLot handles parking, pricing, capacity, display, notifications
public class ParkingLot {
    public void park() { ... }
    public void unpark() { ... }
    public double calculatePrice() { ... }        // Not its job
    public void displayAvailability() { ... }      // Not its job
    public void sendSMSNotification() { ... }      // Definitely not its job
    public boolean checkCapacity() { ... }
    public void generateReport() { ... }           // No.
    // 500 lines later...
}
```

### The Fix
```
ParkingLot          → Manages floors and spots
PricingStrategy     → Calculates price
DisplayService      → Shows availability
NotificationService → Sends notifications
Ticket              → Holds parking info
```

**Rule: If a class has > 5-7 methods, it's probably doing too much.**

---

## Mistake 4: Using Strings Where Enums Belong 🔤

### The Problem
```java
// ❌ Magic strings everywhere
public class Vehicle {
    private String type;  // "car", "truck", "bike" — what if someone types "Car"?
}

if (vehicle.getType().equals("car")) { ... }  // Fragile, no compile-time safety
```

### The Fix
```java
// ✅ Type-safe enums
public enum VehicleType {
    CAR, TRUCK, BIKE, ELECTRIC_CAR;
}

public class Vehicle {
    private VehicleType type;  // Compile-time safety
}
```

---

## Mistake 5: Not Making Code Runnable ▶️

### The Problem
You write beautiful interfaces and abstractions but there's no `main` method.
The interviewer can't see it work.

### The Fix
Always include a driver class:
```java
public class ParkingLotDemo {
    public static void main(String[] args) {
        // Setup
        ParkingLot lot = new ParkingLot.Builder()
            .name("Mall Parking")
            .addFloor(new Floor(1, 10, 5, 2))
            .strategy(new NearestFirstStrategy())
            .build();
        
        // Demo: Park a car
        Vehicle car = new Car("KA-01-1234");
        Ticket ticket = lot.park(car);
        System.out.println("Parked: " + ticket);
        
        // Demo: Unpark
        Vehicle returned = lot.unpark(ticket.getId());
        System.out.println("Unparked: " + returned.getLicensePlate());
        
        // Demo: Try parking when full
        // ...
    }
}
```

---

## Mistake 6: Ignoring Edge Cases Entirely 🔲

### The Must-Handle Edge Cases
Every LLD problem has these:
- **Full capacity** → What happens when parking lot is full?
- **Not found** → What if ticket ID doesn't exist?
- **Duplicate** → What if same vehicle is parked twice?
- **Invalid input** → Null vehicle, negative values

```java
// ✅ Handle gracefully with custom exceptions
public Ticket park(Vehicle vehicle) {
    if (vehicle == null) {
        throw new IllegalArgumentException("Vehicle cannot be null");
    }
    
    ParkingSpot spot = strategy.findSpot(vehicle, floors);
    if (spot == null) {
        throw new ParkingLotFullException("No available spot for " + vehicle.getType());
    }
    
    spot.occupy(vehicle);
    return new Ticket(vehicle, spot);
}
```

---

## Mistake 7: Not Using Access Modifiers Properly 🔒

### The Problem
Everything is `public` because "it's just an interview."

```java
// ❌ Everything exposed
public class ParkingSpot {
    public SpotType type;
    public Vehicle vehicle;
    public boolean isAvailable;
}
```

### The Fix
```java
// ✅ Proper encapsulation — shows OOP maturity
public class ParkingSpot {
    private final SpotType type;
    private Vehicle vehicle;
    
    public boolean isAvailable() {
        return vehicle == null;
    }
    
    public boolean canFit(Vehicle v) {
        return isAvailable() && v.getType().getSize() <= type.getSize();
    }
    
    void occupy(Vehicle v) {  // package-private — only ParkingLot should call this
        this.vehicle = v;
    }
}
```

---

## Mistake 8: Deep Inheritance Hierarchies 🪆

### The Problem
```java
// ❌ 5 levels deep — unmaintainable
Vehicle
  └── MotorVehicle
        └── FourWheeler
              └── PersonalVehicle
                    └── Car

// Now you need an ElectricCar — where does it go?
// Does it extend Car? PersonalVehicle? Make a parallel hierarchy?
```

### The Fix
```java
// ✅ Flat hierarchy + composition
public abstract class Vehicle {
    private VehicleType type;
    private String licensePlate;
    // ...
}

public class Car extends Vehicle { }
public class Truck extends Vehicle { }

// For electric vehicles, use composition
public class ElectricVehicle extends Vehicle {
    private BatteryInfo battery;  // Composition, not deeper inheritance
}
```

**Rule: Maximum 2 levels of inheritance. Beyond that, use composition.**

---

## Mistake 9: Not Communicating During the Round 🗣️

### The Problem
You're heads-down coding in silence for 60 minutes.

### Why It's Bad
- Interviewer doesn't know your thought process
- They might think you're stuck
- No opportunity to course-correct

### The Fix
**Think out loud:**
- *"I'm creating a ParkingStrategy interface because I want to support different allocation algorithms"*
- *"I'm going to skip the Observer pattern for notifications now, but I can add it if we have time"*
- *"I'm using a HashMap here for O(1) ticket lookup — I could use a TreeMap if we need sorted access"*

---

## Mistake 10: Premature Optimization 🚀

### The Problem
```java
// ❌ Implementing a custom B-tree for spot lookup in a 90-min round
public class OptimizedSpotIndex {
    private static final int ORDER = 4;
    private Node root;
    // ... 100 lines of B-tree implementation
}
```

### The Fix
```java
// ✅ Use standard data structures and mention the optimization
private Map<SpotType, Queue<ParkingSpot>> availableSpots = new HashMap<>();
// "In production, we might use a more efficient spatial index for nearest-spot queries"
```

---

## 📋 Pre-Submission Checklist

Before saying "I'm done":

- [ ] Code compiles (no syntax errors)
- [ ] `main()` method exists and demos the happy path
- [ ] No God classes (each class ≤ 5-7 methods)
- [ ] Enums used for fixed types (no magic strings)
- [ ] Private fields with proper getters
- [ ] At least 1 design pattern applied and justified
- [ ] Custom exceptions for error cases
- [ ] Meaningful variable and method names
