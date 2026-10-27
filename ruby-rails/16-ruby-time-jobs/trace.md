## Trace the execution

Scheduler tick → compute intended business period → claim unique run → snapshot/request work → job retries → durable completion state. If a process crashes after claiming, define how a stale in-progress run is retried or repaired.

Test a late scheduler, duplicate trigger, a DST boundary, and a provider timeout. “It ran yesterday” is weak evidence for these cases.
