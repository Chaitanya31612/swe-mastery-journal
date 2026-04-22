# PARKING LOT SYSTEM - RUBY IMPLEMENTATION
# ----------------------------------------
# This is a self-contained demonstration of a complete, interview-ready Parking Lot LLD.
#
# TRADE-OFF DISCUSSION in Ruby context:
# 1. Duck Typing vs interfaces: Ruby doesn't have formal interfaces. We use base classes
#    with `StandardError` raises to document "Contracts" and mimic Strategy interfaces.
# 2. Concurrency: Ruby uses a GVL (Global VM Lock) in MRI, but thread-safety is still important
#    for instance variables. Mutex is used to prevent race conditions.
# 3. Code conciseness: Ruby allows much shorter code than Java, making it great for 
#    interviews if the interviewer permits it.

require 'thread'
require 'securerandom'

# ==========================================
# 1. CONSTANTS / ENUMS
# ==========================================
# Ruby uses Symbols instead of Enums natively
VEHICLE_TYPES = [:bike, :car, :truck].freeze
SPOT_TYPES = [:small, :medium, :large].freeze

# ==========================================
# 2. CORE MODELS
# ==========================================
class Vehicle
  attr_reader :license_plate, :type

  def initialize(license_plate, type)
    @license_plate = license_plate
    @type = type
  end
end

class Bike < Vehicle
  def initialize(license_plate)
    super(license_plate, :bike)
  end
end

class Car < Vehicle
  def initialize(license_plate)
    super(license_plate, :car)
  end
end

class Truck < Vehicle
  def initialize(license_plate)
    super(license_plate, :truck)
  end
end

class ParkingSpot
  attr_reader :spot_number, :spot_type, :parked_vehicle

  def initialize(spot_number, spot_type)
    @spot_number = spot_number
    @spot_type = spot_type
    @is_free = true
    @parked_vehicle = nil
  end

  def free?
    @is_free
  end

  def park(vehicle)
    @parked_vehicle = vehicle
    @is_free = false
  end

  def vacate
    @parked_vehicle = nil
    @is_free = true
  end
end

class Floor
  attr_reader :floor_number, :spots

  def initialize(floor_number, spots)
    @floor_number = floor_number
    @spots = spots
  end
end

class Ticket
  attr_reader :ticket_id, :vehicle, :spot, :entry_time

  def initialize(ticket_id, vehicle, spot)
    @ticket_id = ticket_id
    @vehicle = vehicle
    @spot = spot
    @entry_time = Time.now
  end
end

# ==========================================
# 3. EXCEPTIONS
# ==========================================
class ParkingLotFullError < StandardError; end
class InvalidTicketError < StandardError; end

# ==========================================
# 4. STRATEGIES (Abstractions + Implementations)
# ==========================================

# Base Abstract Strategy
class ParkingStrategy
  def find_spot(vehicle_type, floors)
    raise NotImplementedError, "Implement this method in a subclass"
  end
end

class NearestFirstParkingStrategy < ParkingStrategy
  def find_spot(vehicle_type, floors)
    required_spot_type = map_vehicle_to_spot(vehicle_type)

    floors.each do |floor|
      floor.spots.each do |spot|
        return spot if spot.free? && spot.spot_type == required_spot_type
      end
    end

    raise ParkingLotFullError, "No available spot for #{vehicle_type}"
  end

  private

  def map_vehicle_to_spot(type)
    case type
    when :bike then :small
    when :car then :medium
    when :truck then :large
    else raise ArgumentError, "Unknown Vehicle Type"
    end
  end
end

class PricingStrategy
  def calculate_price(ticket)
    raise NotImplementedError, "Implement this method in a subclass"
  end
end

class HourlyPricingStrategy < PricingStrategy
  HOURLY_RATE = 10.0

  def calculate_price(ticket)
    # Mocking actual duration for demonstration purposes.
    # Actual code: ((Time.now - ticket.entry_time) / 3600.0).ceil
    hours_parked = 2
    hours_parked * HOURLY_RATE
  end
end

# ==========================================
# 5. THE FACADE / SINGLETON CONTROLLER
# ==========================================
require 'singleton'

class ParkingLot
  include Singleton

  def initialize
    @active_tickets = {}
    @ticket_counter = 1
    @mutex = Mutex.new # Ensures thread safety during assignment
  end

  def setup(floors:, parking_strategy:, pricing_strategy:)
    @floors = floors
    @parking_strategy = parking_strategy
    @pricing_strategy = pricing_strategy
  end

  def park_vehicle(vehicle)
    @mutex.synchronize do
      spot = @parking_strategy.find_spot(vehicle.type, @floors)
      spot.park(vehicle)

      ticket_id = "TKT-#{@ticket_counter}"
      @ticket_counter += 1

      ticket = Ticket.new(ticket_id, vehicle, spot)
      @active_tickets[ticket_id] = ticket

      puts "Parked #{vehicle.type} at Spot #{spot.spot_number} with #{ticket_id}"
      ticket
    end
  end

  def unpark_vehicle(ticket_id)
    ticket = @active_tickets[ticket_id]
    raise InvalidTicketError, "Ticket ID not found: #{ticket_id}" unless ticket

    spot = ticket.spot
    spot.vacate
    
    price = @pricing_strategy.calculate_price(ticket)
    @active_tickets.delete(ticket_id)

    puts "Unparked ticket #{ticket_id}. Paid: $#{price}"
    price
  end
end

# ==========================================
# 6. MAIN DEMO
# ==========================================
if __FILE__ == $0
  puts "Initializing Parking Lot System..."

  # 1. Initialize Floors
  floor1 = Floor.new(1, [
    ParkingSpot.new(101, :small),
    ParkingSpot.new(102, :medium)
  ])

  floor2 = Floor.new(2, [
    ParkingSpot.new(201, :small),
    ParkingSpot.new(202, :medium)
  ])

  # 2. Setup Strategies
  parking_strategy = NearestFirstParkingStrategy.new
  pricing_strategy = HourlyPricingStrategy.new

  # 3. Setup Parking Lot
  lot = ParkingLot.instance
  lot.setup(
    floors: [floor1, floor2],
    parking_strategy: parking_strategy,
    pricing_strategy: pricing_strategy
  )

  # 4. Run Scenarios
  begin
    puts "\n--- PARKING ---"
    t1 = lot.park_vehicle(Bike.new("BIKE-01"))
    t2 = lot.park_vehicle(Car.new("CAR-01"))
    t3 = lot.park_vehicle(Car.new("CAR-02"))

    puts "\n--- UNPARKING ---"
    lot.unpark_vehicle(t2.ticket_id)

    puts "\n--- PARKING NEW CAR ---"
    t4 = lot.park_vehicle(Car.new("CAR-03"))
  rescue StandardError => e
    puts "Error: #{e.message}"
  end
end
