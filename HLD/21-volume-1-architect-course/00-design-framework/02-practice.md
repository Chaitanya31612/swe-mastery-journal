# Framework practice — no solutions here

## P1 — Narrow the prompt before choosing components

“Design a service for sharing study notes.” Assume 100,000 daily users, each creating one 2 KB note and reading 20 notes/day. Make explicit choices for ownership, sharing, edits, deletion freshness, and availability. Use the seven verbs. Spend 35 minutes on the design and 10 on a changed requirement: one note becomes publicly viral.

Deliver: a bounded contract, estimates that affect choices, API/data, two flows, two deep dives, and a summary of alternatives. No product list without reasons.

## P2 — Complete a partially guided problem

A background PDF-export service receives 10,000 requests/day. Exports take 20 seconds of worker time, spikes reach 30 requests/s, and users can wait up to five minutes. Some export requests are retries of the same action. Fill the missing reasoning: what does “accepted” mean; where does identity live; what limits parallelism; how do users retrieve results; what happens after a crash? Do not merely draw the boxes suggested by the nouns.

## P3 — Critique a bad proposal

“Use microservices, Kafka, Redis, sharding, and two regions for the notes app. That guarantees scaling and availability. We can skip requirements because everyone knows how notes work.” Identify at least five unsupported assumptions or missing mechanisms. Write a simpler starting design and conditions under which you would evolve it.

## Delayed transfer

After at least a week, spend ten minutes organizing a design for a document conversion service without looking at the framework. Record missing steps before checking your notes.
