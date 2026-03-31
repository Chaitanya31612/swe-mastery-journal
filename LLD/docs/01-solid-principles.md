# 🧱 SOLID Principles — Applied to LLD Problems

> You know what SOLID stands for. This doc shows you **how violations look** in machine coding
> and **how to fix them** — because that's what interviewers test.

---

## S — Single Responsibility Principle (SRP)

> **A class should have only one reason to change.**

### ❌ Violation (Common in machine coding)

```java
public class ParkingLot {
    public void parkVehicle(Vehicle v) { /* parking logic */ }
    public void unparkVehicle(String ticketId) { /* unparking logic */ }
    public double calculatePrice(Ticket t) { /* pricing logic */ }  // ← VIOLATION
    public void printTicket(Ticket t) { /* printing logic */ }      // ← VIOLATION
    public void sendNotification(String msg) { /* notification */ }  // ← VIOLATION
}
```

### ✅ Fix

```java
public class ParkingLot {
    private PricingStrategy pricingStrategy;
    private TicketService ticketService;

    public Ticket parkVehicle(Vehicle v) { /* only parking logic */ }
    public Vehicle unparkVehicle(String ticketId) { /* only unparking logic */ }
}

public class HourlyPricingStrategy implements PricingStrategy {
    public double calculatePrice(Ticket t) { /* pricing logic */ }
}

public class TicketService {
    public void printTicket(Ticket t) { /* printing logic */ }
}
```

### 🎯 Interview Signal

When you separate concerns, say: *"I'm keeping ParkingLot focused on its core responsibility — managing parking operations. Pricing is a separate concern that can change independently."*

---

## O — Open/Closed Principle (OCP)

> **Open for extension, closed for modification.**

### ❌ Violation

```java
public class PricingCalculator {
    public double calculatePrice(Vehicle vehicle, long hours) {
        if (vehicle.getType() == VehicleType.CAR) {
            return hours * 20;
        } else if (vehicle.getType() == VehicleType.TRUCK) {
            return hours * 40;
        } else if (vehicle.getType() == VehicleType.BIKE) {
            return hours * 10;
        }
        // Adding ELECTRIC_CAR requires modifying this class!
        return 0;
    }
}
```

### ✅ Fix

```java
public interface PricingStrategy {
    double calculatePrice(long hours);
}

public class CarPricingStrategy implements PricingStrategy {
    public double calculatePrice(long hours) { return hours * 20; }
}

public class TruckPricingStrategy implements PricingStrategy {
    public double calculatePrice(long hours) { return hours * 40; }
}

// Adding ElectricCarPricingStrategy = new class, ZERO changes to existing code
public class ElectricCarPricingStrategy implements PricingStrategy {
    public double calculatePrice(long hours) { return hours * 15; }
}
```

### 🎯 Interview Signal

*"By using the Strategy pattern here, adding a new vehicle type's pricing doesn't require modifying any existing code — I just add a new strategy implementation."*

---

## L — Liskov Substitution Principle (LSP)

> **Subtypes must be substitutable for their base types without breaking behavior.**

### ❌ Violation

```java
public class ParkingSpot {
    public void parkVehicle(Vehicle v) { /* parks vehicle */ }
}

public class HandicappedSpot extends ParkingSpot {
    @Override
    public void parkVehicle(Vehicle v) {
        if (!v.hasHandicappedPermit()) {
            throw new RuntimeException("Only handicapped vehicles!");  // ← VIOLATION
            // Parent doesn't throw this — breaks substitutability
        }
        super.parkVehicle(v);
    }
}
```

### ✅ Fix

```java
public abstract class ParkingSpot {
    protected SpotType type;

    public abstract boolean canFitVehicle(Vehicle v);  // Contract includes capability check

    public void parkVehicle(Vehicle v) {
        if (!canFitVehicle(v)) {
            throw new InvalidParkingException("Vehicle doesn't fit this spot");
        }
        this.vehicle = v;
    }
}

public class HandicappedSpot extends ParkingSpot {
    @Override
    public boolean canFitVehicle(Vehicle v) {
        return v.hasHandicappedPermit() && v.getType().getSize() <= this.type.getSize();
    }
}
```

### 🎯 Interview Signal

*"I use `canFitVehicle()` as a contract method so that all spot types can be used interchangeably — the validation is part of the expected behavior, not a surprise exception."*

---

## I — Interface Segregation Principle (ISP)

> **No client should be forced to depend on methods it doesn't use.**

### ❌ Violation

```java
public interface GamePlayer {
    void makeMove(Board board);
    void undoMove(Board board);    // Not all players support undo
    void saveGame(String path);     // Why would a player save the game?
    void loadGame(String path);     // This is a game manager's job
}
```

### ✅ Fix

```java
public interface Player {
    void makeMove(Board board);
}

public interface UndoablePlayer extends Player {
    void undoMove(Board board);
}

public interface GamePersistence {
    void saveGame(String path);
    void loadGame(String path);
}

// HumanPlayer only needs to make moves
public class HumanPlayer implements Player {
    public void makeMove(Board board) { /* ... */ }
}

// AI player might support undo for analysis
public class AIPlayer implements UndoablePlayer {
    public void makeMove(Board board) { /* ... */ }
    public void undoMove(Board board) { /* ... */ }
}
```

### 🎯 Interview Signal

*"I keep interfaces small and focused — a Player shouldn't need to know about game persistence."*

---

## D — Dependency Inversion Principle (DIP)

> **High-level modules should not depend on low-level modules. Both should depend on abstractions.**

### ❌ Violation

```java
public class ElevatorController {
    private NearestFloorAlgorithm algorithm = new NearestFloorAlgorithm();  // ← Tight coupling
    private ConsoleLogger logger = new ConsoleLogger();                      // ← Tight coupling

    public void processRequest(Request req) {
        logger.log("Processing: " + req);
        Floor target = algorithm.findOptimal(req);
        // ...
    }
}
```

### ✅ Fix

```java
public class ElevatorController {
    private final SchedulingStrategy strategy;   // ← Depends on abstraction
    private final Logger logger;                  // ← Depends on abstraction

    public ElevatorController(SchedulingStrategy strategy, Logger logger) {
        this.strategy = strategy;  // Injected — can swap implementations
        this.logger = logger;
    }

    public void processRequest(Request req) {
        logger.log("Processing: " + req);
        Floor target = strategy.findOptimal(req);
        // ...
    }
}
```

### 🎯 Interview Signal

*"I inject dependencies through the constructor so the ElevatorController doesn't know or care which scheduling algorithm or logger is being used. This makes testing and extending trivial."*

---

## 🔑 Quick Reference Card

| Principle     | One-Liner                                       | Common LLD Fix                                      |
| ------------- | ----------------------------------------------- | --------------------------------------------------- |
| **SRP** | One class, one job                              | Extract pricing, notification into separate classes |
| **OCP** | Add new behavior without changing existing code | Use Strategy/Factory patterns                       |
| **LSP** | Subclass can replace parent without surprises   | Use `canDo()` contract methods                    |
| **ISP** | Don't force unnecessary methods                 | Split fat interfaces                                |
| **DIP** | Depend on interfaces, not concrete classes      | Constructor injection                               |

---

## 💡 Pro Tip for the Interview

You don't need to name-drop "SOLID" or "Liskov Substitution." Just demonstrate it naturally.

When the interviewer asks *"Why did you create an interface here?"*, the best answer is:

> *"Because I want the ParkingLot to work with any pricing strategy — hourly, daily, or something
> we haven't thought of yet. By depending on the PricingStrategy interface rather than a concrete
> class, I can add new pricing models without touching the ParkingLot code."*

That single answer demonstrates **OCP**, **DIP**, **Strategy Pattern**, and **extensibility** — all without buzzword-dropping.
