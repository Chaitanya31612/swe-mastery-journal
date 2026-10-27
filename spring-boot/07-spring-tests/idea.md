# The idea

A unit test checks a small piece of behavior using ordinary objects and controlled dependencies. It should be quick. A web test checks HTTP binding, validation, status, and JSON. An integration test checks actual wiring or external boundaries.

Do not load the entire application for every arithmetic or ownership rule. Do not use only mocks to claim that SQL, transactions, and bean discovery work. Use a small number of database tests against the database type you rely on for concurrency and constraints.

Test observable behavior. A good failure test names what must not happen: a denied request must not write, a failed transaction must not leave half a change, and a duplicate command must not charge twice.
