# Distributed key-value stores and honest consistency claims — practice

Save your attempt before opening answers. Label assistance and previous exposure. Use the seven-part framework; explain assumptions and consequences.

## P1 — Preference store

Ten million keys, 1 KB values, 20,000 reads/s, 2,000 writes/s, three replicas. Preferences may lag up to 30 seconds for other devices; users should see their own acknowledged changes. Design partitioning, read/write acknowledgment, conflict policy, and repair. Estimate raw stored copies, not total production footprint.

## P2 — Change the contract

Use the same infrastructure for “decrement stock only if positive.” Explain why eventual merging or quorum arithmetic alone may fail. Choose a mechanism with a clear authoritative conditional-update guarantee and trace a network partition.

## P3 — Critique the guarantee

“N=3, W=2, R=2 means linearizability forever. We can use last-write-wins from each client’s wall clock and change membership independently.” Construct a counterexample or missing assumption and specify what must be added.

## Delayed gate

State what quorum overlap proves and what it does not. Trace stock decrement under a two-versus-one partition.
