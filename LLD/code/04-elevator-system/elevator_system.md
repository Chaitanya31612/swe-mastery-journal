# Elevator System: The Master's Interview Playbook

This guide is designed not just to give you the code, but to teach you **the pattern of communication and thought** required to ace this problem in a 45-minute LLD interview.

---

## 🧠 The 5-Phase Interview Pattern
1. **Harvest & Clarify (5-7 mins):** Don't write code. Ask questions, lock down scope, identify the MVP.
2. **Entity & Relationship Mapping (5-10 mins):** Identify nouns (Entities) and verbs (Responsibilities). Talk out loud.
3. **Architecture & Patterns (5-10 mins):** Draw the class diagram. Propose Design Patterns (Strategy, Facade) before implementing them.
4. **Core Implementation (15-20 mins):** Write the skeleton first. Focus on the core algorithm. Leave getters/setters and boilerplate for last.
5. **Review & Scale (5 mins):** Critique your own code. Discuss concurrency, scale, and what breaks in production.

---

## Step 1: Requirement Harvest

**🧠 The Master's Approach:** Start by showing you know how to distill vague prompts into actionable engineering requirements. 

**🗣️ Interviewer Communication Script:**
> *"Before I jump into any design, I want to make sure we are aligned on the core requirements. An elevator system can range from a simple array simulation to a massive, real-time concurrent system. Let's define our MVP. I see the core requirements as..."*

**Core Requirements (The MVP)**
- Multiple elevators serving multiple floors.
- Internal requests (buttons inside the elevator: go to floor X).
- External requests (buttons on the floor: up/down).
- Elevators have states: moving up, moving down, idle.
- Dispatching algorithm to assign an external request to the best elevator.

**Out of Scope (Declare these to save time)**
- *"I'm going to assume we don't need to model the physics of acceleration or door timings, and we can treat movement as discrete logical steps. Is that fair?"*
- Hardware integration / raw multithreading (unless explicitly asked).

---

## Step 2: Clarifying Questions & Boundaries

**🧠 The Master's Approach:** This is where you avoid landmines. Ask questions that prove you foresee edge cases. 

**🗣️ Interviewer Communication Script:**
> *"I have a few clarifying questions about edge cases. First, how do we want to handle concurrency? Should I use actual threads with sleep, or a discrete tick-based simulation? (Pro-tip: Always push for tick-based/step-based simulation to avoid 30 mins of debugging race conditions). Second, what dispatch algorithm should we target? Nearest elevator? And do we care about weight limits right now?"*

**Assumptions Locked In:**
- **Concurrency:** Event-driven / Tick-based (`step()`). We advance time manually.
- **Algorithm:** LOOK algorithm (directional sweep). Elevator sweeps UP until no more UP requests, then reverses.
- **Capacity:** Assume infinite for MVP to save time.

---

## Step 3: Entity Identification (The Nouns)

**🧠 The Master's Approach:** Talk out loud while mapping concepts to classes. Show that you know the difference between an Entity, a Value Object, and a Service.

**🗣️ Interviewer Communication Script:**
> *"Let's identify the core entities. We clearly need an `Elevator` to maintain state. We need a `System` or `Controller` to manage them. For the requests, a simple `Request` object. Crucially, the logic to assign an elevator is complex and might change, so I want to extract that into a `Dispatcher` strategy."*

- **ElevatorSystem / Controller**: [Facade] Orchestrator.
- **Elevator**: [Actor] Maintains current floor, direction, and its own target stops.
- **Dispatcher**: [Strategy] Logic to assign external requests.
- **Request**: [ValueObject] Holds floor and direction.
- **Direction**: [Enum] UP, DOWN, IDLE.

---

## Step 4: Relationships & Responsibilities (The Verbs)

**🧠 The Master's Approach:** Define who owns what. Prevent God Classes.

**🗣️ Interviewer Communication Script:**
> *"To prevent the Controller from becoming a God Class, I want a decentralized design. The Controller just delegates external requests to the Dispatcher. The Dispatcher assigns the request to an Elevator. From there, the Elevator is completely autonomous—it uses the LOOK algorithm to decide its next move based on its internal queue."*

- **Controller** delegates to **Dispatcher**.
- **Dispatcher** reads **Elevator** states (read-only) and calls `assign()`.
- **Elevator** owns its internal Set of stops and mutates its own position on `step()`.

---

## Step 5: Class Diagram / Interface Design

**🧠 The Master's Approach:** Sketch this quickly. It acts as your blueprint.

**🗣️ Interviewer Communication Script:**
> *"Here is a rough sketch of how these classes interact. Notice how using the Strategy pattern for the Dispatcher means we can easily swap 'Nearest Elevator' for 'Odd/Even Floors' without touching the core logic."*

```text
 +------------------+        +-------------------+
 |    Controller    | 1----* |     Elevator      |
 |------------------|        |-------------------|
 | -elevators       |        | -id, floor, dir   |
 | -dispatcher      |        | -requests (Set)   |
 |------------------|        |-------------------|
 | +external_request|        | +add_request(flr) |
 | +internal_request|        | +step()           |
 | +step()          |        +-------------------+
 +--------+---------+                 ^
          |                           |
          | uses                      | assigns
          v                           |
 +------------------+                 |
 | <<Strategy>>     |                 |
 |    Dispatcher    | ----------------+
 |------------------|
 | +assign(request, |
 |         elevators|
 +------------------+
```

---

## Step 6: Core Implementation

**🧠 The Master's Approach:** Start with the interfaces and the hardest logic first (The LOOK algorithm). Talk through your logic as you type.

**🗣️ Interviewer Communication Script (While coding):**
> *"I'm going to start with the Elevator class because the LOOK algorithm is the heart of the problem. I'm using a `Set` for requests because an elevator only needs to know IF it should stop at floor X, not how many people pressed the button."*

# ============================================================
# CODE BEGINS
# ============================================================

```ruby
# frozen_string_literal: true
require 'set'

module ElevatorSystem
  module Direction
    UP   = :up
    DOWN = :down
    IDLE = :idle
  end

  class Request
    attr_reader :floor, :direction

    def initialize(floor:, direction: Direction::IDLE)
      @floor = floor
      @direction = direction
    end
  end

  # =================================================================
  # ELEVATOR (The Actor)
  # =================================================================
  class Elevator
    attr_reader :id, :current_floor, :direction, :doors_open

    def initialize(id:, start_floor: 0)
      @id = id
      @current_floor = start_floor
      @direction = Direction::IDLE
      @requests = Set.new # Set is perfect: dedupes multiple button presses
      @doors_open = false
    end

    # Called by Dispatcher or internal buttons
    def add_request(floor)
      @requests.add(floor)
      update_direction if @direction == Direction::IDLE
    end

    # The event loop tick
    def step
      if @doors_open
        @doors_open = false # Close doors after 1 tick
        update_direction
        return
      end

      return if @direction == Direction::IDLE

      move
      check_arrival
    end

    def summary
      "Elevator #{@id}: Floor #{@current_floor} | #{@direction.to_s.upcase} | Req: #{@requests.to_a.sort}"
    end

    private

    def move
      @current_floor += 1 if @direction == Direction::UP
      @current_floor -= 1 if @direction == Direction::DOWN
    end

    def check_arrival
      if @requests.include?(@current_floor)
        @requests.delete(@current_floor)
        @doors_open = true
      end
    end

    # LOOK Algorithm Core Logic
    # Sweep in current direction until no more requests, then reverse
    def update_direction
      if @requests.empty?
        @direction = Direction::IDLE
        return
      end

      case @direction
      when Direction::UP
        @direction = Direction::DOWN unless requests_above?
      when Direction::DOWN
        @direction = Direction::UP unless requests_below?
      when Direction::IDLE
        closest = @requests.min_by { |f| (f - @current_floor).abs }
        @direction = closest > @current_floor ? Direction::UP : Direction::DOWN
      end
    end

    def requests_above?
      @requests.any? { |f| f > @current_floor }
    end

    def requests_below?
      @requests.any? { |f| f < @current_floor }
    end
  end

  # =================================================================
  # DISPATCHER (The Strategy)
  # =================================================================
  class Dispatcher
    def assign(request, elevators)
      raise NotImplementedError
    end
  end

  class NearestDispatcher < Dispatcher
    def assign(request, elevators)
      best_elevator = elevators.min_by do |elevator|
        suitability_score(request, elevator)
      end
      best_elevator.add_request(request.floor)
    end

    private

    def suitability_score(request, elevator)
      distance = (elevator.current_floor - request.floor).abs

      return distance if elevator.direction == Direction::IDLE

      # Perfect match: moving towards the request in the exact direction needed
      if moving_towards?(elevator, request.floor) && elevator.direction == request.direction
        return distance
      end

      # Penalty: elevator is moving away or in wrong direction. 
      # It will have to finish its sweep and come back.
      distance + 1000 
    end

    def moving_towards?(elevator, target_floor)
      if elevator.direction == Direction::UP
        elevator.current_floor < target_floor
      elsif elevator.direction == Direction::DOWN
        elevator.current_floor > target_floor
      else
        false
      end
    end
  end

  # =================================================================
  # CONTROLLER (The Facade)
  # =================================================================
  class Controller
    attr_reader :elevators

    def initialize(num_elevators:, dispatcher: NearestDispatcher.new)
      @elevators = Array.new(num_elevators) { |i| Elevator.new(id: i + 1) }
      @dispatcher = dispatcher
    end

    def external_request(floor:, direction:)
      req = Request.new(floor: floor, direction: direction)
      @dispatcher.assign(req, @elevators)
    end

    def internal_request(elevator_id:, floor:)
      elevator = @elevators.find { |e| e.id == elevator_id }
      elevator&.add_request(floor)
    end

    def step
      @elevators.each(&:step)
    end

    def debug_state
      @elevators.each { |e| puts e.summary }
      puts "-" * 40
    end
  end
end
```

---

## Step 7: Post-Solve Reflection (The "Senior" Close-Out)

**🧠 The Master's Approach:** Don't wait for them to find flaws. Point out the flaws in your own design before they do. This shows maturity and production experience.

**🗣️ Interviewer Communication Script:**
> *"Alright, the core logic is complete and handles the LOOK sweep. If we were putting this into production, I'd immediately want to address a few bottlenecks. First is starvation: this basic Nearest Dispatcher can starve requests at the very top or bottom of the building if the middle floors are highly active. We'd need to add an 'aging' mechanism to increase priority over time. Second, thread safety: right now, mutating the elevator's internal Set while it is calculating its next move would cause a race condition. In a real system, we'd use a thread-safe message queue for each actor."*

### What Else Could Break / Follow-Up Defenses

**Q: "How would you handle weight limits?"**
> **A:** *"I'd add a `current_weight` property to the Elevator. In `check_arrival()`, we'd simulate passengers boarding and check capacity. If `current_weight > capacity`, the elevator sets an `OVERWEIGHT` flag, refuses to close doors, and sounds an alarm. Furthermore, the Dispatcher must skip elevators that are currently full."*

**Q: "Why did you use `step()` instead of spawning a Thread with `sleep()`?"**
> **A:** *"Predictability and testability. In a 45-minute interview, debugging multi-threaded timing issues is a trap. `step()` is a discrete event simulation. It allows us to write deterministic unit tests: 'Given state A, after 3 steps, assert state B'. In production, this maps cleanly to a game loop or an actor model processing a message queue."*

### ❌ The "Junior" Trap (What most people get wrong)
Juniors try to make the central `Controller` micromanage the elevators. They write massive `if/else` blocks in the controller: `if elevator1.floor == 5, move elevator1 up`. 
**The Senior Move:** Decentralize. The Controller just hands out jobs. The Elevator manages its own state and sweeps its own queue. This adheres to Single Responsibility and mirrors real-world distributed hardware.
