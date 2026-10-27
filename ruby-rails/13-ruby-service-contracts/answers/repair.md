## One valid repair

Separate expected business results from unexpected failures and give callers a small explicit result/error policy. Preserve operational exceptions for monitoring.

Test each caller’s visible response and assert no partial writes on failure.

A different answer can work if it meets the stated rule. Explain the failure timeline and the tradeoff.

A product name or a longer answer is not proof.