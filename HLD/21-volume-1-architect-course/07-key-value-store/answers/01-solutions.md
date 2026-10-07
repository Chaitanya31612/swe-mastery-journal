# Distributed key-value stores and honest consistency claims — solutions

Open after saving your attempt. These are defensible reference arguments, not the only valid designs. Check alternatives against the stated contract.

## P1 — Preference design

Raw data is 10 GB decimal; three full copies make 30 GB before indexes/logs/overhead/history. Use partitioned ownership with distinct failure-domain replicas and a coordinator whose consistency policy is explicit. A leader-based log plus writer/session progress tokens is one option for read-your-writes; other devices can use bounded-lag replicas when observed progress supports the 30-second promise. If lag exceeds the bound, route authoritatively or degrade according to contract rather than silently serving arbitrary stale state.

A multi-writer version/conflict model is another option if the UI resolves concurrent preferences or defines field-level merges. Durable ack, bounded repair, and backup restore must be specified. QPS figures require benchmark/skew/size analysis; they do not determine exact node count.

## P2 — Stronger invariant

Use a fenced authoritative leader/transactional conditional update for each inventory ownership unit or a documented distributed conditional protocol. Only an owner with valid authority may commit decrements. A partitioned minority can reject/wait rather than violate stock. If using independently allocated inventory budgets, prove disjoint ownership and avoid double-spending during transfer. Eventual last-write-wins can overwrite one decrement rather than preserve both, so it does not enforce the inventory contract.

## P3 — Missing proof

Concurrent writes can have conflicting versions; client clock skew can make an older logical effect look newer; sloppy membership/replica sets may break the assumed intersection; acknowledgment durability may be insufficient. Specify ordering/version reads, authority/membership/fencing, and persistent acknowledgment before claiming a particular consistency model. R+W>N is a condition in a model, not a complete algorithm.

## Checkpoint explanations

1. **B.** B is the set property. A/C/D require additional mechanisms/assumptions.

2. **C.** Volatile state can disappear. A/B/D are unsupported without persistence/replicas and recovery.

3. **D.** Detection is not semantic reconciliation. A/B discard the issue; C supplies placement not meaning.

4. **A.** A addresses a different failure. B/C/D misstate the roles.

## After feedback

Preserve your first attempt. Record one counterexample, repair the missing mechanism, and reattempt after a delay. Do not mark independence from an open-book repair.
