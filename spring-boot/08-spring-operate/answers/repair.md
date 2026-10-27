# One valid repair

Measure provider latency, attempt count, queue depth, and thread/connection use. Bound timeouts and retry attempts; retry only safe operations. Use backoff and isolate the failing dependency. Preserve pending intent and expose status rather than blocking indefinitely. Verify with a controlled slow fake.

**How to check:** The provider may have completed the action before the response was lost. Treat the outcome as uncertain.

Other repairs are acceptable if they satisfy the stated rule. Explain the failure timeline and show a relevant test. Code length and matching keywords are not evidence.
