## One valid transfer

Bound concurrency, retain per-file outcomes, support cancellation, and use stable upload identities for retries. Progress should count completed files/bytes deliberately.

A single Promise.all over all uploads is not a backpressure strategy.

A different answer can work if it meets the stated rule. Explain the failure timeline and the tradeoff.

A product name or a longer answer is not proof.