# Unique IDs: clocks, coordination, and order — practice

Save your attempt before opening answers. Label assistance and previous exposure. Use the seven-part framework; explain assumptions and consequences.

## P1 — Two-region ID generation

Generate opaque record IDs at 100,000/s peak across 64 workers in two regions. IDs must be unique and roughly time-sortable; strict global order is unnecessary. Choose a scheme and show worker ownership, time rollback, restart, sequence exhaustion, and failure behavior. State whether IDs reveal time/location information.

## P2 — Strict ticket numbering

Change the contract: committed tickets must receive strictly increasing global numbers. Explain the coordination/availability trade-off and why changing bit counts cannot solve it.

## P3 — Fix bad pseudocode

```text
timestamp = wall_clock_ms()
sequence = (sequence + 1) & 4095
return (timestamp << 22) | (worker_id << 12) | sequence
```

Worker IDs are copied from the same image configuration. No last timestamp is retained. Trace duplicate-producing executions and propose a safe state machine.

## Delayed gate

Explain a duplicate after restart and distinguish roughly sorted IDs from a strict global ticket sequence.
