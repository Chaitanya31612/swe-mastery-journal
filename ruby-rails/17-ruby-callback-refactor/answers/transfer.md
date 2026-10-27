## One valid transfer

Define whether the maintenance action should create those effects. If yes, use an explicit batch use case/outbox path with idempotent progress.

If no, document the intentional bypass and test the state it leaves. Do not assume every SQL update should send user notifications.

A different answer can work if it meets the stated rule. Explain the failure timeline and the tradeoff.

A product name or a longer answer is not proof.