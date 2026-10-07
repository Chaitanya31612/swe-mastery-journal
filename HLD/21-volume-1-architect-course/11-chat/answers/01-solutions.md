# Chat: durable acceptance, live delivery, and reconnects — solutions

Open after saving your attempt. These are defensible reference arguments, not the only valid designs. Check alternatives against the stated contract.

## P1 — Model and capacity

Messages average about 116/s and peak 1,157/s. Raw 90-day bodies occupy `10e6 × 90 × 4,000` = 3.6 TB decimal before metadata/copies/indexes. Connection sizing requires per-connection buffers/memory and gateway measurements; average message QPS alone is insufficient.

Use membership-authorized conversations, durable message append with scoped request deduplication, and per-conversation sequence/ownership. Gateway registration is soft routing state. Ack acceptance after the specified durable boundary, then deliver; retain per-device or appropriately modeled user/device cursors and receipt states. Offline devices catch up through history; push is not the history authority. Drain gateways and rate-limit reconnect/send bursts. A lost response after append returns the prior message on retry.

## P2 — Broadcast capacity

100,000 × 10 gives one million recipient-message deliveries/s before retries; at 4 KB each this is about 4 GB/s raw if that payload applies. A hierarchy/partitioned gateway fan-out, compact event references where appropriate, bounded per-device buffers, drop/disconnect-and-catch-up policy, and durable room history can separate serving from storage. Slow consumers cannot be buffered without limit. Explicitly choose receipt/order semantics; avoid a global synchronous acknowledgment from every recipient.

## P3 — Repair

Multiple messages can share one millisecond; clock order is not safe across writers. A successful socket call does not establish durable storage or device processing. Authenticate, assign/deduplicate request identity, append under the conversation’s ordering protocol, acknowledge accepted state, then attempt live delivery. Recipient acknowledgment and catch-up cursor are separate states. Use a durable store/log and fenced ownership if the selected ordering model requires it.

## Checkpoint explanations

1. **D.** D is the bounded claim. A/B/C need other mechanisms.

2. **A.** A links retries to the committed message. B duplicates; C misses server state; D concerns online approximation.

3. **B.** B describes failure detection uncertainty. A overpromises; C/D confuse states.

4. **C.** Live resource state matters. A/B/D alone cannot size or protect gateways.

## After feedback

Preserve your first attempt. Record one counterexample, repair the missing mechanism, and reattempt after a delay. Do not mark independence from an open-book repair.
