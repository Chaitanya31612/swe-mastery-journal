# 🎬 Movie Ticket Booking System (BookMyShow) — LLD Solution

This document outlines the ideal and practical Low-Level Design (LLD) for a Movie Ticket Booking System (like BookMyShow). It is structured specifically for LLD technical interviews, focusing on clean object-oriented design, proper entity associations, and solving the critical concurrency and double-booking challenges.

---

## 1. Interview Starter: Clarifying Questions & Scope

At the beginning of an LLD interview, you must clarify the scope by asking the interviewer targeted questions. Here are the key questions to establish boundaries:

1. **How are seats allocated?** Can users select their own seats, or does the system assign them?  
   *Direction:* Assume users choose their own seats from a visual seat map.
2. **What is the reservation lifecycle?** When is a seat locked? How long does a user have to complete the payment?  
   *Direction:* When a user selects seats and proceeds to checkout, they are temporarily locked for **5–10 minutes** (TTL). If payment fails or times out, they are released.
3. **How do we handle search/discovery?**  
   *Direction:* Users can search by movie, city, theatre, or time. Keep this interface simple to focus on booking and concurrency.
4. **Is cancellation and refund supported?**  
   *Direction:* Yes, bookings can be cancelled, releasing the seats and initiating refunds. Keep the refund payment flow mockable.

---

## 2. Requirements & Boundaries

### Core (Must-Have) Requirements
- **Hierarchy:** Multiple cities $\rightarrow$ multiple theatres $\rightarrow$ multiple screens $\rightarrow$ multiple shows.
- **Show Structure:** A `Show` represents a specific `Movie` playing on a specific `Screen` at a specific time.
- **Seat Map:** Each `Show` has its own seat map. Seats have types (e.g., *Silver, Gold, Platinum*) with different pricing.
- **Booking Flow:** Search movies $\rightarrow$ Select a show $\rightarrow$ Choose seats $\rightarrow$ Lock seats temporarily $\rightarrow$ Make payment $\rightarrow$ Confirm booking.
- **Concurrency:** Ensure **no two users** can book or temporarily lock the same seat simultaneously.

### Out of Scope (for the core LLD coding part)
- User Authentication/Authorization.
- Direct integration with actual Payment Gateway APIs (use a Mock Payment Service instead).
- Notifications (email/SMS sending details—can mock with observers).

---

## 3. Core Entities & Associations

A common pitfall in this LLD is mixing the static physical seat structure with dynamic, show-specific booking states. The **Seat vs. ShowSeat** design pattern is the key differentiator of a senior candidate.

### The Seat vs. ShowSeat Design Pattern
* **`Seat` (Static):** Represents the physical seat on a `Screen` (e.g., Row G, Number 12, Gold Category). It does *not* change based on the movie or time.
* **`ShowSeat` (Dynamic):** Represents the state of a `Seat` for a specific `Show` (e.g., for the 9 PM show of "Inception", Seat G12 is `LOCKED` or `BOOKED`).

### Domain Model Associations
* **`Theatre`** has a 1-to-many (`1 -> *`) relationship with **`Screen`**.
* **`Screen`** has a 1-to-many (`1 -> *`) relationship with **`Seat`**.
* **`Show`** is associated with 1 **`Movie`** and 1 **`Screen`**.
* **`Show`** contains a 1-to-many (`1 -> *`) list of **`ShowSeat`**s.
* **`Booking`** is associated with 1 **`Show`**, 1 **`User`**, and multiple **`ShowSeat`**s.

```
[Theatre] 1 ──── * [Screen] 1 ──── * [Seat] (Static Row/Col/Type)
                      1                │ 1
                      │                │
                      *                *
                   [Show] 1 ──── * [ShowSeat] (Dynamic Status/TTL/Booking)
                      1                *
                      │                │
                      │ 1              │
                  [Movie]           [Booking] 1 ── 1 [Payment]
```

### State Transitions
* **`ShowSeatStatus`:** `AVAILABLE` $\rightarrow$ `LOCKED` $\rightarrow$ `BOOKED` (or revert to `AVAILABLE` on TTL expiry).
* **`BookingStatus`:** `PENDING` $\rightarrow$ `CONFIRMED` or `EXPIRED` or `CANCELLED`.

---

## 4. Resolving Concurrency & Double Booking

The core technical challenge in BookMyShow is handling **concurrent bookings** for the same seat. 

### Step 1: Temporary Locking with TTL (Lazy Expiration)
When a user selects seats:
1. Try to lock the seats. If any seat is already locked or booked, fail the request immediately.
2. If available, change status to `LOCKED` and set a `lockExpiresAt` timestamp (current time + 5 minutes).
3. **Lazy Expiration:** During subsequent checks, if a seat is `LOCKED` but `lockExpiresAt` has passed, treat it as `AVAILABLE`. This avoids needing heavy background cron jobs or active pollers just to release expired locks.

### Step 2: Thread-Safe Lock Management (Show-Level Locking)
Instead of synchronizing the entire booking method (which blocks bookings globally and degrades performance), synchronize at the **Show Level**. Since two users booking tickets for different movies or different screens do not conflict, we only need to serialize operations on the **same show**.

* **Implementation:** Maintain a map of Show IDs to lock objects (e.g., `ReentrantLock` in Java or `Mutex` in Ruby). Acquire the lock for `showId` before verifying availability and updating status.

---

## 5. Design Patterns Applied

| Design Pattern | Where & Why |
| :--- | :--- |
| **Strategy Pattern** | **Pricing Calculation:** Calculate show prices dynamically based on seat types (Silver/Gold/Platinum), day of the week, or time of day. |
| **State Pattern** | **Booking States:** Transition bookings through various phases (`PENDING` $\rightarrow$ `CONFIRMED`/`EXPIRED`/`CANCELLED`) with distinct behaviors. |
| **Observer Pattern** | **Notifications:** Notify users (via Email, SMS, or Push Notification services) upon booking confirmation or cancellation. |

---

## 6. Java Implementation

Here is the clean, thread-safe Java implementation of the booking system.

```java
import java.time.LocalDateTime;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.locks.ReentrantLock;

// --- ENUMS ---
enum SeatType {
    SILVER(100.0), GOLD(150.0), PLATINUM(250.0);
    private final double basePrice;
    SeatType(double basePrice) { this.basePrice = basePrice; }
    public double getBasePrice() { return basePrice; }
}

enum ShowSeatStatus {
    AVAILABLE, LOCKED, BOOKED
}

enum BookingStatus {
    PENDING, CONFIRMED, CANCELLED, EXPIRED
}

// --- CORE MODELS ---
class Movie {
    private final String id;
    private final String title;
    private final int durationMinutes;

    public Movie(String id, String title, int durationMinutes) {
        this.id = id;
        this.title = title;
        this.durationMinutes = durationMinutes;
    }
    public String getId() { return id; }
    public String getTitle() { return title; }
}

class Seat {
    private final String id;
    private final String row;
    private final int column;
    private final SeatType seatType;

    public Seat(String id, String row, int column, SeatType seatType) {
        this.id = id;
        this.row = row;
        this.column = column;
        this.seatType = seatType;
    }
    public String getId() { return id; }
    public SeatType getSeatType() { return seatType; }
}

class Screen {
    private final String id;
    private final String name;
    private final List<Seat> seats;

    public Screen(String id, String name, List<Seat> seats) {
        this.id = id;
        this.name = name;
        this.seats = seats;
    }
    public String getId() { return id; }
    public List<Seat> getSeats() { return seats; }
}

class Theatre {
    private final String id;
    private final String name;
    private final String city;
    private final List<Screen> screens;

    public Theatre(String id, String name, String city) {
        this.id = id;
        this.name = name;
        this.city = city;
        this.screens = new ArrayList<>();
    }
    public void addScreen(Screen screen) { screens.add(screen); }
    public String getId() { return id; }
    public String getCity() { return city; }
    public List<Screen> getScreens() { return screens; }
}

class ShowSeat {
    private final String id;
    private final Seat seat;
    private final Show show;
    private ShowSeatStatus status;
    private LocalDateTime lockExpiresAt;
    private String lockedByBookingId;

    public ShowSeat(String id, Seat seat, Show show) {
        this.id = id;
        this.seat = seat;
        this.show = show;
        this.status = ShowSeatStatus.AVAILABLE;
    }

    public boolean isAvailable() {
        if (status == ShowSeatStatus.AVAILABLE) return true;
        // Lazy expiration of locked seats
        if (status == ShowSeatStatus.LOCKED && LocalDateTime.now().isAfter(lockExpiresAt)) {
            unlock();
            return true;
        }
        return false;
    }

    public void lock(String bookingId, int lockDurationSeconds) {
        this.status = ShowSeatStatus.LOCKED;
        this.lockExpiresAt = LocalDateTime.now().plusSeconds(lockDurationSeconds);
        this.lockedByBookingId = bookingId;
    }

    public void unlock() {
        this.status = ShowSeatStatus.AVAILABLE;
        this.lockExpiresAt = null;
        this.lockedByBookingId = null;
    }

    public void book() {
        if (status != ShowSeatStatus.LOCKED) {
            throw new IllegalStateException("Seat must be locked before booking confirmation!");
        }
        this.status = ShowSeatStatus.BOOKED;
        this.lockExpiresAt = null;
    }

    public Seat getSeat() { return seat; }
    public String getLockedByBookingId() { return lockedByBookingId; }
    public ShowSeatStatus getStatus() { return status; }
}

class Show {
    private final String id;
    private final Movie movie;
    private final Screen screen;
    private final LocalDateTime startTime;
    private final Map<String, ShowSeat> showSeats;

    public Show(String id, Movie movie, Screen screen, LocalDateTime startTime) {
        this.id = id;
        this.movie = movie;
        this.screen = screen;
        this.startTime = startTime;
        this.showSeats = new HashMap<>();
        // Initialize show seats from the screen's layout
        for (Seat seat : screen.getSeats()) {
            this.showSeats.put(seat.getId(), new ShowSeat(id + "-" + seat.getId(), seat, this));
        }
    }

    public String getId() { return id; }
    public Map<String, ShowSeat> getShowSeats() { return showSeats; }
}

class User {
    private final String id;
    private final String name;
    private final String email;

    public User(String id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }
    public String getId() { return id; }
}

class Booking {
    private final String id;
    private final User user;
    private final Show show;
    private final List<ShowSeat> bookedSeats;
    private final double totalAmount;
    private BookingStatus status;
    private final LocalDateTime createdAt;

    public Booking(String id, User user, Show show, List<ShowSeat> bookedSeats, double totalAmount) {
        this.id = id;
        this.user = user;
        this.show = show;
        this.bookedSeats = bookedSeats;
        this.totalAmount = totalAmount;
        this.status = BookingStatus.PENDING;
        this.createdAt = LocalDateTime.now();
    }

    public void confirm() { this.status = BookingStatus.CONFIRMED; }
    public void cancel() { this.status = BookingStatus.CANCELLED; }
    public void expire() { this.status = BookingStatus.EXPIRED; }

    public String getId() { return id; }
    public Show getShow() { return show; }
    public List<ShowSeat> getBookedSeats() { return bookedSeats; }
    public BookingStatus getStatus() { return status; }
    public double getTotalAmount() { return totalAmount; }
}

// --- BOOKING SERVICE (Orchestrator) ---
class BookingService {
    private final ConcurrentHashMap<String, ReentrantLock> showLocks = new ConcurrentHashMap<>();
    private final Map<String, Booking> bookings = new ConcurrentHashMap<>();

    public Booking createBooking(User user, Show show, List<String> seatIds) {
        String bookingId = UUID.randomUUID().toString();
        
        // Step 1: Acquire show-specific lock to prevent race conditions on seats
        ReentrantLock showLock = showLocks.computeIfAbsent(show.getId(), k -> new ReentrantLock());
        showLock.lock();
        try {
            List<ShowSeat> seatsToLock = new ArrayList<>();
            Map<String, ShowSeat> showSeatMap = show.getShowSeats();

            // Step 2: Validate all requested seats are available (considering TTL expiration)
            for (String seatId : seatIds) {
                ShowSeat showSeat = showSeatMap.get(seatId);
                if (showSeat == null || !showSeat.isAvailable()) {
                    throw new IllegalArgumentException("Seat " + seatId + " is not available!");
                }
                seatsToLock.add(showSeat);
            }

            // Step 3: Lock seats temporarily (e.g., 5 seconds for simulation/testing)
            double totalAmount = 0;
            for (ShowSeat seat : seatsToLock) {
                seat.lock(bookingId, 5); // 5-second TTL lock
                totalAmount += seat.getSeat().getSeatType().getBasePrice();
            }

            // Step 4: Create booking entity
            Booking booking = new Booking(bookingId, user, show, seatsToLock, totalAmount);
            bookings.put(bookingId, booking);
            return booking;

        } finally {
            showLock.unlock();
        }
    }

    public void confirmPayment(String bookingId) {
        Booking booking = bookings.get(bookingId);
        if (booking == null) throw new IllegalArgumentException("Booking not found!");

        ReentrantLock showLock = showLocks.get(booking.getShow().getId());
        if (showLock != null) {
            showLock.lock();
        }
        try {
            synchronized (booking) {
                if (booking.getStatus() != BookingStatus.PENDING) {
                    throw new IllegalStateException("Booking is not in PENDING state!");
                }

                // Check if seats have expired their lock
                boolean hasExpired = false;
                for (ShowSeat seat : booking.getBookedSeats()) {
                    if (!bookingId.equals(seat.getLockedByBookingId()) || seat.getStatus() != ShowSeatStatus.LOCKED) {
                        hasExpired = true;
                        break;
                    }
                }

                if (hasExpired) {
                    booking.expire();
                    throw new IllegalStateException("Payment succeeded too late; seats have been released!");
                }

                // Finalize seats and booking
                for (ShowSeat seat : booking.getBookedSeats()) {
                    seat.book();
                }
                booking.confirm();
                System.out.println("Booking " + bookingId + " successfully CONFIRMED!");
            }
        } finally {
            if (showLock != null) {
                showLock.unlock();
            }
        }
    }

    public void handleLockExpiration(String bookingId) {
        Booking booking = bookings.get(bookingId);
        if (booking == null || booking.getStatus() != BookingStatus.PENDING) return;

        synchronized (booking) {
            // Re-verify expiration and release seats
            for (ShowSeat seat : booking.getBookedSeats()) {
                if (bookingId.equals(seat.getLockedByBookingId())) {
                    seat.unlock();
                }
            }
            booking.expire();
            System.out.println("Booking " + bookingId + " has EXPIRED. Seats released.");
        }
    }
}

// --- CONCURRENCY DEMO ---
public class BookingDemo {
    public static void main(String[] args) throws InterruptedException {
        // Init Movie
        Movie movie = new Movie("m-1", "Inception", 148);

        // Init Seats
        List<Seat> seats = Arrays.asList(
            new Seat("s1", "A", 1, SeatType.GOLD),
            new Seat("s2", "A", 2, SeatType.GOLD),
            new Seat("s3", "A", 3, SeatType.SILVER)
        );

        // Init Screen & Theatre
        Screen screen = new Screen("scr-1", "Screen 1", seats);
        Theatre theatre = new Theatre("t-1", "PVR Cinemas", "Mumbai");
        theatre.addScreen(screen);

        // Create a Show
        Show show = new Show("sh-1", movie, screen, LocalDateTime.now().plusHours(2));

        BookingService bookingService = new BookingService();

        User user1 = new User("u-1", "Alice", "alice@example.com");
        User user2 = new User("u-2", "Bob", "bob@example.com");

        List<String> seatsToBook = Arrays.asList("s1", "s2");

        // Thread 1: Alice tries to book seats s1, s2
        Thread t1 = new Thread(() -> {
            try {
                Booking booking = bookingService.createBooking(user1, show, seatsToBook);
                System.out.println("Alice successfully locked seats. Booking ID: " + booking.getId());
                // Simulate quick payment
                Thread.sleep(1000);
                bookingService.confirmPayment(booking.getId());
            } catch (Exception e) {
                System.out.println("Alice booking failed: " + e.getMessage());
            }
        });

        // Thread 2: Bob tries to book same seats s1, s2 simultaneously
        Thread t2 = new Thread(() -> {
            try {
                // Wait slightly to guarantee Alice gets lock first, or execute simultaneously
                Thread.sleep(200);
                Booking booking = bookingService.createBooking(user2, show, seatsToBook);
                System.out.println("Bob successfully locked seats. Booking ID: " + booking.getId());
                bookingService.confirmPayment(booking.getId());
            } catch (Exception e) {
                System.out.println("Bob booking failed: " + e.getMessage());
            }
        });

        t1.start();
        t2.start();

        t1.join();
        t2.join();
    }
}
```

---

## 7. Ruby Implementation

Here is the equivalent Ruby implementation leveraging a thread-safe design.

```ruby
require 'securerandom'
require 'thread'

# --- ENUMS (represented as Symbols) ---
# Seat Types: :silver, :gold, :platinum
# Show Seat Status: :available, :locked, :booked
# Booking Status: :pending, :confirmed, :cancelled, :expired

class Movie
  attr_reader :id, :title, :duration_minutes

  def initialize(id, title, duration_minutes)
    @id = id
    @title = title
    @duration_minutes = duration_minutes
  end
end

class Seat
  attr_reader :id, :row, :column, :seat_type

  def initialize(id, row, column, seat_type)
    @id = id
    @row = row
    @column = column
    @seat_type = seat_type # :silver, :gold, or :platinum
  end

  def base_price
    case @seat_type
    when :silver then 100.0
    when :gold then 150.0
    when :platinum then 250.0
    else 0.0
    end
  end
end

class Screen
  attr_reader :id, :name, :seats

  def initialize(id, name, seats)
    @id = id
    @name = name
    @seats = seats
  end
end

class Theatre
  attr_reader :id, :name, :city, :screens

  def initialize(id, name, city)
    @id = id
    @name = name
    @city = city
    @screens = []
  end

  def add_screen(screen)
    @screens << screen
  end
end

class ShowSeat
  attr_reader :id, :seat, :show, :status, :lock_expires_at, :locked_by_booking_id

  def initialize(id, seat, show)
    @id = id
    @seat = seat
    @show = show
    @status = :available
    @lock_expires_at = nil
    @locked_by_booking_id = nil
  end

  def available?
    return true if @status == :available
    
    # Lazy lock expiration check
    if @status == :locked && Time.now > @lock_expires_at
      unlock
      return true
    end
    
    false
  end

  def lock(booking_id, duration_seconds)
    @status = :locked
    @lock_expires_at = Time.now + duration_seconds
    @locked_by_booking_id = booking_id
  end

  def unlock
    @status = :available
    @lock_expires_at = nil
    @locked_by_booking_id = nil
  end

  def book
    raise "Seat must be locked before booking!" unless @status == :locked
    @status = :booked
    @lock_expires_at = nil
  end
end

class Show
  attr_reader :id, :movie, :screen, :start_time, :show_seats

  def initialize(id, movie, screen, start_time)
    @id = id
    @movie = movie
    @screen = screen
    @start_time = start_time
    @show_seats = {}

    screen.seats.each do |seat|
      @show_seats[seat.id] = ShowSeat.new("#{id}-#{seat.id}", seat, self)
    end
  end
end

class User
  attr_reader :id, :name, :email

  def initialize(id, name, email)
    @id = id
    @name = name
    @email = email
  end
end

class Booking
  attr_reader :id, :user, :show, :booked_seats, :total_amount, :status, :created_at

  def initialize(id, user, show, booked_seats, total_amount)
    @id = id
    @user = user
    @show = show
    @booked_seats = booked_seats
    @total_amount = total_amount
    @status = :pending
    @created_at = Time.now
  end

  def confirm
    @status = :confirmed
  end

  def expire
    @status = :expired
  end
end

# --- BOOKING SERVICE ---
class BookingService
  def initialize
    @locks_mutex = Mutex.new
    @show_locks = {}
    @bookings = {}
  end

  # Fetch or initialize a fine-grained mutex for each individual show
  def get_show_lock(show_id)
    @locks_mutex.synchronize do
      @show_locks[show_id] ||= Mutex.new
    end
  end

  def create_booking(user, show, seat_ids)
    booking_id = SecureRandom.uuid
    show_lock = get_show_lock(show.id)

    show_lock.synchronize do
      seats_to_lock = []
      show_seat_map = show.show_seats

      # Validate
      seat_ids.each do |seat_id|
        show_seat = show_seat_map[seat_id]
        if show_seat.nil? || !show_seat.available?
          raise "Seat #{seat_id} is not available!"
        end
        seats_to_lock << show_seat
      end

      # Lock seats temporarily (e.g. 5 seconds for simulation)
      total_amount = 0.0
      seats_to_lock.each do |show_seat|
        show_seat.lock(booking_id, 5)
        total_amount += show_seat.seat.base_price
      end

      booking = Booking.new(booking_id, user, show, seats_to_lock, total_amount)
      @bookings[booking_id] = booking
      booking
    end
  end

  def confirm_payment(booking_id)
    booking = @bookings[booking_id]
    raise "Booking not found!" if booking.nil?

    show_lock = get_show_lock(booking.show.id)
    show_lock.synchronize do
      if booking.status != :pending
        raise "Booking is not in pending status!"
      end

      # Double check lock validity
      has_expired = false
      booking.booked_seats.each do |show_seat|
        if show_seat.locked_by_booking_id != booking_id || show_seat.status != :locked
          has_expired = true
          break
        end
      end

      if has_expired
        booking.expire
        raise "Payment completed too late; seats have been released!"
      end

      booking.booked_seats.each(&:book)
      booking.confirm
      puts "Booking #{booking_id} successfully CONFIRMED!"
    end
  end

  def handle_lock_expiration(booking_id)
    booking = @bookings[booking_id]
    return if booking.nil? || booking.status != :pending

    booking.booked_seats.each do |show_seat|
      show_seat.unlock if show_seat.locked_by_booking_id == booking_id
    end
    booking.expire
    puts "Booking #{booking_id} has EXPIRED. Seats released."
  end
end

# --- RUNNING CONCURRENT SIMULATION ---
if __FILE__ == $0
  # Init data
  movie = Movie.new("m-1", "Interstellar", 169)
  seats = [
    Seat.new("s1", "A", 1, :gold),
    Seat.new("s2", "A", 2, :gold),
    Seat.new("s3", "B", 1, :silver)
  ]
  screen = Screen.new("scr-1", "Audi-1", seats)
  theatre = Theatre.new("t-1", "IMAX Bangalore", "Bangalore")
  theatre.add_screen(screen)

  show = Show.new("sh-1", movie, screen, Time.now + 7200)
  booking_service = BookingService.new

  user_alice = User.new("u-1", "Alice", "alice@test.com")
  user_bob = User.new("u-2", "Bob", "bob@test.com")

  seats_to_book = ["s1", "s2"]

  # Concurrent booking threads
  t1 = Thread.new do
    begin
      booking = booking_service.create_booking(user_alice, show, seats_to_book)
      puts "Alice successfully locked seats. Booking ID: #{booking.id}"
      sleep(1) # simulate paying time
      booking_service.confirm_payment(booking.id)
    rescue => e
      puts "Alice booking failed: #{e.message}"
    end
  end

  t2 = Thread.new do
    begin
      sleep(0.2) # wait slightly for thread ordering
      booking = booking_service.create_booking(user_bob, show, seats_to_book)
      puts "Bob successfully locked seats. Booking ID: #{booking.id}"
      booking_service.confirm_payment(booking.id)
    rescue => e
      puts "Bob booking failed: #{e.message}"
    end
  end

  t1.join
  t2.join
end
```

---

## 8. Deep-Dive Interview Questions & Answers

### Q1: How do you handle database persistence and database-level concurrency?
* **Pessimistic Locking (`SELECT FOR UPDATE`):** When querying the status of show-seats, we lock the rows corresponding to those `seat_ids` and `show_id` in the database. No other transaction can read/update them until our transaction commits.  
  *Pros:* 100% guarantee against double bookings at the database level.  
  *Cons:* Can cause connection pools to deplete under heavy load, as locks are held until payment begins or transactions finish.
* **Optimistic Locking (Versioning):** Each `ShowSeat` row has a `version` field. When updating the seat status, we verify:  
  `UPDATE show_seats SET status = 'LOCKED', version = version + 1 WHERE id = :id AND version = :current_version`.  
  If the row was modified, update fails and we retry. Highly recommended if seat conflicts are relatively low (e.g. users select different seats in most scenarios).

### Q2: What happens if the booking server crashes after locking seats but before payment completion?
Using **Lazy Expiration** resolves this gracefully. We do not need a cron or daemon to clean up in-memory or database states instantly. When the next user requests availability for those seats, the application checks if `Time.now > lock_expires_at` and automatically releases them back to `AVAILABLE`. 

Alternatively, a distributed worker (e.g. using Redis keys with expirations, or RabbitMQ delayed queues) can trigger a cleanup event after 5 minutes to release the lock explicitly in the database.

### Q3: How do we scale search (read heavy) vs. booking (write heavy)?
1. **Search Scaling:** Movie catalogs, show listings, and screen configurations are relatively static. We can aggressively cache theatre structures and showtimes in Redis. Show listings can be queried directly from read-replicas.
2. **Booking Scaling:** Booking demands high write throughput. We can shard the `bookings` and `show_seats` tables by `show_id` or `theatre_id`. Since all updates happen within the scope of a single show, sharding by `show_id` prevents cross-shard transactions, keeping operations lightning fast.
