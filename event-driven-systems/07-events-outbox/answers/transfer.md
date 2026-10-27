## One valid transfer

It can resend E under the same event_id. The consumer must deduplicate its effect transactionally. Do not mark first to avoid duplicates, because that reintroduces lost delivery.

A different answer can work if it meets the stated rule. Explain the failure timeline and the tradeoff. A product name or a longer answer is not proof.
