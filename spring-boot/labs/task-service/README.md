# Follow a real Spring request

This is an isolated training app: Java 21, the included Maven 3.9.9 wrapper, Spring Boot 4.0.3, and in-memory H2. It binds to localhost:8081. Nothing here reads or connects to the work application.

From this folder (the first run downloads Maven and dependencies from Maven Central):

```sh
./mvnw test
./mvnw spring-boot:run
curl http://127.0.0.1:8081/ping
curl -u alice:training-only http://127.0.0.1:8081/tasks
```

The two local demo users are alice and bob. The password is training-only. These are public synthetic credentials, intentionally local to this disposable app. CSRF stays enabled. The tests show authenticated POSTs both with and without its token. Do not deploy this setup.

Read the tests before the implementation. Predict which ones reach the service. Put a breakpoint at controller → service → repository. Check which bean is a transaction proxy. Change one boundary at a time and observe the failure.

The app saves a completion intent in an outbox table. It does not actually send messages or include a production outbox dispatcher. Repeated sequential completion saves one intent. Concurrent conflicts need deliberate client error handling and a concurrency test; the unique event key and optimistic version are safeguards, not a polished conflict API. The list is intentionally unpaginated for the small lab; add a bound and stable paging as practice.

H2 tests are useful here. They do not establish PostgreSQL locking, migration safety, or production performance. Add PostgreSQL integration tests in a separate training environment before relying on those guarantees.

Exercises by module:

1. Startup: change port via file and command line; explain the winner.
2. DI: add a fake notification boundary and unit-test it without Spring.
3. HTTP: add a missing-resource and malformed-JSON test.
4. JPA: introduce owners and show the N+1 query count before repairing it.
5. Transactions: force failure after intent creation; verify both changes roll back.
6. Security: try another owner and prove no write occurred.
7. Testing: separate a pure policy test from a real HTTP/database test.
8. Operations: add a slow fake provider, limited retry, request ID, and a short recovery note.
