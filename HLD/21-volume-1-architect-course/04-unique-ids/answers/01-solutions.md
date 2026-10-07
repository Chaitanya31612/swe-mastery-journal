# Unique IDs: clocks, coordination, and order — solutions

Open after saving your attempt. These are defensible reference arguments, not the only valid designs. Check alternatives against the stated contract.

## P1 — Conditional design

A time/worker/sequence layout is defensible for rough time sorting if worker identities are uniquely assigned/fenced, clocks/restarts are handled, and rates are backpressured on exhaustion. At uniform peak the mean is about 1,563 IDs/s/worker, far below the nominal 4,096/ms sequence space; nonuniform bursts and measured implementation limits still matter. Keep region allocation disjoint or use a coordinated worker registry. State time/worker information leakage and avoid treating IDs as secrets.

Random IDs plus store uniqueness can be an alternative if time sorting is stored separately. A central/range allocator is another option if dependencies and number gaps are acceptable. There is no requirement to copy a particular book layout exactly.

## P2 — Stronger numbering

Use one authoritative ordered allocation/commit protocol with appropriate durability/leadership/fencing. Explain whether assignment occurs before or at commit, whether gaps are permitted, and how failures affect returned numbers. Partition tolerance and always-available strict global numbering cannot be assumed simultaneously. Independent physical clocks or more sequence bits do not coordinate the order.

## P3 — Repair the state machine

Two workers with the same identity can emit equal fields. More than 4,096 emissions in one millisecond wrap sequence values; clock rollback/restart can repeat past tuples. Validate leased worker ownership, compare to last emitted time, reset sequence only when time advances safely, and wait/fail on rollback or exhausted time slots. Persist/fence restart state or establish a safe new identity/epoch policy. A synchronized method alone fixes only local threading, not copied worker identity or rollback.

## Checkpoint explanations

1. **B.** B is the bounded claim. A requires stronger order reasoning; C/D are unrelated guarantees.

2. **C.** C preserves the uniqueness contract. A/D violate it; B worsens independent collisions.

3. **D.** Physical-clock assumptions need failure handling. Bit size/worker count do not prove monotonic clock behavior.

4. **A.** A is the mechanism. B is not guaranteed; C permits reuse; D is a separate concern.

## After feedback

Preserve your first attempt. Record one counterexample, repair the missing mechanism, and reattempt after a delay. Do not mark independence from an open-book repair.
