# 🎨 Design Patterns Cheatsheet — Only What Matters for LLD Rounds

> There are 23 GoF patterns. You need **8** for machine coding rounds.
> This doc maps each pattern to the **exact LLD problem** where it's used.

---

## Pattern → Problem Map (Quick Glance)

| Pattern | Category | Used In | When To Apply |
|---|---|---|---|
| **Strategy** | Behavioral | Parking Lot, Elevator, Ride Sharing | Multiple algorithms for same task |
| **Factory** | Creational | Parking Lot, Logging, Vending Machine | Create objects without exposing logic |
| **Singleton** | Creational | Parking Lot, Cache, Database | Single instance needed globally |
| **Observer** | Behavioral | Elevator, Ride Sharing, Booking | Notify multiple objects of state change |
| **State** | Behavioral | Elevator, Vending Machine, Booking | Object behavior changes with state |
| **Chain of Responsibility** | Behavioral | Logging Framework, Rate Limiter | Pass request through handler chain |
| **Builder** | Creational | Complex configs, Queries | Complex object construction |
| **Decorator** | Structural | Logging, Caching, Notifications | Add behavior dynamically |

---

## 1. Strategy Pattern ⭐ (Most Important)

> **Use when:** You have multiple ways to do the same thing and want to swap them.

```java
// Interface
public interface ParkingStrategy {
    ParkingSpot findSpot(Vehicle vehicle, List<Floor> floors);
}

// Strategy 1: Find nearest to entrance
public class NearestFirstStrategy implements ParkingStrategy {
    @Override
    public ParkingSpot findSpot(Vehicle vehicle, List<Floor> floors) {
        // Iterate floor by floor, return first available matching spot
    }
}

// Strategy 2: Spread vehicles evenly across floors
public class SpreadEvenlyStrategy implements ParkingStrategy {
    @Override
    public ParkingSpot findSpot(Vehicle vehicle, List<Floor> floors) {
        // Find floor with least occupancy, then find spot there
    }
}

// Usage — easily swappable
ParkingLot lot = new ParkingLot(new NearestFirstStrategy());
// or
ParkingLot lot = new ParkingLot(new SpreadEvenlyStrategy());
```

### Where You'll Use It
- **Parking Lot** → Parking allocation strategy, pricing strategy
- **Elevator** → Scheduling algorithm (FCFS, SSTF, SCAN)
- **Ride Sharing** → Driver matching (nearest, highest-rated, cheapest)
- **Tic Tac Toe** → AI player strategy (random, minimax)

---

## 2. Factory Pattern

> **Use when:** Object creation logic is complex or needs to vary.

```java
public class VehicleFactory {
    public static Vehicle createVehicle(VehicleType type, String licensePlate) {
        switch (type) {
            case CAR:   return new Car(licensePlate);
            case TRUCK: return new Truck(licensePlate);
            case BIKE:  return new Bike(licensePlate);
            default:    throw new IllegalArgumentException("Unknown type: " + type);
        }
    }
}

// Usage
Vehicle v = VehicleFactory.createVehicle(VehicleType.CAR, "KA-01-1234");
```

### Abstract Factory Variant (for families of objects)
```java
public interface SpotFactory {
    ParkingSpot createSpot(int spotNumber);
}

public class CompactSpotFactory implements SpotFactory {
    public ParkingSpot createSpot(int spotNumber) {
        return new CompactSpot(spotNumber);
    }
}
```

### Where You'll Use It
- **Parking Lot** → Vehicle and ParkingSpot creation
- **Logging** → Logger creation based on log level/destination
- **Snake & Ladder** → Dice creation (normal, crooked)
- **Vending Machine** → Product creation

---

## 3. Singleton Pattern

> **Use when:** Only one instance should exist (and you need global access).

```java
public class ParkingLotManager {
    private static volatile ParkingLotManager instance;
    
    private ParkingLotManager() { }  // Private constructor
    
    public static ParkingLotManager getInstance() {
        if (instance == null) {
            synchronized (ParkingLotManager.class) {
                if (instance == null) {
                    instance = new ParkingLotManager();
                }
            }
        }
        return instance;
    }
}
```

### ⚠️ Word of Caution
- Use sparingly — it's basically a global variable
- In interviews, **justify** why Singleton: *"There's only one physical parking lot, so it makes sense to have one manager instance."*
- If asked about testing concerns, mention you'd use dependency injection in production

### Where You'll Use It
- **Parking Lot** → ParkingLotManager
- **LRU Cache** → CacheManager
- **Logging** → LogManager

---

## 4. Observer Pattern

> **Use when:** Multiple objects need to react to state changes.

```java
public interface ElevatorObserver {
    void onFloorChanged(int elevatorId, int newFloor);
    void onDoorStatusChanged(int elevatorId, DoorStatus status);
}

public class Elevator {
    private List<ElevatorObserver> observers = new ArrayList<>();
    
    public void addObserver(ElevatorObserver observer) {
        observers.add(observer);
    }
    
    private void notifyFloorChange(int newFloor) {
        for (ElevatorObserver obs : observers) {
            obs.onFloorChanged(this.id, newFloor);
        }
    }
    
    public void moveToFloor(int floor) {
        this.currentFloor = floor;
        notifyFloorChange(floor);  // All observers notified
    }
}

// Observers
public class DisplayPanel implements ElevatorObserver { /* updates floor display */ }
public class Logger implements ElevatorObserver { /* logs movements */ }
```

### Where You'll Use It
- **Elevator** → Display panels, logging, door controllers
- **Ride Sharing** → Notify driver of new ride, notify rider of driver arrival
- **Booking** → Notify user of booking confirmation
- **Splitwise** → Notify users of new expenses

---

## 5. State Pattern

> **Use when:** Object behavior changes entirely based on its current state.

```java
public interface VendingMachineState {
    void insertCoin(VendingMachine machine, double amount);
    void selectProduct(VendingMachine machine, String productCode);
    void dispenseProduct(VendingMachine machine);
}

public class IdleState implements VendingMachineState {
    public void insertCoin(VendingMachine machine, double amount) {
        machine.setBalance(amount);
        machine.setState(new HasMoneyState());  // Transition!
    }
    
    public void selectProduct(VendingMachine machine, String code) {
        System.out.println("Please insert coin first");  // No transition
    }
    
    public void dispenseProduct(VendingMachine machine) {
        System.out.println("Please insert coin and select product first");
    }
}

public class HasMoneyState implements VendingMachineState {
    public void insertCoin(VendingMachine machine, double amount) {
        machine.setBalance(machine.getBalance() + amount);
    }
    
    public void selectProduct(VendingMachine machine, String code) {
        if (machine.getProductPrice(code) <= machine.getBalance()) {
            machine.setSelectedProduct(code);
            machine.setState(new DispensingState());  // Transition!
        } else {
            System.out.println("Insufficient balance");
        }
    }
    // ...
}
```

### State vs Strategy — The Key Difference
| State | Strategy |
|---|---|
| States know about each other & manage transitions | Strategies are independent |
| Object changes its own behavior | Client chooses the behavior |
| Used for: Elevator, Vending Machine, Order Status | Used for: Algorithms, Policies |

### Where You'll Use It
- **Vending Machine** → Idle, HasMoney, Dispensing, Maintenance
- **Elevator** → Moving, Stopped, DoorOpen, Maintenance
- **Booking System** → PendingPayment, Confirmed, Cancelled, Completed

---

## 6. Chain of Responsibility

> **Use when:** A request should pass through multiple handlers in sequence.

```java
public abstract class LogHandler {
    protected LogLevel level;
    protected LogHandler nextHandler;
    
    public void setNext(LogHandler handler) {
        this.nextHandler = handler;
    }
    
    public void handle(LogMessage message) {
        if (message.getLevel().ordinal() >= this.level.ordinal()) {
            write(message);
        }
        if (nextHandler != null) {
            nextHandler.handle(message);  // Pass to next
        }
    }
    
    protected abstract void write(LogMessage message);
}

public class ConsoleLogHandler extends LogHandler {
    protected void write(LogMessage msg) {
        System.out.println("[" + msg.getLevel() + "] " + msg.getMessage());
    }
}

public class FileLogHandler extends LogHandler {
    protected void write(LogMessage msg) {
        // Write to file
    }
}

// Setup chain
LogHandler console = new ConsoleLogHandler(LogLevel.DEBUG);
LogHandler file = new FileLogHandler(LogLevel.WARNING);
LogHandler email = new EmailLogHandler(LogLevel.ERROR);

console.setNext(file);
file.setNext(email);

// Use: message flows through the chain
console.handle(new LogMessage(LogLevel.ERROR, "DB Connection Failed!"));
// → Console prints it, File logs it, Email sends alert
```

### Where You'll Use It
- **Logging Framework** → Multiple log handlers (console, file, database, email)
- **Rate Limiter** → Multiple limiting strategies chained
- **Vending Machine** → Coin denomination handlers

---

## 7. Builder Pattern

> **Use when:** Object construction is complex with many optional parameters.

```java
public class ParkingLot {
    private String name;
    private int maxFloors;
    private ParkingStrategy strategy;
    private PricingStrategy pricing;
    
    private ParkingLot() { }  // Private — must use Builder
    
    public static class Builder {
        private ParkingLot lot = new ParkingLot();
        
        public Builder name(String name) { lot.name = name; return this; }
        public Builder maxFloors(int floors) { lot.maxFloors = floors; return this; }
        public Builder parkingStrategy(ParkingStrategy s) { lot.strategy = s; return this; }
        public Builder pricingStrategy(PricingStrategy p) { lot.pricing = p; return this; }
        
        public ParkingLot build() {
            // Validate required fields
            if (lot.name == null) throw new IllegalStateException("Name is required");
            return lot;
        }
    }
}

// Usage
ParkingLot lot = new ParkingLot.Builder()
    .name("Downtown Parking")
    .maxFloors(5)
    .parkingStrategy(new NearestFirstStrategy())
    .pricingStrategy(new HourlyPricingStrategy())
    .build();
```

### Where You'll Use It
- Any problem with complex configuration (ParkingLot, Game Board setup)
- When constructor would have > 4 parameters

---

## 8. Decorator Pattern

> **Use when:** You want to add behavior to objects dynamically without changing their class.

```java
public interface Logger {
    void log(String message);
}

public class BasicLogger implements Logger {
    public void log(String message) {
        System.out.println(message);
    }
}

public class TimestampDecorator implements Logger {
    private Logger wrapped;
    
    public TimestampDecorator(Logger wrapped) { this.wrapped = wrapped; }
    
    public void log(String message) {
        wrapped.log("[" + LocalDateTime.now() + "] " + message);
    }
}

public class EncryptionDecorator implements Logger {
    private Logger wrapped;
    
    public EncryptionDecorator(Logger wrapped) { this.wrapped = wrapped; }
    
    public void log(String message) {
        wrapped.log(encrypt(message));
    }
}

// Usage — compose as needed
Logger logger = new EncryptionDecorator(
                    new TimestampDecorator(
                        new BasicLogger()));
logger.log("Sensitive data");
// Output: [encrypted][2024-01-15T10:30] Sensitive data
```

### Where You'll Use It
- **Logging** → Add timestamp, encryption, formatting dynamically
- **Cache** → Add eviction policies, TTL, sync wrappers
- **Notifications** → Add email, SMS, push notification layers

---

## 💡 Pattern Selection Cheat Sheet

```
"I need to swap algorithms at runtime"          → Strategy
"I need to create objects without exposing how"  → Factory
"I need exactly one instance"                    → Singleton
"I need to notify many objects of a change"      → Observer
"Object behavior depends on its state"           → State
"Request passes through multiple handlers"       → Chain of Responsibility
"Object has too many constructor parameters"     → Builder
"I want to add behavior without changing class"  → Decorator
```
