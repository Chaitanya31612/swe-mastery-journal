# Follow the execution

Controller → proxy → begin → service → SQL → commit → return. If an unchecked exception leaves the service, the wrapper rolls back instead.

For a race, draw A reads 1, B reads 1, A writes 0, B writes 0. Both callers may believe they won. A transaction annotation alone does not prevent this lost update. Conditional updates or optimistic version checks turn the second attempt into a visible conflict.
