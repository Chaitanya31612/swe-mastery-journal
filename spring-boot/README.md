# Java · Spring Boot

Beginner builds the model. Intermediate adds real constraints, failure cases, and tradeoffs. Follow the sequence below. Folder names and module IDs stay stable for saved progress.

## Beginner

- 01. [What runs when Spring Boot starts?](01-spring-startup/README.md): Explain how main(), the container, configuration, and the web server fit together.
- 02. [Beans, constructors, and shared state](02-spring-dependencies/README.md): Trace who creates a service and why singleton fields must be safe across requests.
- 03. [From HTTP input to a useful error](03-spring-http/README.md): Trace request binding, validation, service work, and response mapping.
- 04. [Who are you, and may you do this?](06-spring-security/README.md): Separate authentication, ownership checks, CSRF, and CORS.

## Intermediate

- 05. [JPA: Java objects are not SQL](04-spring-persistence/README.md): Explain entity state, repository queries, lazy reads, and the N+1 problem.
- 06. [Transactions, proxies, and races](05-spring-transactions/README.md): Predict whether a transaction starts and design one test that catches a race.
- 07. [Test decisions, wiring, and real SQL separately](07-spring-tests/README.md): Pick the smallest test that can catch each failure without hiding infrastructure differences.
- 08. [Ship and debug a small service](08-spring-operate/README.md): Trace a failed request and explain configuration, timeouts, retries, and safe operation.
- 09. [Configuration you can explain in every environment](09-spring-configuration/README.md): Bind and validate configuration, separate secrets, and diagnose which setting actually won.
- 10. [REST contracts: pages, retries, and useful conflicts](10-spring-api-contracts/README.md): Design bounded APIs and idempotent command handling with explicit retry behavior.
- 11. [SQL plans, connection pools, and transaction size](11-spring-data-performance/README.md): Investigate a slow service without assuming more threads or caching is the first fix.
- 12. [Remote calls: timeouts, retries, and unknown outcomes](12-spring-integration-resilience/README.md): Bound dependency work and design retries around a logical command rather than an exception name.
- 13. [Use-case boundaries and practical modular design](13-spring-modular-usecases/README.md): Separate transport, business rules, persistence, and external adapters without creating needless layers.
- 14. [Integration tests, migrations, and a release rehearsal](14-spring-release-testing/README.md): Prove the deployed configuration, database changes, and failure recovery beyond mock tests.
