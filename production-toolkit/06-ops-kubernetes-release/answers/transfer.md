## One valid transfer

Stop taking new work, handle in-flight work within a bounded grace period, and commit acknowledgement only after the durable effect. Expect repetition after forced termination and make it safe. Test shutdown at the effect/ack gap.

A different answer can work if it meets the stated rule. Explain the failure timeline and the tradeoff. A product name or a longer answer is not proof.
