## One valid repair

Give each independent subscriber a queue and fan out the event to both, with explicit policies and schema. Keep competing workers only within the same subscriber role. Test that one event reaches both logical consumers.

A different answer can work if it meets the stated rule. Explain the failure timeline and the tradeoff. A product name or a longer answer is not proof.
