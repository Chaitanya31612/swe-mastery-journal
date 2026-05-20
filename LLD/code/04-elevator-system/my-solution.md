# Elevator System

## Problem Statement
Design a system that manages elevators in a building.

## Requirements

### Core
1. Multiple elevators servicing multiple floors (N elevators, M floors), via a single controller
2. Elevator can be controlled from inside and outside - two type of requests - Internal and External
    1. Internal requests - person is inside an elevator, and wants to go to some other floor
    2. External requests - person is outside an elevator, and selects a direction to go to (UP or DOWN)
3. Multiple strategies to service floors
   -  one strategy is, first find elevator moving in same direction selected by user, and corresponding current position of elevator
   with respect to the floor user is on. If found, assign request to this elevator. Otherwise
   - Find the nearest idle elevator
4. we'll use step() or simulilution to indicate elevator moving

### Nice to haves (out of scope)
1. Hardware integration, weight restriction, door open/close logic, fire mode, etc
2. floor wise elevator allocation and distribution

## Entities and Data model

### Entities (Nouns)
- Elevator (class)
- Floor (number, property)
- Request (class, floor, direction)
- ElevatorController (class)

### Actions (verbs)
- step
- add request
- select elevator

```ruby

class Elevator
- id <int>
- current_floor <int>
- direction <Enum: UP, DOWN>
- state <Enum: MOVING, DOOR_OPEN, IDLE>
- requests <Set<Integer>> # we only need to service floor from inside the elevator

+ add_request(floor: int): void
+ step(): void
+ get_direction(): Enum: UP, DOWN, IDLE
+ get_cur_floor(): int
+ open_door(): void

enum Direction
- UP
- DOWN
- IDLE

class Request
- floor: int
- direction: Enum: UP, DOWN
- timestamp: Time

+ is_external?: bool

class InternalRequest < Request

class ExternalRequest < Request
- floor <Optional>

class ElevatorController
- elevators: Array<Elevator>
- total_floors: int
- selection_strategy: SelectionStrategy

+ select_elevator(request: Request): Elevator
+ add_request(request: Request): void
+ step()
- internal_request(elevator_id, floor): void
- external_request(floor, direction): void

class SelectionStrategy
+ select_elevator(request: Request, elevators: Array<Elevator>): Elevator


```

### Relationship

ElevatorController 1..* Elevator
ElevatorController 1 1 SelectionStrategy
Elevator 1 * Request
Request < InternalRequest, ExternalRequest


```ruby

enum Direction: UP, DOWN
enum ElevatorState: MOVING, DOOR_OPEN, IDLE

class Request
  attr_reader :floor, :direction, :elevator_id
  def initialize(floor, direction, elevator_id = nil)
    @floor = floor
    @direction = direction
    @elevator_id = elevator_id
    @timestamp = Time.now
  end

  def is_external?
    return !@elevator_id
  end
end

class ElevatorController
  attr_accessor :elevators, :total_floors, :selection_strategy

  def initialize(elevators, total_floors, selection_strategy)
    @elevators = elevators
    @total_floors = total_floors
    @selection_strategy = selection_strategy
  end

  def add_request(request: Request): void
    elevator = select_elevator(request) if request.is_external?
    raise "Error: No suitable elevator found for request: #{request}" if elevator.nil?

    elevator.add_request(request.floor)
  end

  def step
    elevators.each { |elevator| elevator.step }
  end

  def select_elevator(request: Request): Elevator
    selection_strategy.select_elevator(request, elevators)
  end
end

class Elevator
  attr :id, :current_floor, :direction, :state, :requests

  def initialize(id)
    @id = id
    @current_floor = 0
    @direction = nil
    @state = IDLE
    @requests = Set.new
  end

  def add_request(floor)
    requests.add(floor)
  end

  # State machine logic
  def step
    case state
    when IDLE
      next if requests.empty?



    when DOOR_OPEN
    when MOVING
      if requests.include? current_floor
        state = OPEN_DOOR
        requests.delete(current_floor)
        return
      end

      raise "Invalid floor: #{current_floor}" if current_floor < 0 || current_floor > TOTAL_FLOORS

      if direction == UP
        # check if there are requests above
        has_requests_above = requests.any? { |floor| floor > current_floor }
        if has_requests_above
          current_floor += 1
        else
          # if not, check if there are any below, change to down
          has_requests_below = requests.any? { |floor| floor < current_floor }
          if has_requests_below
            direction = DOWN
            current_floor -= 1
          else
            # if none, change to IDLE
            direction = IDLE
            state = IDLE
          end
        elsif direction == DOWN
          # check if there are requests below
          has_requests_below = requests.any? { |floor| floor < current_floor }
          if has_requests_below
            current_floor -= 1
          else
            # if not, check if there are any above, change to up
            has_requests_above = requests.any? { |floor| floor > current_floor }
            if has_requests_above
              direction = UP
            else
              # if none, change to IDLE
              direction = IDLE
            end
          end
        end
      end
    end
  end
end





```
