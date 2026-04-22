package java_demo;

import java.time.Duration;
import java.time.LocalDateTime;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.locks.ReentrantLock;

/**
 * PARKING LOT SYSTEM - JAVA IMPLEMENTATION
 * ----------------------------------------
 * This file is a self-contained demonstration of a complete, interview-ready Parking Lot LLD.
 * In a real codebase, these classes would be separated into packages (e.g., model, strategy, exception).
 *
 * TRADE-OFF DISCUSSION:
 * 1. Single File vs Multiple Files: Kept in one file for an easy interview walkthrough.
 * 2. Concurrency: Used ConcurrentHashMap for activeTickets and ReentrantLock for spot assignment.
 *    - Why? In real life, multiple gates can assign the same spot to two cars.
 * 3. Strategy Pattern: Separated ParkingStrategy and PricingStrategy.
 *    - Why? Pricing changes over time (weekends, holidays). Finding spots also changes (VIP vs general).
 * 4. Extensibility: VehicleType and SpotType are enums, but can be easily extended.
 */

// ==========================================
// 1. ENUMS & CONSTANTS
// ==========================================
enum VehicleType { BIKE, CAR, TRUCK }
enum SpotType { SMALL, MEDIUM, LARGE }


// ==========================================
// 2. CORE MODELS
// ==========================================
abstract class Vehicle {
    private String licensePlate;
    private VehicleType type;

    public Vehicle(String licensePlate, VehicleType type) {
        this.licensePlate = licensePlate;
        this.type = type;
    }
    public VehicleType getType() { return type; }
    public String getLicensePlate() { return licensePlate; }
}

class Bike extends Vehicle { public Bike(String plate) { super(plate, VehicleType.BIKE); } }
class Car extends Vehicle { public Car(String plate) { super(plate, VehicleType.CAR); } }
class Truck extends Vehicle { public Truck(String plate) { super(plate, VehicleType.TRUCK); } }

class ParkingSpot {
    private int spotNumber;
    private SpotType spotType;
    private Vehicle parkedVehicle;
    private boolean isFree;

    public ParkingSpot(int spotNumber, SpotType spotType) {
        this.spotNumber = spotNumber;
        this.spotType = spotType;
        this.isFree = true;
    }

    public boolean isFree() { return isFree; }
    public SpotType getSpotType() { return spotType; }
    public int getSpotNumber() { return spotNumber; }
    public Vehicle getParkedVehicle() { return parkedVehicle; }

    public void park(Vehicle vehicle) {
        this.parkedVehicle = vehicle;
        this.isFree = false;
    }

    public void vacate() {
        this.parkedVehicle = null;
        this.isFree = true;
    }
}

class Floor {
    private int floorNumber;
    private List<ParkingSpot> spots;

    public Floor(int floorNumber, List<ParkingSpot> spots) {
        this.floorNumber = floorNumber;
        this.spots = spots;
    }
    public int getFloorNumber() { return floorNumber; }
    public List<ParkingSpot> getSpots() { return spots; }
}

class Ticket {
    private String ticketId;
    private Vehicle vehicle;
    private ParkingSpot spot;
    private LocalDateTime entryTime;

    public Ticket(String ticketId, Vehicle vehicle, ParkingSpot spot) {
        this.ticketId = ticketId;
        this.vehicle = vehicle;
        this.spot = spot;
        this.entryTime = LocalDateTime.now();
    }
    public ParkingSpot getSpot() { return spot; }
    public LocalDateTime getEntryTime() { return entryTime; }
    public String getTicketId() { return ticketId; }
}

// ==========================================
// 3. EXCEPTIONS
// ==========================================
class ParkingLotFullException extends RuntimeException {
    public ParkingLotFullException(String message) { super(message); }
}
class InvalidTicketException extends RuntimeException {
    public InvalidTicketException(String message) { super(message); }
}

// ==========================================
// 4. STRATEGIES (Interfaces + Implementations)
// ==========================================
interface ParkingStrategy {
    ParkingSpot findSpot(VehicleType vehicleType, List<Floor> floors);
}

// Implements Nearest First strategy (O(N) search)
// Optimization tradeoff: In a high scale system, we'd use a PriorityQueue of available spots
// per SpotType to make this O(1). We use a simple iteration here to demonstrate base logic.
class NearestFirstParkingStrategy implements ParkingStrategy {
    @Override
    public ParkingSpot findSpot(VehicleType vehicleType, List<Floor> floors) {
        SpotType requiredType = mapVehicleToSpotType(vehicleType);

        for (Floor floor : floors) {
            for (ParkingSpot spot : floor.getSpots()) {
                if (spot.isFree() && spot.getSpotType() == requiredType) {
                    return spot;
                }
            }
        }
        throw new ParkingLotFullException("No available spot for " + vehicleType);
    }

    private SpotType mapVehicleToSpotType(VehicleType type) {
        switch (type) {
            case BIKE: return SpotType.SMALL;
            case CAR: return SpotType.MEDIUM;
            case TRUCK: return SpotType.LARGE;
            default: throw new IllegalArgumentException("Unknown Vehicle Type");
        }
    }
}

interface PricingStrategy {
    double calculatePrice(Ticket ticket);
}

// Implements an hourly pricing model.
class HourlyPricingStrategy implements PricingStrategy {
    private static final double HOURLY_RATE = 10.0;

    @Override
    public double calculatePrice(Ticket ticket) {
        // For demonstration, simulating time elapsed.
        // In real world: Duration.between(ticket.getEntryTime(), LocalDateTime.now()).toHours();
        // long hoursParked = 2; // Hardcoded mock for simulation
        long hoursParked = Duration.between(ticket.getEntryTime(), LocalDateTime.now()).toHours();
        return hoursParked * HOURLY_RATE;
    }
}

// ==========================================
// 5. THE FACADE / SINGLETON CONTROLLER
// ==========================================
class ParkingLot {
    private static ParkingLot instance;
    private List<Floor> floors;
    private ParkingStrategy parkingStrategy;
    private PricingStrategy pricingStrategy;

    // ConcurrentHashMap for thread-safe ticket lookups
    private Map<String, Ticket> activeTickets;
    private AtomicInteger ticketCounter;

    // Lock used to prevent race conditions during spot assignment
    private ReentrantLock lock;

    // Singleton pattern - prevents multiple parking lots in the system
    private ParkingLot() {
        this.activeTickets = new ConcurrentHashMap<>();
        this.ticketCounter = new AtomicInteger(1);
        this.lock = new ReentrantLock();
    }

    public static synchronized ParkingLot getInstance() {
        if (instance == null) {
            instance = new ParkingLot();
        }
        return instance;
    }

    // Builder/Setter approach to configure the lot
    public void initialize(List<Floor> floors, ParkingStrategy parkingStrat, PricingStrategy pricingStrat) {
        this.floors = floors;
        this.parkingStrategy = parkingStrat;
        this.pricingStrategy = pricingStrat;
    }

    public Ticket parkVehicle(Vehicle vehicle) {
        lock.lock(); // Thread safety: lock to assign spot
        try {
            ParkingSpot spot = parkingStrategy.findSpot(vehicle.getType(), floors);
            spot.park(vehicle);

            String ticketId = "TKT-" + ticketCounter.getAndIncrement();
            Ticket ticket = new Ticket(ticketId, vehicle, spot);
            activeTickets.put(ticketId, ticket);

            System.out.println("Parked " + vehicle.getType() + " at Floor " +
                               spot.getSpotNumber() + " with " + ticketId);
            return ticket;
        } finally {
            lock.unlock(); // Ensure lock is released even if exception occurs
        }
    }

    public double unparkVehicle(String ticketId) {
        if (!activeTickets.containsKey(ticketId)) {
            throw new InvalidTicketException("Ticket ID not found: " + ticketId);
        }

        Ticket ticket = activeTickets.get(ticketId);
        ParkingSpot spot = ticket.getSpot();

        spot.vacate();
        double price = pricingStrategy.calculatePrice(ticket);
        activeTickets.remove(ticketId);

        System.out.println("Unparked ticket " + ticketId + ". Paid: $" + price);
        return price;
    }
}

// ==========================================
// 6. MAIN DEMO
// ==========================================
public class ParkingLotDemo {
    public static void main(String[] args) {
        // 1. Initialize 2 Floors, 2 Spots per floor (1 Small, 1 Medium)
        List<ParkingSpot> floor1Spots = Arrays.asList(
            new ParkingSpot(101, SpotType.SMALL),
            new ParkingSpot(102, SpotType.MEDIUM)
        );
        Floor floor1 = new Floor(1, floor1Spots);

        List<ParkingSpot> floor2Spots = Arrays.asList(
            new ParkingSpot(201, SpotType.SMALL),
            new ParkingSpot(202, SpotType.MEDIUM)
        );
        Floor floor2 = new Floor(2, floor2Spots);

        // 2. Setup Strategies
        ParkingStrategy parkingStrategy = new NearestFirstParkingStrategy();
        PricingStrategy pricingStrategy = new HourlyPricingStrategy();

        // 3. Initialize Parking Lot
        ParkingLot parkingLot = ParkingLot.getInstance();
        parkingLot.initialize(Arrays.asList(floor1, floor2), parkingStrategy, pricingStrategy);

        try {
            // 4. Run Scenarios
            Vehicle bike1 = new Bike("BIKE-01");
            Vehicle car1 = new Car("CAR-01");
            Vehicle car2 = new Car("CAR-02");

            System.out.println("--- PARKING ---");
            Ticket t1 = parkingLot.parkVehicle(bike1); // Should park at Floor 1, Small
            Ticket t2 = parkingLot.parkVehicle(car1);  // Should park at Floor 1, Medium
            Ticket t3 = parkingLot.parkVehicle(car2);  // Should park at Floor 2, Medium

            System.out.println("\n--- UNPARKING ---");
            parkingLot.unparkVehicle(t2.getTicketId());

            System.out.println("\n--- PARKING NEW CAR ---");
            Vehicle car3 = new Car("CAR-03");
            Ticket t4 = parkingLot.parkVehicle(car3); // Should take the newly freed spot at Floor 1, Medium

        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
}
