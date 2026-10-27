## Trace the execution

Controller validates permitted input and identifies actor → service checks the use-case rule → transaction writes → result maps to HTTP.

A job caller uses the same rule with a deliberate actor/system role.

Unit-test expected branches with a narrow seam. Use database tests for rollback and constraints.

Test the caller’s mapping so a failure is not shown as a success response.