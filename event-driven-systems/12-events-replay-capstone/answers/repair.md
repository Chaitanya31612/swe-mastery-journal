## One valid repair

Use a new versioned projection/inbox identity or a controlled consistent rebuild of both, with clear read cutover and rollback. Verify old/new schema compatibility and retained history.

Do not delete dedup state without understanding external effects.

A different answer can work if it meets the stated rule. Explain the failure timeline and the tradeoff.

A product name or a longer answer is not proof.