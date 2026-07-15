# Booking System

## Problem statement
Develop a booking system that allows users to book movies like bookmyshow

## Requirements

### Must Haves
- movies, theaters and timings
- browse by movies - for a movie show all the theaters and timings for a particular day
- browse by theater - show all movies and timings for a particular theater
- movies catalog
- each movie listing has many theaters
- a theater have many screens
- a screen has many seats
- screen has many timings and movies throughout the day
- a theater can book a seat for a particular movie at a particular timing
- slot has theater, screen, timing, movie
- theater can book multiple slots
- selecting seats and proceeding creates a booking (temp) with a unique booking id and set a TTL of 10minutes, if not confirmed within 10 minutes, the booking is cancelled and seats are released
- States for seats - Booked, Available, Pending
- States for booking - Confirmed, Cancelled, Pending, Expired
- States for payment - Paid, Unpaid, Refunded


### Nice to haves / out of scope
- Payment processing and refund
- authentication
- QR code for booking
- email notifications and reminders
- cancellation

### Flow

App -> Movies Catelog -> Select a Movie -> Theatres Catelog -> Select a Theater -> Multiple slots (screen, timings) -> Select a slot -> Select seats -> Confirm booking -> Seats are locked (has a booking id and TTL of 10 minutes) > Redis store transient booking data -> payment processing -> payment is successful -> booking is confirmed
-> payment failed -> booking is cancelled -> Refunded
-> payment successful but completed after 10 minutes -> lets fail and cancel the booking -> refund

## Classes

### Entities
- Movie (class)
  - is: entity representing a movie
  - knows: title, duration
  - does: nothing
- Theater
  - is: entity representing a theater
  - knows: name, location, screens, slots
  - does: nothing
- Screen
  - is: entity representing a screen
  - knows: seats (list)
  - does: availableSeats, markSeatAsBooked, markSeatAsAvailable
- Seat
  - is: entity representing a seat
  - knows: row, column, bookingId
  - does: isBooked
- Slot
  - is: join entity between theater, screen, movie and time
  - knows: movie, theater, screen, time, startDate, endDate
  - does: bookSeats
- Booking
  - is: entity representing a booking
  - knows: slot, seats, booking_id, status, payment_id
  - does: isConfirmed, isCancelled
- BookingService
  - is: service responsible for booking seats
  - knows: movies, theaters
  - does: getMovies, getTheaters, getSlots(theaterId), bookSeats(slotId, seats)

Booking Controller
get list of movies
selected a movie
get list of theaters for that movie
selected a theater
get the slots for that theater
slot show the time, screen etc for the movie in the theater
selected a slot
get available seats for that slot
selected seat(s)
book the seats
 - creates a booking entity
 - those seats are marked as booked in the screen and stored in redis for quick retrieval
 - the booking entity is stored in the database
 - the booking is confirmed and the user is notified, status is updated to confirmed


### Questions about concurrency

- so what if two or more users try to book the same seat at the same time?
- and they can get the two bookings created and whichever is completed last gets the seat marked as booked -> not ideal
- check then act
- so we can make the entire book method synchronized
- this will ensure that only one thread can execute the book method at a time, preventing concurrent bookings of the same seat
- other options are
- we check the seat's availability before booking
- inside that block we add synchronized block, and check again inside the synchronized block before booking


```java

public class BookingController {
  public static void main(String[] args) {
    BookingService bookingService = new BookingService();

    Movie movie1 = new Movie("Jungle Book", 120, TimeUnit.MINUTES);
    Movie movie2 = new Movie("Jurassic Park", 150, TimeUnit.MINUTES);
    bookingService.addMovie(movie1);
    bookingService.addMovie(movie2);

    // theaters
    Theater theater1 = new Theater("Theater 1");
    bookingService.addTheater(theater1);

    // slots
    Slot slot1 = new Slot()
                  .setMovie(movie1)
                  .setTheater(theater1)
                  .setTime(1000)
                  .setStartDate(LocalDate.of(2026, 06, 1));
    Slot slot2 = new Slot()
                  .setMovie(movie1)
                  .setTheater(theater1)
                  .setTime(1500)
                  .setStartDate(LocalDate.of(2026, 06, 1));
    Slot slot3 = new Slot()
                  .setMovie(movie2)
                  .setTheater(theater1)
                  .setTime(2000)
                  .setStartDate(LocalDate.of(2026, 06, 1));
    bookingService.addSlot(slot1);
    bookingService.addSlot(slot2);
    bookingService.addSlot(slot3);
    
    // movies
    List<Movie> movies = bookingService.getMovies();
    System.out.println("Movies: " + movies);

    // movie to book
    Movie movieToBook = movies.get(0);
    System.out.println("Movie to book: " + movieToBook);
    
    // theaters
    List<Theater> theaters = bookingService.getTheaters(movieToBook);
    System.out.println("Theaters: " + theaters);

    // slots
    List<Slot> slots = bookingService.getSlots(theaters.get(0));
    System.out.println("Slots: " + slots);

    // available seats in that slot
    Slot choosenSlot = slots.get(0);
    System.out.println("Choosen Slot: " + choosenSlot);

    List<Seat> availableSeats = choosenSlot.getAvailableSeats();
    System.out.println("Available Seats: " + availableSeats);

    // book a seat
    List<Seat> seatsToBook = availableSeats.subList(0, 1);
    System.out.println("Seat to book: " + seatsToBook.get(0));

    // book the seat
    Booking booking = bookingService.bookSeat(choosenSlot, seatsToBook);
    System.out.println("Booking: " + booking.status);

    System.out.println("Booking ID: " + booking.bookingId);

    // check available seats again
    List<Seat> updatedAvailableSeats = choosenSlot.getAvailableSeats();
    System.out.println("Updated Available Seats: " + updatedAvailableSeats);
    
  }
}











```
