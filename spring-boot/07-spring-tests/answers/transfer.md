# One valid adaptation

Use a fake provider that records acceptance, then throws a timeout. Retry with the same idempotency key and verify only one logical effect. Also test eventual failure and user-visible status. Keep one separate provider contract test if you own that integration.

**Explain back:** Test at the layer where the bug can live. What changed in the new condition? What would make your answer fail?
