# Transfer assessment and graduation evidence — practice

Save your attempt before opening answers. Label assistance and previous exposure. Use the seven-part framework; explain assumptions and consequences.

## P1 — Three 45-minute unaided rounds

**Round A: package artifact registry.** Teams publish versioned packages and download by tenant/name/version. Assume one million downloads/day, 50,000 publishes/day, mean artifact 10 MB. Versions are immutable; a compromised version must stop being newly downloaded within five seconds. Clarify scope, then design. At minute 30 change the load: one package receives half the downloads.

**Round B: data import jobs.** Accept CSV imports up to 1 GB and report row-level failures. Assume 20,000 jobs/day; retrying submission must not create duplicate logical jobs. Some customers have two imports updating the same records. At minute 30 a worker crashes after a batch commit but before recording progress.

**Round C: scarce appointment slots.** Many clients claim the same available slot across four instances. Confirmation must not double-book; cancellation and ten-minute holds are supported. At minute 30 a hold expiry races with confirmation. Use your own explicit scale/latency assumptions.

Record prior exposure. If a prompt is familiar, replace it via a coach without previewing its solution. Submit each first attempt before reviewing its answer.

## P2 — Real-system evidence

Finalize module 15’s observed architecture review. Explain one justified improvement and a staged verification/rollback plan. Show how evidence would change your hypothesis.

## P3 — Evaluate a false completion claim

“I read all chapters, got 90% MCQs, and matched every diagram with hints. Therefore I can independently solve any HLD interview.” State what evidence is missing and write a narrower honest statement.

## Delayed gate

After two weeks, organize a new problem from memory, identify the central invariant, and justify the two highest-priority deep dives.
