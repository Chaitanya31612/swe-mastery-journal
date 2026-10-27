## Understand the idea

A unit suite can pass while the real application has the wrong bean, migration, permission, or SQL behavior. Keep focused integration tests for the boundaries you rely on.

Use a disposable real database when engine behavior matters.

A release changes code, configuration, and sometimes data. Old and new instances may overlap.

A migration should remain compatible during that overlap. A code rollback does not restore deleted data or unsend messages.

Rehearse a small release with a known failure. Observe readiness, startup migration ownership, graceful shutdown, in-flight requests, and a rollback decision.

A runbook is a short path from symptom to check to safe action to verification.