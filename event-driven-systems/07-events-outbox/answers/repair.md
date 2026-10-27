## One valid repair

Save the event intent with the state change in the DB transaction. Publish only committed outbox rows later. Keep stable IDs and duplicate-safe consumers. Test rollback leaves neither completion nor outbox event.

A different answer can work if it meets the stated rule. Explain the failure timeline and the tradeoff. A product name or a longer answer is not proof.
