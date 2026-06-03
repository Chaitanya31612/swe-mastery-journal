# Parking Lot

## Problem Statement
Design a parking lot system that supports multiple types of vehicles and multiple parking spots.

## Questions
- does parking lot has multiple floors - yes
- can I assume there is only one entrance and one exit - yes
- can I assume three types of vehicles - bike (small), car (medium), truck (large)
- can a spot have only matching vehicle type of smaller vehicle as well - for now only matching types
- can I assume mutliple floors as well, each floor has multiple parking spots - yes

## Requirements
- Parking Lot system = Singleton
- multiple floors with multiple parking spots of a specific type
- we support only specific vehicletype parking
- on entrace we get ticket with vehicle license plate, entry time, spot allocated, vehicle type
- on exit, this ticket is used to calculate amount to be paid
-- special logic = Strategy pattern
- calculation of amount
- finding the spot

## Nice to have / Out of scope
- Payment processing - we'll just assume we have 3 party integration
- multiple entrances and exits
- multiple parking lots
- option to park at vehicle type compatible parking spot or above

### Ask, are we good so far? - yes

## Entities

- ParkingLot
  is- a collection of floors and parking spots
  knows- floors, parking spots (empty or occupied), strategy for finding parking spot and calculating amount to be paid (optional - can be present in ticket)
  does- park and unpark

- Floor
  - is - a floor in the parking lot containing multiple parking spots
  - knows - parking spots (empty or occupied)
  - does - find empty parking spot for vehicle type

- ParkingSpot
  - is - spot for vehicle
  - knows - spot type (small, medium, large) and occupancy status (empty or occupied), vehicle
  - does - park and unpark

- Vehicle
  - is - a vehicle
  - knows - vehicle type (bike, car, truck) and license plate
  - does - nothing

- Ticket
  - is - holds data for parking spot and vehicle parked at time
  - knows - entry time, parking spot, vehicle type, vehicle license plate (unique)
  - does - calculate amount to be paid

## Relationship
ParkingLot has many Floors
Floor has many ParkingSpots
ParkingSpot has one Vehicle
Ticket has one Vehicle
Ticket has one ParkingSpot

## Class Diagram

```ruby
class ParkingLot
    - floors: List<Floor>
    - spotStrategy: SpotStrategy

    + ParkingLot(floors: List<Floor>)
    + setSpotStrategy(spotStrategy: SpotStrategy)
    + park(vehicle: Vehicle): Ticket
    + unpark(ticket: Ticket): Integer

class Floor
  - parkingSpots: List<ParkingSpot>

  + findAvailableSpots(vehicleType: VehicleType): List<ParkingSpot>

class ParkingSpot
  - spotType: SpotType
  - vehicle: Vehicle

  + isOccupied(): boolean
  + park(vehicle: Vehicle)
  + unpark(): Vehicle

class Vehicle
  - vehicleType: VehicleType
  - licensePlate: String

class Ticket
  - vehicle: Vehicle
  - parkingSpot: ParkingSpot
  - entryTime: LocalDateTime
  - exitTime: LocalDateTime # this will mark the ticket as complete and unusable in future
  - amountStrategy: AmountStrategy

  + amountToPay(): Integer
  + isValid(): boolean # retro active inspection maybe

class SpotStrategy
  + findSpot(vehicleType: VehicleType): ParkingSpot

class NearestSpotStrategy
  + findSpot(vehicleType: VehicleType, floors: List<Floor>): ParkingSpot

class AmountStrategy
  + calculateAmount(ticket: Ticket): Integer

class FlatRateStrategy
  - ratePerHour: Integer
  + calculateAmount(ticket: Ticket): Integer

class VehicleTypeRateStrategy
  - rates: Map<VehicleType, Integer>
  + calculateAmount(ticket: Ticket): Integer

```

## Implementation

```java

public class ParkingLotController {
  public static void main(String[] args) {
    Vehicle car1 = new Vehicle(VehicleType.CAR, "CAR1");
    Vehicle car2 = new Vehicle(VehicleType.CAR, "CAR2");
    
    Vehicle bike = new Vehicle(VehicleType.BIKE, "BIKE1");

    // floor 1 only cars and trucks
    ParkingSpot spot1onFloor1 = new ParkingSpot(ParkingSpotType.LARGE);
    ParkingSpot spot3onFloor1 = new ParkingSpot(ParkingSpotType.MEDIUM);
    
    // floor 2 only bikes
    ParkingSpot spot1onFloor2 = new ParkingSpot(ParkingSpotType.SMALL);
    ParkingSpot spot2onFloor2 = new ParkingSpot(ParkingSpotType.SMALL);

    Floor floor1 = new Floor(1, List.of(spot1onFloor1, spot2onFloor1, spot3onFloor1));
    Floor floor2 = new Floor(2, List.of(spot1onFloor2, spot2onFloor2));

    // singleton parking lot
    ParkingLot parkingLot = ParkingLot.getInstance();
    parkingLot.addFloor(floor1);
    parkingLot.addFloor(floor2);

    // park vehicles
    parkVehicle(car1);
    
    parkVehicle(car2);
    parkVehicle(bike);

    // unpark CAR1
    unparkVehicle(ticket1);

    // try parking car2 again
    parkVehicle(car2);
  }

  public Ticket parkVehicle(Vehicle vehicle) {
    ParkingLot parkingLot = ParkingLot.getInstance();

    parkingLot.setSpotStrategy(new NearestSpotStrategy());
    ParkingSpot parkingSpot = parkingLot.allocateSpot(vehicle);
    if (parkingSpot == null) {
      System.out.println("No parking spot available for vehicle: " + vehicle.toString());
      return null;
    }

    parkingSpot.markOccupied(vehicle);
    Ticket ticket = new Ticket(parkingSpot, vehicle);
    ticket.printDetails();
    return ticket;
  }

  public void unparkVehicle(Ticket ticket) {
    ParkingLot parkingLot = ParkingLot.getInstance();

    // calculate Fee
    int parkingFee = ticket.calculateParkingFee();
    System.out.println("Parking Fee for vehicle:" + ticket.toString() + " is " + parkingFee + " Rs.");

    // release spot
    ParkingSpot parkingSpot = ticket.getParkingSpot();
    parkingLot.releaseSpot(parkingSpot);

    // mark ticket as exited
    ticket.markExited();
  }
}

// ENUMS
public enum ParkingSpotType {
  SMALL, MEDIUM, LARGE
}

public enum VehicleType {
  CAR, BIKE, TRUCK
}

// singleton parking lot
public class ParkingLot {
  private List<Floor> floors;
  private static ParkingLot INSTANCE;
  private SpotStrategy spotStrategy;

  private ParkingLot() {}

  public static ParkingLot getInstance() {
    if (INSTANCE == null) {
      INSTANCE = new ParkingLot();
    }
    return INSTANCE;
  } 

  public void addFloor(Floor floor) {
    this.floors.add(floor);
  }

  public void setSpotStrategy(SpotStrategy spotStrategy) {
    this.spotStrategy = spotStrategy;
  }

  // parking spot if found, else null
  public ParkingSpot allocateSpot(Vehicle vehicle) {
    return spotStrategy.allocateSpot(vehicle, floors);
  }

  public void releaseSpot(ParkingSpot parkingSpot) {
    parkingSpot.markAvailable();
  }
}

public class Floor {
  private int floorNumber;
  private List<ParkingSpot> parkingSpots;

  public Floor(int floorNumber, List<ParkingSpot> parkingSpots) {
    this.floorNumber = floorNumber;
    this.parkingSpots = parkingSpots;
  }

  public int getFloorNumber() {
    return floorNumber;
  }

  public List<ParkingSpot> getParkingSpots() {
    return parkingSpots;
  }

  public List<ParkingSpot> getAvailableSpots(VehicleType vehicleType) {
    return parkingSpots.stream()
      .filter(spot -> spot.getSpotType() == vehicleType)
      .filter(spot -> spot.isAvailable())
      .toList();
  }
}

public class ParkingSpot {
  private ParkingSpotType spotType;
  private Vehicle vehicle;

  public ParkingSpot(ParkingSpotType spotType) {
    this.spotType = spotType;
  }

  public ParkingSpotType getSpotType() {
    return spotType;
  }

  public Vehicle getVehicle() {
    return vehicle;
  }

  public void markAvailable() {
    this.vehicle = null;
  }

  public void markOccupied(Vehicle vehicle) {
    this.vehicle = vehicle;
  }

  public boolean isAvailable() {
    return vehicle == null;
  }
}

public class Ticket {
  private ParkingSpot parkingSpot;
  private Vehicle vehicle;
  private LocalDateTime entryTime;
  private LocalDateTime exitTime;
  private FeeCalculationStrategy feeStrategy;

  public Ticket(ParkingSpot parkingSpot, Vehicle vehicle) {
    this.parkingSpot = parkingSpot;
    this.vehicle = vehicle;
    this.entryTime = LocalDateTime.now();
    this.exitTime = null;
  }

  public void setFeeStrategy(FeeCalculationStrategy feeStrategy) {
    this.feeStrategy = feeStrategy;
  }

  public ParkingSpot getParkingSpot() {
    return parkingSpot;
  }

  public Vehicle getVehicle() {
    return vehicle;
  }

  public LocalDateTime getEntryTime() {
    return entryTime;
  }
  
  public void markExited() {
    this.exitTime = LocalDateTime.now();
  }

  public double calculateFee() {
    return feeStrategy.calculateFee(this);
  }

  public void printDetails() {
    System.out.println("Ticket Details");
    System.out.println("Parking Spot: " + parkingSpot.getSpotType());
    System.out.println("Vehicle: " + vehicle.getVehicleType());
    System.out.println("Entry Time: " + entryTime);
    if (exitTime != null) {
      System.out.println("Exit Time: " + exitTime);
    }
    
  }
}

// multithreaded version
/**
public class ParkingLot {


```
