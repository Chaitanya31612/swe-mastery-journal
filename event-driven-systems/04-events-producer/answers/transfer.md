## One valid transfer

No. Enforce one logical completion/outbox event at the authority boundary and use stable event IDs with consumer deduplication. Producer retry idempotence does not infer business sameness from two independent calls.

A different answer can work if it meets the stated rule. Explain the failure timeline and the tradeoff. A product name or a longer answer is not proof.
