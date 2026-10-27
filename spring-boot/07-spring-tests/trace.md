# Follow the execution

First make the test fail for the right reason. Then change the implementation. For a bug in JSON validation, a service mock alone cannot see the problem; exercise MVC. For a missing unique index, an in-memory repository fake cannot see it; test the database.

Avoid asserting exact private method order when the contract allows alternatives. Control time and remote responses. Race tests need controlled overlap; random sleeps create flaky evidence.
